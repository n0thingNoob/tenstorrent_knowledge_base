---
title: "Tenstorrent Wormhole Series Part 5: Taking apart T tiles"
source_type: "blog"
original_url: "https://www.corsix.org/content/tt-wh-part5"
repository: "unknown"
commit_or_version: "blog post dated 2024-09-22"
fetched_at: "2026-05-05"
status: "captured"
license: "unknown"
tags:
  - tenstorrent
  - wormhole
---

# Tenstorrent Wormhole Series Part 5: Taking apart T tiles

Source URL: https://www.corsix.org/content/tt-wh-part5
Captured at: 2026-05-05
Status: captured

## Source Content

Posted at [corsix.org](https://www.corsix.org/) on September 22, 2024

Previously, in [part 4](https://www.corsix.org/content/tt-wh-part4), we identified the 128 usable T tiles on my [Wormhole n300s board](https://tenstorrent.com/hardware/wormhole). These tiles are the workhorse of the board, so it is about time we took a detailed look inside one of them. Ignoring all the NoC functionality, my best guess as to the contents of each T tile is this diagram:

![](https://www.corsix.org/images/tt-wh-part5-t.svg)

Starting at the top of the diagram, we have 1464 KiB of SRAM, which is directly mapped into the tile-local address space starting at address [`0`](https://github.com/tenstorrent/tt-metal/blob/96ea95f42b3c2499aee0d371e8e3933d5472a38e/tt_metal/hw/inc/wormhole/dev_mem_map.h#L28-L29). It is connected to lots of other components within the tile, and other tiles can also access it via NoC requests (again, I have not shown any of the NoC functionality on the above diagram). The advertised capacity is 1.5 MB of SRAM; if you were hoping for 1.5 MiB, then you'd need 72 KiB more than the 1464 KiB shown, but you can find that distributed across the tile (32 KiB in `Dst`, 30 KiB in the core-local RAMs, 4 KiB in `SrcA`, 4 KiB in `SrcB`, 1 KiB in `Lreg`, and so on).

Moving down a row, we have five RISC-V RV32IM cores, which I've labelled as "B", "T0", "T1", "T2", and "NC". Each core has 32 GPRs, each 32 bits wide, along with a 32-bit program counter. The [RV32IM instruction set](https://riscv.org/technical/specifications/) can be roughly split into three pieces: load/store, ALU (arithmetic operations, bitwise operations, and multiply and divide), and branches - these execution resources are shown on the diagram within each core. The host system can put whatever RISC-V machine code it desires in L1, and the RISC-V cores will happily execute it. Said code will have exclusive bare-metal control of the cores; there are no interrupts, no user-mode/kernel-mode split, no hypervisor, etc. The RISC-V cores execute completely independently (of each other, and of the host), though there are mechanisms to synchronize them.

Moving down another row, things start to get interesting. Firstly, each core has 2 KiB or 4 KiB of core-local RAM mapped into the address space starting at address [`0xFFB00000`](https://github.com/tenstorrent/tt-metal/blob/96ea95f42b3c2499aee0d371e8e3933d5472a38e/tt_metal/hw/inc/wormhole/dev_mem_map.h#L35-L39). The C/C++ call stack is [usually located here](https://github.com/tenstorrent/tt-metal/blob/96ea95f42b3c2499aee0d371e8e3933d5472a38e/tt_metal/hw/inc/wormhole/dev_mem_map.h#L103-L108), thereby decreasing the load on L1, albeit with the trade-off that pointers into the stack cannot be meaningfully passed between cores nor used as the source or destination pointer for NoC requests. Next up, the "NC" core has 16 KiB of instruction RAM mapped into the address space starting at address [`0xFFC00000`](https://github.com/tenstorrent/tt-metal/blob/96ea95f42b3c2499aee0d371e8e3933d5472a38e/tt_metal/hw/inc/wormhole/dev_mem_map.h#L41-L43), presumably again to reduce the load on L1. Finally, this row contains three "Tensix" instruction pipes, one attached to each "T" core. This is where we leave the world of standard RISC-V instructions, and enter the world of Tenstorrent special sauce. One way of describing Tensix would be a massive AI coprocessor glued on to the three "T" cores, with emphasis on the word massive: the assorted Tensix pieces occupy much more area and perform vastly more FLOPs than the RISC-V cores that drive them. We'll look at the Tensix instruction pipes in more detail later, but the quick summary is that they ingest Tensix instructions and output (slightly modified) Tensix instructions. Said instructions are 32 bits wide, but other than the width being the same, the Tensix instruction set is completely unrelated to any RISC-V instruction set. The Tensix instruction set is also evolving with each Tenstorrent generation; Grayskull is slightly different to Wormhole, which in turn is slightly different to Blackhole, and so on.

Moving down again, we hit "Tensix Sync". At least conceptually, this unit ingests Tensix instructions coming out of the three pipes, and dispatches Tensix instructions to the eight backend execution resources. A handful of instructions relating to synchronization of the three inbound pipes execute at "Tensix Sync", either manipulating the mutexes and semaphores within "Tensix Sync", or selectively pausing an inbound pipe until certain conditions are met. Instructions leaving "Tensix Sync" are tagged with which pipe they originated from, which is relevant information for most backend instructions.

The next row of the diagram contains the eight Tensix backend execution resources, from left to right: Scalar (often called ThCon), ThCfg, Unpack, Matrix (often called FPU), Pack, Vector (often called SFPU), TDMA, and Xmov. For AI workloads, the star of the show is the Matrix unit, which amongst other things can dispatch [`Dst[8,16] = SrcB[8,16] @ SrcA[16,16]`](https://github.com/tenstorrent/tt-llk-wh-b0/blob/abd3e70304bd24661ccd84c5f712243771cd91d0/llk_lib/llk_math_matmul.h#L32-L38) every cycle (which involves 2048 individual multipliers, each 7b x 5b, followed by the equivalent of 2048 individual additions). To the left of Matrix is the Unpack unit, which moves values from memory (in a [variety of data formats](https://docs.tenstorrent.com/pybuda/latest/dataformats.html), including some block-float ones) into `SrcA` and `SrcB`, and then the Pack unit on the other side does the inverse: moving values from `Dst` back out to memory. Also of note is the Vector unit for performing 32-wide SIMD. This unit cannot directly access memory, but it can do transfers in both directions between `Dst` and the eight SIMD registers. This is suited to performing non-linear functions on the results of matrix multiplies prior to writing said results out to memory. The Matrix and Vector units are sometimes collectively called "Math". All of these units contain far more configuration parameters than can fit into a 32-bit instruction, so there are lots of configuration registers scattered about the place, along with Scalar and ThCfg units to help drive all this configuration. The Tensix Scalar unit also has a set of 64 32-bit GPRs per pipe, meaning that it contains more GPRs than all of the RISC-V cores in the tile do (3 times 64 versus 5 times 32).

The final row of the diagram I've labelled as "L0 ???", as the descriptions of several Tensix instructions mention an L0, but I'm not particularly confident as to its presence or size or functionality. If it exists, possibly it is a hardware-managed cache that all Tensix loads transparently go through, and Tensix stores can either target or skip and write directly to L1 (for when the stored values are less valuable than the pre-existing contents of the cache).

We can now look at some of the pieces in more detail.

## Tensix Instruction Pipe

Each of the three Tensix instruction pipes looks something like this:

![](https://www.corsix.org/images/tt-wh-part5-pipe.svg)

Tensix instructions enter at the top via two means. The conceptually simpler means is the MMIO box in the top right of the diagram; any "T" core can write a 32-bit value to address [`0xFFE40000`](https://github.com/tenstorrent/tt-metal/blob/63e042e27b5b41cc6a46cda27934c00fcf1e7de4/tt_metal/hw/inc/wormhole/tensix.h#L52) to push a Tensix instruction into the pipe associated with that core. Said instructions are 32 bits wide, [laid out as](https://github.com/tenstorrent/tt-llk-wh-b0/blob/abd3e70304bd24661ccd84c5f712243771cd91d0/common/inc/ckernel_ops.h#L12):

![](https://www.corsix.org/images/tt-wh-part5-insn-tensix.svg)

In contrast, 32-bit RISC-V instructions look totally different:

![](https://www.corsix.org/images/tt-wh-part5-insn-rv.svg)

The Tensix opcode is 8 bits wide, but [values ≥ `0xC0` aren't used](https://github.com/tenstorrent/tt-llk-wh-b0/blob/abd3e70304bd24661ccd84c5f712243771cd91d0/common/inc/ckernel_ops.h#L14), meaning that if a Tensix instruction is rotated left by two bits, it will never overlap with a 32-bit RISC-V instruction (it lands in the encoding space normally reserved for 16-bit RVC instructions, though not used for that purpose here):

![](https://www.corsix.org/images/tt-wh-part5-insn-tensix-rotated.svg)

This leads us to the box in the top left of the diagram: if a "T" core tries to execute an instruction whose low two bits are _not_ `0b11`, then the instruction bits will be rotated right by two and then treated as data to be written to the aforementioned `0xFFE40000`. Regardless of the means of entry, once a Tensix instruction has entered the pipe, RISC-V execution and Tensix execution proceed completely independently of each other.

Next up, we hit the Macro-Op Expander, which is where the [`MOP_CFG(u16 zhi)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L2953-L2968) and [`MOP(u1 template, u7 count1, u16 zlo)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L2924-L2951) instructions execute (instructions other than `MOP_CFG` and `MOP` flow through the Macro-Op Expander unchanged). Of these, `MOP_CFG` just stores the 16-bit immediate to a 16-bit register within the expander, whereas `MOP` is the really interesting one; it causes the expander to run through one of the following templates:

### Template 0

```
zmask = (zhi << 16) | zlo;
flags = mop_cfg[1];
for (i = 0; i <= count1; ++i) {
  if ((zmask & 1) == 0) {
    exec(mop_cfg[3]);
    if (flags & 0x02) {
      exec(mop_cfg[4]);
      exec(mop_cfg[5]);
      exec(mop_cfg[6]);
    }
    if (flags & 0x01) {
      exec(mop_cfg[2]);
    }
  } else {
    exec(mop_cfg[7]);
    if (flags & 0x01) {
      exec(mop_cfg[8]);
    }
  }
  zmask >>= 1;
}
```

### Template 1

```
i_count = mop_cfg[0] & 127;
j_count = mop_cfg[1] & 127;
j_inst = mop_cfg[5];
j_inst_flip = 0;
if (mop_cfg[6] != NOP) {
  j_inst_flip = j_inst ^ mop_cfg[6];
  j_count *= 2;
}
if (mop_cfg[2] == NOP && mop_cfg[3] != NOP) {
  if (i_count == 1 && j_count == 0) {
    i_count += 128; // Hardware bug
  }
}
for (i = 1; i <= i_count; ++i) {
  if (mop_cfg[2] != NOP) {
    exec(mop_cfg[2]);
  }
  for (j = 1; j <= j_count; ++j) {
    if (j != j_count) {
      exec(j_inst);
    } else if (i != i_count) {
      exec(mop_cfg[8]);
    } else {
      exec(mop_cfg[7]);
    }
    j_inst ^= j_inst_flip;
  }
  if (mop_cfg[3] != NOP) {
    exec(mop_cfg[3]);
    if (mop_cfg[4] != NOP) {
      exec(mop_cfg[4]);
    }
  }
}
```

Any call to `exec(x)` in the above causes the expander to _output_ the Tensix instruction `x`. In this way, a single `MOP` instruction expands to a somewhat programmable sequence of instructions. The programmability comes from the immediate operands to `MOP` and the values stored in the `mop_cfg` registers. For the latter, each "T" core can set the `mop_cfg` registers of its associated pipe by writing to the `uint32_t[9]` starting at address [`0xFFB80000`](https://github.com/tenstorrent/tt-metal/blob/7a2ca611093587f0fd26db12bea4e0f30585f7b8/tt_metal/hw/inc/wormhole/tensix.h#L71-L72).

Moving down a row in the diagram, we find a sneaky back door allowing the "B" core to inject Tensix instructions into any of the three pipes:

| "B" core MMIO address | Semantics of 32-bit write |
|---|---|
| [`0xFFE40000`](https://github.com/tenstorrent/tt-metal/blob/63e042e27b5b41cc6a46cda27934c00fcf1e7de4/tt_metal/hw/inc/wormhole/tensix.h#L52) | Push instruction into pipe associated with "T0" |
| [`0xFFE50000`](https://github.com/tenstorrent/tt-metal/blob/63e042e27b5b41cc6a46cda27934c00fcf1e7de4/tt_metal/hw/inc/wormhole/tensix.h#L53) | Push instruction into pipe associated with "T1" |
| [`0xFFE60000`](https://github.com/tenstorrent/tt-metal/blob/63e042e27b5b41cc6a46cda27934c00fcf1e7de4/tt_metal/hw/inc/wormhole/tensix.h#L54) | Push instruction into pipe associated with "T2" |

This allows the "B" core to [help initialize some of the state](https://github.com/tenstorrent/tt-metal/blob/7a2ca611093587f0fd26db12bea4e0f30585f7b8/tt_metal/hw/firmware/src/brisc.cc#L237-L251) within the various Tensix units prior the "T" cores being turned on, but it probably isn't intended for much more than this.

Moving down to the final row, we hit the Replay Expander, which is where [`REPLAY(u5 idx, u5 len, u2 mode)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L2971-L3002) instructions execute. The three possible modes of this instruction are:

*   _Record_: The next `len` instructions which enter the Replay Expander are swallowed up by the Replay Expander, and written to `buffer[idx:idx+len]`.
*   _Tee_: The next `len` instructions which flow through the Replay Expander are written to `buffer[idx:idx+len]` in addition to flowing through.
*   _Playback_: The Replay Expander _outputs_ `buffer[idx:idx+len]`, one instruction at a time.

When not in _Record_ mode, instructions other than `REPLAY` will flow through the Replay Expander unchanged (though the incoming stream is paused while _Playback_ is in progress).

## Tensix Sync

There are eight mutexes within this unit, each with four possible states:

*   Acquired by "T0" pipe
*   Acquired by "T1" pipe
*   Acquired by "T2" pipe
*   Released

Some instructions execute at Tensix Sync to manipulate these mutexes:

> [`ATGETM(u3 mutex_index)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L50-L83)
>
> If the specified mutex is already acquired by the pipe on which `ATGETM` appeared, does nothing. Otherwise, pauses said pipe until the mutex is released, and then atomically acquires it for said pipe and unpauses the pipe.
>
> [`ATRELM(u3 mutex_index)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L85-L96)
>
> If the specified mutex is already acquired by the pipe on which `ATRELM` appeared, then it is released. Otherwise, does nothing.

There are also eight semaphores within this unit, each having a four-bit counter value and a four-bit maximum value. Some instructions execute at Tensix Sync to manipulate these semaphores:

> [`SEMINIT(u4 max, u4 ctr, u8 which_sems_mask)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L141-L171)
>
> Set the counter value and the maximum value of the specified semaphores to the given values.
>
> [`SEMPOST(u8 which_sems_mask)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L173-L193)
>
> Increment the counter value of the specified semaphores, if not already equal to 15. Note that the upper limit is always 15; the maximum as set by `SEMINIT` is only used by `SEMWAIT`.
>
> [`SEMGET(u8 which_sems_mask)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L195-L215)
>
> Decrement the counter value of the specified semaphores, if not already equal to zero.
>
> [`SEMWAIT(u9 to_pause_mask, u8 which_sems_mask, u2 condition)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L217-L259)
>
> For as long as (any of) the specified semaphores have counter equal to zero (`condition == 1`) or have counter greater than or equal to their maximum (`condition == 2`), prevent the pipe on which `SEMWAIT` appeared from dispatching any instructions to the execution resources in `to_pause_mask`.

The "T" cores can also manipulate the semaphores via MMIO:

*   [Reading from `0xFFE80020 + 4*i`](https://github.com/tenstorrent/tt-llk-wh-b0/blob/3457491ab21aecd4325851c2607c35582f89e111/common/inc/ckernel.h#L143-L146) gives the counter value of semaphore `i`.
*   [Writing 0 to `0xFFE80020 + 4*i`](https://github.com/tenstorrent/tt-llk-wh-b0/blob/3457491ab21aecd4325851c2607c35582f89e111/common/inc/ckernel.h#L148-L151) does what `SEMPOST(1u << i)` would do.
*   [Writing 1 to `0xFFE80020 + 4*i`](https://github.com/tenstorrent/tt-llk-wh-b0/blob/3457491ab21aecd4325851c2607c35582f89e111/common/inc/ckernel.h#L153-L156) does what `SEMGET(1u << i)` would do.

One final instruction executes at Tensix Sync:

> [`STALLWAIT(u9 to_pause_mask, u15 condition_mask)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L98-L139)
>
> Similar to `SEMWAIT`, but waits while (any of) assorted non-semaphore conditions are met. Said conditions can include various execution resources being busy, SrcA or SrcB being valid, and SrcA or SrcB being clear.

Any instructions not yet described will flow through Tensix Sync to one of the backend execution resources, though that flow can be paused while `ATGETM` or `SEMWAIT` or `STALLWAIT` are in progress.

## Tensix Scalar (ThCon)

This unit contains 3x 64x 32-bit GPRs, the roles for which are [typically statically assigned](https://github.com/tenstorrent/tt-llk-wh-b0/blob/3457491ab21aecd4325851c2607c35582f89e111/common/inc/ckernel_gpr_map.h). Instructions manipulate the set of 64 GPRs corresponding to the pipe from which the instruction originally came. Each "T" core can also access its register set via MMIO to the `uint32_t[64]` starting at address [`0xFFE00000`](https://github.com/tenstorrent/tt-metal/blob/7a2ca611093587f0fd26db12bea4e0f30585f7b8/tt_metal/hw/inc/wormhole/tensix.h#L45-L47).

Various ALU-style operations execute here to manipulate these GPRs:

> [`SETDMAREG(u16 value, u1 mode, u6 gpr_idx, u1 lo_hi)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1389-L1440)
>
> Sets the low 16 bits (`lo_hi == 0`) or high 16 bits (`lo_hi == 1`) of the specified GPR to the specified value, leaving the other bits unchanged. Does something totally different if `mode == 1`; consult the YAML for details.
>
> [`ADDDMAREG(u1 b_is_const, u6 gpr_out, u6 b, u6 gpr_a)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1700-L1726)
>
> Does `gpr_out = gpr_a + (b_is_const ? b : gprs[b])`.
>
> [`SUBDMAREG(u1 b_is_const, u6 gpr_out, u6 b, u6 gpr_a)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1728-L1737)
>
> Does `gpr_out = gpr_a - (b_is_const ? b : gprs[b])`.
>
> [`MULDMAREG(u1 b_is_const, u6 gpr_out, u6 b, u6 gpr_a)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1739-L1748)
>
> Does `gpr_out = (gpr_a & 0xFFFF) * (b_is_const ? b : (gprs[b] & 0xFFFF))`.
> Note only low 16 bits of each input are used.
>
> [`BITWOPDMAREG(u1 b_is_const, u2 op, u6 gpr_out, u6 b, u6 gpr_a)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1750-L1783)
>
> Does `gpr_out = gpr_a &|^ (b_is_const ? b : gprs[b])`,
> where `&|^` is `&` (`op == 0`) or `|` (`op == 1`) or `^` (`op == 2`).
>
> [`CMPDMAREG(u1 b_is_const, u2 op, u6 gpr_out, u6 b, u6 gpr_a)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1816-L1848)
>
> Does `gpr_out = gpr_a <==> (b_is_const ? b : gprs[b])`,
> where `<==>` is `<` (`op == 1`) or `==` (`op == 2`) or `>` (`op == 0`).
>
> [`SHIFTDMAREG(u1 b_is_const, u1 op, u6 gpr_out, u6 b, u6 gpr_a)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1785-L1814)
>
> Does `gpr_out = gpr_a <<>> (b_is_const ? b : gprs[b])`,
> where `<<>>` is `<<` (`op == 0`) or `>>` (`op == 1`).

Then instructions to move between these GPRs and L0/L1:

> [`LOADIND(u2 sz, u6 gpr_ofs, u1 lo_hi, u2 inc, u6 gpr_data, u6 gpr_base)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1509-L1546)
>
> Loads from L1 to GPRs.
> The L1 address is `gpr_base*16 + ((gpr_ofs >> (lo_hi*16)) & 0xFFFF)`.
> Various size modes:
>
> *   `sz == 3`: Load 8 bits (high 24 bits of `gpr_data` unchanged).
> *   `sz == 2`: Load 16 bits (high 16 bits of `gpr_data` unchanged).
> *   `sz == 1`: Load 32 bits.
> *   `sz == 0`: Load 128 bits (to four GPRs starting at `gpr_data & 0x3c`).
>
> Also various options for incrementing after the load:
>
> *   `inc == 0`: No auto-increment.
> *   `inc == 1`: Increment the low/high 16 bits of `gpr_ofs` by 2.
> *   `inc == 2`: Increment the low/high 16 bits of `gpr_ofs` by 4.
> *   `inc == 3`: Increment the low/high 16 bits of `gpr_ofs` by 16.
>
> [`STOREIND(u1 l1, u2 sz, u6 gpr_ofs, u1 lo_hi, u2 inc, u6 gpr_data, u6 gpr_base)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L2034-L2078)
>
> Stores from GPRs to L0/L1.
> Other than the extra `l1` operand, all operands as per `LOADIND`.
>
> [`ATSWAP(u1 l1, u8 ofs_mask, u6 gpr_data, u6 gpr_base)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1966-L1990)
>
> Does an atomic swap between GPRs and L0/L1 of up to 128 bits.
> The L1 address is `gpr_base*16`. Four GPRs starting at `gpr_data & 0x3c` give 128 bits, which are partially swapped with the 128 bits at the L1 address: if bit `i` of `ofs_mask` is set, then bits `i*16` through `i*16+15` are swapped.
>
> [`ATCAS(u1 l1, u4 set_val, u4 cmp_val, u2 ofs, u6 gpr_base)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1992-L2032)
>
> Does an atomic compare/set against L0/L1. The logic is along the lines of:
>
> ```
> uint32_t *word = gpr_base*16 + ofs*4;
> retry:
> atomic {
>   if (*word != cmp_val) {
>     goto retry; // Comparison failed
>   }
>   *word = set_val;
> }
> ```
>
> [`ATINCGET(u1 l1, u5 len, u2 ofs, u6 gpr_data, u6 gpr_base)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1883-L1916)
>
> Does an atomic increment against L0/L1. The logic is along the lines of:
>
> ```
> uint32_t *word = gpr_base*16 + ofs*4;
> uint32_t incr_mask = (1u << (len + 1)) - 1;
> atomic {
>   uint32_t incremented = *word + gpr_data;
>   gpr_data = *word;
>   *word = (incremented & incr_mask) | (*word &~ incr_mask);
> }
> ```
>
> [`ATINCGETPTR(u1 l1, u1 no_incr, u5 incr_log2, u4 len, u2 ofs, u6 gpr_data, u6 gpr_base)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L1918-L1964)
>
> Does an atomic FIFO operation against L0/L1. The logic is along the lines of:
>
> ```
> struct fifo_ctl_t {
>   uint32_t rd;
>   uint32_t wr;
>   uint32_t pad[2];
> } *fifo = gpr_base*16;
> uint32_t *word = gpr_base*16 + ofs*4;
> uint32_t fifo_capacity = 1u << (len - 1);
> uint32_t fifo_mask = (1u << len) - 1;
> retry:
> atomic {
>   if (ofs & 1) {
>     uint32_t fifo_size = (fifo->wr - fifo->rd) & fifo_mask;
>     if (fifo_size == fifo_capacity) {
>       goto retry; // Cannot write to full FIFO
>     }
>   } else {
>     if (fifo->rd == fifo->wr) {
>       goto retry; // Cannot read from empty FIFO
>     }
>   }
>   uint32_t incremented = *word + (!no_incr << incr_log2);
>   gpr_data = *word;
>   *word = (incremented & fifo_mask) | (*word &~ fifo_mask);
> }
> ```

Two instructions move between GPRs and the 1 MiB range of address space starting at `0xFFB00000`, though they cannot access the 2 KiB / 4 KiB core-local RAMs within this range:

> [`LOADREG(u6 gpr_data, u18 ofs)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L2096-L2110)
>
> Does `gpr_data = *(0xFFB00000 | (ofs << 2))`.
>
> [`STOREREG(u6 gpr_data, u18 ofs)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L2080-L2094)
>
> Does `*(0xFFB00000 | (ofs << 2)) = gpr_data`.

## Configuration Registers

There are two broad categories of configuration registers:

1.  [261 per-pipe registers](https://github.com/tenstorrent/tt-metal/blob/c82f308f19c98b88feb759d174e6213191c3ac1f/tt_metal/hw/inc/wormhole/wormhole_b0_defines/cfg_defines.h#L20-L1329), each of which being between 1 and 16 bits wide, packed into 57x 16b per pipe (so 3x 57x 16b total). A packed 16b group is set using the [`SETC16(u6 idx, u16 val)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L2843-L2864) instruction, which executes on the ThCfg unit. I have not found any MMIO region exposing these registers. Contents includes:
    *   `CFG_STATE_ID::StateID`
    *   `DEST_TARGET_REG_CFG_MATH::Offset`
    *   `ADDR_MOD_SET::Base`
    *   `ADDR_MOD_{AB, DST, PACK, BIAS}_SEC[0-7]::*`
    *   `SRCA_SET::{Base, SetOvrdWithAddr}`
    *   `SRCB_SET::Base`
    *   `CLR_DVALID::{SrcA, SrcB}_Disable`
    *   `FIDELITY_BASE::Phase`
    *   `UNPACK_MISC_CFG::CfgContext{Offset, CntReset, CntInc}[01]`
    *   `NOC_OVERLAY_MSG_CLEAR::{StreamId, MsgNum}_[01]`
    *   `CG_CTRL_{EN, KICK}::*`
    *   `PERF_CNT_CMD::Cmd[0-3]{Start, Stop}`
    *   `ENABLE_ACC_STATS::Enable`
    *   `FPU_BIAS_SEL::Pointer`
    *   `FP16A_FORCE::Enable`
2.  248+26+39+174 unit-specific registers, each of which being between 1 and 32 bits wide, packed into (72+14+8+28)x 32b. There are two copies of each of these registers, with the per-pipe `CFG_STATE_ID::StateID` configuration register determining which copy is in use by a given pipe. Both copies are accessible via MMIO from the "B" or "T" cores, the 1st as `uint32_t[188]` at [`0xFFEF0000`](https://github.com/tenstorrent/tt-metal/blob/7a2ca611093587f0fd26db12bea4e0f30585f7b8/tt_metal/hw/inc/wormhole/tensix.h#L68-L69), and the 2nd as `uint32_t[188]` at [`0xFFEF02F0`](https://github.com/tenstorrent/tt-metal/blob/62aeb394caf3080e57ec4f9930dcb3a0fd813b40/tt_metal/hw/inc/wormhole/c_tensix_core.h#L38). A packed 32b group can be moved to / from a Tensix Scalar GPR using the [`RDCFG(u6 gpr, u8 idx)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L2820-L2841) / [`WRCFG(u6 gpr, u1 wr128, u8 idx)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L2795-L2818) instructions, and 8b-aligned subgroups can be manipulated using the [`RMWCIB[0-3](u8 mask, u8 bits, u8 idx)`](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml#L2866-L2921) instructions.

## General shape of low-level kernels

What we've seen so far should make [Tenstorrent's low-level-kernels](https://github.com/tenstorrent/tt-llk-wh-b0/tree/3457491ab21aecd4325851c2607c35582f89e111/llk_lib) _slightly_ more scrutable. Each LLK has an init step which configures the Macro-Op Expander and the Replay Expander and the Tensix Scalar GPRs and the relevant configuration registers, and then a runtime step which takes advantage of all that pre-programming. These LLKs are wrapped by things in [Metalium's `llk_api` directory](https://github.com/tenstorrent/tt-metal/tree/7a2ca611093587f0fd26db12bea4e0f30585f7b8/tt_metal/hw/ckernels/wormhole_b0/metal/llk_api), which in turn are wrapped by things in [Metalium's `compute_kernel_api` directory](https://github.com/tenstorrent/tt-metal/tree/7a2ca611093587f0fd26db12bea4e0f30585f7b8/tt_metal/include/compute_kernel_api), which is the API that developers are _meant_ to use.

The LLKs make use of various instructions not yet covered; you'll have to consult [the mostly-accurate YAML file outlining every instruction](https://github.com/tenstorrent/tt-budabackend/blob/58fab9cd7ac53176363fc3ee61d40f434778c964/src/meta/wormhole_b0/instructions/yaml/assembly.yaml), or the [C header generated from that YAML](https://github.com/tenstorrent/tt-llk-wh-b0/blob/abd3e70304bd24661ccd84c5f712243771cd91d0/common/inc/ckernel_ops.h) for further details. The general pattern of that header is that `TT_OP_X(...)` generates the encoding of instruction `X` (e.g. for later MMIO use), `TT_X(...)` generates the encoding of `X` and immediately does an MMIO write to push it into the instruction pipe, and `TTI_X(...)` uses the T6 as RVC trick to generate the encoding of `X` and splat it into the RISC-V instruction stream (so `TTI_X` can be used instead of `TT_X` when all the operands are compile-time constants).

An obvious next step would be dissecting a matrix multiplication kernel to describe how it orchestrates the Unpack and Matrix and Pack units, but this post is long enough already, so it'll have to wait for another time. That wraps up part 5; if you're reading along, then [part 6](https://www.corsix.org/content/tt-wh-part6) is next.

## Capture Notes

- The most architecturally dense post in the series. Captured fully.
- Tensix instruction definitions are heavily linked to specific lines in tt-budabackend `assembly.yaml` — preserved.
- Configuration register bullet lists abridged in source where the original used `{...}` shorthand — preserved as-is.
- Image references include several SVG diagrams of T-tile internal structure.
