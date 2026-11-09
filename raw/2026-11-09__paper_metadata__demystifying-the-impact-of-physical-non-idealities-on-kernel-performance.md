# Demystifying the Impact of Physical Non-Idealities on Kernel Performance

## Source metadata

- Source URL: https://arxiv.org/abs/2610.37466v2
- Published: 2026-10-27
- Collected: 2026-11-09T14:12:13+00:00
- Collector: weekly_source_collect.py
- Source bucket: paper_metadata
- Evidence hint: paper
- Authors: Supun Kuruppu, Pranav Dangi, Wei Li, Zhenyu Bai, Tulika Mitra

## Summary snippet

Physical non-idealities in integrated circuit (IC) design, fabrication, and operation are concealed
by conventional hardware abstractions, causing unexpected performance variations in kernels. For
large-scale workloads, such as AI training and inference, performance unpredictability can lead to
substantial losses. We investigate this problem in NVIDIA H100 GPUs with their distributed shared
memory (DSMEM) architectural feature that reduces data movement from the L2 cache to Streaming
Multiprocessors (SMs) with multicast loads, and uncover that floorsweeping restricts the number of
SMs usable for clustered execution, increasing the number of execution waves of kernels. To
alleviate this performance penalty, we introduce the wave-aware clustering strategy that accounts
for these resource constraints and improves the throughput of the Hopper version of FlashAttention 4
by up to 5.30% over the unclustered baseline. Furthermore, we discover that the power constraint
imposed by the thermal design power (TDP) limit causes the DSMEM-based memory bandwidth optimization
to improve the throughput even for compute-bound kernels by creating a power headroom for higher SM
frequencies through reduced data movement. Extending this analysis beyond GPUs, we find that power
constraints also limit throughput scaling on Tenstorrent's Wormhole accelerator, highlighting the
broader importance of accounting for physical non-idealities in kernel performance engineering.
