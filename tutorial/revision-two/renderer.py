"""Review render: edge-to-edge portrait, larger phone, normal-rate narration."""
from pathlib import Path
import argparse, ast, base64, json, math, re, subprocess, types
from PIL import Image, ImageDraw, ImageOps
import requests
ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'hellen-tutorial-v3'
OUT = ROOT / 'deliverables'
PRIVATE = ROOT / 'private'
TMP = Path('/dev/shm/openline-hellen-r2')
for p in (OUT, PRIVATE, TMP):
    p.mkdir(exist_ok=True, parents=True)
W, H, FPS = (1920, 1080, 30)
RATE = 1.25
INTRO, OUTRO = (3.04, 7.04)
SPEECH = 175.01825 / RATE
TOTAL = INTRO + SPEECH + OUTRO
MASTER = OUT / 'openline-hellen-guide-r2.mp4'
tree = ast.parse((OLD / 'compose.py').read_text())
body = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any((isinstance(t, ast.Name) and t.id == 'p' for t in node.targets)):
        break
    body.append(node)
namespace = {'__file__': str(OLD / 'compose.py'), '__name__': 'illustration_library'}
exec(compile(ast.Module(body=body, type_ignores=[]), str(OLD / 'compose.py'), 'exec'), namespace)
M = types.SimpleNamespace(**namespace)
portrait = ImageOps.fit(Image.open(ROOT.parent / 'hellen-full-tutorial/deliverables/hellen-office-portrait.jpg').convert('RGB'), (640, 1080), method=Image.Resampling.LANCZOS, centering=(0.5, 0.45))
wordmark = Image.open(ROOT.parent / 'graphics/transparent/wordmark/openline-wordmark-black-1024.png').convert('RGBA')
copy = json.loads((PRIVATE / 'copy.json').read_text()) if (PRIVATE / 'copy.json').exists() else {}

def save(p, obj):
    p.write_text(json.dumps(obj, indent=2) + '\n')

def run(cmd):
    subprocess.run(cmd, check=True)

def text(d, xy, s, n=36, fill=M.INK, b=False, width=530):
    return M.tx(d, xy, s, n, fill, b, width, spacing=10)

def brand(im, x, y, width):
    image = wordmark.resize((width, round(width * wordmark.height / wordmark.width)), Image.Resampling.LANCZOS)
    im.paste(image, (x, y), image)

def frame(t):
    im = Image.new('RGB', (W, H), M.CREAM)
    d = ImageDraw.Draw(im)
    if t < INTRO or t >= INTRO + SPEECH:
        im.paste('white', (0, 0, W, H))
        d = ImageDraw.Draw(im)
        end = t >= INTRO + SPEECH
        age = t - INTRO - SPEECH if end else t
        if end:
            M.logo_at(im, 105, 80, age, size=280)
            brand(im, 450, 131, 670)
            text(d, (110, 410), 'Ready for your next chapter.', 78, b=True, width=1700)
            qr = M.qr.resize((368, 368), Image.Resampling.NEAREST)
            im.paste(qr, (130, 609))
            text(d, (600, 692), 'openline.com/install', 82, b=True, width=1250)
            text(d, (605, 812), 'Scan to open the installation guide.', 36, fill=M.MUTED, width=1180)
        else:
            M.logo_at(im, 110, 285, age, size=420)
            brand(im, 675, 270, 850)
            text(d, (680, 490), "Let's get you connected.", 84, b=True, width=1110)
            text(d, (685, 735), 'Your Openline eSIM, step by step.', 42, fill=M.MUTED, width=1090)
        M.badge(im, t)
        alpha = min(1, age / 0.35)
        tail = (OUTRO if end else INTRO) - age
        alpha = min(alpha, tail / 0.4)
        base = Image.new('RGB', (W, H), '#171717' if end and tail < 0.4 else 'white')
        return Image.blend(base, im, max(0, alpha))
    original = (t - INTRO) * RATE
    chapter = max((c for c in M.chapters if c['start'] <= original), key=lambda c: c['start'], default=M.chapters[0])
    n = next((i for i, c in enumerate(M.chapters) if c['id'] == chapter['id']))
    im.paste(portrait, (0, 0))
    item = copy['chapters'][chapter['id']]
    text(d, (690, 77), f'{n + 1:02} / {len(M.chapters):02}', 24, fill=M.ORANGE, b=True)
    text(d, (690, 139), item['title'], 58, b=True, width=530)
    y = 367
    age = (original - chapter['start']) / RATE
    for i, line in enumerate(item['bullets']):
        M.check(d, 690, y + 9, M.ease((age - 0.25 - i * 0.25) / 0.4), size=30)
        y = text(d, (740, y), line, 34, width=470) + 43
    if item.get('note'):
        text(d, (690, 806), item['note'], 26, fill=M.ORANGE, width=530)
    panel = M.panel(chapter, original)
    phone = panel.crop((546, 143, 1026, 925)).resize((608, 991), Image.Resampling.LANCZOS)
    im.paste(phone, (1286, 40))
    M.badge(im, t)
    d.rounded_rectangle((690, 915, 1220, 919), 2, fill='#E4DCD2')
    d.rounded_rectangle((690, 915, 690 + round(530 * original / 175.01825), 919), 2, fill=M.ORANGE)
    if t - INTRO < 0.25:
        im = Image.blend(Image.new('RGB', (W, H), 'white'), im, (t - INTRO) / 0.25)
    return im

def captions():
    original = json.loads((OLD / 'deliverables/caption-cues.json').read_text())
    header = (OLD / 'deliverables/hellen-tutorial-en.ass').read_text().split('[Events]')[0]
    header = header.replace('Lato,46,', 'Lato,38,')
    header += '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
    events = []
    srt = []
    vtt = []
    for i, cue in enumerate(original, 1):
        start = INTRO + (cue['start'] - 3.04) / RATE
        end = INTRO + (cue['end'] - 3.04) / RATE
        srt.append(f'{i}\n{M.ts(start)} --> {M.ts(end)}\n{cue['text']}')
        vtt.append(f'{M.ts(start, '.')} --> {M.ts(end, '.')}\n{cue['text']}')
        line = ''
        breaks = set()
        for j, w in enumerate(cue['words']):
            test = (line + ' ' + w['word']).strip()
            if M.font(38, True).getlength(test) > 535 and line:
                breaks.add(j)
                line = w['word']
            else:
                line = test
        for j, w in enumerate(cue['words']):
            a = INTRO + w['start'] / RATE
            b = INTRO + cue['words'][j + 1]['start'] / RATE if j + 1 < len(cue['words']) else end
            rendered = ''
            for k, v in enumerate(cue['words']):
                rendered += '\\N' if k in breaks else ' ' if k else ''
                rendered += '{\\c&H008EC9FF&}' + v['word'] + '{\\c&H00FFFFFF&}' if k == j else v['word']
            events.append(f'Dialogue: 0,{M.ass_ts(a)},{M.ass_ts(max(a + 0.02, b))},Default,,0,0,0,,{{\\an2\\pos(957,1038)}}' + rendered)
    (OUT / 'openline-hellen-guide-r2.ass').write_text(header + '\n'.join(events) + '\n')
    (OUT / 'openline-hellen-guide-r2.srt').write_text('\n\n'.join(srt) + '\n')
    (OUT / 'openline-hellen-guide-r2.vtt').write_text('WEBVTT\n\n' + '\n\n'.join(vtt) + '\n')

def preview():
    for name, t in [('intro', 1.5), ('manual', INTRO + 49 / RATE), ('android', INTRO + 150 / RATE), ('outro', TOTAL - 2)]:
        frame(t).save(PRIVATE / f'preview-{name}.jpg', quality=93)

def render():
    captions()
    filters = f"[0:v]subtitles='{OUT / 'openline-hellen-guide-r2.ass'}'[v];[1:a]atempo={RATE},loudnorm=I=-16:TP=-1.5:LRA=8,adelay=3040,apad[voice];[2:a]volume=.55,asplit=2[s1][s2];[s2]adelay={round((INTRO + SPEECH) * 1000)}[end];[voice][s1][end]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=.89:level=0[a]"
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', '30', '-i', '-', '-i', str(OLD / 'deliverables/hellen-narration.wav'), '-i', str(OLD / 'deliverables/openline-pleasant-sting.wav'), '-filter_complex_threads', '1', '-filter_complex', filters, '-map', '[v]', '-map', '[a]', '-t', str(TOTAL), '-c:v', 'libx264', '-threads', '1', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', str(MASTER)]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(math.ceil(TOTAL * FPS)):
        process.stdin.write(frame(i / FPS).tobytes())
        if i % (30 * 15) == 0:
            print('Rendered', i / 30, '/', TOTAL, flush=True)
    process.stdin.close()
    assert process.wait() == 0
    run(['ffmpeg', '-v', 'error', '-y', '-ss', '45', '-i', str(MASTER), '-frames:v', '1', str(OUT / 'openline-hellen-guide-r2.jpg')])
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(MASTER), '-vf', 'scale=640:360', '-r', '12', '-c:v', 'libx264', '-threads', '1', '-preset', 'fast', '-crf', '29', '-c:a', 'aac', '-b:a', '96k', str(TMP / 'review.mp4')])

def qa():
    import cv2
    run(['ffmpeg', '-v', 'error', '-i', str(MASTER), '-f', 'null', '-'])
    cap = cv2.VideoCapture(str(MASTER))
    images = []
    codes = []
    times = [0.05, 1.5, INTRO + 0.1] + [INTRO + (c['start'] + (c['end'] - c['start']) * 0.55) / RATE for c in M.chapters] + [TOTAL - 3.8, TOTAL - 2, TOTAL - 0.8, TOTAL - 0.05]
    for i, t in enumerate(times):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, f = cap.read()
        assert ok
        im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
        im.save(PRIVATE / f'decoded-{i:02}.jpg', quality=90)
        images.append(im.resize((640, 360)))
        if TOTAL - 4 < t < TOTAL - 0.5:
            code, _, _ = cv2.QRCodeDetector().detectAndDecode(f)
            assert code == 'https://openline.com/install', (t, code)
            codes.append(t)
    cap.release()
    sheet = Image.new('RGB', (1920, 360 * math.ceil(len(images) / 3)), 'white')
    for i, im in enumerate(images):
        sheet.paste(im, (i % 3 * 640, i // 3 * 360))
    sheet.save(PRIVATE / 'contact-sheet.jpg', quality=90)
    levels = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(MASTER), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=8:print_format=json', '-f', 'null', '-'], capture_output=True, text=True, check=True).stderr
    loudness = json.loads(levels[levels.rfind('{'):levels.rfind('}') + 1])
    assert float(loudness['input_tp']) <= -1
    save(PRIVATE / 'technical-qa.json', {'decode': True, 'duration': TOTAL, 'speech_speed': RATE, 'portrait_panel': [0, 0, 640, 1080], 'phone_height': 991, 'qr_samples': codes, 'audio': loudness, 'fades': 'Intro in/out, body fade-in and outro in/out', 'new_avatar_generation': False})
