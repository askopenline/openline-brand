# Openline Brand Library v2.8.6

Store graphics and a redesigned /app workspace.

- New Google Play feature graphic (1024 x 500, no alpha): orange recommended version and a light alternate, with the headline "Travel eSIM data without roaming surprises." and two phone screens. Choose one in the Graphics step; the choice feeds the Google preview and ZIP. The older feature graphic is kept for V1 to V3.
- New Graphics step lists every asset each console asks for (icon, feature graphic, phone screenshots, Apple 6.9-inch and 6.3-inch sets), with size, format and alpha validation from `store-graphics.json`, previews, downloads and a proofread tick and note per asset. Optional assets not created (iPad, tablet, video) are listed with reasons.
- /app Current view is now steps: Overview (proofread progress per store), Text (editor with live store preview), Graphics, Screenshots, Category, Review, Export, plus All in one page. A sticky switch changes between App Store and Google Play.
- Text fields show automatic checks (emoji, promo or ranking wording, prices, caps, short-description symbols, keyword format, other-platform names) and a Proofread tick that clears when the text is edited.
- Proofread state is stored in this browser (`openline-proofread-v1`) and included in the export ZIP, JSON and summary. ZIPs now include a graphics report and Google screenshot alt text.
- Candidate 19 alt text shortened to fit Google's 140 character limit.
- Cache-busting updated to ?v=2-8-6. Final is unchanged. V1, V2 and original V3 assets are unchanged.
