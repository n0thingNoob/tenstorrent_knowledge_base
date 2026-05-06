# Wiki Index

> AI-maintained map of the Tenstorrent Wormhole research wiki. Read this first.
> Last updated: 2026-05-05 (initial ingest of 16 raw sources)

## Entities

- [[Tenstorrent]] — the company; product family + open-source software stack
- [[Wormhole]] — the current ASIC; tile inventory, board variants, perf numbers
- [[Tensix]] — the compute tile; 5 RV cores + Tensix coprocessor

## Concepts — programming model & toolchain

- [[Programming Model]] — what the user actually writes; explicit vs implicit
- [[TT-Metal]] — low-level SDK; mesh-first, OpenCL-like
- [[TT-NN]] — Python/C++ NN op library
- [[TT-MLIR]] — MLIR-based compiler (stub — repo README only)
- [[TT-ISA]] — official low-level architecture documentation set
- [[Compiler Stack]] — full lowering path, compile-time vs runtime split

## Concepts — Tensix internals

- [[Reader Compute Writer Kernels]] — canonical 3-kernel decomposition per tile
- [[Circular Buffers]] — producer/consumer FIFOs in L1
- [[Tensix Sync]] — on-tile mutexes / semaphores / STALLWAIT condition matrix
- [[Macro-Op Expander]] — `MOP` template-based instruction expansion
- [[Replay Expander]] — record / tee / playback Tensix-instruction buffer
- [[SFPU]] — Tensix Vector unit (32-lane × 32-bit SIMD)
- [[Matrix Unit]] — Tensix MAC engine (2048× 7b×5b multipliers)
- [[Fidelity Stages]] — LoFi/HiFi2/3/4 multi-stage matmul scheme

## Concepts — memory & interconnect

- [[L1 Memory]] — per-tile SRAM (1464 KiB), addressable not cache
- [[NoC]] — 2D-torus on-chip network (×2)
- [[Atomic Counters]] — ThCon + NoC atomics on L1
- [[Semaphores]] — Tensix Sync semaphores vs TT-Metal host-level semaphores
- [[Tile-Based Execution]] — 32×32 tile + 16×16 face native granularity
- [[Multi-ASIC Addressing]] — 6-D global address space; ethernet routing
- [[Harvesting]] — yield-driven row disabling; n150s vs n300s

## Concepts — execution model

- [[Dataflow Execution]] — spatial/dataflow framing of Wormhole

## Sources

### Blog (corsix.org Wormhole series)

- [[Source - corsix Part 1 - Physicalities]]
- [[Source - corsix Part 2 - Disabled Rows]]
- [[Source - corsix Part 3 - NoC Propagation]]
- [[Source - corsix Part 4 - Ethernet]]
- [[Source - corsix Part 5 - T Tiles]] — densest single architectural ref
- [[Source - corsix Part 6 - Vector ISA]]
- [[Source - corsix Part 7 - MatMul]]

### Official docs

- [[Source - tt-metal README]]
- [[Source - METALIUM_GUIDE]] — canonical programming-model ref
- [[Source - tt-isa-documentation README]]
- [[Source - tt-isa Wormhole Overview]]
- [[Source - tt-isa Tensix Tile]]
- [[Source - tt-isa NoC]] — confirms 9-cycle hop latency

### Papers (metadata + abstract only)

- [[Source - Taylor 2026 Numerical Kernels]] — spatial-accelerator framing
- [[Source - Brown 2025 FFT]] — Wormhole n300 vs Xeon, perf/energy
- [[Source - Cavagna 2025 Grayskull MatMul]] — methodology reusable

## Other top-level files

- [[glossary]] — abbreviations, terms (CB, FPU, SFPU, ThCon, NIU, etc.)
- [[open_questions]] — unresolved technical questions
- [[log]] — chronological ingest / change log
