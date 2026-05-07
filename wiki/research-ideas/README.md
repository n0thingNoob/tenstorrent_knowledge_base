---
type: overview
status: stub
created: 2026-05-06
updated: 2026-05-06
tags: [tenstorrent, wormhole, research-ideas]
evidence_level: mixed
---

# Research Ideas

This section is reserved for ideas that have enough evidence and specificity to deserve their own pages.

## Current likely candidates

- atomic-counter producer-consumer variants that replace two-step semaphore protocols
- compiler-visible modeling of synchronization and data-movement cost
- fidelity-stage selection or modeling beyond fixed format choices
- NoC and L1 contention models tied to Wormhole execution structure

## Promotion rule

Create a dedicated idea page when there is:

- a clear mechanism or bottleneck
- at least one concrete supporting source or experiment signal
- a minimal experiment that could validate or kill the idea
