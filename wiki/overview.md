---
type: overview
status: draft
created: 2026-05-06
updated: 2026-05-06
tags: [tenstorrent, wormhole, overview]
evidence_level: mixed
---

# Overview

## Current state

This vault currently has strong early coverage of Wormhole hardware and TT-Metal programming basics, built from the corsix Wormhole series, selected tt-isa pages, the METALIUM guide, and a small paper metadata seed set.

The strongest parts of the corpus today are:

- Wormhole tile inventory, NoC topology, and board-level structure
- Tensix internals at a high level
- reader / compute / writer decomposition
- circular buffers, semaphores, atomic counters, and Tensix Sync primitives
- the top-level TT-Metal programming model

## Where evidence is weak

- TT-MLIR is still a stub-level area
- host/runtime internals and fast-dispatch implementation details are shallow
- some hardware-mechanism pages depend on inference from corsix rather than direct official docs
- several important follow-up docs are referenced but not yet captured into `raw/`

## Highest-priority open questions

- [[questions/README|Questions]] tracks the full set
- Highest priority right now:
  - circular-buffer metadata substrate and hardware implementation
  - handshake-to-atomic-counter replacement opportunities
  - TT-MLIR dialect responsibilities and placement/lowering boundaries

## Strongest research signals

- synchronization overhead is visible enough to support concrete mechanism-level research
- Wormhole exposes unusually explicit data movement and queueing structure compared with mainstream GPU programming models
- the gap between hardware-visible primitives and compiler-visible abstractions looks large enough to be research-relevant
- fidelity-stage and NoC/L1 tradeoffs suggest measurable performance-modeling opportunities

## Immediate ingest priorities

- TT-MLIR docs and repo documentation
- NoC atomics and deeper tt-isa subpages
- TT-Metal examples or TT-LLK code that show concrete synchronization protocols
- tech reports referenced from the official docs but not yet captured into `raw/`

## Related pages

- [[index]]
- [[toolchain/Programming Model|Programming Model]]
- [[toolchain/TT-Metal|TT-Metal]]
- [[architecture/Wormhole|Wormhole]]
- [[mechanisms/Atomic Counters|Atomic Counters]]
- [[questions/README|Questions]]
