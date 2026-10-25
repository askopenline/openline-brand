import React from 'react';
import {Download,CheckCircle2} from 'lucide-react';
const files=[
 ['PNG · white · 1024','openline-icon-white-1024.png'],
 ['PNG · transparent · 1024','openline-icon-transparent-1024.png'],
 ['PNG · white · 4096','openline-icon-white-4096.png'],
 ['SVG · white','openline-icon-white.svg'],
 ['SVG · transparent','openline-icon-transparent.svg'],
 ['PDF · vector','openline-icon-white.pdf'],
 ['EPS · vector','openline-icon-white.eps'],
 ['JPEG · white','openline-icon-white-1024.jpg'],
 ['WebP · lossless','openline-icon-white-1024.webp'],
 ['ICO · multi-size','openline-icon.ico'],
 ['ICNS · macOS','openline-icon.icns']
];
export default function FinalIconDownloads(){
 return <section className="panel final-formats">
  <div className="panel-top"><div><span className="eyebrow">APPROVED 7 OCTOBER 2026</span><h2>The final icon. Every practical format.</h2></div><CheckCircle2 size={24}/></div>
  <p>43.5% mark width. Original geometry. White square unchanged. PNGs from 16 to 4096px, real vector paths, and complete iOS / Android integration resources.</p>
  <a className="btn primary" href="./downloads/openline-final-icon-all-formats.zip" download><Download size={16}/> Download final icon · all formats</a>
  <div className="format-grid">{files.map(([label,file])=><a key={file} className="btn small" href={'./downloads/final-icon/'+file} download><Download size={14}/>{label}</a>)}</div>
  <div className="inline-actions"><a className="text-btn" href="./downloads/openline-native-icons.zip" download>iOS + Android native kit <Download size={15}/></a><a className="text-btn" href="./downloads/final-icon/manifest.json" download>Checksums & file manifest <Download size={15}/></a></div>
  <p className="format-note">Use opaque PNGs for store listings. SVG/PDF are editable in Illustrator; no native .ai file is claimed. Icon Composer source layers are included, not a compiled .icon document. ICNS/ICO are convenience formats, not iOS/Android submission assets. Native device validation is still required.</p>
 </section>
}
