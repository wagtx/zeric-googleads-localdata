"""Measure token efficiency of raw vs distilled formats for Google Ads exports."""
import pandas as pd
import json
import io
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")


def t(s: str) -> int:
    return len(enc.encode(s))


f1 = "Exports/2026-04-20 1046 CurrentWithStats.csv"
f2 = "Exports/2026-04-20 1046 SearchTerms17th-19th.csv"


def read_csv(path):
    return pd.read_csv(
        path,
        sep="\t",
        encoding="utf-16",
        low_memory=False,
        dtype=str,
        keep_default_na=False,
        na_values=[""],
    )


df1 = read_csv(f1)
df2 = read_csv(f2)

# --- Raw token counts ---
with io.open(f1, "r", encoding="utf-16") as fh:
    raw1 = fh.read()
with io.open(f2, "r", encoding="utf-16") as fh:
    raw2 = fh.read()
print(f"RAW CurrentWithStats: {len(raw1):>10,} chars   {t(raw1):>8,} tokens")
print(f"RAW SearchTerms:      {len(raw2):>10,} chars   {t(raw2):>8,} tokens")
print(f"RAW TOTAL:                                  {t(raw1)+t(raw2):>8,} tokens")
print()

ZEROISH = {"", "0", "0.00", "0.00%", "0%", "--", " --", "nan"}


def is_trivial_col(s: pd.Series) -> bool:
    vals = set(s.dropna().astype(str).str.strip().unique())
    vals -= ZEROISH
    return not vals


def prune(df: pd.DataFrame) -> pd.DataFrame:
    keep = [c for c in df.columns if not is_trivial_col(df[c])]
    return df[keep]


# --- Approach A: drop trivial columns, keep TSV ---
p1 = prune(df1)
p2 = prune(df2)
print(f"A) Prune trivial cols -> TSV:")
print(
    f"   CurrentWithStats cols {len(df1.columns)}->{len(p1.columns)}   "
    f"tokens {t(p1.to_csv(sep=chr(9), index=False)):,}"
)
print(
    f"   SearchTerms      cols {len(df2.columns)}->{len(p2.columns)}   "
    f"tokens {t(p2.to_csv(sep=chr(9), index=False)):,}"
)
print()


# --- Approach B: split by Source/row-type, prune each ---
def tsv(df):
    buf = io.StringIO()
    df.to_csv(buf, sep="\t", index=False)
    return buf.getvalue()


print("B) Split CurrentWithStats by 'Source' row-type, prune each subset:")
tot_b = 0
for src, sub in df1.groupby(df1["Source"].fillna("(blank)")):
    p = prune(sub)
    tk = t(tsv(p))
    tot_b += tk
    print(
        f"   Source={src!r:24s} rows={len(sub):>4d} cols={len(p.columns):>3d} "
        f"tokens={tk:,}"
    )
print(f"   TOTAL: {tot_b:,}")
print()


# --- Approach C: JSON-lines, drop blank/zero cells per row ---
def jsonl(df: pd.DataFrame) -> str:
    lines = []
    for rec in df.to_dict("records"):
        obj = {k: v for k, v in rec.items() if str(v).strip() not in ZEROISH}
        lines.append(json.dumps(obj, separators=(",", ":"), ensure_ascii=False))
    return "\n".join(lines)


j1 = jsonl(p1)
j2 = jsonl(p2)
print("C) JSONL (blank/zero cells dropped per row, full column names):")
print(f"   CurrentWithStats tokens={t(j1):,}")
print(f"   SearchTerms      tokens={t(j2):,}")
print(f"   TOTAL:                  {t(j1)+t(j2):,}")
print()

# --- Approach D: JSONL with short key codes ---
code_map = {
    "Campaign": "c",
    "Ad Group": "g",
    "Campaign Status": "cs",
    "Ad Group Status": "gs",
    "Keyword": "kw",
    "Criterion Type": "mt",
    "Source": "src",
    "Search term": "q",
    "Clicks": "Cl",
    "Cost": "Co",
    "Impressions": "Im",
    "CTR": "ctr",
    "Avg CPC": "cpc",
    "Avg CPM": "cpm",
    "Conversions": "Cv",
    "Cost per conv": "cpa",
    "Conv rate": "cvr",
    "Conv value": "Vl",
    "Value per conv": "vpc",
    "Interactions": "Ix",
    "Interaction Rate": "ixr",
    "Ad Group Type": "gt",
    "Status": "st",
    "Approval Status": "ap",
    "Campaign Type": "ct",
    "Final URL": "url",
    "Top impression percentage": "tip",
    "Absolute top impression rate": "atip",
    "Added or Excluded": "ax",
    "Account": "acc",
    "Account name": "accn",
}


def compact_jsonl(df: pd.DataFrame) -> str:
    d = df.rename(columns={k: v for k, v in code_map.items() if k in df.columns})
    lines = []
    for rec in d.to_dict("records"):
        obj = {k: v for k, v in rec.items() if str(v).strip() not in ZEROISH}
        obj.pop("acc", None)
        obj.pop("accn", None)
        lines.append(json.dumps(obj, separators=(",", ":"), ensure_ascii=False))
    return "\n".join(lines)


c1 = compact_jsonl(p1)
c2 = compact_jsonl(p2)
print("D) JSONL + short key codes + drop acc fields:")
print(f"   CurrentWithStats tokens={t(c1):,}")
print(f"   SearchTerms      tokens={t(c2):,}")
print(f"   TOTAL:                  {t(c1)+t(c2):,}")
print()

# --- Approach E: aggressive distilled TSV of only the fields that matter ---
# For the stats dataset: per-keyword perf, per-campaign summary, per-search-term perf

# Keyword-level stats rows: Source == Keyword OR Criterion Type matches a keyword type
kw_types = {
    "Phrase match", "Phrase", "Phrase match close variant",
    "Exact match", "Exact", "Exact match close variant",
    "Broad match", "Broad",
}
stats_cols = [
    "Campaign", "Ad Group", "Keyword", "Criterion Type", "Campaign Status",
    "Ad Group Status", "Status",
    "Clicks", "Impressions", "Cost", "CTR", "Avg CPC", "Conversions",
    "Conv value", "Cost per conv", "Conv rate",
    "Top impression percentage", "Absolute top impression rate",
]
kw_rows = p1[p1.get("Source").eq("Keyword") |
             p1.get("Criterion Type").isin(kw_types)] if "Source" in p1.columns else pd.DataFrame()
kw_rows = kw_rows[[c for c in stats_cols if c in kw_rows.columns]]

# Campaign summary rows: rows that define the campaign (one per campaign)
camp_summary = p1[p1["Campaign Type"].ne("") & p1["Ad Group"].eq("")] if "Campaign Type" in p1.columns else pd.DataFrame()

# Negative keywords
neg = p1[p1["Criterion Type"].str.contains("Negative", na=False)] if "Criterion Type" in p1.columns else pd.DataFrame()

# Asset/creative rows (headlines, descriptions, images) — usually the most bloat
asset_like = p1[p1["Source"].isin(["Advertiser", "Automatically created"])] if "Source" in p1.columns else pd.DataFrame()

# SearchTerms: keep top columns
st_cols = [
    "Search term", "Added or Excluded", "Keyword", "Criterion Type", "Source",
    "Campaign", "Ad Group", "Campaign Status",
    "Clicks", "Impressions", "Cost", "CTR", "Avg CPC",
    "Conversions", "Conv value", "Cost per conv", "Conv rate",
    "Top impression percentage", "Absolute top impression rate",
]
st_slim = df2[[c for c in st_cols if c in df2.columns]]


def tsv_prune(df):
    return tsv(prune(df))


e_kw = tsv_prune(kw_rows)
e_camp = tsv_prune(camp_summary)
e_neg = tsv_prune(neg)
e_asset = tsv_prune(asset_like)
e_st = tsv_prune(st_slim)

print("E) Distilled TSV (task-shaped tables only):")
print(f"   campaigns          rows={len(camp_summary):>4} tokens={t(e_camp):,}")
print(f"   keywords+perf      rows={len(kw_rows):>4} tokens={t(e_kw):,}")
print(f"   negatives          rows={len(neg):>4} tokens={t(e_neg):,}")
print(f"   asset/creative     rows={len(asset_like):>4} tokens={t(e_asset):,}")
print(f"   search terms       rows={len(st_slim):>4} tokens={t(e_st):,}")
total_e = t(e_kw) + t(e_camp) + t(e_neg) + t(e_asset) + t(e_st)
print(f"   TOTAL:                               {total_e:,}")

# Write a sample of the distilled output for human review
with open("Exports/_distilled_sample_2026-04-20.md", "w", encoding="utf-8") as fh:
    fh.write("# Distilled export preview (2026-04-20)\n\n")
    fh.write(f"## campaigns ({len(camp_summary)} rows)\n\n```\n{e_camp}\n```\n\n")
    fh.write(f"## keywords with perf ({len(kw_rows)} rows, head 30)\n\n```\n")
    fh.write(tsv(prune(kw_rows).head(30)))
    fh.write("\n```\n\n")
    fh.write(f"## search terms ({len(st_slim)} rows, head 30)\n\n```\n")
    fh.write(tsv(prune(st_slim).head(30)))
    fh.write("\n```\n\n")
    fh.write(f"## negatives ({len(neg)} rows)\n\n```\n{e_neg}\n```\n")

print()
print("Wrote Exports/_distilled_sample_2026-04-20.md for review.")
print()
print("Summary:")
print(f"  RAW total:      {t(raw1)+t(raw2):>8,} tokens")
print(f"  A prune TSV:    {t(p1.to_csv(sep=chr(9),index=False))+t(p2.to_csv(sep=chr(9),index=False)):>8,} tokens")
print(f"  B split+prune:  {tot_b + t(tsv(prune(df2))):>8,} tokens  (B on ds1 + pruned ds2)")
print(f"  C JSONL drop0:  {t(j1)+t(j2):>8,} tokens")
print(f"  D + short keys: {t(c1)+t(c2):>8,} tokens")
print(f"  E distilled:    {total_e:>8,} tokens")
