import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const base=process.env.QA_URL||'http://127.0.0.1:5174/',out='/home/user/workspace/openline-fly-deployment/recommended-v2-7-6';
fs.mkdirSync(out,{recursive:true});
const rec=JSON.parse(fs.readFileSync('public/app-v3/recommended-copy.json')),old=JSON.parse(fs.readFileSync('public/app-v3/copy.json')).options[0];
const b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome',args:['--disable-dev-shm-usage']});
try{
 let c=await b.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
 const key='openline-store-workspace-v3';
 const fixture={schema:3,apple:['01','02','11'],google:['01','11'],appleCopy:'B',googleCopy:'C',review:{publisher:{status:'pending',note:'Keep this draft note'}},final:{apple:['01','11','02','03','04','05','06','07','08','09'],google:['11','02','03','04','05','06','07','08'],appleCopy:'A',googleCopy:'A'}};
 let p=await c.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto(base);await p.evaluate(({key,fixture})=>localStorage.setItem(key,JSON.stringify(fixture)),{key,fixture});await p.close();
 const reopen=async(view='recommended')=>{await c.close();c=await b.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});await c.addInitScript(({key,fixture})=>localStorage.setItem(key,JSON.stringify(fixture)),{key,fixture});p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(base+'#/app?version='+view,{waitUntil:'networkidle'})};
 await reopen();
 assert.equal(await p.locator('.sw-verification li').count(),6);
 assert.equal(await p.getByRole('button',{name:'Save final draft',exact:true}).count(),0);
 for(const [platform,button,device] of [['apple','iOS / Apple','Preview on iPhone'],['google','Android / Google','Preview on Android']]){
  await p.getByRole('button',{name:button}).click();
  assert((await p.locator('.sw-copy-details').innerText()).includes(rec[platform].description.split('\n')[0]));
  assert((await p.locator('.sw-selected-image img').nth(2).getAttribute('src')).includes('/recommended/'));
  await p.getByRole('button',{name:platform==='apple'?'Preview App Store':'Preview Google Play',exact:true}).click();
  assert.equal(await p.locator('.sw-store-description').innerText(),rec[platform].description);
  assert((await p.locator('.sw-store-shots img').nth(2).getAttribute('src')).includes('/recommended/'));
  await p.keyboard.press('Escape');
  assert.deepEqual(await p.evaluate(k=>JSON.parse(localStorage.getItem(k)),key),fixture);
  await p.close();await reopen();await p.getByRole('button',{name:button}).click();
  await p.getByRole('button',{name:device,exact:true}).click();
  await p.locator('.sw-device-buttons').getByRole('button',{name:'11',exact:true}).click();
  assert((await p.locator('.sw-phone img').getAttribute('src')).includes('/recommended/screens/types.png'));
  await p.keyboard.press('Escape');
  await p.close();await reopen();await p.getByRole('button',{name:button}).click();
  const d=p.waitForEvent('download');await p.getByRole('button',{name:'Download recommended set',exact:true}).click();await(await d).saveAs(out+'/'+platform+'.zip');
  assert.deepEqual(await p.evaluate(k=>JSON.parse(localStorage.getItem(k)),key),fixture);
  await p.close();await reopen();
 }
 await p.setViewportSize({width:375,height:812});
 await p.locator('.sw-verification').scrollIntoViewIfNeeded();assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await p.screenshot({path:out+'/verification-mobile.png'});
 await p.close();await reopen('final');
 await p.getByRole('button',{name:'Preview App Store',exact:true}).click();
 assert.equal(await p.locator('.sw-store-description').innerText(),old.apple.description);
 assert(!(await p.locator('.sw-store-shots img').nth(1).getAttribute('src')).includes('/recommended/'));
 await p.keyboard.press('Escape');
 assert.deepEqual(await p.evaluate(k=>JSON.parse(localStorage.getItem(k)),key),fixture);
 assert.deepEqual(errors,[]);console.log(JSON.stringify({url:base,revisedCopyBothStores:true,planTypesBothStores:true,devicePreviews:true,verificationFlags:6,downloads:true,finalCopyAndImagesPreserved:true,savedStateUnchanged:true,mobile:true,errors}));
}finally{await b.close()}
