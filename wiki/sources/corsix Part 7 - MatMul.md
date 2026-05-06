---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, blog, matmul]
source_path: raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md
evidence_level: blog
---

# Source — corsix Part 7: Bits of the MatMul

## Why it matters

The clearest published explanation of Wormhole's **multi-stage matrix engine** ("[[Fidelity Stages]]") and its 7×5-bit primitive multiplier. Independently derives the published TFLOP/s numbers.

## Key facts

- Tensix Matrix dispatches `Dst[8,16] += SrcB[8,16] @ SrcA[16,16]` per cycle.
- Implemented as 2048× **7b × 5b** multipliers + 2048-input adder.
- A 32×32 TT-Metal tile's matmul is built from 16 invocations of the 8×16 primitive.
- **Fidelity stages**: LoFi (3×3 mantissa region, fp8/bfp2/bfp4) → +HiFi2 (bfp8) → +HiFi3 → +HiFi4 (bf16/fp16). Each stage doubles compute cost.
- Per-Tensix peak: 4.096 TFLOP/s LoFi, 2.048 LoFi+HiFi2, 1.024 LoFi+HiFi2+3+4.
- n150s (72 T) and n300s (128 T) advertised numbers match these exactly for bfp8 and fp16; fp8 falls 11.1% short, suggesting Unpack/Pack throughput becomes the bottleneck at low precision.
- Conventional core mapping shown in diagram: T0=Unpack, T1=Math (Matrix+Vector), T2=Pack, BRISC+NC drive the two NoC routers.
- IEEE 754 simplifications: denormals flushed; some NaN/Inf cases not strictly handled (referenced to `tech_reports/Handling_Special_Value/special_values.md`).

## Technical details

**Architecture:** the multi-stage multiplier idea is unusual. Most accelerators commit to a fixed multiplier width per format; Wormhole pays latency in extra cycles to spend less area.

**Memory:** Tensix Pack supports `L1 = Dst` and `L1 += Dst` (and ReLU variants), eliminating some Unpack writes back to Dst.

**Performance:** the 88.9% LoFi gap is the most interesting empirical signal — strongly suggests Unpack/Pack is the bottleneck at fp8 throughput, which has compiler/scheduling implications.

## Related pages

- [[Matrix Unit]], [[Fidelity Stages]], [[Tensix]], [[Tile-Based Execution]], [[Reader Compute Writer Kernels]]

## Open questions

- Detailed multiplier scheduling for HiFi3/4 (which mantissa slices, which order) — corsix infers but doesn't confirm.
- Exact Pack throughput limits — the 88.9%-of-peak number suggests a measurable bottleneck worth empirical study.
