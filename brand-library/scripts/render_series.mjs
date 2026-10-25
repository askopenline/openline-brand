import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const root=process.cwd(),config=JSON.parse(fs.readFileSync('public/series.json'));
const browser=await chromium.launch({channel:'chromium',headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE}:{})});
const page=await browser.newPage({deviceScaleFactor:1}),report=[];
for(const series of config.series){
 const dir=path.join(root,'public/series',series.id);fs.mkdirSync(dir,{recursive:true});
 for(const [platform,width,height] of [['ios',1320,2868],['android',1080,1920]]){
  await page.setViewportSize({width,height});
  for(let i=0;i<6;i++){
   await page.goto(`http://localhost:5173/render-series.html?series=${series.id}&platform=${platform}&slide=${i}`,{waitUntil:'networkidle'});
   await page.waitForFunction(()=>window.artworkReady);
   await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));const bg=getComputedStyle(document.querySelector('.backdrop')).backgroundImage.match(/url\(["']?(.*?)["']?\)/)?.[1];if(bg){const i=new Image();i.src=bg;await i.decode()}});
   const bounds=await page.evaluate(()=>{const b=s=>{const r=document.querySelector(s).getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right}};return {copy:b('.copy'),phone:b('.phone'),head:b('h1'),footer:b('.foot')}});
   if(bounds.copy.bottom>bounds.phone.top-10)throw Error(`Copy/phone overlap ${series.id} ${platform} ${i}: ${JSON.stringify(bounds)}`);
   const file=`${platform}-${String(i+1).padStart(2,'0')}.png`;
   await page.screenshot({path:path.join(dir,file)});
   report.push({series:series.id,file,width,height,bounds,status:config.status});
  }
 }
 console.log(`Rendered ${series.id}`);
}
fs.writeFileSync('series-layout-qa.json',JSON.stringify(report,null,2));await browser.close();
