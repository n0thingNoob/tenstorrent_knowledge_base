# Log

Append-only chronological log of wiki and output changes.

## [2026-05-05] ingest | Initial corpus to seed wiki

- Raw files processed: 16 files in `raw/2026-05-05__*.md`
- Wiki created from scratch:
  - `entities/` -> [[toolchain/Tenstorrent|Tenstorrent]], [[architecture/Wormhole|Wormhole]], [[architecture/Tensix|Tensix]]
  - `concepts/` -> core stack, hardware, and execution-model pages
  - `sources/` -> 16 source-summary pages, one per raw file
  - `index.md`, `glossary.md`, open-question tracking, and `log.md`
- Outputs: `outputs/wiki_ingest_report.md`
- Key takeaways:
  - hardware coverage is solid from corsix plus partial official docs
  - programming model coverage is solid around TT-Metal and reader/compute/writer structure
  - compiler stack coverage is shallow, especially TT-MLIR
  - synchronization primitives are better covered than the mapping from those primitives to TT-Metal circular-buffer metadata
- Open questions raised: highest-priority items now live under [[questions/README|Questions]], especially synchronization and TT-MLIR responsibility questions

## [2026-05-05] output | Source collection pass 1

- See `outputs/source_collection_manifest.md` and `outputs/source_collection_report.md`
- Raw files collected: 7 corsix posts, 6 GitHub READMEs/docs, and 3 paper-metadata stubs

## [2026-05-06] lint | Vault simplification and taxonomy alignment

- Added: [[overview]], `purpose.md`, `schema.md`, and `docs/automation.md`
- Restructured wiki toward `architecture/`, `toolchain/`, `mechanisms/`, `questions/`, and `research-ideas/`
- Replaced monolithic open-question tracking with [[questions/README|Questions]] and six category pages
- Reduced low-value operational clutter by removing the duplicate instruction file, moving workflow docs out of `outputs/`, and moving collector state out of `outputs/`
