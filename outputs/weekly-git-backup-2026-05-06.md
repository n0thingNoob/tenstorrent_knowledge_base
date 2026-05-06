# Weekly Git Backup

## Goal

Automatically back up this Obsidian research vault to GitHub every week after source collection and wiki maintenance.

## Current behavior

- Ignores machine-local Obsidian state:
  - `.obsidian/workspace.json`
  - `.obsidian/workspaces*.json`
  - `.obsidian/graph.json`
  - `.obsidian/plugins/`
- Uses `scripts/weekly_git_backup.ps1` to:
  - stage all current changes
  - create a timestamped commit only when there is something new
  - push `main` to `origin`

## Relationship to weekly collection

- Source collection is handled by `scripts/weekly_source_collect.py`.
- The Codex weekly automation is responsible for deciding whether newly collected `raw/` material should update `wiki/`.
- Git backup runs after those wiki edits so the vault snapshot includes both new sources and new distilled notes.

## Manual run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/weekly_git_backup.ps1
```

## Notes

- This is a backup workflow, not a code-review workflow.
- It will include any new files in the vault unless they are covered by `.gitignore`.
- If GitHub authentication expires, the script will fail on `git push` and should be re-authenticated once.
