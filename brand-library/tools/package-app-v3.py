import json,hashlib,shutil
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
APP=Path(__file__).resolve().parents[1];PUB=APP/"public";V=PUB/"app-v3";STATE=APP.parent/"openline-fly-deployment/app-v3-20-v2-7-1"
REPO=APP.parent if APP.name=="brand-library" else APP.parent/"openline-brand-assets"
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
def read(p):return json.loads(p.read_text())
copy=read(V/'copy.json')
for f in copy['frames']:f['alt']=f["title"]+'. '+f["detail"]
save(V/'copy.json',copy)
Image.open(PUB/'app-v2/icons/openline-icon-white-512.png').convert('RGBA').save(V/'google-icon-512.png',optimize=True)
for platform in ['apple','google']:
 sheet=Image.new('RGB',(5*200,4*470),'#f6f1e9');draw=ImageDraw.Draw(sheet)
 for n in range(1,len(copy['frames'])+1):
  p=V/platform/f'{n:02}.png';im=Image.open(p).convert('RGB')
  assert im.size==((1320,2868) if platform=='apple' else (1080,1920))
  im.save(p,optimize=True)
  preview=im.copy();preview.thumbnail((660,1434));preview.save(p.with_suffix('.webp'),quality=85,method=6)
  if platform=='apple':
   (V/'apple-1206').mkdir(exist_ok=True);im.resize((1206,2622),Image.Resampling.LANCZOS).save(V/'apple-1206'/p.name,optimize=True)
  im.thumbnail((180,420));x=((n-1)%5)*200+10;y=((n-1)//5)*470+10;sheet.paste(im,(x,y));draw.text((x,y+425),f'Candidate {n:02}'+(' / Concept' if n>12 else ''),fill='#171717')
 sheet.save(V/platform/'contact-sheet.jpg',quality=90)
# Check preserved original assets and V2 against the previous release inventory.
old=read(APP.parent/'openline-fly-deployment/app-v2-v2-6-0/v1-hashes.json')
assert all(hashlib.sha256((PUB/n).read_bytes()).hexdigest()==h for n,h in old.items())
inv=read(REPO/'brand-library/PUBLIC-ASSETS.json');oldv2=[f for f in inv['files'] if f['path'].startswith('app-v2/')]
assert all(hashlib.sha256((PUB/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in oldv2)
cat=read(PUB/'library/catalog.json');cat['version']='2.7.1'
cat['appLibraryV3']={'candidatesPerPlatform':len(copy['frames']),'conceptsPerPlatform':8,'limits':{'apple':10,'google':8},'copyOptions':3,'icon':'./app-v2/icons/openline-icon-white-1024.png','preview':'#/app?version=v3','notes':'./app-v3/README.md','status':'Design review; owner selection pending'}
save(PUB/'library/catalog.json',cat)
for name in ['package.json','package-lock.json']:
 p=APP/name;d=read(p);d['version']='2.7.1'
 if name=='package-lock.json':d['packages']['']['version']='2.7.1'
 save(p,d)
changed=[p.relative_to(PUB).as_posix() for p in V.rglob('*') if p.is_file()]+['library/catalog.json']
save(STATE/'public-changed-files.json',changed)
index={f['path']:f for f in inv['files']}
for name in changed:
 b=(PUB/name).read_bytes();index[name]={'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'url':'https://brand.openline.com/'+name}
inv['version']='2.7.1';inv['files']=list(index.values());inv['total_bytes']=sum(f['bytes'] for f in inv['files']);save(REPO/'brand-library/PUBLIC-ASSETS.json',inv)
files=['AppSubmissionWorkbench.jsx','submission-workbench.css','submission-fields.js','selection-zip.js','src.jsx','FLOWS.md','package.json','package-lock.json','scripts/capture_app_v3.mjs','scripts/capture_app_v3_concepts.mjs','scripts/render_app_v3.mjs','tools/package-app-v3.py','tools/qa-app-v3.py','public/app-v3/copy.json','public/app-v3/apple-examples.json','public/app-v3/README.md']
for name in files:
 a=APP/name;b=REPO/'brand-library'/name;b.parent.mkdir(parents=True,exist_ok=True)
 if not b.exists() or not a.samefile(b):shutil.copy2(a,b)
print(json.dumps({'candidates':len(copy['frames'])*2,'additional_apple_size':len(copy['frames']),'v1_preserved':len(old),'v2_preserved':len(oldv2),'public_files':len(changed),'megabytes':sum((PUB/n).stat().st_size for n in changed)/1e6}))
