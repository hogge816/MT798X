#!/usr/bin/env python3
"""Fail CI if dependency resolution drops any required S20P component."""
import pathlib
import sys

required = {
    'TARGET_mediatek', 'TARGET_mediatek_filogic',
    'TARGET_DEVICE_mediatek_filogic_DEVICE_clx_s20p',
    'PACKAGE_kmod-mediatek_hnat', 'PACKAGE_kmod-mt_wifi',
    'PACKAGE_kmod-warp', 'PACKAGE_kmod-conninfra',
    'MTK_CHIP_MT7986', 'MTK_MT_WIFI_DRIVER_VERSION_7673',
    'PACKAGE_luci-app-mtwifi-cfg', 'PACKAGE_firewall4',
    # nikki 已替换为 nikki-rs（clash-rs 内核）；不再要求旧 nikki/mihomo 链路
    'PACKAGE_luci-app-nikki-rs', 'PACKAGE_nikki-rs', 'PACKAGE_clash-rs',
    'PACKAGE_luci-app-rtp2httpd', 'PACKAGE_rtp2httpd',
    'PACKAGE_luci-app-ddns-go', 'PACKAGE_ddns-go',
    'PACKAGE_luci-app-homeproxy', 'PACKAGE_sing-box',
    'PACKAGE_miniupnpd-nftables', 'PACKAGE_luci-app-upnp',
    'PACKAGE_luci-theme-aurora', 'PACKAGE_luci-app-aurora-config',
}
forbidden = {
    'PACKAGE_luci-app-openclash', 'PACKAGE_luci-app-passwall',
    'PACKAGE_luci-app-passwall2', 'PACKAGE_mihomo-alpha',
    'PACKAGE_miniupnpd-iptables', 'PACKAGE_luci-theme-argon',
    'PACKAGE_luci-app-argon-config',
    # 与 nikki-rs 互斥：旧 nikki 链路不得随镜像发布
    'PACKAGE_luci-app-nikki', 'PACKAGE_nikki', 'PACKAGE_mihomo-meta',
}
config = {}
for line in pathlib.Path(sys.argv[1]).read_text().splitlines():
    if line.startswith('CONFIG_') and '=' in line:
        key, value = line.split('=', 1)
        if key in config:
            raise SystemExit(f'Duplicate configuration: {key}')
        config[key] = value
errors = [f'Missing CONFIG_{key}=y' for key in sorted(required)
          if config.get('CONFIG_' + key) != 'y']
errors += [f'Unexpected enabled CONFIG_{key}' for key in sorted(forbidden)
           if config.get('CONFIG_' + key) in ('y', 'm')]
if errors:
    raise SystemExit('\n'.join(errors))
print(f'S20P configuration: all {len(required)} required selections retained.')
