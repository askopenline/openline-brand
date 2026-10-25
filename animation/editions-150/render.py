"""85 deterministic editions: 17 original scores x 5 exact-artwork layouts.
No paid media generation. Original 152-frame/3.04s timing preserved four times.
Run sequentially on two-CPU sandboxes; resumes completed files.
"""
from pathlib import Path
import argparse, hashlib, json, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw
from scipy.signal import butter, sosfilt, resample_poly

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/"motion-plus/sources/readme-original.gif"
if not SOURCE.exists():SOURCE=ROOT.parents[1]/"animation/loading-loop/openline-loading-loop.gif"
HASH="7ac58794335fb9250d87161122a51867fd5cdd7c49a158468015453b5980cc0c"
FPS=50; SR=48000; DURATION=12.16
FF=["ffmpeg","-hide_banner","-loglevel","error","-y","-threads","1","-filter_threads","1"]
LAYOUTS=[
 ("native-square","Native square",1000,1000,(255,255,255),0,0,False),
 ("horizontal-white","Horizontal white",1920,1080,(255,255,255),460,40,False),
 ("horizontal-orange","Horizontal orange",1920,1080,(255,101,24),460,40,True),
 ("horizontal-cream","Horizontal cream",1920,1080,(255,245,233),10,40,False),
 ("horizontal-night","Horizontal night",1920,1080,(23,23,23),910,40,True),
]
SCORES=[
 ("felt-keys","Felt keys","felt",48,[0,4,7,12],.8),
 ("wooden-steps","Wooden steps","wood",50,[0,7,3,10],.55),
 ("glass-orbit","Glass orbit","bell",60,[0,2,7,9],1.25),
 ("soft-marimba","Soft marimba","mallet",53,[0,5,7,12],.75),
 ("warm-circuit","Warm circuit","reed",45,[0,7,10,14],.8),
 ("air-and-oak","Air and oak","wood",43,[0,5,9,12],.6),
 ("quiet-celesta","Quiet celesta","bell",57,[0,4,9,7],1.4),
 ("rounded-pulse","Rounded pulse","bass",38,[0,7,12,5],.5),
 ("paper-rhythm","Paper rhythm","brush",55,[0,2,9,7],.4),
 ("plucked-horizon","Plucked horizon","pluck",50,[0,4,7,11],.85),
 ("velvet-chords","Velvet chords","pad",45,[0,5,9,12],1.4),
 ("reed-and-rain","Reed and rain","reed",52,[0,3,7,10],.8),
 ("amber-bells","Amber bells","bell",55,[0,7,9,14],1.25),
 ("low-tide","Low tide","bass",41,[0,5,7,12],.8),
 ("silver-answer","Silver answer","mallet",59,[0,2,7,12],.8),
 ("soft-arrival","Soft arrival","felt",53,[0,4,9,12],1.0),
 ("open-cadence","Open cadence","pluck",48,[0,7,12,16],1.0),
]

def run(args):return subprocess.run(args,check=True,capture_output=True)
def save(path,obj):path.write_text(json.dumps(obj,indent=2)+"\n")
def sha(path):return hashlib.file_digest(path.open("rb"),"sha256").hexdigest()
def tone(kind,f,d,rng):
 t=np.arange(int(d*SR))/SR; attack=1-np.exp(-t/.012)
 if kind=="wood":x=np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*f*1.47*t);env=attack*np.exp(-t*12)
 elif kind=="bell":x=np.sin(2*np.pi*f*t)+.16*np.sin(2*np.pi*f*2.04*t);env=attack*np.exp(-t*3)
 elif kind=="mallet":x=np.sin(2*np.pi*f*t)+.2*np.sin(2*np.pi*f*3*t)*np.exp(-t*12);env=attack*np.exp(-t*6)
 elif kind=="reed":x=np.sin(2*np.pi*f*t)+.1*np.sin(2*np.pi*f*3*t);env=attack*np.exp(-t*5)
 elif kind=="bass":x=np.sin(2*np.pi*(f*t+1.8*(1-np.exp(-t*16))));env=attack*np.exp(-t*6)
 elif kind=="brush":x=sosfilt(butter(2,[300,2600],fs=SR,btype="bandpass",output="sos"),rng.normal(size=len(t)));env=attack*np.exp(-t*15)
 elif kind=="pad":x=np.sin(2*np.pi*f*t)+.1*np.sin(2*np.pi*f*2*t);env=np.sin(np.pi*t/d)**2
 else:x=np.sin(2*np.pi*f*t)+.16*np.sin(2*np.pi*f*2*t)*np.exp(-t*8);env=attack*np.exp(-t*(4 if kind=="felt" else 7))
 return x*env*np.clip((d-t)/.08,0,1)

def plates():
 assert sha(SOURCE)==HASH
 im=Image.open(SOURCE);assert im.n_frames==152 and im.size==(1000,1000)
 for slug,title,w,h,bg,x,y,white in LAYOUTS:
  path=ROOT/"plates"/f"{slug}.mp4";cycle=ROOT/"private"/f"{slug}-cycle.mp4"
  if path.exists():continue
  p=subprocess.Popen(FF+["-f","rawvideo","-pix_fmt","rgb24","-s",f"{w}x{h}","-r","50","-i","-","-an","-c:v","libx264","-threads","1","-preset","fast","-crf","18","-pix_fmt","yuv420p","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",str(cycle)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  for k in range(152):
   im.seek(k);assert im.info["duration"]==20
   a=np.asarray(im.convert("RGB"));frame=Image.new("RGB",(w,h),bg)
   if slug in ("native-square","horizontal-white"):frame.paste(Image.fromarray(a),(x,y))
   else:
    alpha=np.clip((255-a.min(axis=2).astype(float))*255/231,0,255).astype("uint8")
    fg=Image.new("RGB",(1000,1000),(255,255,255)) if white else Image.fromarray(a)
    frame.paste(fg,(x,y),Image.fromarray(alpha))
    # Quiet framing lines stay outside the source mark; never redraw the icon.
    dr=ImageDraw.Draw(frame)
    if slug=="horizontal-cream":
     for j in range(3):dr.line((1120,440+j*100,1690-j*110,440+j*100),fill=(225,208,193),width=2)
    elif slug=="horizontal-night":
     for j in range(3):dr.line((200+j*110,440+j*100,800,440+j*100),fill=(65,61,57),width=2)
   p.stdin.write(frame.tobytes())
   if k==90:frame.save(ROOT/"posters"/f"{slug}.jpg",quality=92)
  p.stdin.close();err=p.stderr.read();assert p.wait()==0,err
  run(FF+["-stream_loop","3","-i",str(cycle),"-t",str(DURATION),"-c","copy","-movflags","+faststart",str(path)])
  run(FF+["-i",str(path),"-vf","fps=10,scale=320:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse","-loop","0",str(ROOT/"gif"/f"{slug}-silent.gif")])
  cycle.unlink();print("PLATE",slug,flush=True)

def audio(si,li):
 score=SCORES[si];slug,title,kind,base,intervals,decay=score
 rng=np.random.default_rng(82000+si*5+li);mix=np.zeros((round(DURATION*SR),2));events=[]
 def add(k,at,midi,gain,d,pan=0):
  f=440*2**((midi-69)/12);v=tone(k,f,d,rng)*gain
  start=round(at*SR);n=min(len(v),len(mix)-start)
  if n<=0:return
  mix[start:start+n]+=v[:n,None]*np.array([math.sqrt((1-pan)/2),math.sqrt((1+pan)/2)])
  events.append({"kind":k,"at":round(at,3),"midi":midi,"duration":d,"gain":gain,"pan":pan})
 # Quarter turns are 0.76 seconds at native speed; five arrangements per score.
 for q in range(16):
  at=q*.76+.44; note=base+intervals[(q+(li if li%2 else 0))%4]
  if li==4:note=base+intervals[(15-q)%4]
  add(kind,at,note,.65,decay,(-.28 if q%2 else .28))
  if li in (1,3) and q%2==0:add("felt",at+.19,note+12,.18,.55,.3)
  if li in (2,4) and q%4==0:add("pad",q*.76,base-12,.24,2.6)
  if (q+si)%3==0:add("brush",q*.76+.12,base,.035,.32,-.2)
  if li==0 and q%4==0:add("bass",q*.76+.1,base-12,.13,.45)
 for m in [base,base+7,base+12]:add("felt",10.95,m,.15,1.15)
 mix=sosfilt(butter(3,4200,fs=SR,output="sos"),mix,axis=0)
 fade=round(.1*SR);mix[:fade]*=np.linspace(0,1,fade)[:,None];mix[-fade:]*=np.linspace(1,0,fade)[:,None]
 peak=np.max(np.abs(resample_poly(mix,4,1,axis=0)));mix*=10**(-5/20)/max(peak,1e-9)
 name=f"{si+1:02d}-{slug}-{LAYOUTS[li][0]}";temp=ROOT/"private"/"temp.wav"
 with wave.open(str(temp),"wb") as f:
  f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((mix*32767).astype("<i2").tobytes())
 out=ROOT/"audio"/f"{name}.flac"
 run(FF+["-i",str(temp),"-c:a","flac","-compression_level","8",str(out)])
 temp.unlink()
 return name,events

def editions():
 allitems=[];checks=[]
 for si,score in enumerate(SCORES):
  for li,layout in enumerate(LAYOUTS):
   slug,title,w,h,*_=layout;name=f"{si+1:02d}-{score[0]}-{slug}"
   video=ROOT/"mp4"/f"{name}.mp4";sound=ROOT/"audio"/f"{name}.flac"
   events=ROOT/"scores"/f"{name}.json"
   if not sound.exists():
    _,ev=audio(si,li);save(events,ev)
   if not video.exists():
    run(FF+["-i",str(ROOT/"plates"/f"{slug}.mp4"),"-i",str(sound),"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","160k","-t",str(DURATION),"-movflags","+faststart",str(video)])
   check=ROOT/"qa"/f"{name}.json"
   if not check.exists():
    run(FF+["-i",str(video),"-f","null","-"])
    probe=json.loads(run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(video)]).stdout)
    v=next(s for s in probe["streams"] if s["codec_type"]=="video")
    assert (v["width"],v["height"])==(w,h) and abs(float(probe["format"]["duration"])-DURATION)<.08
    raw=run(FF+["-i",str(video),"-vn","-f","f32le","-"]).stdout
    a=np.frombuffer(raw,dtype="<f4").reshape(-1,2);peak=float(np.max(np.abs(resample_poly(a,4,1,axis=0))))
    assert peak<.9
    save(check,{"whole_decode":True,"duration":float(probe["format"]["duration"]),"width":w,"height":h,"true_peak_db":round(20*math.log10(peak),2),"clipped_samples":int(np.sum(np.abs(a)>=1)),"sha256":sha(video)})
   checks.append(json.loads(check.read_text()))
   allitems.append({"id":"native-sound-"+name,"title":score[1]+" · "+title,"score":score[1],"layout":title,
    "duration_seconds":DURATION,"width":w,"height":h,"mp4":"mp4/"+video.name,"audio":"audio/"+sound.name,
    "poster":f"posters/{slug}.jpg","gif":f"gif/{slug}-silent.gif","score_events":"scores/"+events.name})
   print("EDITION",len(allitems),name,flush=True)
 save(ROOT/"manifest.json",{"version":1,"editions":allitems,"count":len(allitems),"sound_families":17,"visual_layouts":5,"horizontal_editions":68,"source_sha256":HASH,"source_frames":152,"source_cycle_seconds":3.04,"cycles":4,"native_speed_preserved":True,"notes":"85 sound/layout editions, not 85 new animation concepts. GIFs are silent shared layout previews. FLAC files are lossless original stereo scores. No paid media calls; synthesized audio, not recorded instruments. Artwork derivatives are review candidates."})
 save(ROOT/"qa-summary.json",{"count":len(checks),"all_pass":len(checks)==85 and all(x["whole_decode"] and x["clipped_samples"]==0 for x in checks),"checks":checks})

if __name__=="__main__":
 for p in ["mp4","audio","scores","plates","posters","gif","qa","private"]:(ROOT/p).mkdir(parents=True,exist_ok=True)
 plates();editions()
