---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, paper_metadata, fft, hpc]
source_path: raw/2026-05-05__paper_metadata__brown-fft-wormhole.md
evidence_level: paper
---

# Source — Brown et al. 2025: Exploring FFTs on the Tenstorrent Wormhole

## Why it matters

Concrete data point on **Wormhole as RISC-V HPC accelerator**: explicit perf and energy numbers vs a 24-core Xeon Platinum. Frames [[TT-Metal]] as "decoupling data movement from compute" — useful confirmatory framing of the [[Reader Compute Writer Kernels|reader/compute/writer]] split.

## Key facts

- arXiv: **2506.15437** (v1, 18 Jun 2025).
- Authors: **Nick Brown, Jake Davies, Felix LeClair** (EPCC, University of Edinburgh).
- Workshop: "RISC-V for HPC" at ISC 2025.
- Workload: Cooley-Tukey FFT ported to Wormhole n300.
- Headline result: 2D FFT on n300 is **slower than a 24-core Xeon Platinum** but uses **~8× less power and ~2.8× less energy**.

## Technical details

**Captured as metadata + abstract only.** Likely contains kernel-implementation details for FFT on TT-Metal (twiddle data movement, butterfly compute, DRAM↔L1 staging) — useful comparison for any future custom-kernel work.

## Related pages

- [[TT-Metal]], [[Programming Model]], [[Wormhole]], [[Dataflow Execution]]

## Open questions

- Specific kernel layout, sharding strategy, and bottleneck identification — in the full paper, not in `raw/` yet.
- Same lead author has slides at `riscv.epcc.ed.ac.uk/assets/files/hpcasia25/Tenstorrent.pdf` — separate capture target.
