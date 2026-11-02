import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {execSync} from 'node:child_process';
const base=process.env.QA_URL||'http://127.0.0.1:5173/';
const b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'});
const ctx=await b.newContext({viewport:{width:1280,height:900},acceptDownloads:true,permissions:['clipboard-read','clipboard-write']});
const p=await ctx.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
// default is Current
await p.goto(base+'app',{waitUntil:'networkidle'});
assert.equal(await p.locator('.sw-editions').count(),1);
assert.equal(await p.getByRole('button',{name:'Current',exact:true}).getAttribute('aria-pressed'),'true');
assert.equal(await p.getByRole('button',{name:'Final draft'}).count(),0,'archives hidden by default');
await p.getByRole('button',{name:/^Archives/}).click();
const items=await p.getByRole('menuitem').allInnerTexts();assert.equal(items.length,4);
await p.keyboard.press('Escape');assert.equal(await p.getByRole('menuitem').count(),0);
for(const [label,key] of [[/V2/,'v2'],[/V1/,'v1'],[/V3/,'v3'],[/Final draft/,'final']]){
 await p.getByRole('button',{name:/^Archives/}).click();await p.getByRole('menuitem',{name:label}).click();await p.waitForTimeout(500);
 assert(p.url().includes('version='+key),key);assert.equal(await p.locator('.sw-editions').count(),1,key+' single nav');
 assert((await p.getByRole('button',{name:/^Archives/}).innerText()).includes('Archives ·'));}
await p.getByRole('button',{name:'Current',exact:true}).click();await p.waitForTimeout(500);assert(p.url().includes('version=recommended'));
const cat=await p.locator('#sw-category').innerText();assert(cat.includes('Travel and Local')&&cat.includes('Telecommunications')&&cat.includes('App Store Connect'));
await p.getByRole('button',{name:/Download category setup/}).click().catch(()=>{});
// large editor + note editor
await p.goto(base+'app?version=recommended',{waitUntil:'networkidle'});
await p.getByRole('button',{name:'Expand Full description'}).click();
const big=p.getByLabel('Large editor text for Full description');await big.fill('Large editor rewrite.');
assert((await p.getByRole('button',{name:'Done'}).boundingBox()).width>40);
await p.getByRole('button',{name:'Done'}).click();
assert.equal(await p.getByLabel('Edit Full description',{exact:true}).inputValue(),'Large editor rewrite.');
const h1=await p.getByLabel('Edit Promotional text',{exact:true}).evaluate(n=>n.getBoundingClientRect().height);
await p.getByLabel('Edit Full description',{exact:true}).fill('x\n'.repeat(60));
assert((await p.getByLabel('Edit Full description',{exact:true}).evaluate(n=>n.getBoundingClientRect().height))>600,'auto-grow');
await p.getByLabel('Edit Full description',{exact:true}).fill('Large editor rewrite.');
await p.getByLabel('Edit Subtitle',{exact:true}).fill('Edited subtitle');
// review note
const note=p.getByLabel(/review note/).first();await note.scrollIntoViewIfNeeded();await note.fill('Evidence: ticket 42');
// bottom share bar is last section
assert(await p.locator('.sw-sharebar').count()===1);
await p.getByRole('button',{name:/Share or export/}).click();
const url=await p.locator('.sw-share-dialog input').inputValue();assert(url.includes('t='));
const dl=async(name)=>{const [d]=await Promise.all([p.waitForEvent('download'),p.getByRole('button',{name}).click()]);const f='/dev/shm/'+d.suggestedFilename();await d.saveAs(f);return f};
const zip=await dl(/Download ZIP/);
const names=execSync('unzip -Z1 '+zip).toString();for(const n of ['README.md','openline-app-modifications.json','listing-copy-app-store.md','listing-copy-google-play.md'])assert(names.includes(n),n);
const readme=execSync('unzip -p '+zip+' README.md').toString();assert(readme.includes('Edited subtitle')&&readme.includes('Evidence: ticket 42')&&readme.includes('Large editor rewrite.'));
const js=JSON.parse(execSync('unzip -p '+zip+' openline-app-modifications.json').toString());assert.equal(js.recommendedCopyEdits.apple.subtitle,'Edited subtitle');
assert(execSync('unzip -p '+zip+' listing-copy-app-store.md').toString().includes('Edited subtitle'));
await dl(/^JSON$/);await dl(/Summary/);
await p.keyboard.press('Escape');
// share link in a fresh context shows edits, not notes
const c2=await b.newContext({viewport:{width:1280,height:900}});const q=await c2.newPage();
await q.goto(url,{waitUntil:'networkidle'});
assert.equal(await q.getByLabel('Edit Subtitle',{exact:true}).inputValue(),'Edited subtitle');
assert.equal(await q.getByLabel('Edit Full description',{exact:true}).inputValue(),'Large editor rewrite.');
assert.equal(await q.getByLabel(/review note/).first().inputValue(),'');
assert(!q.url().includes('t='));
await q.reload({waitUntil:'networkidle'});assert.equal(await q.getByLabel('Edit Subtitle',{exact:true}).inputValue(),'Edited subtitle');
// mobile
const m=await b.newContext({viewport:{width:390,height:800},hasTouch:true});const mp=await m.newPage();
await mp.goto(base+'app',{waitUntil:'networkidle'});
await mp.getByRole('button',{name:/^Archives/}).click();assert(await mp.getByRole('menuitem').first().isVisible());
assert(await mp.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'no overflow');
await b.close();
console.log(JSON.stringify({url:base,currentDefault:true,archivesMenu:true,singleNav:true,largeEditor:true,autoGrow:true,shareLink:true,exportZip:true,mobile:true,errors}));
