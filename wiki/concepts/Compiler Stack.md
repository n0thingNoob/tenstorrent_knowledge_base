---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, compiler, runtime]
evidence_level: mixed
---

# Compiler Stack

## Summary

Tenstorrent's compiler/runtime stack lowers high-level model graphs through several layers down to per-Tensix kernels. The current open-source state, top to bottom:

```
PyTorch / JAX / StableHLO (frontend)
    ↓ (tt-forge / tt-xla / tt-torch)
TT-MLIR  (custom dialects on top of LLVM MLIR)
    ↓
TTNN / TT-Metal kernels  (C++)
    ↓ compile
Reader / Compute / Writer kernel binaries per baby RV core
    ↓ runtime dispatch (fast dispatch, command queues)
Tensix coprocessor + NoC + L1
```

## Layers (current corpus knowledge)

### TT-Forge / tt-xla / tt-torch

Frontend ingestors. Bridge from PyTorch / StableHLO / ONNX into [[TT-MLIR]]. Detail not in `raw/`.

### TT-MLIR

MLIR-based compiler. Defines custom dialects targeting [[TT-NN]] / [[TT-Metal]]. Goals include first-class scaling primitives for multi-chip and human-in-the-loop guided optimisation. ([[Source - tt-mlir README]] in raw via metadata; deeper dialect doc not yet captured.)

### TT-Metal (kernel-side compile)

The user's compute kernel C++ is **compiled three times** — once each for the Unpack / Math / Pack baby RV cores — with hardware-specific code sections selected by the Compute API templates. Reader and writer C++ each produce one binary on RISCV_0 / RISCV_1.

The Compute API is the **portability seam**: `sin_tile()` lowers to different Tensix instruction sequences on Grayskull (64-lane SFPU), Wormhole (32-lane SFPU), and Blackhole. ([[Source - METALIUM_GUIDE]].)

### Tensix LLK ([[TT-LLK]])

Low-level kernels: per-Tensix sequences of Tensix instructions (`MOP_CFG`, `MOP`, `REPLAY`, `SETC16`, `WRCFG`, `SFPLOAD`, etc.) plus C-header wrappers `TT_OP_X` / `TT_X` / `TTI_X`. Generated from `tt-budabackend/.../assembly.yaml`. Handles configuration-register init + the runtime-time instruction stream that drives Unpacker / Matrix / Packer / SFPU.

### Runtime / dispatch

- **Fast dispatch** — dedicated RV core (often on an unused E tile) feeds the command queue. ([[Source - METALIUM_GUIDE]].)
- Two command queues per device with event-based cross-queue ordering.
- Slow dispatch mode for debugging.

## Compile-time vs runtime responsibilities (current understanding)

| Responsibility | Where |
|---|---|
| Frontend graph capture | TT-Forge / tt-xla / tt-torch |
| Op fusion, layout decisions | TT-MLIR (dialect passes) — *details not captured in raw/* |
| Sharding placement | TT-MLIR + TT-NN — *details unclear in raw/* |
| Kernel selection (which TT-NN op) | TT-MLIR / TT-NN |
| Per-core kernel code | TT-Metal (compile) |
| Hardware-generation specialisation | Compute API → LLK (compile) |
| Per-core runtime args | Host program (run-time) |
| Tile-flow synchronisation | Circular buffers + Tensix Sync (run-time) |
| Cross-tile orchestration | Host program + NoC atomics + host-level semaphores |
| Command stream feed | Fast-dispatch core (run-time) |

## Gaps in current corpus

- TT-MLIR dialect descriptions and lowering pipeline.
- Where exactly mapping decisions (which op on which Tensix; tile shape; sharding scheme) are made — TT-MLIR vs TT-NN host code vs hand-written.
- Auto-tuning / cost models, if any.
- Integration with vLLM and other higher-level runtimes.

Tracked in [[open_questions]].

## Related pages

- [[TT-Metal]], [[TT-NN]], [[TT-MLIR]], [[TT-LLK]], [[Programming Model]], [[Compute API and Hardware Abstraction]], [[Tensix]]

## Sources

- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
- `raw/2026-05-05__github_readme__tt-metal-readme.md`
- `raw/2026-05-05__github_readme__tt-isa-documentation-readme.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
