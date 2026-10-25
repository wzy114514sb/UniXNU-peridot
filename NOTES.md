# UniXNU-peridot — state

Cloned from UniXNU-sheng (template), board.toml partly adapted.

## Done
- board: name=peridot, soc=SM8635, description="Poco F6 / Redmi Turbo 3", kit=peridot
- userdata: first_lba=2437120, last_lba=128628730, lba_bytes=4096
  (from TWRP: userdata start 19496960 x512B, size 0x78587FB000 = 126191611 x4096B)
- firmware: dsc/peridotPkg, fd Build/peridotPkg/{target}_CLANGPDB/FV/SILICIUM_UEFI.fd
- device_tree: dts/peridot.dts (copied from Mu-Silicium Resources/DTBs)
- payload: volume=PERIDOTESP, splash_region=0xe3940000 size 0x2b00000 (from dts)

## Still sheng-specific (must change before a build can work)
- "soc_source" = "sm8550"   -> needs an sm8635 soc source (configs/sm8635.config)
- kernel config_fragments  -> soc:configs/sm8550.config
- kernel archives/components: ShengUfs, Adreno740, ShengHidInput, ShengNovatekTouch ...
  peridot needs SM8635 UFS (ufshc@1d84000, same base as sheng family), its touch IC,
  and its display panel (1220x2712)
- payload kernel_args: all "sheng-*" prefixes and features

## Facts read from peridot.dts
- splash_region 0xe3940000 + 0x2b00000 (SimpleFbDxe FB, 1220x2712)
- ufshc1 = /soc/ufshc@1d84000
- framebuffer/panel: 1220x2712

## Next
1. Decide the SM8635 UFS path: adapt ShengUfs or use generic NativeUfs.
2. Add soc configs/sm8635.config (copy sm8550 and adjust).
3. Push to GitHub, add .github/workflows/build.yml (macos-14) running
   unixnu fetch / tree / build / bootimg.
4. First milestone: CI produces boot.img; menu lists an entry.
