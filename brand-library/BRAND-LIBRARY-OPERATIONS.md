# Openline brand library

The v2 library is a static React/Vite application with a versioned catalogue. It preserves the app/store studio at `studio.html` and the previous creative gallery at `brand-expansion/index.html`; no account system, database or runtime API key is required.

## Build and run

```sh
npm ci
npm run dev
npm run build
npm run preview
```

The build creates `dist/`, including all public assets. On the same filesystem the final asset step uses hardlinks to avoid duplicating large media files; it falls back to copying across filesystems.

## Catalogue and new content

- **Source of truth:** the public repository snapshot recorded in `public/library/catalog.json`; files retain pinned source URLs and original filenames.
- **Editable catalogue builder:** `tools/build-library.py`, with `OPENLINE_ASSET_REPO` and `OPENLINE_PRODUCTION` environment overrides for source checkout and production folders. It preserves the catalogue's pinned source commit; set `OPENLINE_SOURCE_COMMIT` explicitly to adopt a newly verified upstream revision. Locally edited source files are restored from that commit when creating the public snapshot.
- **Public creative assets:** selected final media only. Do not publish API credentials, generation request payloads, private reference files, private receipts or unlabelled raw presenter takes.
- **New collection workflow:** validate each final manifest, integrate its selected files, rebuild the catalogue, generate missing posters, package the approved public files, run QA, then build.
- **Review status:** new campaign concepts remain `Review`; source assets and archives keep their separate provenance. The 43.5%-width app icon remains the approved icon.

For this production workspace:

```sh
python tools/package-library-collections.py
python tools/build-library.py
python tools/library-posters.py
npm run build
```

Use the pinned upstream source revision. The builder reads that commit's tracked tree rather than including untracked generated mirrors, so local handoff folders do not recursively become canonical source assets.

## GitHub handoff

The working copy was refreshed from `askopenline/openline-brand-assets` at commit `74f6cccad9f9149a3141b35883e66326054fd8d6`. The connector reports `READ`, so local preparation is not proof of a remote push.

Once write access is available, preserve the latest repository README, update the studio source, include selected final media and manifests, and retain the old directions in the archive. Keep generated collection ZIPs as release downloads where appropriate rather than silently dropping their contents from the resource catalogue.

## Live Fly deployment

Published and verified on 2026-10-24 at https://brand.openline.com, with https://openline-brand.fly.dev as the Fly address. DNS and Let's Encrypt certificates are active. The user explicitly chose always-on hosting, not scale-to-zero.

- App: `openline-brand`, region `cdg`.
- Active Machine: `867543ae795138`, one shared CPU, 256 MB RAM, autostop disabled, minimum one running Machine.
- Persistent encrypted volume: `vol_re1q7zyz7wlw2qo4`, 3 GB mounted at `/data`; five-day snapshot retention.
- Nginx serves `/data/current`. No database, runtime AI, or dependency on Perplexity hosting.
- Legacy Machine `8d7155be3ed118` is stopped and removed from public routing, retained as a rollback reference.
- Base bundle SHA-256: `1660f95633b32a03a34ef4d3d448251976444dde145c275a7b903d1a9c0106cf`. A separately verified small frontend delta updates the custom-domain footer.

The one-off release workflow is recorded in `scripts/fly_library_deploy.py`; deployment receipts live outside the public project in `../openline-fly-deployment/`. Its temporary upload route was removed during activation. Do not blindly repeat `stage`, reset the volume, or run a Docker deployment that detaches the current persistent assets. Inspect the active configuration and preserve a rollback before the next release.

Configured DNS, using DNS-only mode:

| Type | Name | Value |
|---|---|---|
| CNAME | `brand` | `w09ly3d.openline-brand.fly.dev` |
| CNAME | `_acme-challenge.brand` | `brand.openline.com.w09ly3d.flydns.net` |
| TXT | `_fly-ownership.brand` | `app-w09ly3d` |

Verified on the actual custom domain: all seven content routes plus overview, mobile navigation at 375 px without overflow or broken loaded images, presenter and short-ad playback, legacy `studio.html`, HTTP 206 range requests, and a full 30-ad ZIP download whose checksum matches the local master and whose archive integrity passes. Fly health checks are passing. GitHub synchronization remains separate and blocked by the connector's READ access.

## Acceptance gates

### Voiced campaign release 2.1

Published and verified on 2026-10-25 at https://brand.openline.com. The active release is `/data/releases/brand-2-1-64b698cf71a7`; its streamed transfer SHA-256 is `0a6ed0a4e6ed566ed4356a6686843836a4d64e28e54812cd716419e3a1d842a6`.

The live catalogue reports 40 ads, five presenter entries, 320 collections and 1,924 indexed files. All eight library routes, the retained studio, mobile navigation, real media playback, captions and ZIP delivery were checked on the custom domain; all ten new MP4s return HTTP 206. The temporary upload endpoint returns 404, the Machine health check passes, and the previous release remains available for rollback.

The new collection adds ten 22.08-second voiced ads and one 12.27-second Hellen continuity audition. It retains the earlier 30 ads, all four longer presenters, original logo/GIF files and the approved app icon. Campaign copy and all ten final mixed-audio videos received an OpenRouter review; Hellen is explicitly an unapproved fixed-voice pilot, not a completed installation tutorial.

`tools/integrate-voiced-campaign.py` builds the new public selection and download ZIP. Its baseline is the saved v2 catalogue in the private deployment state directory. Run it after the original catalogue builder if rebuilding from scratch; otherwise the campaign entries would be omitted. `tools/record-campaign-costs.py` updates the aggregate public cost summary and records unresolved billing replies privately. Never publish `_private/`, provider payloads, receipts or raw presenter takes.

`scripts/fly_incremental_release.py` publishes only an explicit changed-file list to the existing Machine. `bundle` records the manifest without making a large local tarball; `prepare` checks identity/storage and enables a short-lived private upload route. Run `upload` outside the credential proxy to stream the tar through HTTPS. Run `verify`, `status` and `activate` with the Fly Machines credential. Activation switches the `/data/current` symlink and removes the upload route, retaining the previous hardlinked release for `rollback`. Do not use the original one-off `stage` or `prepare-transfer` operations.

The new ads are marketing concepts for review, not claims of platform approval. Their scenes and voices are AI-generated; they do not show real customers, actual app UI or measured network performance. The full tutorial still requires real iPhone capture, verified activation/reinstallation rules and the user's voice/quality approval.

- Desktop and 375px mobile navigation, catalogue search, filters, no-results state and reset.
- Media preview, native video controls, keyboard/Escape dismissal, captions and file downloads.
- Existing icon/device/store preview tools remain reachable and their content unchanged.
- Counts are derived from actual files, not planned productions.
- No claim that store drafts are a fully approved submission or that AI presenters are human.
- New public hosting and GitHub synchronization are reported separately from the attached preview.

## Tutorial and campaign releases 2.2–2.3

Published on 2026-10-25 at https://brand.openline.com. Release state and rollback metadata are outside the public tree in `../openline-fly-deployment/tutorial-v2-2/` and `../openline-fly-deployment/campaign-v2-3/`. Use the incremental release script with the corresponding `--release-key`; never reuse another release's transfer state.

The full Hellen tutorial is an approximately 89-second continuous presenter take with one Ashley narration master, a softly blurred fictional office, and a clearly labeled illustrated installation guide. The user explicitly approved the illustrated format instead of genuine iPhone footage. The presenter is not time-spliced; instructional panels transition independently. A constant spatial crop removes unwanted generated text. Mild synthetic artifacts may remain, and plan-specific activation/reinstallation rules are not invented. The prior pilot remains historical, not the featured tutorial.

The ten revised campaign videos retain their original audio streams and generated scenes. They add speech-aligned word-pop captions, remove mid-screen message blocks, separate the logo motion, QR and URL in the outro, and retain a white-circle AI badge after “Generated by” begins disappearing at 1.2 seconds. The original ten-video edition remains in Archives. There are still 40 active ads, not 50.

The v2.3 catalogue contains 322 collections, 1,985 indexed files, 40 ads and six presenter entries. All ten revised MP4s passed whole-file decoding, unchanged-audio hash checks, QR checks and audiovisual review. Local browser checks passed for all eight routes, 30/40-ad pagination, tutorial playback, the legacy studio and 375px overflow. A fresh production browser check was unavailable because the retained sandbox is incompatible with the newly introduced browser harness; do not claim that check was performed. Production checks confirmed the exact v2.3 catalogue bytes, range delivery for all ten revised MP4s, both ZIP lengths and initial-byte matches, tutorial delivery and removal of the temporary upload endpoint. The complete uploaded release archive passed its SHA-256 check before activation.

Public entry points:

- Campaign: https://brand.openline.com/#/ads
- Tutorial: https://brand.openline.com/#/presenters
- Revised ads ZIP: https://brand.openline.com/library/downloads/openline-ten-voiced-campaign-ads-v2.zip
- Tutorial ZIP: https://brand.openline.com/library/downloads/openline-hellen-full-tutorial.zip

New tutorial API costs were USD 4.066432 Runware and USD 0.0231141 OpenRouter. Ad revision required no new Runware generation; audiovisual review cost USD 0.0276247 OpenRouter. The aggregate ledger now records USD 69.195994 Runware and USD 0.2770482 confirmed OpenRouter charges, with two historical blank-response calls still unreconciled. The USD 100 Runware ceiling is not a spending target. Hosting and Computer usage are excluded.

Reproduction order after the earlier catalogue integrations: `tools/integrate-full-tutorial.py`, then `tools/integrate-pop-campaign.py`, followed by validation and the Vite build. Public-only file selection remains mandatory; never publish generation payloads, receipts, private source cuts or upload capabilities. GitHub synchronization is still separate from Fly publication and was not performed by these releases.

## Motion and layout release 2.4

GitHub synchronization completed on 25 October 2026: write access was verified and commit `c78916861e619f07a02721d330b7cb15adfbc86f` was pushed to `askopenline/openline-brand` on `main`. Earlier read-only notes below describe the preparation stage, not the current access state. Large runtime media remains distributed through the public-assets manifest rather than duplicated in Git history.

The Motion inventory is 150 collections: 65 preserved entries plus 85 new sound/layout editions. The new work combines 17 synthesized score families with five layouts, including 68 horizontal 1920×1080 editions and 17 native-square 1000×1000 editions. Every new video is 12.16 seconds at 50 fps, preserving four cycles of the exact 152-frame source GIF at its original speed. These are not 85 unrelated animation concepts.

Each edition offers an MP4 with AAC audio, lossless FLAC score, JSON sound-event score, and a shared layout JPEG/GIF preview. GIFs remain silent. Five visual layouts share posters and silent GIF previews intentionally; each sound arrangement differs. All 85 videos passed whole-file decode and zero-clipping checks. Decoded true peaks ranged from −5.19 to −4.77 dBTP. An automated audiovisual reviewer checked one complete sample from each of the 17 score families, covering all five layouts, and found no material issues. This was not a human listening session.

The catalogue has 407 total collection cards and 2,255 indexed files after including the representative-review summary and contact sheet. Motion adds all/new/horizontal filters and FLAC support. Presenters now has a wrapping action row with a 24px desktop gap and stacked mobile buttons. Select controls use a consistently inset chevron with reserved right padding.

Local QA exercised all routes, all 150 Motion cards through pagination, the new 85/68 filters, FLAC filtering, empty/reset states, landscape media playback, tutorial CTA, legacy studio and 375px layouts without overflow or application errors. Private state lives in `../openline-fly-deployment/motion-v2-4/`.

The canonical repository was renamed by the user to https://github.com/askopenline/openline-brand. Documentation preparation covers all 61 previously tracked Markdown files: 20 editorial refreshes and 41 historical/preparation annotations, plus six new guides. Historical findings are not rewritten as current guarantees. Source and documentation synchronization to GitHub requires write access; the connected `paulfxyz` account reported read-only access during preparation. A prepared patch is not a completed remote push.

`tools/prepare-repository-handoff.py` prepares lean application source plus `PUBLIC-ASSETS.json`; `tools/hydrate-public.py` downloads explicitly opted-in runtime files with size/SHA-256 checks. Large public media remains available on the live domain rather than duplicated into Git history. Media generation incurred no new Runware charges. Documentation drafting/review cost USD 0.1505031 and representative audiovisual review cost USD 0.0283717 through OpenRouter.
