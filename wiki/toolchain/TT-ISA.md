---
type: toolchain
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, isa, blackhole]
evidence_level: official
---

# TT-ISA

## Summary

`tenstorrent/tt-isa-documentation` is the official open repository of **low-level architecture documentation** for Tenstorrent silicon. Two architectures are covered: **Wormhole B0** (n150/n300/Galaxy) and **Blackhole A0** (p100/p150).

Intended audience per the README: "software developers writing code at, or below, the level of [[TT-LLK]]" — i.e. anyone going below the [[TT-Metal]] compute API.

## Relation to other layers

```
TT-Forge (highest)
   ↓
TT-NN
   ↓
TT-Metalium
   ↓
TT-LLK
   ↓
TT-ISA  ← this repo's documentation level
```

## What "TT-ISA" actually documents

For Wormhole B0, the README enumerates per-tile content of the ASIC:

- 80 [[Tensix]] tiles (some fused-off via [[Harvesting]])
- 18 DRAM tiles (12 GiB GDDR6 total; each 2 GiB shared by 3 tiles)
- 16 Ethernet tiles (100 GbE bidirectional each)
- 1 PCIe tile (PCIe 4.0 x16)
- 1 ARC tile (board management)
- 2 [[NoC|NoCs]] forming a 2D torus

The repo organises material as a per-tile / per-component tree (TensixTile/, NoC/, EthernetTile/, DRAMTile/, PCIExpressTile/, ARCTile/).

Note: this is **not** a single-document opcode reference. It's a structured set of pages covering tile internals, memory maps, NoC packet semantics, atomics, ordering, etc.

## Tensix ISA proper (instruction-level)

Tensix instructions are 32-bit, disjoint from RV32IM (low 2 bits never `0b11`), with 8-bit opcodes (values < 0xC0 used). Authoritative-but-imperfect references discovered:

- `tt-budabackend/.../assembly.yaml` (per [[Source - corsix Part 5 — T Tiles]])
- `tt-llk-wh-b0/common/inc/ckernel_ops.h` (C-header generated from the YAML)

The tt-isa-documentation repo is the cleaner narrative replacement for these source-only references, but instruction-level pages are still being filled in.

## Related pages

- [[Tensix]], [[NoC]], [[L1 Memory]], [[TT-LLK]], [[TT-Metal]], [[Compiler Stack]]

## Sources

- `raw/2026-05-05__github_readme__tt-isa-documentation-readme.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-overview.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-tensix-tile.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-noc.md`
