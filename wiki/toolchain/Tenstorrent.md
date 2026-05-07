---
type: overview
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, ecosystem, toolchain]
evidence_level: official
---

# Tenstorrent

## Summary

Tenstorrent designs and sells RISC-V-based AI accelerators (PCIe cards and rack systems). The company's hardware is built around a grid of "Tensix" compute tiles connected by an on-chip 2D-torus NoC, with an open-source software stack.

## Products

- **[[Wormhole]]** — current shipping ASIC. Boards: n150s, n150d (single ASIC, 12 GiB GDDR6) and n300s, n300d (two ASICs, 24 GiB GDDR6 total).
- **Wormhole Galaxy** — 32-ASIC system.
- **Blackhole** — next-generation ASIC. Boards: p100, p150.
- **Grayskull** — earlier generation (e75, e150). Architecturally older Tensix; superseded by Wormhole.

## Software stack

From highest to lowest abstraction (per [[Source - tt-isa-documentation README]]):

1. [[TT-Forge]] — frontend / framework integration
2. [[TT-NN]] — operator library
3. [[TT-Metal|TT-Metalium]] — low-level programming model
4. [[TT-LLK]] — low-level kernels (Tensix instruction sequences)

Other open-source components: tt-mlir (compiler), tt-kmd (kernel driver), tt-umd (user-mode driver), tt-firmware, tt-flash, tt-topology, tt-smi, tt-exalens.

## Related pages

- [[Wormhole]]
- [[Tensix]]
- [[TT-Metal]]
- [[TT-MLIR]]

## Sources

- `raw/2026-05-05__github_readme__tt-metal-readme.md`
- `raw/2026-05-05__github_readme__tt-isa-documentation-readme.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part1-physicalities.md`
