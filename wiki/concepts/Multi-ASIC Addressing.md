---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, ethernet, scaleout]
evidence_level: official
---

# Multi-ASIC Addressing

## Summary

[[Wormhole]] uses a custom **6-dimensional addressing scheme** for cross-ASIC and cross-rack communication via Ethernet. Per [[Source - corsix Part 4 — Ethernet]] (`routing_cmd_t` structure):

| Dimension | Bits | Range | Meaning |
|---|---|---|---|
| NoC X | 6 | within ASIC | tile X coord |
| NoC Y | 6 | within ASIC | tile Y coord |
| Shelf X | 6 | within shelf | ASIC column |
| Shelf Y | 6 | within shelf | ASIC row |
| Rack # | 8 | within aisle | rack index |
| Shelf # (Rack Y) | 8 | within rack | shelf index |

Every NoC transaction sent to the **base firmware on an Ethernet tile** (`routing_cmd_t`) carries this 6-tuple plus a 32-bit tile-local target address.

## Routing decision (per E-tile firmware)

When an E-tile receives a request:

1. If target = self → execute via local RV load/store.
2. Else if target is on the same ASIC → satisfy via local NoC #0 (default) or NoC #1 (if `CMD_USE_NOC1`).
3. Else → forward via ethernet (either to the link-partner E-tile or to another local E-tile that is closer to the destination).

## Boards in this taxonomy

- **n150s**: rack#=0, shelf#=0, shelf=(0,0). One ASIC.
- **n300s**: rack#=0, shelf#=0, with shelf=(0,0) for the PCIe-connected ASIC and shelf=(1,0) for the secondary ASIC reachable only via E8/E9 ↔ E0/E1 internal ethernet.
- Galaxy / multi-host: assignments of shelf and rack coordinates done by `tt-topology` configuration tool.

## Submission interface

Each Ethernet tile exposes an `eth_base_firmware_queues_t` structure in its L1, address stored at tile-local `0x170`. Layout:

- 16 × 64-bit `latency_counter`
- `sq` submission queue (host → E)
- one reserved `eth_queue_t` slot
- `cq` completion queue (E → host)
- 4 × 1024 B small-data buffers

Each queue holds 4 entries, with `wr_idx` and `rd_idx` taking values mod 8.

## Why this matters for research

- The "6-D address space" is a software contract — TT-Metal's mesh / multi-mesh APIs sit on top of it. Cross-ASIC traffic crosses Ethernet and pays an order of magnitude more latency than on-chip NoC. Performance modelling and placement strategy for big models (e.g. Llama 70B on 32-ASIC Galaxy) heavily depends on this routing layer.
- The scheme is **not standard IP / Ethernet routing** — it's a custom protocol layered on 100 GbE PHY links. Tools like `tt-topology` configure the coordinates statically.

## Related pages

- [[Wormhole]], [[NoC]], [[TT-Fabric]], [[Programming Model]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part4-ethernet.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-overview.md`
- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
