import {readdir,mkdir,link,copyFile,realpath} from 'node:fs/promises';
import {join} from 'node:path';
async function mirror(source,target){await mkdir(target,{recursive:true});for(const e of await readdir(source,{withFileTypes:true})){const s=join(source,e.name),d=join(target,e.name);if(e.isDirectory())await mirror(s,d);else if(e.isFile()||e.isSymbolicLink()){if(e.isSymbolicLink()){const resolved=await realpath(s);if(!resolved.startsWith('/dev/shm/openline-')||resolved.split('/').some(p=>['private','_private','receipts'].includes(p)))throw Error('Unexpected public asset symlink: '+s)}try{await link(s,d)}catch(error){if(error.code!=='EEXIST')await copyFile(s,d)}}}}
await mirror('public','dist');
console.log('Public library assets linked into dist.');
