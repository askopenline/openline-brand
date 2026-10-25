"""Record confirmed costs only; the pending avatar render is not a billed result."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT.parent / "openline-brand-expansion"
PUB = ROOT / "public"
STATE = ROOT.parent / "openline-fly-deployment/final-media-v2-5"
ads = json.loads((EXP / "campaign-final-twenty/PROGRESS.json").read_text())
tutorial = json.loads((EXP / "hellen-tutorial-v3/RESUME.json").read_text())["reported_costs"]
costs = {
    "Runware": ads["runware_actual_usd"] + tutorial["Runware_reported_so_far"],
    "OpenRouter": ads["openrouter_actual_usd"] + tutorial["OpenRouter_reported_so_far"],
}


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".new")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


path = EXP / "cost-ledger.json"
ledger = json.loads(path.read_text())
before = ledger.setdefault("before_final_media", dict(ledger["reported_costs"]))
ledger["reported_costs"] = {key: round(before[key] + costs[key], 9) for key in costs}
entry = {
    "additional_approved_api_cap_usd": 200,
    "reported_costs": {key: round(value, 9) for key, value in costs.items()},
    "ads": {"Runware": ads["runware_actual_usd"], "OpenRouter": ads["openrouter_actual_usd"]},
    "tutorial_status": "Avatar processing; status endpoint unavailable. Final charge not yet returned.",
    "tutorial_reported_so_far": {"Runware": tutorial["Runware_reported_so_far"],
                               "OpenRouter": tutorial["OpenRouter_reported_so_far"]},
}
ledger["final_media"] = entry
save(path, ledger)
path = PUB / "brand-expansion/downloads/cost-ledger.json"
summary = json.loads(path.read_text())
summary["cumulative_api_reported_costs"] = ledger["reported_costs"]
summary["latest_final_media"] = entry
save(path, summary)
catalog_path = PUB / "library/catalog.json"
catalog = json.loads(catalog_path.read_text())
for item in catalog["files"]:
    if item["url"] == "./brand-expansion/downloads/cost-ledger.json":
        item["bytes"] = path.stat().st_size
save(catalog_path, catalog)
changed = set(json.loads((STATE / "public-changed-files.json").read_text()))
changed.add("brand-expansion/downloads/cost-ledger.json")
save(STATE / "public-changed-files.json", sorted(changed))
print(json.dumps(entry))
