import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {initialWorkspace,fieldSpecs,suggestedSettings} from '../data.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const out=path.join(root,'public/downloads');
let md='# Openline store listing drafts\n\nEnglish (US), audited October 7, 2026. Verify every statement against the native release build before submission. No coverage, speed or timing claims are assumed.\n\n';
for(const p of ['apple','google']){
 md+=`## ${p==='apple'?'Apple App Store':'Google Play'}\n\n`;
 for(const [key,label,max,unit] of fieldSpecs[p]){
  const text=initialWorkspace.copy[p][key],len=unit==='bytes'?Buffer.byteLength(text):Array.from(text).length;
  if(len>max)throw Error(`${p} ${key} exceeds limit`);
  md+=`### ${label}\n\n${text}\n\n${len} / ${max} ${unit||'characters'}\n\n`;
 }
}
md+='\nOfficial metadata references:\nhttps://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/\nhttps://support.google.com/googleplay/android-developer/answer/9859152?hl=en\n';
fs.writeFileSync(path.join(out,'openline-store-copy.md'),md);
fs.writeFileSync(path.join(out,'openline-launch-workspace.json'),JSON.stringify(initialWorkspace,null,2));
fs.writeFileSync(path.join(out,'openline-store-settings.md'),'# Openline store settings proposal\n\nNo console settings have been changed. Confirm all unknowns against the actual build and account.\n\n'+suggestedSettings.map(s=>`## ${s.field}\n\n${s.value}\n\nStatus: ${s.status}. ${s.detail}\n`).join('\n')+'\nSee store-requirements.md for official source links and policy detail.\n');
fs.writeFileSync(path.join(out,'openline-release-checklist.md'),'# Openline release checklist\n\nThe final flat icon visual choice is approved. Native integration, capture replacement and release evidence remain separate. Nothing here is store approval.\n\n'+initialWorkspace.tasks.map(t=>`- [${t.status==='done'?'x':' '}] ${t.title} (${t.platform}; ${t.requirement}; ${t.status})\n  Owner: ${t.owner}\n  ${t.detail}\n`).join('\n'));
console.log('Copy limits validated and handoff text generated.');
