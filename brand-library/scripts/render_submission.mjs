import {chromium} from 'playwright';
import fs from 'node:fs';
const config=JSON.parse(fs.readFileSync('public/submission.json'));
const browser=await chromium.launch({channel:'chromium',headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE}:{})});
const page=await browser.newPage({deviceScaleFactor:1}),report=[];
for(const platform of ['apple','google']){
 const spec=config[platform],folder=`public/submission/${platform}`;fs.mkdirSync(folder,{recursive:true});
 await page.setViewportSize({width:spec.width,height:spec.height});
 for(let n=0;n<6;n++){
  await page.goto(`http://localhost:5173/render-submission.html?platform=${platform}&slide=${n}`,{waitUntil:'networkidle'});
  await page.waitForFunction(()=>window.artworkReady);
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(x=>x.decode()))});
  const bounds=await page.evaluate(()=>{
   const r=s=>{const b=document.querySelector(s).getBoundingClientRect();return {top:b.top,bottom:b.bottom,left:b.left,right:b.right,width:b.width,height:b.height}};
   return {copy:r('.copy'),brand:r('.brand'),capture:r('.capture'),headline:r('h1')};
  });
  if(bounds.copy.bottom+24>bounds.capture.top)throw Error(`Copy overlaps capture: ${platform} ${n+1}`);
  if(bounds.headline.right>spec.width||bounds.headline.left<0)throw Error('Headline outside artwork');
  const taglineHeightRatio=bounds.copy.height/spec.height;
  const overlayBoundingAreaRatio=(bounds.copy.width*bounds.copy.height+bounds.brand.width*bounds.brand.height)/(spec.width*spec.height);
  if(platform==='google'&&(taglineHeightRatio>.20||overlayBoundingAreaRatio>.20))throw Error(`Google overlay area too large: ${n+1}`);
  await page.screenshot({path:`${folder}/${String(n+1).padStart(2,'0')}.png`});
  report.push({platform,frame:n+1,width:spec.width,height:spec.height,taglineHeightRatio,overlayBoundingAreaRatio,bounds,status:config.status});
 }
}
await page.setViewportSize({width:1024,height:500});
await page.goto('http://localhost:5173/render-submission.html?platform=google&format=feature',{waitUntil:'networkidle'});
await page.waitForFunction(()=>window.artworkReady);
await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(x=>x.decode()))});
await page.screenshot({path:'public/submission/google/feature-graphic.png'});
fs.writeFileSync('submission-layout-qa.json',JSON.stringify(report,null,2));
await browser.close();console.log('Rendered 12 submission drafts; geometry and Google overlay area checks passed.');
