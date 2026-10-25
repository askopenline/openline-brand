"""Final approved composition, derived from original vector paths, not auto-traced."""
from pathlib import Path
from PIL import Image
from svgpathtools import parse_path
import cairosvg
import xml.etree.ElementTree as ET
import subprocess, json, zipfile, hashlib, shutil

root=Path(__file__).resolve().parents[1]
repo=root.parent if (root.parent/'logo').exists() else root.parent/'openline-brand-assets'
out=root/'public/downloads/final-icon'
out.mkdir(parents=True,exist_ok=True)
source=out/'canonical-source.svg'
subprocess.run(['pdftocairo','-svg','-f','1','-l','1',str(repo/'logo/pdf/openline-logo.pdf'),str(source)],check=True)
tree=ET.parse(source)
paths=[]
seen=set()
for p in tree.getroot():
    d=p.get('d')
    if d and d not in seen:
        paths.append(p);seen.add(d)
assert len(paths)==2,'Expected the original two-path mark'
boxes=[parse_path(p.get('d')).bbox() for p in paths]
x0,x1=min(b[0] for b in boxes),max(b[1] for b in boxes)
y0,y1=min(b[2] for b in boxes),max(b[3] for b in boxes)
scale=1024*.435/(x1-x0)
tx=(1024-(x1-x0)*scale)/2-x0*scale
ty=(1024-(y1-y0)*scale)/2-y0*scale
geometry=''.join(f'<path fill="{("#ff6616" if i==0 else "#000000")}" d="{p.get("d")}"/>' for i,p in enumerate(paths))
def svg(transparent=False):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><title>Openline final app icon · 43.5% artwork width</title>'+('' if transparent else '<rect width="1024" height="1024" fill="#ffffff"/>')+f'<g transform="translate({tx} {ty}) scale({scale})">{geometry}</g></svg>'
for name,transparent in [('openline-icon-white',False),('openline-icon-transparent',True)]:
    text=svg(transparent);(out/f'{name}.svg').write_text(text)
    for size in [16,24,32,48,64,128,180,192,256,512,1024,2048,4096]:
        cairosvg.svg2png(bytestring=text.encode(),write_to=str(out/f'{name}-{size}.png'),output_width=size,output_height=size)
        if not transparent:
            im=Image.open(out/f'{name}-{size}.png').convert('RGB');im.save(out/f'{name}-{size}.png',optimize=True)
    cairosvg.svg2pdf(bytestring=text.encode(),write_to=str(out/f'{name}.pdf'))
    if not transparent:
        cairosvg.svg2eps(bytestring=text.encode(),write_to=str(out/f'{name}.eps'))
    im=Image.open(out/f'{name}-1024.png')
    im.save(out/f'{name}-1024.webp',lossless=True)
    if not transparent:
        im.convert('RGB').save(out/f'{name}-1024.jpg',quality=98,subsampling=0)
        im.save(out/'openline-icon.ico',sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
        im.convert('RGBA').save(out/'openline-icon.icns')
# EPS from Cairo is PostScript with a valid single-page bounding box. No fake AI extension.
source.unlink()
readme="""# Openline final icon · approved 7 October 2026

Final choice: 43.5% visible mark width inside an unchanged white square.
Vector paths come from page 1 of the canonical Openline Illustrator PDF,
deduplicated and uniformly scaled. They are not an auto-trace or redrawn mark.

## Included
- SVG and vector PDF: white square and transparent-canvas compositions.
- EPS: white-square composition, single-page vector PostScript.
- PNG: white and transparent canvases, 16 through 4096 pixels.
- WebP: lossless 1024px, white and transparent.
- JPEG: white-square 1024px, presentation use only.
- ICO: 16–256px multi-resolution desktop/web convenience export.
- ICNS: macOS convenience export, not an iOS submission asset.
- Native package: Xcode PNG catalog, Icon Composer source layers, Android
  legacy/adaptive/monochrome resources and Play 512px listing icon.

Transparent variants are for design/integration, never Apple or Play store
listing upload. Do not bake a rounded mask or shadow into a store icon.
Use the native package's platform-specific resources for integration.
SVG/PDF can be edited in Illustrator; no native .ai document is claimed.
Icon Composer layers are not a compiled .icon file. That file must be built
and validated in Apple's tools. Android has no single file equivalent:
adaptive icon XML, background, foreground and monochrome resources work together.

## Approval scope
Paul approved the visual 43.5% composition on 7 October 2026. This does not
certify platform rendering or store acceptance. The 39.6dp adaptive treatment
still needs native legibility testing; the 48dp fallback is retained separately.
Dark and tinted appearances remain references, not separate approved identities.

Guidance:
https://developer.apple.com/design/human-interface-guidelines/app-icons
https://developer.android.com/develop/ui/compose/system/icon_design_adaptive
https://support.google.com/googleplay/android-developer/answer/9866151?hl=en
"""
(out/'README.md').write_text(readme)
files=[{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(out.iterdir()) if p.is_file() and p.name!='manifest.json']
(out/'manifest.json').write_text(json.dumps({'status':'visual-choice-approved','coverage':.435,'approvedAt':'2026-10-07','files':files},indent=2))
with zipfile.ZipFile(root/'public/downloads/openline-final-icon-all-formats.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(out.iterdir()):z.write(p,'final-icon/'+p.name)
    for p in sorted((root/'icon-package').rglob('*')):
        if p.is_file():z.write(p,'native/'+str(p.relative_to(root/'icon-package')))
print(f'Packaged {len(files)} final composition exports plus native resources.')
