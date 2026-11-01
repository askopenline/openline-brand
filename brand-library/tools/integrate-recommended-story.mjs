// Integrates reviewed copy and recorded owner decisions; does not modify Final or V3 sources.
import fs from 'node:fs';
const input=process.argv[2];if(!input)throw Error('Provide reviewed editorial JSON.');
const draft=JSON.parse(fs.readFileSync(input)),path='public/app-v3/recommended-copy.json',rec=JSON.parse(fs.readFileSync(path));
for(const platform of ['apple','google']){
 let text=draft[platform+'Description'];
 text=text.replace(', so you can stay connected on your own terms while keeping your regular SIM active for calls and texts.','. Keep maps, messages and travel apps within reach.')
 .replace(/Openline offers two plan types:.*?Getting started is straightforward\./s,'Choose Unlimited usage or Fixed usage plans, where available. Fixed usage provides a set data allowance. Review the plan’s validity, fair-use and applicable usage terms, and check remaining data in the app where applicable.\n\nGetting started is straightforward.')
 .replaceAll('manual activation details','manual installation details').replaceAll(' — ','. ')
 .replace('confirm data roaming on your home SIM is off, ','')
 .replace('SMS. note','SMS. Note')
 .replace("Browse, use maps, and keep your travel apps running without relying on your home operator's roaming rates. ",'');
 if(text.length>4000||/[$€£¥₹₽]|\bcheaper\b|\bnever caught short\b|high-data allowance tier/i.test(text))throw Error('Copy validation');
 rec[platform].description=text;
}
rec.apple.promotional=draft.applePromotional.replace('Avoid roaming surprises','Avoid data-roaming surprises');rec.google.shortDescription=draft.googleShortDescription.replace('Avoid roaming surprises','Avoid data-roaming surprises');
rec.selection={apple:['01','02','11','04','19','10','06','18'],google:['01','02','11','04','19','10','18']};
rec.frames=draft.frames;
rec.frames['19'].detail='A clear checklist to help avoid unexpected data-roaming charges.';
const phone=rec.frames['19'].phone;
phone.rows=[
 {title:'Install your Openline eSIM',detail:'Scan the QR code or enter installation details.'},
 {title:'Home-SIM data roaming OFF',detail:'Turn it off before you travel.'},
 {title:'Select Openline for data',detail:'Use Openline as your mobile data line.'},
 {title:'Openline data roaming ON',detail:'At your destination, follow the setup guide.'},
 {title:'Automatic data switching OFF',detail:'Turn it off where your device supports it.'}
];
phone.note='On dual-SIM phones, keep your home SIM for calls/SMS if needed. Operator charges may apply.';
for(const [id,capture]of [['04','duration-calendar'],['19','setup-checklist'],['18','live-chat']]){
 Object.assign(rec.frames[id],{id,capture,concept:true});
 if(rec.frames[id].head.some(s=>s.length>24)||rec.frames[id].detail.length>85)throw Error('Screenshot copy too long');
}
rec.verification[4].detail='Recommended 04 calendar, 18 support and 19 checklist are proposed UI concepts, not verified native captures. Confirm the calendar only chooses duration/dates, not activation timing. All selected images need release-matched screenshots.';
rec.verification[2].detail='Validate the checklist on release devices: home-line data roaming OFF, Openline as data line, Openline roaming ON per its guide, automatic data switching OFF where supported. Home-line calls/SMS may still incur charges. Device setting names vary.';
rec.verification=rec.verification.filter(f=>f.id<7);
rec.verification.push(
 {id:7,title:'Comparative Pricing Held',detail:'Owner reports lower prices for some data allowances and durations. No dated like-for-like evidence was supplied, so cheaper-than-national-operator claims are excluded. Supply destination, operator/plan, data allowance, validity, fees and comparison date before adding them.'},
 {id:8,title:'Live Chat & Network Claims',detail:'24/7 live chat is owner-confirmed and publicly advertised at openline.com/contact; actual staffing/availability and the release app’s link still need verification. Candidate 15 is excluded from Recommended: a standalone network graphic is not an app-in-use screenshot, and automatic network/profile switching needs product evidence.'}
);
fs.writeFileSync(path,JSON.stringify(rec,null,2)+'\n');
console.log(JSON.stringify({selection:rec.selection,verification:rec.verification.length,characters:[rec.apple.description.length,rec.google.description.length]}));
