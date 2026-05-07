---
type: mechanism
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, tensix, isa]
evidence_level: official
---

# Macro-Op Expander

## Summary

Inside each Tensix pipe (one per T0/T1/T2 core), the **Macro-Op Expander** sits between the instruction-pipe entry and the [[Replay Expander]]. It implements a programmable instruction expansion: a single `MOP` instruction triggers an expansion through one of two hardware **templates** that emit further Tensix instructions.

This lets one RV-core write per loop iteration drive many cycles of Tensix-backend work — the RV core gains slack to do control flow.

## Configuration

| Item | Notes |
|---|---|
| `MOP_CFG(zhi)` | sets a 16-bit register inside the expander |
| `mop_cfg[0..8]` | 9 32-bit slots, set by writes to `0xFFB80000 …` from the associated T core |
| `MOP(template, count1, zlo)` | runs template 0 or template 1 with `count1+1` iterations and a 32-bit `zmask` from `(zhi << 16) | zlo` |

## Template 0 (z-mask iteration)

Walks `count1+1` iterations, branching per low bit of `zmask`:

- bit 0: emit `mop_cfg[3]`, optionally `mop_cfg[4..6]` (flag 0x02), optionally `mop_cfg[2]` (flag 0x01).
- bit 1: emit `mop_cfg[7]`, optionally `mop_cfg[8]`.

Useful for sparse / patterned dispatch — the bitmask drives which sequence of instructions runs each iteration.

## Template 1 (i,j nested loop)

Two nested loops `i_count × j_count`. `mop_cfg[5]` is the inner instruction (with optional XOR-flip on every other iteration via `mop_cfg[6]`). `mop_cfg[2]` and `mop_cfg[3..4]` bracket each `i` iteration; `mop_cfg[7]/[8]` handle the last-iteration corners.

This is a natural fit for tiled matrix-multiply control flow.

## Why this matters

- A single `MOP` instruction can output dozens or hundreds of Tensix instructions without further RV-core writes.
- Combined with the [[Replay Expander]] and `SFPLOADMACRO`, Wormhole has **three independent mechanisms** for one instruction expanding to many — extreme amplification of dispatch bandwidth.
- Architectural curiosity: this is closer in spirit to a CGRA's static schedule template than to a CPU's instruction stream.

## Related pages

- [[Tensix]], [[Replay Expander]], [[Tensix Sync]], [[Compiler Stack]], [[Programming Model]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md`
