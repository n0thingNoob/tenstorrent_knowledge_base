---
type: mechanism
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, synchronization, atomics]
evidence_level: official
---

# Atomic Counters

## Summary

Wormhole offers atomic primitives at **two granularities**:

1. **Tensix Scalar Unit (ThCon)** 鈥?atomics on **L1 / L0** within the local Tensix.
2. **NoC** 鈥?atomic transactions on **128 b in a remote tile's L1**, returning 32 b to the initiator.

Both can be used to build software-level **atomic counters**, lock-free queues / FIFOs, and producer-consumer synchronisation between distant tiles.

## Tensix Scalar atomics (local)

Per [[Source - corsix Part 5 鈥?T Tiles]]:

| Instruction | Behaviour (pseudo) |
|---|---|
| `ATSWAP(l1, mask, gpr_data, gpr_base)` | atomic swap of up to 128 b between 4 GPRs and L0/L1 at `gpr_base*16`; `mask` selects which of 8 16-bit lanes swap |
| `ATCAS(l1, set_val, cmp_val, ofs, gpr_base)` | retry until `*word == cmp_val`, then `*word = set_val` (4-bit values) |
| `ATINCGET(l1, len, ofs, gpr_data, gpr_base)` | atomic increment of `*word` by `gpr_data` modulo `2^(len+1)`; returns prior `*word` |
| `ATINCGETPTR(l1, no_incr, incr_log2, len, ofs, gpr_data, gpr_base)` | atomic FIFO control: ptr increment iff FIFO non-empty/non-full; returns prior ptr |

`ATINCGETPTR` is essentially **a hardware FIFO control primitive**. This is highly suggestive of the substrate underneath [[Circular Buffers]].

## NoC atomics (remote)

Per [[Source - tt-isa NoC]]:

- An **Atomic** packet acts on **128 bits in receiver's L1**.
- Returns a **32-bit result** back to (usually) initiator's L1.
- Optionally **posted** (no response) and optionally **broadcast** to a Tensix rectangle.

Detailed semantics live in `WormholeB0/NoC/Atomics.md` and `WormholeB0/TensixTile/L1.md#atomics` 鈥?**not yet in `raw/`**.

## Use cases

- **Software counters across cores / tiles** 鈥?increment with NoC atomic; threshold trigger via [[Semaphores]] + STALLWAIT.
- **Lock-free producer/consumer queues** 鈥?`ATINCGETPTR` for ring-buffer pointers; underpins potential implementations of [[Circular Buffers]].
- **Distributed barriers / collectives** 鈥?atomic decrements signalling "N-1 cores done".
- **Replacing 2-semaphore handshakes** 鈥?single counter increment on producer side; consumer reads; less round-tripping than post+wait.

## Research signal

The user's stated interest is in *replacing two-semaphore handshakes with atomic counters*. The hardware primitives above are precisely the surface that enables that. Open question: which TT-Metal/TT-NN ops still use 2-step handshakes that could be folded into a single atomic increment? Tracked in [[questions/README|Questions]].

## Related pages

- [[Semaphores]], [[Circular Buffers]], [[NoC]], [[L1 Memory]], [[Tensix]], [[Programming Model]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-noc.md`

