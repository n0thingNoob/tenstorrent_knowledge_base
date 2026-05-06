---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, blog]
source_path: raw/2026-05-05__blog__corsix-tt-wh-part2-disabled-rows.md
evidence_level: blog
---

# Source — corsix Part 2: Which Disabled Rows?

## Why it matters

Practical low-level walkthrough of how to talk to a Wormhole ASIC **without** the user-mode driver. Establishes the PCIe BAR layout, TLB-style window scheme, and how to query harvested-row masks. Useful both as background and as a recipe for instrumented experiments.

## Key facts

- Open `/dev/tenstorrent/0`, query mappings via `TENSTORRENT_IOCTL_QUERY_MAPPINGS (0xFA02)`.
- Recommended layout: 464 MB BAR0 as write-combining, 32 MB BAR0 as UC, 16 MB BAR2 as UC. Total 512 MB.
- BAR0 maps to PCIe-tile NoC reads/writes; BAR2 holds ARC/PCIe config registers.
- The 496 MB region is sliced into **156 × 1 MB + 10 × 2 MB + 20 × 16 MB = 186 "TLB" pieces**. Each piece is independently configured to target an (X, Y) tile (or rectangle for multicast), an aligned address window, and NoC#0 vs NoC#1.
- TLB config registers start at `0x1FC00000`, 8 B per piece.
- Tile-local registers `0xFFB20108` (`MC_DISABLE_ROW`) and `0xFFB20110` (`MC_DISABLE_COL`) reveal the harvest pattern.
- corsix's chip: row mask `0b100001` = rows 0 and 5 disabled; col mask `0b110001000001` = cols 0, 6, 11 used as multicast-disable for D / E columns.

## Technical details

**Architecture:** PCIe-tile bridges host MMIO to NoC reads/writes; the TLB system is the configuration that controls which NoC (X, Y) any given chunk of host VA maps to.

**Memory:** WC vs UC distinction at host side only — the PCIe tile sees both as PCIe transactions.

**Synchronisation:** not covered.

## Related pages

- [[Wormhole]], [[Harvesting]], [[NoC]]

## Open questions

- The TLB scheme is the key low-level entry point for any custom firmware / experiment. If/when we want to write benchmarking code (later), this is the page to cite.
