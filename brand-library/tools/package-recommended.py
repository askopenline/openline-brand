import hashlib,json,shutil
from pathlib import Path
from PIL import Image

app=Path(__file__).resolve().parents[1];pub=app/'public';v=pub/'app-v3/recommended'
repo=app.parent/'openline-brand-assets/brand-library'
state=app.parent/'openline-fly-deployment/recommended-v2-7-6';state.mkdir(exist_ok=True)
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
inventory=json.loads((repo/'PUBLIC-ASSETS.json').read_text())
old={x['path']:x for x in inventory['files']}
protected=['app-v3/copy.json','app-v3/screens/types.png','app-v3/apple/11.png','app-v3/google/11.png','app-v3/apple-1206/11.png']
for n in protected:assert hashlib.sha256((pub/n).read_bytes()).hexdigest()==old[n]['sha256'],n
for platform,size in [('apple',(1320,2868)),('google',(1080,1920))]:
 p=v/platform/'11.png';im=Image.open(p).convert('RGB');assert im.size==size;im.save(p,optimize=True)
 preview=im.copy();preview.thumbnail((660,1434));preview.save(p.with_suffix('.webp'),quality=85,method=6)
 if platform=='apple':
  (v/'apple-1206').mkdir(exist_ok=True);im.resize((1206,2622),Image.Resampling.LANCZOS).save(v/'apple-1206/11.png',optimize=True)
for name in ['package.json','package-lock.json']:
 p=app/name;x=json.loads(p.read_text());x['version']='2.7.6'
 if 'packages' in x:x['packages']['']['version']='2.7.6'
 save(p,x)
p=pub/'library/catalog.json';x=json.loads(p.read_text());x['version']='2.7.6'
x['appLibraryV3']['recommendedSelection'].update({'copy':'./app-v3/recommended-copy.json','productVerificationPending':True,'planTypesOwnerConfirmed':['Unlimited usage','Fixed usage'],'separateAssets':'./app-v3/recommended/'})
save(p,x)
changed=['library/catalog.json','app-v3/README.md','app-v3/recommended-copy.json']+[p.relative_to(pub).as_posix() for p in sorted(v.rglob('*')) if p.is_file()]
for n in changed:
 p=pub/n;d=app/'dist'/n;d.parent.mkdir(parents=True,exist_ok=True)
 if not d.exists() or not p.samefile(d):shutil.copyfile(p,d)
 b=p.read_bytes();old[n]={'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'url':'https://brand.openline.com/'+n}
inventory['version']='2.7.6';inventory['files']=list(old.values());inventory['total_bytes']=sum(x['bytes'] for x in old.values())
save(repo/'PUBLIC-ASSETS.json',inventory);save(state/'public-files.json',changed);save(state/'protected-originals.json',{n:old[n]['sha256'] for n in protected})
for n in ['AppSubmissionWorkbench.jsx','submission-workbench.css','FLOWS.md','package.json','package-lock.json','scripts/capture_app_v3.mjs','scripts/render_app_v3.mjs','tools/package-recommended.py','public/app-v3/README.md','public/app-v3/recommended-copy.json','scripts/qa_recommended_content.mjs']:
 p=app/n;d=repo/n;d.parent.mkdir(parents=True,exist_ok=True)
 if not d.exists() or not p.samefile(d):shutil.copyfile(p,d)
print(json.dumps({'files':len(changed),'bytes':sum((pub/n).stat().st_size for n in changed),'originalsPreserved':protected}))
