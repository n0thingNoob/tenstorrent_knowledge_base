---
title: "Assessing Tenstorrent's RISC-V MatMul Acceleration Capabilities"
source_type: "paper_metadata"
original_url: "https://arxiv.org/abs/2505.06085"
repository: "unknown"
commit_or_version: "arXiv v3, 2025-06-20"
fetched_at: "2026-05-05"
status: "metadata_only"
license: "unknown"
tags:
  - tenstorrent
  - wormhole
---

# Assessing Tenstorrent's RISC-V MatMul Acceleration Capabilities

Source URL: https://arxiv.org/abs/2505.06085
Captured at: 2026-05-05
Status: metadata_only

## Source Content

# Assessing Tenstorrent's RISC-V MatMul Acceleration Capabilities

## Authors

- Hiari Pizzini Cavagna
- Daniele Cesarini
- Andrea Bartolini

## Abstract

> The increasing demand for generative AI as Large Language Models (LLMs) services has driven the need for specialized hardware architectures that optimize computational efficiency and energy consumption. This paper evaluates the performance of the Tenstorrent Grayskull e75 RISC-V accelerator for basic linear algebra kernels at reduced numerical precision, a fundamental operation in LLM computations. We present a detailed characterization of Grayskull's execution model, gridsize, matrix dimensions, data formats, and numerical precision impact computational efficiency. Furthermore, we compare Grayskull's performance against state-of-the-art architectures with tensor acceleration, including Intel Sapphire Rapids processors and two NVIDIA GPUs (V100 and A100). Whilst NVIDIA GPUs dominate raw performance, Grayskull demonstrates a competitive trade-off between power consumption and computational throughput, reaching a peak of 1.55 TFLOPs/Watt with BF16.

## Submission metadata

- arXiv ID: 2505.06085
- Category: cs.PF (Performance)
- Submitted: 9 May 2025 (v1)
- Last revised: 20 Jun 2025 (v3)
- Status: Accepted to Computational Aspects of Deep Learning Workshop at ISC High Performance 2025
- HTML version: https://arxiv.org/html/2505.06085v3
- PDF: https://arxiv.org/pdf/2505.06085

## Capture Notes

- Metadata only.
- Targets Grayskull rather than Wormhole, but Tensix execution-model characterization (gridsize, precision, data formats) carries over to Wormhole architecturally and is directly useful as a baseline for performance-modeling research on Wormhole.
- Includes head-to-head comparison vs A100/V100/Sapphire Rapids — useful "where does Tenstorrent fit" data point.
