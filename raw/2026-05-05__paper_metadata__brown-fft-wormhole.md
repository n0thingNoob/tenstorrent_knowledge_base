---
title: "Exploring Fast Fourier Transforms on the Tenstorrent Wormhole"
source_type: "paper_metadata"
original_url: "https://arxiv.org/abs/2506.15437"
repository: "unknown"
commit_or_version: "arXiv v1, 2025-06-18"
fetched_at: "2026-05-05"
status: "metadata_only"
license: "unknown"
tags:
  - tenstorrent
  - wormhole
---

# Exploring Fast Fourier Transforms on the Tenstorrent Wormhole

Source URL: https://arxiv.org/abs/2506.15437
Captured at: 2026-05-05
Status: metadata_only

## Source Content

# Exploring Fast Fourier Transforms on the Tenstorrent Wormhole

## Authors

- Nick Brown
- Jake Davies
- Felix LeClair

## Abstract

> Whilst numerous areas of computing have adopted the RISC-V Instruction Set Architecture (ISA) wholesale in recent years, it is yet to become widespread in HPC. RISC-V accelerators offer a compelling option where the HPC community can benefit from the specialisation offered by the open nature of the standard but without the extensive ecosystem changes required when adopting RISC-V CPUs. In this paper we explore porting the Cooley-Tukey Fast Fourier Transform (FFT) algorithm to the Tenstorrent Wormhole PCIe RISC-V based accelerator. Built upon Tenstorrent's Tensix architecture, this technology decouples the movement of data from compute, potentially offering increased control to the programmer. Exploring different optimisation techniques to address the bottlenecks inherent in data movement, we demonstrate that for a 2D FFT whilst the Wormhole n300 is slower than a server-grade 24-core Xeon Platinum CPU, the Wormhole draws around 8 times less power and consumes around 2.8 times less energy than the CPU when computing the Fourier transform.

## Submission metadata

- arXiv ID: 2506.15437
- Category: cs.DC (Distributed, Parallel, and Cluster Computing)
- Submitted: 18 Jun 2025 (v1)
- Comments: Author accepted version of paper submitted to RISC-V for HPC ISC workshop 2025
- DOI: https://doi.org/10.48550/arXiv.2506.15437
- HTML version: https://arxiv.org/html/2506.15437v1
- PDF: https://arxiv.org/pdf/2506.15437

## Capture Notes

- Metadata only — PDF not fetched.
- Useful for: data-movement-vs-compute decoupling discussion, real Wormhole-n300 perf/power numbers, and example of porting a non-ML algorithm to TT-Metal.
- Same lead author (Nick Brown, EPCC) is involved in the riscv.epcc.ed.ac.uk Tenstorrent intro slides — useful tutorial cluster.
