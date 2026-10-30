// Integrate an approved editorial result without regenerating media or changing Final.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const app=path.resolve(import.meta.dirname,'..'),pub=path.join(app,'public');
const repo=path.resolve(app,'../openline-brand-assets/brand-library');
const [input,version]=process.argv.slice(2);
assert(input&&/^\d+\.\d+\.\d+$/.test(version),'Provide reviewed result JSON and version.');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const write=(p,x)=>fs.writeFileSync(p,JSON.stringify(x,null,2)+'\n');
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const inventory=read(path.join(repo,'PUBLIC-ASSETS.json'));
const old=new Map(inventory.files.map(x=>[x.path,x]));
const protectedNames=['app-v3/copy.json','app-v3/screens/types.png','app-v3/apple/11.png','app-v3/google/11.png','app-v3/apple-1206/11.png'];
for(const n of protectedNames)assert.equal(hash(path.join(pub,n)),old.get(n).sha256,n);
const copyPath=path.join(pub,'app-v3/recommended-copy.json'),copy=read(copyPath),result=read(input);
const preserved=JSON.stringify({planSelection:copy.planSelection,verification:copy.verification});
copy.apple.description=result.appleDescription;copy.apple.promotional=result.applePromotional;
copy.google.description=result.googleDescription;copy.google.shortDescription=result.googleShortDescription;
assert(copy.apple.promotional.length<=170&&copy.google.shortDescription.length<=80);
for(const p of ['apple','google']){
 assert(copy[p].description.length<=4000);
 assert(!/[$€£¥₹]/.test(copy[p].description));
}
assert.equal(JSON.stringify({planSelection:copy.planSelection,verification:copy.verification}),preserved);
write(copyPath,copy);
fs.writeFileSync(path.join(pub,'app-v3/recommended-copy-audit.md'),result.auditMarkdown+'\n');
for(const n of ['package.json','package-lock.json']){
 const p=path.join(app,n),x=read(p);x.version=version;
 if(x.packages)x.packages[''].version=version;
 write(p,x);
}
const catalogPath=path.join(pub,'library/catalog.json'),catalog=read(catalogPath);
catalog.version=version;catalog.appLibraryV3.recommendedSelection.copyAudit='./app-v3/recommended-copy-audit.md';write(catalogPath,catalog);
const changed=['library/catalog.json','app-v3/README.md','app-v3/recommended-copy.json','app-v3/recommended-copy-audit.md'];
for(const n of changed){
 const p=path.join(pub,n),d=path.join(app,'dist',n);fs.mkdirSync(path.dirname(d),{recursive:true});
 if(!fs.existsSync(d)||fs.statSync(p).ino!==fs.statSync(d).ino)fs.copyFileSync(p,d);
 old.set(n,{path:n,bytes:fs.statSync(p).size,sha256:hash(p),url:'https://brand.openline.com/'+n});
}
inventory.version=version;inventory.files=[...old.values()];inventory.total_bytes=inventory.files.reduce((a,b)=>a+b.bytes,0);write(path.join(repo,'PUBLIC-ASSETS.json'),inventory);
const state=path.resolve(app,'../openline-fly-deployment/listing-v'+version.replaceAll('.','-'));fs.mkdirSync(state,{recursive:true});
write(path.join(state,'public-files.json'),changed);
write(path.join(state,'protected-originals.json'),Object.fromEntries(protectedNames.map(n=>[n,old.get(n).sha256])));
for(const n of ['AppSubmissionWorkbench.jsx','FLOWS.md','package.json','package-lock.json','scripts/qa_recommended_content.mjs','tools/package-store-copy.mjs','public/app-v3/README.md','public/app-v3/recommended-copy.json','public/app-v3/recommended-copy-audit.md']){
 const d=path.join(repo,n);fs.mkdirSync(path.dirname(d),{recursive:true});fs.copyFileSync(path.join(app,n),d);
}
console.log(JSON.stringify({version,files:changed,copy:Object.fromEntries(['apple','google'].map(p=>[p,{words:copy[p].description.split(/\s+/).length,characters:copy[p].description.length}]))}));
