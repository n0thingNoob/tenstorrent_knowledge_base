---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, github_doc, tensix]
source_path: raw/2026-05-05__github_doc__tt-isa-wormhole-tensix-tile.md
evidence_level: official
---

# Source — tt-isa Wormhole Tensix Tile

## Why it matters

Tenstorrent's own per-Tensix component catalogue. Confirms corsix Part 5's enumeration with one notable difference (4 Packers vs 1 Pack unit framing — see Open questions).

## Key facts

Each Tensix contains:

- 1464 KiB L1
- 5× Baby RV32IM cores
- 2× NoC connections + 1× NoC overlay
- Tensix coprocessor with:
  - **2× Unpacker**
  - 1× Matrix Unit (FPU) — low-precision MAC + other matrix ops
  - 1× Vector Unit (SFPU) — 32-wide × 32-bit SIMD
  - 1× Scalar Unit (ThCon) — 32-bit integer ops + 128-bit L1 atomics
  - **4× Packer**
- Utility devices: Mover, Mailboxes, TDMA-RISC, DebugTimestamper, PIC.

Stated programming convention: "two RISCV cores oversee the NoC and three RISCV cores oversee the Tensix coprocessor". The RV cores are explicitly orchestrators, not high-perf compute.

## Technical details

**Architecture:** confirms RV-as-orchestrator design philosophy.

**Memory:** L1 entry only (deeper detail in `L1.md`, not yet captured).

## Related pages

- [[Tensix]], [[L1 Memory]], [[Matrix Unit]], [[SFPU]], [[NoC]], [[Atomic Counters]]

## Open questions

- **4 Packers vs 1 Pack unit**: this page lists 4 Packers; corsix Part 5 lists "1 Pack" as one of the 8 backend execution resources. Likely the same hardware described differently (4 Pack pipelines being addressed via the single Pack instruction-pipe interface), but **not pinned down** — flagged in [[open_questions]].
- Sub-pages (`L1.md`, `BabyRISCV/README.md`, `TensixCoprocessor/{MatrixUnit,VectorUnit,ScalarUnit,Unpackers,Packers}.md`) are linked but not yet captured. Pass-2 priorities.
