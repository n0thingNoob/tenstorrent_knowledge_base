# Source Collection Report — initial pass

Date: 2026-05-05
Scope: build the seed `raw/` corpus for the Tenstorrent Wormhole research wiki. No `wiki/` updates and no research-idea generation in this pass.

## 1. What was collected

16 raw files. Inventory by source_type:

| source_type | Count | Files |
|---|---|---|
| `blog` | 7 | corsix.org Wormhole series, parts 1–7 |
| `github_readme` | 2 | tt-metal, tt-isa-documentation |
| `github_doc` | 4 | tt-metal METALIUM_GUIDE, tt-isa Wormhole-overview / TensixTile / NoC |
| `paper_metadata` | 3 | Taylor 2026, Brown 2025, Cavagna 2025 |

Coverage achieved:

- **Hardware physical layout, NoC, ethernet, harvesting, addressing** — covered in depth (corsix Part 1–4, tt-isa NoC).
- **Tensix tile internals (RISC-V cores, Tensix coprocessor, FPU/SFPU, configuration registers)** — covered (corsix Part 5/6, tt-isa Tensix Tile).
- **Matrix engine fidelity stages and FP details** — covered (corsix Part 7).
- **TT-Metalium programming model (reader/compute/writer kernels, circular buffers, MeshDevice/MeshWorkload, fast dispatch, SPMD)** — covered with verbatim code examples (METALIUM_GUIDE).
- **Academic positioning / spatial-accelerator framing** — three paper abstracts captured.

## 2. Most important sources

Ranked by research value for the user's CGRA / spatial-accelerator angle:

1. **`corsix-tt-wh-part5-t-tiles.md`** — most architecturally dense single source. Tensix instruction pipe, Macro-Op/Replay expanders, Tensix Sync, mutexes, semaphores, ThCon GPRs, atomics (`ATCAS`, `ATINCGET`, `ATINCGETPTR`), configuration registers. Maps directly to the user's interest in synchronization mechanisms and atomic counters.
2. **`tt-metal-metalium-guide.md`** — canonical programming-model reference. Reader/compute/writer kernel pattern, circular-buffer producer-consumer protocol, fast dispatch, SPMD vs MPMD, hardware-generation abstraction via Compute API. Pair with corsix Part 5 for the hardware/software co-design picture.
3. **`tt-isa-wormhole-noc.md`** — authoritative on packet format, virtual channels, broadcast semantics, deadlock guarantees, ordering, performance numbers (9-cycle hop, 256-bit/flit). Independently confirms corsix Part 3's 9-cycle measurement.
4. **`corsix-tt-wh-part1-physicalities.md`** — sets up the 10×12 grid mental model used everywhere else.
5. **`corsix-tt-wh-part6-vector-isa.md`** — full SFPU instruction-set reference. Critical for any vector-unit / non-linear-op research.
6. **`corsix-tt-wh-part7-matmul.md`** — fidelity stages (LoFi/HiFi2/3/4), 7×5 multiplier, TFLOP/s cross-check. Critical for performance-modeling research.
7. **`taylor-numerical-kernels-wormhole.md`** (paper) — only academic source that explicitly frames Wormhole as a "spatial computing platform". Most directly relevant to the user's CGRA angle.

## 3. Under-covered areas

The corpus is intentionally small in this initial pass. Major gaps:

- **Compiler stack** — almost nothing on TT-MLIR dialects (TTIR, TTNN, TTKernel), lowering passes, or tile-level IR. The TT-Forge frontend is also untouched.
- **Runtime / dispatch internals** — METALIUM_GUIDE describes fast dispatch at a conceptual level only. No detail on the dispatch-core firmware, kernel binary layout, or the host-device command stream.
- **Tensix Coprocessor sub-units beyond Vector** — Unpacker, Packer, Matrix engine internals are described one level deep at most. The tt-isa subtree pages on these are not yet collected.
- **L1 SRAM details and atomics** — the tt-isa `TensixTile/L1.md` page (atomic semantics on L1) is referenced but not captured. This is directly relevant to the user's atomic-counter producer/consumer interest.
- **Multichip / scaleout / TT-Fabric** — no source captured. Only mentioned in METALIUM_GUIDE.
- **Performance-modeling reports** — GEMM_FLOPS, Saturating_DRAM_bandwidth, FlashAttention tech reports are referenced but not captured.
- **Data formats and special values** — bfp/fp variants, denormal handling — referenced but not captured.
- **Programming examples with concrete kernel code beyond the vector-add example** — matmul multi-core, eltwise variants, sharding/padding examples not captured.
- **Simulation / emulation infrastructure** — corsix's wormhole-vector emulator referenced in Part 6; no Tenstorrent-official simulator captured.
- **Mesh / multi-device programming** — Programming_Mesh_of_Devices and Programming_Multiple_Meshes reports not captured.

## 4. Next sources to collect (concrete URLs)

If the user wants a second pass, capture in this order — small files first to maximise breadth-of-coverage per file:

1. `tt_metal/tech_reports/matrix_engine/matrix_engine.md` — corroborate corsix Part 7
2. `tt_metal/tech_reports/data_formats/data_formats.md`
3. `tt_metal/tech_reports/Handling_Special_Value/special_values.md`
4. `tt_metal/tech_reports/tensor_layouts/tensor_layouts.md`
5. `tt-isa-documentation/WormholeB0/TensixTile/L1.md` (L1 + atomics)
6. `tt-isa-documentation/WormholeB0/NoC/Atomics.md` and `Ordering.md`
7. `tt_metal/tech_reports/Saturating_DRAM_bandwidth/Saturating_DRAM_bandwidth.md`
8. `tt_metal/tech_reports/FlashAttention/FlashAttention.md`
9. `tt_metal/tech_reports/TT-Fabric/TT-Fabric-Architecture.md`
10. tt-mlir docs site landing — TTIR, TTNN, TTKernel dialect descriptions
11. arXiv 2603.23343 full HTML body (Taylor et al. — spatial-accelerator framing)
12. arXiv 2506.15437 full HTML body (Brown et al. — FFT)
13. corsix Wormhole Part 8 ("Reference", 2025-09-11)
14. SemiAnalysis "Tenstorrent Wormhole Analysis" long-form post

## 5. Suggested future wiki pages (names only)

Page titles that the current corpus is sufficient to seed. Page creation is **out of scope** for this task — this is a forward-looking suggestion.

### `wiki/architecture/`
- `Wormhole ASIC Overview.md` — 10×12 tile grid, tile types, harvesting (sources: corsix Part 1/2, tt-isa Wormhole overview)
- `Tensix Core.md` — five Baby RISC-V cores, Tensix coprocessor block diagram (sources: corsix Part 5, METALIUM_GUIDE, tt-isa Tensix Tile)
- `NoC.md` — 2D torus, two NoCs, packet/flit format, virtual channels, propagation delay (sources: corsix Part 1/3/4, tt-isa NoC)
- `L1 SRAM.md` — 1.5 MB / 1464 KiB capacity, addressable not cache (sources: corsix Part 5, tt-isa Tensix Tile, METALIUM_GUIDE)
- `Matrix Unit (FPU).md` — 7×5 multiplier, fidelity stages (sources: corsix Part 7)
- `Vector Unit (SFPU).md` — SFPU instruction set, 32 lanes × 32b (source: corsix Part 6)
- `Ethernet and Multi-ASIC.md` — E-tile, n300s ASIC-to-ASIC, 6D addressing (sources: corsix Part 4)
- `Harvesting.md` — disabled rows, fused-off tiles (sources: corsix Part 2)

### `wiki/toolchain/`
- `TT-Metal.md` — host API, MeshDevice, kernels, dispatch (source: METALIUM_GUIDE, tt-metal README)
- `TT-NN.md` — op library, layer of TT-Metal (source: tt-metal README)
- `TT-MLIR.md` — compiler dialects, lowering (source: tt-mlir README — needs deeper capture pass)
- `TT-LLK.md` — low-level kernels, init/runtime split (sources: corsix Part 5, tt-isa README)
- `Compute API and Hardware Abstraction.md` — generation-portability (source: METALIUM_GUIDE)

### `wiki/concepts/`
- `Reader Compute Writer Kernels.md`
- `Circular Buffer.md` — producer/consumer queue semantics, hardware metadata
- `Tile Based Execution.md` — 32×32 tile, 16×16 face
- `Producer Consumer Synchronization.md` — semaphores, atomics, circular buffers (sources: corsix Part 5, tt-isa NoC)
- `Atomic Counter Synchronization.md` — `ATINCGET`, NoC atomics — directly tied to the user's research interest
- `SPMD vs MPMD on Tensix.md`
- `Fast Dispatch.md`
- `Sharded vs Interleaved Buffers.md`

### `wiki/mechanisms/`
- `Macro-Op Expander.md` — Tensix instruction expansion, MOP_CFG/MOP templates (source: corsix Part 5)
- `Replay Expander.md` — record/tee/playback (source: corsix Part 5)
- `Tensix Sync mutexes and semaphores.md` (source: corsix Part 5)
- `NoC Multicast and Broadcast.md` (sources: corsix Part 3, tt-isa NoC)
- `NoC Virtual Channels.md` (source: tt-isa NoC)
- `6D Network Addressing.md` (source: corsix Part 4)
- `Soft Reset and Cycle Counter.md` (source: corsix Part 3)
- `TLB-based PCIe Window.md` (source: corsix Part 2)

### `wiki/sources/`
- One source page per file in `raw/` (16 stubs).

### `wiki/comparisons/`
- `Wormhole vs CUDA Programming Model.md` (source: METALIUM_GUIDE "for GPU experts" section)
- `Wormhole vs Cell Processor.md` (source: METALIUM_GUIDE "for CPU experts" section)
- `Wormhole as a CGRA — what fits and what doesn't.md` (source: Taylor 2026 paper framing)

### `wiki/questions/`
- `What is L0 inside Tensix?` — corsix Part 5 explicitly flags this as unclear
- `Exact 7×5 multiplier sequencing for HiFi3/HiFi4` — corsix Part 7 left this as inference
- `Ordering semantics of NoC writes when using NOC_CMD_VC_LINKED` — tt-isa NoC partial coverage
- `What does Wormhole's dispatch firmware actually do?` — only described conceptually so far
