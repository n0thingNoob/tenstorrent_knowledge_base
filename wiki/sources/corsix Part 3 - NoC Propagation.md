---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, blog, noc]
source_path: raw/2026-05-05__blog__corsix-tt-wh-part3-noc-propagation.md
evidence_level: blog
---

# Source — corsix Part 3: NoC Propagation Delay

## Why it matters

Direct experimental measurement of [[NoC]] tile-to-tile latency. **Confirms the official 9-cycle figure** (later corroborated by [[Source - tt-isa NoC]]). Also documents the soft-reset and per-tile cycle-counter mechanism that any custom microbenchmark on Wormhole would need.

## Key facts

- Each Tensix has a **64-bit cycle counter** at `0xFFB121F0/0xFFB121F8`, increments every clock, starts at chip power-on.
- Each Tensix has a **soft-reset register** at `0xFFB121B0`. Value `0x47800` = all 5 baby cores held in reset; clearing individual bits releases individual cores.
- Methodology: NoC-multicast a 6-instruction RV stub to every Tensix at L1 address 0; the stub records `cycle_counter` to L1 byte 128 and spins. Then unicast-read every tile's byte 128 to gather measurements.
- Tile-coord translation feature: X coords 16/17/18..25 and Y coords 16/17/18..25 map to the right physical tile types (PCIe/ARC vs D vs T) regardless of harvest pattern.
- Result after correcting for per-tile cycle-counter offset: **tile-to-tile propagation delay = 9 cycles** ≈ 9 ns at 1 GHz.
- For round-trips (NoC read or ack'd write), latency includes both directions on the same NoC: 10 hops same-row = 90 cycles, 12 hops same-col = 108 cycles, mixed = 198 cycles.

## Technical details

**Architecture:** documents the cycle-counter, soft-reset, and tile-coord-translation mechanisms — three things you need before you can run any Tensix microbenchmark.

**NoC:** the 9-cycle hop figure here matches the official table in `tt-isa-documentation/NoC/README.md`, raising confidence in both.

**Synchronisation:** the soft-reset register is also how host code starts/stops kernels at low level (in the absence of TT-Metal).

## Related pages

- [[NoC]], [[Tensix]], [[Wormhole]]

## Open questions

- Per-tile cycle-counter skew (a few cycles) noted by corsix — not pinned down. If we ever need cycle-accurate cross-tile traces, this matters.
