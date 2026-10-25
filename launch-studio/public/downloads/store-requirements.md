> Historical or submission-preparation reference. This document records its original scope and date; it is not current store approval or evidence of a production release. See the [current brand library](https://brand.openline.com/) and [repository documentation](https://github.com/askopenline/openline-brand/tree/main/docs).

# Openline — store submission requirements

## Audit addendum: 7 October 2026

The prior baseline below was rechecked against current primary documentation.
The source index now contains 17 references. These additional release gates are
reflected in the 33-item checklist and `submission-audit.md`:

- Validate Android native dependencies for 64-bit and 16 KB compatibility from
  the actual AAB and Console results; do not infer compliance from UI code.
  https://support.google.com/googleplay/android-developer/answer/17492799?hl=en-GB
  https://developer.android.com/guide/practices/page-sizes
- Validate listed Apple SDK privacy manifests and conditional binary signatures.
  https://developer.apple.com/support/third-party-SDK-requirements
- Validate the eSIM provisioning entitlement/profile if using the native
  CTCellularPlanProvisioning route; QR/manual workflows do not automatically
  inherit this requirement.
  https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.commcenter.fine-grained
- Declare Apple trader status independently of the conditional EU trader
  public-contact verification.
  https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements/
- Verify actual Android developer/package/signing-key registration for intended
  territories.
  https://developer.android.com/developer-verification
- First Google production release has no percentage rollout; all eligible users
  in selected countries can receive it. Release notes have a 500-Unicode-character
  per-language limit.
  https://support.google.com/googleplay/android-developer/answer/9859348?hl=en
- Prepare verified support/privacy/deletion URLs, copyright owner/year, review
  contact and Google support email. Console fields in `console-metadata.json`
  are deliberately blank until confirmed.
  https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/
  https://support.google.com/googleplay/android-developer/answer/9859152?hl=en

The flat icon's visual choice is approved at 43.5%. Native masking/appearance,
the 39.6dp adaptive treatment and actual app integration still require testing.
Screenshot artwork is a labelled reference, ready for replacement of its image
inputs rather than ready for store upload.

**Research checkpoint: 6 October 2026.** Scope: a phone-first travel eSIM app; iPad/tablet distribution remains an explicit decision, not an assumed Openline setting. This is a requirements reference, not a declaration that the app complies. **Required** means a submission rule; **Conditional** applies only when its trigger is met; **Recommended** is launch guidance, not a universal store gate. The accompanying JSON contains 12 primary official references; narrowly scoped supporting documentation is linked inline below.

## 1. Screenshot and graphics production

### Apple

| Status / slot | Exact accepted dimensions, width × height | Upload rule |
|---|---|---|
| Required iPhone coverage; recommended master: **6.9-inch** | Portrait **1260 × 2736**, **1290 × 2796**, or **1320 × 2868**; landscape **2736 × 1260**, **2796 × 1290**, or **2868 × 1320** | Use a supported 6.9-inch set rather than preparing every smaller iPhone slot. [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) |
| Conditional **6.5-inch** fallback | Portrait **1284 × 2778** or **1242 × 2688**; landscape **2778 × 1284** or **2688 × 1242** | Required if the app runs on iPhone and no 6.9-inch screenshots are supplied; otherwise Apple can scale the 6.9-inch set. [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) |
| Conditional **13-inch iPad** | Portrait **2064 × 2752** or **2048 × 2732**; landscape **2752 × 2064** or **2732 × 2048** | Required if the app runs on iPad; do not assume the iPhone set satisfies this slot. [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) |

**Required:** upload **1–10** screenshots for a supplied display set, in `.jpeg`, `.jpg`, or `.png`, without alpha channels or transparency; screenshots and metadata must accurately represent the app. [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) [App Review Guidelines §2.3](https://developer.apple.com/app-store/review/guidelines/)

**Recommended production baseline:** create six actual-flow iPhone screenshots at **1320 × 2868**, and only commission an iPad set after supported device families are confirmed. Six is a proposed creative brief, not Apple's minimum. Suggested narrative: destination discovery → plan details → checkout → installation guidance → usage/balance → top-up/support. Show only implemented flows; do not imply live features that are not in the submitted build.

### Google Play

| Status / asset | Exact specification |
|---|---|
| Required listing screenshots | At least **2 screenshots across device types** to publish; up to **8 per supported device type**. JPEG or **24-bit PNG, no alpha**; each dimension **320–3840 px**, and the longer dimension must be no more than **2×** the shorter. For a phone-only launch, supply at least two phone screenshots. [Google preview assets](https://support.google.com/googleplay/android-developer/answer/9866151?hl=en) |
| Recommended for screenshot-based recommendation formats | At least **4 screenshots**: portrait **9:16**, minimum **1080 × 1920**, or landscape **16:9**, minimum **1920 × 1080**. These promotional-eligibility recommendations are not the universal two-screenshot publication minimum. [Google preview assets](https://support.google.com/googleplay/android-developer/answer/9866151?hl=en) |
| Conditional large-screen asset work | If targeting tablets/Chromebooks, produce true large-screen layouts; Google's large-screen guidance calls for at least **4 screenshots**, **1080–7680 px**, **16:9 landscape / 9:16 portrait**. This is distinct large-screen guidance, not a new mandatory phone slot or a rule to upload four screenshots for every phone app. [Google preview assets](https://support.google.com/googleplay/android-developer/answer/9866151?hl=en) |
| Required Play listing icon | **512 × 512 px**, **32-bit PNG with alpha**, maximum **1024 KB**; this does not replace the in-app launcher icon. [Google preview assets](https://support.google.com/googleplay/android-developer/answer/9866151?hl=en) |
| Required feature graphic | **1024 × 500 px**, JPEG or **24-bit PNG, no alpha**. [Google preview assets](https://support.google.com/googleplay/android-developer/answer/9866151?hl=en) |

**Recommended production baseline:** six phone screenshots at **1080 × 1920**, separate from the Apple exports; keep essential UI and copy legible. A literal resize of Apple's taller frames is not the production plan.

## 2. App icons: store assets are not launcher source files

- **Apple required design asset:** iOS/iPadOS icon layout is **1024 × 1024 px**, square before system masking. For layered work, make an imported background full-bleed and opaque; foreground layers can use opacity. Do not apply a blanket “no transparency in any layer” rule to Icon Composer source artwork. [Apple app-icon HIG](https://developer.apple.com/design/human-interface-guidelines/app-icons)
- **Apple recommended, not a verified universal submission gate:** use Icon Composer for the iOS 26-era Liquid Glass layered icon workflow, preview its appearances, and integrate the Icon Composer file into the Xcode target. Apple's HIG permits a flattened image; it does not say every app must adopt Icon Composer. The App Icon build field must match the file name without its extension, and Xcode generates icon images for supported earlier OS releases. [Apple app-icon HIG](https://developer.apple.com/design/human-interface-guidelines/app-icons) [Icon Composer integration](https://developer.apple.com/documentation/Xcode/creating-your-app-icon-using-icon-composer?changes=latest_5_1_1_2_2&language=objc)
- **Android recommended launcher delivery; conditional specifications when using adaptive icons:** foreground and background layers, each **108 × 108 dp**; key logo at least **48 × 48 dp**, no more than **66 × 66 dp** in the safe zone; avoid pre-applied outline masks/shadows. Supply a single **monochrome** layer for controlled themed-icon support on Android 13+; the official page does not describe monochrome as a universal Play submission requirement. Use `android:icon` and an adaptive-icon resource such as `res/mipmap-anydpi-v26/ic_launcher.xml`; `android:roundIcon` is optional. [Android adaptive icons](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive)

## 3. Store copy and contact fields

| Platform / field | Limit and status |
|---|---|
| Apple name | **2–30 characters**; required. [Apple app information](https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/) |
| Apple subtitle | **30 characters** maximum; optional. [Apple app information](https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/) |
| Apple promotional text | **170 characters** maximum; optional. [Apple platform version information](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/) |
| Apple description | **4000 characters**, plain text; required. [Apple platform version information](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/) |
| Apple keywords | **100 bytes**, not a blanket 100-character allowance; required. Non-ASCII characters can consume more than one byte. [Apple platform version information](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/) |
| Apple What's New | **4000 characters**; not available for first version, required for subsequent versions. [Apple platform version information](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/) |
| Apple review notes | **4000 bytes**; provide explanations and test instructions as applicable. [Apple platform version information](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/) |
| Google app name | **30 characters**. [Google app setup](https://support.google.com/googleplay/android-developer/answer/9859152?hl=en) |
| Google short description | **80 characters**. [Google app setup](https://support.google.com/googleplay/android-developer/answer/9859152?hl=en) |
| Google full description | **4000 characters**. [Google app setup](https://support.google.com/googleplay/android-developer/answer/9859152?hl=en) |

**Required:** provide accurate support/contact information; Apple's review contact requires a name, email and international-format phone number, and the Support URL must give users an easy way to contact the developer. [Apple platform version information](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/) [App Review Guidelines §1.5](https://developer.apple.com/app-store/review/guidelines/)

**Recommended:** maintain a locale-by-locale copy sheet, validated in characters and UTF-8 bytes where appropriate. Do not fabricate coverage, speeds, roaming partners, “unlimited” terms, refunds, activation timing, compatibility, or savings.

## 4. Privacy, deletion, declarations and login

### Required

- **Apple:** provide a privacy-policy link in App Store Connect and an easily accessible link inside the app; describe collected data, uses, third parties, retention/deletion and consent withdrawal. Complete App Privacy details for the app and integrated partners/SDKs; these disclosures feed the Privacy Nutrition Label. [App Review Guidelines §5.1.1](https://developer.apple.com/app-store/review/guidelines/) [Apple submission checklist](https://developer.apple.com/app-store/submitting/)
- **Google:** complete an accurate Data safety section, including third-party SDK practices, and keep it consistent with actual behavior and the privacy policy. Every app needs a policy in the designated Console field and a policy link/text in-app, even if it does not collect sensitive data; the URL must be active, public, non-geofenced, non-editable and not a PDF. Include privacy contact, data use/sharing, security, retention and deletion. [Google Developer Program Policy — User Data](https://support.google.com/googleplay/android-developer/answer/17517561?hl=en)
- **Store declarations:** complete Apple's age-rating questionnaire; complete Google's content rating, target-audience and ads declarations and any applicable App content declarations. Do not pre-fill Openline as “no ads,” “no tracking,” “no data collected,” or a particular age rating without evidence. [Apple submission checklist](https://developer.apple.com/app-store/submitting/) [Google review preparation](https://support.google.com/googleplay/android-developer/answer/9859455?hl=en)

### Conditional

- **Account creation:** Apple requires **in-app account deletion**; Google requires a readily discoverable deletion-request route **inside the app and outside it**, with the external URL entered in Play Console. Google requires deletion of associated user data, not merely deactivation; legitimate security/fraud/regulatory retention must be disclosed. [App Review Guidelines §5.1.1(v)](https://developer.apple.com/app-store/review/guidelines/) [Google Developer Program Policy — Account Deletion](https://support.google.com/googleplay/android-developer/answer/17517561?hl=en)
- **Apple login:** if there are no significant account-based features, allow use without login. Third-party/social login for the primary account triggers §4.8's equivalent privacy-preserving login option unless an exception applies; an app using exclusively its own account system is an exception. Do not describe Sign in with Apple as compulsory for every login-based app. [App Review Guidelines §§5.1.1(v), 4.8](https://developer.apple.com/app-store/review/guidelines/)
- **Apple tracking / SDKs / APIs:** ATT permission is required for tracking; review SDK privacy manifests and declare required-reason APIs in `PrivacyInfo.xcprivacy` when applicable. The public privacy label, privacy policy, permissions and bundled manifest are separate deliverables, not interchangeable documents. [App Review Guidelines §5.1.2](https://developer.apple.com/app-store/review/guidelines/) [Apple privacy manifests](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
- **Google sensitive access:** permissions must be necessary for implemented, disclosed functionality; unexpected sensitive-data collection needs prominent in-app disclosure and affirmative consent, and some sensitive permissions need additional approval. [Google Developer Program Policy — User Data / Permissions](https://support.google.com/googleplay/android-developer/answer/17517561?hl=en) [Google review preparation](https://support.google.com/googleplay/android-developer/answer/9859455?hl=en)

**Openline evidence needed:** inventory actual account identifiers, purchase/transaction records, eSIM identifiers, device/network data, diagnostics, analytics, support content and every SDK/provider; determine collection/sharing, purposes, optionality, linkage/tracking, retention and deletion behavior. These are investigation categories, not asserted Openline disclosures.

## 5. Reviewer access and telecom payment treatment

### Review access

- **Required when restricted:** Apple needs complete review access, non-expiring demo credentials where login is required, any needed resources such as sample QR codes, and live backends. A demo-mode substitute necessitated by legal/security constraints needs prior Apple approval under §2.1(a). [App Review Guidelines §2.1 and Before You Submit](https://developer.apple.com/app-store/review/guidelines/) [Apple platform version information](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/)
- **Required when restricted:** Google needs reusable, continuously working, location-independent credentials in English, bypassing OTP/2-step gates; include social-login details, static URLs for QR credentials, and full/free access behind paywalls. Do not leave review dependent on the founder answering an OTP request. [Google reviewer credentials](https://support.google.com/googleplay/android-developer/answer/15748846?sjid=13063250944672200885-NC)
- **Recommended reviewer pack:** describe purchase → provisioning → installation → balance → top-up → deletion; supply a funded/safe test account and explain hardware, country, carrier and irreversible provisioning constraints. Arrange a compliant way to inspect restricted functions without reviewer expense or travel; do not silently fake production functionality.

### Payments — classification must be confirmed

- **Apple rule:** services consumed outside the app must use methods other than IAP under **§3.1.3(e)**; unlocking digital app functionality generally falls under **§3.1.1**. [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- **Google rule:** Play Billing is generally required for digital in-app features/services, but must not be used for the stated physical goods/services exceptions or **“a remittance in respect of a credit card bill or utility bill (such as cable and telecommunications services).”** [Google Developer Program Policy — Payments](https://support.google.com/googleplay/android-developer/answer/17517561?hl=en)
- **Provisional Openline interpretation, not an approval:** a plan purchasing real cellular connectivity may fit outside-app/telecom treatment; do **not** turn that into “every eSIM transaction is automatically exempt.” Google's explicit utility-bill wording does not itself conclusively classify every prepaid eSIM resale. Confirm the exact SKU, merchant/reseller relationship, consumption, checkout and territory, and explain the model in review notes; evaluate separately any paid digital app features or bundles. [App Review Guidelines §§3.1, 3.1.1, 3.1.3(e)](https://developer.apple.com/app-store/review/guidelines/) [Google Payments policy](https://support.google.com/googleplay/android-developer/answer/17517561?hl=en)

## 6. Build, account, testing and EU readiness

| Status | Launch requirement |
|---|---|
| Required Apple build floor now | Since **28 April 2026**, uploads must use **Xcode 26+** with the applicable **iOS/iPadOS 26 SDK or later**. This is a build-SDK floor, not an instruction to set minimum supported iOS to 26. Apple's separately announced **April 2027** SDK-27 requirement is future, not today's gate. [Apple SDK requirement](https://developer.apple.com/news/upcoming-requirements/?id=02032026a) [Apple submission checklist](https://developer.apple.com/app-store/submitting/) |
| Required Google mobile target now | Since **31 August 2026**, new apps and updates must target **Android 16 / API 36+**. The API-35 rule for existing-app discoverability is not the new-app requirement. An extension to **1 November 2026** can be requested in eligible Console workflows; do not assume Openline has or qualifies for one. `targetSdkVersion` is not `minSdkVersion`. [Google target API requirements](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en) |
| Required Android package work | Prepare a signed Android App Bundle, configure Play App Signing for the new release, choose the permanent package name carefully, and manage increasing version codes. [Google app setup](https://support.google.com/googleplay/android-developer/answer/9859152?hl=en) |
| Required Apple account; conditional organization proof | Complete Developer Program enrollment and agreements with 2FA. Organization enrollment requires legal-entity status, binding authority, D-U-N-S except government entities, organizational contact details and a functional organization-domain website; individual and organization seller-name presentation differs. [Apple enrollment](https://developer.apple.com/programs/enroll/) |
| Required Google identity; conditional organization proof | Verify legal identity through the linked payments profile and operational contact details. Organizations generally require D-U-N-S and matching legal details; legal name/address plus developer email/phone are public for organization accounts. A personal account has different public-information rules. [Google developer account information](https://support.google.com/googleplay/android-developer/answer/13628312?hl=en) |
| Conditional Google testing gate | **Personal accounts created after 13 November 2023:** closed test with **at least 12 testers continuously opted in for the preceding 14 days**, then **apply for production access**; elapsed time alone is not approval. Do not apply this particular cohort rule to every organization account. [Google personal-account testing](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en) |
| Conditional Google device verification | New personal accounts must verify access to a **physical, non-rooted Android device running Android 10+**, using the Play Console mobile app as account owner. [Google device verification](https://support.google.com/googleplay/android-developer/answer/14316361?hl=en) |
| Required Apple trader declaration; conditional EU trader verification | Declare trader status even without EU distribution. Traders distributing in the EU must verify contact information that Apple publishes: address, phone and email; organizations use the D-U-N-S-associated address. Determine the actual legal status rather than choosing non-trader for privacy. [Apple DSA requirements](https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements/) |

**Google DSA caution:** the reviewed Google documentation verifies developer identity and public information, but does not establish an Apple-identical universal trader-status toggle. Check actual Play Console legal/trader prompts for the selected account and territories; do not copy Apple's procedure into the Google checklist as a verified rule.

**Recommended QA, not a stated universal cohort gate:** device testing of eSIM-compatible/unsupported/locked-device cases, payment success/failure/refunds, provisioning and QR reuse limits, low/no connectivity, top-up, deletion, privacy links, localization and accessibility. Confirm native SDK/build compatibility using the actual dependency inventory.

## 7. Decisions needed before marking “ready”

1. Legal publishing entity and account type, account creation date, existing verification and production-access status.
2. Bundle ID/package name, supported device families, minimum supported OS, actual build/target SDK, and distribution countries.
3. Whether iPad/tablet is genuinely supported; screenshot locales, final in-app flows and exact localized claims.
4. Authentication providers, guest-access design, account creation/deletion paths, and external deletion URL.
5. Actual SDK/data map and permissions; legal retention rules; verified privacy-policy/support URLs.
6. Exact telecom products, merchant/payment architecture, renewals/refunds, and any digital-only paid features.
7. Reviewer credentials, provisioning resources, geographic/hardware constraints, and test access that does not require a real purchase.
8. EU trader determination and approved public legal/contact details; account-specific Google legal prompts.

No Openline Console settings, source code, entitlements, data flows, privacy answers or account credentials were inspected or changed during this research.
