# Great Expectations: Benchmarking the Real-World Performance of RVV 1.0 in HPC

## Source metadata

- Source URL: https://arxiv.org/abs/2608.28097v1
- Published: 2026-08-28
- Collected: 2026-08-31T14:19:55+00:00
- Collector: weekly_source_collect.py
- Source bucket: paper_metadata
- Evidence hint: paper
- Authors: Stepan Nassyr, Prateek Chawla, Daniel Seibel, Jayesh Badwaik, Kaveh Haghighi Mood, Andreas Herten

## Summary snippet

Following the ratification of the RISC-V Vector Extension (RVV 1.0), new commercially available
silicon has been adopting the extension. This paper revisits the question of RISC-V viability for
High-Performance-Computing (HPC) by benchmarking the latest RVV 1.0-capable hardware (SiFive X280
(Tenstorrent Blackhole), SpacemiT X60 (K1) and X100/A100 (K3), and T-Head C920v2 (Sophon SG2044)).
We assess these platforms using standard HPC benchmarks (BLAS, FFTW, HPL, HPCG) and synthetic
workloads (STREAM, FMA throughput) and compare them to a state-of-the-art HPC ARM64 chip (NVIDIA
Grace). Our findings show that while RVV 1.0 delivers significant performance improvements over
scalar execution, hardware-specific implementation challenges remain. We detail these performance
characteristics and discuss the remaining hurdles for RISC-V, including RVV, to become a mainstay in
the HPC landscape.
