---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, blog, ethernet]
source_path: raw/2026-05-05__blog__corsix-tt-wh-part4-ethernet.md
evidence_level: blog
---

# Source — corsix Part 4: A Touch of Ethernet

## Why it matters

The only source in `raw/` that documents the **Ethernet-tile base-firmware interface** at struct/code level. Establishes the **6-D global addressing scheme** (NoC-XY, shelf-XY, rack#, shelf#) and the submission/completion-queue contract that every higher-level mesh API sits on top of.

## Key facts

- 1st ASIC E0–E1 connect to one QSFP-DD; E6–E7 to the other; E8–E9 ↔ E0/E1 of 2nd ASIC; E14–E15 to a Warp 100 Bridge.
- 2nd ASIC has **no PCIe** — host can only reach it via 1st ASIC + ethernet.
- `routing_cmd_t` (32 B) is the request/response unit. Carries: target-addr, target-noc-XY, target-shelf-XY, inline_data / data_block_length, flags, target-rack-XY, dma_addr.
- Flags: `CMD_WR_REQ`, `CMD_RD_REQ`, `CMD_WR_ACK`, `CMD_RD_DATA`, `CMD_DATA_BLOCK`, `CMD_DATA_BLOCK_DMA`, `CMD_BROADCAST`, `CMD_USE_NOC1`, `CMD_TIMESTAMP`, `CMD_ORDERED`, `CMD_DEST_UNREACHABLE`.
- **6-D address space**: NoC-X, NoC-Y, shelf-X, shelf-Y, rack#, shelf#.
- E-tile firmware has 4-entry SQ + 4-entry CQ in `eth_base_firmware_queues_t` at L1 address pointed to by `*((u32*)L1[0x170])`.
- Routing decision per E-tile: (1) self → local load/store, (2) same ASIC → NoC, (3) else → forward via ethernet.
- For a single n300s board: rack#=0, shelf#=0, shelf=(0,0) and (1,0).

## Technical details

**Architecture:** every E-tile is both an endpoint and a router for the 6-D mesh.

**Memory / Synchronisation:** SQ/CQ is a producer-consumer ring with single-writer fields per index (`wr_idx`, `rd_idx`). 4-slot small-data buffers (`buffers[4][1024]`) shared between SQ and CQ entries by index alignment.

**Performance:** not measured here, but each link is 100 GbE bidirectional.

## Related pages

- [[NoC]], [[Multi-ASIC Addressing]], [[Wormhole]], [[Programming Model]]

## Open questions

- E-tile *base firmware* source isn't open; the routing logic, congestion handling, and broadcast forwarding are inferred from headers. Confirming behaviour empirically would be a small but meaningful experiment.
