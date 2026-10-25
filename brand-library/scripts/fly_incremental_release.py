"""Incremental, reversible releases on the existing Openline Fly machine.

Control operations use the approved Machines API credential proxy. Upload runs
separately, outside that proxy. Private transfer capabilities never enter dist.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import secrets
import shlex
import subprocess
import tarfile
import requests

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT.parent / "openline-fly-deployment" / "campaign-v2-1"
STATE.mkdir(parents=True, exist_ok=True)
MACHINE = "867543ae795138"
API = f"https://api.machines.dev/v1/apps/openline-brand/machines/{MACHINE}"
SESSION = requests.Session()
SESSION.verify = "/etc/ssl/certs/ca-certificates.crt"

def write(name, value):
    path = STATE / name
    path.write_text(json.dumps(value, indent=2))
    os.chmod(path, 0o600)

def read(name):
    return json.loads((STATE / name).read_text())

def api(method, suffix="", data=None):
    r = SESSION.request(method, API + suffix, json=data, timeout=150)
    if not r.ok:
        raise RuntimeError(f"Fly control HTTP {r.status_code}")
    return r.json()

def execute(command, timeout=90):
    r = api("POST", "/exec", {"cmd": "sh -c " + shlex.quote(command), "timeout": timeout})
    if r.get("exit_code"):
        raise RuntimeError("Remote release operation failed: " + r.get("stderr", "")[:500])
    return r.get("stdout", "")

def nginx_config():
    return (ROOT / "hosting/library-nginx.conf").read_text().replace("/usr/share/nginx/html", "/data/current")

def configure(text):
    encoded = base64.b64encode(text.encode()).decode()
    execute(f"printf %s {shlex.quote(encoded)} | base64 -d > /etc/nginx/conf.d/default.conf; nginx -t && nginx -s reload")

p = argparse.ArgumentParser()
p.add_argument("operation", choices=["bundle", "prepare", "upload", "verify", "status", "activate", "close-transfer", "rollback"])
p.add_argument("--file-list", help="JSON array of dist-relative, public-only files")
p.add_argument("--release-key", default="campaign-v2-1", help="Isolated resumable release state")
a = p.parse_args()
assert all(c.isalnum() or c in "-_" for c in a.release_key)
STATE = ROOT.parent / "openline-fly-deployment" / a.release_key
STATE.mkdir(parents=True, exist_ok=True)

if a.operation == "bundle":
    names = json.loads(Path(a.file_list).read_text())
    names += ["index.html", "studio.html"]
    names += [str(x.relative_to(ROOT/"dist")) for x in (ROOT/"dist/assets").iterdir()
              if x.suffix in (".js", ".css", ".woff", ".woff2")]
    names = sorted(set(names))
    assert names and "index.html" in names and "library/catalog.json" in names
    for name in names:
        path = Path(name)
        assert not path.is_absolute() and ".." not in path.parts
        assert (ROOT / "dist" / path).is_file()
        assert not any(s in path.parts for s in ("private", "_private", "receipts", "requests", ".git", "node_modules"))
    assert all("\n" not in name for name in names)
    (STATE / "transfer-files.txt").write_text("\n".join(names) + "\n")
    expanded = sum((ROOT / "dist" / name).stat().st_size for name in names)
    digest = hashlib.sha256(json.dumps([(n, (ROOT/"dist"/n).stat().st_size,
                                         (ROOT/"dist"/n).stat().st_mtime_ns) for n in names]).encode()).hexdigest()
    write("bundle.json", {"sha256": None, "bytes": expanded, "expanded_bytes": expanded,
                          "files": names, "release": "brand-" + a.release_key + "-" + digest[:12]})
    print(json.dumps({"files": len(names), "expanded_bytes": expanded, "streaming_upload": True}))
elif a.operation == "prepare":
    assert not (STATE / "transfer-private.json").exists(), "Inspect existing transfer; never reset blindly."
    machine = api("GET")
    assert machine["config"]["metadata"]["openline.purpose"] == "brand-library"
    assert machine["state"] == "started"
    write("machine-before.json", machine)
    previous = execute("readlink /data/current").strip()
    assert previous.startswith("/data/releases/")
    bundle = read("bundle.json")
    free_kib = int(execute("df -k /data | tail -1 | awk '{print $4}'").strip())
    expanded = sum((ROOT / "dist" / name).stat().st_size for name in bundle["files"])
    required = max(2 * bundle["bytes"], bundle["bytes"] + expanded) + 80 * 1024 * 1024
    assert free_kib * 1024 > required, "Insufficient staging space; do not start transfer."
    transfer = {"path": "/__brand_update_" + secrets.token_urlsafe(40) + "/",
                "previous": previous, "release": bundle["release"]}
    write("transfer-private.json", transfer)
    execute("mkdir -p /data/campaign-incoming /data/client-temp; rm -f /data/campaign-incoming/verified; chown nginx:nginx /data/campaign-incoming /data/client-temp")
    temporary = f"""
  location ^~ {transfer['path']} {{
    alias /data/campaign-incoming/;
    client_max_body_size 20m;
    client_body_timeout 180s;
    client_body_temp_path /data/client-temp;
    dav_methods PUT;
    create_full_put_path on;
    dav_access user:rw group:r;
    limit_except PUT {{ deny all; }}
    access_log off;
  }}
"""
    configure(nginx_config().rsplit("}", 1)[0] + temporary + "}\n")
    print("Transfer ready; capability kept private. Current site unchanged.")
elif a.operation == "upload":
    transfer = read("transfer-private.json")
    count = 0
    tar = subprocess.Popen(["tar", "--dereference", "-C", str(ROOT/"dist"), "-cf", "-", "-T", str(STATE/"transfer-files.txt")],
                           stdout=subprocess.PIPE)
    gzip = subprocess.Popen(["gzip", "-1"], stdin=tar.stdout, stdout=subprocess.PIPE)
    tar.stdout.close()
    digest, total = hashlib.sha256(), 0
    try:
        while chunk := gzip.stdout.read(16 * 1024 * 1024):
            try:
                r = SESSION.put("https://openline-brand.fly.dev" + transfer["path"] + f"part-{count:05d}",
                                data=chunk, timeout=180)
            except requests.RequestException:
                raise RuntimeError("Transfer transport failed; capability withheld") from None
            if r.status_code not in (201, 204):
                raise RuntimeError(f"Transfer HTTP {r.status_code}; capability withheld")
            digest.update(chunk)
            total += len(chunk)
            count += 1
            if count % 5 == 0:
                print(json.dumps({"uploaded_mib": round(total/1048576, 1)}), flush=True)
        assert gzip.wait() == 0 and tar.wait() == 0
    finally:
        gzip.stdout.close()
        if gzip.poll() is None:
            gzip.terminate()
        if tar.poll() is None:
            tar.terminate()
    bundle = read("bundle.json")
    bundle.update({"sha256": digest.hexdigest(), "bytes": total})
    write("bundle.json", bundle)
    write("upload.json", {"chunks": count, "bytes": total})
    print(json.dumps({"uploaded": True, "chunks": count}))
elif a.operation == "verify":
    transfer, bundle = read("transfer-private.json"), read("bundle.json")
    dest = "/data/releases/" + bundle["release"]
    # -l hardlinks unchanged media. Unlink ONLY changed destination files before
    # extraction so writing them cannot modify the prior release's hardlinks.
    job = (
        "set -eu; cd /data/campaign-incoming; "
        "cat part-* > release.tar.gz; "
        f"echo '{bundle['sha256']}  release.tar.gz' | sha256sum -c -; "
        "rm part-*; "
        f"test ! -e {shlex.quote(dest)}; mkdir {shlex.quote(dest)}; "
        f"cp -al {shlex.quote(transfer['previous'])}/. {shlex.quote(dest)}/; "
        "tar -tzf release.tar.gz > file-list; "
        f"while IFS= read -r file; do rm -f {shlex.quote(dest)}/\"$file\"; done < file-list; "
        f"tar -xzf release.tar.gz -C {shlex.quote(dest)}; "
        f"test -s {shlex.quote(dest)}/index.html; test -s {shlex.quote(dest)}/library/catalog.json; "
        "rm release.tar.gz; touch verified"
    )
    execute("nohup sh -c " + shlex.quote(job) + " </dev/null >/data/campaign-verify.log 2>&1 &")
    print("Verification and staging started; production unchanged.")
elif a.operation == "status":
    print(execute("if test -f /data/campaign-incoming/verified; then echo VERIFIED; fi; tail -4 /data/campaign-verify.log; df -h /data"))
elif a.operation == "activate":
    bundle = read("bundle.json")
    dest = "/data/releases/" + bundle["release"]
    execute(f"test -f /data/campaign-incoming/verified && ln -s {shlex.quote(dest)} /data/current.next && mv -Tf /data/current.next /data/current")
    configure(nginx_config())
    write("activation.json", {"release": bundle["release"], "previous": read("transfer-private.json")["previous"],
                               "sha256": bundle["sha256"], "machine": MACHINE})
    print("Release activated atomically; transfer endpoint removed; previous release retained.")
elif a.operation == "close-transfer":
    configure(nginx_config())
    print("Temporary transfer endpoint removed.")
elif a.operation == "rollback":
    previous = read("transfer-private.json")["previous"]
    execute(f"test -f {shlex.quote(previous)}/index.html && ln -s {shlex.quote(previous)} /data/current.rollback && mv -Tf /data/current.rollback /data/current")
    configure(nginx_config())
    print("Previous release restored; new assets retained privately for diagnosis.")
