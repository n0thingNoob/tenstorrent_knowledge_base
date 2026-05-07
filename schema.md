# Schema

## Repository roles

- `raw/`: immutable source material and acquisition artifacts
- `wiki/`: durable, curated knowledge pages with Obsidian wikilinks
- `outputs/`: reusable analyses, corpus provenance, and research artifacts
- `docs/`: operational documentation for workflows and maintenance

## Preferred wiki taxonomy

- `wiki/architecture/`: hardware components and architectural entities
- `wiki/toolchain/`: compiler, runtime, SDK, and stack-layer pages
- `wiki/concepts/`: cross-cutting abstractions and stable conceptual frames
- `wiki/mechanisms/`: concrete protocols, behaviors, and execution mechanisms
- `wiki/sources/`: source summary pages derived from `raw/`
- `wiki/questions/`: structured open-question tracking
- `wiki/research-ideas/`: candidate or active research directions

## Page types

Use frontmatter `type` values from this set when updating or creating pages:

- `overview`
- `source`
- `architecture`
- `toolchain`
- `concept`
- `mechanism`
- `question`
- `research-idea`
- `comparison`
- `experiment`

## Naming rules

- Use title-case filenames for durable concepts and entities
- Prefer direct names like `Tensix.md`, `Circular Buffers.md`, `TT-Metal.md`
- Keep source summaries under `wiki/sources/` with stable human-readable names
- Use Obsidian wikilinks for internal references and markdown links for external URLs

## Evidence labels

Preferred evidence labels:

- `official-doc`
- `source-code`
- `paper`
- `experiment`
- `issue-pr`
- `inference`
- `speculation`
- `unknown`

Do not upgrade `inference` or `speculation` into fact without stronger evidence.

## Promotion rules

- Put stable knowledge in `wiki/`
- Put one-off reports, answer artifacts, and provenance reports in `outputs/`
- Keep operational workflow notes out of `outputs/`; place them in `docs/`
- Do not modify `raw/` unless explicitly asked
