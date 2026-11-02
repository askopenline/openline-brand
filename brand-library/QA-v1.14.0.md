# Preview release QA: v1.14.0

## Verified locally

- Production Vite build succeeds.
- Main opens iPhone, Android, App Store and Google Play dialogs.
- Both store dialogs switch between Marketing master and Submission draft.
- Device next-screen and numbered-screen controls work; app images load.
- Archive opens the existing full workbench; Main returns to the clean mobile view.
- Brand & Motion is reachable from the Main download recap.
- Brand collection is responsive at 1365px and 375px, with no horizontal overflow.
- All seven video players load metadata without media errors: Hellen 7.2s, four logo animations 4s each, two vertical ads 15s each.
- Hellen video plays in the browser at 1920 × 1080.
- All fourteen download controls return HTTP 200 with expected ZIP, GIF or MP4 content types.
- No JavaScript page errors observed in exercised main and collection flows.
- Hellen's generated voice was transcribed against the requested script and evaluated for accent, pacing and audio artifacts.
- Presenter frames and branded composition were visually inspected. This is a creative-review pilot, not final human approval of every lip-sync frame.
- Logo, motion and ad exporters provide separate decoded-frame, dimensions, alpha/checksum and ZIP-integrity reports.

## Not claimed

- No actual iPhone recording has been delivered.
- No full installation tutorial has been completed.
- No store submission or advertising campaign has been published.
- No GitHub push or Fly production deployment has occurred for this version.
- Project file persistence was blocked by a busy checkout after one bounded retry; the attached website preview carries the downloadable collection.
