"""Explicit static-library deployment using Fly Machines HTTPS API.

No raw provider credentials, Docker builder, public upload endpoint or Perplexity
hosting dependency. Run through the approved Fly Machines credential proxy.
"""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import os
import secrets
import shlex
import io
import tarfile
import subprocess
import time
import requests

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT.parent / "openline-fly-deployment"
STATE.mkdir(exist_ok=True)
API = "https://api.machines.dev/v1/apps/openline-brand"
OLD = "8d7155be3ed118"
VOLUME = "vol_re1q7zyz7wlw2qo4"
SESSION = requests.Session()
SESSION.verify = "/etc/ssl/certs/ca-certificates.crt"

def api(method, path, data=None, timeout=120):
    r = SESSION.request(method, API + path, json=data, timeout=timeout)
    if not r.ok:
        raise RuntimeError(f"Fly {method} {path}: HTTP {r.status_code}: {r.text[:600]}")
    return r.json() if r.content else {}

def save(name, value):
    (STATE / name).write_text(json.dumps(value, indent=2))

def machine_id():
    return json.loads((STATE / "new-machine.json").read_text())["id"]

def execute(cmd, stdin="", timeout=60):
    response = api("POST", f"/machines/{machine_id()}/exec",
                   {"cmd": cmd, "stdin": stdin, "timeout": timeout}, timeout=timeout+30)
    if response.get("exit_code"):
        raise RuntimeError(f"Remote command failed: {response.get('stderr', '')[:500]}")
    return response

parser = argparse.ArgumentParser()
parser.add_argument("operation", choices=["stage", "prepare-transfer", "probe", "upload", "verify-upload", "upload-delta", "activate", "status", "exec"])
parser.add_argument("--command")
args = parser.parse_args()

if args.operation == "stage":
    if (STATE / "new-machine.json").exists():
        raise SystemExit("Stage already recorded; inspect before creating anything else.")
    old = api("GET", "/machines/" + OLD)
    assert old["config"]["metadata"]["openline.purpose"] == "brand-launch-studio"
    save("old-machine-before.json", old)
    nginx = (ROOT / "hosting/library-nginx.conf").read_text().replace(
        "/usr/share/nginx/html", "/data/current")
    config = {
        "image": old["config"]["image"],
        "guest": {"cpu_kind": "shared", "cpus": 1, "memory_mb": 256},
        "init": {"exec": ["/bin/sh", "-c", "nginx -t && exec nginx -g 'daemon off;'"]},
        "files": [{"guest_path": "/etc/nginx/conf.d/default.conf",
                   "raw_value": base64.b64encode(nginx.encode()).decode()}],
        "mounts": [{"volume": VOLUME, "path": "/data"}],
        "restart": {"policy": "always"},
        "metadata": {"openline.purpose": "brand-library", "openline.version": "2.0.0"},
        "services": [],
    }
    result = api("POST", "/machines", {
        "name": "openline-brand-library", "region": "cdg", "config": config})
    save("new-machine.json", result)
    print(json.dumps({k: result.get(k) for k in ("id", "name", "state", "region")}))
elif args.operation == "prepare-transfer":
    old = json.loads((STATE / "old-machine-before.json").read_text())
    url = shlex.quote(old["config"]["env"]["BUNDLE_URL"])
    sha = old["config"]["env"]["BUNDLE_SHA256"]
    assert len(sha) == 64 and all(c in "0123456789abcdef" for c in sha)
    execute("sh -c 'mkdir -p /data/fallback /data/incoming; chown nginx:nginx /data/incoming'")
    execute(f"sh -c \"wget -q -T 60 -O /data/fallback.tar.gz {url}; "
            f"echo '{sha}  /data/fallback.tar.gz' | sha256sum -c - && "
            "tar -xzf /data/fallback.tar.gz -C /data/fallback && "
            "ln -sfn /data/fallback /data/current && rm /data/fallback.tar.gz\"", timeout=90)
    token = secrets.token_urlsafe(48)
    save("transfer-private.json", {"path": "/__brand_transfer_" + token + "/"})
    os.chmod(STATE / "transfer-private.json", 0o600)
    config = api("GET", "/machines/" + machine_id())["config"]
    nginx = (ROOT / "hosting/library-nginx.conf").read_text().replace("/usr/share/nginx/html", "/data/current")
    temporary = f"""
  location ^~ /__brand_transfer_{token}/ {{
    alias /data/incoming/;
    client_max_body_size 32m;
    client_body_timeout 180s;
    client_body_temp_path /data/client-temp;
    dav_methods PUT;
    create_full_put_path on;
    dav_access user:rw group:r;
    limit_except PUT {{ deny all; }}
    access_log off;
  }}
"""
    nginx = nginx.rsplit("}", 1)[0] + temporary + "}\n"
    config["files"] = [{"guest_path": "/etc/nginx/conf.d/default.conf",
                        "raw_value": base64.b64encode(nginx.encode()).decode()}]
    service = old["config"]["services"][0].copy()
    service.update({"autostop": "off", "autostart": True, "min_machines_running": 1})
    service.pop("force_instance_key", None)
    config["services"] = [service]
    save("transfer-machine-private.json", api("POST", "/machines/" + machine_id(), {"config": config}))
    # Serve the old verified site during transfer; retain old Machine as stopped rollback.
    old_config = api("GET", "/machines/" + OLD)["config"]
    old_config["services"] = []
    old_config.pop("checks", None)
    api("POST", "/machines/" + OLD, {"config": old_config})
    api("POST", "/machines/" + OLD + "/stop", {"signal": "SIGTERM", "timeout": "10s"})
    print(json.dumps({"transfer_ready": True, "fallback_verified": sha, "token_printed": False}))
elif args.operation == "probe":
    # One bounded 8 MiB stdin probe; never prints uploaded data.
    data = bytes(8 * 1024 * 1024)
    response = execute("sh -c 'mkdir -p /data/incoming; base64 -d > /data/incoming/probe; wc -c /data/incoming/probe; rm /data/incoming/probe'",
                       base64.b64encode(data).decode(), 60)
    print(json.dumps(response))
elif args.operation == "upload":
    # Streaming gzip avoids another ~1GB local archive and retains all downloads.
    chunk_size = 16 * 1024 * 1024
    transfer = json.loads((STATE / "transfer-private.json").read_text())["path"]
    tar = subprocess.Popen(["tar", "-C", str(ROOT / "dist"), "-czf", "-", "."],
                           stdout=subprocess.PIPE)
    digest = hashlib.sha256()
    count = total = 0
    try:
        while True:
            chunk = tar.stdout.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
            name = f"/data/incoming/part-{count:05d}"
            # Short-lived HTTPS PUT capability, removed before final signoff.
            try:
                response = SESSION.put("https://openline-brand.fly.dev" + transfer + f"part-{count:05d}",
                                       data=chunk, headers={"Content-Type": "application/octet-stream"},
                                       timeout=180)
            except requests.RequestException as error:
                raise RuntimeError("Asset transfer transport failed; private capability URL withheld") from None
            if response.status_code not in (201, 204):
                raise RuntimeError(f"Asset transfer HTTP {response.status_code}; URL withheld")
            total += len(chunk)
            count += 1
            if count % 5 == 0:
                print(json.dumps({"uploaded_mib": round(total / 1048576, 1), "chunks": count}), flush=True)
    finally:
        tar.stdout.close()
    assert tar.wait() == 0
    sha = digest.hexdigest()
    save("upload.json", {"sha256": sha, "bytes": total, "chunks": count})
    print(json.dumps({"uploaded": True, "sha256": sha, "bytes": total, "chunks": count}))
elif args.operation == "verify-upload":
    upload = json.loads((STATE / "upload.json").read_text())
    sha, total, count = upload["sha256"], upload["bytes"], upload["chunks"]
    # Verify transfer before extraction. Explicit glob is restricted to this release's chunks.
    job = (f"set -eu; cat /data/incoming/part-* | sha256sum > /data/transfer.sha256; "
           f"test \"$(cut -d ' ' -f1 /data/transfer.sha256)\" = {sha}; "
           f"mkdir -p /data/releases/{sha}; "
           f"cat /data/incoming/part-* | tar -xzf - -C /data/releases/{sha}; "
           f"test -f /data/releases/{sha}/index.html; "
           f"ln -sfn /data/releases/{sha} /data/current; "
           "rm /data/incoming/part-*; touch /data/install-complete")
    result = execute("sh -c " + shlex.quote(
        "nohup sh -c " + shlex.quote(job) + " </dev/null >/data/install.log 2>&1 & echo started"))
    print(json.dumps({"verification_started": True, "sha256": sha, "bytes": total, "chunks": count}))
elif args.operation == "upload-delta":
    buffer = io.BytesIO()
    paths = [ROOT / "dist/index.html", ROOT / "dist/studio.html"]
    paths += list((ROOT / "dist/assets").glob("*.js"))
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for path in paths:
            archive.add(path, arcname=str(path.relative_to(ROOT / "dist")))
    data = buffer.getvalue()
    transfer = json.loads((STATE / "transfer-private.json").read_text())["path"]
    response = SESSION.put("https://openline-brand.fly.dev" + transfer + "delta.tar.gz",
                           data=data, timeout=60)
    assert response.status_code in (201, 204), response.status_code
    save("delta.json", {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    print(json.dumps({"delta_uploaded": True, "bytes": len(data)}))
elif args.operation == "activate":
    new = api("GET", "/machines/" + machine_id())
    old = api("GET", "/machines/" + OLD)
    assert new["config"]["metadata"]["openline.purpose"] == "brand-library"
    execute("sh -c 'test -f /data/install-complete && test -f /data/current/index.html && test -f /data/current/library/catalog.json && wget -qO- http://127.0.0.1:8080/healthz'")
    if (STATE / "delta.json").exists():
        delta = json.loads((STATE / "delta.json").read_text())
        result = execute("sha256sum /data/incoming/delta.tar.gz")
        assert result["stdout"].split()[0] == delta["sha256"]
        execute("sh -c 'set -eu; tar -xzf /data/incoming/delta.tar.gz -C /data/current; rm /data/incoming/delta.tar.gz'")
    config = new["config"]
    nginx = (ROOT / "hosting/library-nginx.conf").read_text().replace("/usr/share/nginx/html", "/data/current")
    config["files"] = [{"guest_path": "/etc/nginx/conf.d/default.conf",
                       "raw_value": base64.b64encode(nginx.encode()).decode()}]
    service = json.loads((STATE / "old-machine-before.json").read_text())["config"]["services"][0]
    service.update({"autostop": "off", "autostart": True, "min_machines_running": 1})
    service.pop("force_instance_key", None)
    config["services"] = [service]
    config["checks"] = {"web": {"type": "http", "port": 8080, "method": "GET",
                               "path": "/healthz", "interval": "30s", "timeout": "5s",
                               "grace_period": "10s"}}
    config["metadata"]["openline.bundle_sha256"] = json.loads((STATE / "upload.json").read_text())["sha256"]
    # Enable the verified new library, then remove the obsolete origin from routing.
    save("activation.json", api("POST", "/machines/" + machine_id(), {"config": config}))
    if old["config"].get("services"):
        old_config = old["config"]
        old_config["services"] = []
        old_config.pop("checks", None)
        save("old-unrouted.json", api("POST", "/machines/" + OLD, {"config": old_config}))
    if old["state"] != "stopped":
        save("old-stopped.json", api("POST", "/machines/" + OLD + "/stop", {"signal": "SIGTERM", "timeout": "10s"}))
    print(json.dumps({"active_machine": machine_id(), "old_machine_unrouted": OLD,
                      "always_on": True, "volume_gb": 3}))
elif args.operation == "status":
    value = api("GET", "/machines/" + machine_id())
    print(json.dumps({k: value.get(k) for k in ("id", "state", "checks")}))
elif args.operation == "exec":
    if not args.command:
        parser.error("--command required")
    print(json.dumps(execute(args.command, timeout=120)))
