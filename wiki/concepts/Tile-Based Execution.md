---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, tiles]
evidence_level: official
---

# Tile-Based Execution

## Summary

Wormhole hardware natively operates on **32×32 element tiles**. Tiles are the unit of:

- L1 storage allocation
- Circular-buffer slots
- DMA transfers (`noc_async_read_tile`, `noc_async_write_tile`)
- TT-NN op dispatch
- Compute-API operands (`add_tiles`, `pack_tile`, `sin_tile`, etc.)

A larger Tensix-native sub-tile unit is the **face**: 16×16 elements. A "tile" in TT-NN is the 32×32 outer block, made of four 16×16 faces. The 8×16 chunk operated on by a single Matrix MAC is the primitive ([[Source - corsix Part 7 — MatMul]]).

Per [[Source - METALIUM_GUIDE]]:

> "Tenstorrent hardware natively operates on 32×32 element tiles, which optimizes common deep learning operations like matrix multiplication and convolution."

## Implications

- A 48×1024 matrix becomes 64×1024 once tile-aligned (padding 16 rows).
- Tilization / untilization (data-layout conversions between linear and tiled formats) can run on-device.
- Memory accesses match tile granularity — large stride-by-row buffering is avoided.
- The hardware's matmul throughput is reported per-tile cycles, not per element.

## Tile data format zoo

`Dst` (and L1) can hold tile lanes in many formats: fp32, bf16, fp16, int32, signmag32, signmag16, signmag11, signmag8, plus block-float variants (bfp2, bfp4, bfp8). Format affects fidelity stages on the matrix engine. See [[Fidelity Stages]] and the (uncaptured) `tech_reports/data_formats/data_formats.md`.

## Related pages

- [[Circular Buffers]], [[L1 Memory]], [[Matrix Unit]], [[Fidelity Stages]], [[Programming Model]]

## Sources

- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
