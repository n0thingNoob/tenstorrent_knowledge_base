# Purpose

This vault exists to turn raw Tenstorrent Wormhole material into a durable research wiki that helps surface high-value, measurable research ideas.

## Primary objective

Identify research opportunities that are specific enough to Wormhole and its software stack to be worth pursuing, especially in:

- synchronization and producer-consumer protocols
- NoC behavior, routing, and communication cost
- data movement and L1 / circular-buffer usage
- compiler/runtime boundaries across TT-MLIR, TT-NN, and TT-Metal
- CGRA/dataflow interpretations of Wormhole and where that analogy breaks
- bottlenecks that can be measured, modeled, or optimized

## What counts as a strong lead

A strong lead usually has all of the following:

- evidence in official docs, source code, or experiment logs
- a concrete mechanism, mismatch, or bottleneck
- a clear reason it matters on Wormhole specifically
- a plausible validation path through code reading or experiment

## What this vault should optimize for

- fewer, better pages over broad coverage
- source traceability and explicit uncertainty
- reusable synthesis rather than one-off answers
- questions and ideas that can turn into experiments

## Immediate standing questions

- What synchronization paths in TT-Metal could collapse from two-step handshakes into atomic-counter protocols?
- Which compiler/runtime decisions are explicit today, and which are still hidden in undocumented layers?
- Where do NoC and L1 constraints show up as user-visible or compiler-visible bottlenecks?
