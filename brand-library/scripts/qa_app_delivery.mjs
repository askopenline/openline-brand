import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {execSync} from 'node:child_process';
const base=process.env.QA_URL||'http://127.0.0.1:5173/';
const out=process.env.QA_OUT||'/dev/shm/q';fs.mkdirSync(out,{recursive:true});
const KEY='openline-delivery-checklist-v2',errors=[];
const b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'});
const c=await b.newContext({viewport:{width:1440,height:1000},acceptDownloads:true,permissions:['clipboard-read','clipboard-write']});
const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>m.type()==='error'&&errors.push(m.text()));
const imgsOk=async()=>{
 const n=await p.locator('.dl img').count();
 for(let i=0;i<n;i++){const l=p.locator('.dl img').nth(i);await l.scrollIntoViewIfNeeded();await p.waitForTimeout(60)}
 await p.waitForTimeout(800);
 const bad=await p.evaluate(()=>[...document.querySelectorAll('.dl img')].filter(i=>!(i.complete&&i.naturalWidth>0)).map(i=>i.src));
 assert.deepEqual(bad,[]);return n};
const unzip=async(dl,name)=>{const f=`${out}/${name}.zip`;await dl.saveAs(f);const d=`${out}/${name}`;fs.rmSync(d,{recursive:true,force:true});fs.mkdirSync(d,{recursive:true});execSync(`unzip -qo ${f} -d ${d}`);
 const all=execSync(`cd ${d} && find . -type f | sort`).toString().trim().split('\n');return {d,all}};
try{
 for(const store of ['apple','google']){
  await p.goto(base+'app'+(store==='google'?'?store=google':''),{waitUntil:'networkidle'});
  await p.evaluate(k=>localStorage.removeItem(k),KEY);await p.reload({waitUntil:'networkidle'});
  await p.getByRole('heading',{name:'App & store.',exact:true}).waitFor();
  assert.equal(await p.locator('.dl-switch [aria-pressed=true]').innerText().then(t=>t.includes(store==='apple'?'App Store':'Google Play')),true);
  const copies=await p.locator('#dl-listing .dl-copy').count();assert(copies>=3,'copy buttons '+copies);
  await p.locator('#dl-listing .dl-copy').first().click();
  const clip=await p.evaluate(()=>navigator.clipboard.readText());assert(clip.length>3);
  assert.equal(await p.locator('.dl-count.is-over').count(),0);
  console.log(store,'images',await imgsOk());
  // checklist
  const boxes=p.locator('#dl-checklist .dl-group input[type=checkbox]');const n=await boxes.count();assert(n>10,'items '+n);
  await boxes.nth(0).check({force:true});await boxes.nth(1).check({force:true});
  assert.equal(Object.keys(await p.evaluate(k=>JSON.parse(localStorage.getItem(k)),KEY)).length,2);
  await p.reload({waitUntil:'networkidle'});assert.equal(await boxes.nth(0).isChecked(),true);
  await p.getByLabel('Show open items only').check();assert.equal(await boxes.count(),n-2);
  await p.getByLabel('Show open items only').uncheck();
  await p.getByRole('button',{name:/Reset/}).click();assert.equal(await boxes.nth(0).isChecked(),false);
  // zip
  const [dl]=await Promise.all([p.waitForEvent('download'),p.getByRole('button',{name:/^Download .* package/}).click()]);
  const z=await unzip(dl,store);console.log(z.all.join('\n'));
  for(const must of ['README','HANDOFF.md','listing.md','listing.json','category.md','checklist.md','graphics/','screenshots/'])assert(z.all.some(f=>f.includes(must)),'zip missing '+must);
  assert(z.all.some(f=>/screenshots\/\d+x\d+\/01-.*\.png$/.test(f)));
  assert.equal(z.all.some(f=>/reviewer/i.test(f)),false);
  if(store==='google')assert(z.all.some(f=>f.includes('screenshot-alt-text.md')));
  for(const f of z.all.filter(f=>f.endsWith('.png')))assert(fs.statSync(z.d+'/'+f).size>1000,f);
  // mobile
  await p.setViewportSize({width:375,height:812});await p.reload({waitUntil:'networkidle'});
  assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow');
  await p.screenshot({path:`${out}/${store}-mobile.png`});
  await p.setViewportSize({width:1440,height:1000});
 }
 await p.goto(base+'app',{waitUntil:'networkidle'});await p.screenshot({path:out+'/desktop-top.png'});
 await p.goto(base+'app?version=v2',{waitUntil:'networkidle'});await p.getByRole('heading',{name:'App & store.'}).waitFor();
 assert.deepEqual(errors,[]);console.log('Delivery QA passed');
}finally{await b.close()}
