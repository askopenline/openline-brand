// Deterministic design-only derivatives of the supplied React screen resources.
// Original app source and V1 captures are never modified.
import {chromium} from 'playwright';
import fs from 'node:fs';
const out='public/app-v2/screens';
fs.mkdirSync(out,{recursive:true});
const installed='/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome';
const executablePath=process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||(fs.existsSync(installed)?installed:undefined);
const browser=await chromium.launch({channel:'chromium',...(executablePath?{executablePath}:{}),headless:true,args:['--disable-dev-shm-usage']});
const screens=[['countries','Countries'],['settings','Settings'],['profile','eSIM profile (activated)'],['esims','My eSIMs'],['dashboard','Dashboard'],['plans','Plans · 3 · options']];
const report=[];
for(const [id,label] of screens){
 const page=await browser.newPage({viewport:{width:400,height:800},deviceScaleFactor:4});
 await page.goto('http://127.0.0.1:5176/?view=gallery',{waitUntil:'networkidle'});
 const panel=page.locator('.ol-app-motion').filter({has:page.locator(':scope > p').filter({hasText:new RegExp('^'+label.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'$')})}).locator(':scope > div').first();
 await panel.waitFor();
 await panel.evaluate((el,id)=>{
  const leaf=()=>[...el.querySelectorAll('p,span,button')].filter(x=>!x.querySelector('p,span,button'));
  if(id==='settings'){
   const heading=[...el.querySelectorAll('p')].find(x=>x.textContent==='Form elements');
   if(heading){while(heading.nextElementSibling)heading.nextElementSibling.remove();heading.remove()}
   for(const x of leaf())if(x.textContent==='Currency'||x.textContent==='Marketing emails')x.closest('div.flex.items-center')?.remove();
  }
  // Keep country identity and chevrons, remove the complete amount/From group.
  if(id==='countries')for(const x of el.querySelectorAll('.text-right'))x.remove();
  if(id==='esims'){
   for(const x of leaf())if(/Refunded|Ended Nov/i.test(x.textContent))x.closest('.rounded-2xl.border-2.bg-white')?.remove();
  }
  for(const x of [...el.querySelectorAll('button')]){
   if(/buy|top.?up|refill|checkout|wallet|payment|billing/i.test(x.textContent))x.remove();
  }
  for(const x of leaf()){
   const text=x.textContent.trim();
   if(/[$€£¥₹₽]|best value|full speed|hotspot included|purchased on|use your purchase|payment|billing|refund/i.test(text)){x.remove();continue}
   if(text==='Purchase code'){x.closest('.border-orange-200')?.remove();continue}
   if(/Purchase code · not activated/.test(text))x.textContent='Not activated';
  }
  // Avoid leaving an empty area reserved for monetary checkout controls.
  for(const x of [...el.querySelectorAll('div')].reverse())if(!x.children.length&&!x.textContent.trim()&&x.style.paddingBottom==='28px')x.remove();
  // Turn off entrance animation only after its intended final geometry is applied.
  const style=document.createElement('style');style.textContent='*{animation:none!important;transition:none!important}';el.append(style);
  el.style.borderRadius='0';el.style.border='0';el.style.boxShadow='none';
  el.dataset.captureId=id;
  document.body.replaceChildren(el);
 },id);
 await page.evaluate(()=>document.fonts.ready);
 const isolated=page.locator(`[data-capture-id="${id}"]`);
 const text=await isolated.innerText();
 if(/[$€£¥₹₽]|\b(price|prices|pay|payment|checkout|refund|cheap|savings|buy|purchase|purchased)\b/i.test(text))throw Error('Monetary text remains: '+id+'\n'+text);
 await isolated.screenshot({path:`${out}/${id}.png`});
 report.push({id,source:label,text,width:1360,height:2800,modifiedDesignReference:true});
 await page.close();
}
fs.writeFileSync('public/app-v2/capture-provenance.json',JSON.stringify(report,null,2));
await browser.close();
console.log('Captured six price-free derivatives from the supplied app resources.');
