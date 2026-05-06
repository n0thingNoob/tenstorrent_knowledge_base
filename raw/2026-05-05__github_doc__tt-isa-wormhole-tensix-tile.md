---
title: "tt-isa-documentation — Wormhole Tensix Tile"
source_type: "github_doc"
original_url: "https://github.com/tenstorrent/tt-isa-documentation/blob/main/WormholeB0/TensixTile/README.md"
repository: "tenstorrent/tt-isa-documentation"
commit_or_version: "main"
fetched_at: "2026-05-05"
status: "captured"
license: "unknown"
tags:
  - tenstorrent
  - wormhole
---

# tt-isa-documentation — Wormhole Tensix Tile

Source URL: https://github.com/tenstorrent/tt-isa-documentation/blob/main/WormholeB0/TensixTile/README.md
Captured at: 2026-05-05
Status: captured

## Source Content

# Tensix Tile

Each Tensix tile contains:
  * [1464 KiB of RAM called L1](L1.md)
  * [5x "Baby" RISCV (RV32IM) cores](BabyRISCV/README.md)
  * [2x NoC connections](../NoC/README.md) allowing the local RISCV cores to access data in other tiles, and allowing other tiles to access data from this tile
  * [1x NoC overlay](../NoC/Overlay/README.md) - a little coprocessor that can assist with NoC transactions
  * [1x Tensix coprocessor](TensixCoprocessor/README.md) - a big AI coprocessor, itself containing:
    * [2x Unpacker](TensixCoprocessor/Unpackers/README.md), for moving data from L1 into the coprocessor
    * [1x Matrix Unit (FPU)](TensixCoprocessor/MatrixUnit.md), for performing low precision matrix multiply-accumulate operations and some other matrix operations
    * [1x Vector Unit (SFPU)](TensixCoprocessor/VectorUnit.md), for performing 32-wide SIMD operations on 32-bit lanes, including FP32 multiply-accumulate operations
    * [1x Scalar Unit (ThCon)](TensixCoprocessor/ScalarUnit.md), for performing integer scalar operations and 128-bit memory operations against L1 (including atomics)
    * [4x Packer](TensixCoprocessor/Packers/README.md), for moving data from the coprocessor back to L1
  * A variety of little utility devices, mainly for the benefit of the RISCV cores: [the mover](Mover.md), [mailboxes](BabyRISCV/Mailboxes.md), [TDMA-RISC](TDMA-RISC.md), [the debug timestamper](DebugTimestamper.md), and the [PIC](PIC.md).

It is expected that the programmer will provide code for the RISCV cores to execute. High performance will be achieved by having that code oversee the operation of the NoC and the Tensix coprocessor. One very natural division of labour is to have two RISCV cores oversee the NoC and three RISCV cores oversee the Tensix coprocessor. The RISCV cores are not intended to achieve high performance on their own; they are intended to oversee the other components that _actually_ drive performance.

## Capture Notes

- This is the index page for the Tensix Tile sub-tree. Each linked sub-page (L1.md, BabyRISCV/README.md, TensixCoprocessor/README.md, TensixCoprocessor/Unpackers, MatrixUnit, VectorUnit, ScalarUnit, Packers, Mover, Mailboxes, TDMA-RISC, DebugTimestamper, PIC) is a separate high-priority capture target.
- Note: includes "4x Packer" — Wormhole has 4 packers, distinct from the 2 unpackers — corroborate against corsix.
- This sub-tree is the deepest authoritative ISA-level documentation outside source code.
