import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const base=process.env.ARTWORK_BASE_URL||'http://localhost:5173';
const config=JSON.parse(fs.readFileSync(path.join(root,'public/artwork.json')));
// Safety: this renderer makes review artwork only. A native release requires a
// separate verification of captures, copy and account declarations.
if(config.status!=='design-reference-not-native-capture')throw Error('Native release export requires a new verified capture audit.');
const browser=await chromium.launch({channel:'chromium',headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE}:{})});
const page=await browser.newPage({deviceScaleFactor:1});
const report=[];
for(const [platform,width,height] of [['ios',1320,2868],['android',1080,1920],['feature',1024,500]]){
 await page.setViewportSize({width,height});
 for(let i=0;i<(platform==='feature'?1:config.slides.length);i++){
  await page.goto(`${base}/render.html?platform=${platform}&slide=${i}`,{waitUntil:'networkidle'});
  await page.waitForFunction(()=>window.artworkReady);
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()))});
  const bounds=await page.evaluate(()=>{
   const box=s=>{const b=document.querySelector(s).getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height,bottom:b.bottom,right:b.right}};
   return {headline:box('h1'),deck:box('.deck'),phone:box('.phone'),footer:box('.foot'),copy:box('.copy')};
  });
  if(bounds.headline.bottom>bounds.deck.y||bounds.deck.bottom>bounds.phone.y&&platform!=='feature')throw Error('Artwork text overlap');
  if(bounds.phone.right>width||bounds.headline.right>width)throw Error('Artwork overflow');
  const name=platform==='feature'?'google-feature.png':`${platform}-${String(i+1).padStart(2,'0')}.png`;
  await page.screenshot({path:path.join(root,'public/assets',name)});
  report.push({file:name,width,height,bounds});
 }
}
fs.writeFileSync(path.join(root,'artwork-layout-qa.json'),JSON.stringify(report,null,2));
await browser.close();
console.log('Rendered and checked 12 review screenshots and feature graphic.');
