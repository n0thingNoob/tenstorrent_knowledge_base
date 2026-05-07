---
type: question
status: needs-source
created: 2026-05-06
updated: 2026-05-06
tags: [tenstorrent, wormhole, architecture, questions]
evidence_level: unknown
---

# Architecture Questions

## Q1. Does Tensix "L0" exist? If so, what is it?

- Why it matters: Several Tensix instruction descriptions reference L0/L1, but the current corpus does not confirm presence, size, or semantics.
- Evidence needed: deeper tt-isa subpages such as `L1.md` or scalar-unit documentation; possibly measurement.
- Related pages: [[architecture/Tensix|Tensix]], [[architecture/L1 Memory|L1 Memory]]

## Q2. Are "4 Packers" and "1 Pack unit" the same hardware viewed differently?

- Why it matters: official and reverse-engineered descriptions disagree on presentation, which affects how we talk about backend resources.
- Evidence needed: official packer subpage in tt-isa.
- Related pages: [[architecture/Tensix|Tensix]], [[architecture/Matrix Unit|Matrix Unit]]

## Q3. How large is per-tile cycle-counter skew at power-on?

- Why it matters: cross-tile cycle comparison becomes noisy without a model of skew.
- Evidence needed: official statement or a direct measurement experiment.
- Related pages: [[architecture/Wormhole|Wormhole]], [[architecture/NoC|NoC]]

## Q4. What is the exact multiplier scheduling for HiFi3 and HiFi4?

- Why it matters: current understanding is inferred and affects fidelity-stage modeling.
- Evidence needed: matrix-engine tech report or lower-level official documentation.
- Related pages: [[concepts/Fidelity Stages|Fidelity Stages]], [[architecture/Matrix Unit|Matrix Unit]]
