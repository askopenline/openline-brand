import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {execSync} from 'node:child_process';
const base=process.env.QA_URL||'http://127.0.0.1:5178/';
const rec=JSON.parse(fs.readFileSync('public/app-v3/recommended-copy.json'));
const b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'});
const ctx=await b.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
let p=await ctx.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
const MAIN='openline-store-workspace-v3',EDIT='openline-recommended-copy-edits-v1';
const open=async()=>{await p.goto(base+'app?version=recommended&tab=all',{waitUntil:'networkidle'})};
try{
 await open();
 const mainBefore=await p.evaluate(k=>localStorage.getItem(k),MAIN);
 assert.equal(await p.getByLabel('Edit Promotional text',{exact:true}).inputValue(),rec.apple.promotional);
 // Edit Apple promo + subtitle, Google short description
 await p.getByLabel('Edit Promotional text',{exact:true}).fill('My own promo text for Apple.');
 await p.getByLabel('Edit Subtitle',{exact:true}).fill('A subtitle I wrote');
 assert((await p.locator('.sw-text-field',{hasText:'Promotional text'}).innerText()).includes('Edited'));
 assert((await p.locator('.sw-text-field',{hasText:'Promotional text'}).innerText()).includes('28 / 170'));
 await p.getByRole('button',{name:/Android \/ Google/}).click();
 await p.getByLabel('Edit Short description',{exact:true}).fill('Short Google text I typed.');
 await p.getByLabel('Edit Full description',{exact:true}).fill('Full Google description I edited.');
 // previews follow edits
 await p.getByRole('button',{name:'Preview Google Play',exact:true}).click();
 assert.equal(await p.locator('.sw-store-description').innerText(),'Full Google description I edited.');
 assert((await p.locator('.sw-store-brand').innerText()).includes('Short Google text I typed.'));
 await p.keyboard.press('Escape');
 // persistence across reload (fresh page, same context storage)
 await p.close();p=await ctx.newPage();p.on('pageerror',e=>errors.push(e.message));await open();
 assert.equal(await p.getByLabel('Edit Promotional text',{exact:true}).inputValue(),'My own promo text for Apple.');
 assert.equal(await p.getByLabel('Edit Subtitle',{exact:true}).inputValue(),'A subtitle I wrote');
 await p.getByRole('button',{name:/Android \/ Google/}).click();
 assert.equal(await p.getByLabel('Edit Full description',{exact:true}).inputValue(),'Full Google description I edited.');
 // saved storage holds only changed fields and main state is untouched
 const saved=await p.evaluate(k=>JSON.parse(localStorage.getItem(k)),EDIT);
 assert.deepEqual(Object.keys(saved.apple).sort(),['promotional','subtitle']);assert.deepEqual(Object.keys(saved.google).sort(),['description','shortDescription']);
 assert.equal(await p.evaluate(k=>localStorage.getItem(k),MAIN),mainBefore);
 // download text uses edits
 const d=p.waitForEvent('download');await p.getByRole('button',{name:'Download text'}).click();
 const dl=await d;const path='/dev/shm/qa-copy.md';await dl.saveAs(path);const md=fs.readFileSync(path,'utf8');
 assert(md.includes('Full Google description I edited.')&&md.includes('Short Google text I typed.'));
 // zip listing-copy uses edits
 const d2=p.waitForEvent('download');await p.getByRole('button',{name:'Download recommended set',exact:true}).click();
 const z=await d2;await z.saveAs('/dev/shm/qa-google.zip');
 const listing=execSync('unzip -p /dev/shm/qa-google.zip listing-copy.md').toString();assert(listing.includes('Full Google description I edited.'));
 // over-limit warning, reset single, reset all
 await p.getByLabel('Edit Short description',{exact:true}).fill('x'.repeat(90));
 assert((await p.locator('.sw-text-field',{hasText:'Short description'}).innerText()).includes('over limit'));
 await p.getByRole('button',{name:'Reset Short description to the recommended text'}).click();
 assert.equal(await p.getByLabel('Edit Short description',{exact:true}).inputValue(),rec.google.shortDescription);
 await p.getByRole('button',{name:'Restore all Google Play text'}).click();
 assert.equal(await p.getByLabel('Edit Full description',{exact:true}).inputValue(),rec.google.description);
 assert.equal(await p.getByRole('button',{name:'Restore all Google Play text'}).count(),0);
 // Apple edits remain after Google reset
 await p.getByRole('button',{name:/iOS \/ Apple/}).click();
 assert.equal(await p.getByLabel('Edit Promotional text',{exact:true}).inputValue(),'My own promo text for Apple.');
 await p.getByRole('button',{name:'Preview App Store',exact:true}).click();
 assert((await p.locator('.sw-store-brand').innerText()).includes('A subtitle I wrote'));
 await p.keyboard.press('Escape');
 // other editions unaffected
 await p.goto(base+'app?version=final',{waitUntil:'networkidle'});
 await p.getByRole('button',{name:'Preview App Store',exact:true}).click().catch(()=>{});
 assert(!(await p.locator('body').innerText()).includes('A subtitle I wrote'));
 // mobile
 await open();await p.setViewportSize({width:375,height:812});
 assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await p.getByLabel('Edit Full description',{exact:true}).scrollIntoViewIfNeeded();
 await p.screenshot({path:(process.env.QA_OUT||'/dev/shm')+'/edit-mobile.png'});
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({url:base,editable:true,persists:true,previewsAndDownloadsUseEdits:true,resetField:true,resetAll:true,mainStateUntouched:true,overLimitWarning:true,mobile:true,errors}));
}finally{await b.close()}
