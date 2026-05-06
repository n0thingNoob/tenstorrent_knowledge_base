---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, github_readme]
source_path: raw/2026-05-05__github_readme__tt-metal-readme.md
evidence_level: official
---

# Source — tt-metal README

## Why it matters

The landing page of the [[TT-Metal]] / [[TT-NN]] monorepo. Useful as an *index* into the substantial tech-report tree (`tech_reports/`) and the programming-examples tree, both of which are higher-value than the README itself for research purposes.

## Key facts

- **TT-NN** = Python & C++ NN op library; **TT-Metalium** = low-level kernel programming. Both ship in this one repo.
- Featured production models on Wormhole: Llama 3.3 70B (TP=32, Galaxy), Qwen 2.5 7B (n300, TP=2), Qwen 2.5 72B (QuietBox, TP=8), Whisper distil-large-v3, Mixtral 8x7B.
- Releases on a monthly cadence (v0.65 — v0.68 listed Dec 2025 → Apr 2026).
- License: Apache 2.0.
- Blackhole optimization "under active development".
- Tooling: TT-NN Visualizer, TT-Exalens (debug), TT-SMI, Model Explorer, Tracy Profiler, DPRINT (Kernel Print Debug), Watcher, Inspector.

## Technical details

**Architecture / programming model:** none directly — see [[Source - METALIUM_GUIDE]].

**Memory / NoC / synchronisation:** none directly.

**Tech reports referenced (not yet in `raw/`)** — high-priority Pass 2 targets:

- TT-NN: Advanced Performance Optimizations for Models, ViT-TTNN, LLMs, CNNs.
- Benchmarks: GEMM_FLOPS.
- TT-Metalium: Matrix Engine, Data Formats, Reconfiguring Data Formats, Special Values, Allocator, Tensor Layouts, Saturating DRAM Bandwidth, FlashAttention, CNNs, EthernetMultichip, Blackhole Bring-Up, SubDevices.
- Scaleout: Programming Mesh of Devices, Programming Multiple Meshes, TT-Fabric, TT-Distributed.

## Related pages

- [[TT-Metal]], [[TT-NN]], [[Tenstorrent]], [[Wormhole]]

## Open questions

- Most of the technical depth of this repo lives in `tech_reports/*` and `tt_metal/programming_examples/*`. Recommend a Pass-2 capture round targeting at least Matrix Engine, Data Formats, Tensor Layouts, FlashAttention.
