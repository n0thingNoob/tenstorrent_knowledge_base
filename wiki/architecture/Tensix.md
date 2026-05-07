---
type: architecture
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, architecture, tensix]
evidence_level: mixed
---

# Tensix

## Summary

A **Tensix tile** (also "T tile", "worker tile", "compute tile") is the workhorse compute element of [[Wormhole]]. Each Tensix contains 1464 KiB of L1 SRAM, five "Baby" RV32IM cores, and a large **Tensix coprocessor** that performs the actual heavy compute. The RISC-V cores act as **orchestrators**, not primary compute engines 鈥?they dispatch instructions to the coprocessor units.

## Components per tile

Per [[Source - tt-isa Tensix Tile]] and [[Source - corsix Part 5 鈥?T Tiles]]:

| Component | Count | Role |
|---|---|---|
| L1 RAM | 1464 KiB | Local SRAM ([[L1 Memory]]) |
| Baby RV32IM cores | 5 | "B", "T0", "T1", "T2", "NC" 鈥?orchestration / kernel dispatch |
| NoC connections | 2 | NoC #0 + NoC #1 ([[NoC]]) |
| NoC overlay | 1 | Coprocessor for assisted NoC transactions |
| Tensix coprocessor | 1 | See sub-units below |
| Utility devices | several | Mover, Mailboxes, TDMA-RISC, DebugTimestamper, PIC |

### Tensix coprocessor sub-units

- **2脳 Unpacker** 鈥?move data from L1 鈫?SrcA / SrcB / Dst
- **1脳 Matrix Unit (FPU)** 鈥?low-precision matrix MAC (2048 multipliers, 7b脳5b)
- **1脳 Vector Unit (SFPU)** 鈥?32-lane 脳 32-bit SIMD (fp32, int32, signmag32). See [[SFPU]].
- **1脳 Scalar Unit (ThCon)** 鈥?integer scalar ops, 128-bit L1 atomics ([[Atomic Counters]])
- **4脳 Packer** 鈥?Dst 鈫?L1 (with optional `+=`, ReLU)
- **ThCfg** 鈥?configuration-register manipulation
- **TDMA**, **Xmov** 鈥?auxiliary movers

> Note: corsix Part 5 lists "8 backend execution resources" including Scalar/ThCfg/Unpack/Matrix/Pack/Vector/TDMA/Xmov. tt-isa lists 4 packers (vs corsix's "1 Pack unit"). Likely the same hardware grouped differently 鈥?flagged in [[questions/README|Questions]].

## Conventional kernel mapping

Per [[Source - METALIUM_GUIDE]] and [[Source - corsix Part 7 鈥?MatMul]]:

| Baby core | Conventional role |
|---|---|
| B (BRISC) | Boot, dispatch helper |
| NC | NoC #1 / writer kernel |
| T0 | Unpacker driver / reader |
| T1 | Math (Matrix + Vector) driver |
| T2 | Packer driver |

But: any RV core can drive any Tensix unit. The convention is just the typical "[[Reader Compute Writer Kernels|reader/compute/writer]]" decomposition.

## Tensix instruction set

Tensix instructions are 32 bits, **disjoint from RV32IM** (low 2 bits never `0b11`). They enter a per-T0/T1/T2 instruction pipe and flow through Macro-Op Expander 鈫?"B"-core injection point 鈫?Replay Expander 鈫?Tensix Sync 鈫?8 backend units.

Mechanisms inside the pipe:

- [[Macro-Op Expander]] 鈥?`MOP` template-based instruction expansion
- [[Replay Expander]] 鈥?record / tee / playback instruction sequences
- [[Tensix Sync]] 鈥?8 mutexes + 8 semaphores + STALLWAIT condition matrix
- 3脳 64-GPR Scalar register file (one per pipe)

## Related pages

- [[Wormhole]], [[L1 Memory]], [[NoC]], [[SFPU]], [[Matrix Unit]], [[Programming Model]], [[Reader Compute Writer Kernels]], [[Circular Buffers]], [[Macro-Op Expander]], [[Replay Expander]], [[Tensix Sync]], [[Atomic Counters]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part6-vector-isa.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-tensix-tile.md`
- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`

