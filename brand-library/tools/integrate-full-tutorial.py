"""Publish only reviewed tutorial deliverables; preserve the current library."""
from pathlib import Path
import os, json, hashlib, shutil, zipfile, subprocess

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT.parent/"openline-brand-expansion"
WORK=EXP/"hellen-full-tutorial"
OUT=WORK/"deliverables";PRIVATE=WORK/"private";PUB=ROOT/"public"
STATE=ROOT.parent/"openline-fly-deployment/tutorial-v2-2"
STATE.mkdir(parents=True,exist_ok=True)
catpath=PUB/"library/catalog.json"
baseline=STATE/"catalog-before.json"
if not baseline.exists():shutil.copy2(catpath,baseline)
catalog=json.loads(baseline.read_text())
qa=json.loads((PRIVATE/"final-review.json").read_text())
assert qa["pass"] and not qa.get("material_issues"),qa
tech=json.loads((PRIVATE/"technical-qa.json").read_text())
assert tech["complete_decode"] and tech["qr"]=="https://openline.com"
script=json.loads((OUT/"script.json").read_text())
duration=float(tech["video"]["format"]["duration"])
assert 60<=duration<=100
changed=set()

def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+".new")
    tmp.write_text(json.dumps(obj,indent=2)+"\n");tmp.replace(path)
    if path.is_relative_to(PUB):changed.add(str(path.relative_to(PUB)))

rw=0
for job in ("portrait-v2","tts","avatar-v2"):
    complete=PRIVATE/f"{job}-complete.json"
    row=json.loads(complete.read_text()) if complete.exists() else json.loads((PRIVATE/f"{job}-response.json").read_text())["data"][0]
    rw+=float(row.get("cost",0))
or_cost=sum(float(json.loads(p.read_text()).get("usage",{}).get("cost",0))
            for p in PRIVATE.glob("*-response.json"))
ledgerpath=EXP/"cost-ledger.json"
ledger=json.loads(ledgerpath.read_text())
before=ledger.setdefault("before_full_tutorial",dict(ledger["reported_costs"]))
ledger["budget_caps"]["Runware"]=100
ledger["reported_costs"]={**before,"Runware":round(before["Runware"]+rw,9),
                         "OpenRouter":round(before["OpenRouter"]+or_cost,9)}
assert ledger["reported_costs"]["Runware"]<100
ledger["full_hellen_tutorial"]={"Runware":round(rw,9),"OpenRouter_confirmed":round(or_cost,9),
    "scope":"Office portrait, one continuous narration, one continuous avatar render, editorial and audiovisual review",
    "validation_rejections":"Two pre-generation validation errors; no returned charge. Not assumed a complete billing statement."}
save(ledgerpath,ledger)
publicledger=PUB/"brand-expansion/downloads/cost-ledger.json"
summary=json.loads(publicledger.read_text())
summary["budget_caps"]=ledger["budget_caps"]
summary["cumulative_api_reported_costs"]=ledger["reported_costs"]
summary["latest_full_tutorial"]={"Runware":round(rw,9),"OpenRouter_confirmed":round(or_cost,9)}
summary["reconciliation"]="OpenRouter confirmed receipts only; two historical blank-response calls remain unreconciled. Validation-rejected Runware requests returned no cost; charges are not inferred."
save(publicledger,summary)

notes="""# Hellen: Openline eSIM installation tutorial

## Finished illustrated edition

An approximately 89-second, 1920×1080 landscape tutorial with one continuous fictional presenter take and one uninterrupted Ashley narration pass. Hellen is shown in a generated, softly blurred open-plan office setting. It is not a photograph or recording of an actual Openline office, and no New York location is claimed in the narration.

The right-hand panel is a clearly labeled illustrated guide, not genuine iPhone footage or a simulated Apple interface. The presenter remains visible from start to finish; only the illustration panel crossfades. The opening and closing use Openline's original logo geometry and motion. The final QR points to https://openline.com, not to an installable eSIM.

## Procedure and limits

The guide presents QR scanning and manual entry as alternatives, includes compatible/unlocked-device and Wi-Fi prerequisites, explains the supplied SM-DP+ and activation fields, and separates home-line settings from Openline data settings. Menu labels and order vary by iOS, region and provider. General QR and manual steps were checked against [Apple's eSIM setup documentation](https://support.apple.com/en-us/118669).

Openline-specific settings were checked against the [Openline installation guide](https://staging.openline.com/installation-guide). That page contains conflicting activation-timing statements, so this video directs viewers to their individual plan instructions rather than asserting one universal validity trigger. It makes no single-use/reinstallation guarantee, instant-activation promise, coverage guarantee or claim that all roaming charges disappear.

## Files and production

- MP4: final composed landscape video with burned-in captions and subtle original intro/outro sound.
- WAV: original single-pass voice master, without speed changes or narration edits.
- SRT/VTT: English captions, with chapter-aligned timing and approximate individual cue boundaries.
- JSON/text: narration and timed chapter content.
- JPEG: office portrait and final-video poster.

The 1920×1080 output is a composition, not a claim that the generated presenter footage is native 1080p. Generated-avatar texture, mouth motion and blinking may still look synthetic. Automated audiovisual review supplements technical checks; it is not proof of flawless realism or a substitute for a human sign-off.

## Future real-device edition

Replace only the illustrated panel when an authorized, compatible iPhone recording is available. Redact personal information and usable eSIM credentials. Verify current menu labels and product-specific activation/reinstallation policy. Do not describe this illustrated edition as a real-device demonstration.

The library's existing samples and original approved 43.5% app icon are unchanged. No store submission or YouTube/TikTok publication is performed by this update.
"""
(OUT/"README.md").write_text(notes)
save(OUT/"manifest.json",{"title":"Hellen: full illustrated installation tutorial",
    "duration_seconds":duration,"output_resolution":"1920x1080","fps":30,
    "presenter":"Hellen04","voice":"Ashley / Inworld TTS 1.5 Max","presenter_takes":1,
    "narration_passes":1,"background":"Fictional blurred open-plan office",
    "phone_visuals":"Clearly labeled illustrated guide; not genuine iPhone footage",
    "qr_target":"https://openline.com","status":"Completed illustrated edition for owner review",
    "review":{k:v for k,v in qa.items() if k!="transcript"},
    "caption_timing":"Chapter-aligned; individual cue boundaries approximate",
    "sources":["https://support.apple.com/en-us/118669","https://staging.openline.com/installation-guide"]})

names=["openline-hellen-installation-tutorial.mp4","openline-hellen-tutorial-poster.jpg",
       "hellen-office-portrait.jpg","hellen-narration.wav","hellen-tutorial-en.srt",
       "hellen-tutorial-en.vtt","script.json","narration.txt","chapters.json","README.md","manifest.json"]
files=[];downloads=[]
labels={"mp4":"MP4 master","wav":"Voice WAV","srt":"English SRT","vtt":"English VTT",
        "txt":"Narration text","json":"Production JSON","md":"Tutorial notes"}
for name in names:
    source=OUT/name;dest=PUB/"library/hellen-full-tutorial"/name
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():dest.unlink()
    os.link(source,dest)
    rel=str(dest.relative_to(PUB));changed.add(rel);url="./"+rel
    ext=dest.suffix[1:].upper()
    label="Office portrait JPEG" if "office-portrait" in name else "Video poster JPEG" if "poster" in name else labels.get(dest.suffix[1:],ext)
    downloads.append({"label":label,"url":url,"bytes":dest.stat().st_size})
    files.append({"id":hashlib.sha1(url.encode()).hexdigest()[:12],"title":dest.stem,"path":rel,"url":url,
         "category":"presenters","series":"hellen-full-tutorial","status":"Review","format":ext,
         "bytes":dest.stat().st_size,"kind":"video" if ext=="MP4" else "audio" if ext=="WAV" else "image" if ext=="JPG" else "file","source":None})
bundle=PUB/"library/downloads/openline-hellen-full-tutorial.zip"
temp=bundle.with_suffix(".zip.new")
with zipfile.ZipFile(temp,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    for name in names:z.write(OUT/name,name)
with zipfile.ZipFile(temp) as z:assert z.testzip() is None
temp.replace(bundle);changed.add(str(bundle.relative_to(PUB)))
downloads.append({"label":"Complete tutorial ZIP","url":"./"+str(bundle.relative_to(PUB)),"bytes":bundle.stat().st_size})
disclosure="Fictional AI presenter in a generated office. One continuous presenter take and voice master. Clearly labeled illustrated installation steps, not a real iPhone recording. Mild synthetic artifacts may remain."
card={"id":"hellen-full-tutorial","title":"Hellen · full illustrated tutorial","category":"presenters",
      "series":"hellen-full-tutorial","status":"Review","description":"A complete 89-second QR and manual installation guide. One continuous Hellen take, a blurred office setting and Openline intro/outro.",
      "duration":round(duration,2),"preview":"./library/hellen-full-tutorial/openline-hellen-installation-tutorial.mp4",
      "kind":"video","poster":"./library/hellen-full-tutorial/openline-hellen-tutorial-poster.jpg",
      "downloads":downloads,"source":None,"tags":["Tutorial","Continuous take","Illustrated guide","Hellen"],
      "script":script["narration"],"disclosure":disclosure}
catalog["cards"]=[card]+catalog["cards"]
catalog["files"]=files+catalog["files"]
for item in catalog["files"]:
    if item["url"]=="./brand-expansion/downloads/cost-ledger.json":item["bytes"]=publicledger.stat().st_size
catalog["fullTutorial"]=True
catalog["tutorial"]={
    "title":"Hellen’s full installation guide",
    "summary":"The complete illustrated edition is ready: one continuous voice and presenter take, with QR and manual setup guidance. Earlier auditions remain below.",
    "description":"An 89-second guide with a softly blurred office background, readable step graphics and Openline intro/outro. This edition uses illustrations, not genuine iPhone footage.",
    "planUrl":"./library/hellen-full-tutorial/README.md",
    "gates":[{"title":"Continuous presentation","detail":"One narration pass and one presenter take. No stitched presenter clips or voice changes."},
             {"title":"Illustrated edition completed","detail":"QR and manual methods are alternatives. The visuals are labeled, with captions and downloadable source text."},
             {"title":"Future real-device edition","detail":"Swap in authorized iPhone footage and reconfirm current plan-specific rules. No universal activation-timing claim is made."}]}
catalog["bundles"].insert(0,{"category":"presenters","title":"Hellen: full illustrated tutorial",
      "url":"./"+str(bundle.relative_to(PUB)),"bytes":bundle.stat().st_size})
catalog["counts"]={c["id"]:sum(a["category"]==c["id"] for a in catalog["cards"]) for c in catalog["categories"]}
catalog["inventory"]["assetFiles"]=len(catalog["files"])
catalog["version"]="2.2.0"
save(catpath,catalog)
save(STATE/"public-change-list.json",sorted(changed))
print(json.dumps({"version":"2.2.0","files":len(changed),"costs":ledger["reported_costs"],
                  "new_runware":rw,"new_openrouter":or_cost,"bundle_bytes":bundle.stat().st_size},indent=2))
