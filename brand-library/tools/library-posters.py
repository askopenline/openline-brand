from pathlib import Path
import json,subprocess
from urllib.parse import unquote
APP=Path(__file__).resolve().parents[1];PUB=APP/"public";catalog=PUB/"library/catalog.json"
data=json.loads(catalog.read_text())
out=PUB/"library/posters";out.mkdir(exist_ok=True)
for a in data["cards"]:
    if a["kind"]!="video" or a.get("poster"):continue
    src=PUB/unquote(a["preview"][2:]);dst=out/(a["id"]+".jpg")
    if not dst.exists():
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-threads","1","-ss","0.5","-i",str(src),"-frames:v","1","-vf","scale=480:-2","-threads","1","-q:v","3",str(dst)],check=True)
    a["poster"]="./library/posters/"+dst.name
catalog.write_text(json.dumps(data,ensure_ascii=False,separators=(",",":")))
print("Video poster previews completed")
