---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, noc, network-on-chip]
evidence_level: official
---

# NoC

## Summary

The **Network on Chip** is the on-die interconnect of [[Wormhole]]. Each ASIC has **two physically independent NoCs** (NoC #0 and NoC #1) forming 2D-torus grids in opposite directions over the same set of tiles. Routers + NIUs (NoC Interface Units) at every tile.

## Topology

- 10×12 logical tile grid; left/right and top/bottom edges are connected (torus).
- NoC #0: combines east-bound + south-bound channels.
- NoC #1: combines west-bound + north-bound channels.
- Each tile-tile link is **256 bits / 32 B per cycle** (per direction).
- Physical tile placement is interleaved (vs the logical grid) to equalise wire lengths around the torus, but software almost always uses logical coordinates.

## Packet & flit format

Per [[Source - tt-isa NoC]]:

- A **transaction** = one or more **packets**.
- A **packet** = exactly one **header flit** + 0–256 **data flits**.
- A **flit** = exactly **256 bits (32 B)**.

So one packet carries up to 8192 B (32 B × 256 data flits) of payload.

## Request types

| Type | Notes |
|---|---|
| Read | Contiguous span from receiver address space → initiator address space |
| Write | Initiator address space (or 32-bit immediate) → receiver. Optional posted (no ack), broadcast to a rectangle of Tensix, [[Multicast|multicast]], NoC-overlay notification |
| Atomic | Acts on 128 b in receiver's L1; 32-bit result back to initiator. See [[Atomic Counters]] |

Writes ≤ 16 B can target an arbitrary subset of 16 bytes (sparse mask). Writes ≤ 32 B can target an arbitrary subset of 32 bytes.

## Virtual channels

Each hop assigns a 4-bit VC number = `{ dateline:1, class:2, buddy:1 }`:
- `class=0b00` / `0b01`: unicast request
- `class=0b10`: broadcast request
- `class=0b11`: response (always unicast, even to broadcast)

The **buddy** bit can flip per hop in response to congestion; software can pin it for stronger ordering at latency cost.

## Performance

| Hop | Throughput | Latency |
|---|---|---|
| NIU → directly connected router | 1 flit / cycle | ~5 cycles |
| Router → router | 1 flit / cycle / axis | **9 cycles** |
| Router → NIU | 1 flit / cycle | ~5 cycles |

Independently confirmed by experiment in [[Source - corsix Part 3 — NoC Propagation]].

Round-trip examples (request + response, same row): 10 hops × 9 cycles = 90 cycles. Same column: 12 × 9 = 108. Different row+col: 198 cycles.

## Ordering

Default: weakly ordered. Strengthening flags include `NOC_CMD_VC_LINKED`, `NOC_CMD_VC_STATIC`, `NOC_CMD_PATH_RESERVE`. RISC-V code initiates transactions via MMIO; completion observed via [[Counters|NoC counters]].

## Deadlock freedom

Hardware guarantees deadlock freedom for common cases. Software is partly responsible when using:
- Multi-packet transactions (`NOC_CMD_VC_LINKED`)
- Broadcast without `NOC_CMD_PATH_RESERVE`
- Non-zero arbitration priority

## Related pages

- [[Multi-ASIC Addressing]], [[Atomic Counters]], [[L1 Memory]], [[NoC Overlay]]
- [[Tensix]], [[Programming Model]], [[Reader Compute Writer Kernels]]

## Sources

- `raw/2026-05-05__github_doc__tt-isa-wormhole-noc.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part1-physicalities.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part3-noc-propagation.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part4-ethernet.md`
- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
