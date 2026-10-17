<!-- OPENLINE-GUIDE-VISUAL -->
![Brand Assets: company resource guide](https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/.github/assets/guide-header.png)

# Payment methods

The full public library of payment-method logos used across Openline's checkout, receipts,
docs and marketing. Extracted from the payment-methods reference page and reproduced here
as clean, individual, self-contained assets.

## What's inside

```
payment-methods/
├── svg/            ← 99 individual SVGs + 1 raster fallback (cashfree.jpg)
├── app-source/     ← 6 hand-built SVG logotypes used inside the mobile checkout
│                     (Bancontact, BLIK, iDEAL, Pix, Revolut, TWINT)
└── reference.html  ← Standalone HTML index — open in a browser to preview every logo
                       side-by-side with names and dimensions
```

## Sizing conventions

| Type | Canonical size | Notes |
| --- | --- | --- |
| Card marks (Visa, Mastercard, Amex, Discover, JCB…) | **38 × 24** | Standard credit-card aspect ratio |
| Wallets, brand wordmarks (Apple Pay, PayPal, Klarna…) | native | Keep each brand's own aspect ratio |
| Crypto (BTC, ETH, USDC, SOL…) | native | Uses the reference logo from each ecosystem |

Every SVG is **self-contained** — no external font, no shared defs, no CSS dependency —
so you can inline them, drop them into a bundler, or serve them straight from raw GitHub.

## Hot-link (raw GitHub)

```
https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/payment-methods/svg/visa.svg
https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/payment-methods/svg/mastercard.svg
https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/payment-methods/svg/apple-pay.svg
https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/payment-methods/svg/google-pay.svg
https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/payment-methods/svg/paypal.svg
```

## Usage policy

These are third-party trademarks reproduced for identification and interoperability
purposes only. **Openline does not own these marks**. Follow each brand's own usage
guidelines when embedding them in your surface.

## Adding a new payment method

1. Drop a clean SVG into `svg/` named `slug-with-dashes.svg` (lowercase, hyphen-separated).
2. Prefer 38×24 for card marks, native aspect for wallets and wordmarks.
3. Add it to `reference.html` so it shows up in the visual index.
4. Open a PR describing the source and licensing status.

<!-- OPENLINE-GUIDE-NAV -->
## Company reference

This guide belongs to [Openline Brand Assets](https://github.com/askopenline/openline-brand-assets), maintained by Openline. Return to the [project overview](../README.md) for the broader system, current company links, and release context.
