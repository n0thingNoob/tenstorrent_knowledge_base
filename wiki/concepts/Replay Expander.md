---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, tensix, isa]
evidence_level: official
---

# Replay Expander

## Summary

The Replay Expander is the second instruction-amplification stage in each [[Tensix]] pipe (after the [[Macro-Op Expander]]). It can **record** and **playback** sequences of Tensix instructions out of a small per-pipe buffer.

Per [[Source - corsix Part 5 — T Tiles]]:

| Mode | Effect |
|---|---|
| Record | the next `len` instructions arriving at the expander are *swallowed* and written to `buffer[idx:idx+len]` |
| Tee | the next `len` instructions flow through *and* are copied to `buffer[idx:idx+len]` |
| Playback | the expander itself emits `buffer[idx:idx+len]`, one per cycle |

Triggered by `REPLAY(idx, len, mode)`. While in playback, the upstream stream is paused.

## Why this matters

- Combined with the [[Macro-Op Expander]] and `SFPLOADMACRO`, gives the Tensix coprocessor three independent mechanisms for **one Tensix instruction expanding to many**.
- An LLK init phase can record instruction templates, runtime then triggers playback — keeping per-iteration RV core code tiny.
- Reduces per-iteration RV → Tensix MMIO pressure, which matters for hitting peak Matrix-Unit throughput.

## Related pages

- [[Tensix]], [[Macro-Op Expander]], [[Tensix Sync]], [[Programming Model]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
