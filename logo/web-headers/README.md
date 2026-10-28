# Openline website and blog header logos

Observed on October 28, 2026 from [openline.com](https://openline.com) and [blog.openline.com](https://blog.openline.com). Both current headers combine the same raster icon with live Play Bold text, rather than using the original vector wordmark as one image. The two retrieved icon files are byte-identical.

The website uses a 32px-high icon, an 8px gap and 26px bold Play text. The blog adds a divider and “the blog”; its [header stylesheet](https://blog.openline.com/assets/blog.css?v=86e6ef2571e123e7) defines those treatments. These observed header logos are static. Animated artwork is available separately in the brand library.

## Included

- `website-header.html` and `blog-header.html`: self-contained, script-free visual examples with embedded icon and Play font. Preview scales the logo to 150%; base CSS retains native header sizes.
- `header-logos.css`: reusable class-scoped CSS at original sizes.
- `website-observed-header.html.txt` and `blog-observed-header.html.txt`: actual observed logo element markup, without unrelated navigation or tracking.
- `website-mark.png`, `blog-mark.png`, `play-bold.woff2` and font license.

The blog descriptor uses Inter where available, with Arial fallback in the portable example. These are isolated logo demonstrations, not complete website-header components; original navigation, framework classes and application scripts are not included. No header on the main site or blog was modified.
