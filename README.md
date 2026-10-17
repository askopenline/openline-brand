# Openline Brand Assets

The official Openline library for brand identity, product artwork, design references, and reusable visual resources. Maintained by [Openline](https://openline.com) in [askopenline/openline-brand-assets](https://github.com/askopenline/openline-brand-assets) for company teams, partners, and editorial use under the usage policy below.

## Find the right resource

| Resource | Location | Use |
| --- | --- | --- |
| Brand symbol | [`logo/`](logo/) | Canonical marks and format variants |
| Wordmark | [`wordmark/`](wordmark/) | Approved Openline name artwork |
| Social assets | [`social/`](social/) | Profile and social-format resources |
| Motion | [`animation/`](animation/) | Animated brand exports |
| Approved app icon | [`app-icons/final/`](app-icons/final/README.md) | Final visual composition, export formats, and native resources |
| App icon history | [`app-icons/`](app-icons/README.md) | Prior deliveries and integration notes |
| Brand Studio | [`launch-studio/`](launch-studio/README.md) | Store artwork, preview tools, copy drafts, and download packages |
| Mobile UI references | [`mobile/`](mobile/README.md) | Buildable screen gallery and delivery records |
| Figma sources | [`figma/`](figma/README.md) | Design snapshots, exports, and live-reference links |
| Payment marks | [`payment-methods/`](payment-methods/README.md) | Third-party identification assets and attribution |
| Email resources | [`email/`](email/README.md) | Transactional templates, letterhead, and company signatures |
| Shared web styles | [`web/`](web/README.md) | Openline UI stylesheet and integration examples |
| Virtual-office previews | [`workadventure/`](workadventure/README.md) | Embeddable interface concepts and screenshots |

The [Brand Studio preview](https://openline-brand.fly.dev) is hosted separately from this repository. Copying or editing this company repository does not automatically update that deployment or existing asset consumers.

## Current app-icon reference

The approved flat composition uses the original Openline mark at 43.5% visible width inside an unchanged white square. Start with [`app-icons/final/`](app-icons/final/README.md), not the historical September icon delivery.

The package includes vector and raster exports plus platform-specific integration resources. Visual approval is not native-device validation, store approval, or permission to substitute a transparent design export for a required opaque store asset.

Brand Studio distinguishes the marketing presentation from separate Apple and Google submission drafts. Screens based on the supplied React gallery remain design references until replaced or validated against the actual native application.

## Use and embed assets

Prefer checked-in assets or URLs pinned to a reviewed commit when reliability matters. Use `main` only when a consumer intentionally follows ongoing changes.

```text
https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/openline-mark-512.png
https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/payment-methods/svg/visa.svg
https://cdn.jsdelivr.net/gh/askopenline/openline-brand-assets@main/web/openline-ui.css
```

Raw file URLs are useful for images and downloads; they are not a substitute for a configured HTML application host. Review MIME types, caching, relative links, and access requirements before using a CDN or raw URL in a product.

Existing deployed templates and applications may still reference earlier hosting locations. Updating examples here does not rewrite those applications or change their active deployment configuration.

## Brand principles

- **Artwork:** Use the supplied mark and wordmark. Do not redraw, recolor, stretch, rotate, or add effects without brand approval.
- **Contrast:** Choose the approved light or dark variant for the background and preserve clear space.
- **Color:** Openline orange is `#FF6616`; individual product systems may document additional scoped tokens.
- **Typography:** Use the font and layout specifications of the relevant asset family rather than assuming every product surface shares one implementation.
- **App icons:** Keep the approved composition separate from historical alternatives and platform appearance references.
- **Third-party marks:** Preserve their proportions, attribution, and applicable usage guidance. Inclusion does not imply a payment integration or commercial relationship.

## Usage policy

These files are published so journalists, partners, integrators, and customers can reference Openline accurately. Public availability is not a blanket open-source license for the brand library or a transfer of third-party rights.

- Use Openline brand assets as supplied, without recoloring, rotation, or distortion.
- Do not imply a partnership, endorsement, or affiliation that does not exist.
- Do not use the assets for products, services, or content that compete with or disparage Openline.
- Respect Openline's name and mark, and the rights attached to third-party materials.
- Request approval before co-branding, merchandising, paid placement, or large-scale physical signage.

Contact [ask@openline.com](mailto:ask@openline.com) for brand permissions and press or partnership enquiries. Any explicit file-level license continues to apply to that file; this README does not replace it.

## Maintenance

1. Preserve canonical source artwork and record the provenance of new deliveries.
2. Use descriptive filenames and retain existing integration paths unless a migration is planned.
3. Update the relevant folder README, previews, and prepared downloads together.
4. Check image dimensions, transparency, file integrity, and the consuming application.
5. Tag reviewed releases so integrators can pin a stable version.

Changes to the core mark, wordmark, or primary brand direction require company brand review. Request formats, report broken assets, or propose documentation improvements through [company repository issues](https://github.com/askopenline/openline-brand-assets/issues).

## Ownership and attribution

Openline maintains this collection and its company-created brand materials through the official [askopenline account](https://github.com/askopenline). Payment-provider logos, fonts, upstream software, competitor references, and other third-party resources retain their respective ownership and license terms.
