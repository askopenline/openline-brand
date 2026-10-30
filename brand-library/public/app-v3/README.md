# Openline App & Store V3

V3 is a selection workspace with twenty candidates for each phone platform, three complete English listing-copy directions, interactive store/device previews and a source-linked submission review. The Final draft is a user-confirmed creative snapshot, not a submission to either store.

## Select and prepare

The [Recommended selection](https://brand.openline.com/#/app?version=recommended) is available without confirming Final:

- Apple: 01 → 02 → 11 → 04 → 19 → 10 → 17 → 06 → 15 → 18.
- Google: 01 → 02 → 11 → 04 → 19 → 10 → 17 → 18.

Its previews and downloads follow these orders. Existing V3 choices, listing copy, review answers and saved Final snapshots are preserved. “Use recommended in V3” copies only the screenshot selections into the editable draft; it does not confirm Final. New workspaces start with the recommendation and no Final snapshot.

Recommended previews and downloads use Direction A (Travel-first) for both stores, independently of existing V3 or Final copy choices.

Version 2.7.7 expands those Recommended descriptions with everyday travel uses, plan-choice explanations and a short getting-started flow. The [competitor copy audit](./recommended-copy-audit.md) compares the US-English Apple and Google listings for Saily, Holafly and Airalo. Its findings inform the structure, not Openline's product claims; longer copy does not establish submission readiness.

The revised Recommended edition uses `recommended-copy.json` and a separate candidate 11 image set. Its plan options read “Unlimited usage” and “Fixed usage,” as confirmed by the owner, without prices or currency symbols. Original V3 copy/images and saved Final views retain their earlier assets. Plan availability and applicable usage terms still require release verification.

Six product-verification flags appear on the Recommended page and in a separate `product-verification.md` inside each Recommended ZIP. They cover destination availability, unlimited-plan terms, installation, data-display behavior, real release screenshots and reviewer/privacy/support readiness. These flags are not overlaid on screenshots or inserted into the customer-facing descriptions. No review item is automatically marked complete.

Enlarged screenshots support arrow buttons, keyboard arrows and mobile swipes. Swipe left for the next screenshot or right for the previous one; navigation wraps around and follows the selected order, or all twenty options when opened from the candidate grid. Vertical scrolling and pinch zoom remain available, and browsing never changes a selection.

Concepts 15, 17, 18 and 19 remain subject to product validation. Candidate 15 requires actual in-app network choice; use 05 instead if that interface does not exist.

- **Apple:** choose and order ten candidates. Download contains 1320×2868 PNGs and a separate 1206×2622 folder for the currently required Dynamic Island medium-display family; upload each family into its corresponding size slot, not both sets into one slot. Apple allows up to ten screenshots per size ([Apple specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)).
- **Google:** choose and order eight candidates. Download contains 1080×1920 PNGs, the 512px icon and a 1024×500 feature graphic. Google allows up to eight screenshots per device type ([Google specifications](https://support.google.com/googleplay/android-developer/answer/9866151?hl=en-GB)).
- **Text:** choose A, B or C independently for each platform. The selected copy, screenshots and order feed the preview and generated ZIP.
- **Final:** confirm the creative selection to save a fixed snapshot. Return to V3 to make another selection; V1/V2 remain unchanged archives.

## Persistence and privacy

Selections and non-sensitive review notes save in this browser. Export the review JSON as a portable backup, or use Share selection to carry only screenshot/copy choices and the final snapshot to another browser. Shared links exclude review notes. There is no shared server-side approval database; send the link or exported selection to the team when agreeing the final public edition.

Never enter passwords, reviewer-login credentials, API keys or signing material in the review notes. Enter those only in the stores' private submission systems.

## Artwork status

Candidates 13–20 are eight new imagined UI concepts: Europe browsing, arrival, network choices, data overview, installation checklist, help, dual-SIM guidance and language selection. They are not evidence of implemented features. The concept label is shown in the workspace, rather than stamped over the artwork. Validate every concept against the release build before considering it for a store submission.

Every Apple-related review field includes a copyable example. These are editable inspiration templates, not verified declarations. Replace bracketed placeholders, check applicability, and leave private reviewer credentials in App Store Connect. Copying an example does not mark a field reviewed. The Apple download also contains the example templates.

These are adaptations of supplied React app design resources, not captures from a verified native release. Monetary UI, unsupported promotional treatments and prototype-only controls were removed. QR/manual profile candidates 06/07 deliberately provide two views of the same source profile. Additional candidates are based on destination, package-type, account, expanded eSIM and notification resources. The white tile retains the V2 mark enlargement of 12.5%; original V1 icon approval is not changed.

Check each selected view and claim against the actual iOS/Android build before submission. Native screenshot evidence, iPad/other form factors, adaptive icons, app identifiers, privacy declarations, entitlement/billing classification, signed builds and account-specific console questions still require owner/engineering review. Final creative selection does not certify compliance or readiness.

## Reproducibility

Source capture and composition scripts are in the repository's `brand-library/scripts/`. `capture-provenance.json` records source panels, `layout-qa.json` records dimensions/geometry and `copy.json` contains the three entry directions. The application creates selected ZIPs locally without a paid service. API requests, prompts, receipts and private identifiers are excluded.
