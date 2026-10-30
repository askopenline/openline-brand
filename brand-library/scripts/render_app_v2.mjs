import {chromium} from 'playwright';
import fs from 'node:fs';
const copy=JSON.parse(fs.readFileSync('public/app-v2/copy.json'));
const browser=await chromium.launch({executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome',headless:true,args:['--disable-dev-shm-usage']});
let page;
const captures=['countries','settings','profile','esims','dashboard','plans'];
const report=[];
for(const edition of ['marketing','submission']){
 for(const [platform,width,height] of [['apple',1320,2868],['google',1080,1920]]){
  const dir=`public/app-v2/${edition}/${platform}`;fs.mkdirSync(dir,{recursive:true});
  page=await browser.newPage({deviceScaleFactor:1});
  await page.setViewportSize({width,height});
  for(let n=0;n<6;n++){
   // Reuse the established art direction, typefaces and layout without rewriting V1.
   await page.goto(`http://localhost:5173/render-submission.html?platform=${platform}&slide=${n}`,{waitUntil:'networkidle'});
   await page.waitForFunction(()=>window.artworkReady);
   await page.evaluate(({frame,capture,n,edition})=>{
    document.querySelector('h1').replaceChildren(document.createTextNode(frame.head[0]),document.createElement('br'),Object.assign(document.createElement('span'),{textContent:frame.head[1]}));
    document.querySelector('.copy p').textContent=frame.detail;
    document.querySelector('.capture img').src='./app-v2/screens/'+capture+'.png';
    // Preserve the angled treatment for all slides on both platforms.
    if(edition==='marketing')document.querySelector('.capture').style.border='5px solid #252525';
   },{frame:copy.frames[n],capture:captures[n],n,edition});
   await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(x=>x.decode()))});
   const qa=await page.evaluate(()=>{
    const b=s=>{const r=document.querySelector(s).getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width,height:r.height}};
    return {copy:b('.copy'),capture:b('.capture'),head:b('h1'),brand:b('.brand'),text:document.querySelector('.copy').innerText};
   });
   if(qa.copy.bottom+18>qa.capture.top)throw Error('Overlap '+edition+platform+n);
   if(qa.head.left<0||qa.head.right>width)throw Error('Headline bounds');
   if(platform==='google'&&(qa.copy.width*qa.copy.height+qa.brand.width*qa.brand.height)/(width*height)>.2)throw Error('Google overlay footprint');
   await page.screenshot({path:`${dir}/${String(n+1).padStart(2,'0')}.png`});
   report.push({edition,platform,frame:n+1,width,height,...qa});
  }
  await page.close();
 }
}
page=await browser.newPage({deviceScaleFactor:1});
await page.setViewportSize({width:1024,height:500});
await page.goto('http://localhost:5173/render-submission.html?platform=google&format=feature',{waitUntil:'networkidle'});
await page.waitForFunction(()=>window.artworkReady);
await page.evaluate(()=>{document.querySelector('.capture img').src='./app-v2/icons/openline-icon-white-1024.png'});
await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(x=>x.decode()))});
await page.screenshot({path:'public/app-v2/submission/google/feature-graphic.png'});
fs.writeFileSync('public/app-v2/layout-qa.json',JSON.stringify(report,null,2));
await browser.close();console.log('Rendered 24 price-free V2 screenshots and Google feature graphic.');
