---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, synchronization, kernels]
evidence_level: official
---

# Circular Buffers

## Summary

A **circular buffer (CB)** in [[TT-Metal]] is a producer-consumer FIFO **in [[L1 Memory]]** with hardware-assisted metadata synchronisation. CBs are how the [[Reader Compute Writer Kernels|reader, compute, and writer]] kernels exchange tile data without explicit semaphores in the user-visible code.

Per [[Source - METALIUM_GUIDE]]:

> "These circular buffers act as producer-consumer queues, enabling safe and efficient data exchange between kernels."

## API surface (kernel-side)

| Call | Role | Side |
|---|---|---|
| `cb_reserve_back(cb, n)` | wait for `n` free tiles, get write ptr | producer |
| `cb_push_back(cb, n)` | mark `n` tiles as full | producer |
| `cb_wait_front(cb, n)` | wait for `n` tiles available, get read ptr | consumer |
| `cb_pop_front(cb, n)` | release `n` tiles | consumer |
| `get_tile_size(cb)` | bytes per tile in this CB | both |
| `get_write_ptr(cb)` / `get_read_ptr(cb)` | L1 addresses | both |

In compute kernels, each call only emits code on the appropriate baby core (Unpack vs Pack vs Math) — selection is automatic.

## API surface (host-side)

```cpp
constexpr auto cb_in0_index = tt::CBIndex::c_0;
CBHandle cb_in0 = CreateCircularBuffer(
    program, core,
    CircularBufferConfig(
        /*total_size=*/tiles_per_cb * tile_size_bytes,
        /*data_format_spec=*/{{cb_in0_index, tt::DataFormat::Float16_b}})
        .set_page_size(cb_in0_index, tile_size_bytes));
```

`tiles_per_cb >= 2` is the typical knob — larger gives better overlap between data movement and compute, but with diminishing returns and L1 budget pressure. CB indices `c_0`, `c_1`, `c_16`, etc. are arbitrary — only uniqueness matters.

## Why this matters

CBs are the central synchronisation primitive of the [[Programming Model]]: they hide the fact that NoC, Unpacker, Pack, and the Math units all run independently and asynchronously. Backpressure is automatic — `cb_reserve_back` blocks the producer when the buffer is full; `cb_wait_front` blocks the consumer when empty.

Implementation note: the underlying hardware metadata is touched by both producer-side and consumer-side calls; corsix Part 5 documents per-tile semaphores and ThCon's `ATINCGETPTR` FIFO atomic — which is precisely a hardware FIFO control structure. Whether TT-Metal's CB metadata is implemented via these atomics or via the dedicated per-pipe Tensix Sync semaphores is **not yet pinned down in `raw/`** ([[open_questions]]).

## Cross-kernel vs self-loop

CBs can also be used by a single kernel to communicate with itself across iterations (per the METALIUM_GUIDE diagram caption "send data cross-kernel or itself").

## Related pages

- [[Reader Compute Writer Kernels]], [[Semaphores]], [[Atomic Counters]], [[L1 Memory]], [[Programming Model]], [[Tile-Based Execution]], [[Tensix Sync]]

## Sources

- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
