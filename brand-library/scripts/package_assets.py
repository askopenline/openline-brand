from pathlib import Path
from PIL import Image, ImageDraw
import zipfile, json, hashlib, csv, io
root=Path(__file__).resolve().parents[1]
assets=root/'public/assets';downloads=root/'public/downloads'
manifest=[]
for prefix,size in [('ios',(1320,2868)),('android',(1080,1920))]:
    for i in range(1,7):
        p=assets/f'{prefix}-{i:02d}.png'
        im=Image.open(p).convert('RGB');assert im.size==size
        im.save(p,optimize=True)
        manifest.append({'file':p.name,'width':size[0],'height':size[1],'mode':'RGB','status':'design-reference-not-native-capture','sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
p=assets/'google-feature.png';im=Image.open(p).convert('RGB');assert im.size==(1024,500);im.save(p,optimize=True)
manifest.append({'file':p.name,'width':1024,'height':500,'mode':'RGB','status':'design-reference-not-native-capture','sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(downloads/'asset-manifest.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(downloads/'openline-store-artwork.zip','w',zipfile.ZIP_DEFLATED) as z:
    for row in manifest:z.write(assets/row['file'],row['file'])
    z.write(downloads/'asset-manifest.json','asset-manifest.json')
    z.write(downloads/'screenshot-handoff.md','screenshot-handoff.md')
    z.writestr('README.md','# Openline store artwork: review candidates\n\nThese images are rendered from React design-reference screens, NOT the native release binaries. Keep the review footer until accurate native screenshots and all copy are approved. Mock prices/data are illustrative. No iPad/tablet set is included; native device support must first be confirmed.\n\nApple: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications\nGoogle: https://support.google.com/googleplay/android-developer/answer/9866151?hl=en\n')
config=json.loads((root/'public/artwork.json').read_text())
alt=[]
for index,slide in enumerate(config['slides'],1):
    text=f"Openline {slide['short'].lower()}: {slide['detail']} App design preview; sample data."
    assert len(text)<=140
    alt.append({'order':index,'file':f'android-{index:02d}.png','locale':'en-US','altText':text,'status':'draft-replace-with-native'})
(downloads/'google-artwork-alt-text.json').write_text(json.dumps(alt,indent=2))
with zipfile.ZipFile(downloads/'openline-screenshot-sources.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['render.html','artwork.json']:
        z.write(root/'public'/name,'public/'+name)
    for p in (root/'public/fonts').rglob('*'):
        if p.is_file():z.write(p,'public/fonts/'+str(p.relative_to(root/'public/fonts')))
    for name in sorted({'mark.png'}|{Path(s['captures'][p]).name for s in config['slides'] for p in ['ios','android']}):
        z.write(assets/name,'public/assets/'+name)
    z.write(root/'scripts/render_artwork.mjs','scripts/render_artwork.mjs')
    z.write(downloads/'screenshot-handoff.md','README.md')
    z.writestr('package.json',json.dumps({'name':'openline-screenshot-sources','private':True,'type':'module','scripts':{'serve':'vite public --host 127.0.0.1 --port 5173','render':'node scripts/render_artwork.mjs'},'devDependencies':{'vite':'6.4.3','playwright':'^1.58.0'}},indent=2))
sheet=Image.new('RGB',(1440,550),'#f4f2ef')
draw=ImageDraw.Draw(sheet)
for i in range(6):
    image=Image.open(assets/f'ios-{i+1:02d}.png')
    image.thumbnail((220,680))
    sheet.paste(image,(10+i*240,20))
    draw.text((14+i*240,520),f'{i+1:02d}  {config["slides"][i]["slug"]}',fill='#333333')
sheet.save(assets/'artwork-contact-sheet.jpg',quality=92)
with zipfile.ZipFile(downloads/'openline-launch-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['openline-final-icon-all-formats.zip','openline-native-icons.zip','openline-store-artwork.zip','openline-screenshot-sources.zip','screenshot-handoff.md','submission-audit.md','google-artwork-alt-text.json','console-metadata.json','openline-store-copy.md','openline-store-settings.md','openline-release-checklist.md','openline-launch-workspace.json','store-requirements.md','competitor-review.md','asset-manifest.json']:
        z.write(downloads/name,('archive-r03/' if name in ['openline-store-artwork.zip','openline-screenshot-sources.zip','asset-manifest.json','google-artwork-alt-text.json'] else '')+name)
    z.write(downloads/'orange-series-handoff.md','orange-series-handoff.md')
    z.write(downloads/'orange-series-manifest.json','orange-series-manifest.json')
    z.write(downloads/'positioning-claims.md','positioning-claims.md')
    z.writestr('CURRENT-SCREENSHOT-OPTIONS.md','# Current creative review / Revision 10\n\nSix distinct app views alternate orange and warm cream. Network dashboard is frame 5; plan selection is frame 6. No illustration-only frames remain. Android uses a neutral plan-choice headline. Native captures, sample data/FUP and claim verification remain required. Download:\n\nhttps://openline-brand.fly.dev/downloads/openline-orange-series.zip\n\nEditable sources:\nhttps://openline-brand.fly.dev/downloads/openline-orange-series-sources.zip\n\nPolicy assessment:\nhttps://openline-brand.fly.dev/downloads/screenshot-compliance-review.md\n\nThe archive-r03 folder is superseded. The final 43.5% app icon is unchanged. Competitor imagery is excluded.\n')
    z.write(downloads/'screenshot-compliance-review.md','screenshot-compliance-review.md')
    z.write(root/'README.md','README.md')
    z.write(root/'sources.json','official-sources.json')
print('Validated 12 RGB store compositions and feature graphic; packaged launch kit.')
