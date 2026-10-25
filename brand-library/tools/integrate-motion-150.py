"""Add verified native-animation sound editions without replacing originals."""
from pathlib import Path
import hashlib,json,os,shutil
ROOT=Path(__file__).resolve().parents[1];PUB=ROOT/"public"
WORK=ROOT.parent/"openline-brand-expansion/motion-150"
DEST=PUB/"library/productions/motion-150"
STATE=ROOT.parent/"openline-fly-deployment/motion-v2-4"
STATE.mkdir(parents=True,exist_ok=True)
baseline=STATE/"catalog-before.json"
if not baseline.exists():shutil.copy2(PUB/"library/catalog.json",baseline)
d=json.loads(baseline.read_text());m=json.loads((WORK/"manifest.json").read_text())
qa=json.loads((WORK/"qa-summary.json").read_text());assert qa["all_pass"] and len(m["editions"])==85
assert sum(x["category"]=="motion" for x in d["cards"])==65
changed=set();indexed=set()
def resource(rel,label,w=0,h=0):
 source=WORK/rel;target=DEST/rel;target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():target.unlink()
 os.link(source,target);path=str(target.relative_to(PUB));url="./"+path;changed.add(path)
 if path not in indexed:
  ext=target.suffix[1:].upper();ext="JPEG" if ext=="JPG" else ext
  d["files"].append({"id":hashlib.sha1(url.encode()).hexdigest()[:12],"title":target.stem,"path":path,"url":url,
   "category":"motion","series":"native-motion-150","status":"Review","format":ext,"bytes":target.stat().st_size,
   "kind":"video" if ext=="MP4" else "audio" if ext=="FLAC" else "image" if ext in ("GIF","JPEG") else "file",
   "width":w,"height":h,"source":None})
  indexed.add(path)
 return {"label":label,"url":url,"bytes":target.stat().st_size}
cards=[]
for e in m["editions"]:
 downloads=[resource(e["mp4"],"MP4 with sound",e["width"],e["height"]),
  resource(e["audio"],"FLAC lossless sound",e["width"],e["height"]),
  resource(e["poster"],"JPEG poster",e["width"],e["height"]),
  resource(e["gif"],"GIF silent layout preview",e["width"],e["height"]),
  resource(e["score_events"],"JSON sound score",e["width"],e["height"])]
 cards.append({"id":e["id"],"title":e["title"],"category":"motion","series":"native-motion-150","status":"Review",
  "description":f"{e['score']}. Original animation at native speed; four cycles with a synthesized stereo score. {e['layout']} layout.",
  "duration":e["duration_seconds"],"preview":downloads[0]["url"],"kind":"video","poster":downloads[2]["url"],
  "downloads":downloads,"source":"https://github.com/askopenline/openline-brand/tree/main/animation/loading-loop",
  "width":e["width"],"height":e["height"],"tags":["Original GIF","Sound","Horizontal" if e["width"]>e["height"] else "Square",e["score"]]})
assert json.loads((WORK/"audiovisual-review.json").read_text())["pass"]
for name,label in [("manifest.json","Manifest"),("qa-summary.json","Technical QA"),("audiovisual-review.json","Representative audiovisual QA"),("contact-sheet.jpg","JPEG layouts"),("render.py","Editable renderer")]:resource(name,label)
d["cards"]=cards+d["cards"];d["version"]="2.4.0";d["motionExpansion"]={"new":85,"soundFamilies":17,"layouts":5,"horizontal":68}
d["repository"]="https://github.com/askopenline/openline-brand"
d["counts"]={c["id"]:sum(a["category"]==c["id"] for a in d["cards"]) for c in d["categories"]}
assert d["counts"]["motion"]==150 and d["counts"]["ads"]==40 and d["counts"]["presenters"]==6
d["inventory"]["assetFiles"]=len(d["files"])
temp=PUB/"library/catalog.json.new";temp.write_text(json.dumps(d,indent=2)+"\n");temp.replace(PUB/"library/catalog.json")
changed.add("library/catalog.json")
(STATE/"public-change-list.json").write_text(json.dumps(sorted(changed),indent=2))
for name in ["package.json","package-lock.json"]:
 p=ROOT/name;j=json.loads(p.read_text());j["version"]="2.4.0"
 if "packages" in j:j["packages"][""]["version"]="2.4.0"
 p.write_text(json.dumps(j,indent=2)+"\n")
print(json.dumps({"counts":d["counts"],"new_files":len(changed),"bytes":sum((PUB/p).stat().st_size for p in changed)},indent=2))
