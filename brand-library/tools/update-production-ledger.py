from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];PROD=ROOT.parent/"openline-brand-expansion"
path=PROD/"cost-ledger.json";d=json.loads(path.read_text())
base=d.setdefault("before_brand_library_v2",dict(d["reported_costs"]))
presenters=json.loads((PROD/"presenters-long/receipts/summary.json").read_text())
ad=json.loads((PROD/"ads-volume-three/receipts/usage.json").read_text())
adcost=ad.get("total_actual_cost_usd",ad.get("cost_usd",sum(u.get("cost",0) for u in ad.get("usages",[]))))
copycost=sum(json.loads(p.read_text()).get("usage",{}).get("cost",0) for p in (ROOT/"tools/editorial").glob("*response.json"))
newor=adcost+copycost+presenters["openrouter_actual_usd"]
newrw=presenters["new_runware_actual_usd"]
d["budget_caps"]["Runware"]=60
d["reported_costs"]={"OpenRouter":round(base["OpenRouter"]+newor,10),"Runware":round(base["Runware"]+newrw,10)}
d["brand_library_v2"]={"OpenRouter":{"ads":adcost,"library_copy":copycost,"presenters_script_and_qa":presenters["openrouter_actual_usd"]},"Runware":{"new_presenter_segments":newrw,"retakes":presenters["retakes"]},"local_rendering_paid_api_cost":0}
assert d["reported_costs"]["Runware"]<=60 and d["reported_costs"]["OpenRouter"]<=30
path.write_text(json.dumps(d,indent=2))
public={"currency":"USD","budget_caps":d["budget_caps"],"cumulative_api_reported_costs":d["reported_costs"],"this_expansion":d["brand_library_v2"],"scope":"API-reported generation charges for this brand expansion only. Excludes Computer credits, taxes and unrelated account activity."}
(ROOT/"public/library/production-costs.json").write_text(json.dumps(public,indent=2))
print(json.dumps(public,indent=2))
