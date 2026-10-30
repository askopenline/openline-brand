// Dependency-free ZIP STORE writer. Images are already compressed.
const enc=new TextEncoder(),table=Uint32Array.from({length:256},(_,n)=>{for(let k=0;k<8;k++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0});
function crc(a){let c=0xffffffff;for(const b of a)c=table[(c^b)&255]^(c>>>8);return(c^0xffffffff)>>>0}
export async function makeZip(entries){
 const parts=[],central=[];let offset=0;
 for(const e of entries){
  const name=enc.encode(e.name),bytes=typeof e.data==='string'?enc.encode(e.data):new Uint8Array(e.data);
  const head=new Uint8Array(30+name.length),v=new DataView(head.buffer),checksum=crc(bytes);
  v.setUint32(0,0x04034b50,true);v.setUint16(4,20,true);v.setUint16(6,0x800,true);v.setUint16(12,0x21,true);v.setUint32(14,checksum,true);v.setUint32(18,bytes.length,true);v.setUint32(22,bytes.length,true);v.setUint16(26,name.length,true);head.set(name,30);
  const cd=new Uint8Array(46+name.length),c=new DataView(cd.buffer);
  c.setUint32(0,0x02014b50,true);c.setUint16(4,20,true);c.setUint16(6,20,true);c.setUint16(8,0x800,true);c.setUint16(14,0x21,true);c.setUint32(16,checksum,true);c.setUint32(20,bytes.length,true);c.setUint32(24,bytes.length,true);c.setUint16(28,name.length,true);c.setUint32(42,offset,true);cd.set(name,46);
  parts.push(head,bytes);central.push(cd);offset+=head.length+bytes.length;
 }
 const end=new Uint8Array(22),v=new DataView(end.buffer),cdSize=central.reduce((n,a)=>n+a.length,0);
 v.setUint32(0,0x06054b50,true);v.setUint16(8,entries.length,true);v.setUint16(10,entries.length,true);v.setUint32(12,cdSize,true);v.setUint32(16,offset,true);
 return new Blob([...parts,...central,end],{type:'application/zip'});
}
export function saveBlob(blob,name){const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),30000)}
