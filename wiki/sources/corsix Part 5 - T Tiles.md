---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, blog, tensix]
source_path: raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md
evidence_level: blog
---

# Source — corsix Part 5: Taking Apart T Tiles

## Why it matters

**The single densest architectural reference in the corpus.** Documents the internal structure of a [[Tensix]] tile, the per-pipe Tensix instruction stream, and the synchronisation / configuration primitives. Every concept page on Tensix internals (Macro-Op, Replay, Tensix Sync, Atomic Counters, ThCon GPRs, configuration registers) cites this post.

## Key facts

- Each Tensix has 1464 KiB L1 + 5 RV32IM cores (B/T0/T1/T2/NC) + the **Tensix coprocessor**.
- Tensix coprocessor has 8 backend execution resources: Scalar (ThCon), ThCfg, Unpack, Matrix (FPU), Pack, Vector (SFPU), TDMA, Xmov.
- Each "T" core has its own **instruction pipe** containing a Macro-Op Expander, B-core injection point, and Replay Expander, feeding into Tensix Sync, then the 8 backend units.
- Tensix instructions are 32-bit, low 2 bits never `0b11` (so disjoint from RV32IM); rotated 2 bits left by hardware so RV32 cores can dispatch them via the "T6 as RVC" trick.
- **Macro-Op Expander**: `MOP_CFG(zhi)` + `MOP(template, count1, zlo)` runs one of two hardware templates emitting many backend instructions per single MOP.
- **Replay Expander**: `REPLAY(idx, len, mode)` records / tees / plays back instruction sequences.
- **Tensix Sync**: 8 mutexes (per-pipe ownership), 8 semaphores (4-bit counter + 4-bit max), instructions `ATGETM/ATRELM/SEMINIT/SEMPOST/SEMGET/SEMWAIT/STALLWAIT`.
- **Tensix Scalar (ThCon)**: 3× 64× 32-bit GPRs (one bank per pipe). Instructions: `SETDMAREG`, `ADD/SUB/MUL/BITWOP/CMP/SHIFT-DMAREG`, `LOADIND/STOREIND`, atomic ops `ATSWAP/ATCAS/ATINCGET/ATINCGETPTR`, `LOADREG/STOREREG`. MMIO at `0xFFE00000…`.
- **Configuration registers**: 261 per-pipe (16-bit packed in 57× 16b per pipe; set via `SETC16`) + 248+26+39+174 unit-specific (32-bit packed; double-buffered by `CFG_STATE_ID::StateID`; set via `WRCFG`/`REG2FLOP`/`RMWCIB`).
- "L0" — referenced by some Tensix instructions; possibly a hardware-managed cache, **unconfirmed**.

## Technical details

**Architecture:** the most complete on-chip dataflow inside a Tensix in the entire corpus. This is the page that tells you the difference between Unpack/Pack/Math/Vector and how they're driven from per-T instruction pipes.

**Memory:** L1 layout — 1464 KiB SRAM at addr 0+, 1 MB MMIO range at 0xFFB00000+, instruction RAM at 0xFFC00000+.

**Synchronisation:** mutexes, semaphores, STALLWAIT, MMIO sem control. ThCon atomics: `ATCAS`, `ATINCGET` (counter), `ATINCGETPTR` (FIFO control) — the substrate for [[Atomic Counters]] and likely for [[Circular Buffers]].

**Compiler/runtime:** describes the LLK init/runtime split and three layers of op wrappers (`TT_OP_X`, `TT_X`, `TTI_X`).

## Related pages

- [[Tensix]], [[Macro-Op Expander]], [[Replay Expander]], [[Tensix Sync]], [[Semaphores]], [[Atomic Counters]], [[L1 Memory]], [[Matrix Unit]], [[SFPU]], [[Compiler Stack]], [[Reader Compute Writer Kernels]]

## Open questions

- "L0" — actual existence, capacity, semantics.
- Detailed mapping from TT-Metal CB metadata to ThCon atomics vs Tensix Sync semaphores.
