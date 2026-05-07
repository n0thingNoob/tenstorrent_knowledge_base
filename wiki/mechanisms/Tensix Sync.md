---
type: mechanism
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, synchronization, tensix]
evidence_level: official
---

# Tensix Sync

## Summary

"Tensix Sync" is the synchronisation unit at the entry of the [[Tensix]] coprocessor backend. It sits **between the three per-pipe instruction streams (T0/T1/T2) and the 8 backend execution resources** (Scalar, ThCfg, Unpack, Matrix, Pack, Vector, TDMA, Xmov). All Tensix instructions flow through it; some execute *here* (synchronisation primitives), others flow through.

## Local resources

- **8 mutexes**, each in {acquired by T0/T1/T2 pipe, released}.
- **8 semaphores**, each with 4-bit counter + 4-bit max.
- A "STALLWAIT" condition matrix (15 hardware-state flags).

## Instructions executing at Tensix Sync

| Instruction | Effect |
|---|---|
| `ATGETM(idx)` | acquire mutex `idx` for issuing pipe (block on conflict) |
| `ATRELM(idx)` | release mutex `idx` |
| `SEMINIT(max, ctr, mask)` | initialise selected semaphores |
| `SEMPOST(mask)` | counter += 1, saturating at 15 |
| `SEMGET(mask)` | counter -= 1, saturating at 0 |
| `SEMWAIT(to_pause_mask, mask, condition)` | block selected pipe-resources while sem `==0` (cond 1) or `>= max` (cond 2) |
| `STALLWAIT(to_pause_mask, condition_mask)` | block while any of 15 hardware conditions hold |

Instructions other than the above flow through to the backend, **tagged with the pipe they originated from** (which most backend ops care about).

## Why this matters

The three Tensix pipes (one per "T" core) feed shared backend units. Without arbitration the Math unit could be told to compute on `SrcA`/`SrcB` that hasn't yet been filled by Unpacker, etc. Tensix Sync lets the LLK code:

- guard handoff of `Dst` / `SrcA` / `SrcB` between Unpack 鈫?Math 鈫?Pack
- block until a semaphore meets a condition (e.g. "tile in CB available")
- block until a hardware resource is free

This is the **internal synchronisation substrate** that [[Circular Buffers]] sit on top of (probably 鈥?exact mapping to TT-Metal CB metadata not yet pinned down in `raw/`; tracked in [[questions/README|Questions]]).

## MMIO access from "T" cores

- Read sem `i` counter: load from `0xFFE80020 + 4*i`
- `SEMPOST(1<<i)`: store `0` to that address
- `SEMGET(1<<i)`: store `1` to that address

## Related pages

- [[Tensix]], [[Semaphores]], [[Circular Buffers]], [[Macro-Op Expander]], [[Replay Expander]], [[Reader Compute Writer Kernels]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-tensix-tile.md`

