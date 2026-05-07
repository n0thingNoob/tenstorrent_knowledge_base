---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, matmul, fp]
evidence_level: official
---

# Fidelity Stages

## Summary

Wormhole's [[Matrix Unit]] uses a **7b 脳 5b multiplier** as its primitive. To handle data formats with more mantissa than 7脳5 covers, the multiplier is invoked in stages: **LoFi**, **HiFi2**, **HiFi3**, **HiFi4** ([[Source - corsix Part 7 鈥?MatMul]]). The programmer chooses how many stages to run.

## Stage-by-format coverage

| Format | Stages required | Notes |
|---|---|---|
| bfp2 / bfp4 | LoFi | All mantissa fits |
| fp8 (e5m2) | LoFi | 3-bit mantissa fits in 5-bit |
| bfp8 | LoFi + HiFi2 | full coverage; can drop HiFi2 if losing 2 bits is acceptable |
| bf16 | LoFi + HiFi2 + HiFi3 + HiFi4 | full coverage; HiFi3/HiFi4 contribute few bits |
| fp16 | LoFi + HiFi2 + HiFi3 + HiFi4 | even with all 4 stages, 1 bit of SrcA mantissa not consumed |

Each Matrix unit can dispatch `Dst[8,16] += SrcB[8,16] @ SrcA[16,16]` per cycle at LoFi.

## TFLOP/s implications

Per [[Wormhole]] page:

| Format | n150s (72 Tensix) | n300s (128 Tensix) |
|---|---|---|
| LoFi only (e.g. fp8) | 294.9 TFLOP/s expected (advertised slightly lower 鈥?bottleneck is data transfer) | 524.3 TFLOP/s |
| LoFi + HiFi2 (bfp8) | 147.5 | 262.1 |
| LoFi + HiFi2 + HiFi3 + HiFi4 (fp16) | 73.7 | 131.1 |

Each extra stage doubles compute cost; data-movement cost stays constant 鈥?at LoFi, advertised throughput is **88.9%** of the multiplier-only ceiling, suggesting the bottleneck shifts to Unpacker/Packer at low precision.

## Programmer surface

The programmer chooses the stage count for an op (typically driven by the data format being used). Higher fidelity = lower throughput, more arithmetic precision.

## Inter-stage rounding

An extra rounding step (to `Dst` precision) occurs between each fidelity stage when more than just LoFi is used.

## Research signal

This is a fairly unusual primitive: most accelerators commit to a fixed multiplier width per format. Wormhole's "iterate the small multiplier" approach trades latency for chip-area savings. Performance modelling and possible compiler-driven fidelity selection (not just based on input format but on output-precision needs) is a candidate research direction. Tracked in [[questions/README|Questions]].

## Related pages

- [[Matrix Unit]], [[Tile-Based Execution]], [[Tensix]], [[Programming Model]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-tensix-tile.md`

