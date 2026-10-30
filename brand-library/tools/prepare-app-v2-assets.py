import json,hashlib,re
from pathlib import Path
import cairosvg
from PIL import Image
root=Path(__file__).resolve().parents[1];pub=root/"public"
state=root.parent/"openline-fly-deployment/app-v2-v2-6-0";state.mkdir(exist_ok=True)
snapshot=state/"v1-hashes.json"
if not snapshot.exists():
    paths=[*(pub/"series").rglob("*"),*(pub/"submission").rglob("*"),*(pub/"downloads/final-icon").rglob("*"),pub/"submission.json",pub/"series.json",pub/"assets/icon-43.5-light.png"]
    snapshot.write_text(json.dumps({str(p.relative_to(pub)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()},indent=2))
icons=pub/"app-v2/icons";icons.mkdir(parents=True,exist_ok=True)
for kind in ("white","transparent"):
    svg=(pub/f"downloads/final-icon/openline-icon-{kind}.svg").read_text()
    svg=re.sub(r'<title>.*?</title>','<title>Openline V2 app icon · original mark enlarged 12.5%</title>',svg)
    svg=svg.replace('<g transform=', '<g transform="translate(512 512) scale(1.125) translate(-512 -512)"><g transform=',1).replace('</svg>','</g></svg>')
    (icons/f"openline-icon-{kind}.svg").write_text(svg)
    for size in (1024,512,256,128,64):
        p=icons/f"openline-icon-{kind}-{size}.png"
        cairosvg.svg2png(bytestring=svg.encode(),write_to=str(p),output_width=size,output_height=size)
        Image.open(p).save(p.with_suffix('.webp'),lossless=True)
    cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(icons/f"openline-icon-{kind}.pdf"))
    if kind=="white":Image.open(icons/"openline-icon-white-1024.png").convert("RGB").save(icons/"openline-icon-white-1024.jpg",quality=96)
print('Original paths preserved; V2 vector mark scaled 1.125 around the tile center.')
