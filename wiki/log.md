# Log

Append-only chronological log of wiki / outputs changes.

## [2026-05-05] ingest | Initial corpus → seed wiki

- **Raw files processed:** 16 files in `raw/2026-05-05__*.md`.
- **Wiki created from scratch:**
  - `entities/` — [[Tenstorrent]], [[Wormhole]], [[Tensix]] (3 pages)
  - `concepts/` — [[Programming Model]], [[TT-Metal]], [[TT-NN]], [[TT-MLIR]] (stub), [[TT-ISA]], [[Compiler Stack]], [[Reader Compute Writer Kernels]], [[Circular Buffers]], [[Tensix Sync]], [[Macro-Op Expander]], [[Replay Expander]], [[SFPU]], [[Matrix Unit]], [[Fidelity Stages]], [[L1 Memory]], [[NoC]], [[Atomic Counters]], [[Semaphores]], [[Tile-Based Execution]], [[Multi-ASIC Addressing]], [[Harvesting]], [[Dataflow Execution]] (22 pages)
  - `sources/` — 16 source-summary pages, one per `raw/` file
  - `index.md`, `glossary.md`, `open_questions.md`, `log.md` (this file)
- **Outputs:** `outputs/wiki_ingest_report.md`.
- **Key takeaways:**
  - Hardware coverage is solid (corsix series + tt-isa partial + METALIUM_GUIDE).
  - Programming model coverage is solid (METALIUM_GUIDE + Reader/Compute/Writer + Circular Buffers).
  - Compiler stack coverage is shallow — TT-MLIR is a stub.
  - Synchronisation primitives are well-covered at hardware level (Tensix Sync, ThCon atomics, NoC atomics) but the bridge from those to TT-Metal CB metadata is not pinned down.
- **Open questions raised:** 19 items in [[open_questions]]; highest-priority: Q5 (CB hardware substrate), Q7 (handshake-to-atomic-counter folding opportunities), Q9 (TT-MLIR dialect responsibilities).

## [2026-05-05] collect | Pass 1 raw corpus

(For completeness — not a wiki change, but the prior step that produced the inputs to this ingest.)

- See `outputs/source_collection_manifest.md` and `outputs/source_collection_report.md`.
- 16 raw files: 7 corsix posts + 6 GitHub READMEs/docs + 3 paper-metadata stubs.
