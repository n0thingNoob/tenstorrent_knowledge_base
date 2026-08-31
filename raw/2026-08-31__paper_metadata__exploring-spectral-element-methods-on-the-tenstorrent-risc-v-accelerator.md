# Exploring spectral element methods on the Tenstorrent RISC-V accelerator

## Source metadata

- Source URL: https://arxiv.org/abs/2608.22964v1
- Published: 2026-08-24
- Collected: 2026-08-31T14:19:55+00:00
- Collector: weekly_source_collect.py
- Source bucket: paper_metadata
- Evidence hint: paper
- Authors: Daniyal Arshad, Nick Brown

## Summary snippet

The growing availability of commodity RISC-V hardware has sparked interest in its use for High
Performance Computing (HPC), with PCIe accelerator cards offering a practical near-term pathway to
adoption. The Tenstorrent Wormhole is one example, with dedicated vector and matrix units across 128
Tensix cores, and is widely available. In this paper, we explore porting the AX kernel of Nekbone, a
widely used HPC mini-application derived from the Gordon Bell Prize-winning Nek5000 spectral element
solver, onto the Wormhole accelerator. This kernel evaluates the Poisson operator, and we describe
the mapping of the algorithm onto the Tensix. The initial performance results reveal that the host-
side data transposition, required for the z-direction gradient computation, is a severe bottleneck.
Consequently, we investigated two optimisation strategies that yield dramatic improvements,
achieving 242.97 GFLOPS for 100000 elements across 128 Tensix cores, outperforming a 24-core Xeon
Platinum CPU and drawing approximately 7 times less power.
