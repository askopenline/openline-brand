# Openline brand library v2 QA

The library replaces the launch-only landing page while preserving the mobile workbench and earlier creative gallery. This report records local checks; hosted verification is a separate gate.

## Content acceptance

- Thirty short-ad concepts are present: the eight earlier videos plus twenty-two new directions. The new directions have original sound design; the two original examples remain silent.
- Twelve new original-GIF editions run for exactly twelve seconds, with MP4, WAV, JPEG and reduced silent GIF derivatives.
- Gary 01, Gary 02, Gary 03 and Hellen 04 each have a 24-second video track. Their MP4 containers report 24.114667 seconds because of the short audio tail.
- Presenter exports include 1920×1080 landscape, 810×1080 portrait, JPEGs, silent GIFs, WAVs and English VTT/SRT captions. Portrait is 3:4, not 9:16.
- The catalogue has 309 asset collections and 1,848 indexed files, including all 897 tracked files from source revision `74f6cccad9f9149a3141b35883e66326054fd8d6`.
- The approved icon checksum remains `5bded92247397e8999be6d0f668bbb7facca064136dbfe45a043d0fc9e54b60b`.
- Source README bytes were compared with the pinned Git blob after local handoff edits; they match.

## Interaction checks

- All eight library routes render at 1440px and 375px with no measured horizontal overflow or broken completed image loads.
- Search, collection/format/status filters, no-results reset, file view, pagination and colour-copy feedback work.
- Video playback, metadata, seeking into the third presenter chapter, landscape/portrait switching and caption-track loading work.
- Modal dismissal via Escape restores focus to the triggering preview button.
- Catalogue-load failure shows a retry action; retry restores the library after the failed request is removed.
- Failed video loading shows a useful fallback while leaving downloads accessible.
- A real final-icon ZIP download and legacy workspace JSON export succeeded through browser download events.
- Original iPhone/Android preview opening, navigation, store-edition switching, store-image enlargement, checklist editing/restoration and Archive/Main routes remain operational.
- No new JavaScript page errors were observed in the exercised local flows.

## Packaging and limitations

The all-30-ads bundle contains sixty video/poster entries. The twenty-two-new-ads source bundle contains 101 entries; the original-GIF sound pack contains 54; the four-presenter pack contains 34, including a sanitized manifest and README. ZIP integrity checks passed.

AI presenters remain visibly disclosed. The samples are edited comparisons, not a complete installation walkthrough or real device recordings. Mild synthetic cadence remains, music beds were reported in Gary 02/Hellen 04, and Gary 03's beanie tip touches or slightly clips the top edge in some frames. These limitations were not concealed with fabricated footage.

The new ads use contextual existing artwork, not native app captures. Source-photo rights were not independently re-audited. Campaign concepts and app/store drafts remain review material.

## Publication status

The canonical GitHub repository reports `READ` access. An additive local handoff is prepared on `brand-library-v2`, but no remote push or release upload is claimed. ZIP release assets require their separate publication/binding step.

Fly configuration is prepared; this revision has not changed the existing Fly deployment or connected `brand.openline.com`. The attached preview is the intended review delivery.

## Hosted verification

The same attached app was updated in place as Openline Brand Library v2.0.0. A fresh browser context confirmed the hosted catalogue, all thirty ads, all four presenter cards, Hellen playback, a twelve-second motion edition, the preserved iPhone preview and mobile navigation at 375px.

The hosted all-thirty-ads ZIP downloaded successfully and passed archive integrity checks. Its SHA-256 matches the local bundle: `f46ba7b8cef989532d5b2fbb5e8aa9ce840dac290dadf2f234130616fac31a25`.

No JavaScript page errors appeared in the exercised hosted flows. The public wrapper presented browser security verification to automation, so functional checks used the deployment tool's authorized temporary preview URL; that temporary URL is not a user-facing deliverable.
