"""Sanitize public copies only; preserve originals and media byte-for-byte."""
from pathlib import Path
import hashlib
import json
import os
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "public"
DOWN = PUB / "brand-expansion/downloads"
NOTE = "PUBLIC-CONTENTS.txt"
summary = (PUB / "library/production-costs.json").read_bytes()

def replace_file(path, data):
    if path.exists() and path.read_bytes() == data:
        return
    temp = path.with_name(path.name + ".safe-tmp")
    temp.write_bytes(data)
    os.replace(temp, path)  # Break hardlinks; never change original source copies.

def sanitize_zip(path, replacements=None):
    replacements = replacements or {}
    with zipfile.ZipFile(path) as original:
        if NOTE in original.namelist():
            return
        temp = path.with_suffix(".safe-tmp")
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=3) as output:
            for entry in original.infolist():
                parts = Path(entry.filename).parts
                name = Path(entry.filename).name
                if "receipts" in parts or name in ("create_storyboards.py", "correct_copy.py"):
                    continue
                if name.endswith("-response.json") and "qa" in parts:
                    continue
                data = original.read(entry)
                if name == "cost-ledger.json":
                    data = summary
                elif name in replacements:
                    data = replacements[name].read_bytes()
                output.writestr(entry, data)
            output.writestr(NOTE, "Public distribution: private API requests, responses and receipts are excluded. Historical detailed ledgers are replaced by the current aggregate summary. Original creative media is unchanged. Unmodified production sources remain in the private working archive.\n")
    with zipfile.ZipFile(temp) as check:
        assert check.testzip() is None
    os.replace(temp, path)

sanitize_zip(DOWN / "openline-six-additional-ads-volume-two.zip")
sanitize_zip(DOWN / "openline-presenter-comparison.zip")
sanitize_zip(DOWN / "openline-brand-expansion.zip", {
    name: DOWN / name for name in (
        "openline-six-additional-ads-volume-two.zip",
        "openline-presenter-comparison.zip",
    )
})
replace_file(DOWN / "cost-ledger.json", summary)
checksums = {
    p.name: hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(DOWN.iterdir()) if p.is_file() and p.name != "checksums.json"
}
replace_file(DOWN / "checksums.json", json.dumps(checksums, indent=2).encode())

helper = """// Public-distribution hardening: escape local editable text before HTML interpolation.
function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
"""
patches = {
    "notes.html": ["n.title", "fmt(n.date)", "n.body.replace(/#+ /g,'').slice(0,80)", "t"],
    "database.html": [
        "e.name", "e.status", "e.country", "e.contact", "e.priority", "e.mrr",
        "e.notes", "e.lastContact", "e.tags.join(', ')", "entry[field]", "t",
        "init", "formatDate(e.lastContact)", "countryNames[e.country]||e.country",
    ],
}
changed = []
for name, expressions in patches.items():
    path = PUB / "library/repository/workadventure/apps" / name
    text = path.read_text()
    if "function escapeHtml(value)" not in text:
        text = text.replace("<script>", "<script>\n" + helper, 1)
        for expr in expressions:
            text = text.replace("${" + expr + "}", "${escapeHtml(" + expr + ")}")
        replace_file(path, text.encode())
    changed.append(str(path.relative_to(PUB)))

catalog_path = PUB / "library/catalog.json"
catalog = json.loads(catalog_path.read_text())
from urllib.parse import unquote
for row in catalog["files"]:
    path = PUB / unquote(row["url"].removeprefix("./"))
    row["bytes"] = path.stat().st_size
    if row["path"] in changed:
        row["status"] = "Hardened source"
for card in catalog["cards"]:
    for download in card["downloads"]:
        download["bytes"] = (PUB / unquote(download["url"].removeprefix("./"))).stat().st_size
    if card["id"] in ("wa-notes", "wa-database"):
        card["description"] = "Virtual-office interface preview. Public source includes local-input escaping fixes; the linked GitHub revision is the original."
catalog["publicHardening"] = {
    "privateProductionPayloadsExcluded": True,
    "aggregateCostsOnly": True,
    "patchedSourceFiles": changed,
    "originalSourceCommit": catalog["sourceCommit"],
}
replace_file(catalog_path, json.dumps(catalog, ensure_ascii=False, separators=(",", ":")).encode())
print(json.dumps({"sanitized": True, "patched_sources": changed, "media_modified": False}))
