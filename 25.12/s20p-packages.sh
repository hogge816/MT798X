#!/bin/bash
# Run from the OpenWrt source root AFTER installing the standard feeds.
set -euo pipefail
[[ -f rules.mk && -d feeds/luci && -d feeds/packages ]] || {
    printf '%s\n' 'Run this script from an OpenWrt tree with installed feeds.' >&2
    exit 1
}
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cache="$(mktemp -d)"
trap 'rm -rf -- "$cache"' EXIT
fetch() {
    local name="$1" url="$2" rev="$3"
    git init -q "$cache/$name"
    git -C "$cache/$name" remote add origin "$url"
    git -C "$cache/$name" fetch --depth 1 origin "$rev"
    git -C "$cache/$name" checkout -q --detach FETCH_HEAD
    [[ "$(git -C "$cache/$name" rev-parse HEAD)" == "$rev" ]]
}
# Replace only exact package definitions; never delete unrelated feed packages.
install_package() {
    local source="$1" name="$2"
    [[ -f "$source/Makefile" ]]
    python3 - "$name" <<'PY'
import pathlib, shutil, sys
name = sys.argv[1]
for feed in pathlib.Path('feeds').iterdir():
    if not feed.is_dir():
        continue
    for path in feed.rglob(name):
        if path.is_symlink():
            path.unlink()
        elif path.is_dir() and (path / 'Makefile').is_file():
            shutil.rmtree(path)
for feed in pathlib.Path('package/feeds').glob('*'):
    path = feed / name
    if path.is_symlink():
        path.unlink()
PY
    rm -rf -- "package/custom/$name"
    cp -a -- "$source" "package/custom/$name"
}
mkdir -p package/custom
fetch nikki https://github.com/nikkinikki-org/OpenWrt-nikki.git 31339d53b454f575082dc4e16510c96858e01921
fetch rtp https://github.com/stackia/rtp2httpd.git 5e53989835c33a68fcb78d60587c861afb2133ca
fetch ddns https://github.com/sirpdboy/luci-app-ddns-go.git 7092e6de6ad9fe3f7d327f70468dfd19e00d6f0e
fetch viking https://github.com/VIKINGYFY/packages.git af37004515fff4057d31fe7557748bbee5e293cf
for name in nikki luci-app-nikki mihomo-meta; do
    install_package "$cache/nikki/$name" "$name"
done
for name in rtp2httpd luci-app-rtp2httpd; do
    install_package "$cache/rtp/openwrt-support/$name" "$name"
    cp "package/custom/$name/Makefile.versioned" "package/custom/$name/Makefile"
done
for name in ddns-go luci-app-ddns-go; do
    install_package "$cache/ddns/$name" "$name"
done
for name in sing-box luci-app-homeproxy; do
    install_package "$cache/viking/$name" "$name"
done
# Keep the user's chosen themes, without the unrelated all-device DIY scripts.
fetch argon https://github.com/sbwml/luci-theme-argon.git "$(git ls-remote https://github.com/sbwml/luci-theme-argon.git refs/heads/openwrt-25.12 | cut -f1)"
install_package "$cache/argon/luci-theme-argon" luci-theme-argon
install_package "$cache/argon/luci-app-argon-config" luci-app-argon-config
fetch aurora https://github.com/eamonxg/luci-theme-aurora.git "$(git ls-remote https://github.com/eamonxg/luci-theme-aurora.git HEAD | cut -f1)"
install_package "$cache/aurora" luci-theme-aurora
fetch aurora-config https://github.com/eamonxg/luci-app-aurora-config.git "$(git ls-remote https://github.com/eamonxg/luci-app-aurora-config.git HEAD | cut -f1)"
install_package "$cache/aurora-config" luci-app-aurora-config
# Persist package source revisions as a build artifact.
mkdir -p bin
for name in nikki rtp ddns viking argon aurora aurora-config; do
    printf '%s %s\n' "$name" "$(git -C "$cache/$name" rev-parse HEAD)"
done > bin/s20p-package-revisions.txt
