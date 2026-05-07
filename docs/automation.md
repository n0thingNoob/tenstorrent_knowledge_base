# Automation

## Purpose

Automation in this vault is intentionally narrow:

- cloud automation collects candidate sources into `raw/`
- local scripts help back up manual wiki maintenance
- automation does not rewrite the curated wiki on its own

## GitHub Actions collection

The workflow at `.github/workflows/weekly-source-collection.yml` runs weekly and can also be triggered manually.

It does the following:

1. Read `scripts/source_feeds.json`
2. Fetch recent source candidates
3. Write new source captures into `raw/`
4. Write a collection report into `outputs/source-collection-YYYY-MM-DD.md`
5. Update collector state in `scripts/source_collection_state.json`
6. Commit and push those source-collection changes

Current source set:

- `tenstorrent-newsroom` — official Tenstorrent newsroom page, keyword-filtered
- `corsix-tenstorrent` — corsix posts matching Wormhole or ET-SoC patterns
- `arxiv-tenstorrent` — arXiv API query for `tenstorrent`

Schedule:

- GitHub Actions cron: every Monday at 14:00 UTC
- This is 10:00 in US Eastern Daylight Time and 09:00 in US Eastern Standard Time

## Local backup

`scripts/weekly_git_backup.ps1` is a local convenience script for manual maintenance sessions. It:

- stages all changes
- commits only when something changed
- pushes `main` to `origin`

Example:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/weekly_git_backup.ps1
```

## Manual wiki policy

- Keep `raw/` as acquisition, not distilled knowledge
- Promote only durable, research-relevant material into `wiki/`
- Prefer updating existing pages over creating many tiny pages
- Keep uncertainty explicit when evidence is weak
