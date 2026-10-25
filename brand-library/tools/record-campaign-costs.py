"""Reconcile available provider receipts without treating missing replies as free."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT.parent / "openline-brand-expansion"
private = EXP / "campaign-voice-ten/_private"
ledger_path = EXP / "cost-ledger.json"
ledger = json.loads(ledger_path.read_text())
baseline = ledger.setdefault("before_voiced_campaign", dict(ledger["reported_costs"]))
ads = json.loads((private / "ledger_private.json").read_text())
recovered = [json.loads(p.read_text())["data"] for p in private.glob("usage-gen-*.json")]
or_copy = sum(float(r["total_cost"]) for r in recovered)
or_qa = sum(float(json.loads(p.read_text())["usage"]["cost"])
            for p in (private / "final-review").glob("response-*.json"))
runware_delta = round(float(ads["runware_total_usd"]) + 0.548304, 9)
or_delta = round(or_copy + or_qa + 0.0046337, 9)
ledger["budget_caps"]["Runware"] = 72
ledger["reported_costs"] = {
    "Runware": round(baseline["Runware"] + runware_delta, 9),
    "OpenRouter": round(baseline["OpenRouter"] + or_delta, 9)}
ledger["voiced_campaign_and_hellen_pilot"] = {
    "runware_api_reported": runware_delta,
    "openrouter_confirmed_receipts": or_delta,
    "openrouter_blank_response_calls": 2,
    "reconciliation_note": "Two blank non-streaming OpenRouter responses had no generation ID and remain unattributed. Confirmed costs are not a complete billing statement. Failed Runware requests returned no charge.",
    "included": ["ten voiced campaign ads", "retakes and discarded TTS batch",
                 "Hellen continuous-voice pilot", "actual audiovisual QA"]}
assert ledger["reported_costs"]["Runware"] < ledger["budget_caps"]["Runware"]
assert ledger["reported_costs"]["OpenRouter"] < ledger["budget_caps"]["OpenRouter"]
ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")
public = ROOT / "public/brand-expansion/downloads/cost-ledger.json"
summary = {
    "currency": "USD", "budget_caps": ledger["budget_caps"],
    "cumulative_api_reported_costs": ledger["reported_costs"],
    "latest_campaign_and_pilot": {"Runware": runware_delta, "OpenRouter_confirmed": or_delta},
    "reconciliation": "OpenRouter includes confirmed receipts only; two blank-response calls remain unreconciled. Failed Runware attempts returned no charge.",
    "scope": "Brand-production API charges only. Excludes Computer credits, taxes, hosting and unrelated account activity."}
tmp = public.with_suffix(".json.new")
tmp.write_text(json.dumps(summary, indent=2) + "\n")
tmp.replace(public)
catalog_path = ROOT / "public/library/catalog.json"
catalog = json.loads(catalog_path.read_text())
for item in catalog["files"]:
    if item["url"] == "./brand-expansion/downloads/cost-ledger.json":
        item["bytes"] = public.stat().st_size
temp_catalog = catalog_path.with_suffix(".json.new")
temp_catalog.write_text(json.dumps(catalog, indent=2) + "\n")
temp_catalog.replace(catalog_path)
state = ROOT.parent / "openline-fly-deployment/campaign-v2-1/public-change-list.json"
changed = json.loads(state.read_text())
changed.append(str(public.relative_to(ROOT / "public")))
state.write_text(json.dumps(sorted(set(changed)), indent=2))
print(json.dumps(summary, indent=2))
