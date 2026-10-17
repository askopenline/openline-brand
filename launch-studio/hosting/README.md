<!-- OPENLINE-GUIDE-VISUAL -->
![Brand Assets: company resource guide](https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/.github/assets/guide-header.png)

# Openline Brand Studio Hosting

This directory documents the existing Fly.io deployment path for the Openline Brand Studio. The service uses a built static bundle, a pinned source revision, and checksum verification; it is not automatically deployed by a Git push.

## Repository and hosting are separate

The official company source is [askopenline/openline-brand-assets](https://github.com/askopenline/openline-brand-assets). The existing [Brand Studio host](https://openline-brand.fly.dev), its Fly account, and any previously pinned repository URLs remain unchanged until an explicit infrastructure cutover is approved.

Inspect source-URL construction in the deployment helper before using a company-repository commit. Historical helpers may still address the earlier source account; a copied Git history is not a deployment-configuration migration.

## Prepare a release

From `launch-studio/`, install the locked dependencies and build the static application. Review the generated files before producing a boot bundle.

```sh
npm ci
npm run build
tar -C dist --exclude='./downloads/openline-orange-series.zip' \
  --exclude='./downloads/openline-series-*.zip' \
  -czf hosting/openline-brand-dist.tar.gz .
```

The established deployment downloads a public bundle pinned to a full commit and checks its SHA-256 digest. Large review ZIPs may be served through redirects to the matching committed public downloads instead of being duplicated inside the boot bundle.

Verify that the bundle, source commit, checksum, and redirected downloads all refer to the same reviewed release. Never include secrets or private review data in the public bundle.

## Deploy or update

The existing helper is [`../scripts/fly_operation.py`](../scripts/fly_operation.py). Run it only with approved credentials supplied through a secure mechanism and after confirming the intended organization, app, and Machine.

1. Inspect the current app and its recorded source revision.
2. Confirm the correct source repository, commit, bundle, and checksum.
3. Preserve the current Machine configuration and a rollback revision.
4. Apply the explicitly approved update.
5. Verify HTTPS, `/healthz`, the main interface, representative previews, and every affected download.

The historical configuration uses `openline-brand`, the Paris region, a small shared-CPU Machine, and no application database or public write endpoint. Treat recorded identifiers and configuration as operational context to verify, not permission to create, delete, or replace infrastructure.

## Safety checks

- **TLS:** Keep certificate verification enabled. Configure a trusted certificate bundle when a credential-aware transport requires it.
- **Authentication:** Do not paste tokens into documentation, source code, shell history, or build artifacts.
- **Failure behavior:** A failed download or checksum must not fall through to serving an unverified bundle.
- **Rollback:** Retain the last known-good source revision and deployment configuration.
- **Company cutover:** Repoint hosting only after the company repository and its public asset URLs have been checked.

<!-- OPENLINE-GUIDE-NAV -->
## Company reference

This guide belongs to [Openline Brand Assets](https://github.com/askopenline/openline-brand-assets), maintained by Openline. Return to the [project overview](../../README.md) for the broader system, current company links, and release context.
