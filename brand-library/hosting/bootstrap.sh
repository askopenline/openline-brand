#!/bin/sh
set -eu
: "${BUNDLE_URL:?Missing pinned bundle URL}"
: "${BUNDLE_SHA256:?Missing bundle checksum}"
case "$BUNDLE_SHA256" in *[!0-9a-f]*|"") exit 1;; esac
[ "${#BUNDLE_SHA256}" = 64 ]
release="/srv/releases/$BUNDLE_SHA256"
if [ ! -f "$release/.verified" ]; then
    mkdir -p "$release"
    wget -T 45 -O /tmp/openline-bundle.tar.gz "$BUNDLE_URL"
    printf '%s  /tmp/openline-bundle.tar.gz\n' "$BUNDLE_SHA256" | sha256sum -c -
    tar -xzf /tmp/openline-bundle.tar.gz -C "$release"
    test -f "$release/index.html"
    touch "$release/.verified"
fi
ln -sfn "$release" /srv/openline
nginx -t
exec nginx -g 'daemon off;'
