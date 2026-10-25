"""Create separately labeled, non-certified platform drafts and editable sources."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, zipfile, hashlib
root=Path(__file__).resolve().parents[1]
public=root/'public';out=public/'downloads'
out.mkdir(exist_ok=True)
config=json.loads((public/'submission.json').read_text())
qa=json.loads((root/'submission-layout-qa.json').read_text())
limits={'name':30,'subtitle':30,'promotional':170,'keywords':100,'description':4000,'shortDescription':80,'releaseNotes':500}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)
for platform in ['apple','google']:
    spec=config[platform];manifest=[]
    for field,value in spec['metadata'].items():
        assert (len(value.encode()) if field=='keywords' else len(value))<=limits[field],field
    readme=f"# Openline {spec['label']}\n\nNOT READY TO UPLOAD: native captures and release evidence are pending.\n\n"
    readme+="This variant restores the approved Openline visual style: large angled app panels, bold headlines, orange/cream alternation and generous space. Store-specific conservative wording is retained. The approved marketing master is unchanged. Six RGB PNG phone compositions are included; these are still supplied React design references, not certified native screenshots.\n\n"
    readme+=("Apple retains a factual OMDM sourcing explanation without lower-price, Tier-1 or switching claims.\n\n" if platform=='apple' else "Google overlays omit price promotions, superlatives, Tier-1 and switching claims. Angled app panels have no added hardware bezels. Overlay bounding-box area and tagline height are each tested below 20%; this engineering check is not store certification. The source UI still contains sample prices and a BEST VALUE badge, so replacement captures remain a blocker.\n\n")
    readme+="## Required before upload\n\n"+'\n'.join('- [ ] '+x for x in config['gates'])
    readme+="\n\n## Official policy references\n\n"+'\n'.join('- '+x for x in config['sources'])+'\n'
    copy='# '+spec['label']+' listing copy\n\nDraft only; verify features, OMDM sourcing and actual release UI before submission.\n\n'
    for key,value in spec['metadata'].items():copy+=f'## {key}\n\n{value}\n\n'
    (out/f'openline-{platform}-submission-copy.md').write_text(copy)
    (out/f'openline-{platform}-submission-readiness.md').write_text(readme)
    sheet=Image.new('RGB',(1560,690),'#f5f2ec');draw=ImageDraw.Draw(sheet)
    draw.text((24,15),spec['label']+' / Native captures pending',font=font,fill='#20211f')
    for n in range(6):
        p=public/'submission'/platform/f'{n+1:02d}.png'
        im=Image.open(p).convert('RGB');assert im.size==(spec['width'],spec['height'])
        im.save(p,optimize=True)
        thumb=im.copy();thumb.thumbnail((420,913));thumb.save(p.with_suffix('.webp'),quality=86)
        small=im.copy();small.thumbnail((238,590));sheet.paste(small,(24+n*256,70))
        manifest.append({'file':p.name,'width':im.width,'height':im.height,'mode':'RGB','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':spec['frames'][n]['capture'],'status':config['status']})
    sheet.save(public/'submission'/platform/'contact-sheet.jpg',quality=90)
    if platform=='google':
        feature=public/'submission/google/feature-graphic.png'
        im=Image.open(feature).convert('RGB');assert im.size==(1024,500);im.save(feature,optimize=True)
    with zipfile.ZipFile(out/f'openline-{platform}-submission-draft.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted((public/'submission'/platform).glob('[0-9][0-9].png')):z.write(p,'screenshots/'+p.name)
        if platform=='google':z.write(feature,'feature-graphic.png')
        z.write(public/'submission'/platform/'contact-sheet.jpg','contact-sheet.jpg')
        z.writestr('README-BEFORE-UPLOAD.md',readme)
        z.writestr('listing-copy.md',copy)
        z.writestr('metadata.json',json.dumps(spec['metadata'],indent=2))
        z.writestr('screenshot-manifest.json',json.dumps(manifest,indent=2))
        z.writestr('layout-qa.json',json.dumps([x for x in qa if x['platform']==platform],indent=2))
        z.writestr('readiness.json',json.dumps({'status':config['status'],'gates':config['gates']},indent=2))
        z.write(out/'submission-copy-review.md','copy-review.md')
        icon='apple-icon-1024.png' if platform=='apple' else 'google-play-icon-512.png'
        z.write(public/'assets'/icon,'icon/'+icon)
with zipfile.ZipFile(out/'openline-submission-sources.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write(out/'submission-copy-review.md','public/downloads/submission-copy-review.md')
    for name in ['submission.json','render-submission.html']:z.write(public/name,'public/'+name)
    for p in (public/'fonts').rglob('*'):
        if p.is_file():z.write(p,'public/fonts/'+str(p.relative_to(public/'fonts')))
    for name in {'mark.png','icon-43.5-light.png','apple-icon-1024.png','google-play-icon-512.png'}|{f['capture'] for k in ['apple','google'] for f in config[k]['frames']}:
        z.write(public/'assets'/name,'public/assets/'+name)
    for name in ['render_submission.mjs','package_submission.py']:z.write(root/'scripts'/name,'scripts/'+name)
    z.writestr('package.json',json.dumps({'private':True,'type':'module','scripts':{'serve':'vite public --host 127.0.0.1 --port 5173','render':'node scripts/render_submission.mjs'},'devDependencies':{'vite':'6.4.3','playwright':'^1.63.0'}},indent=2))
    z.writestr('README.md','# Openline submission draft sources\n\nRun npm install, npx playwright install chromium, then npm run serve. In another terminal run npm run render. Install Pillow and a DejaVuSans font, then run python scripts/package_submission.py to package. Replace public/assets captures with real release-build screens, update public/submission.json and re-render before approval. Create public/downloads before packaging standalone sources. These are not approved submissions.\n')
print('Packaged Apple and Google drafts, validated copy limits, RGB images and separate editable sources.')
