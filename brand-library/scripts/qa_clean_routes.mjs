import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const base=process.env.QA_URL||'http://127.0.0.1:5178/';
const out='/home/user/workspace/openline-fly-deployment/clean-routes-v2-7-9';fs.mkdirSync(out,{recursive:true});
const routes=['overview','logos','assets','ads','motion','presenters','app','guidelines','archives'];
const errors=[],b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'});
let c=await b.newContext({viewport:{width:1440,height:1000}}),p=await c.newPage();
const fresh=async()=>{await c.close();c=await b.newContext({viewport:{width:1440,height:1000}});p=await c.newPage();p.on('pageerror',e=>errors.push(e.message))};
const active=()=>p.locator('nav[aria-label="Main navigation"] a[aria-current="page"]');
try{
 for(const route of routes){
  await fresh();
  const r=await p.goto(base+route,{waitUntil:'networkidle'});assert.equal(r.status(),200);
  assert.equal(await active().getAttribute('href'),'/'+route);
  await p.reload({waitUntil:'networkidle'});assert.equal(await active().getAttribute('href'),'/'+route);
  await p.goto(base+route+'/',{waitUntil:'networkidle'});assert.equal(new URL(p.url()).pathname,'/'+route);
  assert.equal(await active().getAttribute('href'),'/'+route);
  assert(await p.locator('.library-brand img').evaluate(e=>e.complete&&e.naturalWidth>0));
  await p.goto(base+'#/'+route,{waitUntil:'networkidle'});assert.equal(new URL(p.url()).hash,'');assert.equal(await active().getAttribute('href'),'/'+route);
  console.log('Route passed:',route);
 }
await fresh();await p.goto(base+'app?version=recommended',{waitUntil:'networkidle'});
 await p.getByRole('heading',{name:'App & store.',exact:true}).waitFor();
 const nav=p.locator('nav[aria-label="Main navigation"]');
 await nav.getByRole('link',{name:'Logos',exact:true}).click();assert.equal(new URL(p.url()).pathname,'/logos');
 await nav.getByRole('link',{name:'Motion',exact:true}).click();assert.equal(new URL(p.url()).pathname,'/motion');
 await p.goBack();await p.waitForURL('**/logos');assert.equal(await active().getAttribute('href'),'/logos');
 await p.goForward();await p.waitForURL('**/motion');assert.equal(await active().getAttribute('href'),'/motion');
 await p.goto(base+'#/app?store=google',{waitUntil:'networkidle'});
 assert.equal(new URL(p.url()).hash,'');assert.equal(new URL(p.url()).searchParams.get('store'),'google');
 await p.getByRole('heading',{name:'App & store.',exact:true}).waitFor();
 await p.setViewportSize({width:375,height:812});
 assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 await p.goto(base+'#iphone',{waitUntil:'networkidle'});assert.equal(new URL(p.url()).pathname,'/studio.html');assert.equal(new URL(p.url()).hash,'#iphone');
 if(base.startsWith('https:')){
  for(const path of ['not-a-real-brand-page','assets/missing-test.js','app/nested-missing','missing.zip']){
   const r=await c.request.get(base+path);assert.equal(r.status(),404,path);
  }
 }
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({base,routes:routes.length,direct:true,refresh:true,trailingSlashes:true,legacyHashes:true,backForward:true,sharedSelection:true,editionQuery:true,legacyStudio:true,mobile:true,errors}));
}finally{await b.close()}
