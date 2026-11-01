"""Package the Recommended-only revision and preserve original editions."""
import hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageDraw
app=Path(__file__).resolve().parents[1];pub=app/'public';v=pub/'app-v3/recommended'
repo=app.parent/'openline-brand-assets/brand-library'
state=app.parent/'openline-fly-deployment/recommended-story-v2-8-1';state.mkdir(exist_ok=True)
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
inventory=json.loads((repo/'PUBLIC-ASSETS.json').read_text());old={x['path']:x for x in inventory['files']}
protected=[n for n in old if n=='app-v3/copy.json' or any(n.startswith('app-v3/'+s+'/') for s in ['apple','google','apple-1206','screens']) or n.startswith('app-v3/recommended/icon-2026-11/') or n=='app-v2/downloads/openline-v2-icons.zip']
for n in protected:assert hashlib.sha256((pub/n).read_bytes()).hexdigest()==old[n]['sha256'],n
rec=json.loads((pub/'app-v3/recommended-copy.json').read_text())
changed=['library/catalog.json','app-v3/recommended-copy.json','app-v3/recommended-update-notes.md']
for platform,ids in rec['selection'].items():
 for id in ids:
  p=v/platform/(id+'.png');im=Image.open(p).convert('RGB')
  assert im.size==((1320,2868) if platform=='apple' else (1080,1920))
  im.save(p,optimize=True);preview=im.copy();preview.thumbnail((660,1434));preview.save(p.with_suffix('.webp'),quality=85,method=6)
  changed.extend([p.relative_to(pub).as_posix(),p.with_suffix('.webp').relative_to(pub).as_posix()])
  if platform=='apple':
   (v/'apple-1206').mkdir(exist_ok=True);dest=v/'apple-1206'/(id+'.png');im.resize((1206,2622),Image.Resampling.LANCZOS).save(dest,optimize=True);changed.append(dest.relative_to(pub).as_posix())
for n in ['screens/duration-calendar.png','screens/setup-checklist.png','screens/live-chat.png','revision-provenance.json','revision-layout-qa.json']:
 changed.append('app-v3/recommended/'+n)
for name in ['package.json','package-lock.json']:
 p=app/name;x=json.loads(p.read_text());x['version']='2.8.1'
 if 'packages' in x:x['packages']['']['version']='2.8.1'
 save(p,x)
p=pub/'library/catalog.json';x=json.loads(p.read_text());x['version']='2.8.1'
x['appLibraryV3']['recommendedSelection'].update({'apple':rec['selection']['apple'],'google':rec['selection']['google'],'copy':'./app-v3/recommended-copy.json','revisionNotes':'./app-v3/recommended-update-notes.md','productVerificationPending':True})
save(p,x)
for n in changed:
 p=pub/n;d=app/'dist'/n;d.parent.mkdir(parents=True,exist_ok=True)
 if not d.exists() or not p.samefile(d):shutil.copyfile(p,d)
 b=p.read_bytes();old[n]={'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'url':'https://brand.openline.com/'+n}
inventory['version']='2.8.1';inventory['files']=list(old.values());inventory['total_bytes']=sum(x['bytes'] for x in old.values())
save(repo/'PUBLIC-ASSETS.json',inventory);save(state/'public-files.json',changed);save(state/'protected-originals.json',{n:old[n]['sha256'] for n in protected})
# Private visual QA sheet; no production-only claims or provider material.
sheet=Image.new('RGB',(1440,1680),'#ededed');draw=ImageDraw.Draw(sheet)
for row,platform in enumerate(['apple','google']):
 for col,id in enumerate(['04','19','18']):
  im=Image.open(v/platform/(id+'.png')).convert('RGB');im.thumbnail((455,790));sheet.paste(im,(col*480+(480-im.width)//2,row*840+30))
  draw.text((col*480+10,row*840+8),platform+' '+id,fill='black')
sheet.save(state/'revised-screens.jpg',quality=90)
print(json.dumps({'files':len(changed),'bytes':sum((pub/n).stat().st_size for n in changed),'protected':len(protected)}))
