---
type: source
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, source, blog, sfpu]
source_path: raw/2026-05-05__blog__corsix-tt-wh-part6-vector-isa.md
evidence_level: blog
---

# Source — corsix Part 6: Vector Instruction Set

## Why it matters

The **most complete reference for the [[SFPU]] (Tensix Vector) instruction set** outside Tenstorrent's source tree. Used as the basis for the SFPU concept page. Where TT-Metal exposes `sin_tile()`, the underlying machine ops live here.

## Key facts

- Tensix Vector = 32-lane, 32-bit SIMD. Lane viewed as fp32, int32, or signmag32 depending on instruction.
- 8 vector regs `L0`–`L7`; 4 fixed constants (0.0, 1.0, 0.8373, lane#×2); 4 programmable constants (8 lanes × 32 b); 32-lane × 1-bit per-lane flags + flag stack (up to 8 entries).
- 32-lane LFSR PRNG state (for stochastic rounding) — quality is poor (30/32 bits shared between adjacent lanes).
- `Dst` register (in Tensix Matrix area) is the only memory the SFPU reaches via `SFPLOAD`/`SFPSTORE` (4 rows × 16 lanes per access).
- **No fp32 subtract instruction** — use `SFPMAD` with VB=−1.0.
- **No FMA negation modifiers** — fixed in Blackhole.
- `SFPLUT` / `SFPLUTFP32` — 3- or 6-entry piecewise-linear LUT for unary functions.
- `SFPTRANSP` — 8×8 transpose across L0–L3 (and L4–L7), implemented (likely) by re-indexing storage banks.
- Most arithmetic instructions are 2-cycle (require an `SFPNOP` if next instruction would consume the result).

## Technical details

**Architecture:** captures the full opcode list for SFPU + the 6 instruction-encoding families (Mod0/Mod1).

**Memory:** SFPU does not access L1 directly. Data flows L1 → Unpack → SrcA/SrcB → Matrix → Dst → SFPU → Dst → Pack → L1.

**Compiler / runtime:** SFPI (separate repo `tenstorrent/sfpi`) is the userspace toolchain. The `sfpi-gcc` fork knows about the 2-cycle latency and inserts `SFPNOP`s as needed.

## Related pages

- [[SFPU]], [[Tensix]], [[Matrix Unit]], [[Tile-Based Execution]]

## Open questions

- Stochastic-rounding PRNG quality is poor; would workloads relying on it benefit from a software xorshift instead? (Research direction — not pursued here.)
- The four `SFPLUTFP32` mode tables (FP16_3ENTRY, FP32_3ENTRY, FP16_6ENTRY1/2) were abridged during capture — re-fetch source HTML if the LUT mode internals become research-relevant.
