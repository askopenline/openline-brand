"""Bundle selected public deliverables, never API payloads or private credentials."""
from pathlib import Path
import json,zipfile,hashlib,os
ROOT=Path(__file__).resolve().parents[1]
PROD=ROOT.parent/"openline-brand-expansion"
OUT=ROOT/"public/library/downloads";OUT.mkdir(parents=True,exist_ok=True)
packs=[
 ("readme-motion-twelve","openline-original-gif-twelve-sound-editions.zip",["mp4","gif","posters","wav","sources"],["manifest.json","HANDOFF.txt","render_readme_twelve.py","verify_motion.py","requirements.txt"]),
 ("ads-volume-three","openline-short-ads-09-to-30.zip",["mp4","previews","posters","audio","source-assets","fonts"],["manifest.json","README.txt","storyboards.json","source-provenance.json","render_volume_three.py"]),
 ("presenters-long","openline-four-presenters-24-second-previews.zip",["deliverables"],["manifest.json","HANDOFF.txt","README.md","compose.py","script.json"])
]
rows=[]
for folder,name,dirs,individual in packs:
    root=PROD/folder
    if not (root/"manifest.json").exists():continue
    target=OUT/name
    if folder=="presenters-long":
        manifest=json.loads((root/"manifest.json").read_text())
        if len(manifest)!=4:continue
        files=[root/p for p in json.loads((root/"public-files.json").read_text())["files"]]
    else:
        files=sorted({p for d in dirs for p in (root/d).rglob("*") if p.is_file() and p.suffix not in (".zip",".pyc")}|{root/p for p in individual if (root/p).is_file()})
    signature=hashlib.sha256("".join(str(p)+str(p.stat().st_size)+str(p.stat().st_mtime_ns) for p in files).encode()).hexdigest()
    stamp=ROOT/"tools"/(name+".build")
    if not target.exists() or not stamp.exists() or stamp.read_text()!=signature:
        with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
            for p in files:z.write(p,arcname=str(p.relative_to(root)))
            if folder=="presenters-long":
                z.writestr("manifest.json",json.dumps([{k:v for k,v in a.items() if k!="sourcecuts"} for a in manifest],indent=2))
                z.writestr("README.txt","Four fictional AI-presenter comparison samples. Each video track is 24 seconds; the container includes a short audio tail. Landscape 1920x1080 and portrait 810x1080 (3:4), not a 9:16 master. Three intentional edited takes, not seamless continuity. Mild synthetic cadence remains. These are not a complete installation tutorial or genuine device recordings. Raw unlabelled takes and private provider payloads are excluded. Captions use approximate phrase timing. GIF previews are silent.\n")
        with zipfile.ZipFile(target) as z:assert z.testzip() is None
        stamp.write_text(signature)
    rows.append({"id":folder,"filename":name,"bytes":target.stat().st_size,"sha256":hashlib.sha256(target.read_bytes()).hexdigest(),"entries":len(files)+(2 if folder=="presenters-long" else 0)})
if (PROD/"ads-volume-three/manifest.json").exists():
    target=OUT/"openline-all-30-short-ads-mp4-and-posters.zip"
    media=ROOT/"public/brand-expansion/media"
    inputs=[(media/f"openline-ad-{n:02}.mp4",f"{n:02}/video.mp4") for n in (1,2)]+[(media/f"ad-{n:02}-poster.jpg",f"{n:02}/poster.jpg") for n in (1,2)]
    for n,a in enumerate(json.loads((PROD/"ads-volume-two/manifest.json").read_text())["ads"],3):
        inputs.extend([(media/"ads-v2"/a["mp4"],f"{n:02}/"+Path(a["mp4"]).name),(media/"ads-v2"/a["poster"],f"{n:02}/"+Path(a["poster"]).name)])
    for a in json.loads((PROD/"ads-volume-three/manifest.json").read_text())["ads"]:
        inputs.extend([(PROD/"ads-volume-three"/a["mp4"],str(a["id"])+"/"+Path(a["mp4"]).name),(PROD/"ads-volume-three"/a["poster"],str(a["id"])+"/"+Path(a["poster"]).name)])
    assert len(inputs)==60 and all(p.is_file() for p,_ in inputs)
    if not target.exists() or target.stat().st_mtime<max(p.stat().st_mtime for p,_ in inputs):
        with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
            for p,arc in inputs:z.write(p,arcname=arc)
        with zipfile.ZipFile(target) as z:assert z.testzip() is None
    rows.append({"id":"all-30-ads","filename":target.name,"bytes":target.stat().st_size,"sha256":hashlib.sha256(target.read_bytes()).hexdigest(),"entries":len(inputs)})
(OUT/"manifest.json").write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
