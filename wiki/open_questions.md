# Open Questions

Unresolved technical questions surfaced during ingest of the initial 16-source corpus. Each item has: (1) the question, (2) why it matters, (3) what evidence is needed, (4) candidate sources.

## Architecture

### Q1 — Does Tensix "L0" exist? If so, what is it?

- **Why:** corsix Part 5 mentions L0 in several Tensix instruction descriptions but doesn't confirm presence/size/semantics. ThCon load/store (`LOADIND`/`STOREIND`) and atomic ops both reference "L0/L1".
- **Evidence needed:** confirmation in `tt-isa-documentation/WormholeB0/TensixTile/L1.md` or `TensixCoprocessor/ScalarUnit.md`; possibly a measurement experiment.
- **Where to look next:** tt-isa sub-pages not yet captured.

### Q2 — Is "4 Packers" the same as "1 Pack unit"?

- **Why:** [[Source - tt-isa Tensix Tile]] lists **4× Packer**; [[Source - corsix Part 5 - T Tiles]] lists **1× Pack** unit among 8 backend execution resources. Likely the same hardware framed differently (4 Pack pipelines accessed via one Pack instruction stream).
- **Evidence needed:** `tt-isa-documentation/WormholeB0/TensixTile/TensixCoprocessor/Packers/README.md`.

### Q3 — Per-tile cycle-counter skew

- **Why:** corsix Part 3 found a few-cycles-of skew between Tensix cycle counters at chip power-on. He compensated empirically. For cycle-accurate cross-tile traces this matters.
- **Evidence needed:** experiment, or any official statement.

### Q4 — Detailed multiplier scheduling for HiFi3/HiFi4

- **Why:** corsix Part 7 infers but doesn't confirm which mantissa slices are multiplied in which order during HiFi3/4 stages.
- **Evidence needed:** `tech_reports/matrix_engine/matrix_engine.md` (referenced from tt-metal README, not yet captured).

## Synchronisation

### Q5 — How are TT-Metal circular-buffer metadata implemented in hardware?

- **Why:** [[Circular Buffers]] are *the* synchronisation primitive of [[TT-Metal]]. The substrate could be (a) ThCon `ATINCGETPTR` (hardware FIFO atomic), (b) Tensix Sync semaphores, (c) NoC-overlay metadata, or some combination.
- **Evidence needed:** TT-LLK code reading + tt-isa Atomics.md / L1.md.

### Q6 — TT-Metal host-level `Semaphore` API surface

- **Why:** [[Semaphores]] page splits Tensix Sync semaphores from "TT-Metal host semaphores" but the latter is not in `raw/`. Necessary for cross-tile synchronisation in multi-core kernels.
- **Evidence needed:** TT-Metal API docs or programming-examples that use semaphores.

### Q7 — Two-step handshakes that could fold into single atomic increments

- **Why:** Direct user research interest. Need concrete code examples in TT-Metal / TT-LLK where producer-consumer uses a `SEMPOST` + `SEMWAIT` pair that could be replaced with a single `ATINCGET` or NoC atomic increment.
- **Evidence needed:** read TT-Metal kernels (matmul_multi_core, FlashAttention) and TT-LLK helpers.

### Q8 — Detailed NoC-atomic semantics

- **Why:** [[Atomic Counters]] page summarises but the exact opcodes and restrictions live in `tt-isa-documentation/WormholeB0/NoC/Atomics.md` — not in `raw/`.
- **Evidence needed:** capture that page.

## Compiler / runtime

### Q9 — TT-MLIR dialect responsibilities

- **Why:** [[TT-MLIR]] page is a stub. We don't yet know which lowering passes live in TTIR vs TTNN vs TTKernel dialects, or where mapping decisions (op placement, sharding scheme, kernel selection) are made.
- **Evidence needed:** tt-mlir docs site (https://docs.tenstorrent.com/tt-mlir/) and the `docs/` folder in tt-mlir repo.

### Q10 — Is there an auto-tuner / cost model?

- **Why:** the user-facing API choices (interleaved vs sharded buffers, fidelity-stage count, core grid shape) seem to be hand-tuned per op. Whether tt-mlir has an auto-tuning pass is unclear.
- **Evidence needed:** tt-mlir docs.

### Q11 — Fast-dispatch core internals

- **Why:** [[Source - METALIUM_GUIDE]] describes fast dispatch as "a dedicated RV core processing queued operations" but doesn't go into the firmware's structure or its perf characteristics.
- **Evidence needed:** TT-Metal source under `tt_metal/impl/dispatch/`, and possibly the slow-dispatch fallback path for comparison.

## Performance

### Q12 — Why is fp8 throughput 88.9% of expected?

- **Why:** corsix Part 7 inferred Unpack/Pack as the bottleneck at LoFi precision. If correct, this is a measurable, generalisable bottleneck — direct research value.
- **Evidence needed:** GEMM_FLOPS tech report; Tensix Pack throughput modelling.

### Q13 — Sharded vs interleaved memory placement: when does each win?

- **Why:** [[Source - METALIUM_GUIDE]] mentions that sharded mode helps attention/conv "where the computation pattern aligns with data distribution", but quantitative guidance is absent.
- **Evidence needed:** `tech_reports/tensor_layouts/tensor_layouts.md`.

### Q14 — What is the realistic NoC bandwidth utilisation for typical workloads?

- **Why:** Theoretical max = 32 B/cycle/link/direction × N links. Empirical ratio is unknown.
- **Evidence needed:** `Saturating_DRAM_bandwidth.md`, FlashAttention report.

## Multi-chip / scale-out

### Q15 — TT-Fabric routing / failure handling

- **Why:** [[Source - METALIUM_GUIDE]] mentions tt-Fabric for multi-host scale-out but no detail.
- **Evidence needed:** `tech_reports/TT-Fabric/TT-Fabric-Architecture.md`.

### Q16 — How does broadcast performance scale with destination rectangle size?

- **Why:** [[Source - tt-isa NoC]] describes broadcast and `NOC_CMD_PATH_RESERVE` reservation protocol. Reservation latency vs bandwidth tradeoff is implementation-defined.
- **Evidence needed:** experiment + maybe `RoutingPaths.md`.

## Documentation hygiene

### Q17 — `tt-isa-documentation/WormholeB0/README.md` partial capture

- **Why:** WebFetch returned only the lead section. The rest may include harvest-pattern details, address-space layout, etc.
- **Evidence needed:** re-fetch from `raw.githubusercontent.com` or git clone.

### Q18 — corsix Part 6 LUT-mode tables abridged

- **Why:** Four mode-specific tables for `SFPLUTFP32` were truncated during capture. Low priority unless we go deep on SFPU LUT optimisation.
- **Evidence needed:** re-fetch source HTML.

### Q19 — corsix Part 8 ("Reference") not yet captured

- **Why:** Referenced from the Part 7 navigation, posted 2025-09-11. Content unknown.
- **Evidence needed:** WebFetch.
