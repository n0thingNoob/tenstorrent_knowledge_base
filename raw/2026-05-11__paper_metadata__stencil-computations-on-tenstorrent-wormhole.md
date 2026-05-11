# Stencil Computations on Tenstorrent Wormhole

## Source metadata

- Source URL: https://arxiv.org/abs/2605.07599v1
- Published: 2026-05-08
- Collected: 2026-05-11T15:11:33+00:00
- Collector: weekly_source_collect.py
- Source bucket: paper_metadata
- Evidence hint: paper
- Authors: Lorenzo Piarulli, Daniele De Sensi

## Summary snippet

As investment in AI-focused accelerators grows and their deployment in supercomputing facilities
expands, understanding whether these architectures can efficiently support traditional scientific
kernels is critical for the future of High-Performance Computing. We investigate the mapping of 2D
5-point stencil computations onto the Tenstorrent Wormhole, a RISC-V AI dataflow accelerator. We
develop two heterogeneous implementations: Axpy, which decomposes the stencil into element-wise
submatrix operations, and MatMul, which reformulates it as a matrix multiplication. While the CPU
baseline remains 3x faster end-to-end, profiling reveals that the isolated Wormhole kernel is
competitive with CPU execution, with the gap driven by PCIe transfers, device initialization, and
host-side preprocessing. Despite slower runtime, Axpy achieves lower energy consumption than the CPU
baseline for large inputs. Through detailed profiling and theoretical analysis, we identify key
architectural and software limitations of the current platform and outline concrete hardware and
software directions that could make AI accelerators competitive for HPC workloads.
