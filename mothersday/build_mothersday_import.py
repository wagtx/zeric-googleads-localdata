# -*- coding: utf-8 -*-
"""Build mothersday-main-import.csv from Google Ads export; every row has 307 tab-separated fields."""

from __future__ import annotations

import csv
from copy import deepcopy
from pathlib import Path

ROOT = Path(r"c:\projects\repos\zeric-googleads-localdata")
EXPORT_NEW = ROOT / "exports" / "2026-04-12 1446.csv"
EXPORT_OLD = ROOT / "exports" / "2026-04-09 AfterImport-FullAccount.csv"
OUT = ROOT / "mothersday" / "mothersday-main-import.csv"

OLD_SEARCH = "2026-Search - Gift Cards (Mother's Day)"
NEW_SEARCH = "2026-Search - Gift Cards"
DISPLAY = "2026-Display - Gift Cards (Mother's Day)"
NETWORKS_SEARCH = "Google search;Search Partners"
BUDGET_SEARCH = "15.00"

# Valentine's Display block in 2026-04-09 export (0-based index into *data* rows from load_tsv = file line - 2).
VALentine_CAMPAIGN_IDX = 5849  # file line 5851
VALentine_AG1_IDX = 5850
VALentine_RDA1_IDX = 5851
VALentine_AG2_IDX = 5852
VALentine_RDA2_IDX = 5853
# Location row from current Search campaign (same coordinates as existing gift campaign).
SEARCH_LOCATION_LINE = 345  # 1-based file line in 2026-04-12 export


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


RSA_UPDATES: dict[str, dict] = {
    "Mother's Day Gift": {
        "headlines": [
            "Mother's Day At Spavia",
            "Pamper Mom This Year",
            "Spa Gift Cards Online",
            "The Perfect Gift For Mom",
            "Massage & Facial Gift Cards",
            "Award-Winning Day Spa",
            "Give Mom What She Deserves",
            "Gift Cards From $50",
            "Spavia West Plano Spa",
            "Spa Packages For Mom",
            "Treat Mom To A Spa Day",
            "Order Gift Cards Now",
            "Voted Best Spa In Plano",
            "Gift Cards Emailed Instantly",
            "Give The Gift Of Relaxation",
        ],
        "descriptions": [
            "Make Mother's Day special with Spavia gift cards for massage, facials & spa packages.",
            "Order a Spavia gift card online and have it delivered by email instantly. Mom chooses her own treat.",
            "Award-winning day spa in West Plano. Gift cards from $50 for any massage, facial, or spa service.",
            "Spa packages make the perfect Mother's Day gift. Give mom massage, facial & total relaxation.",
        ],
        "path1": "mothers-day",
        "path2": "gift",
        "url": "https://planotx.spaviadayspa.com/gift-cards?utm_campaign=2026-mothers-day",
        "pin_headlines": (1, 2, 3),
    },
    "Massage Gift Card": {
        "headlines": [
            "Massage Gift Cards Online",
            "Spavia Day Spa Plano",
            "Buy Massage Gift Cards",
            "The Perfect Gift For Mom",
            "Gift Cards Emailed Instantly",
            "Award-Winning Massage",
            "Give The Gift Of Relaxation",
            "Order Online Today",
            "Massage Gift Certificates",
            "Voted Best Spa In Plano",
            "Massages Starting At $119",
            "Signature Deep Tissue & More",
            "Gift Cards From $50",
            "Plano TX Massage Gifts",
            "Treat Someone You Love",
        ],
        "descriptions": [
            "Give a massage gift card from Spavia West Plano. Order online, delivered by email instantly.",
            "Massage gift cards for the perfect Mother's Day gift. Award-winning spa in West Plano.",
            "Skip the crowds. Order a massage gift card online and deliver it by email in minutes.",
            "Signature, deep tissue, couples, and hot stone massage. Gift cards valid for all treatments.",
        ],
        "path1": "gift-cards",
        "path2": "massage",
        "url": "https://planotx.spaviadayspa.com/gift-cards?utm_campaign=2026-mothers-day",
        "pin_headlines": (1, 2, 3),
    },
    "Spa Gift Card": {
        "headlines": [
            "Mother's Day Spa Gift Cards",
            "Spavia Day Spa Plano",
            "The Gift Of Relaxation",
            "Buy Spa Gift Cards Online",
            "Gift Cards Emailed Instantly",
            "Award-Winning Day Spa",
            "The Perfect Gift For Mom",
            "Massage & Facial Gift Cards",
            "Spa Gift Cards From $50",
            "Voted Best Spa In Plano",
            "Pamper Mom This Year",
            "Give Mom A Spa Day",
            "Valid For All Spa Services",
            "Plano TX Day Spa Gifts",
            "No Expiration On Gift Cards",
        ],
        "descriptions": [
            "Give mom the gift of relaxation this Mother's Day. Spa gift cards available online now.",
            "Spavia gift cards are valid for massages, facials, skincare, and all spa treatments.",
            "The perfect last-minute gift. Order a spa gift card now and deliver by email in minutes.",
            "Award-winning day spa in West Plano. Gift cards for massage, facials, and spa packages.",
        ],
        "path1": "gift-cards",
        "path2": "mothers-day",
        "url": "https://planotx.spaviadayspa.com/gift-cards?utm_campaign=2026-mothers-day",
        "pin_headlines": (1, 2, 3),
    },
    "Spa Packages": {
        "headlines": [
            "Mother's Day Spa Packages",
            "Spavia Day Spa Plano",
            "Give Mom A Spa Day",
            "Massage & Facial Packages",
            "Buy Spa Packages Online",
            "Award-Winning Day Spa",
            "Affordable Luxury Packages",
            "Order Online Today",
            "Packages Starting At $238",
            "Voted Best Spa In Plano",
            "Couples Packages Available",
            "The Complete Spa Experience",
            "Gift Cards For Any Package",
            "Plano's Favorite Day Spa",
            "Relaxation She'll Remember",
        ],
        "descriptions": [
            "Spa packages make the perfect Mother's Day gift. Massage, facial & relaxation packages.",
            "Give mom a complete spa day at Spavia West Plano. Packages from $238 for the full experience.",
            "Relax, Recenter, Renew, and Rejuvenate packages. Gift cards available for all packages.",
            "Award-winning West Plano day spa. Massage, facial & body treatment packages from $238.",
        ],
        "path1": "spa",
        "path2": "packages",
        "url": "https://planotx.spaviadayspa.com/spa-packages",
        "pin_headlines": (1, 2, 3),
    },
}

NEW_KEYWORDS: dict[str, list[tuple[str, str]]] = {
    "Mother's Day Gift": [
        ("mothers day gift card", "Phrase"),
        ("mothers day gift card", "Exact"),
        ("gift card for mom", "Phrase"),
        ("last minute mothers day gift", "Phrase"),
        ("mothers day spa near me", "Phrase"),
        ("spa day for mom", "Phrase"),
    ],
    "Massage Gift Card": [
        ("massage gift card for mom", "Phrase"),
        ("massage gift certificate near me", "Phrase"),
    ],
    "Spa Gift Card": [
        ("day spa gift certificate", "Phrase"),
        ("spa gift card for mothers day", "Phrase"),
    ],
    "Spa Packages": [
        ("spa package gift", "Phrase"),
        ("couples massage gift card", "Phrase"),
        ("spa day gift", "Phrase"),
    ],
}


def apply_rsa(row: list[str], ix: dict[str, int], spec: dict) -> None:
    for n, text in enumerate(spec["headlines"], start=1):
        row[ix[f"Headline {n}"]] = text
    for n, text in enumerate(spec["descriptions"], start=1):
        row[ix[f"Description {n}"]] = text
    row[ix["Path 1"]] = spec["path1"]
    row[ix["Path 2"]] = spec["path2"]
    row[ix["Final URL"]] = spec["url"]
    # Pin first N headlines
    pins = spec["pin_headlines"]
    for pi, hi in enumerate(pins, start=1):
        row[ix[f"Headline {hi}#Original"]] = spec["headlines"][hi - 1]
        row[ix[f"Headline {hi} position"]] = str(pi)
    row[ix["Description 1#Original"]] = spec["descriptions"][0]
    row[ix["Description 1 position"]] = "1"


def build_search_block(h_new: list[str], rows_new: list[list[str]]) -> list[list[str]]:
    ix = col_index(h_new)
    camp_col = ix["Campaign"]
    block = [deepcopy(r) for r in rows_new if r[camp_col].strip() == OLD_SEARCH]
    if not block:
        raise RuntimeError(f"No rows found for campaign {OLD_SEARCH!r}")

    for r in block:
        replace_campaign_name(r, ix, OLD_SEARCH, NEW_SEARCH)

    # Campaign-level row: has Campaign Type = Search
    ct_col = ix["Campaign Type"]
    for r in block:
        if r[ct_col].strip() == "Search":
            r[ix["Budget"]] = BUDGET_SEARCH
            r[ix["Networks"]] = NETWORKS_SEARCH
            break

    # Insert new keywords before each RSA; patch RSA assets
    out: list[list[str]] = []
    i = 0
    while i < len(block):
        r = block[i]
        adt = r[ix["Ad type"]].strip()
        ag = r[ix["Ad Group"]].strip()
        if adt == "Responsive search ad" and ag in NEW_KEYWORDS:
            # template = previous row if it looks like a keyword
            tmpl = block[i - 1]
            if not (tmpl[ix["Keyword"]].strip() and tmpl[ix["Criterion Type"]].strip()):
                raise RuntimeError(f"No keyword template before RSA for {ag}")
            for kw_text, match_type in NEW_KEYWORDS[ag]:
                nr = deepcopy(tmpl)
                nr[ix["Keyword#Original"]] = kw_text
                nr[ix["Keyword"]] = kw_text
                nr[ix["Criterion Type#Original"]] = match_type
                nr[ix["Criterion Type"]] = match_type
                out.append(nr)
            spec = RSA_UPDATES.get(ag)
            if spec:
                apply_rsa(r, ix, spec)
        out.append(r)
        i += 1

    return out


def build_display_rows(h_new: list[str], rows_new: list[list[str]], h_old: list[str], rows_old: list[list[str]]) -> list[list[str]]:
    ix_new = col_index(h_new)
    # rows_new[0] is file line 2 -> file line L is rows_new[L - 2]
    loc_template = deepcopy(rows_new[SEARCH_LOCATION_LINE - 2])

    def proj(idx_old: int) -> list[str]:
        return project_row(rows_old[idx_old], h_old, h_new)

    campaign = proj(VALentine_CAMPAIGN_IDX)
    ag1 = proj(VALentine_AG1_IDX)
    rda1 = proj(VALentine_RDA1_IDX)
    ag2 = proj(VALentine_AG2_IDX)
    rda2 = proj(VALentine_RDA2_IDX)
    location = deepcopy(loc_template)

    for r in (campaign, ag1, rda1, ag2, rda2, location):
        replace_campaign_name(r, ix_new, OLD_SEARCH, DISPLAY)  # no-op unless OLD in cell
        for key in ("Campaign#Original", "Campaign"):
            c = ix_new[key]
            if r[c] and "Valentine" in r[c]:
                r[c] = DISPLAY
            elif not r[c].strip() and key == "Campaign":
                r[c] = DISPLAY

    # Campaign row fields (match intended import)
    c = campaign
    set_fields(
        c,
        ix_new,
        {
            "Campaign#Original": DISPLAY,
            "Campaign": DISPLAY,
            "Campaign Type": "Display",
            "Networks": "Display Network",
            "Budget": "10.00",
            "Budget type": "Daily",
            "Languages": "en",
            "Bid Strategy Type": "Maximize clicks",
            "Enhanced CPC": "Disabled",
            "Maximum CPC bid limit": "1.50",
            "Broad match keywords": "Off",
            "Ad rotation": "Optimize for conversions",
            "Content exclusions": "[]",
            "Targeting method": "Location of presence",
            "Exclusion method": "Location of presence",
            "Campaign Status": "Enabled",
            "Ad Group": "",
            "Ad Group#Original": "",
        },
    )

    # Location: same as Search gift campaign location row
    location[ix_new["Campaign#Original"]] = ""
    location[ix_new["Campaign"]] = DISPLAY
    for key in ("Campaign Type", "Ad Group"):
        location[ix_new[key]] = ""

    # Ad group 1: In-Market
    set_fields(
        ag1,
        ix_new,
        {
            "Ad Group#Original": "Display - In-Market Gifts & Spa",
            "Ad Group": "Display - In-Market Gifts & Spa",
            "Max CPC": "0.75",
            "Age demographic": "25-34;35-44;45-54",
            "Interest categories": "",
            "Ad Group Status": "Enabled",
        },
    )

    # RDA 1
    set_fields(
        rda1,
        ix_new,
        {
            "Ad Group#Original": "Display - In-Market Gifts & Spa",
            "Ad Group": "Display - In-Market Gifts & Spa",
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

    # Ad group 2: Custom intent / searchers
    set_fields(
        ag2,
        ix_new,
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
        rda2,
        ix_new,
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

    for r in (rda1, rda2):
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
            r[ix_new[k]] = ""

    return [campaign, location, ag1, rda1, ag2, rda2]


def main() -> None:
    h_new, rows_new = load_tsv(EXPORT_NEW)
    h_old, rows_old = load_tsv(EXPORT_OLD)

    search_block = build_search_block(h_new, rows_new)
    display_block = build_display_rows(h_new, rows_new, h_old, rows_old)

    all_rows = search_block + display_block
    for i, r in enumerate(all_rows):
        assert_row_width(h_new, r, f"row {i+2}")

    with OUT.open("w", encoding="utf-16", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(h_new)
        w.writerows(all_rows)

    print(f"Wrote {OUT} ({len(all_rows)} data rows + header), {len(h_new)} columns each.")


if __name__ == "__main__":
    main()