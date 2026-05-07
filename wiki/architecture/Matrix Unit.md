---
type: architecture
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, matmul, fpu]
evidence_level: official
---

# Matrix Unit

## Summary

The **Matrix Unit** (a.k.a. **FPU**) is the per-Tensix matrix multiply-accumulate engine. Per [[Source - corsix Part 7 — MatMul]] it can dispatch:

```
Dst[8,16] += SrcB[8,16] @ SrcA[16,16]
```

every cycle. Implemented as **2048 multipliers, each 7b × 5b**, plus an equivalent 2048-input adder tree. To handle wider mantissa formats, the multiplier is invoked in stages — see [[Fidelity Stages]].

## Operand sources

| Operand | Comes from |
|---|---|
| `SrcA` (16×16) | filled by Tensix Unpacker from L1 |
| `SrcB` (8×16) | filled by Tensix Unpacker from L1 |
| `Dst` (8×16) | matrix output; also the input for the [[SFPU]]; drained by Tensix Packer |

`Dst` can hold either 512 rows of 16 lanes × 32 b, or 1024 rows of 16 lanes × 16 b.

## TT-NN tile mapping

TT-NN exposes a **32×32 tile** as the API granularity. A 32×32 matmul block is built from **16 invocations of the 8×16 primitive** (8 chunks of `Dst` × 32-element dot product = 16 primitive calls).

## Performance

| Format | Per-Tensix TFLOP/s | n150s (72 T) | n300s (128 T) |
|---|---|---|---|
| LoFi (fp8 e5m2) | 4.096 | ~294.9 | ~524.3 |
| LoFi+HiFi2 (bfp8) | 2.048 | 147.5 | 262.1 |
| LoFi+HiFi2+HiFi3+HiFi4 (fp16) | 1.024 | 73.7 | 131.1 |

For LoFi, advertised number is 88.9% of expected — 16/18 — suggesting Unpacker/Packer is the bottleneck at very low precision, not the multipliers.

## Special-value handling

Wormhole does **not** implement full IEEE 754. Some inputs of NaN/Inf are handled correctly, others not (per the `tech_reports/Handling_Special_Value/special_values.md` report referenced in raw, not yet captured). Denormals are flushed to zero on input and output.

## Related operations

The Matrix Unit also supports a few non-MAC matrix ops; full list lives in `tech_reports/matrix_engine/matrix_engine.md` (referenced in raw, not yet captured).

## Related pages

- [[Tensix]], [[Fidelity Stages]], [[SFPU]], [[Tile-Based Execution]], [[L1 Memory]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-tensix-tile.md`
