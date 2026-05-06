# Source Collection Manifest

Last updated: 2026-05-05

## Collected

| # | Title | source_type | Raw filename | Original URL | Status |
|---|---|---|---|---|---|
| 1  | Tenstorrent Wormhole Series Part 1: Physicalities | blog | `raw/2026-05-05__blog__corsix-tt-wh-part1-physicalities.md` | https://www.corsix.org/content/tt-wh-part1 | captured |
| 2  | Tenstorrent Wormhole Series Part 2: Which disabled rows? | blog | `raw/2026-05-05__blog__corsix-tt-wh-part2-disabled-rows.md` | https://www.corsix.org/content/tt-wh-part2 | captured |
| 3  | Tenstorrent Wormhole Series Part 3: NoC propagation delay | blog | `raw/2026-05-05__blog__corsix-tt-wh-part3-noc-propagation.md` | https://www.corsix.org/content/tt-wh-part3 | captured |
| 4  | Tenstorrent Wormhole Series Part 4: A touch of Ethernet | blog | `raw/2026-05-05__blog__corsix-tt-wh-part4-ethernet.md` | https://www.corsix.org/content/tt-wh-part4 | captured |
| 5  | Tenstorrent Wormhole Series Part 5: Taking apart T tiles | blog | `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md` | https://www.corsix.org/content/tt-wh-part5 | captured |
| 6  | Tenstorrent Wormhole Series Part 6: Vector instruction set | blog | `raw/2026-05-05__blog__corsix-tt-wh-part6-vector-isa.md` | https://www.corsix.org/content/tt-wh-part6 | partial (LUT mode tables abridged) |
| 7  | Tenstorrent Wormhole Series Part 7: Bits of the MatMul | blog | `raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md` | https://www.corsix.org/content/tt-wh-part7 | captured |
| 8  | tt-metal README | github_readme | `raw/2026-05-05__github_readme__tt-metal-readme.md` | https://github.com/tenstorrent/tt-metal/blob/main/README.md | captured |
| 9  | TT Architecture and Metalium Guide | github_doc | `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md` | https://github.com/tenstorrent/tt-metal/blob/main/METALIUM_GUIDE.md | captured |
| 10 | tt-isa-documentation README | github_readme | `raw/2026-05-05__github_readme__tt-isa-documentation-readme.md` | https://github.com/tenstorrent/tt-isa-documentation/blob/main/README.md | captured |
| 11 | tt-isa Wormhole B0 overview | github_doc | `raw/2026-05-05__github_doc__tt-isa-wormhole-overview.md` | https://github.com/tenstorrent/tt-isa-documentation/blob/main/WormholeB0/README.md | partial |
| 12 | tt-isa Wormhole Tensix Tile | github_doc | `raw/2026-05-05__github_doc__tt-isa-wormhole-tensix-tile.md` | https://github.com/tenstorrent/tt-isa-documentation/blob/main/WormholeB0/TensixTile/README.md | captured |
| 13 | tt-isa Wormhole NoC | github_doc | `raw/2026-05-05__github_doc__tt-isa-wormhole-noc.md` | https://github.com/tenstorrent/tt-isa-documentation/blob/main/WormholeB0/NoC/README.md | captured |
| 14 | Numerical Kernels on a Spatial Accelerator: A Study of Tenstorrent Wormhole (Taylor et al., 2026) | paper_metadata | `raw/2026-05-05__paper_metadata__taylor-numerical-kernels-wormhole.md` | https://arxiv.org/abs/2603.23343 | metadata_only |
| 15 | Exploring Fast Fourier Transforms on the Tenstorrent Wormhole (Brown et al., 2025) | paper_metadata | `raw/2026-05-05__paper_metadata__brown-fft-wormhole.md` | https://arxiv.org/abs/2506.15437 | metadata_only |
| 16 | Assessing Tenstorrent's RISC-V MatMul Acceleration Capabilities (Cavagna et al., 2025) | paper_metadata | `raw/2026-05-05__paper_metadata__cavagna-grayskull-matmul.md` | https://arxiv.org/abs/2505.06085 | metadata_only |

Total: 16 files (13 captured/partial content + 3 paper metadata).

## Failed / partial

| Source | URL | Reason | Action |
|---|---|---|---|
| Original seed `tt-wh` URL | https://www.corsix.org/content/tt-wh | 404 — no such page; the series lives at `tt-wh-partN` | Use the part-N URLs (collected above) |
| Corsix Part 6 LUT-mode tables | https://www.corsix.org/content/tt-wh-part6 | WebFetch model trimmed the four large `SFPLUTFP32` lookup tables to a placeholder note | Re-fetch raw HTML if the LUT tables become research-relevant |
| tt-isa Wormhole B0 overview | https://github.com/tenstorrent/tt-isa-documentation/blob/main/WormholeB0/README.md | WebFetch returned the lead section only; deeper content of the page may exist | Re-fetch raw via raw.githubusercontent.com or git clone |
| Three arXiv papers | (URLs above) | Captured as metadata + abstract only; full PDF/HTML body not stored | Fetch HTML versions when ingesting into wiki |

## Candidate sources not yet collected

Listed in priority order. Each line is a deliberate next-pass capture target.

### Tenstorrent tech reports (from `tt-metal` repo)
- `tech_reports/matrix_engine/matrix_engine.md` — definitive matrix-engine reference
- `tech_reports/data_formats/data_formats.md` and `reconfig_data_format.md` — bfp/fp formats, runtime reconfiguration
- `tech_reports/Handling_Special_Value/special_values.md` — NaN/Inf/denormal behavior
- `tech_reports/memory/allocator.md` — L1/DRAM allocator
- `tech_reports/tensor_layouts/tensor_layouts.md` — interleaved vs sharded, tile layout
- `tech_reports/Saturating_DRAM_bandwidth/Saturating_DRAM_bandwidth.md` — DRAM-BW perf model
- `tech_reports/FlashAttention/FlashAttention.md` — Wormhole-specific attention impl
- `tech_reports/CNNs/ttcnn.md`, `tech_reports/CNNs/cnn_optimizations.md`
- `tech_reports/EthernetMultichip/BasicEthernetGuide.md`
- `tech_reports/Blackhole/BlackholeBringUpProgrammingGuide.md`
- `tech_reports/SubDevices/SubDevices.md`
- `tech_reports/Programming_Mesh_of_Devices/...`, `Programming_Multiple_Meshes/...`
- `tech_reports/TT-Fabric/TT-Fabric-Architecture.md`
- `tech_reports/TT-Distributed/TT-Distributed-Architecture-1219.md`
- `tech_reports/AdvancedPerformanceOptimizationsForModels/...`
- `tech_reports/LLMs/llms.md`, `tech_reports/ViT-TTNN/vit.md`
- `tech_reports/GEMM_FLOPS/GEMM_FLOPS.md`

### tt-isa-documentation deeper subtree
- `WormholeB0/TensixTile/L1.md` — L1 SRAM details, atomics
- `WormholeB0/TensixTile/BabyRISCV/README.md` — Baby RV core memory map
- `WormholeB0/TensixTile/TensixCoprocessor/README.md` and per-unit pages (MatrixUnit, VectorUnit, ScalarUnit, Unpackers, Packers)
- `WormholeB0/NoC/Atomics.md`, `Ordering.md`, `MemoryMap.md`, `Counters.md`, `RoutingPaths.md`, `Overlay/`
- `WormholeB0/EthernetTile/`, `DRAMTile/`, `PCIExpressTile/`, `ARCTile/`

### TT-MLIR / TT-Forge / tooling
- tt-mlir architecture book (https://docs.tenstorrent.com/tt-mlir/) — TTIR, TTNN, TTKernel dialects
- tt-mlir lowering pipeline doc
- tt-forge-fe README + arch
- tt-llk repo — LLK overview and kernel patterns
- sfpi compiler README and SFPU intrinsics ref (https://github.com/tenstorrent/sfpi)

### Programming examples (tt-metal)
- `tt_metal/programming_examples/matmul/matmul_multi_core/matmul_multi_core.md`
- `programming_examples/eltwise_sfpu/eltwise_sfpu.md`
- `programming_examples/eltwise_binary/eltwise_binary.md`
- `programming_examples/loopback/dram_loopback.md`

### Academic papers (full content)
- arXiv:2603.23343 — fetch HTML body
- arXiv:2506.15437 — fetch HTML body
- arXiv:2505.06085 — fetch HTML body
- arXiv:2509.19294 — N-body on Wormhole (Brown group)

### Talks / slides
- `riscv.epcc.ed.ac.uk/assets/files/hpcasia25/Tenstorrent.pdf` — Introduction to Tenstorrent (HPC Asia '25)
- SemiAnalysis: Tenstorrent Wormhole Analysis (long industry analysis post)
- Tenstorrent newsroom Wormhole community-highlight posts

### Linked corsix code gists
- gist `cdc676f08bb26ddb858d45bd8a2062fc` — part 2 100-line code
- gist `07760dc4a0a62d7a51aed77e0058861c` — part 3 164-line code
- gist `604455f58d851b006cda2daa0ea9d095` — part 4 201-line code
- corsix wormhole-vector emulator https://github.com/corsix/wormhole-vector

### Newer corsix posts
- Tenstorrent Wormhole Series Part 8: Reference (2025-09-11) — exists per Part 7 navigation; not yet collected.
