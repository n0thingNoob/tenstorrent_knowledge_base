---
title: "Tenstorrent Wormhole Series Part 3: NoC propagation delay"
source_type: "blog"
original_url: "https://www.corsix.org/content/tt-wh-part3"
repository: "unknown"
commit_or_version: "blog post dated 2024-09-08"
fetched_at: "2026-05-05"
status: "captured"
license: "unknown"
tags:
  - tenstorrent
  - wormhole
---

# Tenstorrent Wormhole Series Part 3: NoC propagation delay

Source URL: https://www.corsix.org/content/tt-wh-part3
Captured at: 2026-05-05
Status: captured

## Source Content

Posted at [corsix.org](https://www.corsix.org/) on September 8, 2024

Continuing the trend from [part 2](https://www.corsix.org/content/tt-wh-part2) of eschewing the useful software layers provided by Tenstorrent, and instead manually poking around in various address spaces, every T tile contains a 64-bit counter at tile-local address [`0xFFB121F0` and `0xFFB121F8`](https://github.com/tenstorrent/tt-metal/blob/6d468cd6541380cce6b38f738e739de7bb448a44/tt_metal/hw/inc/wormhole/tensix.h#L145-L146) which starts at zero when the chip is powered on, and increments by one every clock cycle. Every T tile also contains a soft-reset register at tile-local address [`0xFFB121B0`](https://github.com/tenstorrent/tt-metal/blob/6d468cd6541380cce6b38f738e739de7bb448a44/tt_metal/hw/inc/wormhole/tensix.h#L107); if this register contains [`0x47800`](https://github.com/tenstorrent/tt-umd/blob/3db6c02db250845384fc95fd7406cb2865722457/device/tt_silicon_driver_common.hpp#L27-L31) then all five Baby RISC-V cores are held in soft reset, and then individual bits can be cleared to take individual cores out of soft reset (i.e. allow them to run).

With these two pieces of information, we can do something interesting: use a NoC multicast write to take one core out of reset on every tile, have RISC-V code on every tile record its cycle counter somewhere as soon as it comes out of reset, then collect and plot the results.

In order to start from a clean slate, we'll want to use a NoC multicast write to put all cores into soft-reset, specifying (0, 0) through (9, 11) inclusive as the multicast rectangle, and relying on the multicast disable row/column we saw in [part 2](https://www.corsix.org/content/tt-wh-part2) to ensure that the multicast only goes to T tiles:

```c
#define RV_ADDR_SOFT_RESET 0xFFB121B0

#define SOFT_RESET_ALL_CORES 0x47800

char* reg_tlb = set_tlb(dev, TLB_IDX_UC0, TLB_CFG_MULTICAST(0, 0, 9, 11), RV_ADDR_SOFT_RESET);
*(volatile uint32_t*)(reg_tlb + RV_ADDR_SOFT_RESET) = SOFT_RESET_ALL_CORES;
```

With all the cores held in soft-reset, it is safe to send them new code. The SRAM (or, for D tiles, DRAM) within a tile starts at tile-local address 0, and execution will also start at address 0 when soft-reset is cleared, so we can send some RISC-V code to tile-local addresses starting at 0, again multicasting it out. The code will read from the tile-local 64-bit cycle counter at `0xFFB121F0` and `0xFFB121F8`, then write it to tile-local address `128`:

```c
const uint32_t rv_code[] = {
  0xFFB12537, // lui a0, 0xFFB12
  0x1F052583, // lw a1, 0x1F0(a0)
  0x1F852603, // lw a2, 0x1F8(a0)
  0x08B02023, // sw a1, 128(x0)
  0x08C02223, // sw a2, 132(x0)
  0x0000006F, // loop: j loop
};
char* l1_tlb = set_tlb(dev, TLB_IDX_0, TLB_CFG_MULTICAST(0, 0, 9, 11), 0);
memcpy(l1_tlb, rv_code, sizeof(rv_code));
```

We can then perform a multicast to bring one core out of reset on each T tile:

```c
*(volatile uint32_t*)(reg_tlb + RV_ADDR_SOFT_RESET) = SOFT_RESET_ALL_CORES & (SOFT_RESET_ALL_CORES - 1);
```

We can't use multicast to collect the results - instead we need to perform a unicast read against each T tile in turn. That requires knowing the tile coordinates of each T tile, and said grid isn't entirely regular: it'll be disturbed by a column of D tiles, and be disturbed by a row of E tiles, and have one or two disabled rows. We can sidestep this problem by using a [convenient translation feature](https://github.com/tenstorrent/tt-umd/blob/3db6c02db250845384fc95fd7406cb2865722457/src/firmware/riscv/wormhole/noc/noc_parameters.h#L136-L144): an X coordinate of 16 will be replaced with 0 (PCIe / ARC / D column), 17 will be replaced with 5 (2nd D column), then 18 through 25 will be replaced with the column indices containing T tiles. Similarly, a Y coordinate of 16 will be replaced with 0 (E0-E7 row), 17 will be replaced with 6 (E8-E15 row), and 18 through 25 or 26 will be replaced with whatever row indices contain active T tiles (if you need a reminder of the coordinate grid, see [part 1](https://www.corsix.org/content/tt-wh-part1)). This allows us to easily iterate over the active T tiles:

```c
uint64_t times[8][8];
for (uint32_t y = 0; y < 8; ++y) {
  for (uint32_t x = 0; x < 8; ++x) {
    l1_tlb = set_tlb(dev, TLB_IDX_0, TLB_CFG_UNICAST(18 + x, 18 + y), 0);
    times[y][x] = *(volatile uint64_t*)(l1_tlb + 128);
  }
}
```

For neatness, we can then put everything back into reset:

```c
*(volatile uint32_t*)(reg_tlb + RV_ADDR_SOFT_RESET) = SOFT_RESET_ALL_CORES;
```

With `T` denoting the minimum value seen in the `times` matrix, I observe:

![](https://www.corsix.org/images/tt-wh-part3-times-0.svg)

If instead multicasting via NoC #1 (by adding `TLB_CFG_NOC1` to the `TLB_CFG_MULTICAST` result), and calling `S` the minimum value seen this time, I observe:

![](https://www.corsix.org/images/tt-wh-part3-times-1.svg)

Both sets of measurements suggest that the tile-to-tile propagation delay might be around 9 cycles, but the numbers are far from perfect. The imperfections are very clear if we plot both sets of measurements at the same time, and look at just the row containing the PCIe tile:

![](https://www.corsix.org/images/tt-wh-part3-onerow-times.svg)

Going rightwards, the first tile is "T+3" and the last is "T+75", meaning 72 cycles to traverse 8 tiles. Going leftwards, the first tile is "S+0" and the last is "S+72", again meaning 72 cycles to traverse 8 tiles. However, going rightwards, the 2nd tile is "T+0", which isn't great: taken at face value it would mean that the multicast reached the 2nd tile before reaching the first, which is clearly nonsense. There is one obvious explanation for this: the cycle counters on different tiles aren't perfectly aligned - they're _meant_ to all start from 0 when the chip powers on, but powering on is a physically complex process, so some tiles might start counting a few cycles before or after others.

If the tile-to-tile latency was identical for every hop, and we called this unknown quantity X, then what we'd hope to see is:

![](https://www.corsix.org/images/tt-wh-part3-onerow-algebra.svg)

Regardless of what S or T or X actually are, it so happens that the average of the two expressions in each tile is `(S + T)/2 + 4X`. As this expression should be the same for all tiles, we can use it to correct for the different counter start times between the different tiles. We need to assume that there is a per-tile counter adjustment, with all readings taken on a given tile adjusted by the same amount, and then set those adjustments so that "should be the same" becomes "is the same". Because I'm lazy, I'll assume that all tiles within a given column have the same adjustment, which isn't quite true, but it'll do for now. After computing and applying this adjustment, the NoC #0 measurements are:

![](https://www.corsix.org/images/tt-wh-part3-times-0b.svg)

And NoC #1 are:

![](https://www.corsix.org/images/tt-wh-part3-times-1b.svg)

The results still aren't perfect, but they're good enough for me to conclude that the tile-to-tile propagation delay is 9 clock cycles (i.e. 9 nanoseconds when the clock is running at 1GHz), and that imperfections in measurements are due to the aforementioned laziness. For tile-to-tile communication there'll be some latency to get on to the NoC, then a propagation delay for every traversed tile, and then some latency to get off the NoC. For messages requiring a response, there'll be all that twice, as after the request has done all that, the response needs to get on to the NoC, then propagate back to the requestor, then get off the NoC. For NoC reads (and presumably NoC writes-with-acknowledgement, if you use them), that response travels on the same NoC as the request, so if requestee and respondee are in the same row, the combination of request and response will have 10 tiles (90 cycles) of propagation delay, versus 12 tiles (108 cycles) of propagation delay if they're in the same column, and 10+12 tiles (198 cycles) if they're in different row and column.

That wraps up part 3. The [complete code](https://gist.github.com/corsix/07760dc4a0a62d7a51aed77e0058861c) comes out to 164 lines, but a lot of it is common with [part 2](https://www.corsix.org/content/tt-wh-part2)'s 100 lines. If you're reading along, [part 4](https://www.corsix.org/content/tt-wh-part4) is next.

## Capture Notes

- Images preserved with absolute URLs.
- All RISC-V machine-code listings preserved verbatim including disassembly comments.
- Cross-reference to tile-local registers `0xFFB121F0`/`0xFFB121F8` (cycle counter) and `0xFFB121B0` (soft-reset) is core architectural data.
- Linked gist `07760dc4a0a62d7a51aed77e0058861c` not fetched separately — candidate for future capture.
