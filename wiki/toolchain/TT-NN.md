---
type: toolchain
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, toolchain, ttnn]
evidence_level: official
---

# TT-NN

## Summary

TT-NN is Tenstorrent's **Python and C++ neural-network operator library**. It sits one layer above [[TT-Metal]] and provides ready-made tile-aligned ops (matmul, attention, eltwise, layout conversions, etc.) used by model demos.

Per [[Source - tt-metal README]]: "TT-NN is a Python & C++ Neural Network OP library."

## Position in stack

```
High-level model / vLLM / framework
   鈫?TT-NN ops (Python / C++)
   鈫?TT-Metal kernels
   鈫?Tensix + NoC
```

## Coverage in current corpus

The README enumerates featured models (Llama 3.3 70B, Qwen 2.5 7B/72B, Whisper, Mixtral 8x7B) and gives perf metrics on n150 / n300 / QuietBox / Galaxy. Tech reports referenced under TT-NN: Advanced Performance Optimizations for Models, ViT-TTNN, LLMs in TT-NN, CNN bring-up.

> Detail beyond the README is **not yet in `raw/`**. Op semantics, sharding policies, and host-side runtime details are flagged in [[questions/README|Questions]].

## Related pages

- [[TT-Metal]], [[TT-MLIR]], [[Programming Model]]
- [[Tile-Based Execution]] (TT-NN ops always operate on 32脳32 tiles)

## Sources

- `raw/2026-05-05__github_readme__tt-metal-readme.md`
- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md` (mentions TT-NN as a higher layer)

