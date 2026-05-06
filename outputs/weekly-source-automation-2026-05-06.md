# Weekly Source Automation

## Goal

Collect candidate external sources into `raw/` every week from GitHub Actions, then review them for later wiki ingestion.

## Current cloud workflow

1. Read `scripts/source_feeds.json` for configured sources.
2. Fetch recent items from blog pages and arXiv.
3. Write new candidates into `raw/` using the existing date-prefixed naming style.
4. Write a run report into `outputs/source-collection-YYYY-MM-DD.md`.
5. Commit the new `raw/` files, collection report, and state file back to GitHub.

The GitHub Actions workflow lives at `.github/workflows/weekly-source-collection.yml`.

## Current source set

- `tenstorrent-newsroom` — official Tenstorrent newsroom page, keyword-filtered.
- `corsix-tenstorrent` — corsix posts matching Wormhole or ET-SoC patterns.
- `arxiv-tenstorrent` — arXiv API query for `tenstorrent`.

## Manual wiki-writing policy

- Prefer updating existing concept, architecture, toolchain, and source-summary pages over creating many tiny pages.
- Only material with durable research value should be promoted from `raw/` into `wiki/`.
- Business announcements can stay in `raw/` unless they reveal architecture, software-stack, benchmarking, or research-relevant facts.
- Uncertainty should stay explicit when the new source is weak or ambiguous.

## Why this split is safer

- `raw/` remains the acquisition layer.
- `wiki/` remains evidence-curated rather than becoming a news dump.
- Cloud automation does not rewrite core knowledge pages without review.

## Schedule

- GitHub Actions cron: every Monday at 14:00 UTC.
- This is 10:00 in US Eastern Daylight Time and 09:00 in US Eastern Standard Time.

## Next improvements

- Add GitHub release/doc watchers for `tt-metal`, `tt-mlir`, and related repos.
- Add HTML snapshots or PDF download for papers when needed.
- Add a second-stage ingest helper that drafts `wiki/sources/...` pages from selected raw files.
- Add source scoring so only high-value candidates are considered for wiki updates.
