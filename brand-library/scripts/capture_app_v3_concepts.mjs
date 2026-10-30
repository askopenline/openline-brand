// Imagined review concepts, not native app captures or implemented-feature claims.
import {chromium} from 'playwright';
import fs from 'node:fs';
const copy=JSON.parse(fs.readFileSync('public/app-v3/copy.json'));
if(new Set(copy.frames.filter(f=>f.concept).map(f=>f.capture)).size!==8)throw Error('Concept capture filenames must be unique');
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const browser=await chromium.launch({executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome',args:['--disable-dev-shm-usage']});
const report=JSON.parse(fs.readFileSync('public/app-v3/capture-provenance.json')).filter(x=>!x.concept);
for(const f of copy.frames.filter(f=>f.concept)){
 const phone=f.phone, id=Number(f.id);
 const page=await browser.newPage({viewport:{width:340,height:700},deviceScaleFactor:4});
 const flags=id===13?['🇵🇹','🇫🇷','🇩🇪','🇮🇹']:id===20?['EN','FR','PT','ES']:[];
 const rows=phone.rows.map((r,i)=>`<article class="row ${id===19?'line-card':''}"><span class="symbol">${id===15?'<i class="signal"><b></b><b></b><b></b><b></b></i>':id===17?(i===0?'✓':i+1):id===18?['?','⌁','○','?'][i]:flags[i]||['◉','◷','▦','○'][i]}</span><div><strong>${escape(r.title)}</strong><small>${escape(r.detail)}</small></div><span class="trailing">${id===15||id===20?(i===0?'●':'○'):id===17?(i===0?'Done':''):id===19?'<i class="toggle"></i>':'›'}</span></article>`).join('');
 const metric=phone.metric?`<section class="metric ${id===16?'ring-metric':''}"><div><small>${escape(phone.metricLabel)}</small><strong>${escape(phone.metric)}</strong></div>${id===16?'<div class="ring"><span>68%</span></div>':'<div class="progress"><i></i></div>'}</section>`:'';
 const bars=id===16?'<div class="chart" aria-label="Illustrated data activity"><i style="height:26%"></i><i style="height:44%"></i><i style="height:37%"></i><i style="height:63%"></i><i style="height:49%"></i><i style="height:78%"></i><i style="height:56%"></i></div>':'';
 await page.setContent(`<!doctype html><html><head><style>
 @font-face{font-family:Inter;src:url('http://127.0.0.1:5173/fonts/inter-latin-600-normal.woff2');font-weight:600}
 @font-face{font-family:Inter;src:url('http://127.0.0.1:5173/fonts/inter-latin-800-normal.woff2');font-weight:800}
 *{box-sizing:border-box}body{margin:0;background:#f7f8fa;color:#171717;font-family:Inter,sans-serif;font-weight:600;width:340px;height:700px;overflow:hidden}
 .status{display:flex;justify-content:space-between;padding:20px 22px 0;font-size:12px}.status em{font-style:normal;letter-spacing:2px}
 main{padding:24px 20px 80px}h1{font-size:27px;letter-spacing:-1px;line-height:1.1;margin:0 0 9px;font-weight:800}p{font-size:12px;line-height:1.5;color:#727984;margin:0 0 14px}
 .badge{display:inline-block;background:#fff0e4;color:#c64b0b;padding:7px 11px;border-radius:20px;font-size:10px;margin:0 0 13px}
 .section{font-size:10px;color:#929aa5;text-transform:uppercase;letter-spacing:1px;margin:8px 0 10px}
 .row{display:flex;align-items:center;gap:11px;background:#fff;border:1px solid #edf0f2;border-radius:17px;padding:15px 12px;margin-bottom:10px;min-height:67px;box-shadow:0 2px 3px #17223106}.row>div{min-width:0;flex:1}.row strong{display:block;font-size:13px;line-height:1.25}.row small{font-size:10px;color:#929aa5;display:block;line-height:1.4;margin-top:4px}
 .symbol{font-size:21px;width:30px;flex-shrink:0;text-align:center}.trailing{color:#cdd2d8;font-size:19px;flex-shrink:0}
 .metric{border-radius:22px;padding:21px;background:#ff6418;color:white;margin:2px 0 16px}.metric small{display:block;font-size:11px;opacity:.9}.metric strong{display:block;font-size:34px;letter-spacing:-1px;margin:6px 0}.metric span{font-size:11px}.progress{height:6px;border-radius:9px;background:#ffffff55;margin-top:17px}.progress i{display:block;height:100%;width:68%;background:#fff;border-radius:9px}
 .ring-metric{display:flex;align-items:center;justify-content:space-between}.ring{width:84px;height:84px;border-radius:50%;background:conic-gradient(white 68%,#ffffff45 0);display:grid;place-items:center}.ring span{width:68px;height:68px;border-radius:50%;background:#ff6418;display:grid;place-items:center;font-size:19px}
 .chart{height:78px;display:flex;align-items:end;gap:14px;padding:0 16px 8px;margin-bottom:10px}.chart i{background:#ffccb0;flex:1;border-radius:4px 4px 0 0}.chart i:nth-last-child(2){background:#ff6418}
 .signal{display:flex;align-items:end;gap:3px;height:23px}.signal b{width:4px;background:#ff6418;border-radius:2px;height:25%}.signal b:nth-child(2){height:50%}.signal b:nth-child(3){height:75%}.signal b:nth-child(4){height:100%}
 .toggle{display:block;width:29px;height:17px;border-radius:10px;background:#ff6418;padding:2px}.toggle:after{content:'';display:block;width:13px;height:13px;border-radius:50%;background:#fff;margin-left:auto}
 .line-card{padding:23px 12px}.concept-17 .symbol{background:#fff0e4;border-radius:50%;color:#ff6418;width:29px;height:29px;display:grid;place-items:center;font-size:14px}.concept-17 .row{min-height:90px}.concept-17 .trailing{font-size:9px;color:#ff6418}
 .concept-20 .symbol{font-size:11px;background:#fff0e4;color:#d34e0c;padding:9px 0;border-radius:9px}
 .concept-15 .row:first-of-type,.concept-20 .row:first-of-type{border-color:#ff6418}.concept-16 .row{min-height:52px;padding:10px 12px;margin-bottom:7px}
 .concept-14 .row{padding:10px 12px;min-height:58px;margin-bottom:7px}.concept-14 .metric{padding:17px}
 .concept-16 .badge{display:none}.concept-16 .chart{height:50px}.concept-16 .metric{padding:15px}
 footer{position:absolute;bottom:0;left:0;right:0;height:71px;background:#fff;border-top:1px solid #edf0f2;display:flex;align-items:center;justify-content:space-around;color:#9aa2ad;font-size:10px}footer span{display:grid;gap:6px;text-align:center}footer b{font-size:20px;font-weight:600}footer .active{color:#ff6418}
 </style></head><body class="concept-${id}"><div class="status"><span>9:41</span><em>▂▄▆ ▰</em></div><main><h1>${escape(phone.title)}</h1><p>${escape(phone.subtitle)}</p><div class="badge">${escape(phone.badge)}</div>${metric}${bars}<div class="section">${escape(phone.section)}</div>${rows}</main><footer><span class="${id===14||id===16?'active':''}"><b>⌂</b>Home</span><span class="${id===13||id===15?'active':''}"><b>◎</b>Plans</span><span class="${id===17||id===19?'active':''}"><b>▣</b>eSIMs</span><span class="${id===18||id===20?'active':''}"><b>○</b>Me</span></footer></body></html>`);
 await page.evaluate(()=>document.fonts.ready);
 const bottom=await page.locator('.row').last().evaluate(el=>el.getBoundingClientRect().bottom);
 if(bottom>629)throw Error('Concept content overlaps navigation: '+f.id+' '+bottom);
 const text=await page.locator('body').innerText();
 await page.screenshot({path:`public/app-v3/screens/${f.capture}.png`});
 report.push({id:f.capture,source:'Imagined Openline UI concept '+f.id,text,width:1360,height:2800,concept:true,status:'Proposed UI, not an implemented feature or native release capture'});
 await page.close();
}
fs.writeFileSync('public/app-v3/capture-provenance.json',JSON.stringify(report,null,2));await browser.close();
console.log('Eight clearly classified UI concepts captured.');
