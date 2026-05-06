---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, paper_metadata, matmul, perf]
source_path: raw/2026-05-05__paper_metadata__cavagna-grayskull-matmul.md
evidence_level: paper
---

# Source — Cavagna et al. 2025: Tenstorrent Grayskull MatMul

## Why it matters

Targets **Grayskull e75** rather than Wormhole, but most architectural concepts (Tensix, FPU, formats) carry over. Provides external **measured perf-per-Watt numbers** and a head-to-head against V100 / A100 / Sapphire Rapids — useful "where does Tenstorrent fit" data.

## Key facts

- arXiv: **2505.06085** (v1 9 May 2025, v3 20 Jun 2025).
- Authors: **Hiari Pizzini Cavagna, Daniele Cesarini, Andrea Bartolini**.
- Workshop: Computational Aspects of Deep Learning, ISC HPC 2025.
- Workload: characterisation of Grayskull e75 BLAS kernels at reduced precision (BF16 etc.).
- Result: peak **1.55 TFLOPs/Watt** at BF16; raw perf below A100/V100 but power efficiency competitive.

## Technical details

**Captured as metadata + abstract only.** Paper characterises gridsize, matrix dimensions, data formats, numerical precision impact on efficiency.

**Architecture caveat:** Grayskull's SFPU is 64-lane / 19-bit-FP, vs Wormhole's 32-lane / 32-bit-FP — perf numbers won't transfer verbatim, but the **methodology** (gridsize sweep, precision sweep) is reusable.

## Related pages

- [[Tensix]], [[Matrix Unit]], [[Fidelity Stages]], [[Tenstorrent]], [[TT-Metal]]

## Open questions

- Wormhole-specific equivalent of this characterisation: **GEMM_FLOPS tech report** in `tt-metal/tech_reports/` (referenced in [[Source - tt-metal README]], not yet captured).
