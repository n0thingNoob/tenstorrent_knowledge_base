# Schedules Are Solvable Symbols: Tuning-Free Compilation of Tile Programs on Dataflow Architectures

## Source metadata

- Source URL: https://arxiv.org/abs/2609.29219v1
- Published: 2026-09-24
- Collected: 2026-10-05T14:22:55+00:00
- Collector: weekly_source_collect.py
- Source bucket: paper_metadata
- Evidence hint: paper
- Authors: Heru Wang, Wei Li, Zhenyu Bai, Tulika Mitra

## Summary snippet

Modern AI and HPC accelerators increasingly expose dataflow features: software-visible mechanisms
for data movement and overlap, such as inter-core communication through the on-chip network and
intra-core asynchronous pipelining. These features shift scheduling responsibility from hardware to
the compiler, and because placement, movement, and synchronization become software-visible, they
also make the performance of static schedules predictable. Yet high performance on such hardware
still relies on vendor-engineered kernel libraries or profile-based auto-tuning, whose embedded
expert knowledge transfers poorly across architectures and algorithms. We present Loom, a tuning-
free symbolic compiler framework for tile-based SPMD programs on spatial dataflow architectures. The
central idea is to treat tile-based SPMD compilation as a hardware-explicit static optimization
problem. Loom enumerates discrete spatial-mapping and communication candidates while keeping value
parameters, such as tiling factors and pipeline knobs, symbolic within each candidate. From an
explicit hardware description, it derives symbolic legality constraints and latency expressions,
formulates one CP-SAT problem per schedule candidate, and jointly solves inter-core dataflow, intra-
core asynchronous scheduling, and block sizes at compile time. On two Tenstorrent generations,
Wormhole and Blackhole, Loom matches or exceeds the vendor-optimized TTNN library on GEMM, Flash
Attention, and Flash Decode, out of the box and without per-shape profiling or profile-based
platform-specific schedule tuning. These results suggest that hardware-derived symbolic compilation
provides a retargetable alternative to profiling-based tuning for spatial dataflow architectures
while remaining interpretable by keeping optimization decisions traceable to source-level symbols.
