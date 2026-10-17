<!-- OPENLINE-GUIDE-VISUAL -->
![Brand Assets: company resource guide](https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/.github/assets/guide-header.png)

# Openline - App Icons (iOS + Android)

## Current approved icon

**Use [final/](final/) for the approved 43.5% white-square composition**, finalized
by Openline on 7 October 2026. It includes native resources and PNG, SVG, vector PDF,
EPS, JPEG, WebP, ICO and ICNS exports. Native device validation remains separate.

Direct download:
https://openline-brand.fly.dev/downloads/openline-final-icon-all-formats.zip

The `ios/` and `android/` paths described below are the historical September
intake, preserved for compatibility and comparison. They are not the final
approved export. New integrations should start from `final/native/`.

## Historical September delivery

Registered in media kit **v1.4** from the September 24, 2026 delivery. The pack
contains 24 PNGs: 15 iOS images and nine Android images, plus the Xcode catalog.
Native filenames are intentionally preserved for integration.

![Openline app icon](android/play-store-icon-512.png)

These are native app/store icons, distinct from the transparent
[brand marks](../logo/png/). Do not replace the existing README hero or web mark
with an opaque launcher icon.

The supplied pack describes these as generated from the 2250x2250 Openline
master logotype. Keep the original PNGs and validate them in the consuming
native project before store submission.

## iOS - `ios/AppIcon.appiconset/`

Drop the whole `AppIcon.appiconset` folder into your Xcode asset catalog
(`Assets.xcassets`) - the included `Contents.json` maps every size automatically.

- Full iPhone + iPad set (20pt to 83.5pt at 1x/2x/3x) plus the 1024x1024 App Store
  marketing icon.
- All icons are fully opaque (no alpha channel content) as required by App Store
  Review - iOS applies its own corner mask, so the artwork is a plain square.
- If you are on Xcode 14+ you can alternatively use just `icon-1024.png` with the
  "Single Size" option.

## Android - `android/`

### Adaptive icon (API 26+) - `android/adaptive/`

- `ic_launcher_foreground.png` (432x432): mark centered inside the 66dp safe zone,
  transparent background - safe for round, squircle, and square masks.
- `ic_launcher_background.png` (432x432): solid white. You can replace this with a
  color resource instead if you prefer (`#FFFFFF`).
- `ic_launcher_monochrome.png` (432x432): silhouette layer for Android 13+ themed
  icons.

Place the PNGs in `res/mipmap-xxxhdpi/` (or convert to drawables) and reference them
from `res/mipmap-anydpi-v26/ic_launcher.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@mipmap/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
    <monochrome android:drawable="@mipmap/ic_launcher_monochrome" />
</adaptive-icon>
```

### Legacy launcher icons (API < 26) - `android/mipmap-*/`

Pre-rendered `ic_launcher.png` at mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi
(48/72/96/144/192 px), opaque white background.

### Play Store listing - `android/play-store-icon-512.png`

512x512 RGB PNG, opaque, under 1MB, with no baked-in corner radius.
Validate the listing asset against the target store's requirements at submission.

## Validation and maintenance

The intake checks verified all 18 Xcode catalog references, their expected pixel
dimensions and opaque iOS pixels. The store-listing PNG is RGB (512x512), and
Android adaptive layers are 432x432. The supplied integration notes above are
guidance, not evidence of a store submission or native-device test.

Keep `Contents.json` filenames and Android resource names intact. The adaptive
XML shown above is an integration example, not a supplied native project;
add resources and SDK-appropriate configuration in the consuming Android app.

See the [mobile resources](../mobile/README.md) and
[delivery record](../mobile/deliveries/2026-09-24.md) for the companion sources.

<!-- OPENLINE-GUIDE-NAV -->
## Company reference

This guide belongs to [Openline Brand Assets](https://github.com/askopenline/openline-brand-assets), maintained by Openline. Return to the [project overview](../README.md) for the broader system, current company links, and release context.
