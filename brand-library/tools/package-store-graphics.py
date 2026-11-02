"""Package v2.8.6: Google feature graphics, store-graphics manifest, /app store workspace. Lighter than package-recommended-story.py."""
import hashlib,json,shutil,subprocess
from pathlib import Path
app=Path(__file__).resolve().parents[1];pub=app/'public'
repo=app.parent/'openline-brand-assets/brand-library'
state=app.parent/'openline-fly-deployment/recommended-story-v2-8-6';state.mkdir(exist_ok=True)
V='2.8.6'
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
subprocess.run(['python3',str(app/'tools/validate-store-graphics.py')],check=True)
for name in['package.json','package-lock.json']:
 p=app/name;x=json.loads(p.read_text());x['version']=V
 if 'packages' in x:x['packages']['']['version']=V
 save(p,x)
p=pub/'library/catalog.json';x=json.loads(p.read_text());x['version']=V;save(p,x)
changed=['library/catalog.json','app-v3/recommended-copy.json','app-v3/recommended/google/feature-graphic.png','app-v3/recommended/google/feature-graphic-light.png','app-v3/recommended/store-graphics.json']
inv=json.loads((repo/'PUBLIC-ASSETS.json').read_text());old={x['path']:x for x in inv['files']}
for n in changed:
 p=pub/n;d=app/'dist'/n;d.parent.mkdir(parents=True,exist_ok=True)
 if not d.exists() or not p.samefile(d):shutil.copyfile(p,d)
 b=p.read_bytes();old[n]={'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'url':'https://brand.openline.com/'+n}
inv['version']=V;inv['files']=list(old.values());inv['total_bytes']=sum(x['bytes'] for x in old.values())
save(repo/'PUBLIC-ASSETS.json',inv);save(state/'public-files.json',changed)
print(json.dumps({'files':len(changed),'bytes':sum((pub/n).stat().st_size for n in changed)}))
