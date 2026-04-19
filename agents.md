# Agent context: zeric-googleads-localdata

This repository holds **Google Ads account data and tooling** for Spavia (West Plano) and related campaign work. It is not a generic app codebase; it is a **working area** for exports, Editor-style imports, playbooks, and small Python utilities.

## What is here

- **`exports/`** — Tab-separated full-account (or large) pulls from Google Ads Editor (they may arrive as UTF-16). These define the **column layout** and realistic field values for a given date. When you replace or add files under version control, prefer **UTF-8** so the repo stays editor-friendly.
- **`imports/`** and **`mothersday/`** — Campaign-specific import files, playbooks (for example Mother's Day / gift cards), and **`build_mothersday_import.py`**, which generates the wide "full account" CSV from a reference export plus intentional edits.
- **`_compare_import_export.py`** — Example pattern for comparing import vs export keywords/entities using `csv.reader` and UTF-16.

## Rules of thumb for agents

1. **Wide Editor imports** (hundreds of tab-separated columns) must stay **aligned** to the latest export header. Prefer changing **`build_mothersday_import.py`** and having the user run it, rather than hand-editing giant TSV rows.
2. Read **`DECISIONS-ImportFile.md`** before building or fixing import files. It documents column-count discipline, UTF-16 + `csv.reader`, off-by-one row indexing, Display vs Search field strings, and other mistakes to avoid.
3. **Encoding:** Create and save plain text in this repo as **UTF-8** (not UTF-16). Markdown, Python, playbooks, configs, and hand-edited CSV/TSV meant for Cursor or Git should be UTF-8; UTF-16 (especially without BOM) garbles many tools and diffs. It is fine to **read** UTF-16 when parsing Google Ads Editor exports in Python—just do not **write** or re-save project files as UTF-16. For Markdown and CSV in this repo, UTF-8 with BOM is acceptable and helps some editors detect encoding.

## Canonical doc for import mistakes

**[DECISIONS-ImportFile.md](DECISIONS-ImportFile.md)** — Teaching notes so agents (and humans) do not repeat common Google Ads Editor import errors.
