# Openline Brand Library v2.8.7

Apple product page header and search results graphics, a 170-character promotional text, and checklist coverage.

- New graphics in `app-v3/recommended/apple-creative/`, each in orange (recommended) and light (alternate): product page header 3840 x 1646 (21:9), search results 3840 x 2560 and 1920 x 1280 (3:2), and a universal 5244 x 2950 (16:9) PNG that can fill both slots. All are RGB PNG without alpha, validated by `tools/validate-store-graphics.py`.
- /app Graphics step (App Store) shows the three new groups with previews, checks, downloads, proofread ticks and notes. The App Store ZIP includes an `apple-creative` folder.
- Recommended Apple promotional text now uses 170 of 170 characters (setup checklist, travel dates and live chat added). Previous text remains visible as the recommended original after edits.
- Review checklist gains "Product page header & search results" (optional, iOS 27 and later) with Apple's creative assets specification as source.
- Renderer: `scripts/render_apple_creative.mjs`. Final is unchanged; V1, V2 and original V3 are unchanged.
- Safe areas are not published on Apple's specification page. Check the templates in App Store Connect before upload.
