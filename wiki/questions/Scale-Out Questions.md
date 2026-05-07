---
type: question
status: needs-source
created: 2026-05-06
updated: 2026-05-06
tags: [tenstorrent, wormhole, scale-out, questions]
evidence_level: unknown
---

# Scale-Out Questions

## Q15. What does TT-Fabric do for routing and failure handling?

- Why it matters: multi-host scale-out is present in the official story but not yet technically grounded in this vault.
- Evidence needed: TT-Fabric architecture docs or firmware notes.
- Related pages: [[concepts/Multi-ASIC Addressing|Multi-ASIC Addressing]], [[architecture/Wormhole|Wormhole]]

## Q16. How does broadcast cost scale with destination shape?

- Why it matters: reservation and routing overhead may be a hidden systems bottleneck in scale-out or multi-core communication.
- Evidence needed: routing-path docs or experiment.
- Related pages: [[architecture/NoC|NoC]], [[concepts/Multi-ASIC Addressing|Multi-ASIC Addressing]]
