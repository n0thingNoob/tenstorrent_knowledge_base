---
type: concept
status: stub
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, compiler, mlir]
evidence_level: official
---

# TT-MLIR

## Summary

TT-MLIR is an open-source **MLIR-based compiler** for Tenstorrent AI accelerators. It defines custom MLIR dialects and lowering passes targeting [[TT-Metal|TTNN/TT-Metalium]]. Built on LLVM's MLIR. Frontend: StableHLO (and via tt-xla, tt-torch, tt-forge).

Per the README:

> "tt-mlir is a compiler project aimed at defining MLIR dialects to abstract compute on Tenstorrent AI accelerators. It is built on top of the MLIR compiler infrastructure and targets TTNN."

## Stated goals

- Generality (training + inference, wide model coverage)
- First-class scaling primitives for multi-chip
- Out-of-box performance
- Human-in-the-loop guided optimization
- Open-source development

## Coverage in current corpus

Only the README is in `raw/`. The dialect tree (TTIR, TTNN, TTKernel) and the lowering pipeline are **not yet captured**. Doc site: https://docs.tenstorrent.com/tt-mlir/.

Referenced sibling projects: tt-xla, tt-forge-fe, tt-torch (deprecated), tt-tvm.

## Open questions

See [[open_questions]] for: TTIR vs TTNN dialect responsibilities, TTKernel lowering, where mapping decisions (placement, sharding, kernel selection) are made, and how compile-time vs runtime cost is split.

## Related pages

- [[Compiler Stack]], [[TT-Metal]], [[TT-NN]], [[TT-Forge]]

## Sources

- `raw/2026-05-05__github_readme__tt-metal-readme.md` (mentions TT-MLIR as related project)
- README of tenstorrent/tt-mlir captured during Pass 1 (referenced in manifest)
