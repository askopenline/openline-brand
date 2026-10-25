"""One complete current mobile launch bundle; no competitor assets or obsolete art."""
from pathlib import Path
import json, zipfile, hashlib

root=Path(__file__).resolve().parents[1]
public=root/'public'
downloads=public/'downloads'
manifest=[]
with zipfile.ZipFile(downloads/'openline-all-resources.zip','w',zipfile.ZIP_DEFLATED) as z:
    def add(p,arc):
        z.write(p,arc)
        manifest.append({'path':arc,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    for p in sorted((public/'series/signal').glob('*.png')):
        add(p,'screenshots/'+('iphone/' if p.name.startswith('ios') else 'android/')+p.name)
    add(public/'series/signal/contact-sheet.jpg','screenshots/contact-sheet.jpg')
    for name,dest in [
        ('openline-final-icon-all-formats.zip','icons/approved-icon-all-formats.zip'),
        ('openline-native-icons.zip','icons/native-icon-resources.zip'),
        ('openline-orange-series-sources.zip','editable-artwork/screenshot-sources.zip'),
        ('openline-apple-submission-draft.zip','submission-drafts/apple.zip'),
        ('openline-google-submission-draft.zip','submission-drafts/google.zip'),
        ('openline-submission-sources.zip','editable-artwork/submission-sources.zip')
    ]: add(downloads/name,dest)
    for name in ['openline-store-copy.md','openline-store-settings.md','openline-release-checklist.md',
                 'openline-launch-workspace.json','store-requirements.md','submission-audit.md',
                 'screenshot-compliance-review.md','positioning-claims.md','orange-series-handoff.md',
                 'orange-series-manifest.json','console-metadata.json','submission-copy-review.md']:
        add(downloads/name,'handoff/'+name)
    add(root/'sources.json','handoff/official-sources.json')
    add(public/'series.json','editable-artwork/series.json')
    add(public/'assets/google-feature.png','feature-graphic/google-feature-review.png')
    z.writestr('README.md',"""# Openline complete mobile launch resources

Current iPhone and Android screenshot designs, approved icon formats, native icon
resources, editable screenshot sources, store copy, settings, checklist and policies.
The icon choice is final; screenshots and feature graphic are review candidates.
Separate Apple and Google submission drafts are included under submission-drafts/.
They use conservative metadata and overlays without replacing the marketing master.
Both remain blocked on native captures and release evidence; read their readiness notes.

Both platforms end with “Smarter market. Better prices.” and an explicit OMDM
supplier-comparison explanation. Comparative pricing needs launch evidence. The network dashboard
is fifth. Backgrounds alternate orange and warm cream. All six app views are
supplied React design captures, not verified native release captures.
Artwork has no review footer, category micro-label or qualification strip.
The larger final headline restores the value story. Review status and claim boundaries
are retained in the handoff documents and the site's Archive view.

No competitor imagery, superseded screenshot series, credentials, signed app
binaries or native app source code is included. This is the complete current
mobile launch resource bundle, not an archive of the entire brand repository.
Read handoff/screenshot-compliance-review.md before any store submission.

Live previews: https://openline-brand.fly.dev
Archive and working notes: https://openline-brand.fly.dev/#archive
iPhone: https://openline-brand.fly.dev/#iphone
Android: https://openline-brand.fly.dev/#android
App Store: https://openline-brand.fly.dev/#app-store
Google Play: https://openline-brand.fly.dev/#google-play
""")
    z.writestr('manifest.json',json.dumps(manifest,indent=2))
print(f'Packaged {len(manifest)} current resources with checksums.')
