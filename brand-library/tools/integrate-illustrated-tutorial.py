"""Publish only the reviewed illustrated edition; preserve the current library."""
from pathlib import Path
import ast, hashlib, json, os, shutil
from urllib.parse import quote

APP = Path(__file__).resolve().parents[1]
EXP = APP.parent/"openline-brand-expansion"
SOURCE = EXP/"hellen-illustrated-guide"
PUB = APP/"public"
REPO = APP.parent/"openline-brand-assets"
STATE = APP.parent/"openline-fly-deployment/hellen-illustrated-v2-5-1"
STATE.mkdir(parents=True,exist_ok=True)
PREFIX = "library/hellen-illustrated-guide/"
ID = "hellen-illustrated-guide-complete"

def load(path):
    return json.loads(path.read_text())

def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_name(path.name+".new")
    temp.write_text(json.dumps(obj,indent=2)+"\n")
    temp.replace(path)

qa=load(SOURCE/"deliverables/qa-summary.json")
assert qa["technical"]["full_decode"] and qa["perceptual_review"]["pass"]
assert not qa["perceptual_review"]["material_issues"]
manifest=load(SOURCE/"deliverables/manifest.json")
catalog=load(PUB/"library/catalog.json")
before={cat:sum(c["category"]==cat for c in catalog["cards"]) for cat in ("ads","motion")}
assert before=={"ads":60,"motion":150}
catalog["cards"]=[c for c in catalog["cards"] if c["id"]!=ID]
catalog["files"]=[f for f in catalog["files"] if not f["path"].startswith(PREFIX)]
changed=[]
resource={}
for row in load(SOURCE/"public-files.json")["files"]:
    relative=Path(row["path"])
    assert relative.parts[0]=="deliverables" and ".." not in relative.parts
    file=SOURCE/relative
    assert hashlib.sha256(file.read_bytes()).hexdigest()==row["sha256"]
    target=PUB/PREFIX/relative.name
    target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():
        os.link(file,target)
    assert target.samefile(file)
    url="./"+PREFIX+relative.name
    extension=relative.suffix[1:].upper()
    item={"id":hashlib.sha1(url.encode()).hexdigest()[:12],"title":relative.stem,
          "path":PREFIX+relative.name,"url":url,"category":"presenters",
          "series":"hellen-illustrated-guide","status":"Review","format":extension,
          "bytes":row["bytes"],"kind":"video" if extension=="MP4" else
          "audio" if extension=="WAV" else "image" if extension=="JPG" else "file","source":None}
    catalog["files"].append(item)
    changed.append(PREFIX+relative.name)
    resource[relative.name]=item

downloads=[]
for name,label in [
    (manifest["video"],"Full tutorial MP4"),(manifest["poster"],"Poster JPEG"),
    ("tutorial-notes.md","Tutorial notes"),("hellen-tutorial-en.srt","English SRT"),
    ("hellen-tutorial-en.vtt","English VTT"),("narration.txt","Full transcript"),
    ("hellen-narration.wav","Continuous narration WAV"),("chapters.json","Chapter timings"),
    ("qa-summary.json","QA summary")]:
    row=resource[name]
    downloads.append({"url":row["url"],"bytes":row["bytes"],"label":label})
description=("A complete three-minute example: Hellen's office portrait on the left, "
             "animated installation screens on the right and one continuous voice. "
             "Includes QR and manual routes, line settings, roaming and Android guidance.")
catalog["cards"].insert(0,{"id":ID,"title":"Install your Openline eSIM · complete illustrated guide",
    "category":"presenters","series":"hellen-illustrated-guide","status":"Review",
    "kind":"video","duration":round(manifest["duration_seconds"],2),
    "description":description,"preview":resource[manifest["video"]]["url"],
    "poster":resource[manifest["poster"]]["url"],"downloads":downloads,
    "script":(SOURCE/"deliverables/narration.txt").read_text().strip(),
    "disclosure":"AI-generated static Hellen portrait and synthetic voice. The portrait is not lip-synced. "
    "Phone screens are animated illustrations, not real device recordings.","source":None})
catalog["tutorial"]={"title":"Hellen’s complete animated installation guide",
    "summary":description,"description":description,
    "planUrl":resource["tutorial-notes.md"]["url"],
    "gates":[{"title":"One continuous voice","detail":"The same narration from start to finish, with no voice joins."},
             {"title":"Animated phone walkthrough","detail":"QR or manual entry, checked recaps, data and roaming settings, plus Android examples."},
             {"title":"Illustrated example","detail":"Hellen’s static portrait stays on the left. The phone screens are demonstrations, not real activation footage."}]}
catalog["fullTutorial"]=True
catalog["fullTutorialId"]=ID
catalog["version"]="2.5.1"
catalog["counts"]={c["id"]:sum(x["category"]==c["id"] for x in catalog["cards"])
                   for c in catalog["categories"]}
assert {cat:catalog["counts"][cat] for cat in before}==before
catalog["inventory"]["assetFiles"]=len(catalog["files"])

# Idempotent accounting: only add this review once; never infer failed-job billing.
cost=manifest["new_review_cost_usd"]
ledger=load(EXP/"cost-ledger.json")
previous=ledger.get("illustrated_guide",{}).get("OpenRouter",0)
ledger["reported_costs"]["OpenRouter"]=round(ledger["reported_costs"]["OpenRouter"]+cost-previous,9)
ledger["illustrated_guide"]={"Runware":0,"OpenRouter":cost,"new_generation":False}
ledger["final_media"]["tutorial_status"]="Long avatar failed with provider timeout; completed illustrated edition uses existing voice and static portrait. Failed-job charge unconfirmed."
save(EXP/"cost-ledger.json",ledger)
public_ledger=load(PUB/"brand-expansion/downloads/cost-ledger.json")
public_ledger["cumulative_api_reported_costs"]=ledger["reported_costs"]
public_ledger["latest_final_media"]=ledger["final_media"]
public_ledger["illustrated_guide"]=ledger["illustrated_guide"]
save(PUB/"brand-expansion/downloads/cost-ledger.json",public_ledger)
changed+=["brand-expansion/downloads/cost-ledger.json","library/catalog.json"]
for row in catalog["files"]:
    if row["path"]=="brand-expansion/downloads/cost-ledger.json":
        row["bytes"]=(PUB/row["path"]).stat().st_size
save(PUB/"library/catalog.json",catalog)
save(STATE/"public-changed-files.json",changed)

# Keep source and public metadata synchronized without putting large media in Git.
inventory_path=REPO/"brand-library/PUBLIC-ASSETS.json"
inventory=load(inventory_path)
rows={r["path"]:r for r in inventory["files"]}
for name in changed:
    path=PUB/name
    rows[name]={"path":name,"url":"https://brand.openline.com/"+quote(name),
                "bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
inventory.update(version="2.5.1",files=sorted(rows.values(),key=lambda r:r["path"]))
inventory["total_bytes"]=sum(r["bytes"] for r in rows.values())
save(inventory_path,inventory)
docs=REPO/"tutorial/illustrated-guide"
docs.mkdir(parents=True,exist_ok=True)
for name in ("manifest.json","qa-summary.json","sources-audit.json","chapters.json","narration.txt","tutorial-notes.md"):
    shutil.copy2(SOURCE/"deliverables"/name,docs/name)
# Publish only the deterministic renderer/QA, not provider calls or review prompts.
tree=ast.parse((SOURCE/"build.py").read_text())
tree.body=[node for node in tree.body
           if not (isinstance(node,ast.FunctionDef) and node.name in {"review","finalize"})
           and not (isinstance(node,ast.If) and "__name__" in ast.unparse(node.test))]
tree.body.extend(ast.parse(
    "if __name__ == '__main__':\n"
    "    parser = argparse.ArgumentParser()\n"
    "    parser.add_argument('operation', choices=['compose', 'qa'])\n"
    "    globals()[parser.parse_args().operation]()\n").body)
(docs/"renderer.py").write_text(ast.unparse(tree)+"\n")
if (docs/"build.py").exists():
    (docs/"build.py").unlink()
poster=REPO/".github/assets/hellen-illustrated-guide.jpg"
shutil.copy2(SOURCE/"deliverables"/manifest["poster"],poster)
save(STATE/"integration-summary.json",{"version":"2.5.1","duration_seconds":manifest["duration_seconds"],
    "new_files":len(resource),"counts":catalog["counts"],"new_runware_spend":0,"review_cost":cost})
print(json.dumps(load(STATE/"integration-summary.json"),indent=2))
