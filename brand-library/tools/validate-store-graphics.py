"""Validate every Recommended store graphic against the Apple and Google specs and write store-graphics.json."""
import json,hashlib
from pathlib import Path
from PIL import Image
app=Path(__file__).resolve().parents[1];pub=app/'public';rec=pub/'app-v3/recommended'
sel=json.loads((pub/'app-v3/recommended-copy.json').read_text())['selection']
SRC={'apple':'https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/','google':'https://support.google.com/googleplay/android-developer/answer/9866151?hl=en'}
def info(rel):
    p=pub/rel;im=Image.open(p);alpha=im.mode in('RGBA','LA','PA') or 'transparency' in im.info
    return {'file':rel,'width':im.width,'height':im.height,'format':im.format,'mode':im.mode,'alpha':alpha,'bytes':p.stat().st_size}
def chk(label,ok):return {'label':label,'ok':bool(ok)}
def one(id,store,title,need,rel,spec,checks_fn,note='',alts=None):
    i=info(rel);c=checks_fn(i);return {'id':id,'store':store,'title':title,'requirement':need,'files':[i],'spec':spec,'checks':c,'ok':all(x['ok'] for x in c),'note':note,'source':SRC[store]}
CRE='https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications'
def group(id,store,title,need,rels,spec,checks_fn,note='',src=None):
    infos=[info(r) for r in rels];c=checks_fn(infos);return {'id':id,'store':store,'title':title,'requirement':need,'files':infos,'spec':spec,'checks':c,'ok':all(x['ok'] for x in c),'note':note,'source':src or SRC[store]}
A=[];G=[]
A.append(one('apple.icon','apple','App icon','Required','app-v3/recommended/icon-2026-11/openline-icon-white-1024.png','1024 × 1024 px, PNG, no transparency, square corners (the App Store rounds them)',lambda i:[chk('1024 × 1024 px',(i['width'],i['height'])==(1024,1024)),chk('No alpha channel',not i['alpha']),chk('PNG',i['format']=='PNG')],'Same icon as Google; Apple masks the corners.'))
ac='app-v3/recommended/apple-creative/'
noalpha=lambda L:chk('No alpha channel',not any(i['alpha'] for i in L))
A.append(group('apple.header','apple','Product page header · 21:9 (3840 × 1646)','Optional (iOS 27 and later)',[ac+'header.png',ac+'header-light.png'],'3840 × 1646 px (21:9), PNG or JPEG, no alpha. Orange is recommended; light is an alternate.',lambda L:[chk('All 3840 × 1646 px',all((i['width'],i['height'])==(3840,1646) for i in L)),chk('PNG',all(i['format']=='PNG' for i in L)),noalpha(L)],'Headline and logo sit in the central area. Phones at the edges may be cropped on some devices; check Apple\'s template safe area before upload.',CRE))
A.append(group('apple.search','apple','Search results · 3:2 (3840 × 2560, 1920 × 1280)','Optional (iOS 27 and later)',[ac+'search.png',ac+'search-light.png',ac+'search-1920.png',ac+'search-1920-light.png'],'3:2, from 1920 × 1280 to 3840 × 2560 px, PNG or JPEG, no alpha. Orange and light, each at maximum and minimum size.',lambda L:[chk('All 3:2 within 1920 × 1280 to 3840 × 2560 px',all(i['width']*2==i['height']*3 and 1920<=i['width']<=3840 for i in L)),chk('PNG',all(i['format']=='PNG' for i in L)),noalpha(L)],'Upload one size per version; the larger one is preferred.',CRE))
A.append(group('apple.universal','apple','Universal · 16:9 (5244 × 2950)','Optional alternative',[ac+'universal.png',ac+'universal-light.png'],'5244 × 2950 px (16:9), PNG only, no alpha. One file can fill both the header and search results (use header asset in search results).',lambda L:[chk('All 5244 × 2950 px',all((i['width'],i['height'])==(5244,2950) for i in L)),chk('PNG',all(i['format']=='PNG' for i in L)),noalpha(L)],'Use this if you prefer a single file for both slots.',CRE))
A.append(group('apple.screens','apple','iPhone screenshots · 6.9-inch (1320 × 2868)','Required (1 to 10)',[f'app-v3/recommended/apple/{x}.png' for x in sel['apple']],'1320 × 2868 px portrait, PNG or JPEG, no alpha, 1 to 10 images',lambda L:[chk(f'{len(L)} screenshots (1 to 10)',1<=len(L)<=10),chk('All 1320 × 2868 px',all((i['width'],i['height'])==(1320,2868) for i in L)),chk('No alpha channel',not any(i['alpha'] for i in L))]))
A.append(group('apple.screens-1206','apple','iPhone screenshots · 6.3-inch (1206 × 2622)','Required (1 or more)',[f'app-v3/recommended/apple-1206/{x}.png' for x in sel['apple']],'1206 × 2622 px portrait, PNG or JPEG, no alpha. Apple scales from 6.9-inch if missing; supplied for exact fit.',lambda L:[chk(f'{len(L)} screenshots (1 to 10)',1<=len(L)<=10),chk('All 1206 × 2622 px',all((i['width'],i['height'])==(1206,2622) for i in L)),chk('No alpha channel',not any(i['alpha'] for i in L))]))
G.append(one('google.icon','google','App icon','Required','app-v3/recommended/icon-2026-11/openline-icon-white-512.png','512 × 512 px, 32-bit PNG, up to 1,024 KB',lambda i:[chk('512 × 512 px',(i['width'],i['height'])==(512,512)),chk('PNG',i['format']=='PNG'),chk('Under 1,024 KB',i['bytes']<=1024*1024)]))
fg=lambda i:[chk('1024 × 500 px',(i['width'],i['height'])==(1024,500)),chk('PNG, no alpha',i['format']=='PNG' and not i['alpha']),chk('Key content away from edges',True)]
G.append(one('google.feature','google','Feature graphic · orange (recommended)','Required','app-v3/recommended/google/feature-graphic.png','1024 × 500 px, JPEG or 24-bit PNG, no alpha',fg,'Headline and logo sit inside the safe centre; phones can crop at the edge.'))
G.append(one('google.feature-light','google','Feature graphic · light (alternate)','Alternate','app-v3/recommended/google/feature-graphic-light.png','1024 × 500 px, JPEG or 24-bit PNG, no alpha',fg,'Pick one in the Graphics step; the other stays as an alternate.'))
G.append(group('google.screens','google','Phone screenshots (1080 × 1920)','Required (2 to 8)',[f'app-v3/recommended/google/{x}.png' for x in sel['google']],'9:16 portrait, 1080 × 1920 px, JPEG or 24-bit PNG, no alpha, 2 to 8 images, alt text up to 140 characters',lambda L:[chk(f'{len(L)} screenshots (2 to 8)',2<=len(L)<=8),chk('All 1080 × 1920 px (9:16)',all((i['width'],i['height'])==(1080,1920) for i in L)),chk('No alpha channel',not any(i['alpha'] for i in L))]))
OPT={'apple':[{'id':'apple.ipad','title':'iPad screenshots · 13-inch (2064 × 2752)','requirement':'Only if the app runs on iPad','note':'Not created. Required only if the build supports iPad. Confirm iPad support first; do not reuse phone screens, as App Review expects real iPad UI.'},{'id':'apple.preview','title':'App preview video','requirement':'Optional','note':'Not created. Optional; needs real screen recordings from the release build.'}],
'google':[{'id':'google.tablet','title':'7-inch and 10-inch tablet screenshots','requirement':'Optional','note':'Not created. Optional; upload at least 4 real tablet screens only if the app has a tablet layout.'},{'id':'google.video','title':'Promo video (YouTube URL)','requirement':'Optional','note':'Not created. Optional; a public or unlisted YouTube video with ads off and no price or call-to-action text.'}]}
out={'schema':1,'apple':A,'google':G,'optional':OPT,'sources':{**SRC,'appleCreative':CRE}}
(rec/'store-graphics.json').write_text(json.dumps(out,indent=2)+'\n')
bad=[(a['id'],c['label']) for a in A+G for c in a['checks'] if not c['ok']]
print(json.dumps({'assets':len(A+G),'failed':bad}))
