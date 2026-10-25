"""One explicit Fly Machines API operation per invocation.

Authentication is injected by the approved credential proxy, never read by this
script. Inspect before writes. No retry of failed/uncertain mutations is automatic.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys
import requests

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("operation", choices=["inspect", "create-app", "list-apps",
                                        "ips", "allocate-ip", "machines",
                                        "create-machine", "update-machine", "machine", "exec"])
parser.add_argument("--app", default="openline-brand")
parser.add_argument("--org")
parser.add_argument("--machine")
parser.add_argument("--commit")
parser.add_argument("--ip-type", choices=["shared_v4", "v6"], default="shared_v4")
args = parser.parse_args()
base = "https://api.machines.dev/v1"
method = "GET"
path = f"/apps/{args.app}"
payload = None
if args.operation == "create-app":
    if not args.org:
        parser.error("--org required")
    method, path = "POST", "/apps"
    payload = {"app_name": args.app, "org_slug": args.org,
               "network": "openline-brand-public"}
elif args.operation == "list-apps":
    if not args.org:
        parser.error("--org required")
    path = f"/apps?org_slug={args.org}"
elif args.operation in ["ips", "allocate-ip"]:
    path += "/ip_assignments"
    if args.operation == "allocate-ip":
        method, payload = "POST", {"type": args.ip_type}
elif args.operation in ["machines", "create-machine", "update-machine"]:
    path += "/machines"
    if args.operation in ["create-machine", "update-machine"]:
        if not args.commit:
            parser.error("--commit required")
        bundle = root / "hosting/openline-brand-dist.tar.gz"
        digest = hashlib.sha256(bundle.read_bytes()).hexdigest()
        files = [
            {"guest_path": "/tmp/openline-bootstrap.sh",
             "raw_value": base64.b64encode((root / "hosting/bootstrap.sh").read_bytes()).decode()},
            {"guest_path": "/etc/nginx/conf.d/default.conf",
             "raw_value": base64.b64encode((root / "hosting/nginx.conf").read_text().replace("__SOURCE_COMMIT__", args.commit).encode()).decode()}
        ]
        method = "POST"
        payload = {
            "name": "openline-brand-web",
            "region": "cdg",
            "config": {
                "image": "registry-1.docker.io/library/nginx:stable-alpine",
                "init": {"exec": ["/bin/sh", "/tmp/openline-bootstrap.sh"]},
                "files": files,
                "env": {
                    "BUNDLE_URL": f"https://raw.githubusercontent.com/paulfxyz/openline-brand-assets/{args.commit}/launch-studio/hosting/openline-brand-dist.tar.gz",
                    "BUNDLE_SHA256": digest
                },
                "metadata": {"openline.source_commit": args.commit,
                             "openline.purpose": "brand-launch-studio"},
                "guest": {"cpu_kind": "shared", "cpus": 1, "memory_mb": 256},
                "restart": {"policy": "on-failure", "max_retries": 3},
                "services": [{
                    "protocol": "tcp", "internal_port": 8080,
                    "ports": [{"port": 80, "handlers": ["http"], "force_https": True},
                              {"port": 443, "handlers": ["tls", "http"]}],
                    "autostart": True, "autostop": "stop", "min_machines_running": 0,
                    "concurrency": {"type": "requests", "soft_limit": 50, "hard_limit": 100}
                }],
                "checks": {"web": {"type": "http", "port": 8080, "method": "GET",
                                   "path": "/healthz", "interval": "15s",
                                   "timeout": "5s", "grace_period": "45s"}}
            }
        }
        if args.operation == "update-machine":
            if not args.machine:
                parser.error("--machine required")
            path += "/" + args.machine
            existing = requests.get(base + path, timeout=30)
            existing.raise_for_status()
            prior = existing.json()
            if prior.get("config", {}).get("metadata", {}).get("openline.purpose") != "brand-launch-studio":
                sys.exit("Refusing to update a machine without the expected purpose marker.")
            if prior.get("image_ref", {}).get("digest"):
                payload["config"]["image"] = "registry-1.docker.io/library/nginx@" + prior["image_ref"]["digest"]
            payload = {"config": payload["config"]}
elif args.operation in ["machine", "exec"]:
    if not args.machine:
        parser.error("--machine required")
    path += f"/machines/{args.machine}"
    if args.operation == "exec":
        method, path = "POST", path + "/exec"
        payload = {"command": ["/bin/sh", "-c",
                              "wget -qO- http://127.0.0.1:8080/healthz; test -f /srv/openline/downloads/openline-launch-kit.zip"],
                   "timeout": 15}

response = requests.request(method, base + path, json=payload, timeout=90)
print("HTTP", response.status_code)
try:
    data = response.json()
except ValueError:
    print(response.text[:3000])
    sys.exit(1)
if args.operation in ["machine", "create-machine", "update-machine"] and response.ok:
    # Avoid returning injected startup files repeatedly; there are no secrets in them.
    output = {k: data.get(k) for k in ["id", "name", "state", "region", "instance_id",
                                      "image_ref", "checks", "events"]}
    output["services"] = data.get("config", {}).get("services")
else:
    output = data
print(json.dumps(output, indent=2))
if not response.ok:
    sys.exit(1)
