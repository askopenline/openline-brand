# Openline mobile icon · final visual choice · 2026-10-07

> Openline company documentation: maintained in [askopenline/openline-brand-assets](https://github.com/askopenline/openline-brand-assets). See the [repository README](../../../README.md) for ownership, scope, and release boundaries.

Canonical mark geometry preserved. Default visible mark width: 43.5% of square,
approximately 17.5% smaller linearly than the 52.7% candidate. White square unchanged.
44.8% and 42.2% alternatives represent approximately 15% and 20% reductions from 52.7%.
Original export: approximately 68%. No pre-rendered corners or shadows.

## iOS
Import ios/AppIcon.appiconset into Assets.xcassets for the standard PNG workflow.
Default icons are opaque RGB PNGs. The 1024px icon is included.
icon-composer-layers contains full-canvas background, black mark and orange accent
layers for manual assembly in Apple's Icon Composer. These are SOURCE LAYERS,
not a compiled .icon document. Validate default, dark, tinted and clear appearances
in current Xcode on-device. Appearance-reference PNGs are design references only.

## Android
Merge android/res into your application resources; do not overwrite app resources
blindly. Point android:icon to @mipmap/ic_launcher. Configure roundIcon as appropriate
for your app and test masks on real devices. v26 adaptive XML and v33 monochrome XML
are supplied. The adaptive candidate spans 39.6dp on a 108dp canvas, a 17.5%
reduction from the prior 48dp artwork. This is below Android's recommended
48–66dp range: it is an explicit smaller-size experiment, not a recommendation
to skip native legibility testing. The android/48dp-reference directory supplies
foreground and monochrome replacements at the prior guideline-aligned size.
Masked appearance differs from iOS; validate every mask on actual launchers.
The 43.5% flat composition applies to iOS, legacy Android and store-listing icons.
Google Play icon: 512x512 RGBA PNG, fully opaque. No rounded corners baked in.

## Release gate
Openline approved the 43.5% flat visual composition on 7 October 2026. These files
are not store approval. Verify rendering in signed release builds; native
adaptive sizing, masks and appearances still need engineering/device validation.

Official guidance:
https://developer.apple.com/design/human-interface-guidelines/app-icons
https://developer.android.com/develop/ui/compose/system/icon_design_adaptive
https://support.google.com/googleplay/android-developer/answer/9866151?hl=en
