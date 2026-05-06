---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, github_doc, programming-model]
source_path: raw/2026-05-05__github_doc__tt-metal-metalium-guide.md
evidence_level: official
---

# Source — TT Architecture and Metalium Guide

## Why it matters

**The canonical official programming-model reference** for [[TT-Metal]]. Pairs with corsix Part 5 (hardware) to give the full hardware-software story. Source for nearly every concept page in the wiki.

## Key facts

- Each [[Tensix]] = 5 baby RV cores + 2 NoC + Matrix (FPU) + Vector (SFPU) + Pack/Unpack + 1.5 MB SRAM (called "L1").
- Two NoCs traverse the chip in opposite directions; quasi-full-duplex with wraparound topology.
- Conventional kernel decomposition: **reader (NoC0)** + **compute (Unpack/Math/Pack co-op)** + **writer (NoC1)**, coordinating via [[Circular Buffers]] in L1.
- Mesh-first API: `MeshDevice::create_unit_mesh()` even for single-chip programs.
- Tile = 32×32; tilization/untilization can run on-device.
- Two CQs per device, conventional split = compute (Q0) + transfer (Q1); event-based ordering via `enqueue_record_event` / `enqueue_wait_for_event`.
- **Compute API** is the hardware-portability layer. `sin_tile()` lowers to different SFPU sequences on Grayskull (64-lane, 4 iters), Wormhole (32-lane, 8 iters), Blackhole.
- Slow-dispatch mode (`TT_METAL_SLOW_DISPATCH_MODE=1`) blocks host on every op — debug only.
- Multi-chip: standard 100 GbE links between ASICs (no NVLink-style proprietary interconnect). EDM (Ethernet Data Mover) handles routing.
- Galaxy = 32-chip mesh per host; multi-host meshes routed by tt-Fabric firmware.

## Technical details

**Architecture:** explains DRAM-controller layout, "interleaved" vs "sharded" memory placement (sharded for attention/conv).

**Memory:** explicit DMA only — no cache hierarchy. SRAM is addressable, not transparent cache.

**NoC:** opposing-direction NoCs, wraparound torus, sometimes both NoCs used simultaneously to double bandwidth.

**Synchronisation:** circular-buffer producer-consumer via hardware metadata; events for cross-CQ ordering.

**Compiler / runtime:** Compute API templates, `tile_regs_acquire/commit/wait/release` dance, `split_work_to_cores` SPMD helper.

**Performance:** Tile-native execution avoids GPU-style row-buffering; references `GEMM_FLOPS.md` (not in `raw/`).

## Related pages

- [[TT-Metal]], [[Programming Model]], [[Reader Compute Writer Kernels]], [[Circular Buffers]], [[Tile-Based Execution]], [[Tensix]], [[NoC]], [[L1 Memory]], [[Compiler Stack]], [[Multi-ASIC Addressing]]

## Open questions

- "GPU experts" / "CPU experts" sections are summary prose without measurement — useful for orientation, not for citations.
- Some claims (e.g. SRAM as L1, "no cache coherency") are slightly imprecise (corsix shows core-local stack RAMs, debug-timestamper, etc. — there's more on-tile storage than "1.5 MB L1").
