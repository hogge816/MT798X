#!/usr/bin/env python3
"""Check the S20P image and manifest before publishing."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
images = list(root.glob('*clx_s20p*sysupgrade*.bin'))
if len(images) != 1 or images[0].stat().st_size == 0:
    raise SystemExit(f'Expected one nonempty S20P sysupgrade image, found {images}')
manifests = list(root.glob('*clx_s20p*.manifest'))
if not manifests:
    manifests = list(root.glob('*.manifest'))
if len(manifests) != 1:
    raise SystemExit(f'Expected one S20P or target manifest, found {manifests}')
packages = {line.split(' - ', 1)[0] for line in manifests[0].read_text().splitlines()}
required = {'kmod-mt_wifi', 'kmod-warp', 'kmod-conninfra',
            'luci-app-mtwifi-cfg', 'luci-app-nikki-rs', 'nikki-rs', 'clash-rs',
            'luci-app-rtp2httpd', 'rtp2httpd', 'luci-app-ddns-go', 'ddns-go',
            'luci-app-upnp', 'miniupnpd-nftables'}
missing = sorted(required - packages)
if missing:
    raise SystemExit('Manifest missing packages: ' + ', '.join(missing))
print(f'Image: {images[0]} ({images[0].stat().st_size} bytes); verified {len(required)} packages in {manifests[0]}')
