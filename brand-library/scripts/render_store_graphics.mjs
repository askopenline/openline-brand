// Renders the Google Play feature graphic (1024x500) in two variants from approved brand assets and native captures.
import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import {execSync} from 'node:child_process';
const root=path.resolve('public'),out=path.join(root,'app-v3/recommended/google');
const rel=p=>'file://'+path.join(root,p);
const font=w=>`@font-face{font-family:Inter;src:url('${rel('assets/fonts/inter-latin-'+w+'-normal.woff2')}');font-weight:${w}}`;
const logo=n=>rel(`library/graphics/transparent/lockup-horizontal/openline-lockup-horizontal-${n}-2048.png`);
const shots={a:rel('app-v3/recommended/screens/countries.png'),b:rel('app-v3/recommended/screens/dashboard.png')};
const variants={
 orange:{bg:'#ff6418',ink:'#ffffff',accent:'#171717',sub:'#ffffff',logo:'white',blob:'#ff9a5e',card:'0 18px 40px rgba(120,40,0,.35)',file:'feature-graphic.png'},
 light:{bg:'#fff4e8',ink:'#171717',accent:'#ff6418',sub:'#3a3a3a',logo:'black',blob:'#ffdcc0',card:'0 18px 40px rgba(120,60,10,.22)',file:'feature-graphic-light.png'}
};
const html=v=>`<!doctype html><meta charset=utf-8><style>${font(400)}${font(600)}${font(800)}
*{box-sizing:border-box}body{margin:0;width:1024px;height:500px;overflow:hidden;background:${v.bg};font-family:Inter,sans-serif;position:relative}
.blob{position:absolute;right:-120px;bottom:-210px;width:560px;height:560px;border-radius:50%;background:${v.blob}}
.logo{position:absolute;left:64px;top:52px;height:34px}
h1{position:absolute;left:64px;top:128px;margin:0;font-weight:800;font-size:56px;line-height:1.04;letter-spacing:-1.6px;color:${v.ink}}
h1 span{color:${v.accent}}
p{position:absolute;left:64px;top:340px;margin:0;font-size:20px;font-weight:600;color:${v.sub};width:490px;line-height:1.35}
.card{position:absolute;width:236px;height:480px;border-radius:30px;overflow:hidden;background:#f7f8fa;box-shadow:${v.card};border:5px solid #fff}
.card img{width:100%;display:block}
.c1{left:560px;top:48px;transform:rotate(-7deg)}.c2{left:776px;top:112px;transform:rotate(6deg)}
</style><div class=blob></div><img class=logo src="${logo(v.logo)}">
<h1>Travel eSIM data<br>without roaming<br><span>surprises.</span></h1>
<p>Buy, install and track your data in the app.</p>
<div class="card c1"><img src="${shots.a}"></div><div class="card c2"><img src="${shots.b}"></div>`;
const b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'});
for(const [k,v] of Object.entries(variants)){
 const p=await b.newPage({viewport:{width:1024,height:500},deviceScaleFactor:2});
 fs.writeFileSync('/dev/shm/fg-'+k+'.html',html(v));
 await p.goto('file:///dev/shm/fg-'+k+'.html');
 await p.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(x=>x.decode()))});
 await p.screenshot({path:'/dev/shm/fg-'+k+'@2x.png'});await p.close();
 execSync(`python3 -c "from PIL import Image;im=Image.open('/dev/shm/fg-${k}@2x.png').convert('RGB').resize((1024,500),Image.LANCZOS);im.save('${path.join(out,v.file)}',optimize=True)"`);
 console.log('wrote',v.file);
}
await b.close();
