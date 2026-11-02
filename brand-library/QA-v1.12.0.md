# Openline Brand Studio v1.12.0 QA

## Local acceptance

- Production build succeeds.
- All 12 screenshots regenerated; dimension and headline/device bounds pass.
- Desktop Main visually inspected at 1440px; mobile Main at 375px.
- Mobile has no horizontal document overflow.
- No browser runtime errors during tested interactions.
- Main hides the previous sidebar and workbench.
- Archive preserves the full workbench and review notes.
- Test notes survive Archive → Main → Archive; test content cleared afterward.
- iPhone and Android preview controls work, including plan-selection frame.
- Store previews open and screenshot enlargement works.
- Escape returns from enlarged artwork to listing, then closes the preview.
- Fresh `#archive` and `#google-play` links route correctly.
- Closing a preview restores the Main view.
- Final screenshot visually reviewed: larger neutral headline, no micro-labels.

## Scope

This is browser/layout and packaging QA, not native-device or store-approval QA.
Supplied React captures and sample commercial UI remain subject to release review.
