import json,re,hashlib,subprocess
from pathlib import Path
from PIL import Image,ImageChops
APP=Path(__file__).resolve().parents[1];PUB=APP/"public";V=PUB/"app-v2"
STATE=APP.parent/"openline-fly-deployment/app-v2-v2-6-0"
checks=[]
images=list((V/"screens").glob("*.png"))
images+=list((V/"marketing").glob("*/*.png"))+list((V/"submission").glob("*/*.png"))
for p in images:
    text=subprocess.run(["tesseract",str(p),"stdout","--psm","11"],capture_output=True,text=True,check=True).stdout
    hits=re.findall(r"[$€£¥₹₽]|\b(?:prices?|savings|cheap|checkout|payment|refund|buy|purchased|purchase|value)\b",text,re.I)
    checks.append({"path":p.relative_to(PUB).as_posix(),"hits":hits,"ocr":text})
def bbox(p):
    im=Image.open(p).convert("RGB");mask=ImageChops.difference(im,Image.new("RGB",im.size,"white")).convert("L").point(lambda x:255 if x>18 else 0)
    b=mask.getbbox();return {"width":b[2]-b[0],"height":b[3]-b[1],"bbox":b}
a=bbox(PUB/"assets/icon-43.5-light.png");b=bbox(V/"icons/openline-icon-white-1024.png")
ratio=b["width"]/a["width"];assert 1.10<=ratio<=1.15
snap=json.loads((STATE/"v1-hashes.json").read_text())
assert all(hashlib.sha256((PUB/n).read_bytes()).hexdigest()==h for n,h in snap.items())
result={"ocr":checks,"flagged":[r for r in checks if r["hits"]],"icon_v1":a,"icon_v2":b,"measured_width_ratio":ratio,"v1_preserved":len(snap)}
(STATE/"detailed-qa.json").write_text(json.dumps(result,indent=2))
print(json.dumps({"ocr_images":len(checks),"flagged":[{"path":r["path"],"hits":r["hits"]} for r in checks if r["hits"]],"icon_ratio":ratio,"v1_preserved":len(snap)}))
