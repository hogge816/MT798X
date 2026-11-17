#!/usr/bin/env python3
"""Reject a resolved configuration missing the S20P radio or selected apps."""
import pathlib
import sys

required = (
    'TARGET_mediatek', 'TARGET_mediatek_filogic',
    'TARGET_DEVICE_mediatek_filogic_DEVICE_clx_s20p',
    'PACKAGE_kmod-mediatek_hnat', 'PACKAGE_kmod-mt_wifi',
    'PACKAGE_kmod-warp', 'PACKAGE_kmod-conninfra',
    'MTK_CHIP_MT7986', 'MTK_MT_WIFI_DRIVER_VERSION_7673',
    'MTK_FIRST_IF_IPAILNA', 'MTK_FIRST_IF_EEPROM_FLASH',
    'PACKAGE_luci-app-mtwifi-cfg', 'PACKAGE_firewall4',
    'PACKAGE_luci-app-nikki-rs', 'PACKAGE_nikki-rs', 'PACKAGE_clash-rs',
    'PACKAGE_luci-app-rtp2httpd', 'PACKAGE_rtp2httpd',
    'PACKAGE_luci-app-ddns-go', 'PACKAGE_ddns-go',
    'PACKAGE_luci-app-homeproxy', 'PACKAGE_sing-box',
    'PACKAGE_miniupnpd-nftables', 'PACKAGE_luci-app-upnp',
)
config = {}
for line in pathlib.Path(sys.argv[1]).read_text().splitlines():
    if line.startswith('CONFIG_') and '=' in line:
        key, value = line.split('=', 1)
        if key in config:
            raise SystemExit(f'Duplicate configuration: {key}')
        config[key] = value
missing = [key for key in required if config.get('CONFIG_' + key) != 'y']
if missing:
    raise SystemExit('Missing or disabled: ' + ', '.join(missing))
print(f'S20P high-power configuration: {len(required)} required symbols enabled')
