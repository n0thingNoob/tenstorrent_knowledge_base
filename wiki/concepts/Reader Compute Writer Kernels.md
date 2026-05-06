---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, kernels, programming-model]
evidence_level: official
---

# Reader / Compute / Writer Kernels

## Summary

The conventional [[TT-Metal]] kernel decomposition for one [[Tensix]] tile splits work across the 5 baby RISC-V cores into **three** logical kernels:

| Kernel | Drives | Conventional core | Role |
|---|---|---|---|
| **Reader** | NoC #0 + Unpacker | RISCV_0 (often "T0" + DM0) | Pulls tiles from DRAM / other tiles into [[Circular Buffers]] in [[L1 Memory]] |
| **Compute** | Tensix Math (FPU+SFPU) + Pack | T0/T1/T2 cooperatively | Reads tiles from input CBs, runs MAC/SFPU, packs results into output CB |
| **Writer** | NoC #1 + Packer drain | RISCV_1 ("NC") | Pulls tiles from output CB and ships them to DRAM / other tiles |

Compute is logically one kernel, but the **same C++ source is compiled three times** (once each for Unpack/Math/Pack baby cores). The compute API uses per-core conditional code blocks; the runtime selects the right binary per core.

Per [[Source - METALIUM_GUIDE]]:

> "The three kernels — reader, compute, and writer — coordinate their execution using circular buffers, which are implemented in SRAM and facilitated by hardware metadata synchronization."

## Why this is the natural decomposition

- 2 NoCs → naturally 2 data-movement kernels (one per direction).
- 3 cores in compute group (T0/T1/T2) drive 3 "phases" of Tensix (Unpack / Math / Pack).
- Reader and Writer kernels are **largely reusable across ops** since data-movement patterns repeat.

## Canonical example: vector add

The reader pulls two input tiles A[i] and B[i] into `c_0` and `c_1`. The compute kernel waits for both, calls `add_tiles`, and packs into `c_16`. The writer pulls from `c_16` and writes to output buffer C.

Key code patterns from [[Source - METALIUM_GUIDE]]:

```cpp
// Reader (DM0)
cb_reserve_back(cb_in0, 1);
noc_async_read_tile(i, a, get_write_ptr(cb_in0));
noc_async_read_barrier();
cb_push_back(cb_in0, 1);

// Compute (Unpack/Math/Pack)
binary_op_init_common(cb_in0, cb_in1, cb_out);
add_tiles_init(cb_in0, cb_in1, false);
cb_wait_front(cb_in0, 1); cb_wait_front(cb_in1, 1);
tile_regs_acquire();
add_tiles(cb_in0, cb_in1, 0, 0, dst_reg);
tile_regs_commit();
cb_pop_front(cb_in0, 1); cb_pop_front(cb_in1, 1);
cb_reserve_back(cb_out, 1);
tile_regs_wait();
pack_tile(dst_reg, cb_out, 0);
tile_regs_release();
cb_push_back(cb_out, 1);

// Writer (DM1)
cb_wait_front(cb_out, 1);
noc_async_write_tile(i, c, get_read_ptr(cb_out));
noc_async_write_barrier();
cb_pop_front(cb_out, 1);
```

## Tile-register dance (compute kernel)

`tile_regs_acquire / commit / wait / release` mediate handoff of the Tensix `Dst` register between Math and Pack — Math acquires/commits, Pack waits/releases.

## Variants & exceptions

- For deeper SFPU ops (e.g. `sin_tile`), data must be **explicitly** copied to `Dst` first: `copy_tile(...)` then `sin_tile(...)`. FPU ops (e.g. `add_tiles`) accept circular-buffer indices directly.
- MPMD: special operators (data-reuse matmul) override the convention with custom per-core kernels.
- The convention is "two RISCV cores oversee the NoC and three RISCV cores oversee the Tensix coprocessor" ([[Source - tt-isa Tensix Tile]]). Any RV core can drive any unit, but the runtime conventionally maps T0=Unpack, T1=Math, T2=Pack, B=boot/dispatch helper, NC=NoC #1 / writer.

## Related pages

- [[Circular Buffers]], [[Tensix]], [[Programming Model]], [[Tile-Based Execution]], [[Compute API and Hardware Abstraction]], [[NoC]]

## Sources

- `raw/2026-05-05__github_doc__tt-metal-metalium-guide.md`
- `raw/2026-05-05__github_doc__tt-isa-wormhole-tensix-tile.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md`
