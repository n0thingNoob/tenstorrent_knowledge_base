---
type: question
status: needs-source
created: 2026-05-06
updated: 2026-05-06
tags: [tenstorrent, wormhole, performance, questions]
evidence_level: unknown
---

# Performance Questions

## Q12. Why is fp8 throughput about 88.9% of expected?

- Why it matters: if pack/unpack is the real limiter, that is a reusable performance model and possibly a research result.
- Evidence needed: GEMM-related tech reports or direct modeling.
- Related pages: [[architecture/Matrix Unit|Matrix Unit]], [[concepts/Fidelity Stages|Fidelity Stages]]

## Q13. When does sharded placement beat interleaved placement?

- Why it matters: current docs give qualitative guidance but not decision-quality criteria.
- Evidence needed: tensor-layout or attention/conv tech reports.
- Related pages: [[architecture/L1 Memory|L1 Memory]], [[toolchain/TT-Metal|TT-Metal]]

## Q14. What is realistic NoC bandwidth utilization on real workloads?

- Why it matters: the gap between theoretical and achieved utilization is central to systems interpretation.
- Evidence needed: bandwidth tech reports or trace-based experiments.
- Related pages: [[architecture/NoC|NoC]], [[architecture/Wormhole|Wormhole]]
