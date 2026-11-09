# A RISC-V Simulator for the Tenstorrent Tensix Architecture

## Source metadata

- Source URL: https://arxiv.org/abs/2611.04740v1
- Published: 2026-11-03
- Collected: 2026-11-09T14:12:13+00:00
- Collector: weekly_source_collect.py
- Source bucket: paper_metadata
- Evidence hint: paper
- Authors: Nick Brown, Daniyal Arshad

## Summary snippet

RISC-V based AI accelerators have become popular and not only for AI and ML, but also as vehicles
for exploring HPC workloads more generally. Tenstorrent are one example, and whilst they document
their Tensix architecture in detail and develop their software stack openly, running code has
historically required a physical card, and their recently released simulator targets hardware
equivalence rather than introspection. In this paper we present Wolfpine, a community developed
RISC-V simulator for the Tensix architecture, supporting both the Wormhole and Blackhole generations
and integrating seamlessly with the TT-Metal software stack. Constructed entirely from publicly
available documentation, open source software and measurements on physical hardware, Wolfpine is
written in pure Python for readability and ease of modification. An opt-in, provenance-tracked cost
model adds timing fidelity incrementally, and typed event streams, per-component tracing and
timeline export enable programmers to identify and diagnose performance bottlenecks that the
hardware itself hides.
