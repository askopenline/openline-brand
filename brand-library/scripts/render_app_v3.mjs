import {chromium} from 'playwright';
import fs from 'node:fs';
const copy=JSON.parse(fs.readFileSync('public/app-v3/copy.json'));
const recommended=process.env.RECOMMENDED==='1';
if(recommended&&process.env.FRAME_ONLY!=='11')throw Error('Recommended rendering is restricted to candidate 11.');
if(recommended)copy.frames[10].detail=JSON.parse(fs.readFileSync('public/app-v3/recommended-copy.json')).planSelection.detail;
const installed='/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome';
const browser=await chromium.launch({channel:'chromium',executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||(fs.existsSync(installed)?installed:undefined),args:['--disable-dev-shm-usage']});
const captures=['countries','dashboard','destination','duration','esims','profile','profile','settings','account','collection','types','notifications',...copy.frames.slice(12).map(f=>f.capture)];
const report=[];
for(const [platform,width,height] of [['apple',1320,2868],['google',1080,1920]]){
 const dir=`public/app-v3/${recommended?'recommended/':''}${platform}`;fs.mkdirSync(dir,{recursive:true});
 for(let n=0;n<copy.frames.length;n++){
  if(process.env.FRAME_MIN&&n+1<Number(process.env.FRAME_MIN))continue;
  if(process.env.FRAME_ONLY&&n+1!==Number(process.env.FRAME_ONLY))continue;
  const page=await browser.newPage({viewport:{width,height}});
  await page.goto(`http://127.0.0.1:5173/render-submission.html?platform=${platform}&slide=${n%2}`,{waitUntil:'networkidle'});
  await page.waitForFunction(()=>window.artworkReady);
  await page.evaluate(({f,capture,n,platform,recommended})=>{
   document.querySelector('h1').replaceChildren(document.createTextNode(f.head[0]),document.createElement('br'),Object.assign(document.createElement('span'),{textContent:f.head[1]}));
   document.querySelector('.copy p').textContent=f.detail;
   document.querySelector('h1').style.color=n%2?'#171717':'#fff';
   document.querySelector('h1 span').style.color='inherit';
   const image=document.querySelector('.capture img');image.src='./app-v3/'+(recommended?'recommended/':'')+'screens/'+capture+'.png';
   image.alt=f.alt;
   const cap=document.querySelector('.capture');
   // Large, inclined UI with the established orange/cream rhythm.
   cap.style.top=platform==='apple'?'34%':'34%';
   cap.style.width=platform==='apple'?'79%':'73%';
   cap.style.left=platform==='apple'?'11%':'14%';
   document.querySelector('h1').style.fontSize=platform==='apple'?'117px':'90px';
   document.querySelector('.copy p').style.fontSize=platform==='apple'?'43px':'33px';
   if(n===6){cap.style.height=platform==='apple'?'1660px':'1160px';image.style.transform='translateY(-32%)';cap.style.width='83%';cap.style.left='9%'}
   if(n===11){cap.style.top='32%';cap.style.width=platform==='apple'?'79%':'65%';cap.style.left=platform==='apple'?'11%':'18%'}
  },{f:copy.frames[n],capture:captures[n],n,platform,recommended});
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(x=>x.decode()))});
  const qa=await page.evaluate(()=>{const b=s=>{const r=document.querySelector(s).getBoundingClientRect();return{top:r.top,bottom:r.bottom,width:r.width,height:r.height,left:r.left,right:r.right}};return{copy:b('.copy'),capture:b('.capture'),brand:b('.brand')}});
  if(qa.copy.bottom+14>qa.capture.top)throw Error(`Overlap ${platform} ${n+1}`);
  if(platform==='google'&&(qa.copy.width*qa.copy.height+qa.brand.width*qa.brand.height)/(width*height)>.2)throw Error('Text footprint >20%');
  await page.screenshot({path:`${dir}/${String(n+1).padStart(2,'0')}.png`});
  report.push({platform,frame:n+1,width,height,...qa});await page.close();
 }
}
const qaPath=`public/app-v3/${recommended?'recommended/':''}layout-qa.json`;
const previous=(process.env.FRAME_ONLY||process.env.FRAME_MIN)&&fs.existsSync(qaPath)?JSON.parse(fs.readFileSync(qaPath)):[];
const merged=[...previous.filter(x=>!report.some(r=>r.platform===x.platform&&r.frame===x.frame)),...report].sort((a,b)=>a.platform.localeCompare(b.platform)||a.frame-b.frame);
fs.writeFileSync(qaPath,JSON.stringify(merged,null,2));await browser.close();
console.log(`${report.length} V3 screenshot candidates rendered.`);
