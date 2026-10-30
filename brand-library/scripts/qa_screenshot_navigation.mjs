import {chromium} from 'playwright';
import assert from 'node:assert/strict';
const base=process.env.QA_URL||'http://127.0.0.1:5174/';
const b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome',args:['--disable-dev-shm-usage']});
try{
 const c=await b.newContext({viewport:{width:1440,height:1000}});
 let p=await c.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
 const saved=()=>p.evaluate(()=>localStorage.getItem('openline-store-workspace-v3'));
 const check=async(id,n)=>{assert((await p.locator('.sw-dialog-bar').innerText()).includes(`Candidate ${id} · ${n}`));assert((await p.locator('.sw-image-stage img').getAttribute('src')).includes('/'+id+'.png'));assert((await p.locator('.sw-full-art a').getAttribute('href')).includes('/'+id+'.png'))};
 await p.goto(base+'#/app?version=recommended',{waitUntil:'networkidle'});const initial=await saved();
 await p.locator('.sw-selected-image').first().click();await check('01','1 / 10');
 await p.getByRole('button',{name:'Next screenshot',exact:true}).click();await check('02','2 / 10');
 await p.keyboard.press('ArrowRight');await check('11','3 / 10');
 await p.keyboard.press('ArrowLeft');await check('02','2 / 10');
 await p.getByRole('button',{name:'Previous screenshot',exact:true}).click();await check('01','1 / 10');
 await p.keyboard.press('ArrowLeft');await check('18','10 / 10');
 await p.keyboard.press('ArrowRight');await check('01','1 / 10');
 await p.keyboard.press('Escape');assert.equal(await p.locator('dialog').count(),0);
 assert.equal(await p.locator('.sw-selected-image').first().evaluate(e=>document.activeElement===e),true);
 await p.getByRole('button',{name:'Preview Google Play',exact:true}).click();
 await p.getByRole('button',{name:'Preview selected screenshot 8',exact:true}).click();await check('18','8 / 8');
 await p.getByRole('button',{name:'Next screenshot',exact:true}).click();await check('01','1 / 8');
 await p.setViewportSize({width:375,height:812});assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 for(const label of ['Previous screenshot','Next screenshot']){const box=await p.getByRole('button',{name:label,exact:true}).boundingBox();assert(box.width>=44&&box.height>=44&&box.y>=0&&box.y+box.height<=812)}
 await p.screenshot({path:'/home/user/workspace/openline-fly-deployment/recommended-v2-7-2/navigation-mobile.png'});
 await p.keyboard.press('Escape');assert.equal(await saved(),initial);
 await p.close();p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));
 await p.goto(base+'#/app?version=v3',{waitUntil:'networkidle'});const before=await saved();
 await p.locator('.sw-candidates article').last().scrollIntoViewIfNeeded();
 await p.getByRole('button',{name:'Enlarge candidate 20',exact:true}).click();await check('20','20 / 20');
 await p.keyboard.press('ArrowRight');await check('01','1 / 20');
 await p.keyboard.press('ArrowLeft');await check('20','20 / 20');
 await p.keyboard.press('Escape');assert.equal(await saved(),before);assert.deepEqual(errors,[]);
 console.log(JSON.stringify({url:base,buttons:true,keyboard:true,wraparound:true,selectedOrder:true,allCandidates:true,mobile:true,downloadTracksImage:true,focusRestored:true,selectionsUnchanged:true,errors}));
}finally{await b.close()}
