"""Normalize the reviewed Final batch into the library's integration schema."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent / "openline-brand-expansion/campaign-final-twenty"
STATE = ROOT.parent / "openline-fly-deployment/final-media-v2-5"
STATE.mkdir(parents=True, exist_ok=True)
manifest = json.loads((WORK / "manifest.json").read_text())
public = json.loads((WORK / "public-files.json").read_text())
qa = json.loads((WORK / "qa-summary.json").read_text())
assert manifest["qa"]["status"] == "complete"
assert len(qa["ads"]) == 20
for row in qa["ads"]:
    assert row["technical"]["pass"]
    assert row["audio_review"]["matches"]
    assert not row["audio_review"].get("issues")
    assert not row["visual_review"].get("critical_issues")
    tech = row["technical"]
    tech.pop("ai_badge_verified_in_all_six_outro_samples", None)
    tech["qr_sample_count"] = len(tech["qr_tests"])
manifest["qa"].pop("every_ad_qr_tested_at_six_outro_times", None)
manifest["qa"]["every_ad_qr_tested_through_outro"] = True
safe_storyboards = {"ads": [
    {key: ad[key] for key in ("id", "title", "destination", "narration", "storyboard")}
    for ad in manifest["ads"]
]}
cards = []
assert len(manifest["ads"]) == 20
for ad in manifest["ads"]:
    downloads = []
    for key, label in [
        ("mp4", "MP4 master"), ("poster", "Poster JPEG"),
        ("caption_srt", "English SRT"), ("caption_vtt", "English VTT"),
        ("word_timestamps", "Word timing JSON"), ("storyboard_image", "Storyboard JPEG"),
    ]:
        if ad.get(key):
            assert ad[key] in public
            downloads.append({"path": ad[key], "label": label})
    cards.append({
        "id": ad["id"], "title": ad["title"], "description": ad["description"],
        "kind": "video", "duration": ad["duration_seconds"],
        "preview": ad["mp4"], "poster": ad["poster"], "script": ad["narration"],
        "disclosure": ad["disclosure"], "downloads": downloads,
        "tags": ["Final batch", ad["destination"], ad["theme"], "Voiced campaign"],
    })
spec = {
    "qa_approved": True,
    "campaign": {**manifest["ui"], "count": 20},
    "groups": [{
        "root": str(WORK), "series": "campaign-final-twenty", "category": "ads",
        "batch": "final", "public_files": public, "cards": cards,
        "sanitized_json": {"storyboards.json": safe_storyboards,
                           "manifest.json": manifest, "qa-summary.json": qa},
    }],
}
path = STATE / "integration-spec.json"
path.write_text(json.dumps(spec, indent=2) + "\n")
print(f"Prepared {len(cards)} reviewed cards with sanitized public metadata.")
