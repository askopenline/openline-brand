"""Render the existing V2 vector mark at another 1.125x; never edit archives."""
import hashlib,json,re,shutil,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
import cairosvg
from PIL import Image,ImageChops,ImageDraw
APP=Path(__file__).resolve().parents[1];PUB=APP/'public'
OUT=PUB/'app-v3/recommended/icon-2026-11'
STATE=APP.parent/'openline-fly-deployment/recommended-icon-v2-7-8'
REPO=APP if APP.name=='brand-library' else APP.parent/'openline-brand-assets/brand-library'
OUT.mkdir(parents=True,exist_ok=True);STATE.mkdir(parents=True,exist_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
protected=[PUB/'app-v3/copy.json',PUB/'app-v3/google-icon-512.png',*list((PUB/'app-v2/icons').glob('*')),PUB/'app-v2/downloads/openline-v2-icons.zip']
before={p.relative_to(PUB).as_posix():digest(p) for p in protected}
for kind in ['white','transparent']:
    source=(PUB/f'app-v2/icons/openline-icon-{kind}.svg').read_text()
    svg=re.sub(r'<title>.*?</title>','<title>Openline Recommended icon: an additional 12.5% mark enlargement over V2</title>',source)
    svg=svg.replace('<g transform=','<g transform="translate(512 512) scale(1.125) translate(-512 -512)"><g transform=',1).replace('</svg>','</g></svg>')
    ns={'s':'http://www.w3.org/2000/svg'}
    assert [e.attrib for e in ET.fromstring(source).findall('.//s:path',ns)]==[e.attrib for e in ET.fromstring(svg).findall('.//s:path',ns)]
    (OUT/f'openline-icon-{kind}.svg').write_text(svg)
    for size in [1024,512,256,128,64]:
        p=OUT/f'openline-icon-{kind}-{size}.png'
        cairosvg.svg2png(bytestring=svg.encode(),write_to=str(p),output_width=size,output_height=size)
        im=Image.open(p).convert('RGB' if kind=='white' else 'RGBA');im.save(p);im.save(p.with_suffix('.webp'),lossless=True)
    cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(OUT/f'openline-icon-{kind}.pdf'))
Image.open(OUT/'openline-icon-white-1024.png').save(OUT/'openline-icon-white-1024.jpg',quality=96)
def bounds(p):
    im=Image.open(p).convert('RGB');return ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
old=bounds(PUB/'app-v2/icons/openline-icon-white-1024.png');new=bounds(OUT/'openline-icon-white-1024.png')
ratios=[(new[i+2]-new[i])/(old[i+2]-old[i]) for i in (0,1)]
assert all(abs(x-1.125)<.006 for x in ratios)
assert all(0<v<1024 for v in new)
for size in [1024,512]:
    im=Image.open(OUT/f'openline-icon-white-{size}.png');assert im.mode=='RGB' and im.size==(size,size)
    assert im.getpixel((0,0))==(255,255,255)
info={'edition':'Recommended 2026-11-01','relative_to':'V2 icon currently used by V3/Recommended','linear_scale_vs_v2':1.125,'linear_scale_vs_original':1.265625,'canvas':[1024,1024],'source_paths_preserved':True,'original_bounds_1024':old,'recommended_bounds_1024':new,'raster_bounds_ratios':ratios,'formats':['PNG','WebP','SVG','PDF','JPEG'],'raster_sizes':[64,128,256,512,1024],'notes':'White PNGs are opaque. Transparent variants are design resources, not store-upload icons. No Android adaptive-layer package is included. Final and archives unchanged.'}
save(OUT/'manifest.json',info)
(OUT/'README.md').write_text('# Openline Recommended App Icon\n\nOriginal vector paths, enlarged another 12.5% in width and height over V2, centered within the unchanged white square. Cumulative linear scale versus the original edition: 1.265625x (+26.5625%).\n\nUse white 1024px PNG for the Apple icon resource and white 512px PNG for the Google Play icon resource. Store submission readiness requires separate validation.\n\nIncluded: PNG and lossless WebP at 64, 128, 256, 512 and 1024px; SVG and vector PDF; 1024px white JPEG. White and transparent variants are separate. Transparent files are design resources, not store-upload icons; native Android adaptive layers are not included.\n\nOnly Recommended uses this edition. V1, V2, V3 and Final remain unchanged.\n')
zip_path=PUB/'app-v3/recommended/downloads/openline-recommended-icons-plus-12-5.zip';zip_path.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.iterdir()):z.write(p,p.name)
with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None
assert all(digest(PUB/n)==h for n,h in before.items())
save(STATE/'protected-originals.json',before)
sheet=Image.new('RGB',(800,440),'#eeeeee');d=ImageDraw.Draw(sheet)
for i,p in enumerate([PUB/'app-v2/icons/openline-icon-white-1024.png',OUT/'openline-icon-white-1024.png']):
    sheet.paste(Image.open(p).resize((350,350)),(25+i*400,50));d.text((25+i*400,20),'V2 (previous)' if i==0 else 'Recommended (+12.5%)',fill='black')
sheet.save(STATE/'comparison.png')
cat=json.loads((PUB/'library/catalog.json').read_text());cat['version']='2.7.8'
cat['appLibraryV3']['recommendedSelection']['icon']='./'+(OUT/'openline-icon-white-1024.png').relative_to(PUB).as_posix()
cat['appLibraryV3']['recommendedSelection']['iconZip']='./'+zip_path.relative_to(PUB).as_posix()
save(PUB/'library/catalog.json',cat)
changed=['library/catalog.json',zip_path.relative_to(PUB).as_posix()]+[p.relative_to(PUB).as_posix() for p in OUT.iterdir()]
for n in changed:
    target=APP/'dist'/n;target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists() or (PUB/n).stat().st_ino!=target.stat().st_ino:shutil.copy2(PUB/n,target)
inv=json.loads((REPO/'PUBLIC-ASSETS.json').read_text());index={f['path']:f for f in inv['files']}
for n in changed:index[n]={'path':n,'bytes':(PUB/n).stat().st_size,'sha256':digest(PUB/n),'url':'https://brand.openline.com/'+n}
inv.update(version='2.7.8',files=list(index.values()),total_bytes=sum(x['bytes'] for x in index.values()));save(REPO/'PUBLIC-ASSETS.json',inv)
for n in ['package.json','package-lock.json']:
    x=json.loads((APP/n).read_text());x['version']='2.7.8'
    if 'packages' in x:x['packages']['']['version']='2.7.8'
    save(APP/n,x)
save(STATE/'public-files.json',changed);save(STATE/'qa-summary.json',info)
print(json.dumps({'zip':str(zip_path),'bytes':zip_path.stat().st_size,'files':len(list(OUT.iterdir())),'ratios':ratios,'protected':len(before)}))
