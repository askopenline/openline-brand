import React,{useEffect,useRef,useState} from 'react';
import {Check,ChevronDown} from 'lucide-react';
export const ARCHIVES=[['final','Final draft (not confirmed)'],['v3','V3 · Selection workspace'],['v2','V2 · No pricing'],['v1','V1 · Original']];
export default function VersionNav({view,onViewChange,finalSaved=false}){
 const[open,setOpen]=useState(false),box=useRef(),archived=view!=='recommended',cur=ARCHIVES.find(a=>a[0]===view);
 useEffect(()=>{if(!open)return;const out=e=>{if(!box.current?.contains(e.target))setOpen(false)},key=e=>{if(e.key==='Escape'){setOpen(false);box.current?.querySelector('button')?.focus()}};document.addEventListener('pointerdown',out);document.addEventListener('keydown',key);return()=>{document.removeEventListener('pointerdown',out);document.removeEventListener('keydown',key)}},[open]);
 return <nav className="sw-editions" aria-label="Store editions">
  <button className="sw-current" aria-pressed={!archived} onClick={()=>{setOpen(false);onViewChange('recommended')}}>Current</button>
  <div className="sw-archives" ref={box}>
   <button aria-haspopup="menu" aria-expanded={open} aria-pressed={archived} onClick={()=>setOpen(o=>!o)}>{archived&&cur?'Archives · '+cur[1].split(' (')[0]:'Archives'}<ChevronDown size={15}/></button>
   {open&&<ul role="menu" aria-label="Archived versions">{ARCHIVES.map(([v,label])=><li key={v} role="none"><button role="menuitem" aria-current={view===v?'true':undefined} onClick={()=>{setOpen(false);onViewChange(v)}}>{label}{v==='final'&&finalSaved&&<small>Saved</small>}{view===v&&<Check size={15}/>}</button></li>)}</ul>}
  </div>
 </nav>;
}
