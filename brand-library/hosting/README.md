# Fly.io static hosting

This deployment path avoids browser automation and private container-registry
credentials. It serves the already-built static studio through the official
NGINX Alpine image on a small Fly Machine.

## Release preparation

```sh
npm ci
npm run build
tar -C dist --exclude='./downloads/openline-orange-series.zip' \
  --exclude='./downloads/openline-series-*.zip' \
  -czf hosting/openline-brand-dist.tar.gz .
```

Commit the bundle to the public brand repository under `launch-studio/hosting/`.
The Fly Machine pins its download URL to a full Git commit and verifies a SHA-256
checksum before serving it. No repository credential is needed in the container.
The bundle contains only the same public static files as the approved preview.

Since v1.8, the large review ZIP downloads are excluded from the boot bundle
to avoid storing identical archived artwork twice. NGINX redirects these exact
download paths to `public/downloads/` in the same public GitHub repository,
pinned to the same full commit by `fly_operation.py`. All other downloads are
served locally. The Perplexity preview includes all ZIPs directly.

## Provisioning

`scripts/fly_operation.py` uses the Fly Machines HTTPS API. Run it only with the
approved Fly organization credential attached by Computer's secure proxy.
It never reads or stores a raw token. Outside Computer, supply authentication
through an appropriate credential-aware HTTP transport.

1. Inspect the intended organization and app; do not overwrite an unrelated app.
2. Create `openline-brand` in the confirmed organization.
3. Allocate shared IPv4 and IPv6 for the new app.
4. Create one small, shared-CPU Machine with the release commit.
5. Verify its health check, HTTPS page, icon controls and download packages.

The API configuration requests Paris (`cdg`), 256 MB memory, one shared CPU,
HTTPS redirect, health checks, autostart and idle autostop with zero minimum
running Machines. No database, volume, API secret, dedicated IPv4, or external
write endpoint is required. Fly compute/transfer usage follows the account's
applicable billing.

The bootstrap reuses a checksum-verified cached release when possible. A first
boot needs access to the public GitHub release bundle. If download or checksum
validation fails, the server does not start with an unverified bundle.

## Updates

Build and commit a new bundle, then call `update-machine` with the same app and
Machine ID and the new full Git commit. The script verifies the existing
Machine's purpose marker before updating and preserves the resolved image digest.
Updates are explicit; no automatic GitHub Actions deployment is configured.

## Status

Live: https://openline-brand.fly.dev

- Organization: `paul-fleury`
- App: `openline-brand`
- Machine: `8d7155be3ed118` (`openline-brand-web`)
- HTTPS and `/healthz` verified; Fly health check passing.
- Nine views include the selected Original orange preview; the final 43.5% icon remains locked.
- Shared IPv4 and IPv6 allocated. No dedicated IPv4, database or volume.
- Madrid rejected new provisioning; Paris was used instead.

In Computer's sandbox, use `REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt`
so Requests trusts the platform credential proxy. Do not disable TLS validation.
Read `config.metadata.openline.source_commit` on the Machine for its exact
deployed source revision. The GitHub repository is the durable release source.

Official API guidance:
https://docs.fly.io/machines/api/apps-resource
https://docs.fly.io/machines/api/machines-resource
https://docs.fly.io/networking/services/
