# Brand Studio QA

## Revision 03 / v1.7.0 verification inventory

7 October 2026. This pass covers all eight views at 1440px and 375px, light/dark
overview, final-icon download links and format validity, screenshot gallery on
both platforms, modal keyboard handling, independent Apple/Google approvals,
schema-2 migration, new 33-task state, copy limits, save/import and invalid import.
Off-happy paths: malformed JSON must not change state; old completed artwork and
expanded technical checks must reopen without undoing the final icon decision.
Review all twelve compositions, contrast, text/phone bounds, feature graphic,
native resources, vector paths, alpha, export sizes and archive checksums.
Deployment verification must compare the live launch-kit hash with the local kit.

Completed local pass:
- Eight desktop and eight 375px mobile views pass overflow and page-error checks.
- Light/dark overview and mobile views inspected after transitions settle.
- All 14 direct final-icon/package/manifest links return 200.
- Final-format validator passes 18 Apple catalog references, opaque Play icon,
  five Android densities, vector-path presence, EPS header, PNG dimensions/
  coverage, 37 file checksums, alt-text limits and archive integrity.
- Schema-2 import preserves copy/notes, adds new tasks, clears obsolete artwork
  approvals, reopens expanded technical requirements and retains final icon approval.
- Apple card approval does not approve Google; both retain independent choices.
- Malformed import is rejected; copy over-limit fields flag errors; Escape closes
  image modals. Workspace JSON exports contain 33 tasks and the final icon state.
- All 12 artboard text/phone bounds and the feature graphic pass layout checks.
- Removed Apple Wallet from the Android profile reference; fixed the orange
  card headline/accent contrast and monochrome brand treatment.

The historical checks below describe prior milestones; the current final icon
is approved and its comparison controls are intentionally removed.

Checked October 6, 2026. This is browser and asset-package QA, not native app
certification or store acceptance.

## Verified

- Production Vite build completes successfully.
- All eight workspace views, including Competitor review, render on desktop and mobile without horizontal overflow.
- Light and dark themes render correctly.
- Icon-size, tone, store-platform and Android-mask controls update their previews.
- Checklist status, owner, evidence notes, search and platform/status filters work.
- Copy character limits show errors for over-limit drafts.
- Save/import restores the workspace, including checklist notes and review state.
- A malformed workspace is rejected without changing state.
- Artwork previews open, Escape closes dialogs, and keyboard focus is kept inside dialogs.
- ZIP download controls trigger file downloads.
- No browser page errors were observed during the interaction pass.
- Native icon dimensions, Apple opacity, Play size/alpha, artwork dimensions,
  RGB modes and ZIP integrity are validated by `scripts/validate_assets.py`.
- Revision 02: all twelve headline/deck pairs fit without overlap; Android
  compositions crop out the iOS-style status bar from the supplied design screens.
- Revision 02: 10%, 15% and 20% icon-reduction options resolve to the correct files.
- Schema-1 imports preserve user copy and notes but clear obsolete artwork
  approvals and return completed artwork-review tasks to review.
- Revision 03: new 42.2%, 43.5% and 44.8% masters resolve correctly; desktop and
  375px mobile icon views have no horizontal overflow or browser errors.
- Revision 03: older completed icon approvals return to review on import.
- Revision 03: adaptive candidate and 48dp fallback bounds are validated at all
  five Android resource densities.

## Production verification: Fly.io

- https://openline-brand.fly.dev serves the studio over HTTPS.
- Machine `8d7155be3ed118` in `cdg` reports a passing HTTP health check.
- All eight views render without browser page errors or horizontal overflow.
- Desktop icon canvas and 375px mobile overview visually checked.
- Default remains Candidate 03, 43.5%; the white square is unchanged.
- Public launch-kit ZIP downloads successfully and passes ZIP integrity checks.
- Hosting uses one shared CPU, 256 MB, shared IPv4/IPv6 and idle autostop.
- Vercel placeholder remains unused. Git pushes do not automatically deploy to Fly.

## Still required

- Final visual approval of the 43.5% icon candidate (another ~17.5% smaller than
  52.7%), with 42.2% and 44.8% alternatives for approximately 20% and 15% reductions.
- Android adaptive legibility testing: the 39.6dp experimental candidate is below
  the recommended 48–66dp artwork range. The prior 48dp fallback is preserved.
- Real iOS and Android device testing, including adaptive masks and Apple appearances.
- Native release screenshots to replace the labelled React design references.
- Verification of production claims, plan prices, permissions and data handling.
- Developer account, app identifiers, privacy, deletion, payment, age-rating,
  reviewer-access and legal answers in the actual consoles.

Use `public/downloads/store-requirements.md` for the official guidance and
`public/downloads/openline-release-checklist.md` for the complete baseline.
