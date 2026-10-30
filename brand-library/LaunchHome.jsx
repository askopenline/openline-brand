import React,{useState,useEffect,useRef} from 'react';
import {ArrowRight,ArrowLeft,Download,X,Archive,Package,Smartphone,Store,ChevronRight} from 'lucide-react';
import {initialWorkspace} from './data';
import creative from './public/series.json';
import submissions from './public/submission.json';
import v2copy from './public/app-v2/copy.json';
import './launch-home.css';

const appViews=[['Destination','screen-countries.png'],['Purchase','screen-purchase.png'],['Setup','screen-profile.png'],['Your eSIMs','screen-esims.png'],['Connection','screen-dashboard.png'],['Choose a plan','screen-plans.png']];
const targets=[['iphone','iPhone','The app on iPhone',Smartphone],['android','Android','The app on Android',Smartphone],['app-store','App Store','The iPhone listing',Store],['google-play','Google Play','The Android listing',Store]];
const resources=[
 ['App icon','All approved formats: PNG, SVG, PDF, EPS, WebP, JPEG, ICO and ICNS.','openline-final-icon-all-formats.zip'],
 ['Native icon kits','Xcode assets and Android adaptive, legacy and monochrome resources.','openline-native-icons.zip'],
 ['Marketing screenshots','The approved six-image story for iPhone and Android.','openline-orange-series.zip'],
 ['Apple submission draft','Six iPhone images, conservative copy and remaining capture checks.','openline-apple-submission-draft.zip'],
 ['Google submission draft','Six Android images, restrained overlays and remaining capture checks.','openline-google-submission-draft.zip'],
 ['Editable artwork','Screenshot layouts, source images, fonts and render scripts.','openline-orange-series-sources.zip'],
 ['Listing copy','The current English App Store and Google Play drafts.','openline-store-copy.md'],
 ['Release handoff','Settings, checklist, metadata and review notes, in the complete bundle.','openline-all-resources.zip']
];
const icon=v=>v==='v2'?'./app-v2/icons/openline-icon-white-1024.png':'./assets/icon-43.5-light.png';
const v2views=['countries','settings','profile','esims','dashboard','plans'];
const screen=(n,p,v)=>v==='v2'?`./app-v2/screens/${v2views[n]}.png`:'./assets/'+(n===2&&p==='google'?'screen-profile-android.png':appViews[n][1]);
const artwork=(n,p,edition='marketing',v='v1',ext='webp')=>v==='v2'?`./app-v2/${edition}/${p}/${String(n+1).padStart(2,'0')}.${ext}`:edition==='submission'?`./submission/${p}/${String(n+1).padStart(2,'0')}.${ext}`:`./series/signal/${p==='apple'?'ios':'android'}-${String(n+1).padStart(2,'0')}.${ext}`;
const headline=(n,p,edition,v)=>v==='v2'?v2copy.frames[n].head.join(' '):edition==='submission'?submissions[p].frames[n].head.join(' '):creative.series[0].heads[n].join(' ');
function VersionSwitch({version,onChange}){return <div className="lh-version-switch" role="group" aria-label="Screenshot version"><button aria-pressed={version==='v1'} onClick={()=>onChange('v1')}>V1 · Original</button><button aria-pressed={version==='v2'} onClick={()=>onChange('v2')}>V2 · No pricing</button></div>}

function Listing({platform,mini=false,onEnlarge,edition='marketing',version='v1'}){
 const copy=version==='v2'?v2copy.metadata[platform]:edition==='submission'?submissions[platform].metadata:initialWorkspace.copy[platform];
 return <div className={`lh-listing ${platform} ${mini?'mini':''}`}>
  <div className="lh-storetitle">{platform==='apple'?'App Store':'Google Play'}</div>
  <div className="lh-app-title"><img src={icon(version)} alt="Openline app icon"/><div><h3>{copy.name}</h3><p>{platform==='apple'?copy.subtitle:copy.shortDescription}</p><span className="lh-install">{platform==='apple'?'GET':'Install'}</span></div></div>
  <div className="lh-store-shots" key={edition+version}>{Array.from({length:6},(_,n)=>mini?<img key={n} src={artwork(n,platform,edition,version)} alt="" loading="lazy"/>:<button key={n} onClick={()=>onEnlarge(n)} aria-label={`Enlarge ${platform==='apple'?'iPhone':'Android'} screenshot ${n+1}`}><img src={artwork(n,platform,edition,version)} alt={headline(n,platform,edition,version)}/></button>)}</div>
  {!mini&&<div className="lh-description"><h3>About Openline</h3><p>{copy.description}</p></div>}
 </div>
}
export default function LaunchHome(){
 const [open,setOpen]=useState(null),[frame,setFrame]=useState(4),[expanded,setExpanded]=useState(null),[edition,setEdition]=useState('marketing');
 const [version,setVersion]=useState(()=>new URLSearchParams(location.search).get('appVersion')==='v2'?'v2':'v1');
 const v2=version==='v2',views=v2?appViews.map((x,n)=>[n===1?'Settings':x[0],x[1]]):appViews;
 const iconZip=v2?'./app-v2/downloads/openline-v2-icons.zip':'./downloads/openline-final-icon-all-formats.zip';
 const bundle=v2?'./app-v2/downloads/openline-v2-complete.zip':'./downloads/openline-all-resources.zip';
 const activeResources=v2?[
  ['V2 app icon','Original mark enlarged 12.5% inside the unchanged white tile.','openline-v2-icons.zip'],
  ['V2 marketing screenshots','Six price-free images for each phone platform.','openline-v2-marketing.zip'],
  ['V2 Apple submission draft','Six iPhone images, listing copy and source notes.','openline-v2-apple.zip'],
  ['V2 Google submission draft','Six Android images, feature graphic, copy and source notes.','openline-v2-google.zip'],
  ['All V2 resources','Artwork, adapted app captures, icon variants and copy.','openline-v2-complete.zip']
 ]:resources;
 function changeVersion(v){setVersion(v);setExpanded(null);const u=new URL(location.href);u.searchParams.set('appVersion',v);history.replaceState(null,'',u.pathname+u.search+u.hash)}
 const dialog=useRef(),closer=useRef(),previousFocus=useRef();
 useEffect(()=>{const sync=()=>{const raw=location.hash.slice(1),id=raw.replace(/-submission$/,'');setOpen(targets.some(t=>t[0]===id)?id:null);setEdition(raw.endsWith('-submission')?'submission':'marketing');setExpanded(null)};sync();window.addEventListener('hashchange',sync);return()=>window.removeEventListener('hashchange',sync)},[]);
 function close(){history.replaceState(null,'','#home');setOpen(null);setExpanded(null)}
 useEffect(()=>{
  if(!open)return;
  previousFocus.current=document.activeElement;
  const old=document.body.style.overflow;document.body.style.overflow='hidden';closer.current?.focus();
  const key=e=>{
   if(e.key==='Escape'){if(expanded!==null)setExpanded(null);else close()}
   if(e.key==='Tab'){const controls=[...dialog.current.querySelectorAll('button,a[href]')];const first=controls[0],last=controls.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}
  };document.addEventListener('keydown',key);
  return()=>{document.body.style.overflow=old;document.removeEventListener('keydown',key);previousFocus.current?.focus()}
 },[open,expanded]);
 useEffect(()=>{const el=document.querySelector('.lh-phone-scroll');if(el)el.scrollTop=0},[frame,open]);
 const platform=open==='android'||open==='google-play'?'google':'apple';
 const device=open==='iphone'||open==='android';
 return <div className="lh-page">
  <header className="lh-header"><a href="#home" className="lh-wordmark"><img src="./assets/mark.png" alt=""/><strong>Openline</strong><span>Brand</span></a><nav aria-label="Studio views"><a href="#home" aria-current="page">Main</a><a href="#archive"><Archive size={15}/>Archive</a></nav></header>
  <main className="lh-main">
   <VersionSwitch version={version} onChange={changeVersion}/>
   <section className="lh-identity" aria-label="Openline app icon"><div className="lh-icon-display"><img src={icon(version)} alt={v2?'V2 Openline app icon':'Approved V1 Openline app icon'}/></div><div><span className="lh-kicker">THE MOBILE APP / {version.toUpperCase()}</span><h1>Openline, ready to explore.</h1><p>The icon. The app. The store presentation.<br/>Everything you need, in one place.</p><a className="lh-link" href={iconZip} download>Download the app icon <Download size={16}/></a></div></section>
   <section className="lh-previews" aria-labelledby="lh-preview-title"><div className="lh-section-heading"><h2 id="lh-preview-title">Preview</h2><p>Choose where to see it.</p></div>
    <div className="lh-preview-grid">{targets.map(([id,title,sub,Icon])=>{const p=id==='android'||id==='google-play'?'google':'apple',isDevice=id==='iphone'||id==='android';return <a className="lh-preview-card" href={'#'+id} key={id} aria-label={`Preview ${title}`}>
     <div className={'lh-preview-art '+(isDevice?'device '+p:'store')} aria-hidden="true">{isDevice?<div className={'lh-mini-phone '+p}><div className="lh-camera"/><img src={screen(4,p,version)} alt=""/></div>:<Listing platform={p} version={version} mini/>}</div>
     <div className="lh-card-caption"><Icon size={19}/><div><h3>{title}</h3><p>{sub}</p></div><ArrowRight size={19}/></div></a>})}</div>
   </section>
   <section className="lh-resources" aria-labelledby="lh-download-title"><div className="lh-section-heading"><div><h2 id="lh-download-title">Downloads / {version.toUpperCase()}</h2><p>Take everything, or just what you need.</p></div><a className="lh-primary" href={bundle} download><Package size={18}/>Download mobile launch resources</a></div><div className="lh-resource-grid">{activeResources.map(([name,detail,file])=><a className="lh-resource" href={(v2?'./app-v2/downloads/':'./downloads/')+file} download key={name}><div><h3>{name}</h3><p>{detail}</p></div><Download size={18}/></a>)}<a className="lh-resource" href="./index.html#/overview"><div><h3>Everything Openline.</h3><p>Find logo files, motion assets, campaign ideas, and product sources all in one place.</p></div><ArrowRight size={18}/></a></div></section>
  </main>
  <footer className="lh-footer"><span>Openline Brand</span><a href="#archive">Archive & working notes <ChevronRight size={14}/></a></footer>
  {open&&<div className="lh-modal-backdrop" onClick={e=>{if(e.target===e.currentTarget)close()}}><section className="lh-modal" role="dialog" aria-modal="true" aria-label={`${targets.find(t=>t[0]===open)[1]} preview`} ref={dialog}>
   <header><div><h2>{targets.find(t=>t[0]===open)[1]} / {version.toUpperCase()}</h2><span>{expanded!==null?`Screenshot ${expanded+1} of 6`:device?views[frame][0]:'Store listing preview'}</span></div><button ref={closer} onClick={close} aria-label="Close preview"><X size={23}/></button></header>
   <VersionSwitch version={version} onChange={changeVersion}/>
   {!device&&<div className="lh-editions"><div role="group" aria-label="Listing edition">{['marketing','submission'].map(e=><button key={e} aria-pressed={edition===e} onClick={()=>{setEdition(e);setExpanded(null);history.replaceState(null,'','#'+open+(e==='submission'?'-submission':''))}}>{e==='marketing'?'Marketing master':'Submission draft'}</button>)}</div>{edition==='submission'&&<p>Native captures and release checks pending. <a href={v2?`./app-v2/downloads/openline-v2-${platform}.zip`:`./downloads/openline-${platform}-submission-draft.zip`} download>Download {platform==='apple'?'Apple':'Google'} draft</a> · <a href={v2?'./app-v2/README.md':`./downloads/openline-${platform}-submission-readiness.md`}>Readiness notes</a></p>}</div>}
   <div className="lh-modal-content">{expanded!==null?<div className="lh-expanded"><button className="lh-link" onClick={()=>setExpanded(null)}><ArrowLeft size={16}/>Back to listing</button><img src={artwork(expanded,platform,edition,version,'png')} alt={headline(expanded,platform,edition,version)}/></div>:device?<div className={'lh-device '+platform}><div className="lh-camera"/><div className="lh-phone-scroll"><img src={screen(frame,platform,version)} alt={`${views[frame][0]} app view`}/></div></div>:<Listing platform={platform} edition={edition} version={version} onEnlarge={setExpanded}/>}</div>
   {device&&<div className="lh-device-controls"><button onClick={()=>setFrame((frame+5)%6)} aria-label="Previous app screen"><ArrowLeft size={18}/></button><div>{views.map(([name],n)=><button key={name} aria-label={`Show ${name}`} aria-pressed={frame===n} className={frame===n?'selected':''} onClick={()=>setFrame(n)}>{n+1}</button>)}</div><button onClick={()=>setFrame((frame+1)%6)} aria-label="Next app screen"><ArrowRight size={18}/></button></div>}
  </section></div>}
 </div>
}
