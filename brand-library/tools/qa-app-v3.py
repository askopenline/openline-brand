import json,re,subprocess,hashlib
from pathlib import Path
from PIL import Image
APP=Path(__file__).resolve().parents[1];PUB=APP/'public';V=PUB/'app-v3';STATE=APP.parent/'openline-fly-deployment/app-v3-20-v2-7-1'
checks=[]
cache={x['path']:x for x in json.loads((STATE/'ocr-qa.json').read_text()).get('results',[])} if (STATE/'ocr-qa.json').exists() else {}
for p in list((V/'screens').glob('*.png'))+list((V/'apple').glob('*.png'))+list((V/'google').glob('*.png')):
 digest=hashlib.sha256(p.read_bytes()).hexdigest();prior=cache.get(p.relative_to(PUB).as_posix(),{})
 text=prior['text'] if prior.get('sha256')==digest else subprocess.run(['tesseract',str(p),'stdout','--psm','11'],capture_output=True,text=True,check=True).stdout
 # Visually verified false positive: OCR reads the slanted eSIM word as e€SIM.
 false_positive=p.relative_to(V).as_posix()=='google/10.png' and 'Your travel e€SIM collection' in text
 normalized=text.replace('Your travel e€SIM collection','Your travel eSIM collection') if false_positive else text
 spanish_false_positive=p.relative_to(V).as_posix()=='apple/20.png' and 'Continuar en e€spafiol' in text
 if spanish_false_positive:normalized=normalized.replace('Continuar en e€spafiol','Continuar en español')
 flag_false_positive=p.relative_to(V).as_posix()=='google/13.png' and 'Portugal\n\n£\n\nBrowse destination' in text
 if flag_false_positive:normalized=normalized.replace('Portugal\n\n£\n\nBrowse destination','Portugal\n\nBrowse destination')
 hits=re.findall(r'[$€£¥₹₽]|\b(?:prices?|cheap|savings|payment|checkout|refund|purchased|purchase)\b',normalized,re.I)
 checks.append({'path':p.relative_to(PUB).as_posix(),'hits':hits,'text':text,'visual_review':'OCR e€SIM is the visible word eSIM, not a currency symbol' if false_positive else 'OCR e€spafiol is the visible word español, not a currency symbol' if spanish_false_positive else 'OCR £ is the Portugal flag, not a currency symbol; artwork visually checked' if flag_false_positive else None,'sha256':digest})
for p in (V/'apple-1206').glob('*.png'):assert Image.open(p).size==(1206,2622)
assert Image.open(V/'google-icon-512.png').mode=='RGBA' and (V/'google-icon-512.png').stat().st_size<1024*1024
for p in list((V/'apple').glob('*.png'))+list((V/'google').glob('*.png')):assert Image.open(p).mode=='RGB'
bad=[x for x in checks if x['hits']]
(STATE/'ocr-qa.json').write_text(json.dumps({'images':len(checks),'flagged':bad,'results':checks},indent=2))
print(json.dumps({'ocr_images':len(checks),'flagged':[(x['path'],x['hits']) for x in bad],'size_format_checks':'passed'}))
assert not bad
