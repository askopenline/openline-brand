"""Synchronize reviewed source and public metadata, not private production files."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent / "openline-brand-assets"
PUB = ROOT / "public"
STATE = ROOT.parent / "openline-fly-deployment/final-media-v2-5"
changed = set()


def save(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".sync-new")
    temp.write_text(text)
    temp.replace(path)
    changed.add(str(path.relative_to(REPO)))


def copy(source, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or not source.samefile(path):
        temp = path.with_name(path.name + ".sync-new")
        shutil.copy2(source, temp)
        temp.replace(path)
    changed.add(str(path.relative_to(REPO)))


for name in [
    "src.jsx", "FLOWS.md", "package.json", "package-lock.json",
    "tools/link-public.mjs", "tools/integrate-final-media.py",
    "tools/prepare-final-media-spec.py", "tools/update-final-media-ledger.py",
    "tools/sync-final-campaign-repository.py", "scripts/fly_incremental_release.py",
]:
    copy(ROOT / name, REPO / "brand-library" / name)

campaign = PUB / "library/campaign-final-twenty"
manifest = json.loads((campaign / "manifest.json").read_text())
for name in ("manifest.json", "storyboards.json", "qa-summary.json", "public-files.json"):
    copy(campaign / name, REPO / "campaign/final-batch" / name)
notes = (campaign / "README.txt").read_text()
notes = notes.replace("Final batch\n", "# Final batch\n", 1)
for heading in ("Package overview", "Limitations", "Approved public intro/disclosure"):
    notes = notes.replace(heading + ":\n", "## " + heading + "\n")
save(REPO / "campaign/final-batch/README.md", notes)
table = "\n".join(
    f"| {ad['number']:02} | {ad['title']} | [MP4](https://brand.openline.com/library/campaign-final-twenty/{ad['mp4']}) |"
    for ad in manifest["ads"]
)
campaign_doc = (
    "# Openline Campaign Ads\n\n" + manifest["ui"]["description"] +
    "\n\n[Open the Final batch](https://brand.openline.com/#/ads).\n\n"
    "## Editions\n\n"
    "- **Final batch:** 20 voiced ads, 22.08 seconds each.\n"
    "- **Voiced campaign:** 10 earlier voiced ads.\n"
    "- **Earlier work:** 30 earlier short ads.\n"
    "- **All ads:** 60 collections. Original variants remain available in Archives.\n\n"
    "## Final batch downloads\n\n| ID | Story | Download |\n|---|---|---|\n" + table +
    "\n\n## Production notes\n\n" +
    "[Public overview and limitations](../campaign/final-batch/README.md). "
    "[Manifest](../campaign/final-batch/manifest.json). "
    "[QA results](../campaign/final-batch/qa-summary.json).\n\n" +
    manifest["ui"]["disclosure"] + "\n"
)
save(REPO / "docs/CAMPAIGN-ADS.md", campaign_doc)
readme_path = REPO / "README.md"
readme = readme_path.read_text()
section = (
    "## Final batch · v2.5.0\n\n" + manifest["ui"]["description"] +
    "\n\n[Watch all 20 new ads](https://brand.openline.com/#/ads) · "
    "[Stories and downloads](docs/CAMPAIGN-ADS.md) · "
    "[Production notes](campaign/final-batch/README.md)\n\n"
    "The library now contains 60 short ads, with separate filters for Final batch, "
    "the previous voiced campaign, earlier work and all ads. Earlier editions and "
    "all 150 Motion collections are preserved.\n\n"
)
for number in (1, 6, 17):
    ad = manifest["ads"][number - 1]
    poster = REPO / f".github/assets/videos-v2.5/final-ad-{number:02}.jpg"
    poster.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-ss", "4",
        "-i", str(campaign / ad["mp4"]), "-frames:v", "1",
        "-vf", "scale=360:-1", "-q:v", "3", "-threads", "1", str(poster)
    ], check=True)
    changed.add(str(poster.relative_to(REPO)))
    section += (
        f'<a href="https://brand.openline.com/library/campaign-final-twenty/{ad["mp4"]}">'
        f'<img src=".github/assets/videos-v2.5/final-ad-{number:02}.jpg" '
        f'alt="{ad["title"]}: decoded final video frame" width="220"></a>\n'
    )
section += (
    "\nThe revised continuous Hellen tutorial is still awaiting its provider render. "
    "The existing illustrated tutorial remains available; the new tutorial is not "
    "included in this update.\n\n"
)
if "## Final batch · v2.5.0" not in readme:
    readme = readme.replace("## Expanded brand library", section + "## Expanded brand library", 1)
save(readme_path, readme)
for relative in ("brand-library/README.md", "docs/DEPLOYMENT.md", "docs/BRAND-LIBRARY.md"):
    path = REPO / relative
    if path.exists():
        text = path.read_text().replace("3GB volume", "6GB volume").replace("40 active short ads", "60 active short ads")
        save(path, text)

inventory_path = REPO / "brand-library/PUBLIC-ASSETS.json"
inventory = json.loads(inventory_path.read_text())
rows = {row["path"]: row for row in inventory["files"]}
for name in json.loads((STATE / "public-changed-files.json").read_text()):
    path = PUB / name
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    rows[name] = {"path": name, "url": "https://brand.openline.com/" + quote(name),
                  "bytes": path.stat().st_size, "sha256": digest}
inventory.update(version="2.5.0", files=sorted(rows.values(), key=lambda row: row["path"]))
inventory["total_bytes"] = sum(row["bytes"] for row in inventory["files"])
save(inventory_path, json.dumps(inventory, indent=2) + "\n")
(STATE / "repository-files.json").write_text(json.dumps(sorted(changed), indent=2) + "\n")
print(json.dumps({"repository_files": len(changed), "public_assets": len(rows)}))
