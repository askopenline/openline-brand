<!-- OPENLINE-GUIDE-VISUAL -->
![Brand Assets: company resource guide](https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/.github/assets/guide-header.png)

# Openline Figma References

The "code side" of the Openline design system — React/TSX components generated from Figma via **Dev Mode → Copy code**, plus a place to keep the live Figma share links so this repo stays in sync with the design source of truth.

This folder is a company-maintained reference collection, not proof that every export is an original Openline design or a production component. Legacy exports can include other brands or comparison material; preserve their attribution and review their rights before using them in an Openline product.

## What's inside

```
figma/
├── code-exports/    ← Auto-generated TSX / TS components straight from Figma Dev Mode
│                      — named by what they render, not by Figma's auto-labels
├── mobile/          ← Dated native mobile .fig snapshots and embedded previews
└── LINKS.md         ← Paste Figma share links here (one row per file / design)
```

### Named components (v1.3+)

Every export has been renamed from Figma's generic auto-labels (`Frame1.tsx`, `Container.tsx`, `List.tsx`, …) to descriptive `kebab-case` filenames. The `svg-*.ts` path-data modules keep their hashed names because they're shared assets referenced by hash from multiple components.

| Area | Files |
| --- | --- |
| **Hero & marketing** | `hero-best-signal.tsx`, `testimonial-quote-card.tsx`, `referral-cta-banner.tsx`, `how-does-saily-work.tsx`, `saily-footer.tsx`, `partner-logos-row.tsx`, `bundle-app-logos.tsx`, `dual-image-panel.tsx` |
| **Coverage & carriers** | `carriers-row-5.tsx`, `carriers-row-6.tsx`, `carriers-grid-34.tsx`, `carriers-grid-37-airtel-play.tsx`, `carriers-grid-37-alt.tsx`, `carriers-row-airtel-play-turkcell.tsx`, `country-flags-strip.tsx`, `regions-quad-1.tsx`, `regions-quad-2.tsx`, `world-map-dotted.tsx` |
| **Checkout / payment** | `payment-list.tsx`, `payment-list-3.tsx`, `payment-list-item.tsx`, `payment-list-alipay-1.tsx`, `payment-list-alipay-2.tsx`, `payment-list-alipay-3.tsx`, `payment-list-wechat.tsx`, `payment-methods-alipay-1.tsx`, `payment-methods-alipay-2.tsx`, `payment-group-mini.tsx`, `visa-glyph.tsx`, `wechat-pay-glyph.tsx`, `wechat-pay-icon-1.tsx`, `wechat-pay-icon-2.tsx` |
| **Icons & glyphs** | `chevron-glyph.tsx`, `security-shield-icon.tsx`, `phosphor-currency-eth.tsx`, `icon-mini-1.tsx`, `icon-mini-2.tsx` |
| **Shared SVG paths** | `svg-*.ts` (path-data modules, keep hashed names) |

## What these files are (and aren't)

- **Are:** raw React/TSX and inline SVG modules copied verbatim from Figma Dev Mode. Useful as a **reference implementation** — the exact spacing, typography, colours, and structure the designer intended, expressed as code you can diff and lift from.
- **Aren't:** production components. They use hard-coded pixel values, embed raw SVG, reference `imgGroup*` placeholders, and don't wire up interactivity. Treat them as a specification you translate into your real design-system components.

## Where the images live

Figma-exported **PNG** assets are large and belong with the app that consumes them (typically `openline-native-sdk/src/assets/` inside the mobile / SDK repo), not here. The legacy `code-exports/` folder holds the code side of those exports. The standalone [mobile gallery](../mobile/app-screens/) includes its own image dependencies so it builds without the original site repository.

## Source files (`.fig`)

Native mobile snapshots now live in [`mobile/`](mobile/), starting with the September 24, 2026 delivery. Use [`LINKS.md`](LINKS.md) for live design references; the buildable companion is in [`../mobile/app-screens/`](../mobile/app-screens/).

## Contributing

- **Refreshing an export:** in Figma, select the frame, switch to Dev Mode, choose React + Tailwind, copy the code, replace the corresponding file here, and commit.
- **New design:** drop the export into `code-exports/` using a descriptive filename (e.g. `checkout-summary.tsx` beats `Frame3.tsx`) and add the Figma link to `LINKS.md`.
- **Cleanup PRs welcome:** renaming the auto-generated `Frame*.tsx` files to human names, or grouping svg-hash modules alongside the component that uses them, is a great low-risk contribution.

<!-- OPENLINE-GUIDE-NAV -->
## Company reference

This guide belongs to [Openline Brand Assets](https://github.com/askopenline/openline-brand), maintained by Openline. Return to the [project overview](../README.md) for the broader system, current company links, and release context.
