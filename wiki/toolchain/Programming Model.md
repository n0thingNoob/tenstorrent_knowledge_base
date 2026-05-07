---
type: toolchain
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, programming-model]
evidence_level: official
---

# Programming Model

## Summary

The user-visible programming model of [[TT-Metal]] is "OpenCL-like": explicit device, command queues, buffers, kernels, runtime arguments. Underneath the hood, the model is **distributed software pipelining over a 2D-torus mesh of compute tiles** — each [[Tensix]] runs three small kernels ([[Reader Compute Writer Kernels|reader / compute / writer]]) coordinating via [[Circular Buffers]] in [[L1 Memory]].

## Stack

```
High-level model (PyTorch / JAX / vLLM)
   ↓
TT-Forge / TT-MLIR / TT-NN
   ↓
TT-Metal (host C++ + kernel C++)
   ↓
Reader / Compute / Writer kernels per Tensix
   ↓
Tensix coprocessor + NoC + L1
   ↓
Wormhole hardware
```

## What the user writes

For one Tensix:

- A reader kernel C++ file (NoC #0).
- A compute kernel C++ file (compiled three times for Unpack/Math/Pack baby cores).
- A writer kernel C++ file (NoC #1).
- A host-side program: open device → allocate buffers → create CBs → create kernels → set runtime args → enqueue → read back.

For multi-Tensix:

- The same kernels assigned to a `CoreRange`.
- Per-core runtime args carry per-core data ranges (no built-in `get_global_id()`).
- `tt::tt_metal::split_work_to_cores` helper for SPMD work distribution.

## What is explicit vs implicit

|                               Item                                |        Explicit (user controls)         |       Implicit (runtime/compiler)        |
|:-----------------------------------------------------------------:|:---------------------------------------:|:----------------------------------------:|
|                        Tile shape (32×32)                         |                   n/a                   |              hardware-fixed              |
|                           L1 placement                            |                   yes                   |                  mostly                  |
|                        DRAM ↔ L1 transfers                        |    yes (`noc_async_read/write_tile`)    |                   n/a                    |
|                Per-tile core count and assignment                 |                   yes                   |                   n/a                    |
|                    Reader/compute/writer split                    |                   yes                   |                   n/a                    |
|            Unpack vs Math vs Pack split inside compute            |             mostly implicit             |   runtime dispatches code by core type   |
| Hardware-generation differences (vector width, instruction names) |               abstracted                | Compute API picks correct LLK at compile |
|                  Tensix configuration registers                   |            abstracted by LLK            |                 LLK init                 |
|                  NoC virtual channel / buddy bit                  |             mostly implicit             |        hardware + flags if needed        |
|               Synchronisation between three kernels               |                implicit                 |         circular buffer metadata         |
|                   Cross-Tensix synchronisation                    | explicit (host semaphores, NoC atomics) |                   n/a                    |

## Mesh-first design

`MeshDevice::create_unit_mesh()` treats every device as part of a mesh. Even a single chip = 1×1 mesh. Multi-chip programs use the same API.

## Fast vs slow dispatch

- **Fast dispatch** (default) — host queues commands; a dedicated dispatch core (often on an unused Ethernet tile) feeds the device. Async, low CPU overhead.
- **Slow dispatch** (`TT_METAL_SLOW_DISPATCH_MODE=1`) — host blocks on each operation. Debug only.

## Strict in-order command queue, two queues per device

Two queues per device — typically Q0 = compute, Q1 = data transfer. Cross-queue ordering via events.

## Related pages

- [[TT-Metal]], [[TT-NN]], [[TT-MLIR]], [[Reader Compute Writer Kernels]], [[Circular Buffers]], [[Tile-Based Execution]], [[Tensix]], [[NoC]], [[L1 Memory]], [[Compiler Stack]], [[Compute API and Hardware Abstraction]]

## Sources

- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
- `raw/2026-05-05__github_readme__tt-metal-readme.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
