<!-- OPENLINE-GUIDE-VISUAL -->
![Brand Assets: company resource guide](https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/.github/assets/guide-header.png)

# Openline Mobile - app screens (buildable export)

Registered in the media kit as part of **v1.4**. See the [mobile resource index](../README.md), [native Figma snapshot](../../figma/mobile/README.md), and [iOS/Android app icons](../../app-icons/README.md).

Extracted from the main Openline site on 24 Sep 2026 for the company's mobile
implementation handoff. The gallery includes its own source and asset
dependencies, but it remains a web-based design reference rather than the
production native application.

Companion delivery: the same 19 screens as native Figma frames, in the
shared file - https://www.figma.com/design/xOFkfha4CK3pNQQz46tKzo/ , page
"Openline Mobile - app screens" (rebuilt frames) and page "Mobile screens -
22 Sep - 19 frames (capture)" (pixel captures of this exact code, for
side-by-side reference).

## What's in here

- `src/components/MobileScreensPage.tsx` - all 19 screens: Login, Dashboard,
  My eSIMs, Plans (3 steps), Checkout, Payment success, eSIM profile, Me,
  Settings, Slow connection / offline, and six variant states (empty list,
  no search results, payment declined, wrong login code, a dense 9-eSIM
  list, notifications prompt). One component, no router - each screen is a
  function, selected by the on-device switcher or the gallery grid.
- `src/components/PaymentLogos.tsx` - the card/wallet network marks used on
  Checkout and Payment success (Visa, Mastercard, Apple/Google Pay, Alipay,
  WeChat Pay, crypto, etc.), as real SVG paths - no image dependencies.
- `src/imports/svg-*.ts` - the raw path data those logos are built from.
- `src/assets/*.png` - four images: the Openline mark, and the three
  payment logos that ship as bitmaps in the original set (Alipay, WeChat
  Pay, Bitcoin) rather than vectors.
- `src/index.css` - the site's precompiled Tailwind stylesheet. It is
  precompiled (no PostCSS step) and already contains every class this page
  uses - see "if you edit this" below before adding new classes.
- `preview/` - a pre-built static copy (`npm run build` output), so you can
  look at it before running anything. Serve it with any static server, e.g.
  `npx serve preview` or `python3 -m http.server -d preview 8000`, then open
  the printed URL. It won't open directly as a `file://` URL - it's a single-
  page app and needs to be served.

## Running it

```
npm ci
npm run typecheck
npm run dev       # http://localhost:3000
```

or to rebuild the static output:

```
npm run build      # writes to build/
npm run preview    # serves that build
```

The repository uses `base: "./"` in Vite so built assets resolve when hosted
under a subdirectory. To refresh the checked-in static copy after editing:

```sh
npm run build -- --outDir preview
```

Commit the refreshed `preview/` alongside its source changes. Do not commit
`node_modules/`, the disposable `build/` folder, or local environment files.

No env vars, no backend, no auth - every screen is populated with realistic
mock data (see "Mock data" below).

## How the screens are organised

`MobileScreensPage` renders two views, both driving the same 19 screen
components:

- **Gallery** (default): all screens in a scrollable grid, for a fast scan.
- **On-device view**: one screen at a time inside an iPhone-shaped frame
  (`DeviceView`, 340x700 logical px), with Back/Gallery, a Previous/Next
  pager, and a screen picker. Opens automatically on a narrow viewport, or
  via the "Open on-device view" button. The URL takes `?view=device` or
  `?view=gallery` and `?screen=<name>` to open directly on a specific
  screen (read once at module load into `LAUNCH_QUERY`) - useful for
  linking a teammate straight to one screen.

Shared building blocks worth knowing about, all in this one file:

- `CopyableField` - the ICCID / SM-DP+ / activation-code rows on the eSIM
  profile screen. Tap to reveal the full value and copy it; collapsed it
  shows a truncated preview. Real-length values (see Mock data).
- `ConnectionScreen` / `ConnectionMark` - the slow-connection / offline
  state, using the Openline mark as the loading spinner over the screen
  you came from, so context isn't lost. Two states (slow / offline).
- `CheckboxRow`, `RadioGroupRows` - the settings-screen form controls.

## Mock data (replace with real integration)

- ICCID: `8944478100001234567` (19 digits, real length)
- SM-DP+ address: `consumer.rsp.openline.com`
- Activation code: `TN202612040982590B44A913`
- Card on file: `•••• 4242`
- Plan pricing, country list, eSIM list: all inline arrays near the top of
  `MobileScreensPage.tsx` - each screen's own function is preceded by a
  banner comment (e.g. `/* ---- DASHBOARD ---- */`, `/* ---- SETTINGS ---- */`);
  search for the screen name to jump to its component and its data.

None of this reaches a network - there is no fetch/axios/API client in the
file. Wiring it to the real backend is entirely additive.

## If you edit this

`src/index.css` is a **precompiled** Tailwind build, not a Tailwind config -
there's no build step that generates classes on demand. Any class you add
in JSX that isn't already in this stylesheet will silently do nothing (no
error, the element just renders unstyled). The main site guards this with a
script (`scripts/check-classes.mjs`, not included in this extract since it
walks the whole site); if you add real UI here, either reuse an existing
class already in `index.css`, use an inline style, or hand-add a rule to
the `@layer utilities` block at the bottom of `index.css`.

## Questions

Coordinate design questions through Openline's design and product team, and
check the current mobile implementation handoff before changing approved
screens. The companion site repository may carry additional delivery context.

<!-- OPENLINE-GUIDE-NAV -->
## Company reference

This guide belongs to [Openline Brand Assets](https://github.com/askopenline/openline-brand-assets), maintained by Openline. Return to the [project overview](../../README.md) for the broader system, current company links, and release context.
