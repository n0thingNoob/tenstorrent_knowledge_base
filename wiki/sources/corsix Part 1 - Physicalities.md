---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, blog]
source_path: raw/2026-05-05__blog__corsix-tt-wh-part1-physicalities.md
evidence_level: blog
---

# Source 鈥?corsix Part 1: Physicalities

## Why it matters

First in a 7-part deep dive of [[Wormhole]] hardware. Establishes the canonical mental model: 10脳12 logical tile grid, tile types, NoC torus topology, dual-NoC layout, and how physical interleaving of tiles is hidden by the logical view. Every later post (and most other sources) refers back to this geometry.

## Key facts

- Wormhole ASIC = 10脳12 logical grid: 80 [[Tensix]] (T), 18 DRAM (D, six 脳 three NIUs), 16 Ethernet (E), 1 PCIe, 1 ARC.
- Each Tensix has 5脳 Baby RV32IM (B/T/T/T/NC), 1.5 MB SRAM, Matrix Unit (2048脳 5b脳7b), Vector Unit (32 lanes 脳 32b).
- Each Ethernet tile drives 100 GbE bidirectional.
- Two NoCs: NoC #0 (east + south) and NoC #1 (west + north). Each tile-tile link = 32 B per cycle (256 b).
- Torus: edges wrap around. Physical placement is interleaved to equalise wire lengths.
- n150s = 12 GiB GDDR6 + one ASIC; n300s = 24 GiB + two ASICs (only first PCIe-connected; second reachable via internal ethernet E8鈫擡0 / E9鈫擡1).
- Manufacturing yield 鈫?row "[[Harvesting]]": n150s ships 72 usable T, n300s ships 64 per ASIC.

## Technical details

**Architecture:** the tile grid is the building block. ARC tile manages the chip via PCIe; PCIe tile bridges to host. Tiles other than empty ones each contain RISCV cores + SRAM + a function-specific bridge.

**NoC:** torus, two physically separate NoCs in opposite directions. 32 B / cycle / link. Going east from rightmost edge wraps to leftmost. (Used by Part 3 to measure 9-cycle hop latency.)

**Memory:** 12 GiB GDDR6 per ASIC, six chips 脳 2 GiB. Each 2 GiB exposed identically through 3 D tiles.

**Synchronisation / kernels:** not covered in this post.

## Related pages

- [[Wormhole]], [[Tensix]], [[NoC]], [[Harvesting]], [[Multi-ASIC Addressing]]

## Open questions

- Exact physical-vs-logical interleaving permutation beyond the documented `HARVESTING_NOC_LOCATIONS`. Captured in [[questions/README|Questions]] but low-priority.

