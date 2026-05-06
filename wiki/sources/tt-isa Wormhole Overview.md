---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, github_doc]
source_path: raw/2026-05-05__github_doc__tt-isa-wormhole-overview.md
evidence_level: official
---

# Source — tt-isa Wormhole B0 Overview

## Why it matters

Tenstorrent's own one-line-per-component ASIC inventory. **Authoritative tile counts** corroborating corsix Part 1.

## Key facts

- 80× Tensix tiles (some fused-off via [[Harvesting]]).
- 18× DRAM tiles (12 GiB GDDR6 total; each 2 GiB exposed identically on 3 tiles).
- 16× Ethernet tiles (each 100 GbE bidirectional).
- 1× PCIe tile (PCIe 4.0 x16).
- 1× ARC tile (board management; "customers can mostly ignore").
- 2× NoCs forming a 2D torus.

## Technical details

**Architecture:** the page is essentially a catalogue / index of subdirectories. The actual specs are in sub-pages.

## Related pages

- [[Wormhole]], [[Tensix]], [[NoC]], [[L1 Memory]], [[Multi-ASIC Addressing]], [[Harvesting]]

## Open questions

- Capture was partial — the WebFetch returned only the lead section. The rest of this page (likely covering tile-coord translation, harvesting masks, and address-space layout) remains uncaptured. Re-fetch via `raw.githubusercontent.com` or `git clone` for full content.
