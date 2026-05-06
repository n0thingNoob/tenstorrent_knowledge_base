---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags: [tenstorrent, wormhole, sfpu, vector]
evidence_level: official
---

# SFPU

## Summary

**SFPU** (Special Function Processing Unit) is the **Tensix Vector unit**: a 32-lane × 32-bit SIMD engine inside each [[Tensix]] tile. Distinct from the [[Matrix Unit]] (FPU). Per [[Source - corsix Part 6 — Vector ISA]]:

> "Tensix Unpack/Matrix/Pack are like tensor cores, whereas Tensix Vector is like CUDA cores."

Used for non-linear functions, dropout, cumsum, normalisation tail-ops — anything not a linear-MAC matrix operation.

## Resources per Tensix

| Resource | Size |
|---|---|
| Vector regs `L0`–`L7` | 8 × (32 lanes × 32 b) |
| Fixed constants | 4 × 32 b (e.g. 0.0, 1.0, 0.8373, lane#×2) |
| Programmable constants | 4 × 8 lanes × 32 b (set via `SFPCONFIG`) |
| Per-lane flags | 32 × 1 b + active flag |
| Flag stack | up to 8 entries, each (1 + 32) b |
| PRNG | 32-lane LFSR (low-quality — 30/32 bits shared between lanes; 31/32 bits shared between consecutive draws) |
| `Dst` access | via `SFPLOAD` / `SFPSTORE` (4 rows × 16 lanes per access) |

## Instruction families

- Int32 + bitwise: `SFPIADD`, `SFPAND/OR/XOR/NOT`, `SFPLZ`, `SFPABS`, `SFPSHFT`, `SFPSHFT2`, `SFPSETCC`
- Flag stack: `SFPENCC`, `SFPPUSHC`, `SFPCOMPC`, `SFPPOPC`
- Fp32 field manipulation: `SFPEXEXP`, `SFPEXMAN`, `SFPSETSGN`, `SFPSETEXP`, `SFPSETMAN`, `SFPDIVP2`
- Fp32 arithmetic: `SFPMUL`, `SFPADD`, `SFPMAD` (fused), `SFPMULI`, `SFPADDI`, `SFPLUT`, `SFPLUTFP32`
- Min/max/swap: `SFPSWAP` (with min/max mode for total-ordering compare)
- Type conversions: `SFPSTOCHRND`, `SFPCAST`
- Constants: `SFPLOADI`, `SFPCONFIG`
- Cross-lane data movement: `SFPMOV`, `SFPSHFT2` (rotate/shift), `SFPTRANSP` (8×8 transpose)
- Dst transfer: `SFPLOAD`, `SFPSTORE`, `SFPLOADMACRO`

## Notable design choices

- No fp32 subtract; achieved by `SFPMAD` with VB = `-1.0`.
- No multiply-add negation variants — flagged as a Wormhole quirk fixed in Blackhole.
- `SFPLUTFP32` provides 3- or 6-entry piecewise-linear LUTs (FP16 / FP32 modes) for unary function approximation.
- `SFPTRANSP` does an 8×8 transpose across L0–L3 (and L4–L7) — likely implemented by re-indexing the underlying 8-lane × 32 b storage banks rather than physical data movement.

## Comparison with Matrix Unit

| | Matrix Unit (FPU) | Vector Unit (SFPU) |
|---|---|---|
| Width | 2048 multipliers | 32 lanes × 32 b |
| Operands | `SrcA`, `SrcB`, `Dst` | `L0`-`L7`, `Dst` |
| Memory access | none direct (Unpack/Pack handle it) | none direct; `SFPLOAD/STORE` use `Dst` only |
| Workload | linear (MAC) | non-linear scalar functions per element |

## Related pages

- [[Tensix]], [[Matrix Unit]], [[L1 Memory]], [[Tile-Based Execution]], [[Programming Model]]

## Sources

- `raw/2026-05-05__blog__corsix-tt-wh-part6-vector-isa.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part5-t-tiles.md`
- `raw/2026-05-05__blog__corsix-tt-wh-part7-matmul.md`
