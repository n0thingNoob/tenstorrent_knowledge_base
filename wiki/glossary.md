# Glossary

Tenstorrent Wormhole-specific terms and abbreviations.

| Term | Expansion / meaning |
|---|---|
| **ARC** | Argonaut RISC Core — board-management core in the ARC tile |
| **ASIC** | Application-Specific Integrated Circuit; here = one Wormhole chip |
| **BAR** | PCIe Base Address Register; mapped into host VA |
| **bf16 / bfp4 / bfp8** | bfloat16 / 4-bit / 8-bit block-float formats |
| **B core** | Tensix's "BRISC" RV core — boot, dispatch helper |
| **CB** | [[Circular Buffer|Circular Buffer]] — producer/consumer FIFO in L1 |
| **CGRA** | Coarse-Grain Reconfigurable Array (architectural point of comparison) |
| **CQ** | Command Queue (TT-Metal) or Completion Queue (E-tile firmware) |
| **D tile** | DRAM tile (bridges to GDDR6) |
| **Dst** | Destination register inside Tensix; output of Matrix unit, input/output of SFPU |
| **DM0 / DM1** | Data Movement RV cores 0/1 (drive NoC #0 / #1 respectively in conventional mapping) |
| **E tile** | Ethernet tile (100 GbE bidirectional) |
| **EDM** | Ethernet Data Mover — kernels that route traffic across multi-chip ethernet |
| **FMA / FMAC** | Fused multiply-add / multiply-accumulate |
| **FPU** | "Floating-Point Unit"; here = Tensix's [[Matrix Unit]] |
| **HiFi2/3/4** | High-fidelity multi-stage matmul stages — see [[Fidelity Stages]] |
| **L0** | Possible Tensix-internal cache; existence/size unconfirmed in `raw/` |
| **L1** | Per-Tensix SRAM, 1464 KiB; not a cache — see [[L1 Memory]] |
| **LLK** | Low-Level Kernels — Tensix instruction sequences (lib `tt-llk`) |
| **LoFi** | Low-fidelity matmul stage (multiplier alone) |
| **MAC** | Multiply-Accumulate |
| **MeshDevice** | TT-Metal device handle; even single-chip = 1×1 mesh |
| **MOP** | Macro-Op — Tensix instruction triggering Macro-Op Expander |
| **n150s/d, n300s/d** | Wormhole boards: n150 = 1 ASIC, n300 = 2 ASICs |
| **NC core** | Tensix's "NCRISC" — one of the 5 RV cores (often = NoC #1 / writer) |
| **NIU** | NoC Interface Unit — entry/exit point of a NoC |
| **NoC** | Network-on-Chip — see [[NoC]] |
| **PCIe tile** | Bridges host PCIe to NoC (1 per ASIC) |
| **QSFP-DD** | Form factor for 100GbE direct-attach cabling on Wormhole boards |
| **RV / RV32IM / Baby RISC-V** | The 5 small RISC-V cores in each Tensix |
| **SFPI** | The userspace SFPU compiler / toolchain (repo `tenstorrent/sfpi`) |
| **SFPU** | "Special Function Processing Unit" = Tensix [[SFPU|Vector unit]] |
| **SPMD / MPMD** | Single / Multiple Program, Multiple Data |
| **SrcA / SrcB** | Tensix Matrix-unit input registers, fed by Unpacker |
| **SQ** | Submission Queue (E-tile firmware) |
| **STALLWAIT** | Tensix instruction blocking pipe on hardware-state condition |
| **T0 / T1 / T2** | The three "T" RV cores per Tensix (typically Unpack/Math/Pack drivers) |
| **T tile** | Tensix tile — see [[Tensix]] |
| **Tensix Sync** | Internal sync unit of Tensix coprocessor — see [[Tensix Sync]] |
| **ThCon** | Tensix Scalar Unit — integer ops, atomics, GPRs |
| **ThCfg** | Tensix Configuration unit — sets per-pipe configuration registers |
| **Tile** | 32×32 element block — the API unit in [[TT-NN]] / Compute API |
| **Face** | 16×16 element block — sub-tile internal unit |
| **TLB (Tenstorrent)** | Configurable host-MMIO ↔ NoC-target window; **not** a CPU TLB |
| **TT-Metal / TT-Metalium / Metal** | Tenstorrent's low-level SDK |
| **TT-NN** | Neural-network op library on top of TT-Metal |
| **TT-MLIR** | MLIR compiler targeting TTNN |
| **TT-Forge** | Highest-level frontend bridging frameworks to TT-MLIR |
| **TT-LLK** | Low-Level Kernels repository |
| **TT-Fabric** | Multi-host scale-out routing firmware |
| **VC** | Virtual Channel (in NoC) |
| **WC / UC** | Write-Combining / Uncacheable (host PCIe BAR mapping mode) |
| **Warp 100 Bridge** | Tenstorrent-proprietary 100Gb ethernet connector |
