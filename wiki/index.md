# Index

> Content map for the Tenstorrent Wormhole research wiki.
> Read [[overview]] first for current priorities and weak spots.

## Top Level

- [[overview]] — current corpus coverage, weakest areas, and immediate ingest priorities
- [[glossary]] — abbreviations and recurring terms
- [[log]] — chronological wiki and output history

## Architecture

- [[architecture/Wormhole|Wormhole]] — ASIC-level structure, boards, and key performance anchors
- [[architecture/Tensix|Tensix]] — compute tile structure and execution resources
- [[architecture/NoC|NoC]] — dual torus interconnect behavior and routing notes
- [[architecture/L1 Memory|L1 Memory]] — per-tile SRAM and placement implications
- [[architecture/Matrix Unit|Matrix Unit]] — matrix engine and multiplier organization
- [[architecture/SFPU|SFPU]] — vector unit and special-function execution

## Toolchain

- [[toolchain/Tenstorrent|Tenstorrent]] — product and software-stack overview
- [[toolchain/Programming Model|Programming Model]] — what the user writes versus what the system maps
- [[toolchain/TT-Metal|TT-Metal]] — low-level SDK and runtime model
- [[toolchain/TT-NN|TT-NN]] — operator-library layer
- [[toolchain/TT-MLIR|TT-MLIR]] — compiler stack entry point, currently shallow
- [[toolchain/TT-ISA|TT-ISA]] — official architecture-documentation layer
- [[toolchain/Compiler Stack|Compiler Stack]] — lowering path and responsibility split

## Concepts

- [[concepts/Circular Buffers|Circular Buffers]] — producer-consumer queues in L1
- [[concepts/Tile-Based Execution|Tile-Based Execution]] — 32x32 tile granularity
- [[concepts/Dataflow Execution|Dataflow Execution]] — spatial/dataflow framing of Wormhole
- [[concepts/Fidelity Stages|Fidelity Stages]] — LoFi/HiFi execution-stage interpretation
- [[concepts/Harvesting|Harvesting]] — row disable behavior and SKU consequences
- [[concepts/Multi-ASIC Addressing|Multi-ASIC Addressing]] — Ethernet and scale-out address structure

## Mechanisms

- [[mechanisms/Reader Compute Writer Kernels|Reader Compute Writer Kernels]] — canonical multi-core kernel split
- [[mechanisms/Tensix Sync|Tensix Sync]] — backend synchronization unit
- [[mechanisms/Semaphores|Semaphores]] — synchronization primitives across layers
- [[mechanisms/Atomic Counters|Atomic Counters]] — ThCon and NoC atomics on L1
- [[mechanisms/Macro-Op Expander|Macro-Op Expander]] — instruction-template expansion
- [[mechanisms/Replay Expander|Replay Expander]] — record and playback instruction sequences

## Questions And Ideas

- [[questions/README|Questions]] — structured open questions by area
- [[research-ideas/README|Research Ideas]] — current candidate research directions

## Sources

- [[Source - corsix Part 1 - Physicalities]]
- [[Source - corsix Part 2 - Disabled Rows]]
- [[Source - corsix Part 3 - NoC Propagation]]
- [[Source - corsix Part 4 - Ethernet]]
- [[Source - corsix Part 5 - T Tiles]]
- [[Source - corsix Part 6 - Vector ISA]]
- [[Source - corsix Part 7 - MatMul]]
- [[Source - tt-metal README]]
- [[Source - METALIUM_GUIDE]]
- [[Source - tt-isa-documentation README]]
- [[Source - tt-isa Wormhole Overview]]
- [[Source - tt-isa Tensix Tile]]
- [[Source - tt-isa NoC]]
- [[Source - Taylor 2026 Numerical Kernels]]
- [[Source - Brown 2025 FFT]]
- [[Source - Cavagna 2025 Grayskull MatMul]]
