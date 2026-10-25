import React,{useState,useEffect,useRef} from 'react';
import {ArrowRight,ArrowLeft,Download,X,Archive,Package,Smartphone,Store,ChevronRight} from 'lucide-react';
import {initialWorkspace} from './data';
import creative from './public/series.json';
import submissions from './public/submission.json';
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
const icon='./assets/icon-43.5-light.png';
const screen=(n,p)=>'./assets/'+(n===2&&p==='google'?'screen-profile-android.png':appViews[n][1]);
const artwork=(n,p,edition='marketing')=>edition==='submission'?`./submission/${p}/${String(n+1).padStart(2,'0')}.webp`:`./series/signal/${p==='apple'?'ios':'android'}-${String(n+1).padStart(2,'0')}.webp`;
const headline=(n,p,edition)=>edition==='submission'?submissions[p].frames[n].head.join(' '):creative.series[0].heads[n].join(' ');

function Listing({platform,mini=false,onEnlarge,edition='marketing'}){
 const copy=edition==='submission'?submissions[platform].metadata:initialWorkspace.copy[platform];
 return <div className={`lh-listing ${platform} ${mini?'mini':''}`}>
  <div className="lh-storetitle">{platform==='apple'?'App Store':'Google Play'}</div>
  <div className="lh-app-title"><img src={icon} alt="Openline app icon"/><div><h3>{copy.name}</h3><p>{platform==='apple'?copy.subtitle:copy.shortDescription}</p><span className="lh-install">{platform==='apple'?'GET':'Install'}</span></div></div>
  <div className="lh-store-shots" key={edition}>{Array.from({length:6},(_,n)=>mini?<img key={n} src={artwork(n,platform,edition)} alt="" loading="lazy"/>:<button key={n} onClick={()=>onEnlarge(n)} aria-label={`Enlarge ${platform==='apple'?'iPhone':'Android'} screenshot ${n+1}`}><img src={artwork(n,platform,edition)} alt={headline(n,platform,edition)}/></button>)}</div>
  {!mini&&<div className="lh-description"><h3>About Openline</h3><p>{copy.description}</p></div>}
 </div>
}
export default function LaunchHome(){
 const [open,setOpen]=useState(null),[frame,setFrame]=useState(4),[expanded,setExpanded]=useState(null),[edition,setEdition]=useState('marketing');
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
   <section className="lh-identity" aria-label="Openline app icon"><div className="lh-icon-display"><img src={icon} alt="Approved Openline app icon"/></div><div><span className="lh-kicker">THE MOBILE APP</span><h1>Openline, ready to explore.</h1><p>The icon. The app. The store presentation.<br/>Everything you need, in one place.</p><a className="lh-link" href="./downloads/openline-final-icon-all-formats.zip" download>Download the app icon <Download size={16}/></a></div></section>
   <section className="lh-previews" aria-labelledby="lh-preview-title"><div className="lh-section-heading"><h2 id="lh-preview-title">Preview</h2><p>Choose where to see it.</p></div>
    <div className="lh-preview-grid">{targets.map(([id,title,sub,Icon])=>{const p=id==='android'||id==='google-play'?'google':'apple',isDevice=id==='iphone'||id==='android';return <a className="lh-preview-card" href={'#'+id} key={id} aria-label={`Preview ${title}`}>
     <div className={'lh-preview-art '+(isDevice?'device '+p:'store')} aria-hidden="true">{isDevice?<div className={'lh-mini-phone '+p}><div className="lh-camera"/><img src={screen(4,p)} alt=""/></div>:<Listing platform={p} mini/>}</div>
     <div className="lh-card-caption"><Icon size={19}/><div><h3>{title}</h3><p>{sub}</p></div><ArrowRight size={19}/></div></a>})}</div>
   </section>
   <section className="lh-resources" aria-labelledby="lh-download-title"><div className="lh-section-heading"><div><h2 id="lh-download-title">Downloads</h2><p>Take everything, or just what you need.</p></div><a className="lh-primary" href="./downloads/openline-all-resources.zip" download><Package size={18}/>Download mobile launch resources</a></div><div className="lh-resource-grid">{resources.map(([name,detail,file])=><a className="lh-resource" href={'./downloads/'+file} download key={name}><div><h3>{name}</h3><p>{detail}</p></div><Download size={18}/></a>)}<a className="lh-resource" href="./index.html#/overview"><div><h3>Everything Openline.</h3><p>Find logo files, motion assets, campaign ideas, and product sources all in one place.</p></div><ArrowRight size={18}/></a></div></section>
  </main>
  <footer className="lh-footer"><span>Openline Brand</span><a href="#archive">Archive & working notes <ChevronRight size={14}/></a></footer>
  {open&&<div className="lh-modal-backdrop" onClick={e=>{if(e.target===e.currentTarget)close()}}><section className="lh-modal" role="dialog" aria-modal="true" aria-label={`${targets.find(t=>t[0]===open)[1]} preview`} ref={dialog}>
   <header><div><h2>{targets.find(t=>t[0]===open)[1]}</h2><span>{expanded!==null?`Screenshot ${expanded+1} of 6`:device?appViews[frame][0]:'Store listing preview'}</span></div><button ref={closer} onClick={close} aria-label="Close preview"><X size={23}/></button></header>
   {!device&&<div className="lh-editions"><div role="group" aria-label="Listing edition">{['marketing','submission'].map(e=><button key={e} aria-pressed={edition===e} onClick={()=>{setEdition(e);setExpanded(null);history.replaceState(null,'','#'+open+(e==='submission'?'-submission':''))}}>{e==='marketing'?'Marketing master':'Submission draft'}</button>)}</div>{edition==='submission'&&<p>Native captures and release checks pending. <a href={`./downloads/openline-${platform}-submission-draft.zip`} download>Download {platform==='apple'?'Apple':'Google'} draft</a> · <a href={`./downloads/openline-${platform}-submission-readiness.md`}>Readiness notes</a></p>}</div>}
   <div className="lh-modal-content">{expanded!==null?<div className="lh-expanded"><button className="lh-link" onClick={()=>setExpanded(null)}><ArrowLeft size={16}/>Back to listing</button><img src={edition==='submission'?`./submission/${platform}/${String(expanded+1).padStart(2,'0')}.png`:`./series/signal/${platform==='apple'?'ios':'android'}-${String(expanded+1).padStart(2,'0')}.png`} alt={headline(expanded,platform,edition)}/></div>:device?<div className={'lh-device '+platform}><div className="lh-camera"/><div className="lh-phone-scroll"><img src={screen(frame,platform)} alt={`${appViews[frame][0]} app view`}/></div></div>:<Listing platform={platform} edition={edition} onEnlarge={setExpanded}/>}</div>
   {device&&<div className="lh-device-controls"><button onClick={()=>setFrame((frame+5)%6)} aria-label="Previous app screen"><ArrowLeft size={18}/></button><div>{appViews.map(([name],n)=><button key={name} aria-label={`Show ${name}`} aria-pressed={frame===n} className={frame===n?'selected':''} onClick={()=>setFrame(n)}>{n+1}</button>)}</div><button onClick={()=>setFrame((frame+1)%6)} aria-label="Next app screen"><ArrowRight size={18}/></button></div>}
  </section></div>}
 </div>
}
