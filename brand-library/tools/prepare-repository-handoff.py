"""Prepare source/docs without committing multi-GB binaries or private payloads."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parent/"openline-brand-assets"
WORK=ROOT.parent/"openline-brand-expansion/motion-150"
PREP=WORK/"private/docs/prepared";STATE=ROOT.parent/"openline-fly-deployment/motion-v2-4"
BACK=WORK/"private/repository-before";BACK.mkdir(parents=True,exist_ok=True)
changed=[]
def copy(source,target):
 if target.exists() and source.samefile(target):
  changed.append(str(target.relative_to(REPO)));return
 if target.is_file() and target.is_relative_to(REPO):
  back=BACK/target.relative_to(REPO)
  if not back.exists():back.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,back)
 target.parent.mkdir(parents=True,exist_ok=True)
 temp=target.with_name(target.name+".handoff-tmp");shutil.copy2(source,temp);temp.replace(target)
 changed.append(str(target.relative_to(REPO)))
for source in PREP.rglob("*.md"):copy(source,REPO/source.relative_to(PREP))
LIB=REPO/"brand-library";LIB.mkdir(exist_ok=True)
for source in ROOT.iterdir():
 if source.is_file() and source.suffix in (".jsx",".css",".html",".mjs",".json") and not source.name.startswith("."):copy(source,LIB/source.name)
for folder in ("tools","hosting","scripts"):
 for source in (ROOT/folder).rglob("*"):
  if source.is_file() and source.suffix in (".py",".mjs",".js",".conf",".toml",".md",".sh") and not any(x in source.parts for x in ("__pycache__","editorial","private","_private","receipts")) and source.name not in ("campaign-final-review.py","prepare-library-copy.mjs"):
   copy(source,LIB/source.relative_to(ROOT))
for name in ["Dockerfile","fly.toml","vite.config.js","FLOWS.md","BRAND-LIBRARY-OPERATIONS.md"]:
 if (ROOT/name).is_file():copy(ROOT/name,LIB/name)
copy(PREP/"docs/BRAND-LIBRARY.md",LIB/"README.md")
(LIB/".gitignore").write_text("node_modules/\ndist/\npublic/\n.env*\n.vercel/\n__pycache__/\n*.partial\n")
rows=[]
for p in sorted((ROOT/"public").rglob("*")):
 if not p.is_file():continue
 rel=p.relative_to(ROOT/"public")
 assert not any(x in rel.parts for x in ("private","_private","receipts","requests",".env"))
 rows.append({"path":str(rel),"url":"https://brand.openline.com/"+quote(str(rel)),
  "bytes":p.stat().st_size,"sha256":hashlib.file_digest(p.open("rb"),"sha256").hexdigest()})
(LIB/"PUBLIC-ASSETS.json").write_text(json.dumps({"version":"2.4.0","files":rows,"total_bytes":sum(r["bytes"] for r in rows)},indent=2))
for name in ["render.py","manifest.json","qa-summary.json","audiovisual-review.json","contact-sheet.jpg"]:
 copy(WORK/name,REPO/"animation/editions-150"/name)
(REPO/"animation/editions-150/.gitignore").write_text("mp4/\naudio/\nscores/\nplates/\nposters/\ngif/\nqa/\nprivate/\n__pycache__/\n")
copy(PREP/"docs/MOTION.md",REPO/"animation/editions-150/README.md")
audit=json.loads((WORK/"private/docs/audit.json").read_text())
(REPO/"docs/DOCUMENTATION-AUDIT.json").write_text(json.dumps(audit,indent=2))
links=[]
for p in sorted(PREP.rglob("*.md")):
 rel=str(p.relative_to(PREP));text=p.read_text()
 for dest in re.findall(r"\]\(([^)]+)\)",text):
  if dest.startswith(("http:","https:","mailto:","#","data:")):continue
  target=(REPO/rel).parent/dest.split("#")[0]
  if not target.exists():links.append({"file":rel,"target":dest})
(WORK/"private/docs/local-link-check.json").write_text(json.dumps(links,indent=2))
(STATE/"repository-handoff-files.json").write_text(json.dumps(sorted(set(changed+["brand-library/.gitignore","brand-library/PUBLIC-ASSETS.json","animation/editions-150/.gitignore","docs/DOCUMENTATION-AUDIT.json"])),indent=2))
print(json.dumps({"prepared_markdown":len(list(PREP.rglob("*.md"))),"public_files":len(rows),"source_files":len(changed),"unresolved_relative_links":links},indent=2))
