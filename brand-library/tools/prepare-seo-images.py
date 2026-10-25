"""Use existing approved artwork only; no generative assets or changed geometry."""
from pathlib import Path
from shutil import copyfile
from PIL import Image

root = Path(__file__).resolve().parents[1]
output = root / "public/social"
output.mkdir(parents=True, exist_ok=True)
source = root / "public/library/graphics/social/backgrounds/openline-share-card-white-on-orange-1200x630.png"
assert Image.open(source).size == (1200, 630)
copyfile(source, output / "openline-brand-library-v1.png")
with Image.open(root / "public/assets/apple-icon-1024.png") as image:
    image.convert("RGB").resize((180, 180), Image.Resampling.LANCZOS).save(output / "apple-touch-icon.png", optimize=True)
