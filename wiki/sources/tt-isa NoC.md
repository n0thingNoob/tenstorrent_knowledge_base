---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, github_doc, noc]
source_path: raw/2026-05-05__github_doc__tt-isa-wormhole-noc.md
evidence_level: official
---

# Source — tt-isa Wormhole NoC

## Why it matters

The **authoritative spec** for Wormhole's [[NoC]]: packet format, virtual channels, broadcast semantics, deadlock guarantees, ordering, and performance. Used as the basis for the [[NoC]] concept page. Independently confirms corsix Part 3's measured 9-cycle hop.

## Key facts

- Two physically separate NoCs (NoC #0 + NoC #1), each a 2D torus.
- Transaction = ≥1 packet; packet = 1 header flit + 0–256 data flits; flit = 256 bits = 32 B.
- Per-link throughput: 1 flit / cycle (both directions).
- Tile-to-tile router-to-router: **9 cycles**.
- NIU↔router: **~5 cycles** each side.
- Request types: **Read**, **Write**, **Atomic**.
  - Writes ≤16 B can target arbitrary subset of 16 B; ≤32 B arbitrary subset of 32 B.
  - Writes can be **posted** (no ack), **broadcast** (Tensix rectangle only), and notify NoC overlay.
  - Atomics act on 128 b in receiver L1, return 32 b. Optionally posted/broadcast.
- DRAM tile NIUs: respond only — no transaction initiation.
- PCIe tile: bi-directional NoC↔AXI↔PCIe translation. Requests > 128 B likely become multiple PCIe TLPs.
- Virtual-channel scheme: 4 b per hop = `{dateline:1, class:2, buddy:1}`. Class enforces unicast-req / broadcast-req / response separation. Buddy bit can flip per hop on congestion (or be statically pinned for stronger ordering).
- Deadlock freedom: **hardware-guaranteed for common cases**; software responsibility kicks in for `NOC_CMD_VC_LINKED`, broadcasts without `NOC_CMD_PATH_RESERVE`, and non-zero arbitration priority.
- Ordering: weakly ordered by default. Strengthening flags: `NOC_CMD_VC_LINKED`, `NOC_CMD_VC_STATIC`, `NOC_CMD_PATH_RESERVE`. Async to RV; counters indicate completion.

## Technical details

**Architecture:** routers + NIUs at every tile. Empty tiles have routers + NIUs but only the NIU's own status registers are addressable.

**Memory:** DRAM tiles' NIUs (3 per NoC × 6 controllers = 18) all access the same 2 GiB.

**Synchronisation:** atomics, optional path-reservation broadcasts, ordering flags.

**Performance:** 9-cycle hop empirically confirmed by corsix Part 3.

## Related pages

- [[NoC]], [[Atomic Counters]], [[Multi-ASIC Addressing]], [[Wormhole]], [[L1 Memory]]

## Open questions

- Sub-pages (Atomics.md, Ordering.md, MemoryMap.md, Counters.md, RoutingPaths.md, Overlay/) are linked but not yet captured. Pass-2 priority.
- Detailed virtual-channel routing (which dateline-bit-flip points are statically chosen? how is `NOC_CMD_PATH_RESERVE` arbitrated?) not in this page.
