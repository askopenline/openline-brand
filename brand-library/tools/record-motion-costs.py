from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];EXP=ROOT.parent/"openline-brand-expansion";WORK=EXP/"motion-150"
docs=sum(float(json.loads(p.read_text()).get("usage",{}).get("cost",0) or 0) for p in (WORK/"private/docs").glob("*.json") if p.name.startswith(("draft-","review-","final-corrections")))
review=float(json.loads((WORK/"private/audiovisual-review-response.json").read_text()).get("usage",{}).get("cost",0) or 0)
path=EXP/"cost-ledger.json";d=json.loads(path.read_text());prior=d.setdefault("before_motion_150",dict(d["reported_costs"]))
d["reported_costs"]={**prior,"OpenRouter":round(prior["OpenRouter"]+docs+review,9)}
d["motion_150"]={"Runware":0,"OpenRouter_documents":round(docs,9),"OpenRouter_representative_media_review":review}
path.write_text(json.dumps(d,indent=2)+"\n")
pub=ROOT/"public/brand-expansion/downloads/cost-ledger.json";j=json.loads(pub.read_text())
j["cumulative_api_reported_costs"]=d["reported_costs"];j["latest_motion_expansion"]=d["motion_150"]
temp=pub.with_suffix(".new");temp.write_text(json.dumps(j,indent=2)+"\n");temp.replace(pub)
cat=ROOT/"public/library/catalog.json";c=json.loads(cat.read_text())
for f in c["files"]:
 if f["url"]=="./brand-expansion/downloads/cost-ledger.json":f["bytes"]=pub.stat().st_size
temp=cat.with_suffix(".new");temp.write_text(json.dumps(c,indent=2)+"\n");temp.replace(cat)
state=ROOT.parent/"openline-fly-deployment/motion-v2-4/public-change-list.json";changes=json.loads(state.read_text())
state.write_text(json.dumps(sorted(set(changes+["brand-expansion/downloads/cost-ledger.json"])),indent=2))
print(json.dumps(d["motion_150"],indent=2))
