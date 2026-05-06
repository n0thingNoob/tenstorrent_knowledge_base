# AGENTS.md

This repository is an Obsidian-compatible research knowledge base for **Tenstorrent Wormhole**. It is focused on architecture, hardware behavior, software stack, compiler/toolchain, programming model, simulation, performance analysis, and research-idea discovery.

Codex's role is to act as a disciplined research assistant and wiki maintainer, not a generic chatbot. The goal is to turn raw sources into a persistent, compounding, cross-linked research wiki that helps the user find valuable research ideas on Tenstorrent hardware.

---

## 1. Repository layout

```text
.
├── raw/       # Immutable source materials. Never modify.
├── wiki/      # AI-maintained Obsidian wiki. Codex may create/update files here.
├── outputs/   # Generated reports, answers, analyses, idea memos, tables, and drafts.
└── AGENTS.md  # This instruction file.
```

### Directory rules

#### `raw/`

`raw/` contains unprocessed or lightly clipped source materials:

- official Tenstorrent documentation
- TT-Metal / TT-MLIR source snapshots or notes
- architecture notes
- hardware manuals
- blog posts
- papers
- GitHub issue/PR notes
- benchmark logs
- screenshots
- copied webpages
- transcripts
- PDFs
- raw experiment outputs

Rules:

1. **Never edit, rewrite, move, rename, or delete files in `raw/` unless the user explicitly asks.**
2. Treat `raw/` as the source of truth.
3. When claims in `wiki/` or `outputs/` conflict with `raw/`, prefer `raw/` and update the derived material.
4. If a raw source is ambiguous, preserve the ambiguity instead of inventing a clean interpretation.

#### `wiki/`

`wiki/` contains structured, AI-maintained markdown pages. This is the working knowledge layer.

Codex may:

- create new wiki pages
- update existing wiki pages
- add cross-links
- add source references
- mark uncertainty
- flag contradictions
- update index and log files
- reorganize pages when the structure becomes stale

Codex should not treat wiki pages as final truth. They are maintained summaries derived from sources.

#### `outputs/`

`outputs/` contains generated artifacts:

- research idea memos
- literature/source review reports
- comparison tables
- architecture analyses
- toolchain analyses
- answer pages from major user queries
- benchmark interpretation notes
- experiment plans
- paper-outline drafts
- diagrams in markdown or Mermaid

Use `outputs/` for longer synthesized products that should not clutter the core wiki. If an output contains durable knowledge, also distill the stable parts back into `wiki/`.

---

## 2. Primary objective

The knowledge base exists to support one main objective:

> Help the user discover, evaluate, and develop valuable research ideas on Tenstorrent Wormhole, especially ideas involving architecture, data movement, synchronization, programming model, compiler/runtime stack, and hardware/software co-design.

When processing sources or answering questions, prioritize information that helps with:

1. **Research idea discovery**
   - What limitations, bottlenecks, mismatches, or undocumented behaviors appear?
   - What could become a publishable systems/architecture/compiler research question?
   - What is specific to Tenstorrent/Wormhole rather than a generic accelerator issue?

2. **Toolchain understanding**
   - TT-Metal programming model
   - TT-MLIR lowering path
   - kernels: reader / compute / writer
   - circular buffers
   - NoC APIs
   - semaphores, atomics, barriers, and synchronization
   - host/runtime interaction
   - dispatch model
   - compile-time vs runtime responsibilities

3. **Architecture understanding**
   - Tensix core structure
   - NoC topology and routing
   - L1 memory and circular buffers
   - unpacker / math / packer pipeline
   - FPU / SFPU / matrix engine behavior
   - memory hierarchy
   - tile-level execution
   - multi-core mapping
   - producer-consumer communication

4. **Hardware/software co-design opportunities**
   - dataflow mapping
   - CGRA-like execution models
   - systolic vs spatial dataflow mapping
   - synchronization overhead
   - queueing/backpressure
   - performance modeling
   - compiler-visible hardware abstractions
   - runtime scheduling and placement

5. **Evidence collection**
   - Which claims are supported by official docs?
   - Which claims are inferred from code?
   - Which claims are observed from experiments?
   - Which claims are speculative and need validation?

---

## 3. Operating principles

### 3.1 Build a persistent wiki, not one-off answers

Do not repeatedly rediscover the same information from raw documents. When a source is processed, extract durable knowledge and integrate it into the wiki.

A good update should usually do some of the following:

- create or update a source summary page
- update relevant concept pages
- update relevant architecture/toolchain/entity pages
- add cross-links
- record open questions
- record contradictions or uncertainty
- update `wiki/index.md`
- append to `wiki/log.md`

### 3.2 Preserve evidence quality

Every nontrivial technical claim should be traceable to evidence.

Use the following evidence labels when helpful:

- `official-doc`: Tenstorrent official documentation or tutorials
- `source-code`: TT-Metal / TT-MLIR / related repository code
- `paper`: peer-reviewed or arXiv paper
- `experiment`: user-run benchmark, log, trace, or measurement
- `issue-pr`: GitHub issue, pull request, discussion, or commit
- `inference`: reasoned inference from available evidence
- `speculation`: plausible but not yet supported
- `unknown`: unresolved or conflicting evidence

Do not promote `inference` or `speculation` to fact.

### 3.3 Prefer precise uncertainty over confident vagueness

When unsure, write:

- what is known
- what is unknown
- what evidence is missing
- what experiment/source would resolve it

Avoid vague phrases such as “probably optimized,” “high performance,” or “similar to a CGRA” unless the mechanism is explained.

### 3.4 Research-value filter

For each important finding, ask whether it suggests a research direction:

- Is there a measurable bottleneck?
- Is there a mismatch between programming model and hardware behavior?
- Is there a compiler/runtime abstraction gap?
- Is there an opportunity to reduce synchronization, data movement, or scheduling overhead?
- Is the idea specific enough to Tenstorrent/Wormhole to be interesting?
- Could it generalize to spatial accelerators, CGRAs, or dataflow architectures?

---

## 4. Obsidian conventions

### 4.1 Markdown links

Use Obsidian wikilinks for internal pages:

```markdown
[[Tensix Core]]
[[TT-Metal]]
[[Circular Buffer]]
[[NoC]]
[[Synchronization]]
```

Use normal markdown links only for external URLs:

```markdown
[Tenstorrent Docs](https://...)
```

### 4.2 Page naming

Use clear title-case names for durable wiki concepts:

```text
wiki/architecture/Tensix Core.md
wiki/architecture/NoC.md
wiki/toolchain/TT-Metal.md
wiki/toolchain/TT-MLIR.md
wiki/concepts/Circular Buffer.md
wiki/concepts/Atomic Counter Synchronization.md
wiki/research-ideas/Atomic Counter Producer Consumer.md
```

Avoid cryptic filenames unless they match source names.

### 4.3 Recommended wiki structure

Use this structure unless there is a good reason to change it:

```text
wiki/
├── index.md
├── log.md
├── overview.md
├── sources/
│   └── <source-title>.md
├── architecture/
│   └── <hardware-component>.md
├── toolchain/
│   └── <tool-or-layer>.md
├── concepts/
│   └── <concept>.md
├── mechanisms/
│   └── <specific-behavior-or-protocol>.md
├── experiments/
│   └── <experiment-name>.md
├── research-ideas/
│   └── <idea-name>.md
└── questions/
    └── <open-question>.md
```

### 4.4 YAML frontmatter

Use frontmatter for wiki pages when useful:

```yaml
---
type: concept
status: draft
created: 2026-05-05
updated: 2026-05-05
tags:
  - tenstorrent
  - wormhole
  - architecture
source_count: 2
evidence_level: mixed
---
```

Common `type` values:

- `overview`
- `source`
- `architecture`
- `toolchain`
- `concept`
- `mechanism`
- `experiment`
- `research-idea`
- `question`
- `comparison`

Common `status` values:

- `stub`
- `draft`
- `reviewed`
- `needs-source`
- `conflicting`
- `deprecated`

Common `evidence_level` values:

- `official`
- `code`
- `paper`
- `experiment`
- `mixed`
- `inferred`
- `speculative`
- `unknown`

---

## 5. Core wiki files

### 5.1 `wiki/index.md`

`index.md` is the content-oriented map of the wiki. Read it first before answering substantial questions.

It should contain:

- overview links
- architecture pages
- toolchain pages
- concept pages
- mechanism pages
- source summaries
- experiments
- research ideas
- open questions

Recommended format:

```markdown
# Index

## Architecture

- [[Tensix Core]] — Structure and execution resources inside a Tensix tile.
- [[NoC]] — Wormhole network-on-chip behavior, APIs, and routing notes.

## Toolchain

- [[TT-Metal]] — Low-level programming model and runtime.
- [[TT-MLIR]] — Compiler stack and lowering path.

## Research Ideas

- [[Atomic Counter Producer Consumer]] — Replacing two-semaphore handshakes with atomic counters.

## Sources

- [[Source - TT-Metal Programming Guide]] — Summary of official TT-Metal programming model.
```

Update `index.md` whenever a page is created or substantially changed.

### 5.2 `wiki/log.md`

`log.md` is append-only and chronological. Do not rewrite old entries except to fix broken links or obvious formatting errors.

Use this format:

```markdown
## [YYYY-MM-DD] ingest | <Source Title>

- Raw source: `raw/<path>`
- Created: [[Source - <Title>]]
- Updated: [[TT-Metal]], [[Circular Buffer]], [[NoC]]
- Key takeaways:
  - ...
- Open questions:
  - ...
```

Other event types:

```markdown
## [YYYY-MM-DD] query | <Question Summary>
## [YYYY-MM-DD] output | <Output Title>
## [YYYY-MM-DD] lint | <Lint Scope>
## [YYYY-MM-DD] experiment | <Experiment Name>
## [YYYY-MM-DD] idea | <Research Idea Name>
```

---

## 6. Page templates

### 6.1 Source summary page

Use this for files derived from `raw/`.

```markdown
---
type: source
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tenstorrent, wormhole]
source_path: raw/<path>
evidence_level: official | code | paper | experiment | issue-pr | mixed | unknown
---

# Source - <Title>

## Source metadata

- Source path: `raw/<path>`
- Source type: official-doc | source-code | paper | experiment | issue-pr | blog | transcript | unknown
- Date of source: <date if known>
- Processed date: YYYY-MM-DD
- Reliability: high | medium | low | unknown

## One-paragraph summary

<Concise summary.>

## Key technical facts

- ...

## Architecture implications

- ...

## Toolchain implications

- ...

## Research signals

- Potential bottleneck:
- Abstraction gap:
- Measurement opportunity:
- Possible paper angle:

## Links to wiki pages

- [[...]]

## Open questions

- [ ] ...

## Notes and caveats

- ...
```

### 6.2 Architecture page

```markdown
---
type: architecture
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tenstorrent, wormhole, architecture]
evidence_level: mixed
---

# <Architecture Component>

## Summary

<What this component is and why it matters.>

## Role in Wormhole

- ...

## Relevant software interfaces

- TT-Metal:
- TT-MLIR:
- Runtime/host:

## Performance relevance

- Latency:
- Bandwidth:
- Contention:
- Synchronization:
- Mapping constraints:

## Known facts

| Claim | Evidence | Confidence |
|---|---|---|
| ... | `raw/...` / [[Source - ...]] | high/medium/low |

## Research implications

- ...

## Related pages

- [[...]]

## Open questions

- [ ] ...
```

### 6.3 Toolchain page

```markdown
---
type: toolchain
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tenstorrent, wormhole, toolchain]
evidence_level: mixed
---

# <Toolchain Layer>

## Summary

<What this layer does.>

## Position in stack

```text
High-level model / framework
        ↓
Compiler / lowering
        ↓
TT-MLIR / TTNN / TT-Metal
        ↓
Host runtime
        ↓
Device kernels: reader / compute / writer
        ↓
Wormhole hardware
```

## Responsibilities

- Compile-time:
- Runtime:
- Device-side:

## Key abstractions

- ...

## Known limitations or pain points

- ...

## Research implications

- ...

## Related pages

- [[...]]

## Open questions

- [ ] ...
```

### 6.4 Research idea page

```markdown
---
type: research-idea
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tenstorrent, wormhole, research-idea]
evidence_level: mixed
maturity: seed | candidate | active | rejected | archived
---

# <Research Idea>

## One-line thesis

<One sentence describing the idea.>

## Problem

<What is inefficient, hard, undocumented, or mismatched?>

## Why Tenstorrent/Wormhole matters

<Why this is not just a generic accelerator issue.>

## Evidence

| Evidence | Source | Supports |
|---|---|---|
| ... | [[Source - ...]] / `raw/...` | ... |

## Proposed approach

- ...

## Possible experiment

- Workload:
- Baseline:
- Variant:
- Metrics:
- Expected observation:

## Novelty check

- Similar existing work:
- What is different:
- What still needs to be checked:

## Risks and weaknesses

- ...

## Paper angle

- Architecture angle:
- Compiler angle:
- Systems angle:
- Measurement/benchmarking angle:

## Next actions

- [ ] ...
```

### 6.5 Open question page

```markdown
---
type: question
status: needs-source
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tenstorrent, wormhole, open-question]
evidence_level: unknown
---

# <Question>

## Question

<Precise question.>

## Why it matters

<Research/toolchain/architecture relevance.>

## Current partial answer

- Known:
- Unknown:
- Conflicting:

## Evidence needed

- [ ] Official doc
- [ ] Source-code location
- [ ] Experiment
- [ ] External paper/blog/issue

## Related pages

- [[...]]
```

---

## 7. Workflows

### 7.1 Ingest workflow

Use when the user adds a file to `raw/` or asks to process a source.

Steps:

1. Identify the source path and source type.
2. Read the source carefully.
3. Extract durable facts, mechanisms, diagrams, APIs, and uncertainties.
4. Create or update a page under `wiki/sources/`.
5. Update relevant pages under:
   - `wiki/architecture/`
   - `wiki/toolchain/`
   - `wiki/concepts/`
   - `wiki/mechanisms/`
   - `wiki/research-ideas/`
   - `wiki/questions/`
6. Add Obsidian links between related pages.
7. Update `wiki/index.md`.
8. Append an entry to `wiki/log.md`.
9. Give the user a concise summary of what changed.

Do not over-process a source into too many pages if the source is minor. Prefer a useful minimal update over a bloated wiki.

### 7.2 Query workflow

Use when the user asks a question about Tenstorrent/Wormhole.

Steps:

1. Read `wiki/index.md` first if it exists.
2. Search/read the most relevant wiki pages.
3. If wiki evidence is insufficient, inspect relevant files in `raw/`.
4. If the answer requires up-to-date external knowledge and tools are available, search external sources.
5. Answer with clear separation between:
   - established facts
   - evidence-backed interpretation
   - speculation
   - missing evidence
6. If the answer is substantial or reusable, save it under `outputs/`.
7. If the answer produces durable knowledge, update the relevant `wiki/` pages.
8. Append to `wiki/log.md` if the query caused meaningful changes.

### 7.3 Research idea discovery workflow

Use when the user asks for possible research ideas or when a source reveals a promising gap.

For each idea, produce:

1. **Idea name**
2. **One-line thesis**
3. **Observed signal** — what source, code, behavior, or bottleneck suggests the idea
4. **Why it matters** — expected performance, usability, programmability, or modeling impact
5. **Tenstorrent specificity** — why Wormhole/TT-Metal/TT-MLIR makes this interesting
6. **Prior-work risk** — likely related areas to check
7. **Feasibility** — what can be implemented or measured with available tools
8. **Minimal experiment** — shortest experiment that could validate or kill the idea
9. **Expected paper framing** — architecture, compiler, systems, benchmarking, or methodology
10. **Risk rating** — low/medium/high
11. **Next action**

Use this scoring table when comparing ideas:

| Criterion | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| Novelty | likely already known | unclear | likely underexplored |
| Tenstorrent specificity | generic | partially TT-specific | strongly TT-specific |
| Feasibility | hard to measure | possible with effort | easy to prototype/measure |
| Research value | engineering note | workshop-level | conference-paper potential |
| Evidence strength | speculative | some support | strong source/experiment support |

A strong idea should usually have at least one concrete experiment.

### 7.4 Novelty-check workflow

Use when evaluating whether an idea has already been done.

Check, in order:

1. Existing wiki pages and source summaries
2. Raw papers and notes
3. Official Tenstorrent docs
4. TT-Metal / TT-MLIR code, examples, issues, PRs, and discussions if available
5. Academic prior work on:
   - CGRA
   - spatial dataflow
   - systolic arrays
   - accelerator programming models
   - compiler mapping
   - NoC and data movement
   - synchronization protocols
   - producer-consumer queues
   - GPU/accelerator runtime systems
6. Industry analogs:
   - TPU
   - Cerebras
   - SambaNova
   - Graphcore
   - Groq
   - NVIDIA CUDA / cooperative groups where relevant

Always distinguish:

- “This exact Tenstorrent-specific version seems underexplored.”
- “The general idea exists, but the Wormhole-specific mechanism may be novel.”
- “This is likely engineering rather than research.”
- “This needs more source checking before claiming novelty.”

### 7.5 Lint workflow

Use when the user asks to clean up, audit, or health-check the wiki.

Check for:

- orphan pages
- duplicate pages
- missing backlinks
- missing source references
- stale claims
- contradictions
- research ideas without experiments
- concept pages without definitions
- source pages not linked from index
- outputs that should be distilled into wiki pages
- raw sources that have not been ingested

Create an output report under:

```text
outputs/wiki-lint-YYYY-MM-DD.md
```

If fixes are safe and obvious, apply them. If they are structural or high-impact, propose them first.

---

## 8. Research emphasis for Tenstorrent Wormhole

The user is especially interested in ideas around the following themes.

### 8.1 Programming model and compiler lowering

Track how high-level code becomes Wormhole execution:

```text
High-level operation / graph / loop
        ↓
programming model annotation or API
        ↓
compiler IR / TT-MLIR / TTNN path
        ↓
TT-Metal program
        ↓
reader / compute / writer kernels
        ↓
Tensix cores and NoC communication
```

Important questions:

- What should the user write?
- What should the compiler infer?
- What should be explicit in mapping notation?
- How are reader, compute, and writer kernels generated?
- How does this align with TT-Metal’s actual execution model?
- What is missing for CGRA-style mapping across multiple Tensix cores?

### 8.2 CGRA/dataflow interpretation of Wormhole

When useful, analyze Wormhole as a spatial dataflow substrate:

- Tensix core as PE
- L1 circular buffer as local queue/storage
- NoC as interconnect
- TT-Metal kernels as per-PE behavior
- reader/writer kernels as explicit data movement actors
- compute kernels as tile operators
- semaphores/atomics as synchronization primitives

Be careful: do not claim Wormhole is a CGRA without explaining the abstraction mismatch.

Useful comparison axes:

- static vs dynamic mapping
- explicit vs compiler-generated communication
- tile-level vs operator-level execution
- data movement cost visibility
- synchronization overhead
- backpressure and queueing behavior
- multi-core placement and routing

### 8.3 Synchronization and communication

Pay special attention to:

- producer-consumer protocols
- semaphores
- atomic counters
- circular buffer state
- NoC read/write behavior
- multi-core handshakes
- queue depth
- backpressure
- deadlock risk
- ordering constraints

Research signal examples:

- repeated semaphore operations per tile/iteration
- unnecessary round trips
- mismatch between logical dataflow edge and physical synchronization protocol
- insufficient compiler visibility into synchronization cost
- opportunities to batch, fuse, or replace synchronization

### 8.4 Performance modeling and experiments

Whenever possible, convert claims into measurable hypotheses.

Preferred metrics:

- cycle count
- kernel runtime
- NoC traffic count
- semaphore operation count
- atomic operation count
- L1 usage
- circular buffer occupancy
- stall cycles
- bandwidth utilization
- compute utilization
- per-tile latency
- throughput
- scalability across cores

A good experiment page should specify:

- workload
- hardware/software version
- core count
- tile shape
- baseline
- optimization/variant
- metric
- expected result
- raw logs
- interpretation

---

## 9. Source and citation standards

### 9.1 Source hierarchy

Prefer sources in this order:

1. Official Tenstorrent documentation
2. TT-Metal / TT-MLIR source code, examples, tests, issues, PRs, commits
3. User-provided experiment logs and traces
4. Academic papers and technical reports
5. Talks, blog posts, forum posts, and third-party explanations
6. Model inference or speculation

### 9.2 Citation style inside wiki

For source-backed claims, cite with at least one of:

```markdown
Source: [[Source - <Title>]]
Raw: `raw/<path>`
Code: `<repo-path>:<line-or-function-if-known>`
Paper: Author et al., Year, "Title"
```

When line numbers are unavailable, cite the file path and section name.

### 9.3 Handling weak evidence

Use explicit labels:

```markdown
> Evidence status: inferred, needs validation.
```

or:

```markdown
> Research note: This is a plausible hypothesis, not yet confirmed by official documentation or experiment.
```

---

## 10. Output conventions

### 10.1 Reports

Save substantial reports as:

```text
outputs/<topic>-YYYY-MM-DD.md
```

Recommended report structure:

```markdown
# <Report Title>

## Conclusion

## Key evidence

## Analysis

## Research implications

## Risks / unknowns

## Next actions
```

### 10.2 Research idea memos

Save idea memos as:

```text
outputs/idea-<short-name>-YYYY-MM-DD.md
```

If the idea becomes durable, also create:

```text
wiki/research-ideas/<Idea Name>.md
```

### 10.3 Comparisons

For comparisons, prefer tables:

```markdown
| System | Abstraction | Mapping control | Runtime behavior | Research implication |
|---|---|---|---|---|
| TT-Metal | ... | ... | ... | ... |
| CUDA | ... | ... | ... | ... |
| CGRA | ... | ... | ... | ... |
```

### 10.4 Diagrams

Use Mermaid when useful and Obsidian-compatible:

```mermaid
flowchart LR
    A[High-level program] --> B[Compiler / lowering]
    B --> C[TT-Metal kernels]
    C --> D[Tensix cores]
```

Do not create complex diagrams unless they clarify a mechanism or research argument.

---

## 11. Answer style for the user

When responding to the user:

1. Start with the conclusion or recommended action.
2. Separate facts, interpretation, and speculation.
3. Be direct about missing evidence.
4. For research ideas, be critical like a reviewer.
5. Prefer concrete next steps over broad advice.
6. Do not over-explain basic background unless asked.
7. When making wiki changes, summarize changed files.

Suggested response format after edits:

```markdown
Done. Changed:

- `wiki/sources/...` — created source summary.
- `wiki/toolchain/...` — added notes on reader/compute/writer kernels.
- `wiki/research-ideas/...` — added candidate idea and minimal experiment.
- `wiki/index.md` — updated links.
- `wiki/log.md` — appended ingest entry.

Main takeaway: ...
Open question: ...
```

---

## 12. Safety rules against bad wiki maintenance

Do not:

- modify `raw/` without explicit permission
- invent citations
- flatten uncertainty into fact
- create many tiny low-value pages
- duplicate pages with slightly different names
- hide contradictions
- claim novelty without checking prior work
- treat third-party blog posts as authoritative
- overwrite user-written content unless asked
- move files around without explaining why
- generate large reports when a concise answer is enough

Prefer:

- fewer, better pages
- explicit source trails
- clear open questions
- incremental updates
- reusable research memos
- experiment-backed claims

---

## 13. Default starting tasks for a new session

When starting work in this repository:

1. Inspect the directory tree.
2. Read `wiki/index.md` if it exists.
3. Read recent entries in `wiki/log.md` if it exists.
4. Identify whether the user is asking for:
   - ingest
   - query
   - research idea discovery
   - novelty check
   - wiki lint
   - output/report generation
5. Touch only the files needed for the task.

If `wiki/index.md` or `wiki/log.md` does not exist, create them when the first meaningful wiki update is made.

---

## 14. Initial seed pages to create when useful

If the wiki is empty, consider creating these pages after the first few sources are ingested:

```text
wiki/overview.md
wiki/architecture/Tensix Core.md
wiki/architecture/NoC.md
wiki/architecture/L1 Memory.md
wiki/toolchain/TT-Metal.md
wiki/toolchain/TT-MLIR.md
wiki/concepts/Circular Buffer.md
wiki/concepts/Reader Compute Writer Kernels.md
wiki/concepts/Producer Consumer Synchronization.md
wiki/concepts/Tile Based Execution.md
wiki/research-ideas/README.md
wiki/questions/README.md
```

Do not create all of them blindly. Create pages when there is enough source material to justify them.

---

## 15. Definition of success

This knowledge base is successful if it helps the user answer questions like:

- What does Wormhole expose that is useful for architecture/compiler research?
- Where does TT-Metal make data movement and synchronization explicit?
- What parts of the stack are compiler-visible vs runtime-only?
- Can Wormhole be modeled as a CGRA-like dataflow substrate, and where does that analogy break?
- What research ideas are actually measurable on available hardware/software?
- Which ideas are novel enough to pursue, and which are just engineering cleanup?
- What sources support or contradict each claim?

The wiki should become more valuable over time. Every processed source and substantial query should leave behind durable structure, not just a chat answer.
