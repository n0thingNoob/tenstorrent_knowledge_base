---
type: architecture
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, architecture]
evidence_level: mixed
---

# Wormhole

## Summary

Wormhole is the Tenstorrent ASIC currently shipping to customers. Each ASIC is a **10×12 logical grid of tiles** with two 2D-torus [[NoC|NoCs]] in opposing directions. The shipping silicon is "Wormhole B0".

## Tile inventory (per ASIC)

| Tile type | Logical count | Per-tile contents |
|---|---|---|
| [[Tensix]] (T) | 80 (some fused-off via [[Harvesting]]) | 1.5 MB / 1464 KiB L1, 5× Baby RV32IM, Tensix coprocessor (Matrix/Vector/Unpack/Pack/Scalar/ThCfg/TDMA/Xmov) |
| DRAM (D) | 18 (6 controllers × 3 NIUs) | Bridge to 2 GiB GDDR6 each; each 2 GiB shared by 3 tiles, 12 GiB total |
| Ethernet (E) | 16 | Baby RV32IM, 256 KiB SRAM, 100 GbE bidirectional bridge |
| PCIe | 1 | Bridge to host (PCIe 4.0 x16) |
| ARC | 1 | ARC core for board management |
| Empty | rest of grid | Router + NIU only |

Source: [[Source - corsix Part 1 — Physicalities]], [[Source - tt-isa Wormhole Overview]].

## Boards

- **n150s / n150d** — 1× Wormhole ASIC, 12 GiB GDDR6, 72 usable Tensix (1 row harvested).
- **n300s / n300d** — 2× Wormhole ASICs (1× PCIe + 1× ethernet-connected), 24 GiB GDDR6, 64 usable Tensix per ASIC (2 rows harvested).
- **Galaxy / QuietBox** — multi-ASIC scale-up.

Connectivity: 2× QSFP-DD cages (E0/E1, E6/E7), 2× Warp 100 Bridge connectors, internal E8↔E0 / E9↔E1 links between ASICs on n300s.

## Key performance numbers

- Tile-to-tile NoC propagation delay: **9 cycles per hop** ([[Source - tt-isa NoC]] official, [[Source - corsix Part 3 — NoC Propagation]] confirmed by measurement).
- NoC throughput per hop per axis: **256 bits (32 B) per cycle**.
- Matrix unit per Tensix: **2048 multipliers (7b × 5b)** giving 4.096 TFLOP/s at LoFi (fp8) — half at LoFi+HiFi2 (bfp8), quarter at full LoFi+HiFi2+HiFi3+HiFi4 (fp16). See [[Fidelity Stages]].
- n150s: 73.7 TFLOP/s fp16; n300s: 131.1 TFLOP/s fp16.

## Related pages

- [[Tensix]], [[NoC]], [[L1 Memory]], [[Multi-ASIC Addressing]], [[Harvesting]], [[Fidelity Stages]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part1-physicalities.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part4-ethernet.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-overview.md`
- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
