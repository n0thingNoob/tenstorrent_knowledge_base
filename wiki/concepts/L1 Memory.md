---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, memory, l1, sram]
evidence_level: mixed
---

# L1 Memory

## Summary

"**L1**" in Tenstorrent terminology is the **per-Tensix tile SRAM**, not a CPU-style cache. It is **directly addressable** (no cache coherence, no automatic eviction), accessible by the local 5 RV cores, the local Tensix coprocessor, the local NoC NIUs, and remotely by any other tile via the [[NoC]].

## Capacity

- Per-tile: **1.5 MB advertised**, of which **1464 KiB is L1 SRAM proper**. The remaining ~72 KiB is distributed across other on-tile storage (per [[Source - corsix Part 5 — T Tiles]]):
  - 32 KiB in `Dst`
  - ~30 KiB across the 5 core-local RAMs
  - 4 KiB in `SrcA`, 4 KiB in `SrcB`, 1 KiB in `Lreg`, etc.
- Tile-local address: starts at `0`. L1 is mapped to addresses `0 …` while special MMIO/regs sit above `0xFF000000`.
- Per-core local RAMs: 2 KiB or 4 KiB at `0xFFB00000…`. The C call stack typically lives here (avoids loading L1).
- "NC" core has 16 KiB of instruction RAM at `0xFFC00000…`.

## L1 across the chip

- 80 Tensix × 1464 KiB ≈ 114 MiB of distributed SRAM per ASIC (before harvesting).
- E tiles also have 256 KiB SRAM each.
- **No cache hierarchy on chip.** Data placement is fully explicit.

## Use patterns

- Holds tile-aligned data ([[Tile-Based Execution]]) consumed/produced by Unpacker/Packer.
- Hosts **[[Circular Buffers]]** that synchronise [[Reader Compute Writer Kernels]].
- Can be **interleaved** (default — distributes across DRAM controllers when used as DRAM stage) or **sharded** (placed by topology) — see [tensor_layouts tech report] referenced in [[open_questions]].

## Atomics on L1

L1 supports atomic operations from both:

- Tensix Scalar Unit instructions: `ATSWAP`, `ATCAS`, `ATINCGET`, `ATINCGETPTR` (per [[Source - corsix Part 5 — T Tiles]]).
- Remote tiles via NoC atomic transactions on **128-bit granularity** in receiver L1, returning 32-bit result (per [[Source - tt-isa NoC]]).

These primitives back software [[Atomic Counters]] and lock-free producer-consumer queues.

## Related pages

- [[Tensix]], [[NoC]], [[Circular Buffers]], [[Atomic Counters]], [[Tile-Based Execution]], [[Sharded vs Interleaved]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-tensix-tile.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-noc.md`
- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
