// Deterministic adaptations of supplied design resources. No native capture claim.
import {chromium} from 'playwright';
import fs from 'node:fs';
const recommended=process.env.RECOMMENDED==='1';
if(recommended&&process.env.CAPTURE_ONLY!=='types')throw Error('Recommended capture is restricted to plan types.');
const plan=recommended?JSON.parse(fs.readFileSync('public/app-v3/recommended-copy.json')).planSelection:null;
const out=`public/app-v3/${recommended?'recommended/':''}screens`;fs.mkdirSync(out,{recursive:true});
const installed='/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome';
const browser=await chromium.launch({channel:'chromium',executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||(fs.existsSync(installed)?installed:undefined),args:['--disable-dev-shm-usage']});
const screens=[['countries','Countries'],['dashboard','Dashboard'],['destination','Plans · 1 · country'],['duration','Plans · 3 · options'],['esims','My eSIMs'],['profile','eSIM profile (activated)'],['settings','Settings'],['account','Me'],['collection','Variant · 9 eSIMs, dense list'],['types','Plans · 2 · package type'],['notifications','Variant · Notifications prompt']];
const report=[];
for(const [id,label] of screens){
 if(process.env.CAPTURE_ONLY&&id!==process.env.CAPTURE_ONLY)continue;
 const page=await browser.newPage({viewport:{width:400,height:800},deviceScaleFactor:4});
 await page.goto('http://127.0.0.1:5176/?view=gallery',{waitUntil:'networkidle'});
 const panel=page.locator('.ol-app-motion').filter({has:page.locator(':scope > p').filter({hasText:new RegExp('^'+label.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'$')})}).locator(':scope > div').first();
 await panel.waitFor();
 await panel.evaluate((el,{id,recommended,plan})=>{
  const leaves=()=>[...el.querySelectorAll('h1,h2,h3,p,span,button')].filter(x=>!x.querySelector('h1,h2,h3,p,span,button'));
  if(id==='settings'){
   const h=[...el.querySelectorAll('p')].find(x=>x.textContent==='Form elements');
   if(h){while(h.nextElementSibling)h.nextElementSibling.remove();h.remove()}
   for(const x of leaves())if(/^(Currency|Marketing emails|Auto network switching|Ad & tracker blocking)$/.test(x.textContent))x.closest('div.flex.items-center')?.remove();
  }
  for(const x of el.querySelectorAll('.text-right'))if(/[$€£]|From/.test(x.textContent))x.remove();
  for(const x of leaves()){
   const t=x.textContent.trim();
   if(id==='account'&&/^(Payment methods|Referrals)$/.test(t)){x.closest('div.flex.items-center')?.remove();continue}
   if(id==='account'&&/^\$142$|^saved$/.test(t)){x.parentElement?.remove();continue}
   if(/Refunded|Ended Nov|Ended Aug|Ended Jul|Ended May/.test(t)){x.closest('.rounded-2xl.border-2.bg-white')?.remove();continue}
   if(t==='Purchase code'){if(id==='collection')x.textContent='Not activated';else x.closest('.border-orange-200')?.remove();continue}
   if(t==='Purchase code · not activated')x.textContent='Not activated';
   if(/Search 190/.test(t)){x.textContent='Search destinations';continue}
   if(t==='Europe (30+ countries)'){x.textContent='Europe';continue}
   if(t==='alex@email.com')x.textContent='alex@example.com';
   if(t==='Openline+')x.remove();
   if(/9 eSIMs · scroll/.test(t))x.textContent='Your travel eSIM collection';
   if(t.includes('We will tell you at 50%'))x.textContent='Choose whether Openline can send you notifications.';
   if(t==='Know before you run out')x.textContent='Your notifications';
   if(recommended&&id==='types'&&t==='Unlimited data'){x.textContent=plan.unlimitedLabel;continue}
   if(recommended&&id==='types'&&t==='Fixed package'){x.textContent=plan.fixedLabel;continue}
   if(recommended&&id==='types'&&t.startsWith('Full speed,')){x.textContent=plan.unlimitedDetail;continue}
   if(recommended&&id==='types'&&t.startsWith('A set amount of data')){x.textContent=plan.fixedDetail;continue}
   if(/\bUnlimited\b/.test(t)&&!x.querySelector('svg'))x.textContent=t.replace('Unlimited data','Data plan').replace('Unlimited','Data plan');
   if(t.includes('Pay only for what you need.'))x.textContent=t.replace(' Pay only for what you need.','');
   if(/[$€£¥₹₽]|\b(best value|full speed|hotspot included|purchased on|use your purchase|payment|billing|refund|earned|saved|Most popular)\b|\d+\+? (networks|countries)/i.test(t))x.remove();
  }
  for(const x of [...el.querySelectorAll('button')])if(/buy|top.?up|refill|checkout|wallet|payment|billing|gift/i.test(x.textContent))x.remove();
  for(const x of el.querySelectorAll('svg.lucide-credit-card,svg.lucide-infinity'))x.parentElement?.remove();
  if(id==='account'){const g=el.querySelector('.grid-cols-3');if(g)g.style.gridTemplateColumns='repeat(2,minmax(0,1fr))'}
  const style=document.createElement('style');style.textContent='*{animation:none!important;transition:none!important}';el.append(style);
  el.style.borderRadius='0';el.style.border='0';el.style.boxShadow='none';el.dataset.captureId=id;document.body.replaceChildren(el);
 },{id,recommended,plan});
 await page.evaluate(()=>document.fonts.ready);
 const isolated=page.locator(`[data-capture-id="${id}"]`),text=await isolated.innerText();
 if(id==='countries'&&!/\bEurope\b/.test(text))throw Error('Countries capture must retain the Europe label');
 if(recommended&&(!text.includes('Unlimited usage')||!text.includes('Fixed usage')))throw Error('Missing confirmed plan labels');
 if(/[$€£¥₹₽]|\b(price|prices|pay|payment|checkout|refund|cheap|savings|buy|purchase|purchased)\b/i.test(text))throw Error('Monetary content '+id+'\n'+text);
 await isolated.screenshot({path:`${out}/${id}.png`});
 report.push({id,source:label,text,width:1360,height:2800,status:'Adapted design reference; native release capture required'});
 await page.close();
}
const provenance=`public/app-v3/${recommended?'recommended/':''}capture-provenance.json`;
const previous=process.env.CAPTURE_ONLY&&fs.existsSync(provenance)?JSON.parse(fs.readFileSync(provenance)):[];
fs.writeFileSync(provenance,JSON.stringify(previous.length?previous.map(x=>report.find(r=>r.id===x.id)||x):report,null,2));await browser.close();
console.log(`${report.length} source views captured.`);
