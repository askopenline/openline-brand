// Proposed review UI only. Original V3 artwork and native app sources are untouched.
import fs from 'node:fs';
import {chromium} from 'playwright';
const rec=JSON.parse(fs.readFileSync('public/app-v3/recommended-copy.json'));
const original=JSON.parse(fs.readFileSync('public/app-v3/copy.json'));
const root='public/app-v3/recommended',base='http://127.0.0.1:5173/';
const captures=['countries','dashboard','destination','duration','esims','profile','profile','settings','account','collection','types','notifications',...original.frames.slice(12).map(f=>f.capture)];
const esc=s=>String(s??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
const browser=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'});
fs.mkdirSync(root+'/screens',{recursive:true});
const provenance=[],layout=[];
try{
 for(const id of ['04','19','18']){
  const f=rec.frames[id],p=f.phone,page=await browser.newPage({viewport:{width:340,height:700},deviceScaleFactor:4});
  let content='';
  if(id==='04'){
   const days=['',...Array.from({length:30},(_,i)=>i+1)]; // June 2027 starts Tuesday.
   content=`<img class="original" src="${base}app-v3/screens/duration.png"><section class="calendar"><div class="cal-label">${esc(p.calendarLabel)}</div><div class="month"><span>‹</span>June 2027<span>›</span></div><div class="week">${['M','T','W','T','F','S','S'].map(x=>`<b>${x}</b>`).join('')}</div><div class="days">${days.map(n=>`<span class="${n?'range':''} ${n===1||n===30?'edge':''}">${n}</span>`).join('')}</div><div class="cal-action"><span>30 days selected</span><strong>${esc(p.calendarAction)}</strong></div></section>`;
  }else if(id==='19'){
   content=`<div class="status"><span>9:41</span><span>▂▄▆ ▰</span></div><main><h1>${esc(p.title)}</h1><p>${esc(p.subtitle)}</p><div class="step-label">SETUP GUIDE</div><section class="checklist">${p.rows.map((r,i)=>`<article><span class="check">✓</span><div><strong>${esc(r.title)}</strong><small>${esc(r.detail)}</small></div></article>`).join('')}</section><aside>${esc(p.note)}</aside></main>`;
  }else{
   content=`<div class="status"><span>9:41</span><span>▂▄▆ ▰</span></div><main><h1>${esc(p.title)}</h1><p>${esc(p.subtitle)}</p><section class="chat-card"><div class="chat-icon"><svg width="39" height="39" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5H5l-3 2V11.5A8.5 8.5 0 0 1 10.5 3h2a8.5 8.5 0 0 1 8.5 8.5Z"/><path d="M7 10h10M7 14h7"/></svg></div><span class="badge">${esc(p.badge)}</span><h2>${esc(p.chatTitle)}</h2><p>${esc(p.chatDetail)}</p><div class="chat-cta">${esc(p.chatAction)} <b>↗</b></div><small>openline.com/contact</small></section><section class="help-card"><span>?</span><div><strong>${esc(p.helpTitle)}</strong><p>${esc(p.helpDetail)}</p></div></section></main>`;
  }
  await page.setContent(`<!doctype html><html><head><style>
  @font-face{font-family:Inter;src:url('${base}fonts/inter-latin-600-normal.woff2');font-weight:600}@font-face{font-family:Inter;src:url('${base}fonts/inter-latin-800-normal.woff2');font-weight:800}
  *{box-sizing:border-box}body{margin:0;width:340px;height:700px;overflow:hidden;background:#f7f8fa;color:#171717;font-family:Inter,sans-serif;font-weight:600}.original{position:absolute;width:340px;height:700px;inset:0}.status{display:flex;justify-content:space-between;padding:20px 21px 0;font-size:12px}main{padding:23px 20px 20px}h1{font-weight:800;font-size:27px;line-height:1.1;letter-spacing:-.9px;margin:0 0 10px}p{font-size:12px;line-height:1.5;color:#69717b;margin:0 0 17px}
  .calendar{position:absolute;top:325px;left:20px;width:300px;padding:14px 15px 12px;background:white;border:1px solid #e9e9e9;border-radius:19px;box-shadow:0 2px 5px #00000006}.cal-label{font-size:12px;color:#727984;margin-bottom:12px}.month{display:flex;justify-content:space-between;font-size:15px;font-weight:800;margin-bottom:12px}.month span{color:#ff6418}.week,.days{display:grid;grid-template-columns:repeat(7,1fr);text-align:center;gap:3px}.week{font-size:9px;color:#8a929b;margin-bottom:5px}.days{font-size:11px}.days span{height:23px;display:grid;place-items:center;border-radius:5px}.range{background:#fff0e5;color:#a33e0c}.days .edge{background:#ff6418;color:white;font-weight:800}.cal-action{display:flex;justify-content:space-between;align-items:center;border-top:1px solid #eee;margin-top:10px;padding-top:10px;font-size:9px}.cal-action strong{color:#cf4b0b;font-size:10px}
  .step-label{font-size:10px;letter-spacing:1px;color:#89919b;margin:0 0 10px}.checklist article{display:flex;gap:11px;align-items:flex-start;background:white;border:1px solid #e8ebef;border-radius:15px;padding:10px 12px;margin-bottom:7px}.check{background:#fff0e4;color:#ef5910;border-radius:50%;height:25px;width:25px;flex-shrink:0;display:grid;place-items:center;font-size:15px}.checklist strong{font-size:12px;display:block;line-height:1.3}.checklist small{font-size:9.5px;color:#717984;line-height:1.35;display:block;margin-top:4px}.checklist div{flex:1}aside{font-size:10px;line-height:1.45;padding:12px;color:#565e68;background:#edf0f4;border-radius:12px;margin-top:13px}
  .chat-card{padding:21px;background:white;border:1px solid #eceef0;border-radius:23px;box-shadow:0 4px 10px #00000004}.chat-icon{display:grid;place-items:center;background:#fff0e5;color:#ff6418;border-radius:20px;width:65px;height:65px;margin-bottom:17px}.badge{font-size:10px;color:#167354;background:#e9f6ef;border-radius:20px;padding:7px 10px;display:inline-block}h2{font-size:22px;font-weight:800;letter-spacing:-.5px;margin:15px 0 10px}.chat-card p{font-size:12px;margin-bottom:20px}.chat-cta{background:#ff6418;color:white;display:flex;align-items:center;justify-content:space-between;gap:8px;padding:14px 12px;border-radius:12px;font-size:11px}.chat-card small{display:block;text-align:center;font-size:10px;color:#77808a;margin-top:12px}.help-card{margin-top:16px;display:flex;gap:13px;padding:18px;background:#fff;border:1px solid #eceef0;border-radius:19px}.help-card>span{background:#f2f4f7;border-radius:12px;width:35px;height:35px;display:grid;place-items:center;flex-shrink:0;font-size:20px}.help-card strong{font-size:13px}.help-card p{font-size:11px;margin:7px 0 0}
  </style></head><body>${content}</body></html>`);
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(x=>x.decode()))});
  const text=await page.locator('body').innerText();
  const bottom=await page.locator(id==='04'?'.calendar':id==='19'?'aside':'.help-card').evaluate(e=>e.getBoundingClientRect().bottom);
  if(bottom>620)throw Error('Phone content too low '+id+' '+bottom);
  if(/[$€£¥₹₽]|\b(cheapest|switching networks)\b/i.test(text))throw Error('Unexpected claim');
  await page.screenshot({path:root+'/screens/'+f.capture+'.png'});
  provenance.push({id:f.capture,candidate:id,text,contentBottom:bottom,width:1360,height:2800,concept:true,status:'Proposed review UI, not a verified native release capture'});await page.close();
 }
 for(const [platform,width,height]of [['apple',1320,2868],['google',1080,1920]]){
  fs.mkdirSync(root+'/'+platform,{recursive:true});
  for(const [position,id]of rec.selection[platform].entries()){
   const n=Number(id)-1,f={...original.frames[n],...rec.frames[id]},page=await browser.newPage({viewport:{width,height}});
   await page.goto(base+`render-submission.html?platform=${platform}&slide=${position%2}`,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.artworkReady);
   const capture=['04','18','19'].includes(id)?f.capture:captures[n],path=['04','11','18','19'].includes(id)?'recommended/':'';
   await page.evaluate(({f,id,platform,position,capture,path})=>{
    const h=document.querySelector('h1');h.replaceChildren(document.createTextNode(f.head[0]),document.createElement('br'),Object.assign(document.createElement('span'),{textContent:f.head[1]}));h.style.color=position%2?'#171717':'#fff';h.querySelector('span').style.color='inherit';h.style.fontSize=platform==='apple'?'117px':'90px';
    document.querySelector('.copy p').textContent=f.detail;document.querySelector('.copy p').style.fontSize=platform==='apple'?'43px':'33px';
    const img=document.querySelector('.capture img');img.src='./app-v3/'+path+'screens/'+capture+'.png';img.alt=f.alt;
    const special=['04','18','19'].includes(id),cap=document.querySelector('.capture');
    cap.style.top=platform==='google'&&special?'32%':'34%';cap.style.width=platform==='apple'?(special?'75%':'79%'):(special?'66%':'73%');cap.style.left=platform==='apple'?(special?'13%':'11%'):(special?'15.5%':'14%');
   },{f,id,platform,position,capture,path});
   await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(x=>x.decode()))});
   const qa=await page.evaluate(()=>{const rect=s=>{const r=document.querySelector(s).getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width,height:r.height}};return{copy:rect('.copy'),capture:rect('.capture'),brand:rect('.brand'),background:getComputedStyle(document.querySelector('#canvas')).backgroundColor}});
   if(qa.copy.bottom+14>qa.capture.top)throw Error('Copy overlap '+platform+' '+id);
   if(platform==='google'&&(qa.copy.width*qa.copy.height+qa.brand.width*qa.brand.height)/(width*height)>.2)throw Error('Google text footprint '+id);
   await page.screenshot({path:`${root}/${platform}/${id}.png`});layout.push({platform,candidate:id,position:position+1,width,height,...qa});await page.close();
  }
 }
 fs.writeFileSync(root+'/revision-provenance.json',JSON.stringify(provenance,null,2)+'\n');
 fs.writeFileSync(root+'/revision-layout-qa.json',JSON.stringify(layout,null,2)+'\n');
 console.log(JSON.stringify({captures:provenance.length,frames:layout.length}));
}finally{await browser.close()}
