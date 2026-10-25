"""Integrate reviewed, explicitly whitelisted media without replacing prior editions.

The private integration spec normalizes producer manifests. It contains no secrets
and is not itself a public asset. Paid generation and QA happen before this step.
"""
import argparse
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
STATE = ROOT.parent / "openline-fly-deployment/final-media-v2-5"
FORBIDDEN = {"private", "_private", "receipts", "requests", ".git", "node_modules"}
parser = argparse.ArgumentParser()
parser.add_argument("--spec", type=Path, required=True)
args = parser.parse_args()
spec = json.loads(args.spec.read_text())
assert spec.get("qa_approved") is True, "Finish media review before integration."
STATE.mkdir(parents=True, exist_ok=True)
baseline = STATE / "catalog-before.json"
if not baseline.exists():
    shutil.copy2(PUBLIC / "library/catalog.json", baseline)
catalog = json.loads(baseline.read_text())
changed = set()
new_cards = []
new_files = []


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".new")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temp.replace(path)


for group in spec["groups"]:
    source_root = Path(group["root"]).resolve()
    series = group["series"]
    assert "/" not in series and series not in FORBIDDEN
    prefix = f"library/{series}/"
    files = set(group["public_files"])
    resources = {}
    for name in sorted(files):
        rel = Path(name)
        assert not rel.is_absolute() and ".." not in rel.parts
        assert not FORBIDDEN.intersection(rel.parts)
        assert rel.suffix.lower() not in {".py", ".env", ".log", ".sh"}
        source = source_root / rel
        assert source.is_file(), source
        target = PUBLIC / prefix / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if name in group.get("sanitized_json", {}):
            save(target, group["sanitized_json"][name])
        elif target.exists() and not os.path.samefile(source, target):
            target.unlink()
        if not target.exists():
            try:
                os.link(source, target)
            except OSError as error:
                if error.errno != errno.EXDEV:
                    raise
                # Temporary cross-filesystem media is streamed as regular bytes
                # to Fly. It is not exposed as a symlink in the remote release.
                resolved = source.resolve()
                assert str(resolved).startswith("/dev/shm/openline-")
                assert not FORBIDDEN.intersection(resolved.parts)
                os.symlink(resolved, target)
        url = "./" + prefix + name
        ext = rel.suffix[1:].upper()
        row = {
            "id": hashlib.sha1(url.encode()).hexdigest()[:12],
            "title": rel.stem, "path": prefix + name, "url": url,
            "category": group["category"], "series": series, "status": "Review",
            "format": ext, "bytes": target.stat().st_size,
            "kind": "video" if ext in {"MP4", "WEBM"} else
                    "audio" if ext in {"WAV", "MP3"} else
                    "image" if ext in {"JPG", "JPEG", "PNG", "GIF", "WEBP"} else "file",
            "source": None,
        }
        if group.get("batch"):
            row["batch"] = group["batch"]
        new_files.append(row)
        resources[name] = row
        changed.add(prefix + name)
    for item in group["cards"]:
        card = dict(item)
        card.update(category=group["category"], series=series, status="Review", source=None)
        if group.get("batch"):
            card.update(batch=group["batch"], batchLabel="Final batch")
        for key in ("preview", "poster"):
            assert card[key] in resources, (card["id"], key, card[key])
            card[key] = resources[card[key]]["url"]
        downloads = []
        for download in card["downloads"]:
            row = resources[download["path"]]
            downloads.append({"label": download["label"], "url": row["url"], "bytes": row["bytes"]})
        card["downloads"] = downloads
        new_cards.append(card)

assert len({c["id"] for c in new_cards}) == len(new_cards)
assert len([c for c in new_cards if c.get("batch") == "final"]) == 20
catalog["cards"] = new_cards + catalog["cards"]
catalog["files"] = new_files + catalog["files"]
assert len({c["id"] for c in catalog["cards"]}) == len(catalog["cards"])
assert len({f["id"] for f in catalog["files"]}) == len(catalog["files"])
catalog["finalCampaign"] = spec["campaign"]
if spec.get("tutorial"):
    catalog["tutorial"] = spec["tutorial"]
    catalog["fullTutorial"] = True
    catalog["fullTutorialId"] = spec["tutorial_card_id"]
    assert any(c["id"] == catalog["fullTutorialId"] for c in new_cards)
catalog["version"] = "2.5.0"
catalog["counts"] = {
    category["id"]: sum(card["category"] == category["id"] for card in catalog["cards"])
    for category in catalog["categories"]
}
assert catalog["counts"]["ads"] == 60
assert catalog["counts"]["motion"] == 150
catalog["inventory"]["assetFiles"] = len(catalog["files"])
save(PUBLIC / "library/catalog.json", catalog)
changed.add("library/catalog.json")
save(STATE / "public-changed-files.json", sorted(changed))
save(STATE / "integration-summary.json", {
    "new_cards": len(new_cards), "new_files": len(new_files),
    "counts": catalog["counts"], "preserved_previous_editions": True,
})
print(json.dumps({"new_cards": len(new_cards), "new_files": len(new_files),
                  "counts": catalog["counts"]}))
