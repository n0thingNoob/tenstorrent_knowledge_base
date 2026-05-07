---
type: toolchain
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, toolchain, programming-model]
evidence_level: official
---

# TT-Metal

## Summary

**TT-Metalium** (a.k.a. tt-Metal, Metal) is Tenstorrent's low-level SDK for [[Wormhole]] and other Tensix processors. API design "resembles OpenCL" (per [[Source - METALIUM_GUIDE]]). C++ host API + per-Tensix kernel programming.

It is the **base layer** of the stack: [[TT-NN]], [[TT-MLIR]], and [[TT-Forge]] are built on top.

## Programming model

Every program is implicitly a **mesh** ("a single chip is treated as a 1×1 mesh"). The basic flow:

1. `MeshDevice::create_unit_mesh()` — open device.
2. Allocate `MeshBuffer` (DRAM or L1).
3. Configure circular buffers in [[L1 Memory]] for inter-kernel comms.
4. Compile kernels (typically three per Tensix — see [[Reader Compute Writer Kernels]]).
5. Set `RuntimeArgs` per (kernel, core).
6. Wrap into `MeshWorkload` and `EnqueueMeshWorkload(cq, workload, blocking)`.
7. `EnqueueReadMeshBuffer` to retrieve results.

Two command queues per device. Conventional split: queue 0 = compute, queue 1 = data transfer. Cross-queue sync via events (`enqueue_record_event` / `enqueue_wait_for_event`).

## Compute API and hardware abstraction

The Compute API (e.g. `add_tiles`, `sin_tile`, `pack_tile`) **abstracts hardware-generation differences**. The same `sin_tile()` call lowers to different SFPU sequences on Grayskull (64-lane), Wormhole (32-lane), and Blackhole. This is the *raison d'être* of the abstraction layer per the guide.

## SPMD / MPMD

SPMD is the default. Helper: `tt::tt_metal::split_work_to_cores(grid_size, work_size)` returns two core groups (primary and secondary) so workloads that don't divide evenly remain near-balanced.

MPMD is supported for cases like data-reuse matmul (broadcast-driver kernels on specific Tensix).

## Fast dispatch

A dedicated RV core (often on an unused Ethernet tile) processes queued commands so the host CPU is free. Disabling (`TT_METAL_SLOW_DISPATCH_MODE=1`) reverts to host-driven blocking I/O — debug only.

## Position in stack

```
High-level model / framework
   ↓
TT-Forge / TT-MLIR / TT-NN
   ↓
TT-Metal (host C++ + kernel C++)
   ↓
Reader / Compute / Writer kernels on Baby RV cores
   ↓
Tensix coprocessor + NoC
```

## Related pages

- [[TT-NN]], [[TT-MLIR]], [[TT-Forge]], [[Programming Model]]
- [[Reader Compute Writer Kernels]], [[Circular Buffers]], [[Tile-Based Execution]]
- [[Tensix]], [[NoC]], [[L1 Memory]]

## Sources

- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
- `raw/2026-05-05__github_readme__tt-metal-readme.md`
