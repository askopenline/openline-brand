# Openline Brand Library

This document describes the `brand-library/` application, which serves as the primary interface for Openline brand assets. It is deployed to [brand.openline.com](https://brand.openline.com) and replaces the legacy `launch-studio/` application, which is retained for historical reference.

## Application Structure and Deployment

The `brand-library/` application is a React-based single-page application. It is deployed on Fly.io with an always-on sharedCPU256MB instance, a 6GB volume, and a static Nginx server. The application does not perform any runtime AI calls or database operations.

Releases are handled via incremental atomic symlink updates, allowing for quick rollbacks. A private, short-lived transfer route is used for deployment. Secrets, provider payloads, receipts, and raw unapproved generations are excluded from the deployment.

## Search and social metadata

The homepage serves its title, description, canonical URL, Open Graph/Twitter cards and Organization/WebSite/CollectionPage JSON-LD in the initial HTML. The 1200×630 social card uses the approved white-on-orange artwork; `tools/prepare-seo-images.py` reproduces the card and 180px touch icon without generative assets.

`robots.txt` permits crawling and points to `sitemap.xml`. Only the canonical homepage is listed: the existing hash-based collections are views of one page, not separate crawlable URLs. The HTML includes a JavaScript-free summary and repository link; interactive galleries still require JavaScript. Indexing and third-party preview cache refreshes are not guaranteed by deployment.

## Asset Management and Hydration

Large runtime files are distributed from `brand.openline.com` using a SHA256 hydration manifest located at `brand-library/PUBLIC-ASSETS.json`. The `brand-library/tools/hydrate-public.py` script facilitates this process.

Clean clones of the repository require hydration before a complete gallery of assets can be displayed. Not all binary files are stored directly in Git. Hydration initiates a multi-GB download only after a user explicitly chooses to perform it.

Production files for motion assets are located at `/library/productions/motion-150/`.

## Key Features and Content

The brand library provides access to various brand assets, including:

*   **Overview**: General information about the Openline brand.
*   **Assets**: A collection of static brand assets.
*   **Motion**: Animated brand elements, including the expanded collection of 150 motion cards.
*   **Ads**: Campaign advertisements, including 60 active short ads.
*   **Presenters**: AI-generated presenter content.
*   **App**: Resources related to the Openline app.
*   **Guidelines**: Brand usage guidelines.
*   **Archives**: Historical and legacy assets, including previous versions of ads.

## Brand Colors

Openline utilizes distinct color tokens for specific purposes:

*   **Native Orange**: `#FF6518`
*   **Artwork Orange**: `#FF6616`
*   **Campaign Orange**: `#FF6418`

These tokens are maintained separately to ensure consistency across different brand applications.

## GitHub Integration

Write access and the push to `main` were verified on 25 October 2026. The v2.4 source and documentation update is published in commit [`c789168`](https://github.com/askopenline/openline-brand/commit/c78916861e619f07a02721d330b7cb15adfbc86f). Fly publication and GitHub synchronization remain separate operations; large runtime media is retrieved through the checksum-verified public-assets manifest.

## Company Reference

This guide belongs to [Openline Brand Assets](https://github.com/askopenline/openline-brand), maintained by Openline. Return to the [project overview](../README.md) for the broader system, current company links, and release context.
