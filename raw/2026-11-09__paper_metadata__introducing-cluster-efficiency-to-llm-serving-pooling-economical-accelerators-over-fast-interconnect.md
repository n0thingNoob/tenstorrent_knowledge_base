# Introducing Cluster Efficiency to LLM Serving: Pooling Economical Accelerators over Fast Interconnects

## Source metadata

- Source URL: https://arxiv.org/abs/2611.02975v2
- Published: 2026-11-02
- Collected: 2026-11-09T14:12:13+00:00
- Collector: weekly_source_collect.py
- Source bucket: paper_metadata
- Evidence hint: paper
- Authors: Youhe Jiang, Pavle Glušac, Binhang Yuan, Eiko Yoneki

## Summary snippet

Long-context large language model (LLM) serving places substantial demands on compute, memory
capacity, and memory bandwidth. Economical accelerators can offer these resources at lower cost, but
their limited per-device capacity requires pooling across devices, making communication overhead
critical. We study cluster efficiency, measured in tokens per dollar and per joule, and show how
low-latency, high-bandwidth interconnects enable economical accelerators to retain their cost
advantage. Guided by a characterization of coding-agent workloads and accelerator scaling, we
realize this design on the Tenstorrent Galaxy, a cluster of Blackhole chips. The serving stack
combines integrated communication engines, pipelined ring transfers, communication-computation
overlap, and device-side decode replay to reduce collective overhead. Across three dense models in
BF16 and 8-bit configurations with 8K-256K-token contexts, the Galaxy achieves 1.07-2.24$\times$ the
tokens per dollar of an eight-GPU RTX PRO 6000 Blackwell server under a three-year acquisition-and-
electricity cost model. Emulating TCP-class communication on the same chips reduces throughput by
23.5-67.4% and eliminates the cost advantage in every evaluated configuration. These results
demonstrate how fast interconnects translate the per-dollar resource advantages of economical
accelerators into cost-efficient long-context LLM serving.
