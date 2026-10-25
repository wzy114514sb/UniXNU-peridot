# UniXNU-peridot — state

## Working
- UEFI (Mu-Silicium peridotPkg + UniXNU menu) boots on the device. Verified.
- Device repo scaffolding: board/soc/peridot, userdata LBAs, firmware paths,
  device_tree dts/peridot.dts, splash 0xe3940000/0x2b00000.
- CI (.github/workflows/build.yml, macos-15): defconfig, fetch, tree,
  kernel bootstrap pass and `build prelink` all succeed.

## Blocked
`unixnu build kernel` needs artifacts produced by a step we have not found:
  tree/build/storage-abi/interface-audit.json   (scripts/audit-storage-interface.py)
  tree/build/xnu-prelink/native-apfs-load-positive.macho
The audit reads compile records from a previous kernel build, while the
kernel build needs the audit for the virtio/ram-block archives — a cycle we
have not resolved. Ordering in the workflow today:
  bootstrap (continue-on-error) -> prelink -> audit -> kernel
and the audit still fails on one of the two files above.

## Facts
- Runner needs Xcode 16 (mig -mach_msg2); macos-15 works, macos-14 fails.
- Runner clang rejects the newer -Wno-* flags; scripts/ci-patch-base.py
  strips them and adds GitHub API auth for prepare-xnu-source.py.
- Base repo (main) has no NativeUfs; it was vendored here as a submodule.
- Component names in the current base: ArmDTPlatform, ArmCpu, SoftwareAES,
  AppleKeyStoreState, Ardeno740, AdrenoMetal, GopFramebuffer, QcomGeniSpi,
  RamBlock, VirtioMmioBlock, DarwinBoot; kits: XnuPrelink, VerifiedRoot,
  AirNir, ArmSmmu4K, AdrenoFirmware, AdrenoPM4.

## Next
Ask the UniXNU group for the exact command order for a new device (the
docs list defconfig/fetch/tree/build kernel/firmware/payload/bootimg but do
not mention the audit and prelink artifacts).
