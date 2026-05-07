---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, dataflow, cgra]
evidence_level: mixed
---

# Dataflow Execution

## Summary

Wormhole is often framed as a **spatial / dataflow accelerator** rather than a SIMT GPU. Compute is distributed across [[Tensix]] tiles; data placement and movement are **explicit**, mediated by the [[NoC]] and [[L1 Memory]] rather than by an automatic cache/coherence subsystem.

Per [[Source - METALIUM_GUIDE]]:

> "DRAM access requires explicit DMA operations rather than transparent memory management" and "the deliberate absence of cache hierarchies provides deterministic and consistent memory access patterns."

The Taylor et al. paper ([[Source - Taylor 2026 Numerical Kernels]]) explicitly calls these chips "spatial / dataflow architectures, emphasising the concern of data placement and movement."

## Dataflow as a programming idiom on Wormhole

| Element | Maps to |
|---|---|
| Processing element | Tensix tile |
| Local storage / queue | Tile-local L1 + circular buffer |
| Interconnect | NoC #0 / NoC #1 |
| Per-PE behaviour | Reader / Compute / Writer kernels |
| Inter-PE communication | NoC reads/writes/atomics |
| Synchronisation primitives | [[Semaphores]], [[Atomic Counters]], CB metadata |
| Backpressure | Implicit via `cb_reserve_back` on a finite CB |

This mapping is **suggestive**, not exact. Genuine spatial / CGRA architectures usually statically map operators onto PEs; on Wormhole the RISCV cores execute regular code on each tile. The "spatial" framing applies more to **data flow semantics** (explicit producer/consumer, queue-based) than to circuit-level dataflow execution.

## Pipelined execution within a tile

Within one Tensix the intended pipeline is:

```
NoC #0 → Unpacker → Matrix/Vector → Packer → NoC #1
```

with [[Circular Buffers]] absorbing latency at each boundary. The "Unpack/Math/Pack" cores themselves run as a software-pipelined trio, coordinated by per-pipe Tensix Sync semaphores.

## Comparison axes

The vault guidance highlights useful axes for analysing this further:

- Static vs dynamic mapping
- Explicit vs compiler-generated communication
- Tile-level vs operator-level execution
- Data-movement cost visibility
- Synchronisation overhead
- Backpressure & queuing behaviour
- Multi-core placement & routing

These are research-direction prompts. **Not pursued in this ingest** (per task scope).

## Caveats

> Research caution: do not claim Wormhole is a CGRA without explaining the abstraction mismatch. The substrate has many CGRA-like features, but the RISCV cores are general-purpose and dispatched by software, not statically mapped operators.

## Related pages

- [[Tensix]], [[NoC]], [[Circular Buffers]], [[Programming Model]], [[Reader Compute Writer Kernels]], [[Compiler Stack]]

## Sources

- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md`
- `raw/2026-05-05__paper_metadata__taylor-numerical-kernels-wormhole.md`
- `raw/2026-05-05__paper_metadata__brown-fft-wormhole.md`
