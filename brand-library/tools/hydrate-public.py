"""Download manifest-pinned public assets into a clean clone. Explicit opt-in."""
import argparse,hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument("--download",action="store_true");p.add_argument("--prefix",default="")
a=p.parse_args();m=json.loads((ROOT/"PUBLIC-ASSETS.json").read_text())
rows=[x for x in m["files"] if x["path"].startswith(a.prefix)]
print(f"{len(rows)} public files, {sum(x['bytes'] for x in rows)/1e9:.2f} GB. Existing matching files are reused.")
if not a.download:
 print("Inspect PUBLIC-ASSETS.json; add --download to retrieve, optionally --prefix library/productions/motion-150/");raise SystemExit
for x in rows:
 rel=Path(x["path"]);assert not rel.is_absolute() and ".." not in rel.parts
 assert x["url"].startswith("https://brand.openline.com/")
 target=ROOT/"public"/rel
 def matches(path):return path.is_file() and path.stat().st_size==x["bytes"] and hashlib.file_digest(path.open("rb"),"sha256").hexdigest()==x["sha256"]
 if matches(target):continue
 target.parent.mkdir(parents=True,exist_ok=True);temp=target.with_suffix(target.suffix+".partial")
 try:
  with urllib.request.urlopen(x["url"],timeout=90) as r,temp.open("wb") as f:
   while block:=r.read(1024*1024):f.write(block)
  assert matches(temp),"Downloaded checksum mismatch: "+str(rel)
  temp.replace(target)
 except Exception:
  temp.unlink(missing_ok=True);raise
print("Hydration complete; every downloaded file passed SHA-256 verification.")
