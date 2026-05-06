---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, paper_metadata, spatial]
source_path: raw/2026-05-05__paper_metadata__taylor-numerical-kernels-wormhole.md
evidence_level: paper
---

# Source — Taylor et al. 2026: Numerical Kernels on a Spatial Accelerator

## Why it matters

The most explicit academic framing of [[Wormhole]] as a **spatial / dataflow architecture** in `raw/`. Directly relevant to the user's CGRA-comparison research interest. Paper presents three numerical kernels + a CG solver and compares against Nvidia GPUs.

## Key facts

- arXiv: **2603.23343** (v1, 24 Mar 2026, CC BY 4.0).
- Authors: **Maya Taylor, Carl Pearson, Luc Berger-Vergiat, Giovanni Long, Jan Ciesko**.
- 12 pages, 13 figures.
- Workload: implements three numerical kernels and composes them into a **conjugate-gradient solver** on Wormhole; benchmarks against Nvidia GPUs.
- Frames the chip as a "spatial computing platform"; emphasises sparse-numerical-algorithm optimisations.

## Technical details

Captured as **metadata + abstract only** — full PDF/HTML body not yet ingested. Summary observations from the abstract:

- "AI accelerators merit consideration for workloads traditionally dominated by CPUs and GPUs."
- Identifies "challenges and opportunities in porting numerical methods to spatial architectures".
- Architecture-specific optimisations for sparse algorithms.

## Related pages

- [[Dataflow Execution]], [[Wormhole]], [[Tensix]], [[Programming Model]]

## Open questions

- Specific perf numbers, kernel-implementation strategies, what they found "challenging" about porting numerical methods, and how their CG solver maps to the [[Reader Compute Writer Kernels]] decomposition — all in the full paper, not in `raw/` yet. **Highest-priority paper to upgrade from metadata to full content** in any future capture pass.
