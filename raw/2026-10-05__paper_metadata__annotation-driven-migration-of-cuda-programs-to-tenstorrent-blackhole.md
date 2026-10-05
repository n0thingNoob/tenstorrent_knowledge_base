# Annotation-Driven Migration of CUDA Programs to Tenstorrent Blackhole

## Source metadata

- Source URL: https://arxiv.org/abs/2610.02658v1
- Published: 2026-10-02
- Collected: 2026-10-05T14:22:55+00:00
- Collector: weekly_source_collect.py
- Source bucket: paper_metadata
- Evidence hint: paper
- Authors: Ayumi Ohno, Shinya Takamaeda-Yamazaki

## Summary snippet

Tenstorrent Blackhole combines distributed local memories, explicit inter-core communication, and
Tensix cores decoupling data movement from computation. CUDA offers a substantial HPC software base
but leaves physical data placement and scheduling largely implicit. Migrating CUDA HPC kernels to
Blackhole requires spatial mapping across cores and per-core coordination of compute and data-
movement kernels. We present an MLIR-based compiler deriving data placement, inter-core
communication, and tile computation from a statically shaped affine CUDA subset. Declarative
annotations express choices not fixed by the source, including compute/DM operation placement and
streaming granularity. We evaluate it on Gaussian elimination, five-point stencil, and symmetric
rank-k update. Relative to our compiler's default realizations, the best measured configurations
achieve a 4.2x speedup for BF16 Gaussian and 2.1-2.2x for FP32 Gaussian and Jacobi. A choice's
performance impact can reverse with surrounding policies, precision, and loop schedule, motivating
comparison of alternative per-core realizations rather than independent policy selection.
