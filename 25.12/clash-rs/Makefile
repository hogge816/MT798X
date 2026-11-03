include $(TOPDIR)/rules.mk

PKG_NAME:=clash-rs
PKG_VERSION:=0.20.24_alpha
PKG_RELEASE:=1

# 架构映射与 SHA256 校验码
ifneq ($(findstring x86_64,$(ARCH)),)
  CLASH_TARGET:=x86_64-unknown-linux-musl
  CLASH_HASH:=85fc94c5935926d75737946bf161d5d4595b5a67db801fc8af3f4f422849f288
else ifneq ($(findstring aarch64,$(ARCH)),)
  CLASH_TARGET:=aarch64-unknown-linux-musl
  CLASH_HASH:=58a578e4b443562b9c2db445b37a812b9411963a98c1686d82f4a8419bc19933
else ifneq ($(findstring arm,$(ARCH)),)
  CLASH_TARGET:=armv7-unknown-linux-musleabihf
  CLASH_HASH:=0ca76d547c02a4e0bedf3e5e090140f4e43f501068429f936fa19bb68ad047a9
else ifneq ($(findstring riscv64,$(ARCH)),)
  CLASH_TARGET:=riscv64gc-unknown-linux-musl
  CLASH_HASH:=54a5f38f941e1b532b22d24f613584871dfb697e61baec16fdbb2d10011b6e5f
else ifneq ($(findstring i386,$(ARCH)),)
  CLASH_TARGET:=i686-unknown-linux-musl
  CLASH_HASH:=40f81d9beaf5feae13ade780eac8795c8c3013c4723a0d1c5bc77f7f221321f1
else ifneq ($(findstring i686,$(ARCH)),)
  CLASH_TARGET:=i686-unknown-linux-musl
  CLASH_HASH:=40f81d9beaf5feae13ade780eac8795c8c3013c4723a0d1c5bc77f7f221321f1
endif


PKG_HASH:=$(CLASH_HASH)

PKG_SOURCE:=clash-rs-minimal-$(CLASH_TARGET).tar.gz
PKG_SOURCE_URL:=https://github.com/CHKayanami/clash-rs/releases/download/v0.20.24-alpha/
PKG_BUILD_DIR:=$(BUILD_DIR)/clash-rs-minimal-$(CLASH_TARGET)

include $(INCLUDE_DIR)/package.mk

define Package/clash-rs
  SECTION:=net
  CATEGORY:=Network
  TITLE:=clash-rs proxy core (Prebuilt from CHKayanami/clash-rs)
  URL:=https://github.com/CHKayanami/clash-rs
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(TAR) -xzf $(DL_DIR)/$(PKG_SOURCE) --strip-components=1 -C $(PKG_BUILD_DIR)
endef

define Build/Compile
	true
endef

define Package/clash-rs/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/clash-rs $(1)/usr/bin/clash-rs
endef

$(eval $(call BuildPackage,clash-rs))
