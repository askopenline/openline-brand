from pathlib import Path
import json,hashlib,sys,re,zipfile
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1];PUB=ROOT/"public"
d=json.loads((PUB/"library/catalog.json").read_text())
errors=[]
def check_url(u,label):
    if not u or not u.startswith("./"):errors.append(label+": invalid local URL");return
    p=PUB/unquote(u[2:])
    if not p.is_file():errors.append(label+": missing "+str(p))
for a in d["cards"]:
    check_url(a["preview"],a["id"])
    if a["poster"]:check_url(a["poster"],a["id"]+" poster")
    for x in a["downloads"]:check_url(x["url"],a["id"]+" download")
for a in d["files"]:
    check_url(a["url"],a["id"])
    p=PUB/unquote(a["url"][2:])
    if p.is_file() and p.stat().st_size!=a["bytes"]:errors.append(a["id"]+": size changed")
for key in ("cards","files"):
    ids=[a["id"] for a in d[key]]
    if len(ids)!=len(set(ids)):errors.append(key+": duplicate IDs")
icon=hashlib.sha256((PUB/"assets/apple-icon-1024.png").read_bytes()).hexdigest()
if icon!="5bded92247397e8999be6d0f668bbb7facca064136dbfe45a043d0fc9e54b60b":errors.append("Approved icon changed")
readme=[a for a in d["cards"] if a["id"].startswith("readme-motion-twelve-")]
if len(readme)!=12 or any(a["duration"]<10 for a in readme):errors.append("Original GIF collection incomplete")
if "--complete" in sys.argv:
    campaign=[a for a in d["cards"] if a["category"]=="ads" and a.get("series","").startswith("campaign-voice-ten")]
    expected_ads=40 if d.get("campaign") else 30
    if d["counts"]["ads"]!=expected_ads:errors.append(f"Expected {expected_ads} ads")
    long_presenters=[a for a in d["cards"] if a["category"]=="presenters" and a["id"] not in ("hellen-continuity-pilot","hellen-full-tutorial")]
    if len(long_presenters)!=4:errors.append("Expected four retained longer presenters")
    if any(a["duration"]<23 for a in long_presenters):errors.append("Long presenter too short")
    if d.get("campaign"):
        if len(campaign)!=10:errors.append("Expected ten voiced campaign ads")
        if any(not (20<=a["duration"]<=30) for a in campaign):errors.append("Unexpected campaign duration")
        if any(not a.get("script") or not any(x["url"].endswith(".vtt") for x in a["downloads"]) for a in campaign):errors.append("Campaign script or captions missing")
    if d.get("tutorial"):
        pilots=[a for a in d["cards"] if a["id"]=="hellen-continuity-pilot"]
        if len(pilots)!=1 or not (10<=pilots[0]["duration"]<=16):errors.append("Continuity pilot missing or wrong duration")
        expected_presenters=6 if d.get("fullTutorial") else 5
        if d["counts"]["presenters"]!=expected_presenters:errors.append(f"Expected {expected_presenters} presenter entries")
    if d.get("fullTutorial"):
        full=[a for a in d["cards"] if a["id"]=="hellen-full-tutorial"]
        if len(full)!=1 or not 60<=full[0]["duration"]<=100:errors.append("Full tutorial duration/card wrong")
        if full and (not full[0].get("script") or "illustrated" not in full[0].get("disclosure","").lower()):errors.append("Full tutorial script/disclosure missing")
    if d.get("campaign"):
        bundles=[PUB/"library/downloads/openline-ten-voiced-campaign-ads.zip"]
        if d["campaign"].get("revision")==2:
            bundles.append(PUB/"library/downloads/openline-ten-voiced-campaign-ads-v2.zip")
            if not any(c["id"]=="original-voiced-campaign-archive" for c in d["cards"]):errors.append("Original campaign archive missing")
        for bundle in bundles:
            with zipfile.ZipFile(bundle) as z:
                if z.testzip():errors.append("Campaign ZIP integrity failure")
                if len([n for n in z.namelist() if n.endswith(".mp4")])!=10:errors.append("Campaign ZIP MP4 count wrong")
                for name in z.namelist():
                    if any(x in Path(name).parts for x in ("private","_private","receipts","requests",".env")):errors.append("Private archive member: "+name)
                    if Path(name).suffix.lower() in (".json",".txt",".md",".py"):
                        text=z.read(name).decode("utf-8",errors="replace")
                        if re.search(r'sk-or-v1-[A-Za-z0-9]{15,}|\"taskUUID\"|\"task_uuid\"|\"Authorization\"\\s*:',text):errors.append("Private provider material in "+name)
report={"passed":not errors,"errors":errors,"cards":len(d["cards"]),"files":len(d["files"]),"counts":d["counts"],"repository":d["inventory"],"approved_icon_sha256":icon,"original_gif_editions":len(readme),"complete_gate":"--complete" in sys.argv}
(ROOT/"library-validation.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if errors:sys.exit(1)
