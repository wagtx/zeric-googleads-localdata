# DECISIONS: Google Ads Editor import files (TSV/CSV)

This file captures mistakes we hit when building account imports so future work does not repeat them.

## 1. Column count is the whole game

- Google Ads Editor "full account" style exports are **wide tab-separated rows** (this account: **307** columns as of `exports/2026-04-12 1446.csv`).
- **Every** data row must have **exactly** the same number of fields as the header row. Off-by-one (or off-by-many) causes **column shift**: values land in the wrong fields, you see **Ambiguous row type**, nonsense in "Content exclusions" / "Networks", wrong bid strategies, etc.
- **Do not** hand-build rows by counting tabs or pasting partial rows. Use a script that **asserts** `len(row) == len(header)` before writing.

## 2. Always parse with the CSV module

- These files are **TSV** (`delimiter="\t"`), often **UTF-16 LE** with BOM from Editor.
- Use `csv.reader` (not `line.split("\t")`) so **quoted multiline cells** (structured snippets, long text) do not break row boundaries.
- Pattern:

```python
import csv
from pathlib import Path

path = Path("export.csv")
with path.open("r", encoding="utf-16", newline="") as f:
    rows = list(csv.reader(f, delimiter="\t"))
header, data = rows[0], rows[1:]
```

- The repo already follows this in `_compare_import_export.py`.

## 3. Know what "row index" means in code

- If `load()` returns `rows[1:]` (data only, no header), then **file line N** is **`rows[N - 2]`**, not `rows[N - 1]`.
- Using **full-file 1-based line numbers** as indices into **data-only** lists shifts templates by one row and can turn an **ad group** row into an **ad** row (wrong `Ad type`, wrong `Max CPC`, duplicate ads).

## 4. Clone live rows; edit by column name

- The safest import row is a **deep copy** of a **real** export row from the **same** header version, then overwrite fields by **column name** (build `idx = {name: i for i, name in enumerate(header)}`).
- Do not "minimize" rows by leaving out middle columns that look empty in Excel; those positions often carry `[]`, `Off`, `Doesn't have EU political ads`, `Account-level`, etc., that Editor expects.

## 5. Enum / network strings must match the product

- Values like **Networks** are picky. For example, **`Google search;Google search partners`** was rejected; a working pattern in this account's export was **`Google search;Search Partners`** (capital **P**, no extra "Google" before "Partners").
- When in doubt, **copy the exact string** from another **Search** row in the **same** export.



## 5b. Display campaign row (Editor import warnings)

- **Networks** for a standard Display campaign in this account is **Display Network**, not Google Display Network (Editor: Campaign networks are invalid).
- **Targeting method** and **Exclusion method** on the campaign row must match a known-good Display export, for example **Location of presence** for both, not UI phrases like Target and exclude (Editor: invalid targeting / exclusion method).
- **Ad rotation** on Display rows in exports often reads **Optimize for conversions** (not the shortened Optimize).
- **Interest categories** on ad groups must match Google's exact taxonomy strings from the picker (or export). Free-text in-market paths may trigger unknown warnings. Safer for imports: leave Interest categories empty, import, then add interests in the UI (age and geo still apply).
## 6. `Campaign#Original` vs `Campaign`

- Editor matches entities using **#Original** keys. If the live account was renamed, imports must use **`Campaign#Original` / `Campaign` (and ad group originals)** consistent with **what is actually in the account** at import time, or the row will update the wrong entity or fail to match.

## 7. Display rows when the current export has no Display template

- A newer export may **omit** a Display campaign entirely. You can still build Display rows by **projecting** a row from an **older** export whose header is a **superset** of column names: map by header name into the **new** 307-column header (see `project_row` in `mothersday/build_mothersday_import.py`).
- Fix **off-by-one** when mapping old file line numbers to `rows[1:]` indices (see section 3).

## 8. Regenerating Mother's Day / gift card main import

- Source export: `exports/2026-04-12 1446.csv`.
- Script: `mothersday/build_mothersday_import.py` writes **`mothersday/mothersday-main-import.csv`** (UTF-16 tab, **307** columns per row).
- After changing keywords, RSAs, budgets, or Display copy, **edit the script** and re-run it; do not hand-edit the CSV.

## 9. Sitelinks / callouts / snippets

- Those use a **different** narrow schema (see `mothersday/mothersday-sitelinks-callouts-snippets.csv`). Do not mix that schema into the 307-column "full" file.