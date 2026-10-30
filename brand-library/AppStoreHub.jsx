import React from 'react';
import {ArrowUpRight,Download} from 'lucide-react';

export default function AppStoreHub({library,onOpen,version='v1',onVersionChange}){
 if(!library)return null;
 const v2=version==='v2',studio='./studio.html?appVersion='+version,icon=library.icon||'./assets/apple-icon-1024.png';
 return <div className="app-store-hub">
  <section className="app-version-panel" aria-label="Screenshot version">
   <div><span className="eyebrow">Screenshot editions</span><h2>{v2?'V2. The app, without pricing.':'V1. The original screenshots.'}</h2><p>{v2?'A destination, setup and usage-led story. Original app resources adapted for review, with no monetary content in the artwork.':'Original artwork and icon, preserved unchanged. Previous resources and archives remain available below.'}</p></div>
   <div className="app-version-controls"><div className="series-switch" role="group" aria-label="Choose screenshot version"><button aria-pressed={!v2} onClick={()=>onVersionChange('v1')}>V1 · Original</button><button aria-pressed={v2} onClick={()=>onVersionChange('v2')}>V2 · No pricing</button></div><div className="app-version-icon"><img src={icon} alt={v2?'V2 app icon, mark enlarged 12.5%':'V1 original app icon'}/><div><strong>{v2?'Same icon. More presence.':'Original app icon.'}</strong><small>{v2?'Mark +12.5%; white tile unchanged.':'43.5% mark composition, unchanged.'}</small><a className="text-link" href={v2?'./app-v2/downloads/openline-v2-icons.zip':'./downloads/openline-final-icon-all-formats.zip'} download>Download icon <Download size={15}/></a></div></div></div>
  </section>
  <section className="store-preview-reminder">
   <div><span className="eyebrow">See the complete listing</span><h2>See Openline in the stores.</h2><p>Preview the screenshots, app icon and listing copy together. Switch between the marketing artwork and submission drafts in the studio.</p><small>Interactive previews, not published store listings.</small></div>
   <div className="store-preview-actions"><a className="button primary" href={studio+'#app-store'}>Preview App Store <ArrowUpRight size={18}/></a><a className="button secondary" href={studio+'#google-play'}>Preview Google Play <ArrowUpRight size={18}/></a><div><a href={studio+'#iphone'}>iPhone preview</a><a href={studio+'#android'}>Android preview</a></div></div>
  </section>
  <div className="app-listing-entries">{library.entries.map(e=><article key={e.id}>
   <div className="listing-entry-title"><img src={icon} alt="Openline app icon"/><div><span className="eyebrow">{e.title} / {version.toUpperCase()} submission draft</span><h2>{e.metadata.name}</h2><p>{e.metadata.subtitle||e.metadata.shortDescription}</p></div></div>
   <div className="actions"><a className="text-link" href={e.preview}>Open listing preview <ArrowUpRight size={16}/></a><a className="text-link" href={e.copy} download>Download listing copy <Download size={16}/></a></div>
   <details><summary>Read all listing fields</summary>{Object.entries(e.metadata).map(([k,v])=><div className="listing-field" key={k}><h3>{k.replace(/([A-Z])/g,' $1')}</h3><p>{v}</p></div>)}</details>
   <a className="text-link" href={e.bundle} download>Download submission package <Download size={16}/></a>
  </article>)}</div>
  <div className="context-note"><p>Artwork and listing copy remain review drafts. Replace design references with accurate release-build captures and validate claims before submission; these are not Apple or Google approvals.</p></div>
  {library.rows.map(row=><section className="app-screenshot-section" key={row.id}>
   <div className="section-heading"><div><span className="eyebrow">{row.status}</span><h2>{row.title}</h2></div><a className="text-link" href={row.bundle} download>Download set <Download size={16}/></a></div>
   <div className="app-screenshot-strip">{row.cards.map((a,i)=><button key={a.id} onClick={()=>onOpen(a)} aria-label={'Preview '+a.title}><img loading="lazy" src={a.preview} alt={a.title}/><span>{String(i+1).padStart(2,'0')} · {a.caption}</span></button>)}</div>
  </section>)}
  <div className="section-heading app-all-resources"><div><span className="eyebrow">Everything in one place</span><h2>Browse {version.toUpperCase()} app & store resources.</h2><p>{v2?'V2 files only. Switch to V1 for original and archived resources.':'Current files, source screens and preserved archive versions.'}</p></div>{v2?<a className="text-link" href="./app-v2/downloads/openline-v2-complete.zip" download>Download all V2 resources <Download size={16}/></a>:<a className="text-link" href="./studio.html#archive">Open the review workbench <ArrowUpRight size={16}/></a>}</div>
 </div>
}
