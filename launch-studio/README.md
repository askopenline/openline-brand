# Openline Brand Studio

> Openline company documentation: maintained in [askopenline/openline-brand-assets](https://github.com/askopenline/openline-brand-assets). See the [repository README](../README.md) for ownership, scope, and release boundaries.

Openline's brand-review workspace for app icons, store artwork, listing-copy drafts, and launch handoffs. This React/Vite application is part of the official [Openline brand-assets repository](https://github.com/askopenline/openline-brand-assets).

## Current scope

The studio separates the approved visual direction from submission readiness. Its Main view presents the final icon, device and store previews, and current downloads; Archive retains the broader review workbench and earlier comparisons.

- **Final icon:** The approved flat composition uses 43.5% visible mark width in a white square.
- **Marketing artwork:** The selected orange/cream direction is the presentation master.
- **Submission drafts:** Apple and Google have separate compositions, wording, and readiness records.
- **Preview limitations:** Phone shells are simulations and supplied React-screen captures are design references, not native-device acceptance evidence.
- **Version:** Consult [`package.json`](package.json) and repository history rather than treating older release notes as current instructions.

The existing hosted preview is [openline-brand.fly.dev](https://openline-brand.fly.dev). Its deployment is independent of this company repository copy and does not automatically follow Git pushes.

## Run locally

From this directory:

```sh
npm ci
npm run dev
```

Build and preview the production bundle with:

```sh
npm run build
npm run preview
```

The development server uses port 5173 by default. Review [`hosting/README.md`](hosting/README.md) before any deployment; do not treat a successful local build as permission to update a live service.

## Review and save work

The studio has no public write API or shared review database. Review notes, checklist state, and edited copy are held in the active workspace; use Save workspace to export the JSON and Import workspace to restore it.

Prepared ZIPs represent committed baseline resources, not unsaved session edits. Do not enter credentials, private legal documents, customer records, or account-recovery information into a publicly hosted review tool.

## Resources and release gates

| Resource | Location or guide |
| --- | --- |
| Final icon package | [`public/downloads/final-icon/`](public/downloads/final-icon/README.md) |
| Native icon guidance | [`icon-package/README.md`](icon-package/README.md) |
| Apple draft readiness | [`openline-apple-submission-readiness.md`](public/downloads/openline-apple-submission-readiness.md) |
| Google draft readiness | [`openline-google-submission-readiness.md`](public/downloads/openline-google-submission-readiness.md) |
| Copy-review record | [`submission-copy-review.md`](public/downloads/submission-copy-review.md) |
| Screenshot review | [`screenshot-compliance-review.md`](public/downloads/screenshot-compliance-review.md) |
| Submission audit | [`submission-audit.md`](public/downloads/submission-audit.md) |
| Requirements references | [`store-requirements.md`](public/downloads/store-requirements.md) |

These are dated review records, not a certification of current store policy or approval. Recheck native captures, app behavior, visible sample data, pricing and network claims, OMDM availability, platform metadata, and store-console requirements before submission.

## Icon integration

The vector exports preserve the source mark geometry, and the native kit includes platform-specific resources. SVG/PDF artwork is not a native Illustrator `.ai` document, and Icon Composer source layers are not a compiled `.icon` file.

The smaller Android adaptive treatment is an explicit visual experiment that still requires native legibility and mask testing. Keep the included 48dp reference available, and validate appearance in signed builds rather than relying on browser mockups.

## Regeneration and packaging

Rendering and packaging helpers live in [`scripts/`](scripts/). Select the helpers that match the current artwork family, inspect their input/output paths, and regenerate only the intended resources.

For the separate submission packages, the existing sequence is:

```sh
# Keep the Vite development server running in another terminal.
node scripts/render_submission.mjs
python3 scripts/package_submission.py
python3 scripts/package_resources.py
```

Inspect rendered images, text fit, archive contents, checksums, and download links after regeneration. Historical renderers can recreate superseded artwork; do not run every script as a generic release command.

## Attribution and stewardship

Openline maintains the studio, company-created artwork, and review documentation. Third-party marks and competitor reference images retain their own rights and are not Openline assets to redistribute; preserve attribution and keep reference material out of company download bundles.
