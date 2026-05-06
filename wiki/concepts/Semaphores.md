---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, synchronization]
evidence_level: official
---

# Semaphores

## Summary

Wormhole has multiple synchronisation surfaces called "semaphore" at different levels of the stack. Don't confuse them.

## 1. Tensix Sync semaphores (per Tensix tile)

Inside each [[Tensix]] coprocessor's "Tensix Sync" unit (per [[Source - corsix Part 5 — T Tiles]]) are **8 semaphores**, each with:

- 4-bit **counter** value
- 4-bit **maximum** value (initialised by `SEMINIT`, used only by `SEMWAIT`)

### Tensix instructions

| Instruction | Effect |
|---|---|
| `SEMINIT(max, ctr, mask)` | set max + counter for selected semaphores |
| `SEMPOST(mask)` | counter += 1, saturating at 15 |
| `SEMGET(mask)` | counter -= 1, saturating at 0 |
| `SEMWAIT(to_pause_mask, mask, condition)` | block selected execution resources of *this pipe* while any selected semaphore is `==0` (cond 1) or `>= max` (cond 2) |

### MMIO from "T" cores

- Read counter `i`: load from `0xFFE80020 + 4*i`
- `SEMPOST(1<<i)`: store 0 to that address
- `SEMGET(1<<i)`: store 1 to that address

Note: writing 0 does post, writing 1 does decrement. Counter-intuitive but documented.

## 2. Tensix Sync mutexes

Same unit also has **8 mutexes**, each in one of {acquired by T0, T1, T2 pipe, released}. Instructions: `ATGETM(idx)`, `ATRELM(idx)`. Different from semaphores — fewer states, single owner.

## 3. STALLWAIT (broader condition)

`STALLWAIT(to_pause_mask, condition_mask)` blocks selected execution resources while any of 15 non-semaphore conditions hold (e.g. SrcA/SrcB validity, certain unit busy). Used to pause a pipe pending hardware-state events that aren't software-incremented counters.

## 4. TT-Metal-level "host semaphores"

[[TT-Metal]] also exposes a higher-level semaphore primitive (`CreateSemaphore` style, not yet in `raw/`) used for cross-tile synchronisation in multi-core kernels. These are **L1-resident counters** manipulated via NoC writes/atomics — orthogonal to the on-chip Tensix Sync hardware semaphores. **Detail not yet captured in `raw/`** ([[open_questions]]).

## When you'd use which

| Need | Use |
|---|---|
| Wait for an internal Tensix unit (Unpacker/Math/Pack) to finish | `STALLWAIT` or `SEMWAIT` on a Tensix Sync semaphore |
| Wait for a tile to arrive in an L1 circular buffer | [[Circular Buffers]] APIs (which, internally, use atomics or hardware-managed metadata) |
| Cross-Tensix synchronisation | TT-Metal host-level semaphores + NoC writes/atomics |
| Lock-free queues | [[Atomic Counters]] (NoC atomics or `ATINCGETPTR`) |

## Related pages

- [[Tensix Sync]], [[Atomic Counters]], [[Circular Buffers]], [[NoC]], [[Programming Model]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
