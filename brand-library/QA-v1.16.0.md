# QA: Openline Brand Studio v1.16.0

## Functional and visual checks

- Existing iPhone/Android previews, screen selectors, next/previous and close controls exercised.
- Both listing previews switched between marketing and submission editions; screenshot six enlarged, returned and closed.
- Archive, Launch checklist, Main and Brand & motion navigation exercised.
- Thirty custom play controls advanced their videos and paused again. Starting a second player paused the first after the actual playback event.
- Earlier-ad details opened and closed. All 142 unique download URLs returned successful local responses.
- A real browser presenter-ZIP download matched the packaged file's SHA-256.
- Missing-video simulation in an isolated context displayed “Video unavailable. Please use the download pack.”
- Desktop → 375px mobile → desktop resizing passed. Header, presenter grids, motion grid, ads and downloads visually inspected; no horizontal overflow.
- Secondary text contrast measured 7.55:1 on the gallery background.
- Normal-flow page-error collection remained empty. No automatic audio playback.

## Media and copy checks

- Five new eight-second native presenter clips were decoded and reviewed in frame sheets and audio-input audits. Gary02 selected retake has a full, uncut introduction; some regular/flat cadence remains.
- Gary02 final wide/portrait files fully decoded. Video timing is eight seconds; the audio/container tail extends to 8.1 seconds. Final audio measured −16.8 LUFS and −1.3 dBFS true peak.
- Two earlier Hellen samples are explicitly distinguished from new Veo clips. AI disclosure remains visible; no location statement.
- New wide/portrait compositions retain source timing and generated speech; poster frames refreshed to avoid incidental mid-blink first impressions.
- Fourteen motion masters and six new ads have provider-independent decode, dimensions, duration and numerical audio QA in their packs. No human listening audition claimed.
- Gallery copy received OpenRouter proofreading. Its incorrect suggested interpretation of the 43.5% icon was rejected; the mark-width composition remains the intended meaning.
- Account credential identifiers removed from the public ledger and copied ad receipts. No raw API credentials included.
- Final complete bundle contains 180,216,023 bytes. Sanitized ad archive integrity passed.
- Approved icon SHA-256 remains `5bded92247397e8999be6d0f668bbb7facca064136dbfe45a043d0fc9e54b60b`.

## Final build and hosted check

Production Vite build passed. The existing attached preview was updated in place, retaining asset ID `2a5c000e-ebaf-42ce-bfc1-154792fb6b80`.

- A fresh browser context confirmed the v1.16.0 gallery, three Gary cards, four Hellen cards and fourteen new motion cards.
- Selected Gary02 retake, new Hellen04, a new motion composition and a new ad all played and paused through their visible controls.
- The actual hosted complete-ZIP download completed with no failure: 180,216,023 bytes, SHA-256 `15a4342185ec643ec443419885680973e56f8e9e7bacc9e6155122ef3b361720`, identical to the local release.
- At 375px, no horizontal overflow; return-to-studio navigation passed.
- Hosted iPhone preview opened and closed. Google Play listing opened, switched to Submission draft and closed.
- No page errors in the normal hosted flow. QA browser contexts closed after verification.
- GitHub and Fly were not updated.

## Deliberate exclusions

No native app recording, full tutorial, store approval, GitHub push or Fly deployment is claimed. Hellen01/03 upgrades remain blocked, and AI artifacts have not been guaranteed absent.
