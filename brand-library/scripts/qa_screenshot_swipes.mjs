import {chromium} from 'playwright';
import assert from 'node:assert/strict';
const base=process.env.QA_URL||'http://127.0.0.1:5174/';
const browser=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome',args:['--disable-dev-shm-usage']});
try{
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:2});
 const page=await context.newPage(),cdp=await context.newCDPSession(page),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'#/app?version=recommended',{waitUntil:'networkidle'});
 const saved=()=>page.evaluate(()=>localStorage.getItem('openline-store-workspace-v3')),before=await saved();
 const check=async(id)=>{await page.waitForFunction(id=>document.querySelector('.sw-image-stage img')?.getAttribute('src').includes('/'+id+'.png'),id);assert((await page.locator('.sw-full-art a').getAttribute('href')).includes('/'+id+'.png'))};
 const gesture=async(dx,dy=0,cancel=false,multi=false)=>{
  await page.waitForFunction(()=>{const img=document.querySelector('.sw-image-stage img');return img?.complete&&img.naturalWidth>0});
  const b=await page.locator('.sw-image-stage img').boundingBox(),x=b.x+b.width/2,y=b.y+b.height/2;
  const points=(a,z)=>[{x:a,y:z,id:1},...(multi?[{x:a+45,y:z+45,id:2}]:[])];
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:points(x,y)});
  for(let i=1;i<=5;i++)await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:points(x+dx*i/5,y+dy*i/5)});
  await cdp.send('Input.dispatchTouchEvent',{type:cancel?'touchCancel':'touchEnd',touchPoints:[]});
 };
 for(const [button,last] of [['Preview App Store','18'],['Preview Google Play','18']]){
  await page.getByRole('button',{name:button,exact:true}).click();
  await page.getByRole('button',{name:'Preview selected screenshot 1',exact:true}).click();
  await check('01');
  assert((await page.locator('.sw-image-stage img').evaluate(e=>getComputedStyle(e).touchAction)).includes('pinch-zoom'));
  await gesture(-110);await check('02');
  await gesture(-110);await check('11');
  await gesture(110);await check('02');
  await gesture(15);await check('02');
  await gesture(0,-90);await check('02');
  await gesture(-100,0,true);await check('02');
  await gesture(-60,0,false,true);await check('02');
  await gesture(110);await check('01');
  await gesture(110);await check(last);
  await gesture(-110);await check('01');
  await page.getByRole('button',{name:'Next screenshot',exact:true}).click();await check('02');
  await page.getByRole('button',{name:'Close preview',exact:true}).click();
 }
 assert.equal(await saved(),before);assert.deepEqual(errors,[]);
 console.log(JSON.stringify({url:base,apple:true,google:true,nativeTouchEvents:true,directionsAndOrder:true,wraparound:true,shortDragIgnored:true,verticalIgnored:true,cancelIgnored:true,multitouchIgnored:true,pinchZoomAllowed:true,buttons:true,downloadTracksImage:true,selectionsUnchanged:true,errors}));
}finally{await browser.close()}
