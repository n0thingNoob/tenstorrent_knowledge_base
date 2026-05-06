# Wiki Ingest Report — Initial Pass

Date: 2026-05-05
Scope: ingest the 16 files in `raw/` and build the initial `wiki/` from scratch.

## 1. Raw files processed (16)

### Blog (7) — corsix.org Wormhole series

- `2026-05-05__blog__corsix-tt-wh-part1-physicalities.md`
- `2026-05-05__blog__corsix-tt-wh-part2-disabled-rows.md`
- `2026-05-05__blog__corsix-tt-wh-part3-noc-propagation.md`
- `2026-05-05__blog__corsix-tt-wh-part4-ethernet.md`
- `2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
- `2026-05-05__blog__corsix-tt-wh-part6-vector-isa.md`
- `2026-05-05__blog__corsix-tt-wh-part7-matmul.md`

### Official docs (6)

- `2026-05-05__github_readme__tt-metal-readme.md`
- `2026-05-05__github_doc__tt-metal-metalium-guide.md`
- `2026-05-05__github_readme__tt-isa-documentation-readme.md`
- `2026-05-05__github_doc__tt-isa-wormhole-overview.md` (partial)
- `2026-05-05__github_doc__tt-isa-wormhole-tensix-tile.md`
- `2026-05-05__github_doc__tt-isa-wormhole-noc.md`

### Paper metadata (3)

- `2026-05-05__paper_metadata__taylor-numerical-kernels-wormhole.md`
- `2026-05-05__paper_metadata__brown-fft-wormhole.md`
- `2026-05-05__paper_metadata__cavagna-grayskull-matmul.md`

## 2. Wiki pages created

**Entities (3):** `Tenstorrent`, `Wormhole`, `Tensix`.

**Concepts (22):**

- Programming-model / toolchain: `Programming Model`, `TT-Metal`, `TT-NN`, `TT-MLIR` (stub), `TT-ISA`, `Compiler Stack`.
- Tensix internals: `Reader Compute Writer Kernels`, `Circular Buffers`, `Tensix Sync`, `Macro-Op Expander`, `Replay Expander`, `SFPU`, `Matrix Unit`, `Fidelity Stages`.
- Memory & interconnect: `L1 Memory`, `NoC`, `Atomic Counters`, `Semaphores`, `Tile-Based Execution`, `Multi-ASIC Addressing`, `Harvesting`.
- Execution model: `Dataflow Execution`.

**Source summaries (16):** one per raw file, following the requested template.

**Top-level wiki:** `index.md`, `glossary.md`, `open_questions.md`, `log.md`.

**Total wiki files created: 45.**

No wiki pages were updated (this is a from-empty initial pass).

## 3. Most useful sources (research signal density)

1. **`corsix Part 5 — T Tiles`** — densest single architectural reference. Every internal-Tensix concept page cites it.
2. **`METALIUM_GUIDE`** — canonical official programming-model doc; foundation of `Programming Model`, `Circular Buffers`, `Reader Compute Writer Kernels`.
3. **`tt-isa NoC`** — authoritative NoC packet/VC/ordering spec; corroborates corsix Part 3's empirical hop-latency.
4. **`corsix Part 7 — MatMul`** — only source with multi-stage matmul semantics + perf cross-check.
5. **`corsix Part 6 — Vector ISA`** — full SFPU instruction reference.
6. **`corsix Part 1 — Physicalities`** — ASIC layout mental model used everywhere downstream.
7. **`Taylor 2026 Numerical Kernels`** (paper, metadata only) — only academic source with explicit "spatial accelerator" framing.

## 4. Weakly covered areas

- **TT-MLIR / compiler internals** — only the README is in `raw/`. The `TT-MLIR` concept page is a stub.
- **TT-NN op semantics** — only model-list / perf-table coverage; no per-op algorithmic detail.
- **Runtime / dispatch internals** — fast-dispatch is described conceptually only.
- **L1 atomics + NoC atomics fine-grained semantics** — the `tt-isa-documentation` sub-pages (`L1.md`, `NoC/Atomics.md`, `NoC/Ordering.md`, `NoC/MemoryMap.md`) are referenced but not in `raw/`. Critical for the user's atomic-counter / handshake research direction.
- **Performance modelling** — `GEMM_FLOPS`, `Saturating_DRAM_bandwidth`, `FlashAttention` tech reports are referenced but not in `raw/`.
- **Multi-chip / TT-Fabric** — described conceptually only.
- **TT-LLK code patterns** — corsix Part 5 references `tt-llk-wh-b0` heavily but the actual LLK code is not in `raw/`.

## 5. Recommended next sources (Pass 2, ≤6 files)

In priority order, consistent with the user's "less is more" preference:

1. `tt-isa-documentation/WormholeB0/TensixTile/L1.md` — L1 + atomics — directly tied to user's atomic-counter / producer-consumer interest.
2. `tt-isa-documentation/WormholeB0/NoC/Atomics.md` — NoC atomic semantics.
3. `tt-metal/tech_reports/matrix_engine/matrix_engine.md` — corroborate/extend [[Matrix Unit]] and [[Fidelity Stages]].
4. `tt-metal/tech_reports/tensor_layouts/tensor_layouts.md` — interleaved vs sharded; needed before any perf-modelling research idea.
5. **arXiv 2603.23343 full HTML body** (Taylor et al.) — promote from metadata to full content; the most relevant academic source.
6. corsix Wormhole Part 8 ("Reference", 2025-09-11) — referenced from Part 7 nav but not yet collected.

A Pass 2 of these 6 files would close the most painful gaps without the bloat of dumping every README in the ecosystem.

## 6. Health flags

- **Partial captures:** `tt-isa Wormhole Overview` (lead section only) and `corsix Part 6` (4 LUT-mode tables abridged). Both flagged in [[open_questions]] and the manifest.
- **Stub pages:** `TT-MLIR` (concept) is intentionally a stub — no deeper raw material yet.
- **Cross-references:** all wiki links use Obsidian wikilinks; `[[Source - <title>]]` form for source pages. Glossary cross-links to concept pages.
- **`raw/` integrity:** untouched. No file in `raw/` was edited or moved during this ingest.
