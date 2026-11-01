// Draws one bold status-icon set and applies it to every Recommended screen. Originals stay untouched.
import {chromium} from 'playwright';
import fs from 'node:fs';
const svg=fs.readFileSync('scripts/status-icons.svg','utf8');
const b=await chromium.launch({executablePath:'/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'});
const p=await b.newPage({viewport:{width:120,height:30},deviceScaleFactor:4});
await p.setContent(`<body style="margin:0;background:transparent"><div id=i style="display:inline-flex;align-items:center;gap:6px;padding:0">${svg}</div></body>`);
await p.locator('#i').screenshot({path:'public/app-v3/recommended/status-icons.png',omitBackground:true});
await b.close();
