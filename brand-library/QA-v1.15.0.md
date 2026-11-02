# QA: Openline Brand Studio v1.15.0

## Local build and regression

- Production Vite build passed.
- iPhone and Android previews opened; numbered selectors and next navigation worked; dialogs closed.
- Apple and Google listing previews switched between Marketing master and Submission draft, enlarged frame 6, returned and closed.
- Archive opened, Launch checklist was exercised, and Main returned to the clean mobile-resource view.
- Brand & motion navigation opened the new collection. Return-to-studio worked.
- Main and collection pages showed no horizontal overflow at 375 px; collection also passed desktop → mobile → desktop resizing.
- Missing Gary media was simulated in an isolated browser tab: a useful “Video unavailable” fallback appeared.
- No new page errors during final normal-flow checks.

## Presenters and motion

- All 13 preview videos loaded metadata without errors: four presenters, three remixes, four original motion clips and two ads.
- All seven new Play buttons advanced their video; playback is user-initiated and unmuted. Starting another video paused the previous one.
- Gary duration: 7.2 seconds. Each Hellen: approximately 2.933 seconds.
- Three Hellen final audio tracks transcribed as the same neutral introduction, with no location. Gary's male narration transcribed correctly.
- Automated final audio review used actual audio-input tokens and reported no speech defects. It described both SFX tracks as quiet with distinct soft beeps.
- Every widescreen presenter MP4 fully decoded; H.264/yuv420p video, AAC audio and 1920 × 1080 dimensions verified.
- Half-second portrait frame sheets reviewed. Stray model-generated lettering in Gary and Hellen 03 was removed from final branded exports through documented post-production.
- New remixes: 3.04, 8 and 2.6 seconds, native 1000 × 1000, 50 fps. Original GIF byte identity, native MP4 SSIM and audio/no-clipping checks are supplied in the remix pack.

## Downloads and preservation

- All 33 distinct download URLs returned successful local responses.
- Actual browser download events completed for presenter, remix and complete collection ZIPs.
- Presenter ZIP integrity passed. Raw sources, fonts, exact-source logo PNGs and the portable composition script are included.
- Active Hellen captions, public notes and public HTML contain no retired location reference.
- Complete collection: 45,273,075 bytes.
- Approved icon SHA-256 unchanged: `5bded92247397e8999be6d0f668bbb7facca064136dbfe45a043d0fc9e54b60b`.

## Hosted check

- Attached preview updated in place to v1.15.0; same asset ID `2a5c000e-ebaf-42ce-bfc1-154792fb6b80`.
- Fresh hosted browser context opened the main page and exercised an iPhone preview.
- Brand & motion opened; Gary and Hellen 03 played successfully with correct durations. The sound-enabled extended remix also played.
- Actual hosted complete-ZIP download completed. A separate content check returned HTTP 200, 45,273,075 bytes and valid ZIP magic `504b0304`.
- Hosted GIF and JPEG downloads returned HTTP 200.
- At 375 px, no horizontal overflow. Return-to-studio worked and no page errors were logged.
- Fresh hosted QA context closed; local editing browser retained for further review.

## Limitations

These are creative review assets. Automated audio evaluation is not a human listening audition or a guarantee of perfect lip sync. Raw generated source clips can retain model artifacts that the final compositions remove. The long tutorial, GitHub push, Fly deployment and native-store submission remain separate gates.
