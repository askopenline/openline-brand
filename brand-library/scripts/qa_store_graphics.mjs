import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {execSync} from 'node:child_process';
const base=process.env.QA_URL||'http://127.0.0.1:5173/',out=process.env.QA_OUT||'/tmp/qa';fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'});
const ctx=await b.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});let p=await ctx.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
const PK='openline-proofread-v1',store=()=>p.getByRole('group',{name:'Store'});
const man=JSON.parse(fs.readFileSync('public/app-v3/recommended/store-graphics.json'));
try{
 await p.goto(base+'app',{waitUntil:'networkidle'});
 // steps and overview
 const tabs=await p.getByRole('tab').allInnerTexts();assert.deepEqual(tabs,['Overview','Text','Graphics','Screenshots','Category','Review','Export','All in one page']);
 assert(await p.getByText('0 of 13 proofread').isVisible());
 // graphics: Apple
 await p.getByRole('tab',{name:'Graphics'}).click();
 assert.equal(await p.locator('.sw-gfx').count(),man.apple.length);
 for(const a of man.apple)assert(await p.locator(`[data-asset="${a.id}"] .sw-chip.ok`).isVisible(),a.id);
 for(const img of await p.locator('.sw-gfx img').all()){await img.scrollIntoViewIfNeeded();await img.evaluate(i=>new Promise(r=>{const t=Date.now();(function w(){if(i.complete||Date.now()-t>8000)r();else setTimeout(w,100)})()}));assert(await img.evaluate(i=>i.complete&&i.naturalWidth>0),'image loads')}
 assert((await p.locator('.sw-optional').innerText()).includes('iPad'));
 // proofread persists
 await p.getByLabel('Proofread App icon',{exact:true}).check();
 await p.getByLabel('Note for App icon',{exact:true}).fill('Check corner radius');
 await store().getByRole('button',{name:/App Store/}).waitFor();
 assert((await store().innerText()).includes('1/13'));
 // Google
 await store().getByRole('button',{name:/Google Play/}).click();
 assert.equal(await p.locator('.sw-gfx').count(),man.google.length);
 for(const a of man.google)assert(await p.locator(`[data-asset="${a.id}"] .sw-chip.ok`).isVisible(),a.id);
 const fg=p.locator('[data-asset="google.feature"] img');await fg.scrollIntoViewIfNeeded();await p.waitForFunction(()=>document.querySelector('[data-asset="google.feature"] img').naturalWidth>0);assert.deepEqual(await fg.evaluate(i=>[i.naturalWidth,i.naturalHeight]),[1024,500]);
 await p.locator('[data-asset="google.feature-light"]').getByRole('button',{name:'Use this one'}).click();
 assert((await p.locator('[data-asset="google.feature-light"]').innerText()).includes('in use'));
 // preview uses chosen
 await p.getByRole('tab',{name:'Text'}).click();
 assert((await p.locator('.sw-live .sw-feature').getAttribute('src')).includes('feature-graphic-light.png'));
 assert(await p.locator('.sw-live').isVisible());
 // lint chips show
 assert((await p.locator('.sw-text-field',{hasText:'Short description'}).locator('.sw-checks').innerText()).includes('checks pass'));
 // proofread text then edit clears
 await p.getByLabel('Proofread Short description',{exact:true}).check();
 await p.getByLabel('Edit Short description',{exact:true}).fill('Travel eSIM data for your next trip.');
 assert.equal(await p.getByLabel('Proofread Short description',{exact:true}).isChecked(),false);
 await p.getByLabel('Edit Short description',{exact:true}).fill('Travel eSIM data. Best price!');
 assert((await p.locator('.sw-text-field',{hasText:'Short description'}).locator('.sw-checks').innerText()).includes('Check:'));
 await p.getByLabel('Edit Short description',{exact:true}).fill('Travel eSIM data for your next trip.');
 await p.getByLabel('Proofread Short description',{exact:true}).check();
 // persistence across reload
 await p.close();p=await ctx.newPage();p.on('pageerror',e=>errors.push(e.message));
 await p.goto(base+'app?tab=graphics',{waitUntil:'networkidle'});
 assert.equal(await p.getByLabel('Proofread App icon',{exact:true}).isChecked(),true);
 assert.equal(await p.getByLabel('Note for App icon',{exact:true}).inputValue(),'Check corner radius');
 const saved=await p.evaluate(k=>JSON.parse(localStorage.getItem(k)),PK);assert.equal(saved.choice.feature,'light');assert(saved.ok['apple.icon']);assert(saved.ok['google.text.shortDescription']);
 // Apple creative assets
 for(const id of['apple.header','apple.search','apple.universal'])assert(await p.locator(`[data-asset="${id}"]`).isVisible(),id);
 // graphics ZIP for a group
 await p.locator('[data-asset="apple.screens"]').scrollIntoViewIfNeeded();
 const d=p.waitForEvent('download');await p.locator('[data-asset="apple.screens"]').getByRole('button',{name:/Download 8 files/}).click();await(await d).saveAs(out+'/apple-screens.zip');
 assert.equal(execSync(`unzip -l ${out}/apple-screens.zip | grep -c png`).toString().trim(),'8');
 // google store zip carries chosen feature graphic + report
 await p.getByRole('tab',{name:'Export'}).click();
 await store().getByRole('button',{name:/Google Play/}).click();
 const d2=p.waitForEvent('download');await p.getByRole('button',{name:/Google Play set/}).click();await(await d2).saveAs(out+'/google.zip');
 const lst=execSync(`unzip -l ${out}/google.zip`).toString();assert(lst.includes('feature-graphic.png')&&lst.includes('store-graphics-report.md')&&lst.includes('screenshot-alt-text.md'));
 execSync(`cd ${out} && rm -rf gz && mkdir gz && cd gz && unzip -q ../google.zip feature-graphic.png && python3 -c "from PIL import Image;im=Image.open('feature-graphic.png');assert im.size==(1024,500);print(im.getpixel((5,5)))" > px.txt`);
 const px=fs.readFileSync(out+'/gz/px.txt','utf8');assert(!px.includes('(255, 100, 24)'),'light variant packed: '+px);
 // export zip includes proofread
 await p.getByRole('button',{name:/Share or export/}).click();
 const d3=p.waitForEvent('download');await p.getByRole('button',{name:/Download ZIP/}).click();await(await d3).saveAs(out+'/all.zip');
 const l3=execSync(`unzip -l ${out}/all.zip`).toString();assert(l3.includes('store-graphics-report.md')&&l3.includes('store-graphics/google-feature-graphic-chosen.png'));
 execSync(`cd ${out} && unzip -p all.zip openline-app-modifications.json > all.json && unzip -p all.zip README.md > all.md`);
 const j=JSON.parse(fs.readFileSync(out+'/all.json'));assert(j.proofread.ok['apple.icon']);assert(fs.readFileSync(out+'/all.md','utf8').includes('items proofread'));
 await p.keyboard.press('Escape');
 // overview progress
 await p.getByRole('tab',{name:'Overview'}).click();assert((await p.locator('.sw-overview-grid').innerText()).includes('1 of 13 proofread'));
 // mobile
 const m=await ctx.newPage();await m.setViewportSize({width:390,height:844});await m.goto(base+'app?tab=graphics',{waitUntil:'networkidle'});
 assert.equal(await m.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await m.screenshot({path:out+'/graphics-mobile.png'});
 await m.getByRole('tab',{name:'Text'}).click();assert.equal(await m.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({url:base,steps:true,graphicsAppleGoogle:true,validationBadges:true,featureChoice:true,proofreadPersists:true,editClearsProof:true,lintChips:true,zips:true,export:true,mobile:true,errors}));
}catch(e){console.error(e);process.exitCode=1}finally{await b.close()}
