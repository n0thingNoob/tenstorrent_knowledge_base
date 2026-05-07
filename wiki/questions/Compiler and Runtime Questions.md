---
type: question
status: needs-source
created: 2026-05-06
updated: 2026-05-06
tags: [tenstorrent, wormhole, compiler, runtime, questions]
evidence_level: unknown
---

# Compiler and Runtime Questions

## Q9. What are the actual responsibilities of the TT-MLIR dialects?

- Why it matters: TT-MLIR is currently the shallowest major area in the vault.
- Evidence needed: tt-mlir docs site and repo `docs/`.
- Related pages: [[toolchain/TT-MLIR|TT-MLIR]], [[toolchain/Compiler Stack|Compiler Stack]]

## Q10. Is there an auto-tuner or cost model in the stack?

- Why it matters: sharding, fidelity, and placement choices currently look hand-tuned in user-facing APIs.
- Evidence needed: TT-MLIR or runtime docs.
- Related pages: [[toolchain/Programming Model|Programming Model]], [[toolchain/Compiler Stack|Compiler Stack]]

## Q11. How is fast dispatch actually structured internally?

- Why it matters: dispatch overhead and firmware structure are likely relevant to runtime and systems work.
- Evidence needed: `tt_metal/impl/dispatch/` and comparison against slow-dispatch paths.
- Related pages: [[toolchain/TT-Metal|TT-Metal]]
