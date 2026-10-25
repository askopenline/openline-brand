"""Reproducible native export from the canonical transparent Openline mark."""
from pathlib import Path
from PIL import Image
import json, zipfile, shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/assets'
PACK=ROOT/'icon-package'
REPO=ROOT.parent if (ROOT.parent/'logo/png/openline-logo-color.png').exists() else ROOT.parent/'openline-brand-assets'
SOURCE=REPO/'logo/png/openline-logo-color.png'
mark=Image.open(SOURCE).convert('RGBA')
mark=mark.crop(mark.getbbox())
mark.save(OUT/'mark.png')
def variant(tone):
    m=mark.copy()
    if tone in ('dark','mono'):
        pixels=list(m.getdata())
        m.putdata([(255,255,255,a) if tone=='mono' or max(r,g,b)<160 else (r,g,b,a) for r,g,b,a in pixels])
    return m
def icon(size,coverage=.435,tone='light',transparent=False):
    bg=(18,20,23,255) if tone=='dark' else (255,255,255,255)
    im=Image.new('RGBA',(size,size),(0,0,0,0) if transparent else bg)
    m=variant(tone); target=round(size*coverage); m.thumbnail((target,target),Image.Resampling.LANCZOS)
    im.alpha_composite(m,((size-m.width)//2,(size-m.height)//2))
    return im
for coverage in (42.2,43.5,44.8,49.6,52.7,55.8,58,62,66,68):
    for tone in ('light','dark'):
        icon(1024,coverage/100,tone).convert('RGB').save(OUT/f'icon-{coverage}-{tone}.png',optimize=True)
ios=PACK/'ios/AppIcon.appiconset';ios.mkdir(parents=True,exist_ok=True)
original=REPO/'app-icons/ios/AppIcon.appiconset/Contents.json'
contents=json.loads(original.read_text())
for row in contents['images']:
    size=round(float(row['size'].split('x')[0])*int(row['scale'][0]))
    icon(size).convert('RGB').save(ios/row['filename'],optimize=True)
(ios/'Contents.json').write_text(json.dumps(contents,indent=2)+'\n')
appear=PACK/'ios/appearance-references';appear.mkdir(parents=True,exist_ok=True)
icon(1024,tone='dark').convert('RGB').save(appear/'openline-dark-1024.png')
tinted=Image.new('RGB',(1024,1024),'#dedede')
tinted.paste((30,30,30),(0,0,1024,1024),icon(1024,tone='mono',transparent=True).getchannel('A'))
tinted.save(appear/'openline-tinted-reference-1024.png')
layers=PACK/'ios/icon-composer-layers';layers.mkdir(parents=True,exist_ok=True)
Image.new('RGB',(1024,1024),'white').save(layers/'background.png')
foreground=icon(1024,transparent=True)
for name,is_accent in [('mark-black',False),('accent-orange',True)]:
    im=foreground.copy()
    im.putdata([(r,g,b,a if ((r>g+35 and r>b+35)==is_accent) else 0) for r,g,b,a in im.getdata()])
    im.save(layers/f'{name}.png')
android=PACK/'android';android.mkdir(exist_ok=True)
for density,scale in [('mdpi',1),('hdpi',1.5),('xhdpi',2),('xxhdpi',3),('xxxhdpi',4)]:
    target=android/f'res/mipmap-{density}';target.mkdir(parents=True,exist_ok=True)
    icon(round(48*scale)).convert('RGB').save(target/'ic_launcher.png',optimize=True)
    # User-requested 17.5% reduction from the prior 48dp candidate.
    icon(round(108*scale),39.6/108,transparent=True).save(target/'ic_launcher_foreground.png')
    icon(round(108*scale),39.6/108,'mono',transparent=True).save(target/'ic_launcher_monochrome.png')
    reference=android/f'48dp-reference/mipmap-{density}'
    reference.mkdir(parents=True,exist_ok=True)
    icon(round(108*scale),48/108,transparent=True).save(reference/'ic_launcher_foreground.png')
    icon(round(108*scale),48/108,'mono',transparent=True).save(reference/'ic_launcher_monochrome.png')
for api in ('v26','v33'):
    dest=android/f'res/mipmap-anydpi-{api}';dest.mkdir(parents=True,exist_ok=True)
    mono='\n  <monochrome android:drawable="@mipmap/ic_launcher_monochrome"/>' if api=='v33' else ''
    (dest/'ic_launcher.xml').write_text('<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n  <background android:drawable="@color/openline_icon_background"/>\n  <foreground android:drawable="@mipmap/ic_launcher_foreground"/>'+mono+'\n</adaptive-icon>\n')
values=android/'res/values';values.mkdir(exist_ok=True)
(values/'colors.xml').write_text('<resources><color name="openline_icon_background">#FFFFFF</color></resources>\n')
icon(512).save(android/'google-play-icon-512.png',optimize=True)
icon(432,39.6/108,transparent=True).save(OUT/'android-foreground.png')
icon(432,39.6/108,'mono',transparent=True).save(OUT/'android-monochrome.png')
shutil.copy(ios/'icon-1024.png',OUT/'apple-icon-1024.png')
shutil.copy(android/'google-play-icon-512.png',OUT/'google-play-icon-512.png')
(PACK/'README.md').write_text("""# Openline mobile icon · final visual choice · 2026-10-07

Canonical mark geometry preserved. Default visible mark width: 43.5% of square,
approximately 17.5% smaller linearly than the 52.7% candidate. White square unchanged.
44.8% and 42.2% alternatives represent approximately 15% and 20% reductions from 52.7%.
Original export: approximately 68%. No pre-rendered corners or shadows.

## iOS
Import ios/AppIcon.appiconset into Assets.xcassets for the standard PNG workflow.
Default icons are opaque RGB PNGs. The 1024px icon is included.
icon-composer-layers contains full-canvas background, black mark and orange accent
layers for manual assembly in Apple's Icon Composer. These are SOURCE LAYERS,
not a compiled .icon document. Validate default, dark, tinted and clear appearances
in current Xcode on-device. Appearance-reference PNGs are design references only.

## Android
Merge android/res into your application resources; do not overwrite app resources
blindly. Point android:icon to @mipmap/ic_launcher. Configure roundIcon as appropriate
for your app and test masks on real devices. v26 adaptive XML and v33 monochrome XML
are supplied. The adaptive candidate spans 39.6dp on a 108dp canvas, a 17.5%
reduction from the prior 48dp artwork. This is below Android's recommended
48–66dp range: it is an explicit smaller-size experiment, not a recommendation
to skip native legibility testing. The android/48dp-reference directory supplies
foreground and monochrome replacements at the prior guideline-aligned size.
Masked appearance differs from iOS; validate every mask on actual launchers.
The 43.5% flat composition applies to iOS, legacy Android and store-listing icons.
Google Play icon: 512x512 RGBA PNG, fully opaque. No rounded corners baked in.

## Release gate
Paul approved the 43.5% flat visual composition on 7 October 2026. These files
are not store approval. Verify rendering in signed release builds; native
adaptive sizing, masks and appearances still need engineering/device validation.

Official guidance:
https://developer.apple.com/design/human-interface-guidelines/app-icons
https://developer.android.com/develop/ui/compose/system/icon_design_adaptive
https://support.google.com/googleplay/android-developer/answer/9866151?hl=en
""")
with zipfile.ZipFile(ROOT/'public/downloads/openline-native-icons.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(PACK.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(PACK))
print('Native icon package generated.')
