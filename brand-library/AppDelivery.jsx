import React,{useEffect,useMemo,useState} from 'react';
import {Check,ChevronRight,Copy,Download,ExternalLink,RotateCcw} from 'lucide-react';
import GRAPHICS from './public/app-v3/recommended/store-graphics.json';
import COPY from './public/app-v3/copy.json';
import RECOMMENDED from './public/app-v3/recommended-copy.json';
import {CHECK,G_DELIVERED,G_PROVIDE,G_BUILD} from './delivery-checklist.js';
import {CHECKED} from './submission-fields.js';
import {makeZip,saveBlob} from './selection-zip.js';
import {routeParams,routeURL} from './routing.js';
import './app-delivery.css';
const V='?v=4-0-0',KEY='openline-delivery-checklist-v2',STORE={apple:'App Store',google:'Google Play'};
const PROOFED='5 November 2026';
const frame=id=>({...COPY.frames.find(f=>f.id===id),...(RECOMMENDED.frames?.[id]||{})});
const slug=t=>t.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
const bytesOf=(s,k)=>k==='keywords'?new TextEncoder().encode(s).length:s.length;
const LIMIT={apple:{name:30,subtitle:30,promotional:170,keywords:100,description:4000},google:{name:30,shortDescription:80,description:4000}};
const LABEL={name:'App name',subtitle:'Subtitle',promotional:'Promotional text',keywords:'Keywords',shortDescription:'Short description',description:'Full description'};
const WHERE={apple:{name:'App Information > Name',subtitle:'App Information > Subtitle',promotional:'Distribution > version page > Promotional Text',keywords:'Distribution > version page > Keywords',description:'Distribution > version page > Description'},
 google:{name:'Grow users > Store presence > Main store listing > App name',shortDescription:'Main store listing > Short description',description:'Main store listing > Full description'}};
const CONSOLE={apple:'App Store Connect > your app',google:'Play Console > your app'};
const CATEGORY={
 apple:{where:'App Store Connect > your app > App Information > Category',primary:'Travel',other:'Secondary category: Utilities (optional)',steps:['Open App Information for the app.','Set Primary Category to Travel.','Optionally set Secondary Category to Utilities. Leave it empty if unsure.','Do not add a subcategory: they exist only for Games and Stickers.'],why:'Apple defines Travel as apps that assist with any aspect of travel, such as planning, purchasing or tracking. Airalo and Saily are both listed under Travel.',avoid:[['Business','Apple lists VoIP telephony here. Openline sells mobile data.'],['Social Networking','For apps that connect people by text, voice, photo or video.'],['Utilities as primary','It hides the travel story from people browsing Travel.']],sources:[['Apple categories','https://developer.apple.com/app-store/categories/'],['App information','https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/']]},
 google:{where:'Play Console > your app > Grow users > Store presence > Store settings > App category',primary:'Travel and Local',other:'Application type: App (not Game). Up to five tags.',steps:['Open Store settings for the app.','In App category, set the application type to App.','Choose Travel and Local. Google allows one category and no subcategories.','Open Manage tags and pick up to five tags that are obviously relevant to a traveler.'],why:'Google lists trip booking and trip management tools under Travel and Local. Holafly, the closest eSIM competitor on Google Play, is listed there.',avoid:[['Communications','For messaging, chat, dialers and call management.'],['Tools','Reserved for tools for Android devices.'],['Telecommunications','Google Play has no category with this name.']],sources:[['Categories and tags','https://support.google.com/googleplay/android-developer/answer/9859673']]}};
const GROUPS=[G_DELIVERED,G_PROVIDE,G_BUILD];
const VERIFY=RECOMMENDED.verification.map(v=>({group:G_BUILD,id:'verify-'+v.id,label:v.title,provide:v.detail}));
const ALL={apple:[...CHECK.apple,...VERIFY],google:[...CHECK.google,...VERIFY]};
const loadDone=()=>{try{const o=JSON.parse(localStorage.getItem(KEY));return o&&typeof o==='object'?o:{}}catch{return{}}};
const kb=n=>n>=1e6?(n/1e6).toFixed(1)+' MB':Math.round(n/1e3)+' KB';
const role=f=>/light/.test(f)?'Alternate (light)':'Primary';
const base=f=>f.split('/').pop();
const copyOf=(store)=>RECOMMENDED[store];
const listingMd=store=>`# ${STORE[store]} listing text\n\nPaste into ${CONSOLE[store]}.\n\n${Object.keys(LIMIT[store]).map(k=>`## ${LABEL[k]}\n\nConsole: ${WHERE[store][k]}\nLimit: ${LIMIT[store][k]} ${k==='keywords'?'bytes':'characters'} (used: ${bytesOf(copyOf(store)[k],k)})\n\n${copyOf(store)[k]}\n`).join('\n')}`;
const HANDOFF={
 apple:{who:'Owner or Admin of the App Store Connect account (Account Holder for first submission).',before:['Signed release build uploaded and processed in App Store Connect (TestFlight shows it as ready).','Build number matches the version you are submitting.','Demo or review access (if needed) entered in App Review Information in the private console, never in this package.'],steps:['Unzip the package and read README.md.','Open the app version page. Paste listing.md fields: name, subtitle, promotional text, keywords, description, What\'s New, URLs.','Set the category from category.md (App Information).','Upload graphics/ and the product page assets, then screenshots/1320x2868 and screenshots/1206x2622 in file order.','Attach the processed build to the version.','Answer age rating, App Privacy, export compliance and pricing from checklist.md.','Tick every item in the checklist on /app until it reads complete.','Choose manual or automatic release, then Add for Review and Submit.'],after:['Watch for App Review messages and reply from the console.','Next update: change listing.json only if text changed, keep the numbered screenshot order.']},
 google:{who:'Play Console user with Release manager and Store listing permissions.',before:['Signed Android App Bundle built for release (com.openline.esim).','Release uploaded to a track (internal testing first, then production).','App content declarations (Data safety, content rating, ads, target audience) reviewed against the real build.'],steps:['Unzip the package and read README.md.','Open Grow users > Store presence > Main store listing. Paste listing.md fields: app name, short description (80 characters max), full description.','Set category and tags from category.md under Store settings.','Upload the icon and feature graphic from graphics/, then phone screenshots in file order. Paste screenshot-alt-text.md for each.','Complete App content and Data safety from checklist.md.','Tick every item in the checklist on /app until it reads complete.','Create the production release, add release notes, review and roll out.'],after:['The public listing updates only after Google review finishes.','Feature graphic changes show only after the Play Console upload is published.']}
};
const handoffMd=store=>{const h=HANDOFF[store];return `# ${STORE[store]} engineer handoff\n\nWho: ${h.who}\n\nBefore you start:\n${h.before.map(x=>`- ${x}`).join('\n')}\n\nPublish:\n${h.steps.map((x,i)=>`${i+1}. ${x}`).join('\n')}\n\nAfter submitting:\n${h.after.map(x=>`- ${x}`).join('\n')}\n\nNever put reviewer credentials or secrets in this package.\n`};
const categoryMd=store=>{const c=CATEGORY[store];return `# ${STORE[store]} category\n\nWhere: ${c.where}\n\nSelect: ${c.primary}\n${c.other}\n\n${c.steps.map((s,i)=>`${i+1}. ${s}`).join('\n')}\n\nWhy: ${c.why}\n\nAvoid:\n${c.avoid.map(a=>`- ${a[0]}: ${a[1]}`).join('\n')}\n`};
const items=store=>ALL[store];
const checklistMd=(store,done)=>`# ${STORE[store]} submission checklist\n\nStore requirements last checked ${CHECKED}. Values in [BRACKETS] are owner-only facts to fill in.\n\n${GROUPS.map(g=>{const L=items(store).filter(f=>f.group===g);return L.length?`## ${g}\n\n${L.map(f=>`- [${done[store+':'+f.id]?'x':' '}] ${f.label}${f.provide?`\n  Provide: ${f.provide}`:''}${f.where?`\n  Where: ${f.where}`:''}`).join('\n')}\n`:''}).join('\n')}`;
const altMd=()=>`# Google Play screenshot alt text\n\nUp to 140 characters each, in upload order.\n\n${RECOMMENDED.selection.google.map((id,i)=>`${i+1}. ${frame(id).title} (${frame(id).alt.length}/140): ${frame(id).alt}`).join('\n')}\n`;
export default function AppDelivery(){
 const[store,setStore]=useState(()=>routeParams().get('store')==='google'?'google':'apple'),[done,setDone]=useState(loadDone),[openOnly,setOpenOnly]=useState(false),[toast,setToast]=useState(''),[busy,setBusy]=useState(false),[expanded,setExpanded]=useState({});
 useEffect(()=>{try{localStorage.setItem(KEY,JSON.stringify(done))}catch{}},[done]);
 useEffect(()=>{if(!toast)return;const t=setTimeout(()=>setToast(''),2600);return()=>clearTimeout(t)},[toast]);
 function pick(s){setStore(s);const p=routeParams();p.set('store',s);history.replaceState(null,'',routeURL('app',p))}
 async function copy(text,what){try{await navigator.clipboard.writeText(text);setToast(what+' copied')}catch{setToast('Copy is blocked in this browser')}}
 const list=useMemo(()=>items(store),[store]),count=s=>{const L=items(s);return[L.filter(f=>done[s+':'+f.id]).length,L.length]};
 const[doneN,totalN]=count(store),text=copyOf(store);
 const sel=RECOMMENDED.selection[store],assets=GRAPHICS[store],gfx=assets.filter(a=>!/screens/.test(a.id)),shots=assets.filter(a=>/screens/.test(a.id));
 const toggle=id=>setDone(d=>{const k=store+':'+id,n={...d};if(n[k])delete n[k];else n[k]=true;return n});
 async function fetchAll(entries){const out=[];for(const[name,url]of entries){const r=await fetch(url);if(!r.ok)throw Error('A file could not be fetched: '+name);out.push({name,data:await r.arrayBuffer()})}return out}
 async function pack(){
  setBusy(true);try{
   const e=[];const files=[];
   for(const a of gfx)for(const f of a.files)files.push([`graphics/${role(f.file)==='Primary'?'':'alternates/'}${base(f.file)}`,'./'+f.file+V]);
   const sets=assets.filter(a=>/screens/.test(a.id));
   for(const a of sets){const dir=`screenshots/${a.files[0].width}x${a.files[0].height}`;a.files.forEach((f,i)=>files.push([`${dir}/${String(i+1).padStart(2,'0')}-${slug(frame(sel[i]).title)}.png`,'./'+f.file+V]))}
   const got=await fetchAll(files);
   const readme=`# Openline ${STORE[store]} delivery (v4, proofread ${PROOFED})\n\nUpload order:\n1. listing.md: paste each field into ${CONSOLE[store]}.\n2. category.md: select the category.\n3. graphics/ and screenshots/: upload each size into its own slot. Files in alternates/ are optional.\n4. checklist.md: complete every declaration and console item.\n5. Upload the signed build and submit.\n\nStore requirements last checked ${CHECKED}. Sizes validated by the delivery page. This is a creative handoff, not store approval.\n`;
   const extra=[{name:'README.md',data:readme},{name:'HANDOFF.md',data:handoffMd(store)},{name:'listing.md',data:listingMd(store)},{name:'listing.json',data:JSON.stringify(text,null,2)},{name:'category.md',data:categoryMd(store)},{name:'checklist.md',data:checklistMd(store,done)},...(store==='google'?[{name:'screenshot-alt-text.md',data:altMd()}]:[])];
   saveBlob(await makeZip([...extra,...got]),`openline-${store==='apple'?'app-store':'google-play'}-delivery-v4.zip`);setToast('Package ready');
  }catch(err){setToast(err.message)}finally{setBusy(false)}
 }
 const shown=openOnly?list.filter(f=>!done[store+':'+f.id]):list;
 const open=list.filter(f=>!done[store+':'+f.id]);
 return <div className="dl">
  <div className="page-heading"><div><span className="eyebrow">Openline / App & store</span><h1>App & store.</h1><p>Final delivery v4. Everything an engineer needs to publish on the App Store and Google Play.</p></div></div>
  <div className="dl-status"><span className="dl-stamp"><Check size={14}/> Proofread and validated {PROOFED}</span><span>Store requirements last checked {CHECKED}</span><span>Not a store approval. Final submission still depends on the signed build.</span></div>
  <div className="dl-bar"><div className="dl-switch" role="group" aria-label="Store">{['apple','google'].map(s=><button key={s} aria-pressed={store===s} onClick={()=>pick(s)}>{STORE[s]}<small>{count(s)[0]}/{count(s)[1]}</small></button>)}</div>
   <nav aria-label="Sections">{[['dl-listing','Listing'],['dl-category','Category'],['dl-graphics','Graphics'],['dl-shots','Screenshots'],['dl-checklist','Checklist'],['dl-download','Download']].map(([id,l])=><a key={id} href={'#'+id} onClick={e=>{e.preventDefault();document.getElementById(id)?.scrollIntoView({behavior:'smooth'})}}>{l}</a>)}</nav></div>
  <section className="dl-steps" aria-label="How to publish"><h2>Publish {STORE[store]} in six steps.</h2><ol>
   {[['Paste the listing text','dl-listing'],['Select the category','dl-category'],['Upload icon and graphics','dl-graphics'],['Upload screenshots in order','dl-shots'],['Complete the checklist','dl-checklist'],['Upload the signed build and submit','dl-checklist']].map(([l,id],i)=><li key={l}><a href={'#'+id} onClick={e=>{e.preventDefault();document.getElementById(id)?.scrollIntoView({behavior:'smooth'})}}><b>{i+1}</b>{l}<ChevronRight size={14}/></a></li>)}</ol></section>

  <details className="dl-optional dl-handoff"><summary>Engineer handoff for {STORE[store]}</summary><p className="dl-spec"><strong>Who:</strong> {HANDOFF[store].who}</p><h3>Before you start</h3><ul>{HANDOFF[store].before.map(x=><li key={x}>{x}</li>)}</ul><h3>Publish</h3><ol>{HANDOFF[store].steps.map(x=><li key={x}>{x}</li>)}</ol><h3>After submitting</h3><ul>{HANDOFF[store].after.map(x=><li key={x}>{x}</li>)}</ul><button className="dl-copy" onClick={()=>copy(handoffMd(store),'Handoff guide')}><Copy size={14}/> Copy guide</button></details>

  <section id="dl-listing" className="dl-section"><div className="dl-head"><div><span className="eyebrow">1 / Listing text</span><h2>Paste into {CONSOLE[store]}.</h2></div><button className="button secondary" onClick={()=>copy(listingMd(store),'Listing text')}>Copy all text <Copy size={15}/></button></div>
   <div className="dl-fields">{Object.keys(LIMIT[store]).map(k=>{const v=text[k],n=bytesOf(v,k),max=LIMIT[store][k],long=v.length>420;return <article key={k} className="dl-field"><header><div><h3>{LABEL[k]}</h3><small>{WHERE[store][k]}</small></div><span className={'dl-count'+(n>max?' is-over':'')}>{n} / {max} {k==='keywords'?'bytes':'characters'}</span></header>
    <pre className={long&&!expanded[k]?'is-clamped':''}>{v}</pre><div className="dl-field-actions"><button className="dl-copy" onClick={()=>copy(v,LABEL[k])} aria-label={'Copy '+LABEL[k]}><Copy size={14}/> Copy</button>{long&&<button className="dl-link" onClick={()=>setExpanded(x=>({...x,[k]:!x[k]}))}>{expanded[k]?'Show less':'Show all'}</button>}</div></article>})}</div>
  </section>

  <section id="dl-category" className="dl-section"><div className="dl-head"><div><span className="eyebrow">2 / Category</span><h2>Select {CATEGORY[store].primary}.</h2></div></div>
   <div className="dl-category"><div><p className="dl-pick"><strong>{CATEGORY[store].primary}</strong><small>{CATEGORY[store].other}</small></p><p className="dl-where">{CATEGORY[store].where}</p><ol>{CATEGORY[store].steps.map(s=><li key={s}>{s}</li>)}</ol></div>
    <div><p>{CATEGORY[store].why}</p><h3>Do not select</h3><ul>{CATEGORY[store].avoid.map(a=><li key={a[0]}><strong>{a[0]}.</strong> {a[1]}</li>)}</ul><p className="dl-src">{CATEGORY[store].sources.map(s=><a key={s[1]} href={s[1]} target="_blank" rel="noreferrer">{s[0]} <ExternalLink size={12}/></a>)}<span>Neither store has a Telecommunications category.</span></p></div></div></section>

  <section id="dl-graphics" className="dl-section"><div className="dl-head"><div><span className="eyebrow">3 / Icon and graphics</span><h2>Upload each file to its slot.</h2></div><a className="dl-link" href={GRAPHICS.sources[store]} target="_blank" rel="noreferrer">Official specification <ExternalLink size={13}/></a></div>
   <div className="dl-gfx">{gfx.map(a=><article key={a.id} className="dl-asset" data-asset={a.id}><header><div><span className="dl-req">{a.requirement}</span><h3>{a.title}</h3></div><span className={'dl-chip '+(a.ok?'ok':'warn')}>{a.ok?'Validated':'Check'}</span></header>
    <div className="dl-tiles">{a.files.map(f=><figure key={f.file} className={f.width/f.height>1.4?'is-wide':''}><a href={'./'+f.file+V} target="_blank" rel="noreferrer"><img loading="lazy" src={'./'+f.file+V} alt={`${a.title}, ${role(f.file)}`}/></a><figcaption><b>{role(f.file)}</b><span>{base(f.file)} · {f.width} × {f.height} · {kb(f.bytes)}</span><a className="dl-copy" href={'./'+f.file+V} download={base(f.file)}><Download size={14}/> Download</a></figcaption></figure>)}</div>
    <p className="dl-spec">{a.spec}</p>{a.note&&<p className="dl-spec">{a.note}</p>}</article>)}</div>
   <details className="dl-optional"><summary>Not included: optional or conditional assets</summary><ul>{GRAPHICS.optional[store].map(o=><li key={o.id}><strong>{o.title}</strong> <span>{o.requirement}</span><p>{o.note}</p></li>)}</ul></details></section>

  <section id="dl-shots" className="dl-section"><div className="dl-head"><div><span className="eyebrow">4 / Screenshots</span><h2>Upload in this order.</h2><p>{sel.length} screenshots. Upload each size into its own slot.</p></div></div>
   {shots.map(a=><div key={a.id} className="dl-shotset" data-asset={a.id}><h3>{a.title}</h3><p className="dl-spec">{a.spec}</p><ol className="dl-shots">{a.files.map((f,i)=>{const fr=frame(sel[i]);return <li key={f.file}><a href={'./'+f.file+V} target="_blank" rel="noreferrer"><img loading="lazy" src={'./'+f.file+V} alt={fr.alt}/></a><b>{String(i+1).padStart(2,'0')}</b><span>{fr.title}</span><a className="dl-copy" href={'./'+f.file+V} download={`${String(i+1).padStart(2,'0')}-${slug(fr.title)}.png`}><Download size={13}/> PNG</a></li>})}</ol></div>)}
   {store==='google'&&<div className="dl-alt"><div className="dl-head"><h3>Alt text for each screenshot</h3><button className="dl-copy" onClick={()=>copy(altMd(),'Alt text')}><Copy size={14}/> Copy all</button></div><ol>{sel.map(id=><li key={id}><span>{frame(id).alt}</span><small>{frame(id).alt.length}/140</small><button className="dl-copy" onClick={()=>copy(frame(id).alt,'Alt text')} aria-label={'Copy alt text for '+frame(id).title}><Copy size={13}/></button></li>)}</ol></div>}
  </section>

  <section id="dl-checklist" className="dl-section"><div className="dl-head"><div><span className="eyebrow">5 / Before you submit</span><h2>{STORE[store]} checklist.</h2><p>{doneN} of {totalN} complete. Copy the text under each item and fill in the [BRACKETS] only the owner knows. Ticks are saved in this browser only.</p></div>
   <div className="dl-actions"><label className="dl-toggle"><input type="checkbox" checked={openOnly} onChange={e=>setOpenOnly(e.target.checked)}/> Show open items only</label><button className="dl-copy" onClick={()=>copy(checklistMd(store,done),'Checklist status')}><Copy size={14}/> Copy status</button><button className="dl-copy" onClick={()=>setDone(d=>Object.fromEntries(Object.entries(d).filter(([k])=>!k.startsWith(store+':'))))}><RotateCcw size={14}/> Reset</button></div></div>
   <div className="dl-progress" role="progressbar" aria-valuemin="0" aria-valuemax={totalN} aria-valuenow={doneN} aria-label={STORE[store]+' checklist progress'}><i style={{width:(totalN?doneN/totalN*100:0)+'%'}}/></div>
   {open.length===0&&<p className="dl-allclear"><Check size={16}/> Every item is complete. Upload the signed build and submit.</p>}
   {GROUPS.map(g=>{const L=shown.filter(f=>f.group===g);if(!L.length)return null;const gd=items(store).filter(f=>f.group===g&&done[store+':'+f.id]).length,gt=items(store).filter(f=>f.group===g).length;return <div key={g} className="dl-group"><h3>{g}<small>{gd}/{gt}</small></h3><ul>{L.map(f=>{const on=Boolean(done[store+':'+f.id]);return <li key={f.id} className={on?'is-done':''}><label><input type="checkbox" checked={on} onChange={()=>toggle(f.id)} aria-label={f.label}/><span className="dl-box" aria-hidden="true">{on&&<Check size={13}/>}</span></label><div><h4>{f.label}</h4>{f.provide&&<div className="dl-provide"><p>{f.provide}</p><button className="dl-copy" onClick={()=>copy(f.provide,'Text')} aria-label={'Copy text for '+f.label}><Copy size={13}/> Copy</button></div>}<p className="dl-links">{f.where&&<span>{f.where}</span>}{f.jump&&<a href={'#'+f.jump} onClick={e=>{e.preventDefault();document.getElementById(f.jump)?.scrollIntoView({behavior:'smooth'})}}>Show it above</a>}{f.src&&<a href={f.src} target="_blank" rel="noreferrer">Official guidance <ExternalLink size={12}/></a>}</p></div></li>})}</ul></div>})}
  </section>

  <section id="dl-download" className="dl-section dl-download"><div><span className="eyebrow">6 / Package</span><h2>Take it all in one ZIP.</h2><p>Listing text, category, checklist, icon, graphics and screenshots for {STORE[store]}, named in upload order{store==='google'?', with alt text':''}.</p></div><button className="button primary" disabled={busy} onClick={pack}>{busy?'Preparing…':`Download ${STORE[store]} package`} <Download size={16}/></button></section>
  {toast&&<div className="dl-toast" role="status">{toast}</div>}
 </div>
}
