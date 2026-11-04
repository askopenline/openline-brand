// Renders Apple product page header, search results and universal creative assets (orange + light) from approved brand assets.
import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import {execSync} from 'node:child_process';
const root=path.resolve('public'),out=path.join(root,'app-v3/recommended/apple-creative');fs.mkdirSync(out,{recursive:true});
const rel=p=>'file://'+path.join(root,p);
const font=w=>`@font-face{font-family:Inter;src:url('${rel('assets/fonts/inter-latin-'+w+'-normal.woff2')}');font-weight:${w}}`;
const logo=n=>rel(`library/graphics/transparent/lockup-horizontal/openline-lockup-horizontal-${n}-2048.png`);
const shots=[rel('app-v3/recommended/screens/countries.png'),rel('app-v3/recommended/screens/dashboard.png'),rel('app-v3/recommended/screens/types.png')];
const V={orange:{bg:'#ff6418',ink:'#fff',accent:'#171717',sub:'#fff',logo:'white',blob:'#ff9a5e',card:'0 30px 70px rgba(120,40,0,.38)',sfx:''},
 light:{bg:'#fff4e8',ink:'#171717',accent:'#ff6418',sub:'#3a3a3a',logo:'black',blob:'#ffdcc0',card:'0 30px 70px rgba(120,60,10,.24)',sfx:'-light'}};
// Layouts in CSS px at 2x. W,H = viewport. Text block is centred inside Apple's central safe area.
const L={
 header:{W:1920,H:823,file:'header',h1:64,sub:26,logoH:46,gap:22,phones:[[120,300,330,-8],[1470,300,330,8],[1830,380,330,-4]],blob:[1100,-260,900]},
 search:{W:1920,H:1280,file:'search',h1:66,sub:28,logoH:52,gap:26,phones:[[110,640,430,-7],[1380,640,430,7]],blob:[1050,300,1100]},
 universal:{W:2622,H:1475,file:'universal',h1:84,sub:30,logoH:58,gap:28,phones:[[240,470,560,-7],[1820,470,560,7]],blob:[1500,350,1200]}
};
const html=(l,v)=>`<!doctype html><meta charset=utf-8><style>${font(400)}${font(600)}${font(800)}
*{box-sizing:border-box}body{margin:0;width:${l.W}px;height:${l.H}px;overflow:hidden;background:${v.bg};font-family:Inter,sans-serif;position:relative}
.blob{position:absolute;left:${l.blob[0]}px;top:${l.blob[1]}px;width:${l.blob[2]}px;height:${l.blob[2]}px;border-radius:50%;background:${v.blob};opacity:.7}
.c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:${l.gap}px}
.c img{height:${l.logoH}px}h1{margin:0;font-weight:800;font-size:${l.h1}px;line-height:1.05;letter-spacing:${-l.h1*.03}px;color:${v.ink}}h1 span{color:${v.accent}}
p{margin:0;font-weight:600;font-size:${l.sub}px;color:${v.sub}}
.ph{position:absolute;border-radius:${l.W/60}px;overflow:hidden;background:#f7f8fa;border:${l.W/380}px solid #fff;box-shadow:${v.card};aspect-ratio:1360/2800}.ph img{width:100%;display:block}
</style><div class=blob></div>${l.phones.map((p,i)=>`<div class=ph style="left:${p[0]}px;top:${p[1]}px;width:${p[2]}px;transform:rotate(${p[3]}deg)"><img src="${shots[i]}"></div>`).join('')}
<div class=c><img src="${logo(v.logo)}"><h1>Travel eSIM data<br>without roaming <span>surprises.</span></h1><p>Buy, install and track your data in the app.</p></div>`;
const b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'});
for(const [k,l] of Object.entries(L))for(const [vn,v] of Object.entries(V)){
 const p=await b.newPage({viewport:{width:l.W,height:l.H},deviceScaleFactor:2});
 fs.writeFileSync('/dev/shm/ac.html',html(l,v));await p.goto('file:///dev/shm/ac.html');
 await p.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(x=>x.decode()))});
 const raw='/dev/shm/ac-raw.png';await p.screenshot({path:raw});await p.close();
 const o=path.join(out,l.file+v.sfx+'.png');
 execSync(`python3 -c "from PIL import Image;im=Image.open('${raw}').convert('RGB');print(im.size);im.save('${o}',optimize=True)"`);
 if(k==='search')execSync(`python3 -c "from PIL import Image;Image.open('${o}').resize((1920,1280),Image.LANCZOS).save('${path.join(out,'search-1920'+v.sfx+'.png')}',optimize=True)"`);
 console.log('wrote',path.basename(o));
}
await b.close();
