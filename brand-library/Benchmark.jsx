import React from 'react';
import {ArrowUpRight,Download,CheckCircle2,Info} from 'lucide-react';

const competitors=[
 {name:'Saily',color:'#f2ee00',ink:'#141517',apple:'https://apps.apple.com/us/app/saily-esim-data-for-travel/id6475045151',google:'https://play.google.com/store/apps/details?id=com.saily.android&hl=en_US',lead:'One eSIM. Concrete benefits.',copy:'Its listing opens with roaming bills and airport Wi-Fi, then explains setup, plan choices and support.',visual:'Blue backgrounds, yellow text highlights, a phone held in a hand and enlarged plan callouts. “One eSIM” and “Unlimited Plans” are immediately legible.',lesson:'Make the first image answer “what is this for?” and let each following image explain one decision.'},
 {name:'Airalo',color:'#d7f0a2',ink:'#254422',apple:'https://apps.apple.com/us/app/airalo-esim-for-travel-data/id1475911720',google:'https://play.google.com/store/apps/details?id=com.mobillium.airalo&hl=en_US',lead:'Breadth, emotion and proof.',copy:'“Stay connected anywhere” is backed in the listing by destination breadth, plan categories, setup steps and FAQs.',visual:'The inspected set uses lime backgrounds, large phones, travel illustrations and a dragon across the first cards. Coverage and “30M” social proof feature early.',lesson:'Build a deliberate sequence. Openline should demonstrate product clarity, not borrow unverified scale claims.'},
 {name:'Holafly',color:'#ee8a95',ink:'#7e143c',apple:'https://apps.apple.com/us/app/holafly-esim-unlimited-data/id1629600786',google:'https://play.google.com/store/apps/details?id=com.holafly.holafly&hl=en_US',lead:'A strong promise, repeated.',copy:'Unlimited data, trip-duration choices, guided installation and support dominate its descriptions.',visual:'Coral/pink backgrounds, burgundy headline blocks and large devices. The first cards stress connection, one eSIM, a backup plan and pricing clarity.',lesson:'Be explicit about what a plan contains. Do not promote unlimited data or fixed promises until Openline’s actual SKU terms support them.'}
];

export default function Benchmark(){
 return <>
  <div className="note"><Info size={18}/><p><strong>Observed, not guessed.</strong> US English App Store text and first four visible screenshot cards were inspected on 6 October 2026; Google Play text was checked separately. Publisher claims are not independently verified. No conversion, ranking or A/B-test result is implied.</p></div>
  <section className="panel benchmark-summary"><div><span className="eyebrow">OUR POSITIONING DIRECTION</span><h2>Travel data. Made clear.</h2><p>Let others compete on louder promises. Openline can lead with a clear choice: where you are going, what your plan includes, and where to find your eSIM details.</p></div><a className="btn" href="./downloads/competitor-review.md" download><Download size={16}/> Full review</a></section>
  <div className="benchmark-grid">{competitors.map(c=><article className="panel competitor" key={c.name}>
   <div className="competitor-name" style={{background:c.color,color:c.ink}}><strong>{c.name}</strong><span>Observed positioning</span></div>
   <h2>{c.lead}</h2><h3>Text</h3><p>{c.copy}</p><h3>Graphics</h3><p>{c.visual}</p>
   <div className="competitor-links"><a className="source" href={c.apple} target="_blank" rel="noreferrer">App Store evidence <ArrowUpRight size={14}/></a><a className="source" href={c.google} target="_blank" rel="noreferrer">Google Play text <ArrowUpRight size={14}/></a></div>
   <div className="lesson"><span className="eyebrow">TAKEAWAY FOR OPENLINE</span><p>{c.lesson}</p></div>
  </article>)}</div>
  <div className="section-heading"><div><h2>What changed in the studio</h2><p>Airy revision 03 artwork. Final 43.5% icon approved. Not measured conversion gains.</p></div><span className="badge green">Implemented</span></div>
  <div className="benchmark-changes">{[
   ['A lighter, benefit-led opening','“Go places. Stay connected.” pairs a short headline with an explicit Travel eSIM label and one clear product view.'],
   ['A decision-led sequence','Destination → plan comparison → eSIM details → data view → eSIM library → account. The old settings screen with unverified network/security claims is removed.'],
   ['More air, not more clutter','Complete upright phones, generous margins and shorter headlines. Phone widths are now 840px on iPhone artboards and 576px on Android, instead of oversized crops.'],
   ['Copy that answers first-time questions','The title includes “eSIM & Data”; descriptions explain compatibility, setup information, separate plan purchases and home-carrier charges.'],
   ['A final app icon','Paul approved 43.5% mark coverage on 7 October 2026. Final downloads include genuine vector paths, raster formats and native resources, separate from archived size experiments.'],
   ['No invented proof','No imported ratings, customer counts, destination totals, unlimited guarantees, instant-setup times or round-the-clock support claims.']
  ].map(([title,body])=><article className="panel" key={title}><CheckCircle2 size={19}/><div><h3>{title}</h3><p>{body}</p></div></article>)}</div>
  <div className="section-heading"><div><h2>Our first impression, before and after</h2><p>The same identity, with a clearer product story and more legible detail.</p></div></div>
  <div className="two-col artwork-comparison"><figure className="panel"><figcaption><h3>Revision 01</h3><p>General travel message. Smaller full-screen dashboard.</p></figcaption><img src="./assets/ios-01-r01.png" alt="Earlier Openline first screenshot: Your next trip. Connected." loading="lazy"/></figure><figure className="panel"><figcaption><h3>Revision 03</h3><p>One message, more breathing room and a complete product view.</p></figcaption><img src="./assets/ios-01.png" alt="Openline screenshot: Go places. Stay connected." loading="lazy"/></figure></div>
  <div className="two-col"><section className="panel"><h2>What still needs evidence</h2><p>Replace React-reference UI with native captures. Verify usage reporting, installation steps, plan conditions and support. A help/compatibility screen would be a stronger sixth store image than account preferences once it exists in the release.</p></section><section className="panel"><h2>What to test, not assume</h2><p>Once traffic is sufficient, compare this clarity-led first image against a destination-led alternative. Change one element at a time and judge install conversion alongside activation or purchase quality, not just clicks.</p></section></div>
 </>
}
