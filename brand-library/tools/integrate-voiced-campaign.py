"""Index explicit public campaign/pilot deliverables without generation receipts."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import zipfile
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "public"
EXP = ROOT.parent / "openline-brand-expansion"
STATE = ROOT.parent / "openline-fly-deployment" / "campaign-v2-1"
STATE.mkdir(parents=True, exist_ok=True)
CAT = PUB / "library/catalog.json"
if not (STATE / "catalog-before.json").exists():
    shutil.copy2(CAT, STATE / "catalog-before.json")
catalog = json.loads((STATE / "catalog-before.json").read_text())
new_files, new_cards, changed = [], [], set()

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    # Public files may be hardlinked to a prior build. Replace, never truncate.
    tmp = path.with_suffix(path.suffix + ".new")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    tmp.replace(path)
    changed.add(str(path.relative_to(PUB)))

def stage(root, rel, collection, category, label=None):
    source = (root / rel).resolve()
    assert source.is_relative_to(root.resolve()) and source.is_file(), rel
    assert not any(x in Path(rel).parts for x in ("private", "_private", "requests", "receipts"))
    destination = PUB / "library" / collection / rel
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if not os.path.samefile(source, destination):
            destination.unlink()
            os.link(source, destination)
    else:
        os.link(source, destination)
    path = str(destination.relative_to(PUB))
    changed.add(path)
    url = "./" + quote(path, safe="/")
    extension = destination.suffix[1:].upper()
    kind = "video" if extension == "MP4" else "audio" if extension in ("WAV", "MP3") else "image" if extension in ("JPG", "JPEG", "PNG", "GIF") else "file"
    if not any(f["url"] == url for f in new_files):
        new_files.append({"id": hashlib.sha1(url.encode()).hexdigest()[:12],
                          "title": label or source.stem, "path": path, "url": url,
                          "category": category, "series": collection, "status": "Review",
                          "format": "JPEG" if extension == "JPG" else extension,
                          "bytes": destination.stat().st_size, "kind": kind, "source": None})
    return {"label": label or extension, "url": url, "bytes": destination.stat().st_size}

def make_card(row, root, collection, category, identifier):
    fields = [("mp4", "MP4 master"), ("poster", "JPEG poster"), ("voice", "Voice track"), ("voice_wav", "Voice WAV"),
              ("captions", "English SRT"), ("vtt", "English VTT"), ("gif", "Silent GIF preview")]
    links = {key: stage(root, row[key], collection, category, label + (" · " + Path(row[key]).suffix[1:].upper() if key == "voice" else ""))
             for key, label in fields if row.get(key)}
    assert "mp4" in links and "poster" in links
    return {"id": identifier, "title": row["title"], "category": category,
            "series": collection, "status": "Review", "description": row["description"],
            "duration": round(row["duration_seconds"], 2), "preview": links["mp4"]["url"],
            "kind": "video", "poster": links["poster"]["url"], "downloads": list(links.values()),
            "source": None, "tags": ["Voiceover", "AI-generated", collection],
            "script": row.get("story"),
            "disclosure": row.get("disclosure")}

campaign_root = EXP / "campaign-voice-ten"
campaign = json.loads((campaign_root / "manifest.json").read_text())
review = json.loads((campaign_root / "_private/final-review/review-1.json").read_text())
review2 = json.loads((campaign_root / "_private/final-review/review-2.json").read_text())
assert len(review["reviews"]) == len(review2["reviews"]) == 5
assert all(r["pass"] for r in review["reviews"] + review2["reviews"]), "Resolve material QA issues first."
campaign["ui"] = review["ui"]
campaign["ui"]["title"] = campaign["ui"]["title"].replace(" — ", ": ")
assert len(campaign["ads"]) == 10
for i, ad in enumerate(campaign["ads"], 1):
    ad["vtt"], ad["captions"] = ad["captions"], ad["captions_srt"]
    ad.setdefault("disclosure", campaign["ui"]["disclosure"])
    new_cards.append(make_card(ad, campaign_root, "campaign-voice-ten", "ads", f"campaign-voice-{i:02d}"))
    new_cards[-1]["description"] = ad["hook"] + ". " + ad["benefit"] + "."
    storyboard = f"storyboards/{Path(ad['mp4']).stem}.json"
    if (campaign_root / storyboard).is_file():
        new_cards[-1]["downloads"].append(stage(campaign_root, storyboard, "campaign-voice-ten", "ads", "Storyboard · JSON"))
catalog["campaign"] = {**campaign["ui"], "count": len(new_cards)}

pilot_root = EXP / "hellen-continuity-pilot"
if (pilot_root / "integration.json").exists():
    pilot = json.loads((pilot_root / "integration.json").read_text())
else:
    ui = json.loads((pilot_root / "deliverables/tutorial-ui-metadata.json").read_text())
    video = "deliverables/hellen-continuity-pilot.mp4"
    duration = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(pilot_root / video)], text=True))
    pilot = {"title": "Hellen · continuity pilot", "description": ui["summary"],
             "duration_seconds": duration, "mp4": video,
             "poster": "deliverables/hellen-continuity-pilot-poster.jpg",
             "voice": "deliverables/hellen-pilot-voice.wav",
             "captions": "deliverables/hellen-pilot-captions.srt",
             "disclosure": ui["description"], "ui": ui}
new_cards.append(make_card(pilot, pilot_root, "hellen-continuity-pilot", "presenters", "hellen-continuity-pilot"))
pilot_qa = "deliverables/multimodal-qa-summary.json"
if (pilot_root / pilot_qa).is_file():
    new_cards[-1]["downloads"].append(stage(pilot_root, pilot_qa, "hellen-continuity-pilot", "presenters", "Automated QA notes · JSON"))
catalog["tutorial"] = pilot["ui"]
plan = ROOT.parent / "openline-hellen-tutorial-next-steps.md"
if plan.exists():
    link = stage(ROOT.parent, plan.name, "tutorial-plan", "docs", "Tutorial production plan")
    catalog["tutorial"]["planUrl"] = link["url"]

# Optional public supporting files only: no raw generator source or provider data.
for root, collection, category, info in (
        (campaign_root, "campaign-voice-ten", "ads", campaign),
        (pilot_root, "hellen-continuity-pilot", "presenters", pilot)):
    for rel in info.get("extras", []):
        assert Path(rel).suffix.lower() in (".md", ".txt", ".srt", ".vtt", ".png", ".jpg", ".jpeg", ".wav", ".mp3")
        stage(root, rel, collection, category)

campaign_public = PUB / "library/campaign-voice-ten"
save(campaign_public / "manifest.json", {"count": 10, "collection": catalog["campaign"],
                                      "ads": [c for c in new_cards if c["category"] == "ads"]})
archive = PUB / "library/downloads/openline-ten-voiced-campaign-ads.zip"
archive.parent.mkdir(parents=True, exist_ok=True)
temporary = archive.with_suffix(".zip.new")
with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as z:
    for path in sorted(campaign_public.rglob("*")):
        if path.is_file():
            z.write(path, str(path.relative_to(campaign_public)))
temporary.replace(archive)
superseded_zip = EXP / "openline-campaign-voice-ten.zip"
if superseded_zip.exists():
    with zipfile.ZipFile(archive) as z:
        assert len([n for n in z.namelist() if n.endswith(".mp4")]) == 10
        assert z.testzip() is None
    # Only a duplicate, unpublished packaging artifact; all source assets remain.
    superseded_zip.unlink()
changed.add(str(archive.relative_to(PUB)))
catalog.setdefault("bundles", []).insert(0, {
    "category": "ads", "title": "Ten voiced campaign ads",
    "url": "./library/downloads/" + archive.name, "bytes": archive.stat().st_size})
catalog["cards"] = new_cards + catalog["cards"]
catalog["files"] = new_files + catalog["files"]
catalog["counts"] = {c["id"]: sum(a["category"] == c["id"] for a in catalog["cards"])
                     for c in catalog["categories"]}
catalog["inventory"]["assetFiles"] = len(catalog["files"])
catalog["version"] = "2.1.0"
catalog["domainStatus"] = "Live on Fly.io; DNS and TLS verified"
save(CAT, catalog)
save(PUB / "library/campaign-voice-ten/production-notes.json", {
    "status": "Campaign concepts for review, not advertising-platform approval",
    "qrTarget": "https://openline.com",
    "sourceFootage": "AI-generated fictional travel scenes; not live Openline app footage",
    "fullTutorialStatus": "Continuity pilot only; actual device recording and plan-policy confirmation pending"})
(STATE / "public-change-list.json").write_text(json.dumps(sorted(changed), indent=2))
print(json.dumps({"version": catalog["version"], "counts": catalog["counts"],
                  "indexedFiles": len(catalog["files"]), "changedFiles": len(changed)}))
