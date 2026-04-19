# -*- coding: utf-8 -*-
"""Supplement import: missing Display ad group + RDAs (creative matches mothersday-main-import)."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(r"c:\projects\repos\zeric-googleads-localdata")
EXPORT_NEW = ROOT / "exports" / "2026-04-12 1446.csv"
EXPORT_OLD = ROOT / "exports" / "2026-04-09 AfterImport-FullAccount.csv"
OUT = ROOT / "mothersday" / "display-gift-cards-supplement-import.csv"

OLD_SEARCH = "2026-Search - Gift Cards (Mother's Day)"
DISPLAY = "2026-Display - Gift Cards (Mother's Day)"

VALentine_AG2_IDX = 5852
VALentine_RDA1_IDX = 5851
VALentine_RDA2_IDX = 5853

# Account ad group name for in-market (Editor / live name).
LIVE_INMARKET_AG = "DisplayAG-InMarketMothersDay"


def load_tsv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", encoding="utf-16", newline="") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    return rows[0], rows[1:]


def project_row(old_row: list[str], old_h: list[str], new_h: list[str]) -> list[str]:
    oi = {n: i for i, n in enumerate(old_h)}
    out = [""] * len(new_h)
    for j, name in enumerate(new_h):
        if name in oi:
            k = oi[name]
            if k < len(old_row):
                out[j] = old_row[k]
    return out


def col_index(header: list[str]) -> dict[str, int]:
    return {n: i for i, n in enumerate(header)}


def set_fields(row: list[str], ix: dict[str, int], updates: dict[str, str]) -> None:
    for k, v in updates.items():
        row[ix[k]] = v


def replace_campaign_name(row: list[str], ix: dict[str, int], old: str, new: str) -> None:
    for key in ("Campaign#Original", "Campaign"):
        i = ix[key]
        if row[i] == old:
            row[i] = new


def assert_row_width(header: list[str], row: list[str], label: str) -> None:
    if len(row) != len(header):
        raise ValueError(f"{label}: expected {len(header)} cols, got {len(row)}")


def attach_display_campaign(r: list[str], ix: dict[str, int]) -> None:
    replace_campaign_name(r, ix, OLD_SEARCH, DISPLAY)
    for key in ("Campaign#Original", "Campaign"):
        c = ix[key]
        if r[c] and "Valentine" in r[c]:
            r[c] = DISPLAY
        elif not r[c].strip() and key == "Campaign":
            r[c] = DISPLAY


def clear_rda_location(r: list[str], ix: dict[str, int]) -> None:
    for k in (
        "Max CPC",
        "Location",
        "Location#Original",
        "Radius",
        "Radius#Original",
        "Reach",
        "Unit",
        "Unit#Original",
    ):
        r[ix[k]] = ""


def main() -> None:
    h_new, _ = load_tsv(EXPORT_NEW)
    h_old, rows_old = load_tsv(EXPORT_OLD)
    ix = col_index(h_new)

    def proj(idx_old: int) -> list[str]:
        return project_row(rows_old[idx_old], h_old, h_new)

    ag2 = proj(VALentine_AG2_IDX)
    rda_in = proj(VALentine_RDA1_IDX)
    rda_cu = proj(VALentine_RDA2_IDX)

    for r in (ag2, rda_in, rda_cu):
        attach_display_campaign(r, ix)

    set_fields(
        ag2,
        ix,
        {
            "Ad Group#Original": "Display - Custom Searchers",
            "Ad Group": "Display - Custom Searchers",
            "Max CPC": "0.50",
            "Age demographic": "25-34;35-44;45-54",
            "Interest categories": "",
            "Ad Group Status": "Enabled",
        },
    )

    set_fields(
        rda_cu,
        ix,
        {
            "Ad Group#Original": "Display - Custom Searchers",
            "Ad Group": "Display - Custom Searchers",
            "Headline 1": "Mother's Day Spa Gift Cards",
            "Headline 2": "Gift Cards From $50",
            "Headline 3": "Pamper Mom This Year",
            "Headline 4": "Buy Gift Cards Online",
            "Headline 5": "Award-Winning Day Spa",
            "Long headline 1": "Gift Mom a Spa Day — Massage & Facial Gift Cards at Spavia West Plano",
            "Long headline 2": "Mother's Day Spa Gift Cards — Order Online, Deliver by Email at Spavia",
            "Description 1": "Give mom the gift of relaxation. Spavia gift cards delivered by email. From $50.",
            "Description 2": "Massage, facials, skincare & spa packages. Gift cards available online at Spavia West Plano.",
            "Description 3": "The perfect last-minute Mother's Day gift. Order online and deliver instantly.",
            "Business name": "Spavia Day Spa",
            "Path 1": "gift-cards",
            "Path 2": "spa",
            "Final URL": "https://planotx.spaviadayspa.com/gift-cards?utm_campaign=2026-mothers-day",
            "Ad type": "Responsive display ad",
            "Status": "Enabled",
        },
    )

    set_fields(
        rda_in,
        ix,
        {
            "Ad Group#Original": LIVE_INMARKET_AG,
            "Ad Group": LIVE_INMARKET_AG,
            "Headline 1": "Mother's Day Spa Gift Cards",
            "Headline 2": "Spa Gift Cards From $50",
            "Headline 3": "Award-Winning Day Spa",
            "Headline 4": "Gift Cards Emailed Instantly",
            "Headline 5": "Pamper Mom This Year",
            "Long headline 1": "Give Mom a Spa Day — Gift Cards for Massage, Facials & Packages at Spavia West Plano",
            "Long headline 2": "Mother's Day Gift Cards — Massage, Facials & Spa Packages at Spavia Day Spa",
            "Description 1": "Order a Spavia gift card online. Delivered by email instantly. Mom picks her own treatment.",
            "Description 2": "Award-winning day spa in West Plano. Gift cards for massage, facials, and spa packages.",
            "Description 3": "Gift cards starting at $50. Valid for any service at Spavia Day Spa.",
            "Business name": "Spavia Day Spa",
            "Path 1": "mothers-day",
            "Path 2": "gift",
            "Final URL": "https://planotx.spaviadayspa.com/gift-cards?utm_campaign=2026-mothers-day",
            "Ad type": "Responsive display ad",
            "Status": "Enabled",
        },
    )

    clear_rda_location(rda_cu, ix)
    clear_rda_location(rda_in, ix)

    out_rows = [ag2, rda_cu, rda_in]

    for i, r in enumerate(out_rows):
        assert_row_width(h_new, r, f"row {i+2}")

    with OUT.open("w", encoding="utf-16", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(h_new)
        w.writerows(out_rows)

    print(f"Wrote {OUT} ({len(out_rows)} data rows + header), {len(h_new)} columns each.")


if __name__ == "__main__":
    main()
