import artwork from './public/artwork.json' with {type:'json'};
import creative from './public/series.json' with {type:'json'};
export const screens = artwork.slides;
export const copyDefaults={
  apple:{
    name:'Openline: Travel eSIM & Data',
    subtitle:'Find your plan. See your data.',
    promotional:'Find a travel eSIM for your next destination. Compare data and duration, find installation details, and keep your plans together in Openline.',
    keywords:'international,roaming,internet,connectivity,abroad,holiday,mobile,prepaid',
    description:`Your next destination. Your choice of data.

${creative.differentiator.paragraph}

CHOOSE WITH THE DETAILS IN FRONT OF YOU
Browse your destination, compare data allowances and duration, and review the price and activation conditions before you buy.

KEEP SETUP INFORMATION CLOSE
Find your eSIM's installation information and plan details in the app. Follow the instructions for your device and plan.

SEE YOUR PLANS IN ONE PLACE
Check the usage information shown for your plan and keep your travel eSIMs together. Availability and reporting can vary by plan.

NEW TO eSIM?
An eSIM is a digital SIM for a compatible device. Before purchasing, check that your phone supports eSIM and is network-unlocked.

BEFORE YOU GO
Review destination coverage, validity, activation timing and included services. Do not assume a data plan includes a phone number, calls or SMS. If you keep your usual line active, your home carrier's charges may still apply.

Openline is free to download. Mobile data plans are purchased separately. Availability and service conditions vary by destination and provider.

Visit openline.com for support information.`,
    reviewNotes:`Openline provides travel eSIM connectivity.

Before submission, the release owner must enter a working, non-expiring review account through App Store Connect's secure review fields. Do not put credentials in this workspace.

Explain: supported eSIM devices; provisioning and installation flow; any geography or hardware constraints; how a reviewer can access all functionality without a real purchase or an OTP dependency.

Describe the exact connectivity product and payment model, and confirm the applicable store payment policy. The screenshots must match this submitted build.

Provide tested steps for account deletion, support access, purchases and installation. Replace this preparation note with the verified build-specific instructions.`
  },
  google:{
    name:'Openline: Travel eSIM & Data',
    shortDescription:'Find a travel eSIM, compare plans and keep your mobile data in view.',
    description:`Find a travel eSIM for your next destination.

${creative.differentiator.paragraph}

COMPARE BEFORE YOU BUY
Browse a destination and review available data allowances, duration and prices. Check coverage, activation conditions and included services before choosing a plan.

FIND YOUR SETUP DETAILS
Keep your eSIM's installation information and plan details in reach. Follow the instructions for your device and plan.

KEEP YOUR DATA IN VIEW
See the usage information available for your plan and manage your eSIMs from one place. Availability and reporting can vary by plan.

NEW TO eSIM?
An eSIM is a digital SIM for a compatible device. Check that your phone supports eSIM and is network-unlocked before purchasing.

TRAVEL PREPARED
Mobile data plans are purchased separately from this free app. Coverage, validity and service conditions vary by destination and provider. Check whether your plan includes a phone number, calls or SMS; do not assume these are included with data. Your home carrier's charges may still apply if you keep your usual line active.

Visit openline.com for support information.`,
    releaseNotes:'Welcome to Openline. Explore travel eSIM plans, find installation details and keep your eSIMs together.'
  }
};
export const fieldSpecs={
 apple:[['name','App name',30],['subtitle','Subtitle',30],['promotional','Promotional text',170],['keywords','Keywords',100,'bytes'],['description','Description',4000],['reviewNotes','Review notes template',4000,'bytes']],
 google:[['name','App name',30],['shortDescription','Short description',80],['description','Full description',4000],['releaseNotes','Release notes draft',500]]
};
export const tasks=[
 ['icon','Final icon visual choice approved','Creative','Both','done','Paul finalized the 43.5% white-square composition on 7 October 2026. Download the final all-formats pack. This approval covers the visual choice, not native integration or platform acceptance. Android adaptive 39.6dp legibility remains a native QA gate; 48dp fallback is preserved.','apple-icons','Paul','required'],
 ['native-icons','Integrate icons in release targets','Build','Both','todo','Import the Xcode catalog; merge Android resources; verify masks and dark/themed variants in the actual builds.','android-icons','Engineering','required'],
 ['art','Verify native app screenshots and launch claims','Creative','Both','blocked','Alternating orange/cream, six distinct app views. Dashboard at frame 5 and plan selection at 6 replace illustrations. These are supplied React captures, not native evidence. Verify release UI, network claims, price/FUP wording and platform-specific copy. Both platforms carry OMDM pricing positioning requiring evidence. See screenshot-compliance-review.md.','google-assets','Design','required'],
 ['captures','Recapture from the native release builds','Creative','Both','blocked','Replace the design-reference imagery with accurate platform-native screens. Remove draft labels only after comparison and approval.','apple-screenshots','Engineering','required'],
 ['feature','Approve the Play feature graphic','Creative','Google','review','1024 × 500 RGB PNG included. Verify UI, language and claims against the Android build.','google-assets','Design','required'],
 ['copy','Verify store copy and every claim','Listing','Both','review','Verify network partners, best-effort replacement-profile operations and OMDM supplier comparison against the launch service. Substantiate better-price/value positioning with sourcing and comparable retail evidence before submission. No cheapest, quantified savings, instant switching or universal multi-network guarantee. Unlimited plans remain subject to local fair-use rules.','apple-copy','Product','required'],
 ['locales','Choose launch languages','Listing','Both','todo','English draft supplied. Commission French and Portuguese localization only for supported app languages. Each needs reviewed text and screenshots.','google-assets','Product','recommended'],
 ['tablets','Decide supported device families','Build','Both','blocked','Phone-first is a proposal, not a build setting. If iPad/tablet support is enabled, create and verify native large-screen layouts and screenshots.','apple-screenshots','Engineering','conditional'],
 ['accounts','Verify publishing accounts','Accounts','Both','blocked','Confirm legal publishing entity, enrollment, agreements, contact details and account verification. Organization accounts are recommended for a company app.','google-copy-build','Founder','required'],
 ['ids','Reserve final app identifiers','Build','Both','todo','Confirm the final bundle ID/package before creation. com.openline.app is only a proposed value and has not been reserved or checked.','google-copy-build','Engineering','required'],
 ['apple-sdk','Build with the current Apple SDK','Build','Apple','todo','Use Xcode 26+ and iOS SDK 26+ for current uploads. This is not the minimum supported iOS version.','apple-sdk','Engineering','required'],
 ['android-sdk','Target Android API 36+','Build','Google','todo','New app/update target requirement as of the research date; do not assume a policy extension. Choose minSdk separately based on dependencies.','google-sdk','Engineering','required'],
 ['signing','Complete signing and release artifacts','Build','Both','todo','Upload a signed iOS archive through the developer workflow and a signed Android App Bundle with Play App Signing configured. No builds are included here.','google-copy-build','Engineering','required'],
 ['binary-compat','Verify Android 64-bit / 16 KB compatibility','Build','Google','todo','Inspect the actual AAB and every native SDK dependency for 64-bit and 16 KB page-size compatibility. Save bundle/Console validation and device evidence; Java/Kotlin-only apps are compatible by default. Do not assume a deadline extension.','google-technical','Engineering','conditional'],
 ['provisioning','Validate the native eSIM provisioning path','Build','Apple','todo','If using CTCellularPlanProvisioning, validate the required public-cellular-plan entitlement, distribution profile and real-device provisioning. QR/manual-only installation follows a different route; document which route the release actually uses.','apple-provisioning','Engineering','conditional'],
 ['privacy-map','Map actual data and SDK behavior','Privacy','Both','blocked','Inventory identifiers, eSIM/network data, transactions, diagnostics, support and analytics. Determine collection, sharing, purposes and retention from the actual build.','google-policy','Privacy owner','required'],
 ['privacy-policy','Publish and verify a privacy policy','Privacy','Both','blocked','Provide a public privacy URL and in-app access. Verify owner contact, data practices, retention and deletion. Do not publish a generic policy as if it reflects the app.','google-policy','Privacy owner','required'],
 ['privacy-label','Complete privacy disclosures','Privacy','Both','blocked','Complete App Privacy and Data safety from the verified data map. No “no data collected”, “no tracking” or “no ads” answers are assumed.','google-policy','Privacy owner','required'],
 ['deletion','Implement and test account deletion','Privacy','Both','blocked','If accounts can be created: in-app deletion for Apple; an in-app route plus a public external deletion-request URL for Google. Deactivation alone is not sufficient.','google-policy','Engineering','conditional'],
 ['sdk-manifest','Review SDK manifests, signatures and permissions','Privacy','Both','todo','Audit required-reason APIs, listed SDK privacy manifests and binary SDK signatures, including repackaged listed SDKs. Review runtime permissions. Request ATT only if the app actually tracks under Apple’s definition.','apple-sdks','Engineering','conditional'],
 ['login','Verify the login experience','Review','Apple','todo','The supplied UI shows social login. Confirm implemented providers and §4.8 equivalent-login requirements or an applicable exception.','apple-review','Engineering','conditional'],
 ['payments','Confirm the eSIM payment classification','Review','Both','blocked','Document each SKU, consumption, merchant model and checkout. Telecom/outside-app treatment may apply, but no blanket prepaid-eSIM exemption is presumed.','google-policy','Product / legal','required'],
 ['review-access','Prepare a working review account','Review','Both','blocked','Provide full/free review access, no expiring OTP dependency, clear installation instructions and a safe provisioning path. Store secrets only in the consoles.','apple-review','Engineering','conditional'],
 ['rating','Complete age and audience questionnaires','Listing','Both','todo','Answer age rating, target audience, content rating and ads declarations from actual features and SDK behavior. Do not assume 4+ or Everyone.','google-policy','Product','required'],
 ['export','Assess export compliance','Review','Apple','todo','Inspect encryption usage and answer Apple’s export-compliance flow for the actual binary. Do not automatically set ITSAppUsesNonExemptEncryption to false.','apple-review','Engineering / legal','required'],
 ['trader','Declare Apple trader status','Accounts','Apple','blocked','Declare actual trader status even when not distributing in the EU. This is separate from conditional EU trader contact verification.','apple-dsa','Founder','required'],
 ['trader-eu','Verify EU trader public contacts','Accounts','Apple','blocked','If distributing as a trader in the EU, verify the public legal address, phone and email. Approve what will be displayed; do not infer legal status.','apple-dsa','Founder','conditional'],
 ['package-registration','Verify Android package registration','Accounts','Google','todo','Confirm the actual package/signing key is registered under Android developer verification for selected territories. Most Play apps are automatically registered, but verify Console status rather than assuming it.','android-verification','Engineering','conditional'],
 ['testing','Resolve personal-account testing gate','Testing','Google','todo','If a personal account was created after 13 Nov 2023: 12 testers continuously opted in for 14 days, then production-access approval. Account type/date are unknown.','google-testing','Release owner','conditional'],
 ['qa','Run real-device release QA','Testing','Both','todo','Test unsupported/locked phones, installation, payment failure, low/no connectivity, top-up, deletion and accessibility. Native eSIM functions cannot be certified from a web gallery.','apple-review','QA','required'],
 ['links','Verify support and public URLs','Listing','Both','blocked','Confirm live support, privacy and deletion pages. A proposed URL is not evidence that a page exists or meets policy.','google-policy','Product','required'],
 ['release','Choose rollout and release control','Release','Both','todo','Recommend manual Apple release after approval. The first Google production release cannot use a percentage rollout: it reaches all eligible users in selected countries. Confirm territories, launch timing and monitoring; percentage rollouts are for later updates.','google-release','Release owner','recommended'],
 ['submit','Final submission review','Release','Both','blocked','Compare every listing asset and declaration to the signed build. This workspace does not submit to either store.','apple-review','Release owner','required']
].map(([id,title,group,platform,status,detail,source,owner,requirement])=>({id,title,group,platform,status,detail,source,owner,requirement,notes:''}));
export const suggestedSettings=[
 ['Store identity','App name','Openline: Travel eSIM & Data','Draft','Verify name availability in both consoles.','apple-copy'],
 ['Store identity','Category','Apple: Travel · Google: Travel & Local','Suggested','Confirm these are the best categories for the shipped app.','google-copy-build'],
 ['Store identity','Pricing','Free download; data plans purchased separately','Suggested','Confirm exact product and billing setup. Free download does not mean free data.','google-policy'],
 ['Store identity','Primary language','English (US)','Suggested','Add only languages supported and reviewed for the release.','apple-copy'],
 ['Build configuration','Bundle ID / package','com.openline.app','Unconfirmed','Proposed only; verify ownership and existing identifiers before creating.','google-copy-build'],
 ['Build configuration','Version','1.0.0 · build 1 / versionCode 1','Suggested','Only if this is the first build. Existing apps need unique/increasing build values.','google-copy-build'],
 ['Build configuration','Apple build SDK','Xcode 26+ · iOS SDK 26+','Requirement','Do not confuse the SDK with the deployment target.','apple-sdk'],
 ['Build configuration','Android target SDK','API 36+','Requirement','Current new-app/update baseline; no extension assumed.','google-sdk'],
 ['Build configuration','Minimum OS','Decide after dependency and device audit','Unconfirmed','No minimum iOS or Android version can be verified from the React mockups.','google-sdk'],
 ['Build configuration','Supported devices','Phone-first; tablets pending decision','Suggested','iPad/tablet support creates additional layout and asset work.','apple-screenshots'],
 ['Store declarations','Privacy / Data safety','Needs actual build and SDK inventory','Blocked','Do not infer disclosures from the visual design.','google-policy'],
 ['Store declarations','Age rating / audience / ads','Answer console questionnaires','Blocked','No default “Everyone”, “4+”, “no ads” or “no tracking” claim.','google-policy'],
 ['Store declarations','Encryption / export','Engineering and legal assessment','Blocked','Declare based on actual binary and encryption use.','apple-review'],
 ['Store declarations','Payment route','Confirm SKU-specific telecom treatment','Blocked','External payment may be appropriate for connectivity, but must be verified.','google-policy'],
 ['Release controls','Apple release','Manual release after approval','Suggested','Coordinate support, production APIs and the public launch.','apple-review'],
 ['Release controls','Google release','First release: selected countries, no percentage rollout','Requirement','Initial production goes to all eligible users in selected countries. Plan monitoring; percentage rollouts apply to later updates.','google-release'],
 ['Store identity','Public listing contacts','Support URL, support email, copyright and review contact','Unconfirmed','Enter verified public URLs, legal owner/year and operational contact details in the secure consoles. No reviewer credentials in this studio.','apple-copy'],
 ['Release controls','EU availability','Trader status and legal review first','Blocked','Confirm public legal/contact data before EU distribution.','apple-dsa']
].map(([group,field,value,status,detail,source])=>({group,field,value,status,detail,source}));
export const initialWorkspace={schemaVersion:4,artworkRevision:3,previewRevision:13,copyRevision:3,preferredSeries:'signal',screenshotNotes:'',iconRevision:4,iconApproval:'approved-2026-10-07',iconSize:43.5,iconTone:'light',copy:copyDefaults,tasks,titles:screens.map(s=>s.title),approvedScreens:[],settingsNotes:'',updatedAt:null};
