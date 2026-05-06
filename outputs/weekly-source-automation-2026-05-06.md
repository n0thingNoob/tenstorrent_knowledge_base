# Weekly Source Automation

## Goal

Collect candidate external sources into `raw/` every week, distill worthwhile material into `wiki/`, and then back up the vault to GitHub.

## Full weekly workflow

1. Read `scripts/source_feeds.json` for configured sources.
2. Fetch recent items from blog pages and arXiv.
3. Write new candidates into `raw/` using the existing date-prefixed naming style.
4. Write a run report into `outputs/source-collection-YYYY-MM-DD.md`.
5. Review newly collected `raw/` files and update `wiki/` when the source adds durable knowledge.
6. Update `wiki/index.md` and `wiki/log.md` when meaningful wiki changes were made.
7. Run the git backup workflow to commit and push the updated vault.

## Current source set

- `tenstorrent-newsroom` — official Tenstorrent newsroom page, keyword-filtered.
- `corsix-tenstorrent` — corsix posts matching Wormhole or ET-SoC patterns.
- `arxiv-tenstorrent` — arXiv API query for `tenstorrent`.

## Wiki-writing policy

- Prefer updating existing concept, architecture, toolchain, and source-summary pages over creating many tiny pages.
- Only material with durable research value should be promoted from `raw/` into `wiki/`.
- Business announcements can stay in `raw/` unless they reveal architecture, software-stack, benchmarking, or research-relevant facts.
- Uncertainty should stay explicit when the new source is weak or ambiguous.

## Why this is still conservative

- `raw/` remains the acquisition layer.
- `wiki/` remains evidence-curated rather than becoming a news dump.
- The workflow matches the repository rule that durable claims should be source-backed and uncertainty-preserving.

## Next improvements

- Add GitHub release/doc watchers for `tt-metal`, `tt-mlir`, and related repos.
- Add HTML snapshots or PDF download for papers when needed.
- Add a second-stage ingest helper that drafts `wiki/sources/...` pages from selected raw files.
- Add source scoring so only high-value candidates are considered for wiki updates.
