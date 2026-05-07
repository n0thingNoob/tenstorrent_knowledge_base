---
type: question
status: needs-source
created: 2026-05-06
updated: 2026-05-06
tags: [tenstorrent, wormhole, synchronization, questions]
evidence_level: unknown
---

# Synchronization Questions

## Q5. How are TT-Metal circular-buffer metadata implemented in hardware?

- Why it matters: circular buffers are central to TT-Metal synchronization, and the substrate determines what optimizations are realistic.
- Evidence needed: TT-LLK code, deeper tt-isa atomics/L1 docs, or direct experiment.
- Related pages: [[concepts/Circular Buffers|Circular Buffers]], [[mechanisms/Tensix Sync|Tensix Sync]], [[mechanisms/Atomic Counters|Atomic Counters]]

## Q6. What exactly is the TT-Metal host-level semaphore API surface?

- Why it matters: multi-core synchronization is incomplete in the current corpus without it.
- Evidence needed: TT-Metal API docs or examples using semaphores.
- Related pages: [[mechanisms/Semaphores|Semaphores]], [[toolchain/TT-Metal|TT-Metal]]

## Q7. Which two-step handshakes could fold into a single atomic increment?

- Why it matters: this is one of the most promising mechanism-specific research directions in the current vault.
- Evidence needed: concrete TT-Metal or TT-LLK kernels showing producer-consumer protocols.
- Related pages: [[mechanisms/Atomic Counters|Atomic Counters]], [[mechanisms/Semaphores|Semaphores]], [[concepts/Circular Buffers|Circular Buffers]]

## Q8. What are the precise NoC atomic semantics and restrictions?

- Why it matters: current summaries are enough for orientation but not enough for exact mechanism claims.
- Evidence needed: tt-isa NoC atomics documentation.
- Related pages: [[mechanisms/Atomic Counters|Atomic Counters]], [[architecture/NoC|NoC]]
