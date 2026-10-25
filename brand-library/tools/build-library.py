"""Build a provenance-aware catalogue from the actual repository and local productions.
No credentials or private generation request payloads are copied.
"""
from pathlib import Path
import os,json,subprocess,hashlib,re,shutil
from urllib.parse import quote
APP=Path(__file__).resolve().parents[1]
REPO=Path(os.environ.get("OPENLINE_ASSET_REPO",APP.parent/"openline-brand-assets"))
PROD=Path(os.environ.get("OPENLINE_PRODUCTION",APP.parent/"openline-brand-expansion"))
PUB=APP/"public"; LIB=PUB/"library"
LIB.mkdir(exist_ok=True)
hero_gif=PROD/"motion-plus/previews/01-original-REDUCED-400px-10fps.gif"
previous=LIB/"catalog.json"
PIN=json.loads(previous.read_text()).get("sourceCommit") if previous.exists() else None
SHA=os.environ.get("OPENLINE_SOURCE_COMMIT") or PIN or subprocess.check_output(["git","-C",str(REPO),"rev-parse","HEAD"],text=True).strip()
GH="https://github.com/askopenline/openline-brand-assets"
files=[]; cards=[]; seen=set()
CATS=[("identity","Logo & colours"),("ads","Short ads"),("motion","Motion"),("presenters","Presenters"),
      ("app","App & store"),("figma","Figma & React"),("web","Web & UI"),("email","Email & print"),
      ("payments","Payment marks"),("workadventure","WorkAdventure"),("social","Social & renders"),("archives","Archives"),("docs","Documentation")]
def link(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():
        if os.path.samefile(src,dst):return
        if dst.stat().st_size==src.stat().st_size and hashlib.sha256(dst.read_bytes()).digest()==hashlib.sha256(src.read_bytes()).digest():return
        dst.unlink()
    try:os.link(src,dst)
    except OSError:shutil.copy2(src,dst)
def url(p):return "./"+quote(str(p.relative_to(PUB)),safe="/")
if hero_gif.is_file():link(hero_gif,LIB/"previews/original-loop-reduced.gif")
def title(p):
    return re.sub(r"[-_]+"," ",Path(p).stem).replace("openline ","").strip().capitalize()
def kind(p):
    ext=Path(p).suffix.lower()
    return "image" if ext in [".png",".jpg",".jpeg",".webp",".gif",".svg"] else "video" if ext in [".mp4",".webm",".mov"] else "audio" if ext in [".wav",".mp3",".m4a"] else "file"
def addfile(path,cat,status="Source",source=None,label=None):
    u=url(path)
    if u in seen:return
    seen.add(u)
    row={"id":hashlib.sha1(u.encode()).hexdigest()[:12],"title":label or title(path),"path":str(path.relative_to(PUB)),"url":u,
         "category":cat,"status":status,"format":("JPEG" if path.suffix.lower()==".jpg" else path.suffix[1:].upper()) or "FILE","bytes":path.stat().st_size,
         "kind":kind(path),"source":source}
    files.append(row);return row
def category(p):
    root=p.split("/")[0]
    return {"logo":"identity","wordmark":"identity","animation":"motion","app-icons":"app","figma":"figma","mobile":"figma",
            "email":"email","payment-methods":"payments","workadventure":"workadventure","social":"social","web":"web",
            "launch-studio":"archives","misc":"docs"}.get(root,"docs")
tracked=subprocess.check_output(["git","-C",str(REPO),"ls-tree","-r","--name-only","-z",SHA]).decode().split("\0")
modified=set(subprocess.check_output(["git","-C",str(REPO),"diff","--name-only","-z",SHA]).decode().split("\0"))
for rel in filter(None,tracked):
    src=REPO/rel
    if not src.is_file():modified.add(rel)
    dst=LIB/"repository"/rel.replace(".github/","github/")
    if rel in modified:
        content=subprocess.check_output(["git","-C",str(REPO),"show",SHA+":"+rel])
        if not dst.exists() or dst.read_bytes()!=content:
            dst.parent.mkdir(parents=True,exist_ok=True)
            if dst.exists():dst.unlink()
            dst.write_bytes(content)
    else:link(src,dst)
    cat=category(rel)
    status="Third-party" if cat=="payments" else "Archive" if rel.startswith("launch-studio/") else "Approved" if rel.startswith("app-icons/final/") else "Source"
    addfile(dst,cat,status,GH+"/blob/"+SHA+"/"+quote(rel,safe="/"),rel)

def card(id,title_,cat,paths,preview=None,poster=None,status="Review",description="",duration=None,source=None,tags=None):
    paths=[(name,p) for name,p in paths if p and p.is_file()]
    if not paths:return
    if not preview or not preview.is_file():preview=paths[0][1]
    for name,p in paths:addfile(p,cat,status,source)
    cards.append({"id":id,"title":title_,"category":cat,"status":status,"description":description,"duration":duration,
                  "preview":url(preview) if preview and preview.is_file() else None,"kind":kind(preview) if preview else "file",
                  "poster":url(poster) if poster and poster.is_file() else None,
                  "downloads":[{"label":name,"url":url(p),"bytes":p.stat().st_size} for name,p in paths],
                  "source":source,"tags":tags or []})
R=LIB/"repository"
card("source-mark","The Openline mark","identity",[(p.suffix[1:].upper()+" · "+p.stem,p) for p in (R/"logo").rglob("*") if p.is_file()],
     R/"logo/png/openline-logo-color.png",status="Source",description="Original artwork, with light, dark and vector source variants.",source=GH+"/tree/"+SHA+"/logo")
card("source-wordmark","Original wordmark sources","archives",[(p.suffix[1:].upper()+" · "+p.stem,p) for p in (R/"wordmark").rglob("*") if p.is_file()],
     R/"wordmark/png/openline-wordmark-color.png",status="Archive",description="Untouched original deliveries. New lockups omit the legacy underscore.")
gfx=PROD/"graphics"
if gfx.exists():
    for p in gfx.rglob("*"):
        if not p.is_file() or any(x in p.parts for x in ("internal-archive","originals")) or p.suffix==".zip":continue
        d=LIB/"graphics"/p.relative_to(gfx);link(p,d);addfile(d,"social" if "social" in p.parts else "identity","Review")
    for p in sorted((LIB/"graphics").rglob("*.svg")):
        if "/social/" in str(p):
            preview=p.with_suffix(".webp")
            card("gfx-"+p.stem,title(p),"social",[(ext.upper(),p.with_suffix("."+ext)) for ext in ("svg","png","webp")],preview if preview.exists() else p,description="Brand composition for creative review.")
        elif "transparent" in str(p):
            exports=[("SVG · scalable",p)]+[(q.suffix[1:].upper()+" · "+q.stem.split("-")[-1]+"px",q) for q in sorted(p.parent.glob(p.stem+"-*")) if q.suffix.lower() in (".png",".webp")]
            card("gfx-"+p.stem,title(p),"identity",exports,p,description="Original paths preserved. Review colourway or lockup; not a replacement app icon.")
card("final-icon","The approved app icon","app",[("All formats ZIP",PUB/"downloads/openline-final-icon-all-formats.zip"),("Native kits",PUB/"downloads/openline-native-icons.zip")],
     PUB/"assets/apple-icon-1024.png",status="Approved",description="43.5% visible mark width. Native build acceptance remains a separate check.")
card("mobile-design","Mobile interface sources","figma",[("React source",R/"mobile/app-screens/src/components/MobileScreensPage.tsx"),("Figma source",R/"figma/mobile/openline-mobile-screens.fig")],
     PUB/"assets/screen-dashboard.png",status="Source",description="Design previews and editable sources, not native production captures.")
for p in sorted((R/"workadventure/apps/screenshots").glob("*.png")):
    html=R/"workadventure/apps"/(p.stem+".html")
    card("wa-"+p.stem,title(p),"workadventure",[("Screenshot PNG",p),("HTML source",html)],p,status="Source",description="Virtual-office interface preview. Download the standalone source.")
for p in sorted((R/"payment-methods/svg").glob("*.svg")):
    card("payment-"+p.stem,title(p),"payments",[("SVG",p)],p,status="Third-party",description="Third-party identification mark. Preserve attribution and applicable rights.")
for p in sorted((R/"email").rglob("*.html")):
    card("email-"+p.stem,title(p),"email",[("HTML source",p)],status="Source",description="Reusable email or print layout. Inspect the source before integration.")
for p in sorted((R/"animation").rglob("*.mp4")):
    gif=p.with_suffix(".gif")
    card("original-"+hashlib.sha1(str(p).encode()).hexdigest()[:10],title(p),"motion",[("MP4",p),("GIF",gif)],
         p,status="Source",description="Original repository animation.",source=GH+"/tree/"+SHA+"/animation")
original=R/"animation/loading-loop/openline-loading-loop.gif"
card("original-loading-gif","Original loading loop","motion",[("Original GIF",original),("Lottie JSON",original.with_suffix(".lottie.json"))],original,PUB/"brand-expansion/media/readme-original.jpg",
     status="Source",description="The original README animation. Its moving silhouette is the source for the new sound variations.")
MEDIA=PUB/"brand-expansion/media"; DOWN=PUB/"brand-expansion/downloads"
for n,name in [(1,"Packing list"),(2,"Plan choice")]:
    card("ad-"+str(n).zfill(2),name,"ads",[("MP4",MEDIA/f"openline-ad-0{n}.mp4")],MEDIA/f"openline-ad-0{n}.mp4",MEDIA/f"ad-0{n}-poster.jpg",duration=15,description="Earlier short-ad concept. Silent.",tags=["Silent","Original"])
admanifest=PROD/"ads-volume-two/manifest.json"
if admanifest.exists():
    for n,a in enumerate(json.loads(admanifest.read_text())["ads"],3):
        base=MEDIA/"ads-v2"
        card(f"ad-{n:02}",a["title"],"ads",[(fmt,base/a[key]) for fmt,key in [("MP4","mp4"),("GIF","gif"),("JPEG","poster"),("WAV","wav")]],base/a["mp4"],base/a["poster"],duration=a["duration_seconds"],description="Short-ad creative concept with original sound design.",tags=["Sound"])
for folder,cat in [("ads-volume-three","ads"),("readme-motion-twelve","motion"),("presenters-long","presenters")]:
    manifest=PROD/folder/"manifest.json"
    if not manifest.exists():continue
    data=json.loads(manifest.read_text())
    rows=data if isinstance(data,list) else data.get("ads",data.get("exports",data.get("presenters",data.get("variants",[]))))
    for a in rows:
        keys=[("MP4",a.get("mp4",a.get("wide",a.get("master")))),("Portrait MP4",a.get("portrait")),("GIF",a.get("gif",a.get("preview"))),("JPEG",a.get("poster",a.get("poster_wide"))),("Portrait JPEG",a.get("poster_portrait")),("WAV",a.get("wav",a.get("audio")))]
        captions=a.get("captions",[])
        if isinstance(captions,str):captions=[captions]
        keys.extend(("Captions "+Path(p).suffix[1:].upper(),p) for p in captions)
        resolved=[]
        for fmt,rel in keys:
            if not rel:continue
            src=PROD/folder/rel
            if not src.is_file():continue
            dst=LIB/"productions"/folder/rel;link(src,dst);resolved.append((fmt,dst))
        lookup=dict(resolved)
        if "MP4" not in lookup:continue
        ident=str(a.get("id",a.get("slug",a.get("number",a.get("title","")))))
        display_title="Hellen 04 · A new face" if cat=="presenters" and ident=="hellen-04" else a.get("title",title(ident))
        card(folder+"-"+ident,display_title,cat,resolved,lookup["MP4"],lookup.get("JPEG"),duration=round(a.get("duration_seconds",a.get("duration",0)),2),
             description="AI-generated presenter comparison. Not the complete installation tutorial." if cat=="presenters" else "Original loading-loop artwork with a new sound treatment." if cat=="motion" else "Short-ad creative concept with original sound design.",
             tags=["AI presenter","Longer sample"] if cat=="presenters" else ["Original GIF","Sound"] if cat=="motion" else ["Sound","New"])
    for name in ("manifest.json","HANDOFF.txt","README.txt"):
        p=PROD/folder/name
        if p.is_file():
            dst=LIB/"productions"/folder/name
            if folder=="presenters-long" and name=="manifest.json":
                if dst.exists():dst.unlink()
                dst.parent.mkdir(parents=True,exist_ok=True)
                dst.write_text(json.dumps([{k:v for k,v in a.items() if k!="sourcecuts"} for a in rows],indent=2))
            else:link(p,dst)
            addfile(dst,"docs","Source")
for p in (LIB/"downloads").glob("*.zip"):
    cat="ads" if "ads" in p.stem else "presenters" if "presenter" in p.stem else "motion"
    addfile(p,cat,"Review")
for a in json.loads((PROD/"production/presenter-v2/deliverables/manifest.json").read_text()):
    slug=a["id"]
    card("presenter-"+slug,slug.replace("-"," ").title()+" · Eight-second sample","archives",
         [("Wide MP4",MEDIA/a["wide"]),("Portrait MP4",MEDIA/a["portrait"]),("JPEG",MEDIA/f"{slug}-wide.jpg"),("WAV",MEDIA/f"{slug}-voice.wav"),("Captions",MEDIA/f"{slug}.vtt")],
         MEDIA/a["wide"],MEDIA/f"{slug}-wide.jpg",status="Archive",duration=8,description="Earlier fictional AI presenter comparison.",tags=["AI presenter"])
for slug in ("hellen-01","hellen-03"):
    card("presenter-"+slug,slug.replace("-"," ").title()+" · Original sample","archives",[("Wide MP4",MEDIA/f"openline-{slug}-presenter.mp4"),("Portrait MP4",MEDIA/f"openline-{slug}-portrait.mp4")],
         MEDIA/f"openline-{slug}-presenter.mp4",MEDIA/f"{slug}-wide.jpg",status="Archive",duration=2.93,description="Earlier fictional AI reference; not an upgraded long sample.",tags=["AI presenter"])
for a in json.loads((PROD/"motion-volume-two/manifest.json").read_text())["exports"]:
    base=MEDIA/"motion-v2"
    card("motion-"+str(a["number"]),a["title"],"motion",[(label,base/a[key]) for label,key in [("MP4","master"),("GIF","preview"),("JPEG","poster"),("WAV","wav")]],
         base/a["master"],base/a["poster"],duration=a["duration_seconds"],description=a.get("concept",""),tags=["Sound","Earlier collection"])
for slug,label,duration in [("readme-original","Original GIF · Faithful video",3.04),("readme-extended","Original GIF · Extended",8),("readme-sting","Original GIF · Short sting",2.6)]:
    card(slug,label,"motion",[(ext.upper(),MEDIA/(slug+"."+ext)) for ext in ("mp4","gif","jpg")],MEDIA/(slug+".mp4"),MEDIA/(slug+".jpg"),duration=duration,description="Earlier treatment of the original README animation. The faithful master is intentionally silent.")
for p in sorted(MEDIA.glob("openline-*-1080*.mp4")):
    card("initial-"+p.stem,title(p),"motion",[("MP4",p)],p,duration=4,description="Earlier exact-artwork animation. Silent master.")
for p in sorted(MEDIA.glob("openline-*-1920x1080.mp4")):
    card("initial-"+p.stem,title(p),"motion",[("MP4",p)],p,duration=4,description="Earlier exact-artwork animation. Silent master.")
for p in sorted(MEDIA.glob("*tutorial*.mp4")):
    card("tutorial-"+p.stem,title(p),"archives",[("MP4",p)],p,status="Archive",description="Earlier tutorial concept. Real native-device recordings remain a production requirement.")
card("hellen-original-pilot","Hellen · Original presenter pilot","archives",[("MP4",MEDIA/"openline-hellen-presenter-pilot.mp4")],MEDIA/"openline-hellen-presenter-pilot.mp4",MEDIA/"hellen-pilot-poster.jpg",status="Archive",description="Original short presenter pilot. Not a complete installation tutorial.")
for p in DOWN.glob("*.zip"):
    card("pack-"+p.stem,title(p),"archives",[("ZIP",p)],status="Archive",description="Earlier collection download. Individual newer additions are listed separately.")
for p in PUB.joinpath("downloads").rglob("*"):
    if p.is_file():addfile(p,"app","Review")
for p in MEDIA.rglob("*"):
    if p.is_file():addfile(p,"archives","Archive")
for p in PUB.rglob("*"):
    if not p.is_file() or p.is_relative_to(LIB):continue
    relative=str(p.relative_to(PUB))
    if relative.startswith("references/"):addfile(p,"archives","Third-party")
    elif relative.startswith(("assets/","submission/","mobile-preview/","series/signal/")):addfile(p,"app","Review")
    elif relative.startswith("series/"):addfile(p,"archives","Archive")
    elif relative.startswith("fonts/"):addfile(p,"identity","Source")
    else:addfile(p,"docs" if p.suffix in (".json",".md",".txt") else "archives","Source")
for p in (R/"figma/mobile").glob("*.fig"):
    card("figma-native-"+p.stem,"Native mobile Figma source","figma",[("FIG",p)],status="Source",description="Editable native Figma document.")
for filename,label in [("verified-live-five-series.zip","Five original screenshot directions"),("live-orange-v110.zip","Earlier orange screenshot set")]:
    p=APP.parent/filename
    if p.exists():
        d=LIB/"archives"/filename;link(p,d)
        card(filename,label,"archives",[("ZIP",d)],status="Archive",description="Historical review archive, not the current submission edition.")
for p in list(LIB.glob("productions/*/manifest.json")):addfile(p,"docs","Source")
if (LIB/"production-costs.json").is_file():addfile(LIB/"production-costs.json","docs","Source")
copyfile=APP/"tools/editorial/library-copy-response.json"
copy=json.loads(json.loads(copyfile.read_text())["choices"][0]["message"]["content"]) if copyfile.exists() else {}
fix=APP/"tools/editorial/library-copy-fix-response.json"
if fix.exists():
    edits=json.loads(json.loads(fix.read_text())["choices"][0]["message"]["content"])
    copy["hero"]=edits["hero"];copy["empty"]=edits["empty"];copy["sections"]["motion"]["description"]=edits["motionDescription"]
polish=APP/"tools/editorial/library-copy-polish-response.json"
if polish.exists():
    edits=json.loads(json.loads(polish.read_text())["choices"][0]["message"]["content"])
    copy["hero"]=edits["hero"]
    for key,value in edits.get("sections",{}).items():copy["sections"][key].update(value)
    copy["footer"]=edits["footer"]
order={"identity":0,"ads":1,"presenters":2,"motion":3,"app":4,"figma":5,"social":6,"workadventure":7,"email":8,"web":9,"payments":10,"archives":11,"docs":12}
cards.sort(key=lambda a:(order[a["category"]],0 if a["id"].startswith(("ads-volume-three","presenters-long","readme-motion-twelve")) else 1))
bundles=[]
for p in sorted((LIB/"downloads").glob("*.zip")):
    if "four-presenters" in p.name and sum(c["category"]=="presenters" for c in cards)!=4:continue
    bundles.append({"title":title(p),"category":"ads" if "ads" in p.stem else "presenters" if "presenter" in p.stem else "motion","url":url(p),"bytes":p.stat().st_size})
catalog={"version":"2.0.0","sourceCommit":SHA,"repository":GH,"repositoryAccess":"READ","domain":"brand.openline.com","domainStatus":"Prepared, not connected",
         "categories":[{"id":a,"name":b} for a,b in CATS],"cards":cards,"files":files,"copy":copy,"bundles":bundles,
         "inventory":{"repositoryTrackedFiles":len(list(filter(None,tracked))),"repositoryIndexedFiles":sum(f["source"] is not None for f in files),"assetFiles":len(files)},
         "counts":{cat:sum(c["category"]==cat for c in cards) for cat,_ in CATS}}
(LIB/"catalog.json").write_text(json.dumps(catalog,ensure_ascii=False,separators=(",",":")))
print(json.dumps({"cards":len(cards),"files":len(files),"counts":catalog["counts"],"source":SHA},indent=2))
