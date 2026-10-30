import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const base=process.env.QA_URL||'http://127.0.0.1:5174/';
const out='/home/user/workspace/openline-fly-deployment/recommended-v2-7-2';
fs.mkdirSync(out,{recursive:true});
const key='openline-store-workspace-v3';
const rec={apple:['01','02','11','04','19','10','17','06','15','18'],google:['01','02','11','04','19','10','17','18']};
const read=page=>page.evaluate(k=>JSON.parse(localStorage.getItem(k)),key);
const order=page=>page.locator('.sw-selected > div > span').allTextContents().then(v=>v.map(t=>t.replace('Candidate ','')));
const b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome',args:['--disable-dev-shm-usage']});
try{
 const c=await b.newContext({viewport:{width:1440,height:1000},permissions:['clipboard-read','clipboard-write'],acceptDownloads:true});
 let p=await c.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto(base+'#/app?version=recommended',{waitUntil:'networkidle'});
 await p.getByRole('heading',{name:'Recommended selection.',exact:true}).waitFor();
 assert.deepEqual(await order(p),rec.apple);assert.equal((await read(p)).final,null);
 assert.equal(await p.getByRole('button',{name:'Save final draft',exact:true}).count(),0);
 assert.equal(await p.locator('.sw-confirm').count(),0);
 await p.getByRole('button',{name:'Preview App Store',exact:true}).click();
 assert.equal(await p.locator('.sw-store-shots button').count(),10);await p.keyboard.press('Escape');
 await p.getByRole('button',{name:'Preview on iPhone',exact:true}).click();
 assert.equal(await p.locator('.sw-device-buttons button').count(),10);await p.keyboard.press('Escape');
 await p.getByRole('button',{name:'Android / Google'}).click();assert.deepEqual(await order(p),rec.google);
 await p.getByRole('button',{name:'Share selection',exact:true}).click();
 const link=await p.locator('.sw-share input').inputValue();assert(link.includes('version=recommended'));assert.equal((await read(p)).final,null);
 await p.getByRole('button',{name:'Use recommended in V3',exact:true}).click();
 assert.equal(await p.locator('.sw-candidates article').count(),20);
 assert.equal(await p.locator('.sw-confirm input').isChecked(),false);assert.equal((await read(p)).final,null);
 // Fixture simulates a pre-existing user's choices; no Final-confirmation action is performed.
 const original={schema:3,apple:['03','04','05','06','07','08','09','10','11','12'],google:['03','04','05','06','07','08','09','10'],appleCopy:'B',googleCopy:'C',review:{publisher:{status:'pending',note:'QA private note'}},final:{apple:['01','02','03','04','05','06','07','08','09','10'],google:['01','02','03','04','05','06','07','08'],appleCopy:'A',googleCopy:'B'}};
 await p.evaluate(({key,original})=>localStorage.setItem(key,JSON.stringify(original)),{key,original});
 await p.close();p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));
 await p.goto(base+'#/app?version=recommended',{waitUntil:'networkidle'});
 assert.deepEqual(await read(p),original);assert.deepEqual(await order(p),rec.apple);
 for(const [button,title] of [['Preview App Store','Openline: Travel eSIM Plans'],['Preview Google Play','Openline: Travel eSIM Data']]){
  await p.getByRole('button',{name:button,exact:true}).click();
  assert((await p.locator('dialog').innerText()).includes(title));
  await p.keyboard.press('Escape');
 }
 assert.deepEqual(await read(p),original);
 for(const [platform,button] of [['apple','iOS / Apple'],['google','Android / Google']]){
  await p.getByRole('button',{name:button}).click();
  const download=p.waitForEvent('download');
  await p.getByRole('button',{name:'Download recommended set',exact:true}).click();
  await (await download).saveAs(out+'/'+platform+'.zip');
 }
 await p.close();p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));
 await p.goto(base+'#/app?version=recommended',{waitUntil:'networkidle'});
 await p.getByRole('button',{name:'Share selection',exact:true}).click();
 const shared=await p.locator('.sw-share input').inputValue(),params=new URLSearchParams(shared.split('?')[1]),sharedData=JSON.parse(Buffer.from(params.get('s'),'base64').toString());
 assert.equal(sharedData.review,undefined);
 await p.getByRole('button',{name:'Use recommended in V3',exact:true}).click();
 const after=await read(p);assert.deepEqual(after.apple,rec.apple);assert.deepEqual(after.google,rec.google);
 for(const k of ['final','review','appleCopy','googleCopy'])assert.deepEqual(after[k],original[k]);
 assert.equal(await p.locator('.sw-confirm input').isChecked(),false);
 for(const v of ['v1','v2','final','recommended']){
  await p.close();p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));
  await p.goto(base+'#/app?version='+v,{waitUntil:'networkidle'});assert((await p.locator('body').innerText()).length>500);
 }
 await p.setViewportSize({width:375,height:812});assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await p.screenshot({path:out+'/recommended-mobile.png'});
 assert.deepEqual(errors,[]);console.log(JSON.stringify({url:base,apple:rec.apple,google:rec.google,finalCreated:false,existingDraftPreserved:true,existingFinalPreserved:true,copyAndReviewPreserved:true,zipDownloads:true,previews:true,archives:true,mobileOverflow:false,errors}));
}finally{await b.close()}
