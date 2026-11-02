"""Bounded OpenRouter review of actual final audio/video, not TTS input alone."""
import argparse
import base64
import json
from pathlib import Path
import subprocess
import requests

ROOT = Path(__file__).resolve().parents[2] / "openline-brand-expansion/campaign-voice-ten"
PRIVATE = ROOT / "_private/final-review"
PRIVATE.mkdir(parents=True, exist_ok=True)
manifest = json.loads((ROOT / "manifest.json").read_text())
p = argparse.ArgumentParser()
p.add_argument("operation", choices=["prepare", "review"])
p.add_argument("--batch", type=int, default=0)
a = p.parse_args()
if a.operation == "prepare":
    for i, ad in enumerate(manifest["ads"], 1):
        output = PRIVATE / f"review-{i:02d}.mp4"
        if not output.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / ad["mp4"]),
                            "-vf", "scale=360:640", "-r", "12", "-c:v", "libx264",
                            "-threads", "1", "-preset", "fast", "-crf", "27",
                            "-c:a", "aac", "-b:a", "64k", str(output)], check=True)
    print("Ten complete audiovisual review copies prepared; masters unchanged.")
else:
    assert a.batch in (1, 2)
    response_path = PRIVATE / f"response-{a.batch}.json"
    assert not response_path.exists(), "Response exists; inspect instead of resubmitting."
    ads = manifest["ads"][(a.batch-1)*5:a.batch*5]
    content = [{"type": "text", "text":
        "Review these FIVE finished 22.08-second Openline vertical ads, each WITH ACTUAL AUDIO. "
        "These are 360x640 12fps analysis copies of 1080x1920 50fps masters; do not mistake reduced sampling for a master defect. "
        "Listen to all speech; assess naturalness, intelligibility, continuity, abrupt ending or mismatched voice. "
        "Inspect video for major defects, illegible overlays, QR/endcard overlap, subtitle mismatch and obvious scene continuity errors. "
        "They are fictional AI travel scenes, NOT real customers, UI recordings or network evidence. "
        "Claims allowed: destination travel-data eSIMs, choosing suitable plans, partner-network choices; device compatibility matters. "
        "Do not demand a real phone demonstration from these lifestyle ads. Flag material false promises or confusing copy, not harmless advertising puffery. "
        "For EACH numbered clip return {id,transcript,script_match,voice_quality,visual_quality,material_issues:[],pass:boolean}. "
        "Transcribe what you HEAR, do not simply repeat the supplied expected script. Normalize Openline dot com versus Openline.com. "
        "Also proofread the UI copy below, correcting 'filmed' to 'AI-generated' and wrong 21-second duration to 22 seconds. "
        "Return concise JSON {reviews:[],ui:{title,description,disclosure},publication_notes:[]}. "
        "Review concepts are NOT certified ad-platform compliance. Do not imply fictional images prove actual coverage/speed. "
        "UI input: " + json.dumps(manifest["ui"])}]
    for i, ad in enumerate(ads, (a.batch-1)*5+1):
        content += [{"type": "text", "text": f"CLIP {i:02d}, {ad['title']}. Expected text for comparison only: {ad['story']}"},
                    {"type": "video_url", "video_url": {"url": "data:video/mp4;base64," +
                       base64.b64encode((PRIVATE / f"review-{i:02d}.mp4").read_bytes()).decode()}}]
    payload = {"model": "google/gemini-2.5-flash", "max_tokens": 5500,
               "temperature": 0.15, "response_format": {"type": "json_object"},
               "messages": [{"role": "user", "content": content}], "usage": {"include": True}}
    (PRIVATE / f"request-{a.batch}.json").write_text(json.dumps(payload))
    r = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, timeout=240,
                      verify="/etc/ssl/certs/ca-certificates.crt")
    r.raise_for_status()
    data = r.json()
    response_path.write_text(json.dumps(data, indent=2))
    answer = json.loads(data["choices"][0]["message"]["content"])
    (PRIVATE / f"review-{a.batch}.json").write_text(json.dumps(answer, indent=2))
    print(json.dumps({"review": answer, "usage": data.get("usage")}, indent=2))
