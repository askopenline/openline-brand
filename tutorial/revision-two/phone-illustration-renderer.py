"""Animated illustrated phone walkthrough; streamed frames, one encoding thread."""
from pathlib import Path
import argparse, functools, json, math, re, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import qrcode
ROOT=Path(__file__).resolve().parent;OUT=ROOT/"deliverables";P=ROOT/"private"
TMP=Path("/dev/shm/openline-hellen-v3-scratch");TMP.mkdir(exist_ok=True,parents=True)
EXP=ROOT.parent;W,H=1920,1080;FPS=30;INTRO=3.04;OUTRO=6.04
ORANGE="#FF6418";INK="#191918";MUTED="#706C67";CREAM="#FFF9F3";BLUE="#007AFF"
@functools.lru_cache(None)
def font(n,b=False):return ImageFont.truetype("/usr/share/fonts/truetype/lato/Lato-"+("Bold" if b else "Regular")+".ttf",n)
def tx(d,xy,s,n=26,fill=INK,b=False,width=999,spacing=8):
    y=xy[1];f=font(n,b)
    for para in s.split("\n"):
        line=""
        for word in para.split():
            test=(line+" "+word).strip()
            if d.textlength(test,font=f)>width and line:d.text((xy[0],y),line,font=f,fill=fill);y+=n+spacing;line=word
            else:line=test
        d.text((xy[0],y),line,font=f,fill=fill);y+=n+spacing
    return y
def ease(x):x=max(0,min(1,x));return 1-(1-x)**3
def check(d,x,y,p,color=ORANGE,size=26):
    d.rounded_rectangle((x,y,x+size,y+size),6,outline=color,width=2)
    pts=[(x+6,y+size*.51),(x+size*.43,y+size*.75),(x+size*.84,y+size*.26)];q=max(0,min(1,p))*2
    if q>0:d.line([pts[0],tuple(pts[0][k]+(pts[1][k]-pts[0][k])*min(1,q) for k in (0,1))],fill=color,width=3)
    if q>1:d.line([pts[1],tuple(pts[1][k]+(pts[2][k]-pts[1][k])*(q-1) for k in (0,1))],fill=color,width=3)
def toggle(d,x,y,on,anim=1):
    d.rounded_rectangle((x,y,x+64,y+36),18,fill="#34C759" if on else "#D9D9DE")
    offset=28*(ease(anim) if on else 1-ease(anim))
    d.ellipse((x+3+offset,y+3,x+33+offset,y+33),fill="white")
def tap(im,x,y,elapsed):
    if not 0<elapsed<.85:return
    layer=Image.new("RGBA",im.size);d=ImageDraw.Draw(layer);p=elapsed/.85;r=14+25*p
    d.ellipse((x-r,y-r,x+r,y+r),fill=(255,100,24,int(36*(1-p))),outline=(255,100,24,int(210*(1-p))),width=3)
    d.ellipse((x-7,y-7,x+7,y+7),fill=(255,100,24,int(200*(1-p))));im.paste(layer,(0,0),layer)
def probe(p):return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(p)],text=True))
def run(cmd):subprocess.run(cmd,check=True)
script=json.loads((OUT/"script.json").read_text())
if (OUT/"chapters.json").exists():
    chapters=json.loads((OUT/"chapters.json").read_text());words=json.loads((OUT/"word-alignment.json").read_text())["words"]
    DUR=float(probe(OUT/"hellen-narration.wav")["format"]["duration"])
else:
    chapters=[{**c,"start":i*15,"end":(i+1)*15} for i,c in enumerate(script["chapters"])];words=[];DUR=195
TOTAL=INTRO+DUR+OUTRO
gif=Image.open(EXP/"motion-plus/sources/readme-original.gif");logo=[]
for f in ImageSequence.Iterator(gif):logo.append(f.convert("RGBA").resize((240,240),Image.Resampling.LANCZOS))
brand=Image.open(EXP/"graphics/transparent/wordmark/openline-wordmark-black-512.png").convert("RGBA");brand.thumbnail((250,80),Image.Resampling.LANCZOS)
qr=qrcode.make("https://openline.com/install").convert("RGB").resize((264,264),Image.Resampling.NEAREST)
def logo_at(im,x,y,t,size=240):
    f=logo[min(int(max(0,t)*50),len(logo)-1)]
    if size!=240:f=f.resize((size,size),Image.Resampling.LANCZOS)
    im.paste(f,(x,y),f)
def phone_screen(kind,elapsed=5):
    """440x760 labeled generic phone UI illustration, not OS footage."""
    im=Image.new("RGB",(440,760),"#F2F2F7");d=ImageDraw.Draw(im);d.rectangle((0,0,440,118),fill="#FBFBFD")
    tx(d,(28,16),"9:41",19,b=True)
    for i in range(4):d.rounded_rectangle((347+i*7,29-i*3,351+i*7,36),1,fill=INK)
    d.rounded_rectangle((390,23,419,36),3,outline=INK,width=2);d.rectangle((394,26,413,33),fill=INK)
    if kind in ("samsung","pixel"):d.ellipse((211,17,229,35),fill="#101010")
    else:d.rounded_rectangle((166,13,274,36),13,fill="#101010")
    tx(d,(20,70),"‹ Back",22,BLUE)
    titles={"settings":"Settings","cellular":"Cellular","add":"Add eSIM","scan":"Scan QR Code","fields":"Enter Details","confirm":"Add eSIM","travel":"Travel eSIM","type":"Plan type","label":"Cellular Plan Label","calls":"Default Voice Line","imessage":"iMessage & FaceTime","data":"Cellular Data","lineon":"Openline","openline":"Openline","home":"Primary","homeoff":"Primary","wifi":"Wi-Fi","browser":"Browser","samsung":"SIM manager","pixel":"SIMs","support":"Need a hand?","welcome":"Your travel eSIM"}
    if kind=="cellular_new":title="Cellular"
    elif kind=="data_select":title="Cellular Data"
    else:title=titles.get(kind,kind)
    tx(d,(25,133),title,31,b=True,width=395)
    def row(y,label,value="",selected=False,arrow=True):
        d.rounded_rectangle((18,y,422,y+63),12,fill="white");tx(d,(35,y+19),label,23,width=306)
        if value:tx(d,(302,y+21),value,19,MUTED)
        if selected:tx(d,(380,y+18),"✓",27,BLUE,True)
        elif arrow:tx(d,(394,y+15),"›",28,"#A5A5AD")
    def button(y,label="Continue"):
        d.rounded_rectangle((28,y,412,y+59),15,fill=BLUE);f=font(24,True);d.text(((440-d.textlength(label,font=f))/2,y+15),label,font=f,fill="white")
    if kind=="welcome":
        logo_at(im,100,220,elapsed);tx(d,(71,480),"One eSIM. Your trip.",29,b=True,width=320);tx(d,(62,540),"Install • Configure • Connect",22,MUTED)
    elif kind=="settings":
        row(212,"Wi-Fi","On");row(288,"Bluetooth","On");row(364,"Cellular");row(440,"Notifications");row(516,"General")
    elif kind in ("cellular","cellular_new"):
        row(212,"Cellular Data","Primary");row(288,"Default Voice Line","Primary");tx(d,(30,383),"SIMs",19,MUTED)
        row(418,"Primary","On")
        if kind=="cellular_new":row(494,"New eSIM","Off");row(582,"Add eSIM")
        else:row(494,"Add eSIM")
    elif kind=="add":
        tx(d,(30,207),"Set up your mobile service.",24,MUTED,width=370);row(304,"Transfer from nearby phone");row(386,"Use QR Code")
        tx(d,(30,503),"Choose the QR option if shown.",21,MUTED,width=370)
    elif kind=="scan":
        tx(d,(42,204),"Position your supplied QR code",22,width=360);tx(d,(72,236),"inside the frame.",22,MUTED)
        d.rounded_rectangle((77,292,363,559),20,fill="#E6E4DF",outline="#B8B4AE",width=2)
        for xx,yy in [(102,317),(286,317),(102,485)]:
            d.rectangle((xx,yy,xx+52,yy+52),outline="#4E4A44",width=8);d.rectangle((xx+19,yy+19,xx+33,yy+33),fill="#4E4A44")
        tx(d,(119,414),"DEMO ONLY",24,INK,True);y=303+int((elapsed%2)/2*240);d.line((84,y,355,y),fill=ORANGE,width=3)
        tx(d,(89,641),"Enter Details Manually",23,BLUE)
    elif kind=="fields":
        tx(d,(30,193),"Use your own Openline details.",21,MUTED,width=375)
        for i,(label,value) in enumerate([("SM-DP+ Address","example.invalid"),("Activation Code","EXAMPLE-NOT-VALID"),("Confirmation Code","Only if provided")]):
            y=260+i*115;tx(d,(29,y),label,18,MUTED);d.rounded_rectangle((25,y+32,415,y+90),10,fill="white",outline="#D8D8DF",width=1)
            if i<2:
                n=int(max(0,min(1,(elapsed-i*2.2)/1.6))*len(value));val=value[:n];tx(d,(39,y+49),val,22,INK,True)
                if 0<n<len(value):d.line((40+d.textlength(val,font=font(22,True)),y+47,40+d.textlength(val,font=font(22,True)),y+74),fill=BLUE,width=2)
            else:tx(d,(39,y+50),value,20,"#9A9793")
        tx(d,(34,615),"NONFUNCTIONAL EXAMPLES",17,ORANGE,True);button(660,"Next")
    elif kind=="confirm":
        tx(d,(37,242),"Follow the setup prompts",29,b=True,width=360);tx(d,(37,334),"Your device may ask you to confirm adding this eSIM.",24,MUTED,width=365)
        tx(d,(37,464),"Wait for setup to finish.",24,width=365);button(642)
    elif kind=="travel":
        tx(d,(30,223),"Where will you use this eSIM?",28,b=True,width=370);row(348,"Home");row(430,"Abroad",selected=True,arrow=False)
        tx(d,(30,543),"If this travel question appears.",21,MUTED,width=360);button(651)
    elif kind=="type":
        tx(d,(30,223),"Which type of plan do you have?",28,b=True,width=370);row(351,"Data Only",selected=True,arrow=False);row(433,"Voice and Data")
        tx(d,(30,545),"Match the plan you purchased.",21,MUTED,width=370);button(651)
    elif kind=="label":
        row(216,"Business");row(292,"Personal");row(368,"Travel");tx(d,(31,473),"CUSTOM LABEL",18,MUTED)
        d.rounded_rectangle((20,514,420,583),12,fill="white");tx(d,(38,536),"Openline"[:min(8,int(elapsed*4))],25,b=True);button(651,"Done")
    elif kind in ("calls","imessage"):
        tx(d,(30,218),"Keep your home number selected.",24,MUTED,width=365);row(332,"Primary",selected=True,arrow=False);row(412,"Openline",arrow=False)
        tx(d,(30,528),"Calls and texts may incur home-provider charges.",22,MUTED,width=375)
    elif kind in ("data","data_select"):
        row(224,"Primary",arrow=False);row(304,"Openline",selected=True,arrow=False)
        tx(d,(30,428),"Allow Cellular Data",23);tx(d,(30,459),"Switching",23);toggle(d,338,445,kind=="data_select",1 if kind=="data_select" else elapsed)
        tx(d,(30,550),"Select Openline for mobile data." if kind=="data_select" else "Keep automatic data switching off.",22,MUTED,width=365)
    elif kind in ("lineon","openline","home","homeoff"):
        row(221,"Cellular Plan Label","Openline" if kind in ("lineon","openline") else "Primary")
        row(302,"Turn On This Line",arrow=False);toggle(d,338,317,kind!="homeoff",elapsed)
        row(402,"Network Selection","Auto");row(503,"Data Roaming",arrow=False);toggle(d,338,518,kind=="openline",elapsed)
        tx(d,(29,614),"Follow your plan's roaming instructions." if kind in ("lineon","openline") else "Home data roaming off.\nCalls/texts may still cost extra.",21,MUTED,width=377)
    elif kind=="wifi":
        row(227,"Wi-Fi",arrow=False);toggle(d,338,242,False,elapsed);tx(d,(30,354),"Temporarily off for your test.",24,MUTED,width=370)
    elif kind=="browser":
        d.rounded_rectangle((23,213,417,269),15,fill="white",outline="#DADAE0");tx(d,(54,230),"Open a webpage",22,MUTED)
        d.rounded_rectangle((23,294,417,620),18,fill="white");p=ease(elapsed/1.6);d.rectangle((29,289,29+int(382*p),292),fill=BLUE)
        if p>.98:check(d,193,341,1,size=46);tx(d,(82,423),"Page loaded",32,b=True);tx(d,(59,485),"This checks internet access.",23,MUTED,width=330)
        else:tx(d,(122,416),"Loading…",29,MUTED)
    elif kind=="samsung":
        tx(d,(28,202),"Samsung example",20,MUTED);row(260,"Primary");row(340,"Openline");row(435,"Add eSIM");row(529,"Mobile data","Openline")
    elif kind=="pixel":
        tx(d,(28,202),"Pixel example",20,MUTED);row(260,"Primary");row(340,"Openline");row(435,"Add SIM")
        tx(d,(29,548),"Scan QR, or use the manual code option.",23,MUTED,width=370)
    elif kind=="support":
        logo_at(im,145,220,3.04,size=150);tx(d,(38,413),"Contact Openline support",30,b=True,width=355);tx(d,(38,513),"Before deleting your eSIM.",25,MUTED,width=355)
    d.rounded_rectangle((160,739,280,745),3,fill=INK)
    return im
def anchor(c,phrase,default):
    if not words:return c["start"]+(c["end"]-c["start"])*default
    norm=lambda s:re.sub(r"[^a-z0-9]","",s.lower())
    subset=words[c["word_start"]:c["word_end"]];needle=[norm(s) for s in phrase.split()]
    for i in range(len(subset)-len(needle)+1):
        if [norm(w["word"]) for w in subset[i:i+len(needle)]]==needle:return subset[i]["start"]
    return c["start"]+(c["end"]-c["start"])*default
def states(c):
    m={
      "welcome":[("",0,"welcome")],"prepare":[("",0,"settings")],"choose":[("",0,"add")],
      "qr":[("",0,"scan"),("open Settings",.22,"settings"),("Cellular or Mobile Data",.35,"cellular"),("Tap Add eSIM",.48,"add"),("Scan your code",.65,"scan"),("confirm the onscreen",.8,"confirm")],
      "manual":[("",0,"scan"),("Paste your",.28,"fields"),("Tap Next",.76,"confirm")],
      "installed":[("",0,"travel"),("Data Only",.55,"type")],
      "labels":[("",0,"cellular_new"),("Cellular Plan Label",.48,"label")],
      "calls":[("",0,"calls"),("iMessage and FaceTime",.42,"imessage")],
      "data":[("",0,"lineon"),("Select it",.53,"data_select"),("Turn Allow",.77,"data")],
      "roaming":[("",0,"openline"),("Keep home Data",.27,"home"),("turn the home line off",.72,"homeoff")],
      "test":[("",0,"wifi"),("open a webpage",.22,"browser"),("Contact Openline support",.77,"support")],
      "android":[("",0,"samsung"),("On Pixel",.48,"pixel")],"outro":[("",0,"welcome")]}
    return [(anchor(c,p,f) if p else c["start"],k) for p,f,k in m[c["id"]]]
SIDEBARS={
 "welcome":("Your eSIM,\nstep by step.",["Install your plan","Choose your settings","Test your connection"]),
 "prepare":("A little prep.\nA smoother setup.",["Compatible + unlocked","Trusted, stable Wi-Fi","Your Openline details"]),
 "choose":("One installation.\nTwo alternatives.",["Option A — QR code","OR","Option B — manual entry"]),
 "qr":("A / QR installation",["Show QR on another screen","Open your mobile settings","Scan, confirm, then wait"]),
 "manual":("B / Manual installation",["Use your own supplied details","Copy and paste exactly","Confirmation code: if supplied"]),
 "installed":("Your phone may\nask different questions.",["iOS 26 travel prompts may appear","Abroad for international travel","Data Only: if your plan matches"]),
 "labels":("Make it easy\nto recognize.",["Open your new line","Cellular Plan Label","Name it Openline"]),
 "calls":("Keep your number.\nKnow your charges.",["Primary for calls + texts","Primary for iMessage + FaceTime","Existing chats may keep their line"]),
 "data":("The right line.\nFor your data.",["Follow your plan's timing","Openline line ON","Data switching OFF"]),
 "roaming":("Roaming is\na per-line setting.",["Openline: follow plan instructions","Home data roaming OFF","Optional: switch home line OFF"]),
 "test":("Don't just check\nsignal bars.",["Wi-Fi OFF briefly","Open a webpage","If stuck: support before deletion"]),
 "android":("Same essentials.\nDifferent menus.",["Samsung: Connections → SIM manager","Pixel: Network & internet → SIMs","QR OR manual • Openline for data"]),
 "outro":("Ready for your\nnext chapter.",["One installation method","The right data line","A real connection test"])}
def panel(c,t):
    im=Image.new("RGB",(1080,940),CREAM);d=ImageDraw.Draw(im);elapsed=t-c["start"]
    idx=next(i for i,v in enumerate(chapters) if v["id"]==c["id"])
    tx(d,(28,16),"INSTALLATION GUIDE",19,ORANGE,True);tx(d,(28,53),c["title"],39,b=True,width=1010)
    tx(d,(28,108),"Illustrated guide • screens vary by device",18,MUTED)
    title,lines=SIDEBARS[c["id"]];tx(d,(28,196),title,38,b=True,width=480,spacing=9);y=365
    for i,s in enumerate(lines):
        if s=="OR":tx(d,(74,y),s,19,ORANGE,True);y+=58;continue
        check(d,29,y+6,ease((elapsed-.5-i*.55)/.65));y=tx(d,(74,y),s,25,MUTED,width=420,spacing=7)+27
    if c["id"]=="manual":
        d.rounded_rectangle((28,650,492,818),18,fill="#FFFFFF",outline="#E5D9CF")
        tx(d,(48,670),"EXAMPLE DETAILS",17,ORANGE,True);tx(d,(48,711),"example.invalid",23,b=True);tx(d,(48,751),"EXAMPLE-NOT-VALID",22,b=True)
        tx(d,(28,852),"Never use these placeholder values.",20,MUTED)
    elif c["id"]=="prepare":tx(d,(28,733),"Purchase code ≠ activation code",23,ORANGE,True,width=445)
    elif c["id"]=="calls":tx(d,(28,739),"Home-provider calls and texts\nmay still incur charges.",23,ORANGE,True,width=450)
    elif c["id"]=="data":tx(d,(28,738),"Activation + validity:\nfollow YOUR plan's instructions.",23,ORANGE,True,width=440)
    elif c["id"]=="roaming":tx(d,(28,739),"Switching a line off\nis not deleting the eSIM.",23,ORANGE,True,width=450)
    elif c["id"]=="android":tx(d,(28,753),"Illustrative manufacturer examples.\nExact options vary by model.",21,MUTED,width=440)
    elif c["id"] in ("choose","qr"):tx(d,(28,753),"Choose QR OR manual.\nDo not install twice.",24,ORANGE,True,width=430)
    seq=states(c);active=max(i for i,(a,k) in enumerate(seq) if a<=t);start,kind=seq[active];age=t-start
    screen=phone_screen(kind,age)
    if active and age<.42:
        old=phone_screen(seq[active-1][1],9);mix=Image.new("RGB",(440,760),"#F2F2F7");x=int(440*(1-ease(age/.42)))
        mix.paste(old,(x-440,0));mix.paste(screen,(x,0));screen=mix
    recap_sets={"qr":["QR route selected","Setup prompts followed","Only one installation"],
        "manual":["Your own details used","Setup prompts followed","Only one installation"],
        "calls":["Primary calls + messages","Check existing chats","Home fees may apply"],
        "roaming":["Openline: plan rules","Home data roaming off","Off is not deleted"],
        "test":["Wi-Fi off briefly","Webpage test","Support before deletion"]}
    recap_age=t-(c["end"]-2)
    if c["id"] in recap_sets and recap_age>0:
        card=Image.new("RGB",(440,760),"#FFF9F3");cd=ImageDraw.Draw(card)
        logo_at(card,160,66,3.04,size=120);tx(cd,(40,243),"Quick check",35,b=True)
        for i,label in enumerate(recap_sets[c["id"]]):
            check(cd,41,344+i*94,ease((recap_age-.2-i*.35)/.5),size=30)
            tx(cd,(88,342+i*94),label,24,MUTED,width=313)
        y=int(760*(1-ease(recap_age/.32)));screen.paste(card,(0,y))
    d.rounded_rectangle((558,157,1036,936),52,fill="#E9E0D8");d.rounded_rectangle((546,143,1026,925),50,fill="#3C3C3E",outline="#AAA7A3",width=2)
    d.rounded_rectangle((552,149,1020,919),47,fill="#121213")
    mask=Image.new("L",(440,760));ImageDraw.Draw(mask).rounded_rectangle((0,0,439,759),38,fill=255);im.paste(screen,(566,160),mask)
    targets={"settings":(805,555),"cellular":(806,774),"add":(808,577),"scan":(797,811),"fields":(792,850),"confirm":(795,839),"travel":(815,619),"type":(803,538),"label":(804,721),"calls":(807,520),"imessage":(807,520),"data":(945,622),"openline":(939,697),"home":(938,697),"homeoff":(939,496),"wifi":(940,420),"samsung":(809,627),"pixel":(809,627)}
    if kind=="lineon":targets[kind]=(939,496)
    if kind in ("cellular","cellular_new"):targets[kind]=(806,683)
    if kind=="data_select":targets[kind]=(945,495)
    if kind in targets and not (kind=="scan" and c["id"]!="manual"):tap(im,*targets[kind],age-.55)
    if kind=="fields":
        p=(age%2.2)/2.2
        if p<.65 and age<4.4:
            x=430+int(170*ease(p/.65));y=730-int(250*ease(p/.65))
            d.rounded_rectangle((x,y,x+94,y+35),9,fill="#FFE1CD");tx(d,(x+10,y+7),"Copied",17,ORANGE,True)
    d.rounded_rectangle((28,914,492,918),2,fill="#E8DED3");d.rounded_rectangle((28,914,28+int(464*(idx+1)/len(chapters)),918),2,fill=ORANGE)
    return im
def badge(im,t):
    layer=Image.new("RGBA",im.size);d=ImageDraw.Draw(layer);opacity=255 if t<2 else 178
    if t<1.2:tx(d,(1634,31),"Generated by",22,(70,66,60,255))
    d.rounded_rectangle((1790,20,1878,69),16,fill=(255,255,255,opacity),outline=(225,216,207,opacity),width=1)
    tx(d,(1816,28),"AI",27,(25,25,24,opacity),True);im.paste(layer,(0,0),layer)
def frame(t):
    im=Image.new("RGB",(W,H),CREAM);d=ImageDraw.Draw(im)
    if t<INTRO or t>=INTRO+DUR:
        outro=t>=INTRO+DUR;age=t-INTRO-DUR if outro else t;d.rectangle((0,0,W,H),fill="white")
        logo_at(im,400,290,age);im.paste(brand,(700,350),brand)
        tx(d,(698,444),"Ready for your next chapter." if outro else "Let's get you connected.",49,b=True,width=1000)
        tx(d,(702,520),"Your Openline eSIM, step by step.",27,MUTED)
        if outro:
            im.paste(qr,(705,620));tx(d,(1012,686),"openline.com/install",39,b=True);tx(d,(1015,754),"Scan to open the installation guide.",24,MUTED,width=650)
        else:tx(d,(702,635),"WITH HELLEN",20,ORANGE,True)
    else:
        n=t-INTRO;c=max((c for c in chapters if c["start"]<=n),key=lambda c:c["start"],default=chapters[0])
        d.rounded_rectangle((40,78,760,971),28,fill="#262522");im.paste(panel(c,n),(800,78))
        wordmark=brand.resize((170,int(brand.height*170/brand.width)));im.paste(wordmark,(57,24),wordmark);tx(d,(263,29),"A little guidance. A world of possibility.",22,MUTED)
        tx(d,(59,931),"Hellen",24,"white",True);tx(d,(145,935),"for Openline",20,"#EEE9E4")
    badge(im,t);return im
def ts(t,sep=","):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f"{h:02}:{m:02}:{s:02}{sep}{ms:03}"
def ass_ts(t):
    cs=round(t*100);h,cs=divmod(cs,360000);m,cs=divmod(cs,6000);s,cs=divmod(cs,100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"
def captions():
    cues=[]
    for c in chapters:
        subset=words[c["word_start"]:c["word_end"]];i=0
        while i<len(subset):
            remain=len(subset)-i;n=min(5,remain)
            if remain in (6,7,8):n=remain if remain==6 else 4
            for k in range(3,n+1):
                if re.search("[.!?;]$",subset[i+k-1]["word"]):n=k;break
            if 0<remain-n<3:n=remain-3
            batch=subset[i:i+n];end=batch[-1]["end"]+.08
            if i+n<len(subset):end=min(end,subset[i+n]["start"])
            cues.append({"start":batch[0]["start"]+INTRO,"end":end+INTRO,"text":" ".join(w["word"] for w in batch),"words":batch});i+=n
    (OUT/"hellen-tutorial-en.srt").write_text("\n\n".join(f"{i}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}" for i,c in enumerate(cues,1))+"\n")
    (OUT/"hellen-tutorial-en.vtt").write_text("WEBVTT\n\n"+"\n\n".join(f"{ts(c['start'],'.')} --> {ts(c['end'],'.')}\n{c['text']}" for c in cues)+"\n")
    header="""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Lato,46,&H00FFFFFF,&H00FFFFFF,&H00232323,&H80000000,-1,0,0,0,100,100,0,0,1,2.2,1.2,2,70,70,29,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events=[]
    for c in cues:
        for i,w in enumerate(c["words"]):
            start=w["start"]+INTRO;end=(c["words"][i+1]["start"]+INTRO if i+1<len(c["words"]) else c["end"])
            s=" ".join(("{\\c&H00D8EEFF&\\fscx104\\fscy104}"+v["word"]+"{\\c&H00FFFFFF&\\fscx100\\fscy100}") if j==i else v["word"] for j,v in enumerate(c["words"]))
            events.append(f"Dialogue: 0,{ass_ts(start)},{ass_ts(max(start+.03,end))},Default,,0,0,0,,{s}")
    (OUT/"hellen-tutorial-en.ass").write_text(header+"\n".join(events)+"\n")
    (OUT/"caption-cues.json").write_text(json.dumps(cues,indent=2))
def sting():
    rate=48000;length=3.04;t=np.arange(int(rate*length))/rate;audio=np.zeros_like(t)
    for i,hz in enumerate([523.25,659.25,783.99]):
        local=t-i*.18;env=np.where(local>=0,np.exp(-np.maximum(0,local)*3.8)*(1-np.exp(-np.maximum(0,local)*70)),0)
        audio+=.13*env*(np.sin(2*np.pi*hz*local)+.18*np.sin(4*np.pi*hz*local))
    audio*=np.minimum(1,(length-t)/.3)
    with wave.open(str(OUT/"openline-pleasant-sting.wav"),"w") as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes((audio*32767).astype("<i2").tobytes())
def render():
    captions();sting()
    cmd=["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r",str(FPS),"-i","-","-an","-c:v","libx264","-threads","1","-preset","fast","-crf","20","-pix_fmt","yuv420p",str(TMP/"animated-layout.mp4")]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(math.ceil(TOTAL*FPS)):
        proc.stdin.write(frame(i/FPS).tobytes())
        if i%(FPS*20)==0:print("layout",i/FPS,"/",TOTAL,flush=True)
    proc.stdin.close();assert proc.wait()==0
def compose():
    raw=TMP/"hellen-continuous-raw.mp4"
    patchargs=[];patchfilter="";layout="[0:v]"
    count=4
    for key in ("qr","labels","data","android"):
        c=next(c for c in chapters if c["id"]==key)
        if (TMP/f"{key}-layout-detail.mp4").exists():
            patchargs+=["-itsoffset",str(INTRO+c["start"]),"-threads","1","-i",str(TMP/f"{key}-layout-detail.mp4")]
            patchfilter+=f"{layout}[{count}:v]overlay=0:0:eof_action=pass:enable='between(t,{INTRO+c['start']},{INTRO+c['end']})'[patch{count}];"
            layout=f"[patch{count}]";count+=1
    fc=(patchfilter+"[1:v]scale=720:842:force_original_aspect_ratio=increase,crop=720:842,setsar=1[avatar];"
        f"{layout}[avatar]overlay=40:78:eof_action=pass:enable='between(t,{INTRO},{INTRO+DUR})'[base];"
        f"[base]subtitles='{OUT/'hellen-tutorial-en.ass'}'[v];"
        f"[2:a]loudnorm=I=-16:TP=-1.5:LRA=8,adelay={round(INTRO*1000)}|{round(INTRO*1000)},apad[voice];"
        "[3:a]volume=0.55,asplit=2[s1][s2];"
        f"[s2]adelay={round((INTRO+DUR)*1000)}|{round((INTRO+DUR)*1000)}[end];"
        "[voice][s1][end]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.89:level=0[a]")
    run(["ffmpeg","-v","error","-y","-threads","1","-i",str(TMP/"animated-layout.mp4"),"-itsoffset",str(INTRO),"-threads","1","-i",str(raw),"-i",str(OUT/"hellen-narration.wav"),"-i",str(OUT/"openline-pleasant-sting.wav")]+patchargs+[
         "-filter_complex_threads","1","-filter_complex",fc,"-map","[v]","-map","[a]","-t",str(TOTAL),"-r","30","-c:v","libx264","-threads","1","-preset","fast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-ar","48000","-movflags","+faststart",str(OUT/"openline-hellen-installation-tutorial.mp4")])
    run(["ffmpeg","-v","error","-y","-ss",str(INTRO+2),"-i",str(OUT/"openline-hellen-installation-tutorial.mp4"),"-frames:v","1",str(OUT/"openline-hellen-tutorial-poster.jpg")])
    run(["ffmpeg","-v","error","-y","-i",str(OUT/"openline-hellen-installation-tutorial.mp4"),"-vf","scale=640:360","-r","12","-c:v","libx264","-threads","1","-preset","fast","-crf","29","-c:a","aac","-b:a","96k",str(TMP/"review.mp4")])
def qa():
    import cv2
    video=OUT/"openline-hellen-installation-tutorial.mp4";run(["ffmpeg","-v","error","-threads","1","-i",str(video),"-f","null","-"])
    fractions={"qr":.68,"manual":.5,"labels":.7,"data":.8,"test":.45,"android":.65}
    cap=cv2.VideoCapture(str(video));shots=[];disclosure_frames=[];times=[.6,1.5,2.2]+[INTRO+c["start"]+(c["end"]-c["start"])*fractions.get(c["id"],.5) for c in chapters]+[TOTAL-2.5,TOTAL-.2];decoded=[]
    for i,t in enumerate(times):
        cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=cap.read();assert ok
        if i<3:disclosure_frames.append(f.copy())
        rgb=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB));rgb.save(P/f"decoded-{i:02}.jpg",quality=88)
        if t>TOTAL-3:
            value,_,_=cv2.QRCodeDetector().detectAndDecode(f);assert value=="https://openline.com/install",value;decoded.append({"time":t,"value":value})
        shots.append(rgb.resize((640,360)))
    sheet=Image.new("RGB",(1920,360*math.ceil(len(shots)/3)),"white")
    for i,im in enumerate(shots):sheet.paste(im,((i%3)*640,(i//3)*360))
    sheet.save(P/"decoded-contact-sheet.jpg",quality=88)
    before=disclosure_frames[0][30:60,1634:1775];after=disclosure_frames[1][30:60,1634:1775]
    ai_full=disclosure_frames[0][28:61,1814:1859];ai_fade=disclosure_frames[2][28:61,1814:1859]
    assert before.min()<110 and after.min()>235
    opacity=(255-float(np.percentile(ai_fade,2)))/(255-float(np.percentile(ai_full,2)))
    assert .6<opacity<.8,opacity
    stats={"full_decode":True,"output":probe(video),"avatar":probe(TMP/"hellen-continuous-raw.mp4"),"qr_decodes":decoded,"disclosure_frames_seconds":[.6,1.5,2.2],"decoded_AI_opacity_estimate":opacity,"generated_by_visible_then_removed":True,"intro_seconds":INTRO,"outro_animation_seconds":3.04,"outro_hold_seconds":3,"caption_word_count":len(words),"narration_word_count":len(script["narration"].split()),"one_continuous_presenter":True,"speech_offset_seconds":INTRO}
    (P/"technical-qa.json").write_text(json.dumps(stats,indent=2));print("Full decode and end QR pass",TOTAL)
p=argparse.ArgumentParser();p.add_argument("op");args=p.parse_args()
if args.op=="preview":
    c=next(c for c in chapters if c["id"]=="manual");im=frame(INTRO+c["start"]+(c["end"]-c["start"])*.5)
    portrait=Image.open(EXP/"hellen-full-tutorial/deliverables/hellen-office-portrait.jpg").convert("RGB")
    from PIL import ImageOps
    im.paste(ImageOps.fit(portrait,(720,842)),(40,78));im.save(P/"mockup-preview-manual.jpg",quality=95);print(P/"mockup-preview-manual.jpg")
elif args.op=="render":render()
elif args.op=="android-detail":
    c=next(c for c in chapters if c["id"]=="android")
    cmd=["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r",str(FPS),"-i","-","-an","-c:v","libx264","-threads","1","-preset","fast","-crf","20","-pix_fmt","yuv420p",str(TMP/"android-layout-detail.mp4")]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(math.ceil((c["end"]-c["start"])*FPS)):proc.stdin.write(frame(INTRO+c["start"]+i/FPS).tobytes())
    proc.stdin.close();assert proc.wait()==0
elif args.op=="ui-details":
    for key in ("qr","labels","data"):
        c=next(c for c in chapters if c["id"]==key)
        cmd=["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r",str(FPS),"-i","-","-an","-c:v","libx264","-threads","1","-preset","fast","-crf","20","-pix_fmt","yuv420p",str(TMP/f"{key}-layout-detail.mp4")]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        for i in range(math.ceil((c["end"]-c["start"])*FPS)):proc.stdin.write(frame(INTRO+c["start"]+i/FPS).tobytes())
        proc.stdin.close();assert proc.wait()==0;print("UI detail",key,flush=True)
elif args.op=="compose":compose()
elif args.op=="qa":qa()
