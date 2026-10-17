# Openline mobile resources

> Openline company documentation: maintained in [askopenline/openline-brand-assets](https://github.com/askopenline/openline-brand-assets). See the [repository README](../README.md) for ownership, scope, and release boundaries.

Design and implementation references for the Openline mobile app. The September 24, 2026 delivery includes a React screen gallery, a native Figma snapshot, and iOS/Android icon assets.

## Resource directory

| Resource | Location | Purpose |
| --- | --- | --- |
| React screen gallery | [app-screens/](app-screens/) | Buildable React/TypeScript reference with 19 screens and states |
| Static gallery | [app-screens/preview/](app-screens/preview/) | Prebuilt browser preview; serve over HTTP |
| Native Figma snapshot | [openline-mobile-screens-2026-09-24.fig](../figma/mobile/openline-mobile-screens-2026-09-24.fig) | Original uploaded design file, preserved byte-for-byte |
| App icons | [app-icons/](../app-icons/) | Xcode catalog, Android density variants, adaptive layers and store icons |
| Intake record | [2026-09-24.md](deliveries/2026-09-24.md) | Original upload names, checksums and packaging changes |

## Scope and status

- **Design reference:** The gallery is a React web app for reviewing mobile UI, not a React Native app or a production mobile SDK.
- **Demo data:** Prices, account details, eSIM identifiers, activation codes and payment states are sample content. Do not treat them as live service credentials, commercial claims or a working checkout.
- **Styles:** The gallery includes a precompiled Tailwind stylesheet. New class names are not generated automatically; follow the [editing notes](app-screens/README.md#if-you-edit-this).
- **Source ownership:** The app gallery keeps its own asset and SVG dependencies so it builds independently. Do not deduplicate those files into the legacy Figma exports without updating and testing the imports.

## Quick start

From the repository root:

```sh
cd mobile/app-screens
npm ci
npm run typecheck
npm run dev
```

To rebuild and view the static version:

```sh
npm run build
npm run preview
```

## Future updates

Keep `app-screens/` as the current buildable reference and use Git history for earlier code revisions. Add native `.fig` snapshots under `figma/mobile/` with their delivery date rather than overwriting an earlier snapshot.

For each new delivery, record provenance, run the type check and production build, and refresh the committed preview with `npm run build -- --outDir preview`. Never commit dependency folders, local secrets or real customer data.
