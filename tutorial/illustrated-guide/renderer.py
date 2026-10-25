"""Finish the approved illustrated edition without any new media generation."""
from pathlib import Path
import argparse, base64, hashlib, json, math, os, subprocess
import requests
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'hellen-tutorial-v3'
OUT = ROOT / 'deliverables'
PRIVATE = ROOT / 'private'
TMP = Path('/dev/shm/openline-hellen-v3-scratch')
PORTRAIT = ROOT.parent / 'hellen-full-tutorial/deliverables/hellen-office-portrait.jpg'
INTRO, SPEECH, OUTRO = (3.04, 175.01825, 6.04)
TOTAL = INTRO + SPEECH + OUTRO
MASTER = OUT / 'openline-hellen-animated-installation-guide.mp4'
for folder in (OUT, PRIVATE):
    folder.mkdir(parents=True, exist_ok=True)

def read(path):
    return json.loads(path.read_text())

def save(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')

def run(args):
    subprocess.run(args, check=True)

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], text=True))

def compose():
    for name in ('hellen-narration.wav', 'narration.txt', 'hellen-tutorial-en.ass', 'hellen-tutorial-en.srt', 'hellen-tutorial-en.vtt', 'openline-pleasant-sting.wav'):
        target = OUT / name
        if not target.exists():
            os.link(SOURCE / 'deliverables' / name, target)
    args, filters, layout = ([], '', '[0:v]')
    chapters = read(SOURCE / 'deliverables/chapters.json')
    for count, key in enumerate(('qr', 'labels', 'data', 'android'), 4):
        chapter = next((c for c in chapters if c['id'] == key))
        patch = TMP / f'{key}-layout-detail.mp4'
        assert patch.is_file()
        args += ['-itsoffset', str(INTRO + chapter['start']), '-threads', '1', '-i', str(patch)]
        filters += f"{layout}[{count}:v]overlay=0:0:eof_action=pass:enable='between(t,{INTRO + chapter['start']},{INTRO + chapter['end']})'[p{count}];"
        layout = f'[p{count}]'
    filters += f"[1:v]scale=720:842:force_original_aspect_ratio=increase,crop=720:842,setsar=1[portrait];{layout}[portrait]overlay=40:78:eof_action=pass:enable='between(t,{INTRO},{INTRO + SPEECH})'[illustrated];[illustrated]subtitles='{OUT / 'hellen-tutorial-en.ass'}'[v];[2:a]loudnorm=I=-16:TP=-1.5:LRA=8,adelay={round(INTRO * 1000)},apad[voice];[3:a]volume=0.55,asplit=2[s1][s2];[s2]adelay={round((INTRO + SPEECH) * 1000)}[end];[voice][s1][end]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.89:level=0[a]"
    run(['ffmpeg', '-v', 'error', '-y', '-threads', '1', '-i', str(TMP / 'animated-layout.mp4'), '-loop', '1', '-framerate', '30', '-threads', '1', '-i', str(PORTRAIT), '-i', str(OUT / 'hellen-narration.wav'), '-i', str(OUT / 'openline-pleasant-sting.wav')] + args + ['-filter_complex_threads', '1', '-filter_complex', filters, '-map', '[v]', '-map', '[a]', '-t', str(TOTAL), '-r', '30', '-c:v', 'libx264', '-threads', '1', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-movflags', '+faststart', str(MASTER)])
    run(['ffmpeg', '-v', 'error', '-y', '-ss', '55', '-i', str(MASTER), '-frames:v', '1', str(OUT / 'openline-hellen-guide-poster.jpg')])
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(MASTER), '-vf', 'scale=640:360', '-r', '12', '-c:v', 'libx264', '-threads', '1', '-preset', 'fast', '-crf', '29', '-c:a', 'aac', '-b:a', '96k', str(TMP / 'illustrated-review.mp4')])

def qa():
    import cv2
    import numpy as np
    run(['ffmpeg', '-v', 'error', '-threads', '1', '-i', str(MASTER), '-f', 'null', '-'])
    chapters = read(SOURCE / 'deliverables/chapters.json')
    times = [0.6, 1.5, 2.2] + [INTRO + c['start'] + (c['end'] - c['start']) * 0.55 for c in chapters] + [TOTAL - 2.5, TOTAL - 1.5, TOTAL - 0.2]
    cap = cv2.VideoCapture(str(MASTER))
    images, frames, codes = ([], [], [])
    for i, t in enumerate(times):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, frame = cap.read()
        assert ok, t
        frames.append(frame)
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image.save(PRIVATE / f'decoded-{i:02}.jpg', quality=92)
        images.append(image.resize((640, 360)))
        if t > TOTAL - 3:
            code, _, _ = cv2.QRCodeDetector().detectAndDecode(frame)
            assert code == 'https://openline.com/install', (t, code)
            codes.append({'seconds': t, 'url': code})
    cap.release()
    sheet = Image.new('RGB', (1920, math.ceil(len(images) / 3) * 360), 'white')
    for i, image in enumerate(images):
        sheet.paste(image, (i % 3 * 640, i // 3 * 360))
    sheet.save(PRIVATE / 'decoded-contact-sheet.jpg', quality=90)
    assert frames[0][30:60, 1634:1775].min() < 110
    assert frames[1][30:60, 1634:1775].min() > 235
    opacity = (255 - float(np.percentile(frames[2][28:61, 1814:1859], 2))) / (255 - float(np.percentile(frames[0][28:61, 1814:1859], 2)))
    assert 0.6 < opacity < 0.8
    info = probe(MASTER)
    assert abs(float(info['format']['duration']) - TOTAL) < 0.1
    video = next((s for s in info['streams'] if s['codec_type'] == 'video'))
    assert (video['width'], video['height'], video['r_frame_rate']) == (1920, 1080, '30/1')
    audio = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(MASTER), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=8:print_format=json', '-f', 'null', '-'], capture_output=True, text=True, check=True).stderr
    levels = json.loads(audio[audio.rfind('{'):audio.rfind('}') + 1])
    assert float(levels['input_tp']) <= -1
    save(PRIVATE / 'technical-qa.json', {'full_decode': True, 'duration_seconds': float(info['format']['duration']), 'width': 1920, 'height': 1080, 'fps': 30, 'qr_checks': codes, 'ai_badge_opacity_estimate': opacity, 'generated_by_removed_after_1200ms': True, 'presenter': 'Static approved Hellen office portrait, not a talking avatar', 'audio': 'One existing continuous narration, no joins or time stretch', 'audio_levels': levels, 'decoded_sample_count': len(times)})
    print('Technical QA passed', flush=True)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['compose', 'qa'])
    globals()[parser.parse_args().operation]()
