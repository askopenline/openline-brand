import json,hashlib,re,zipfile,shutil
from pathlib import Path
from PIL import Image,ImageDraw
APP=Path(__file__).resolve().parents[1];PUB=APP/"public";V=PUB/"app-v2"
STATE=APP.parent/"openline-fly-deployment/app-v2-v2-6-0"
REPO=APP.parent if APP.name=="brand-library" else APP.parent/"openline-brand-assets"
def read(p):return json.loads(p.read_text())
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
copy=read(V/"copy.json")
assert len(copy["metadata"]["apple"]["subtitle"])<=30
assert len(copy["metadata"]["google"]["shortDescription"])<=80
assert not re.search(r"[$€£¥₹₽]|\b(price|prices|cheap|pay|payment|savings|purchased|purchase|checkout|refund)\b",json.dumps(copy),re.I)
before=read(STATE/"v1-hashes.json")
assert all(hashlib.sha256((PUB/p).read_bytes()).hexdigest()==h for p,h in before.items()),"V1 changed"
for edition in ("marketing","submission"):
    for platform in ("apple","google"):
        folder=V/edition/platform
        sheet=Image.new("RGB",(1200,480 if platform=="apple" else 390),"#faf9f6")
        for n in range(1,7):
            p=folder/f"{n:02}.png";im=Image.open(p)
            assert im.size==((1320,2868) if platform=="apple" else (1080,1920))
            im.save(p.with_suffix(".webp"),quality=92,method=6)
            thumb=im.copy();thumb.thumbnail((184,440 if platform=="apple" else 350))
            sheet.paste(thumb,(n*200-192,8))
            ImageDraw.Draw(sheet).text((n*200-192,sheet.height-25),f"{n:02}",fill="black")
        sheet.save(folder/"contact-sheet.jpg",quality=94)
for platform in ("apple","google"):
    text="# Openline V2 "+("App Store" if platform=="apple" else "Google Play")+" listing draft\n\n"
    for key,val in copy["metadata"][platform].items():text+="## "+key+"\n\n"+val+"\n\n"
    (V/f"{platform}-listing.md").write_text(text)
def zipfiles(name,paths):
    p=V/"downloads"/name;p.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(p,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in sorted(set(paths)):
            if f.is_file():z.write(f,f.relative_to(V).as_posix())
    with zipfile.ZipFile(p) as z:assert z.testzip() is None
notes=[V/"README.md",V/"copy.json"]
zipfiles("openline-v2-icons.zip",list((V/"icons").glob("*"))+[V/"README.md"])
zipfiles("openline-v2-marketing.zip",list((V/"marketing").rglob("*"))+notes)
for platform in ("apple","google"):
    zipfiles(f"openline-v2-{platform}.zip",list((V/"submission"/platform).glob("*"))+[V/f"{platform}-listing.md",*notes,V/f"icons/openline-icon-white-{'1024' if platform=='apple' else '512'}.png"])
zipfiles("openline-v2-complete.zip",[p for p in V.rglob("*") if "downloads" not in p.parts])
cat=read(PUB/"library/catalog.json")
def dl(p,label):return {"url":"./"+p.relative_to(PUB).as_posix(),"label":label,"bytes":p.stat().st_size}
rows=[];cards=[]
for edition in ("marketing","submission"):
    for platform in ("apple","google"):
        title=("iPhone" if platform=="apple" else "Android")+" · V2 "+edition+" screenshots"
        pack="marketing" if edition=="marketing" else platform
        row={"id":f"v2-{edition}-{platform}","title":title,"status":"V2 · design review",
             "bundle":f"./app-v2/downloads/openline-v2-{pack}.zip","cards":[]}
        for n in range(1,7):
            p=V/edition/platform/f"{n:02}.png";frame=copy["frames"][n-1]
            card={"id":f"v2-{edition}-{platform}-{n}","title":title+f" · {n:02}","caption":" ".join(frame["head"]),
                  "category":"app","status":"Review","kind":"image","preview":dl(p.with_suffix(".webp"),"")["url"],
                  "description":"V2 adapted app-resource artwork. No monetary content. Native release capture still required.",
                  "appGroups":["screenshots"],"downloads":[dl(p,"Full-resolution PNG"),dl(p.with_suffix(".webp"),"WebP preview")]}
            cards.append(card);row["cards"].append(card)
        rows.append(row)
icon={"id":"v2-app-icon","title":"V2 app icon · mark +12.5%","category":"app","status":"Review","kind":"image",
      "preview":"./app-v2/icons/openline-icon-white-1024.png","description":"Original vector mark enlarged inside the unchanged white tile; V1 remains untouched.",
      "appGroups":["icons"],"downloads":[dl(V/"downloads/openline-v2-icons.zip","All V2 icon formats"),dl(V/"icons/openline-icon-white.svg","SVG"),dl(V/"icons/openline-icon-white-1024.png","PNG 1024")]}
cards.insert(0,icon)
for p in sorted((V/"screens").glob("*.png")):
    cards.append({"id":"v2-source-"+p.stem,"title":"V2 app view · "+p.stem,"category":"app","status":"Review","kind":"image",
      "preview":dl(p,"")["url"],"description":"Adapted design resource, not a native release capture.","appGroups":["source"],"downloads":[dl(p,"PNG")]})
entries=[]
for platform,label,route in (("apple","App Store","app-store"),("google","Google Play","google-play")):
    entry={"id":platform,"title":label,"metadata":copy["metadata"][platform],"preview":f"./studio.html?appVersion=v2#{route}-submission",
           "copy":f"./app-v2/{platform}-listing.md","bundle":f"./app-v2/downloads/openline-v2-{platform}.zip"}
    entries.append(entry);cards.append({"id":"v2-listing-"+platform,"title":label+" · V2 listing and package","category":"app",
      "status":"Review","kind":"file","preview":entry["copy"],"description":"V2 neutral listing draft and screenshot package.","appGroups":["listing"],
      "downloads":[dl(V/f"{platform}-listing.md","Markdown"),dl(V/f"downloads/openline-v2-{platform}.zip","Submission ZIP")]})
files=[]
for p in sorted(V.rglob("*")):
    if not p.is_file():continue
    rel=p.relative_to(PUB).as_posix();ext=p.suffix[1:].upper();g=["screenshots"]
    if "/icons/" in rel or "icons.zip" in rel:g=["icons"]
    elif "/screens/" in rel:g=["source"]
    elif "/downloads/" in rel or ext in ("MD","JSON"):g=["listing"]
    files.append({"id":"v2-file-"+hashlib.sha1(rel.encode()).hexdigest()[:12],"path":rel,"url":"./"+rel,"title":p.stem.replace("-"," "),
      "category":"app","status":"Review","kind":"image" if ext in ("PNG","WEBP","SVG","JPG") else "file",
      "format":"JPEG" if ext=="JPG" else ext,"bytes":p.stat().st_size,"appGroups":g})
cat["appLibraryV2"]={"rows":rows,"entries":entries,"cards":cards,"files":files,"icon":icon["preview"]}
cat["version"]="2.6.0"
save(PUB/"library/catalog.json",cat)
changed=["library/catalog.json"]+[f["path"] for f in files]
save(STATE/"public-changed-files.json",changed)
for name in ("package.json","package-lock.json"):
    v=read(APP/name);v["version"]="2.6.0"
    if "packages" in v:v["packages"][""]["version"]="2.6.0"
    save(APP/name,v)
sources=("src.jsx","AppStoreHub.jsx","LaunchHome.jsx","library.css","launch-home.css","FLOWS.md","package.json","package-lock.json")
for name in sources:
    a=APP/name;b=REPO/"brand-library"/name
    if not b.exists() or not a.samefile(b):shutil.copy2(a,b)
# Small configuration needed by Vite is committed; generated media is hydrated from Fly.
dest=REPO/"brand-library/public/app-v2";dest.mkdir(parents=True,exist_ok=True)
if not (dest/"copy.json").exists() or not (V/"copy.json").samefile(dest/"copy.json"):shutil.copy2(V/"copy.json",dest/"copy.json")
inv=read(REPO/"brand-library/PUBLIC-ASSETS.json");index={f["path"]:f for f in inv["files"]}
for name in changed:
    b=(PUB/name).read_bytes();index[name]={"path":name,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"url":"https://brand.openline.com/"+name}
inv["files"]=list(index.values());inv["total_bytes"]=sum(f["bytes"] for f in inv["files"])
save(REPO/"brand-library/PUBLIC-ASSETS.json",inv)
save(STATE/"qa-summary.json",{"v1_files_unchanged":len(before),"screenshots":24,"v2_files":len(files),"icon_scale":1.125,"zip_integrity":"passed"})
print(json.dumps({"screenshots":24,"v2_files":len(files),"v1_unchanged":len(before),"size_mb":sum(f["bytes"] for f in files)/1e6}))
