---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, hardware]
evidence_level: official
---

# Harvesting

## Summary

To improve manufacturing yield, **whole rows of [[Tensix]] tiles are disabled** on a Wormhole ASIC if any tile in that row has a defect. Disabled rows are also called **"harvested"** rows.

Per [[Source - corsix Part 1 — Physicalities]] and [[Source - corsix Part 2 — Disabled Rows]]:

- Original silicon: **80** Tensix arranged 8 rows × 10 columns (within the 10×12 grid that includes non-Tensix tiles).
- **n150s**: 1 row harvested ⇒ 72 usable Tensix.
- **n300s**: 2 rows harvested per ASIC ⇒ 64 usable Tensix per ASIC.
- For consistency, harvested rows are disabled even if they had no defects.

## How software discovers harvested rows

Each tile has two MMIO registers controlling NoC-multicast row/column masks:

- `RV_ADDR_NOC0_MC_DISABLE_ROW` at `0xFFB20108`
- `RV_ADDR_NOC0_MC_DISABLE_COL` at `0xFFB20110`

Reading either reveals the per-ASIC harvest pattern. corsix's example: chip 1 of his n300s board reports `33` (rows mask) and `3137` (cols mask), interpreted via bit positions to identify the disabled rows/columns.

## Tile-coord translation feature

To make code portable across different harvest patterns, the NoC has a translation feature:

- X coord 16 → 0 (PCIe/ARC/D column), 17 → 5 (2nd D column), 18..25 → T columns.
- Y coord 16 → 0 (E0–E7 row), 17 → 6 (E8–E15 row), 18..25/26 → active T rows (skipping harvested).

Software can iterate active Tensix tiles by walking 18..25 in both axes without knowing which physical rows are alive.

## Implications

- **Latency to DRAM differs per board** depending on which rows survived. Some rows have 2 D tiles (4 immediately adjacent T tiles); other rows have 1 D tile (2 immediately adjacent T tiles). Which board you got determines how many low-latency-to-DRAM Tensix you have.
- Power and consistency: even chips with no defects ship with rows harvested to match the SKU's promised tile count.

## Research signal

Harvest pattern variance across n300s boards is a real source of perf variance in real fleets. Understanding worst-case vs best-case mapping is a candidate for performance-modelling work.

## Related pages

- [[Wormhole]], [[Tensix]], [[NoC]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part1-physicalities.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part2-disabled-rows.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part3-noc-propagation.md`
