# Kernel Performance Engineering under Physical Non-Idealities

## Source metadata

- Source URL: https://arxiv.org/abs/2610.37466v1
- Published: 2026-10-27
- Collected: 2026-11-02T14:13:37+00:00
- Collector: weekly_source_collect.py
- Source bucket: paper_metadata
- Evidence hint: paper
- Authors: Supun Kuruppu, Pranav Dangi, Wei Li, Zhenyu Bai, Tulika Mitra

## Summary snippet

Physical non-idealities in integrated circuit (IC) design and fabrication are concealed by
conventional hardware abstractions, yet they can limit kernel performance and obscure optimization
opportunities. Using distributed shared memory (DSMEM) on NVIDIA H100 GPUs as a case study, we show
how floorsweeping restricts hardware resources available for clustered execution, potentially
offsetting the benefits of reduced data movement enabled by DSMEM. Guided by these insights, we
develop a wave-aware clustering strategy that accounts for these resource constraints to improve
kernel performance. Evaluations using a global-load-and-broadcast microbenchmark, GEMM, and the
Hopper version of FlashAttention 4 demonstrate the performance implications of these constraints,
with wave-aware clustering improving FlashAttention 4 throughput by up to 5.30% over its baseline.
We further show that, under thermal design power (TDP) limits, reduced data movement enables higher
Streaming Multiprocessor (SM) frequencies through Dynamic Voltage and Frequency Scaling (DVFS),
explaining otherwise unexpected throughput improvements. Extending this analysis beyond GPUs, we
show that power constraints also limit throughput scaling on Tenstorrent's Wormhole accelerator,
highlighting the broader importance of accounting for physical non-idealities when analyzing and
optimizing kernel performance.
