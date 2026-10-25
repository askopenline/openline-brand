> Historical or submission-preparation reference. This document records its original scope and date; it is not current store approval or evidence of a production release. See the [current brand library](https://brand.openline.com/) and [repository documentation](https://github.com/askopenline/openline-brand/tree/main/docs).

# Openline screenshot production handoff

Revision 03, 7 October 2026. Six iPhone and six Android compositions share one
editable JSON narrative and HTML layout. They are labelled design previews with
sample data, not native release screenshots.

## Art direction

One benefit per card, two short headline lines, a quiet secondary sentence,
generous margins and a complete, upright phone. Warm white, pale peach and one
orange card preserve Openline's identity. The phone no longer overwhelms the
canvas: iPhone width is 840/1320px; Android width is 576/1080px.

The reference is Saily's clear headline/product hierarchy, not its blue/yellow
palette, hand photography, copy or product promises. Its listing was inspected
on 7 October 2026: https://apps.apple.com/us/app/saily-esim-data-for-travel/id6475045151

## Narrative and later capture replacement

| Order | Tagline | Source now | Native capture required later |
|---|---|---|---|
| 01 | Go places. Stay connected. | Countries | Supported destinations, real approved prices and coverage |
| 02 | Your trip. Your kind of plan. | Plans: duration options | Actual SKU terms, duration, total price and accurate unit price |
| 03 | Setup details. Close at hand. | Activated eSIM profile | Real installation/detail flow with sanitized, nonfunctional example identifiers |
| 04 | Know your data. Enjoy your day. | Dashboard | A native balance view with verified usage-update semantics |
| 05 | Every eSIM. One place. | My eSIMs | Implemented states, truthful balances and supported actions |
| 06 | Your account. Made simple. | Me | A safe demo profile with only implemented account features |

Slide 06 replaces the old settings screen, which showed unverified automatic
network switching and ad/tracker blocking. The new account reference still has
sample savings/referral/Openline+ labels: remove or substantiate them when
capturing the mature app. Do not treat a design screenshot as proof of a feature.

The Android profile reference specifically omits the Apple Wallet button from
the supplied React mockup. No Android wallet button or capability was invented
in its place. This adaptation remains a design preview, not an Android capture.

## Files and reproducible export

Download `openline-screenshot-sources.zip`. It includes `public/render.html`,
`public/artwork.json`, input captures, licensed fonts, render script and this guide.

```sh
npm install
npx playwright install chromium
npm run serve
# In a second terminal:
npm run render
```

The standalone source package serves `public/` at port 5173. In the complete
studio repository, use `npm ci`, `npm run dev`, then
`node scripts/render_artwork.mjs`. Set ARTWORK_BASE_URL for a different local URL.

## Native replacement procedure

1. Keep the original design input images in version history. Capture each flow
   separately from the actual iOS and Android release candidate.
2. Use dedicated demo data. Remove live customer details, reusable activation
   codes, working QR codes, private IDs, real card numbers and reviewer secrets.
3. Put native files under platform-specific paths in `public/assets/`.
4. Update `captures.ios` and `captures.android` for each slide in `artwork.json`.
   Never reuse an iOS screenshot as a final Android capture.
5. The current Android reference removes an iOS-style status strip using
   `.android .phone img { margin-top:-61px }`. Remove that rule for genuine
   Android inputs; preserve their native aspect ratio, status and navigation.
6. Fit the phone inside the artboard without distorting the image. Current
   reference inputs are approximately 340:700; native devices may differ.
7. Check prices, coverage, plan terms, balances, captions and every feature against
   the binary. Update copy rather than making the release UI match a mockup.
8. Keep review labels until signoff. The provided renderer deliberately rejects
   non-reference status; enabling release export requires an explicit code
   change after the native/copy audit, not just a hidden query parameter.
9. Remove the preview footer only for the verified final export. Recheck RGB,
   dimensions, order, locale, alpha and all supported device slots.
10. Upload through the consoles after all noncreative release gates are complete.

## Export specifications

- iPhone: 6 × 1320×2868 RGB PNG, one supported 6.9-inch portrait size.
- Android phone: 6 × 1080×1920 RGB PNG, 9:16, no alpha.
- Play feature graphic: 1024×500 RGB PNG, no alpha.
- No stretched iPad/tablet derivatives. Create native large-screen assets only
  after the supported device families are confirmed.
- Google alt text is supplied separately, within 140 characters per image.

Apple specifications:
https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications

Google asset and alt-text guidance:
https://support.google.com/googleplay/android-developer/answer/9866151?hl=en

Truthful metadata:
https://developer.apple.com/app-store/review/guidelines/
