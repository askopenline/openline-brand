# Openline Brand Portal Deployment

This document outlines the deployment process for the Openline brand portal, hosted at `brand.openline.com`.

## Architecture Overview

*   **Application:** The brand portal is built using React and served statically.
*   **Hosting:** Deployed on Fly.io with an `always-on sharedCPU256MB` configuration and a 3GB volume.
*   **Web Server:** Nginx serves the static content.
*   **Data:** No runtime AI calls or database are used. All content is static or pre-generated.
*   **Asset Distribution:** Large runtime files are distributed from `brand.openline.com` and managed via a SHA256 hydration manifest (`brand-library/PUBLIC-ASSETS.json`).

## Deployment Process

Deployment follows an incremental atomic symlink release strategy, allowing for rollbacks.

1.  **Preparation:**
    *   Ensure all new assets are prepared and validated according to brand guidelines.
    *   Update the `brand-library/PUBLIC-ASSETS.json` manifest for any new or updated large binary assets.
    *   Verify that all necessary documentation (`docs/`) is updated.

2.  **Build Process (Local):**
    *   The `brand-library/` directory contains the current application source.
    *   Build the public tree locally: `npm ci`, then `npm run build`.

3.  **Asset Hydration (Local):**
    *   Large binary assets (e.g., motion graphics, high-resolution images) are not committed directly to Git.
    *   Build the public tree locally, then use the `brand-library/tools/hydrate-public.py` script with the `brand-library/PUBLIC-ASSETS.json` manifest to download assets to the local build environment.
    *   The Fly runtime does not run the hydration downloader; assets must be built and hydrated locally before deployment.

4.  **Deployment to Fly.io:**
    *   A private, short-lived transfer route is used for deploying new releases.
    *   Use the existing incremental release script with an explicit release-key and verified-file manifest.
    *   The deployment creates a new release directory and updates a symlink to point to the new release, ensuring atomic updates.
    *   Nginx is configured to serve content from the active symlinked release.
    *   Existing authenticated Fly configuration is used; no blind volume reset/recreate is performed.

5.  **Rollback Capability:**
    *   Due to the symlink-based deployment, immediate rollbacks to previous stable versions are possible by simply updating the symlink.

## Production Asset Paths

*   Motion graphics are located at `/library/productions/motion-150/`.

## Exclusions

*   Secrets, provider payloads, receipts, and raw unapproved generations are explicitly excluded from the deployment process and the public repository.
*   Existing old archives remain accessible but are not part of the active deployment pipeline.

## GitHub Synchronization

Write access to [`askopenline/openline-brand`](https://github.com/askopenline/openline-brand) was verified on 25 October 2026, and the v2.4 source/documentation update was pushed to `main` in commit [`c789168`](https://github.com/askopenline/openline-brand/commit/c78916861e619f07a02721d330b7cb15adfbc86f). Fly publication and GitHub synchronization remain separate processes; confirm both independently for each release.
