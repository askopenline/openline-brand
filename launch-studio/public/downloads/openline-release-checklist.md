> Historical or submission-preparation reference. This document records its original scope and date; it is not current store approval or evidence of a production release. See the [current brand library](https://brand.openline.com/) and [repository documentation](https://github.com/askopenline/openline-brand/tree/main/docs).

# Openline release checklist

The final flat icon visual choice is approved. Native integration, capture replacement and release evidence remain separate. Nothing here is store approval.

- [x] Final icon visual choice approved (Both; required; done)
  Owner: Paul
  Paul finalized the 43.5% white-square composition on 7 October 2026. Download the final all-formats pack. This approval covers the visual choice, not native integration or platform acceptance. Android adaptive 39.6dp legibility remains a native QA gate; 48dp fallback is preserved.

- [ ] Integrate icons in release targets (Both; required; todo)
  Owner: Engineering
  Import the Xcode catalog; merge Android resources; verify masks and dark/themed variants in the actual builds.

- [ ] Verify native app screenshots and launch claims (Both; required; blocked)
  Owner: Design
  Alternating orange/cream, six distinct app views. Dashboard at frame 5 and plan selection at 6 replace illustrations. These are supplied React captures, not native evidence. Verify release UI, network claims, price/FUP wording and platform-specific copy. Both platforms carry OMDM pricing positioning requiring evidence. See screenshot-compliance-review.md.

- [ ] Recapture from the native release builds (Both; required; blocked)
  Owner: Engineering
  Replace the design-reference imagery with accurate platform-native screens. Remove draft labels only after comparison and approval.

- [ ] Approve the Play feature graphic (Google; required; review)
  Owner: Design
  1024 × 500 RGB PNG included. Verify UI, language and claims against the Android build.

- [ ] Verify store copy and every claim (Both; required; review)
  Owner: Product
  Verify network partners, best-effort replacement-profile operations and OMDM supplier comparison against the launch service. Substantiate better-price/value positioning with sourcing and comparable retail evidence before submission. No cheapest, quantified savings, instant switching or universal multi-network guarantee. Unlimited plans remain subject to local fair-use rules.

- [ ] Choose launch languages (Both; recommended; todo)
  Owner: Product
  English draft supplied. Commission French and Portuguese localization only for supported app languages. Each needs reviewed text and screenshots.

- [ ] Decide supported device families (Both; conditional; blocked)
  Owner: Engineering
  Phone-first is a proposal, not a build setting. If iPad/tablet support is enabled, create and verify native large-screen layouts and screenshots.

- [ ] Verify publishing accounts (Both; required; blocked)
  Owner: Founder
  Confirm legal publishing entity, enrollment, agreements, contact details and account verification. Organization accounts are recommended for a company app.

- [ ] Reserve final app identifiers (Both; required; todo)
  Owner: Engineering
  Confirm the final bundle ID/package before creation. com.openline.app is only a proposed value and has not been reserved or checked.

- [ ] Build with the current Apple SDK (Apple; required; todo)
  Owner: Engineering
  Use Xcode 26+ and iOS SDK 26+ for current uploads. This is not the minimum supported iOS version.

- [ ] Target Android API 36+ (Google; required; todo)
  Owner: Engineering
  New app/update target requirement as of the research date; do not assume a policy extension. Choose minSdk separately based on dependencies.

- [ ] Complete signing and release artifacts (Both; required; todo)
  Owner: Engineering
  Upload a signed iOS archive through the developer workflow and a signed Android App Bundle with Play App Signing configured. No builds are included here.

- [ ] Verify Android 64-bit / 16 KB compatibility (Google; conditional; todo)
  Owner: Engineering
  Inspect the actual AAB and every native SDK dependency for 64-bit and 16 KB page-size compatibility. Save bundle/Console validation and device evidence; Java/Kotlin-only apps are compatible by default. Do not assume a deadline extension.

- [ ] Validate the native eSIM provisioning path (Apple; conditional; todo)
  Owner: Engineering
  If using CTCellularPlanProvisioning, validate the required public-cellular-plan entitlement, distribution profile and real-device provisioning. QR/manual-only installation follows a different route; document which route the release actually uses.

- [ ] Map actual data and SDK behavior (Both; required; blocked)
  Owner: Privacy owner
  Inventory identifiers, eSIM/network data, transactions, diagnostics, support and analytics. Determine collection, sharing, purposes and retention from the actual build.

- [ ] Publish and verify a privacy policy (Both; required; blocked)
  Owner: Privacy owner
  Provide a public privacy URL and in-app access. Verify owner contact, data practices, retention and deletion. Do not publish a generic policy as if it reflects the app.

- [ ] Complete privacy disclosures (Both; required; blocked)
  Owner: Privacy owner
  Complete App Privacy and Data safety from the verified data map. No “no data collected”, “no tracking” or “no ads” answers are assumed.

- [ ] Implement and test account deletion (Both; conditional; blocked)
  Owner: Engineering
  If accounts can be created: in-app deletion for Apple; an in-app route plus a public external deletion-request URL for Google. Deactivation alone is not sufficient.

- [ ] Review SDK manifests, signatures and permissions (Both; conditional; todo)
  Owner: Engineering
  Audit required-reason APIs, listed SDK privacy manifests and binary SDK signatures, including repackaged listed SDKs. Review runtime permissions. Request ATT only if the app actually tracks under Apple’s definition.

- [ ] Verify the login experience (Apple; conditional; todo)
  Owner: Engineering
  The supplied UI shows social login. Confirm implemented providers and §4.8 equivalent-login requirements or an applicable exception.

- [ ] Confirm the eSIM payment classification (Both; required; blocked)
  Owner: Product / legal
  Document each SKU, consumption, merchant model and checkout. Telecom/outside-app treatment may apply, but no blanket prepaid-eSIM exemption is presumed.

- [ ] Prepare a working review account (Both; conditional; blocked)
  Owner: Engineering
  Provide full/free review access, no expiring OTP dependency, clear installation instructions and a safe provisioning path. Store secrets only in the consoles.

- [ ] Complete age and audience questionnaires (Both; required; todo)
  Owner: Product
  Answer age rating, target audience, content rating and ads declarations from actual features and SDK behavior. Do not assume 4+ or Everyone.

- [ ] Assess export compliance (Apple; required; todo)
  Owner: Engineering / legal
  Inspect encryption usage and answer Apple’s export-compliance flow for the actual binary. Do not automatically set ITSAppUsesNonExemptEncryption to false.

- [ ] Declare Apple trader status (Apple; required; blocked)
  Owner: Founder
  Declare actual trader status even when not distributing in the EU. This is separate from conditional EU trader contact verification.

- [ ] Verify EU trader public contacts (Apple; conditional; blocked)
  Owner: Founder
  If distributing as a trader in the EU, verify the public legal address, phone and email. Approve what will be displayed; do not infer legal status.

- [ ] Verify Android package registration (Google; conditional; todo)
  Owner: Engineering
  Confirm the actual package/signing key is registered under Android developer verification for selected territories. Most Play apps are automatically registered, but verify Console status rather than assuming it.

- [ ] Resolve personal-account testing gate (Google; conditional; todo)
  Owner: Release owner
  If a personal account was created after 13 Nov 2023: 12 testers continuously opted in for 14 days, then production-access approval. Account type/date are unknown.

- [ ] Run real-device release QA (Both; required; todo)
  Owner: QA
  Test unsupported/locked phones, installation, payment failure, low/no connectivity, top-up, deletion and accessibility. Native eSIM functions cannot be certified from a web gallery.

- [ ] Verify support and public URLs (Both; required; blocked)
  Owner: Product
  Confirm live support, privacy and deletion pages. A proposed URL is not evidence that a page exists or meets policy.

- [ ] Choose rollout and release control (Both; recommended; todo)
  Owner: Release owner
  Recommend manual Apple release after approval. The first Google production release cannot use a percentage rollout: it reaches all eligible users in selected countries. Confirm territories, launch timing and monitoring; percentage rollouts are for later updates.

- [ ] Final submission review (Both; required; blocked)
  Owner: Release owner
  Compare every listing asset and declaration to the signed build. This workspace does not submit to either store.
