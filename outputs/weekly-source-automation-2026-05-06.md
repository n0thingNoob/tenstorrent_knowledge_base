# Weekly Source Automation

## Goal

Collect candidate external sources into `raw/` every week without automatically changing `wiki/`.

## What the automation does

- Reads `scripts/source_feeds.json` for configured sources.
- Fetches recent items from blog pages and arXiv.
- Writes new candidates into `raw/` using the existing date-prefixed naming style.
- Writes a run report into `outputs/source-collection-YYYY-MM-DD.md`.
- Tracks seen URLs in `outputs/source_collection_state.json` to avoid duplicates.

## Current source set

- `tenstorrent-newsroom` — official Tenstorrent newsroom page, keyword-filtered.
- `corsix-tenstorrent` — corsix posts matching Wormhole or ET-SoC patterns.
- `arxiv-tenstorrent` — arXiv API query for `tenstorrent`.

## Suggested operating model

1. Weekly automation runs `scripts/run_weekly_collection.ps1`.
2. New files land in `raw/`.
3. Review the generated report in `outputs/source-collection-YYYY-MM-DD.md`.
4. Manually choose which raw files are worth ingesting into `wiki/`.

## Why this is safer than full auto-ingest

- `raw/` remains the acquisition layer.
- `wiki/` is still evidence-curated and not polluted by noisy business posts.
- The workflow matches the repository rule that durable claims should be source-backed and reviewed.

## Next improvements

- Add GitHub release/doc watchers for `tt-metal`, `tt-mlir`, and related repos.
- Add HTML snapshots or PDF download for papers when needed.
- Add a second-stage ingest helper that drafts `wiki/sources/...` pages from selected raw files.
