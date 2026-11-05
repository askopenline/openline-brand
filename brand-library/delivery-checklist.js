// Simple pre-submission checklist. Values in [BRACKETS] are owner-only facts that this package cannot know.
export const G_DELIVERED='Delivered in this package',G_PROVIDE='Provide for Openline',G_BUILD='Verify in the release build';
export const SRC={
 appleInfo:'https://developer.apple.com/help/app-store-connect/reference/app-information/',
 applePrivacy:'https://developer.apple.com/app-store/app-privacy-details/',
 appleExport:'https://developer.apple.com/help/app-store-connect/manage-app-information/overview-of-export-compliance',
 appleReview:'https://developer.apple.com/app-store/review/guidelines/',
 appleDsa:'https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements/',
 googleData:'https://support.google.com/googleplay/android-developer/answer/10787469',
 googleContent:'https://support.google.com/googleplay/android-developer/answer/9859455',
 googleDelete:'https://support.google.com/googleplay/android-developer/answer/13327111',
 googleTarget:'https://support.google.com/googleplay/android-developer/answer/11926878'
};
const D=(id,label,jump,where)=>({id,group:G_DELIVERED,label,jump,where});
const P=(id,label,provide,where,src)=>({id,group:G_PROVIDE,label,provide,where,src});
export const CHECK={
 apple:[
  D('d-listing','Listing text pasted','dl-listing','Distribution > version page'),
  D('d-category','Category set to Travel','dl-category','App Information'),
  D('d-graphics','Icon, header and search graphics uploaded','dl-graphics','Product page assets'),
  D('d-shots','Screenshots uploaded in order (both sizes)','dl-shots','Version page > Screenshots'),
  P('account','Developer account and seller name','Organization account. Seller name shown on the store: Openline. Legal entity: Openline EOOD, matching the D-U-N-S record. Account Holder: Paul Fleury.','App Store Connect > Business / Users and Access'),
  P('bundle','Bundle ID, SKU and primary language','Bundle ID: [BUNDLE_ID], identical to the signed build. SKU: [UNIQUE_SKU]. Primary language: English (U.S.).','App Information',SRC.appleInfo),
  P('urls','Privacy Policy and Support URLs','Privacy Policy URL: https://openline.com/privacy (public, working). Support URL: https://openline.com/contact. Marketing URL is optional.','App Information / version page',SRC.appleInfo),
  P('privacy','App Privacy answers','Declare data Openline collects and what its SDKs collect: contact details, purchases, identifiers, diagnostics and usage as applicable. Answers must match the build and the privacy policy.','App Privacy',SRC.applePrivacy),
  P('age','Age rating','Answer the questionnaire from real features. Live chat is customer support, not public user content.','App Information > Age Rating',SRC.appleInfo),
  P('export','Export compliance','Standard HTTPS and OS encryption only: answer per Apple\'s exemption rules and set the Info.plist key. Confirm against the build.','Build > Export Compliance',SRC.appleExport),
  P('dsa','EU trader declaration','Trader name, address, phone and email for EU storefronts. Required to distribute in the EU.','Business > Digital Services Act',SRC.appleDsa),
  P('pricing','Price, payment path and territories','Free download. State how eSIM plans are paid for (in-app or external) and keep it identical in the reviewer notes. Storefronts: [LIST_STOREFRONTS]. eSIM destination coverage is separate from storefront availability.','Pricing and Availability',SRC.appleReview),
  P('review','Reviewer access and notes','If sign-in is needed: demo account or guest path, and steps to see a plan and the install flow without paying. Enter credentials and notes only in the console, never in this package.','Version page > App Review Information',SRC.appleReview),
  P('deletion','Account deletion','If users can create accounts, an in-app way to delete the account and its data: once logged in, open Settings (or Me), then Privacy & data, then Delete account.','In the app',SRC.appleReview),
  P('build','Signed build attached','Version [VERSION], build [BUILD_NUMBER], built with a current Xcode SDK. Processed and ready in App Store Connect.','Version page > Build',SRC.appleInfo)
 ],
 google:[
  D('d-listing','Listing text pasted','dl-listing','Main store listing'),
  D('d-category','Category set to Travel and Local','dl-category','Store settings'),
  D('d-graphics','Icon and feature graphic uploaded','dl-graphics','Main store listing > Graphics'),
  D('d-shots','Phone screenshots uploaded in order, with alt text','dl-shots','Main store listing > Phone screenshots'),
  P('account','Developer account and name','Organization account. Developer name shown on Play: Openline. Legal entity: Openline EOOD. Confirm account verification is complete.','Play Console > Account details'),
  P('package','Package name and app signing','Package name: com.openline.esim. Signed Android App Bundle with Play App Signing enabled.','Release > Setup > App signing'),
  P('contact','Store contact details','Public contact email: [SUPPORT_EMAIL]. Website: https://openline.com. Phone is optional.','Store settings > Store listing contact details'),
  P('privacy','Privacy policy and Data safety form','Privacy Policy URL: https://openline.com/privacy. Data safety: declare data Openline and its SDKs collect or share (contact details, purchases, identifiers, diagnostics) and encryption in transit. Must match the build.','App content > Privacy policy / Data safety',SRC.googleData),
  P('rating','Content rating and target audience','Complete the rating questionnaire from real features. Target audience: adults and travellers [CONFIRM_AGE_GROUPS], not directed to children.','App content',SRC.googleContent),
  P('ads','Ads declaration','Declare whether the app shows ads: [CONFIRM_YES_NO]. Then complete any other App content declarations Play asks for.','App content > Ads',SRC.googleContent),
  P('deletion','Account deletion','If users can create accounts: in-app deletion path: once logged in, open Settings (or Me), then Privacy & data, then Delete account; and a public web link [DELETION_URL].','App content > Data deletion',SRC.googleDelete),
  P('access','App access for reviewers','If sign-in is needed: test account or guest path and steps to reach a plan and the install flow. Enter credentials only in the console, never in this package.','App content > App access',SRC.googleContent),
  P('pricing','Price, payments and countries','Free download. State how eSIM plans are paid for (Play Billing or external) in line with Play payments policy. Countries: [LIST_COUNTRIES].','Monetize / Release > Countries',SRC.googleContent),
  P('build','Release build meets Play requirements','Release [VERSION] ([VERSION_CODE]) with a current target API level, 64-bit libraries and 16 KB page-size support where native code is used.','Release > Production',SRC.googleTarget)
 ]
};
