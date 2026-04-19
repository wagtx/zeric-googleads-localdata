# Eulerity Data & Approach — Baseline Analytical Report

> **Subject:** Spavia Day Spa – West Plano  
> **Report date:** 2026-04-18  
> **Author:** Eric Pearson (Zeric), with analysis assisted by Cursor + Claude  
> **Scope:** Full evaluation of the Eulerity data export, comparison against the current in-house Google Ads approach, assessment of the Eulerity model's fit for market-specific adaptation, and documentation of the tooling/workflow now being used.  
> **Purpose:** Baseline "everything" document. Targeted reports (franchisor brief, vendor change memo, ROI recovery plan, etc.) can be derived from this.

---

## 0. Executive summary

- The `EulerityData/` export is a **configuration and keyword archive**, not a performance record. It contains nothing that can measure revenue, conversions, cost per action, or trend. Those dimensions exist inside Eulerity's UI (see screenshots: daily time-series for Ads Displayed, Clicks, CTR, and Budget) but were not shipped in the CSV export we received.
- The **Eulerity campaign type for Spavia's headline campaign is `Maximize Traffic & Drive Engagement`**, not Maximize Conversions. That is a structural choice, not a data gap — the vendor is optimizing for **clicks and engagement** rather than bookings or gift-card revenue. This single fact reframes most of the performance conversation.
- Eulerity's model is a **franchise-friendly omnichannel blueprint**: standardized campaign templates (FTVO, Seasonal Gift Card, etc.) that run across Google Search, Google Display, Facebook, Instagram, and LinkedIn in one unit, with automated seasonal refresh (last year's Mother's Day campaign is retired and replaced by a new one each year — the absence of "Mother's Day 2026" in the export reflects our April 9 disengagement, not a change in vendor practice).
- The in-house 2026 rebuild is the **deliberate opposite**: Search-first, per-service campaigns, tight ad-group-to-keyword alignment, explicit conversion signals (GA4 purchase + QBO reconciliation), and every artifact version-controlled in git so future decisions are auditable.
- Eulerity is **appropriate** for owners who need turnkey omnichannel presence with no in-house ad ops, especially single-location operators and franchisees who value consistency over per-market optimization. It is **inappropriate** where (a) the owner needs ROAS-level attribution to a specific revenue line (e.g., gift cards), (b) there is meaningful market-to-market variation that merits custom structure, or (c) there is internal capacity (or tooling, as documented in §10) to run the account directly.
- Our tooling — Cursor + Claude agents, dated Google Ads Editor TSV snapshots, shape-aware CSV generators, shared `enums.json` validators, playbook + decisions-log docs, and Python utilities for audience/customer-list merges — makes the DIY path reproducible and auditable in a way the vendor dashboard is not.

---

## 1. Scope and evidence base

### Files evaluated in `EulerityData/`

| File | Bytes | SHA-256 (prefix) | Rows (data) | Role |
|---|---:|---|---:|---|
| `Settings.csv` | 6,003 | `166DEE22…` | 5 | Campaign setup, targeting, subscription status |
| `Performance.csv` | 1,605 | `3A596787…` | 5 | Lifetime totals by channel (clicks, CPC, CPM, CTR, impressions, budgeted spend, FB leads) |
| `Performance (1).csv` | 1,605 | `3A596787…` | 5 | **Byte-identical duplicate** of `Performance.csv` |
| `Distribution.csv` | 1,368 | `F742B2C4…` | 5 | Percent mix of clicks/impressions by age, gender, device, channel |
| `Distribution (1).csv` | 1,368 | `F742B2C4…` | 5 | **Byte-identical duplicate** of `Distribution.csv` |
| `Connections.csv` | 2,930 | `CD727BF9…` | 5 | Integration inventory (FB, IG, GA4, GBP, LinkedIn, X) |
| `Connections (1).csv` | 2,930 | `CD727BF9…` | 5 | **Byte-identical duplicate** of `Connections.csv` |
| `keywords-by-keyword.csv` | 158,769 | `199390E4…` | 737 | One row per keyword × match type × polarity, listing which campaigns include it |
| `keywords-by-campaign & blueprint.csv` | 34,526 | `17DD79FA…` | 30 | One row per campaign × match type × polarity, comma-separated term list |

The three `(1)` files are exact duplicates of their counterparts (verified via SHA-256), consistent with Windows "file already exists" auto-renaming.

### Additional evidence from Eulerity's UI (screenshots supplied)

- **Campaign header (FTVO Massage Only):** Primary Campaign of Spavia – West Plano. Paused since Apr 9, 2026. Initial Activation Apr 15, 2022 (1,463 days). Call Tracking Number `+1 469 960 4367` (vendor-provisioned proxy, not the spa's published 469-304-9444). Connected Platforms: Facebook, Instagram, Google Analytics, LinkedIn. Advertising Channels: **Google** and **Facebook and Instagram**.
- **Campaign Type (visible in UI, not in export):** `Maximize Traffic & Drive Engagement`.
- **Metrics and Performances tab with time-series charts:**
  - Ads Displayed 11/4/2025–4/17/2026: **420,140**; Lifetime **6,933,595**; Last 30 days **44,968**; Yesterday 0 (paused).
  - Clicks 11/4/2025–4/1/2026: **9,582**; Lifetime **134,919**; Last 30 days **1,443**; Yesterday 0.
  - CTR 11/4/2025–4/1/2026: **2.361%**; Lifetime **1.946%**; Last 30 days **3.209%**; Yesterday 0%.
  - Advertising Budget 4/11–4/17/2026: **$0.00** (paused); Lifetime **$103,354.98**; Last 30 days **$1,656.74**.
  - A `Download CSV` button exists per metric tab (so daily time-series data is obtainable from Eulerity on demand, but was **not** delivered with the CSV export we received).
- **Existing Google Audience Segments attached to Spavia – West Plano campaigns** (visible in the "Create New Audience Segments" page):
  - **In-Market:** Gifts & Occasions, Personalized Gifts, Gift Baskets, Valentine's Day Items & Decor, Beauty & Personal Care, Skin Care Products, Spas & Beauty Services, Anti-Aging Skin Care Products, Christmas Shopping, Online Christmas Shopping.
  - **Affinity:** Health & Fitness Buffs, Beauty Mavens, Yoga Lovers, Beauty & Wellness.
  - Each segment is scoped to either "Google Display & Google Search Campaigns", "Only Google Display", or "Only Google Search Campaigns".
- **Omni Ads creative panel:** 6 deployed Omni Ads (static image+text, Created Sep 11, 2025). A Dynamic Ad Preview shows per-network rendering (Instagram/Facebook/Web/GBP/Google), with metrics summaries at 7/30/90 days (example: the "First Visit – Save $30" ad: 0 / 2,414 / 11,247 ads shown; 0 / 126 / 558 clicks; 0% / 5.22% / 4.96% CTR at those windows). Search ad headlines/descriptions are machine-assembled (five headlines + four descriptions per Responsive Search Ad).

### Corrective note on seasonal campaigns

An earlier reading suggested seasonal campaigns accumulated under Eulerity. That is incorrect: **Eulerity replaces seasonal campaigns each year**, so the absence of a "Mother's Day 2026" campaign in this export reflects the April 9 disengagement, not a vendor practice change. The "DO NOT USE: Spavia – West Plano Gift Cards" campaign is a separate legacy container that was retained but marked inactive.

### Out-of-folder evidence used for the DIY-side analysis

- `imports/2026-04-09 FirstTake/2026-spavia-google-ads-playbook.md` — current operational north star.
- `spavia-google-ads-decisions-2026-04-12.md` — 12-hour post-launch audit.
- `exports/2026-04-12 EOD/EVALUATION-*.md` — 36-hour evaluation set (strategy, negatives, landing pages & QS, ad copy, cross-check).
- `temp/KEYWORDS-evaluation.md` — gift-card keyword decisions.
- `mothersday/mothers-day-gift-card-playbook.md` — current Mother's Day campaign playbook.
- `AGENTS.md`, `DECISIONS-ImportFile.md` — agent operating rules and import discipline.
- `c:\projects\repos\sugarhill-googleads-localdata\` — sibling account using the same tooling, read for tooling context only.

---

## 2. What Eulerity is, as represented in this data

### The product, based on the artifacts

- **Managed-service, white-label omnichannel advertising** built on top of Google Ads (Search + Display), Meta (Facebook + Instagram), and ancillary connections (GBP, LinkedIn, X).
- **Campaign unit = "Blueprint"**: each Eulerity "campaign" is a multi-channel template that publishes to all configured networks simultaneously, with the same offer, creative pool, and keyword set. Inside the Eulerity dashboard it appears as one campaign; on the back end it corresponds to many Google Ads and Meta campaigns living inside Eulerity's own MCCs.
- **Campaign type:** `Maximize Traffic & Drive Engagement` (shown in the UI header). The optimization objective is **clicks and engagement** — not conversions, not conversion value, not leads, not revenue. This is consistent with what we see in the data: CPMs are high ($12–$287), CTRs are normal (1–9% depending on channel), and `Facebook Leads: Total` is `N/A` on every row.
- **Creative production:** Eulerity generates "Omni Ads" — multi-aspect-ratio static creatives (6 deployed for Spavia). A Responsive Search Ad variant is also generated, with five headlines and four descriptions per ad, assembled from templates ("Limited-Time Spa Offer Today", "Relaxation Starts at Spavia", etc.).
- **Audience layer:** in-market and affinity segments are attached to each campaign (gift-occasion segments on the seasonal campaigns; beauty/wellness/fitness segments on the always-on service campaigns). These do not appear in the CSV export but are visible in the UI.
- **Call tracking:** each campaign gets a unique proxy number (`+1 469 960 4367` for FTVO Massage), which forwards to the spa's real line and attributes the call to the Eulerity campaign.
- **Seasonal rotation:** gift-card campaigns are retired and replaced annually (Winter Holiday, Valentine's, Mother's Day, Father's Day). The owner does not have to design the seasonal creative or keyword list; Eulerity swaps them automatically.

### What you sign up for, implicitly

- Campaign structure is **chosen for you** at the Spavia-system level (FTVO Facial, FTVO Massage, Seasonal Gift Card). You cannot restructure it without leaving the blueprint.
- Bid strategy is **fixed** at Maximize Traffic. There is no exposed lever for Max Conversions, Target CPA, or Target ROAS.
- Budget is represented at the Eulerity-campaign level only (no per-channel or per-ad-group control exposed in the UI we can see).
- The Google Ads account is owned by Eulerity's MCC. You never have a Google-side account that survives disengagement.
- Reporting is whatever the Eulerity dashboard surfaces. The CSV export we received is a **subset** of what the dashboard itself renders.

---

## 3. Inventory of what the export actually contains

### 3.1 `Settings.csv` — what ran and how it was targeted

5 rows, 19 columns. One row per campaign:

| Campaign | Type | Status | Activation | Renewal |
|---|---|---|---|---|
| Spavia – West Plano: FTVO Facial Only | Secondary | Paused | Sep 11, 2025 | May 11, 2026 |
| West Plano – Valentine's Day Gift Card | Secondary | Paused | Jan 20, 2026 | Apr 20, 2026 |
| West Plano – Winter Holiday Gift Card | Secondary | Canceled | Nov 11, 2025 | Apr 11, 2026 |
| Spavia – West Plano: FTVO Massage Only | **Primary** | Paused | Apr 15, 2022 | Apr 30, 2026 |
| DO NOT USE: Spavia – West Plano Gift Cards | Secondary | Canceled | Nov 10, 2022 | Aug 30, 2025 |

Additional columns in each row: `Advertising Name`, `Default Landing Page` (single URL per campaign), `Labels`, business address, billing (`Paid By: Business Owner`), subscription amount (`N/A`), plus audience dials:

- **Age** (multi-select): typical pattern `25-34, 35-44, d, 55-64, 65+` (the `d` appears to be a UI-collapsed "45-54" — worth confirming with Eulerity; it reads identically across rows).
- **Parents:** `Parent, Not Parent`.
- **Gender:** `Male, Female`.
- **Income Targets:** `Modest, Comfortable, Affluent`.
- **Geolocation Targets:** explicit list of **15 Plano/Frisco/Carrollton ZIPs** (75093, 75056, 75024, 75023, 75025, 75287, 75075, 75007, 75010, 75034, 75035, 75252, 75074, 75070, 75068).
- **Georadius Targets:** `Radius: 5mi. (33.029,-96.827)` for all except the legacy gift card campaign at 7mi.

**What this tells us:** targeting is essentially a **template** applied identically across campaigns (same age/gender/parent/income dial settings, same 15-ZIP list, same 5-mile radius). The only per-campaign variation is the **labels** and **default landing page**.

### 3.2 `Performance.csv` — lifetime channel totals

5 rows, 30 columns. Covers **only** lifetime cumulative numbers from activation to export date. Example (FTVO Massage Only, activated Apr 15 2022):

| Column | Value |
|---|---|
| Clicks: Total | 134,919 |
| Clicks: Display / Search / Social / Video | 56,089 / 43,666 / 35,164 / N/A |
| CPC: Total / Display / Search / Social | $0.77 / $0.30 / $1.37 / $0.76 |
| CPM: Total / Display / Search / Social | $14.91 / $4.12 / $103.59 / $12.03 |
| CTR: Total / Display / Search / Social | 1.95% / 1.35% / 7.58% / 1.59% |
| Impressions: Total / Display / Search / Social | 6,933,595 / 4,145,656 / 575,901 / 2,212,038 |
| Budgeted Spend: Total | $103,354.98 |
| Facebook Leads: Total | **N/A** |

Observations:

- **No video channel ever produced for Spavia** (all Video columns `N/A`). Either video was never part of the blueprint for this account or it was never funded.
- **Display dominates impressions** (60% of total) at very cheap CPM ($4.12), with modest CTR (1.35%).
- **Search delivers the best CTR** (7.58%) but at a **very expensive CPM** ($103.59), meaning the Search portion is a small, high-intent slice.
- **Social (Facebook + Instagram)** sits in between: 2.2M impressions, 1.59% CTR, $12.03 CPM.
- **Zero lead/conversion data** exported. `Facebook Leads: Total = N/A` on every row, despite Facebook being "Connected" with advertising and posting access.

### 3.3 `Distribution.csv` — percent mix of clicks and impressions

5 rows, 29 columns. All values are percentages (strings with `%` suffix). Dimensions:

- Clicks by age bracket (18-24, 25-34, 35-44, 45-54, 55-64, 65+).
- Impressions by age bracket (same).
- Clicks and Impressions by gender (Male/Female).
- Clicks and Impressions by device (Desktop/Mobile/Tablet).
- Clicks and Impressions by channel (Display/Search/Social/Video).

Example (FTVO Massage Only):

| Dimension | Breakdown |
|---|---|
| Clicks by age | 5% / 17% / 18% / 19% / 22% / 19% |
| Impressions by age | 10% / 23% / 20% / 18% / 18% / 11% |
| Clicks by gender | 41% M / 59% F |
| Impressions by gender | 44% M / 56% F |
| Clicks by device | 8% Desktop / 86% Mobile / 6% Tablet |
| Impressions by device | 5% Desktop / 88% Mobile / 7% Tablet |
| By channel (clicks) | 17% Display / 58% Search / 26% Social / 0% Video |

Observations:

- **Very mobile-heavy** (86% of clicks). Consistent with local-service search behavior.
- **Clicks skew slightly older** than impressions (18-24 gets 10% of impressions but only 5% of clicks for FTVO Massage; 45+ over-indexes on clicks), suggesting the older audience is higher-intent but the impression feed isn't tuned that way.
- The "DO NOT USE" legacy gift card campaign served **9% Display / 70% Search / 21% Social** — mostly Search, which is unusual for a Eulerity blueprint and may reflect a different era of configuration.
- **Percentages cannot be joined back to `Performance.csv` totals** safely — there is no cross-tab (e.g., clicks from 25-34 females on mobile is not recoverable).

### 3.4 `Connections.csv` — integration inventory

5 rows, 25 columns. Per campaign, the connection state of Facebook (page ID, access, lead form), GA4 (account/property IDs, property name, data filters), Google Business Profile, Instagram (handle, access), LinkedIn, and X.

- **Facebook:** Connected to page ID `329385907257572`, with advertising and posting access. No lead form attached.
- **GA4:** Connected to account `90877988` / property `303576480` ("Corporate – GA4" under account "Spavia Day Spa"). **Data Filters** column shows a JSON expression `[{"fieldName":"pageTitle","value":"West Plano","type":"contains"}]` — Eulerity segments corporate GA4 data by page-title heuristic, not by a dedicated property. (One row has a lowercase `pagetitle`, suggesting inconsistent filter entry.)
- **GBP:** Not Connected across all campaigns — a surprising gap given GBP drives map-pack clicks and directions requests for local businesses.
- **Instagram:** Connected as `spaviawestplano` with advertising/posting access on every row.
- **LinkedIn / X:** Not Connected (X reports N/A landing page).

**Signal:** Eulerity is reading GA4 as a shared corporate property filtered by page-title contains "West Plano", which is a weaker attribution primitive than a dedicated GA4 property. It means any GA4-based metrics Eulerity surfaces for this location depend on whether the franchisor's pages correctly include "West Plano" in the title — brittle at best.

### 3.5 `keywords-by-keyword.csv` — 737 rows of keyword blueprint

Columns: `Keyword, Match Type, Polarity, Campaign 1, Campaign 2, …`. One row per keyword × match type × polarity. The wide, variable-length columns list which `Business (Campaign)` instances the keyword is attached to.

- **Polarities:** "Negative" (vast majority) and "Positive".
- **Match types:** BROAD, PHRASE, EXACT.
- **Campaigns referenced:** includes `DO NOT USE: Spavia - Plano Esthetician Services` — a campaign **not** present in `Settings`, `Performance`, `Distribution`, or `Connections`. This inconsistency suggests the keyword blueprint spans more campaigns than are active in the operational export, or the operational export excludes fully-retired campaigns while the keyword blueprint retains them.
- **Shared negative patterns:** near-identical ~200-term "Do Not Show" blocks replicated per campaign (e.g., the same "booty / bikini / massage school / happy ending / botox / dermaplaning" block appears in FTVO Facial, FTVO Massage, both seasonal gift cards, and the DO NOT USE legacy campaign).
- **Positive keyword groupings:** service-themed blocks per campaign (e.g., "facial spa / day spa / microdermabrasion / hydrafacial / spavia / best facial" on FTVO Facial; "deep tissue massage / couples massage / massage plano" on FTVO Massage; gift-occasion blocks on the seasonal campaigns).

### 3.6 `keywords-by-campaign & blueprint.csv` — 30 wide rows

Same information, pivoted: one row per `Campaign × Match Type × Polarity`, with the term list in the remaining columns. Easier to eyeball per-campaign, harder to machine-process.

### 3.7 What is absent (and matters for performance)

| Missing | Why it matters |
|---|---|
| **Conversions / bookings / leads** | Impossible to compute CPA, conversion rate, or ROI from this file. `Facebook Leads: Total = N/A` everywhere. |
| **Revenue** | No per-campaign gift-card or service-booking revenue; no ROAS. |
| **Time series** | Every number is lifetime-cumulative. No month-over-month, no YoY, no seasonality curve, no pre/post-COVID comparison. (Daily series **does** exist in Eulerity's UI — see §1 — but was not exported.) |
| **Per-keyword performance** | The keyword CSVs show blueprint membership only. No clicks, impressions, cost, or conversion per keyword. |
| **Search-terms report** | No visibility into what actual queries matched the blueprint, which is the single most important data source for negative-keyword work. |
| **Creative performance** | The Omni Ads panel shows 0/2,414/11,247 impressions by ad (7/30/90 days) in the UI but the export has nothing per-ad. |
| **Quality Score / ad strength** | No Google QS signals, no ad-strength ratings, no impression-share or auction-insights data. |
| **Geo performance** | Only the 15 ZIPs and 5mi radius are given as targets. No per-ZIP spend or conversion. |
| **Budget pacing / burn rate** | Only lifetime `Budgeted Spend: Total`. No daily cap, no fee-vs-media split, no pacing curve. |
| **Audience layer details** | The in-market and affinity segments visible in the UI (Gifts & Occasions, Yoga Lovers, Beauty Mavens, etc.) are not in the export. |
| **Call tracking detail** | Call tracking number is visible in the UI; **call volume, call duration, call recordings, or call-to-booking conversion** are not in the export. |
| **GCLID / attribution chain** | No click IDs, no offline conversion import history, no attribution-model notes. |

### 3.8 Internal inconsistencies

- `DO NOT USE: Spavia – Plano Esthetician Services` appears in the keyword files but not in the operational files.
- The `Age` field encodes one bracket as `d` instead of a readable value.
- One GA4 `Data Filters` row uses lowercase `pagetitle` while others use camelCase `pageTitle`.
- Duplicate files (`*(1).csv`) inflate the file count without adding data.

---

## 4. How useful is this data for evaluating performance?

### 4.1 Summary rating

| Use case | Rating | Why |
|---|---|---|
| Confirm what campaigns ran and when | **Strong** | `Settings.csv` is clean and unambiguous. |
| Confirm targeting config (geo, demo, income) | **Strong** | All parameters present. |
| Harvest negative keywords for the new Shared Library | **Very strong** | ~700 curated, match-typed negatives — a major time-saver. |
| Benchmark CTR/CPC by channel | **Moderate** | Lifetime averages only; no seasonality or day-of-week. |
| Evaluate gift-card campaign ROI | **Impossible** | No conversion or revenue data. |
| Evaluate service-booking performance | **Impossible** | Same reason. |
| Evaluate creative performance | **Impossible** | No per-ad data. |
| Diagnose Quality Score drag | **Impossible** | No QS, no ad-strength, no LP-experience metrics. |
| Decide next year's budget allocation | **Weak** | Only lifetime totals, no YoY. Must be combined with QBO revenue. |
| Replace our in-house Editor exports | **No** | Our exports carry QS, impression share, search terms, and per-keyword stats — this does not. |

### 4.2 Why the gaps exist (charitable read)

Eulerity's target customer is a busy single-location or multi-location owner who wants a **monthly "are we running" answer**, not a **weekly "what do we change" answer**. The CSV export is designed around the former:

- Settings snapshot: answers *"what did I pay for?"*
- Lifetime Performance: answers *"how much did that produce in total?"*
- Distribution: answers *"who's seeing it?"*
- Connections: answers *"which accounts are linked?"*
- Keywords: answers *"what are my blueprints made of?"*

None of these require (or allow) weekly optimization decisions. That is consistent with the **Maximize Traffic** campaign type: if you're not optimizing toward conversions, you do not need conversion data to run the playbook.

### 4.3 Why the gaps matter for Spavia specifically

Spavia's strategic question is not "are we running ads" — it is "are ads recovering the ~$88k/yr of gift-card revenue that disappeared between 2019 and 2025" (see `imports/2026-04-09 FirstTake/2026-spavia-google-ads-playbook.md`). Answering that requires:

- **Revenue attribution by campaign and month** — not available.
- **Ad spend by campaign and month** — not available at monthly granularity (the UI has it; the export does not).
- **Year-over-year comparison across the Eulerity tenure (2022–2026)** — not available.
- **A conversion-optimized campaign objective** — not the Eulerity default.

Without those, every claim about "ads worked" or "ads underperformed" during the Eulerity era will be argued from indirect evidence (QBO revenue ÷ Eulerity fee) rather than from campaign-level performance.

### 4.4 What to use this data for anyway

1. **Mine ~700 negatives** into our `Master Negatives` shared list (dedupe against existing 1,003-term list; preserve match type). High-value block keywords include competitor names, adult-intent terms, beauty-school terms, DIY terms, and known waste (`airbnb`, `academy`, `barber mehmet`, `booty`, etc.).
2. **Baseline demographic priors** for observation audiences and bid adjustments:
   - Mobile-first (86% of clicks).
   - Female-leaning on services (59% F on FTVO Massage, 59% F on FTVO Facial; Winter Holiday Gift skewed 59% F in impressions, 59% clicks).
   - Age skew varies by offer (Valentine's heavily 18-34, FTVO Massage 45-64+).
3. **Sanity-check channel CTRs** — anything below Eulerity's Display CTR of 1.3–1.6% on our new PMAX/Display work is suspect; anything above 7% Search CTR is in line with historical norms.
4. **Confirm the integration checklist** (Facebook page ID, Instagram handle, GA4 property, GBP status) matches our own account configuration.
5. **Archive `Settings.csv`** as the historical record of what the franchise blueprint looked like under Eulerity, in case a successor vendor or the franchisor wants to reconstruct it.

---

## 5. The in-house 2026 approach (reference)

See `imports/2026-04-09 FirstTake/2026-spavia-google-ads-playbook.md` for the full playbook; summary here.

### 5.1 Account ownership

- Google Ads account `973-759-8969` lives under `eric@pearsonhome.org`, inside our own MCC.
- All campaign changes are made via the **Google Ads Editor** using versioned TSV import files in `imports/` or built by `mothersday/build_mothersday_import.py`.
- Exports are captured as dated TSVs in `exports/` (e.g., `2026-04-17 2337 SearchTerms17th.csv`, `2026-04-12 EOD/2026-04-12 EOD AllExport.csv`). These are immutable snapshots — we never edit them.

### 5.2 Campaign structure (launched 2026-04-11)

| Campaign | Type | Daily budget | Bid strategy | Geo | Networks |
|---|---|---|---|---|---|
| 2026-Search – Massage & Spa | Search | $30 (later $35) | Maximize Conversions | 10mi radius | Google Search only |
| 2026-Search – Facials & Skincare | Search | $12 | Maximize Conversions | 10mi radius | Google Search only |
| 2026-Search – Waxing | Search | $5 | Maximize Clicks ($3 max CPC) | 10mi radius | Google Search only |
| 2026-Search – Gift Cards (Mother's Day) | Search | $10 → $30 surge | Manual CPC | 20mi radius | Google Search + Partners |
| 2026-PMAX – First Visit Offer | Performance Max | $10 (later $5) | Maximize Conversions | 10mi | All | *paused until 60d of Search conversion data* |

Future seasonal campaigns (Holiday, Valentine's, Father's Day) are calendar-driven with explicit build/activate/peak/pause dates.

### 5.3 Bid strategies

- **Services:** Maximize Conversions, enabled only after the GA4 `purchase` conversion action was imported with $119 per-conversion value.
- **Waxing:** Maximize Clicks with $3 cap, pending enough volume to justify conversion bidding.
- **Gift Cards:** Manual CPC. Rationale: the franchise gift-card purchase flow does **not** fire a GA4 `purchase` event, so automated bidding would optimize toward the wrong signal. Gift-card ROAS is measured out-of-band against QBO P&L line 44100 (Gift Card Sales).
- **PMAX:** paused until at least 60 days of conversion data exist on the Search side.

### 5.4 Conversion tracking

- `Spavia Day Spa - West Plano - GA4 (web) purchase` imported as **Primary** under the Purchases goal.
- Per-conversion value **$119** (weighted average of top-5 booked services).
- Old Universal-Analytics `Healcode Confirmation` action retired; duplicate phone-call actions demoted to Secondary.
- **Known gap:** gift-card purchases don't fire GA4 events. Three planned workarounds: (a) franchise-platform engineering to add a `purchase` event on `/gift-cards`, (b) UTM-parameter attribution (`?utm_campaign=2026-mothers-day`) at the GA4 session level, (c) offline conversion upload matching GCLIDs to QBO line 44100.

### 5.5 Keyword structure

- **Tight ad-group-to-keyword alignment.** The Massage & Spa campaign contains Massage Near Me, Couple's Massage, Deep Tissue, Hot Stone/Salt Stone, Day Spa, Brand. Each ad group has a narrow set of Phrase + Exact keywords plus a matching RSA.
- **Shared Negative Keyword Lists** in the Shared Library:
  - `Master Negatives` — ~1,003 terms migrated from outgoing `[CM]` vendor campaigns, applied to all five `2026-` campaigns.
  - `Gift Card Filter` — ~12 terms (`gift card`, `gift certificate`, `mothers day`, etc.) applied only to the three service campaigns to keep gift-intent traffic from eating service budget.
- Weekly search-terms review for the first 60 days; new negatives feed the shared list.

### 5.6 Landing page strategy

| Ad group type | Final URL |
|---|---|
| Massage (general) | `/massage` (changed from `/first-visit-offer` to fix Landing Page Experience QS) |
| Couples Massage | `/plano-tx/massage/couples-massage/` |
| Day Spa | `/` (homepage) |
| Facials / Skincare | `/skin-care` |
| Waxing | `/beauty` |
| Gift Cards | `/gift-cards?utm_campaign=2026-mothers-day` |
| Brand | `/` |

Franchise CMS content cannot be edited; URL selection is the only QS lever available.

### 5.7 Budget plan

Annual ~$59k (the 2017–2019 historical baseline), redistributed by month to match seasonal intent:

| Month | Monthly | Primary focus |
|---|---:|---|
| Jan | $3,500 | Valentine's ramp |
| Feb | $6,000 | Valentine's peak |
| Mar | $3,500 | Baseline |
| Apr | $5,000 | Mother's Day ramp (gift cards activate Apr 15) |
| May | $6,000 | Mother's Day peak |
| Jun | $4,000 | Father's Day + baseline |
| Jul–Sep | $3,500 ea | Baseline |
| Oct | $4,000 | Holiday ramp |
| Nov | $6,500 | Holiday surge |
| Dec | $10,000 | Holiday peak |

Within-campaign reallocation is driven by Google's `Lost to Rank` vs `Lost to Budget` diagnostics — a metric not surfaced by Eulerity.

### 5.8 Documentation and audit trail

- **`imports/2026-04-09 FirstTake/2026-spavia-google-ads-playbook.md`** — operational north star.
- **`spavia-google-ads-decisions-2026-04-12.md`** — 12-hour post-launch audit (QS analysis, bid diagnostics, decisions taken).
- **`exports/2026-04-12 EOD/EVALUATION-*.md`** — 36-hour evaluation suite (strategy & structure; landing pages & QS; negatives; ad copy & sitelinks; cross-check decisions log).
- **`mothersday/mothers-day-gift-card-playbook.md`** — season-specific playbook.
- **`DECISIONS-ImportFile.md`** — teaching doc for Editor-import discipline.
- **`AGENTS.md`** — operational rules so AI agents and humans read the same playbook.

---

## 6. Side-by-side comparison

| Dimension | Eulerity (as shown in this data + UI) | Zeric / in-house 2026 approach |
|---|---|---|
| Account ownership | Ran in Eulerity's MCC. Nothing survives disengagement. | Own MCC `973-759-8969`, fully portable. |
| Campaign unit | "Blueprint" spanning Search + Display + Facebook + Instagram. | Per-intent campaign, per-channel (Search-only, PMAX separate). |
| Optimization objective | **Maximize Traffic & Drive Engagement** (clicks/engagement). | **Maximize Conversions** (services) / **Manual CPC** (gift cards) / **Max Clicks** (waxing). |
| Channel mix | Always-on omnichannel; Display ~60% of impressions, Search ~8%, Social ~32%. | Search-first; PMAX paused until Search conversions accumulate; Display not yet deployed. |
| Creative | 6 Omni Ads + template-assembled RSAs, centrally produced. | Per-ad-group RSAs, tuned for ad-strength and search-query mirroring; creative production is in-house. |
| Conversion tracking | None visible in the export. `Facebook Leads: Total = N/A`. GA4 read via `pageTitle contains "West Plano"` heuristic on the corporate property. | GA4 `purchase` event primary, $119 value; phone-call actions consolidated; gift-card gap explicitly managed via QBO. |
| Keyword model | ~700 terms in a static blueprint; same ~200 negatives across campaigns; no ad-group granularity. | Tight ad-group-to-keyword alignment; Shared Library negatives (Master + Gift Card Filter); weekly search-terms review. |
| Landing pages | One `Default Landing Page` per campaign (FTVO page or gift-cards page). | Service-specific URLs per ad group chosen to improve LP QS within the franchise CMS. |
| Seasonal | Annual replacement of Winter Holiday, Valentine's, Mother's Day, Father's Day gift-card campaigns. | Calendar-driven builds with explicit ramp/peak/pause budget tables and UTM-tagged URLs. |
| Geo | 15 ZIPs + 5mi radius (7mi on legacy). | 10mi presence radius for services, 20mi for gift cards. Simpler, intentional. |
| Audience layer | Pre-wired In-Market (Gifts & Occasions, Beauty & Personal Care, etc.) and Affinity (Yoga Lovers, Beauty Mavens, etc.) segments. | Shared Library negatives + observation-audience work pending; customer-match audience (MindBody guests) planned. |
| Call tracking | Vendor-provisioned proxy number per campaign; call volume not exported. | Native Google Ads call-reporting + real published number; calls tracked as conversion actions. |
| GBP | **Not Connected** in the export for any campaign. | GBP is live and tied to Brand + Day Spa ad groups via location extension. |
| Reporting cadence | Monthly dashboard view; on-demand CSV export with gaps noted in §3.7. | Dated Editor snapshots every 1–3 days; per-export evaluation markdown docs; decisions log appended. |
| Budget control | Per Eulerity campaign (no per-channel or per-ad-group lever exposed). | Per Google Ads campaign; reallocations driven by impression-share-lost-to-rank vs budget diagnostics. |
| Quality-Score feedback | Not exposed. | First-class: QS-by-ad-group tables produced from every Editor export; ad-strength tracked. |
| Ad-strength tracking | Not exposed. | Tracked per RSA; "Poor" strength is an action item. |
| Change governance | Vendor makes changes; client sees the dashboard. | Every change is a git-tracked playbook/decisions-log entry + a dated Editor import file. |
| Fee model | Fixed monthly subscription (amount not in export; historically ~98% of total ad spend was Google-era vendor fee per the playbook). | Zero third-party fee. 100% of spend is media. |
| Franchisor-level portability | Blueprint travels across locations; consistent presentation. | Per-location customization; not a template. |

---

## 7. Is the Eulerity approach appropriate for adjusting to individual market conditions?

This is the most important section for a franchisor-facing brief. The honest answer is **mixed**: Eulerity is appropriate for some market-adjustment levers and structurally unable to do others. Below is a per-lever assessment.

### 7.1 Levers Eulerity can adjust well

| Lever | How well | Why |
|---|---|---|
| Seasonal offer rotation | **Strong** | Annual replacement of gift-card campaigns is a core competency; the vendor handles creative, copy, keyword lists, and landing pages without owner lift. |
| Geographic fencing (ZIP list, radius) | **Strong** | The 15-ZIP list + 5mi radius is easily altered per location through vendor onboarding. Per market, the ZIP set reflects actual population density. |
| Demographic/income targeting | **Moderate-Strong** | Dials (age, gender, parent, income) are exposed and can be tuned per location, though most locations appear to use the same default. |
| Audience overlay (In-Market, Affinity) | **Moderate-Strong** | Segments like Valentine's Day Items & Decor and Christmas Shopping are attached seasonally. Owner doesn't need to build them. |
| Omnichannel presence | **Strong** | For markets where brand awareness across Facebook/Instagram/Display matters (e.g., new location launch), the blueprint delivers without the owner having to learn five platforms. |
| Brand consistency across a franchise system | **Very strong** | This is Eulerity's best single argument. Every Spavia location looks and sounds the same; creative does not drift. |
| Negative-keyword hygiene (baseline) | **Moderate** | The blueprint ships with ~200 shared negatives. That's better than nothing for a non-technical owner, but it doesn't reflect per-market search terms (which aren't mined). |

### 7.2 Levers Eulerity cannot adjust well, structurally

| Lever | Why it's weak |
|---|---|
| **Campaign objective per market** | Maximize Traffic is the campaign type. If one location needs conversion optimization (bookings, gift-card revenue) and another needs brand awareness, the blueprint does not accommodate that split. |
| **Per-market conversion tracking** | GA4 is read off a **corporate** property with a `pageTitle contains "West Plano"` filter. This is not a per-location conversion signal; it's a page-title heuristic that breaks any time the franchisor changes page titles. It is almost certainly why `Facebook Leads: Total` is `N/A` in the export — the signal doesn't exist at the blueprint level. |
| **Per-market budget reallocation by intent** | The owner can't easily shift budget from "always-on FTVO Massage" to "seasonal gift cards" at a specific market-local inflection (e.g., "gift-card revenue is down 40% YoY at this location — double the gift-card budget and halve the FTVO spend"). The blueprint allocates by Eulerity campaign, not by strategic intent. |
| **Per-market ad-copy tuning to Quality Score** | QS is not exposed. The owner cannot see that `massage near me` has QS 2 with "below average" landing-page experience and respond by changing the ad-group URL. The blueprint uses one `Default Landing Page` per campaign, which forces LP Experience to be average-at-best across a non-trivial keyword portfolio. |
| **Per-market ad-group decomposition** | Eulerity campaigns do not expose an ad-group-level concept in the blueprint. All keywords in FTVO Massage point to one default URL. In a market where Couples Massage, Deep Tissue, and Prenatal Massage each deserve a distinct LP, you cannot get there without leaving the blueprint. |
| **Per-market negative keywords** | Negatives are blueprint-wide, not per-market. If the West Plano location is getting wasted clicks on "massage school Plano" because a local cosmetology school is nearby, the owner cannot add a site-specific phrase-match negative without the vendor doing it globally (affecting all Spavia locations that have the same blueprint). |
| **Per-market customer-match remarketing** | Eulerity does not appear to read the location's booking system (MindBody) as an audience seed. This is a significant missed lever — Spavia has a high-value past-guest list that could drive remarketing at CPCs far lower than cold prospecting. |
| **Per-market bid strategy experiments** | You cannot A/B test Maximize Clicks vs Target ROAS inside the blueprint; it's one setting. |
| **Per-market attribution to offline revenue** | No offline conversion import (e.g., from QBO, MindBody, Staylist). No GCLID capture on booking confirmations. The blueprint treats every market the same, which means it cannot discover that gift-card revenue at West Plano dropped $88k/yr after 2019 — nothing in the Eulerity feedback loop would surface that. |
| **Per-market franchisor-specific integrations** | The franchise CMS (LiveEdit Aurora) has quirks: thin pages, franchisor-controlled headers, brittle URL structure. A per-market optimizer would push for URL-swap strategies; Eulerity's blueprint cannot. |

### 7.3 Where the data says Eulerity *didn't* adjust for this market

Direct evidence from `EulerityData/`:

- **Identical targeting across campaigns.** All 5 campaigns use the same 15 ZIPs and (except the legacy gift card) 5mi radius, the same age/gender/parent/income dials. No market-specific differentiation between, say, a Sunday-brunch-oriented gift-card campaign and a weekday-local FTVO Massage campaign.
- **Identical ~200-keyword negative block** copied across FTVO Facial, FTVO Massage, both seasonal gift-card campaigns, and the legacy gift-card campaign. If the blueprint were per-market, we'd expect market-specific waste terms (e.g., local competitor names, local school names). We don't see them.
- **One `Default Landing Page` per campaign**, with zero per-ad-group URL variation. We know from the franchise CMS that `/massage`, `/skin-care`, `/beauty`, and `/spa-packages` exist; the blueprint uses `/first-visit-offer` or `/gift-cards` universally.
- **GBP Not Connected** — the single biggest local-search asset for a spa is not wired in.
- **Facebook lead form Not Connected** — a no-cost lead-capture mechanism on the blueprint's Social channel is not configured.
- **GA4 attribution via page-title heuristic**, not a dedicated property. A franchisor-level signal, not a market-level one.
- **Campaign type Maximize Traffic** — this is the definitive structural signal that the blueprint is optimizing for eyeballs, not bookings.

### 7.4 Where the data says Eulerity *did* adjust

- **Seasonal campaigns exist** (Winter Holiday, Valentine's), with their own keyword blueprints emphasizing gift-card terms and their own default landing page (`/gift-cards`). This is real market-adjustment work.
- **Audience segments are seasonal** — the In-Market segments visible in the UI (`Valentine's Day Items & Decor`, `Christmas Shopping`) are attached to the seasonal campaigns, which is a real adjustment.
- **The `DO NOT USE` legacy campaign was retired** — evidence that the vendor deprecates old configurations rather than letting them accumulate silently.
- **Activation dates differ** (Apr 2022 for FTVO Massage, Sep 2025 for FTVO Facial, Nov 2025 for Winter Holiday, Jan 2026 for Valentine's) — evidence that new campaigns are launched in response to franchisor/owner requests, not all at once.

### 7.5 Net assessment

Eulerity **is** a legitimate solution for a certain class of operator. It **is not** a legitimate solution for an operator whose strategic question is market-specific ROAS on a specific revenue line. The blueprint is a feature, not a bug — but only if the owner's question is one the blueprint is shaped to answer. At Spavia West Plano, the question (recover ~$88k/yr of gift-card revenue that disappeared) is explicitly a **conversion-objective, per-market, per-revenue-line** question, which is the quadrant where Eulerity is structurally weakest.

---

## 8. Where Eulerity fits and where DIY fits (franchisor-facing framing)

### 8.1 Locations where Eulerity is a good fit

1. **Brand-new locations during launch ramp-up.** Zero historical data, zero brand awareness, owner bandwidth 0. Eulerity's omnichannel blueprint delivers presence on day 1 without the owner having to learn a platform.
2. **Single-location owners without analytical capacity.** The dashboard view and monthly digest is about as much reporting as most owners will consume.
3. **Multi-location owners who value system-wide consistency.** The blueprint means every location's Facebook post looks the same, every Mother's Day campaign uses the same creative rhythm. For a franchisor that wants to protect brand voice, this is valuable.
4. **Locations with modest ad spend (< $2k/mo).** Below that threshold, the marginal gain from per-market optimization is smaller than the overhead of running the account, and Eulerity's fee is easier to justify.
5. **Locations where the primary KPI is call volume.** Eulerity's vendor-provisioned call tracking + omnichannel reach is well-suited to businesses where the phone ringing is enough.
6. **Locations where the owner is transient or the franchisee has high turnover.** A vendor-managed blueprint outlives any specific employee; a DIY approach requires continuity of expertise.

### 8.2 Locations where DIY (or an a-la-carte specialist) is a better fit

1. **Locations with a specific revenue decline to reverse** (e.g., Spavia West Plano's gift-card shrinkage). Recovering a specific revenue line requires campaign-level attribution that the blueprint does not provide.
2. **Locations with strong existing CRM/booking integration** (GA4, MindBody, QBO). The DIY approach can light up offline conversion imports, customer-match remarketing, and per-revenue-line attribution. The blueprint can't.
3. **Locations with internal or contracted ad ops capacity.** Once someone on the team can work a Google Ads Editor export, the fee savings and optimization gains start to compound.
4. **Locations with non-standard competitive dynamics** (a nearby cosmetology school eating the spa's "massage" queries; a competitor doing aggressive paid-search on the brand name; a local Groupon vendor cannibalizing gift-card searches). The blueprint cannot respond; a per-market optimizer can.
5. **Locations where gift cards, packages, or memberships are a disproportionate share of revenue.** These lines typically don't fire a clean GA4 `purchase` event and require offline attribution work — out of scope for the blueprint.
6. **Locations where the franchisor specifically wants ROI evidence per location.** DIY produces a per-location audit trail (exports, playbooks, decisions logs) that a franchisor can review; the blueprint produces a vendor dashboard.

### 8.3 A hybrid model worth considering

Nothing forces a franchisee to choose one path exclusively. A defensible hybrid:

- **Vendor (Eulerity or equivalent) for Meta/Display/awareness work** where their creative pipeline and audience segments add real value. Pay for the pieces where they're strong.
- **In-house (or contracted specialist) for Google Search and seasonal gift-card revenue recovery** where conversion optimization, Quality Score, and offline attribution matter. Own the pieces where the vendor is structurally weak.
- **Shared negatives / shared audience segments** — no reason not to let vendor-mined negatives feed into our Master Negatives list (§4.4), and vice versa.

This split converts the vendor relationship from "do everything" to "do the part you're good at" and reduces the switching cost if/when the relationship changes again.

### 8.4 What the franchisor should ask of any future vendor

Based on the gaps documented here, a short contractual checklist that any vendor — Eulerity or otherwise — should satisfy:

1. **Campaign ownership:** campaigns run in a Google Ads account owned by the franchisee's MCC, not the vendor's. At minimum, the franchisee has view access and can export.
2. **Conversion signal per campaign:** at least one primary conversion action fires per campaign with an attached value (service booking value, gift-card purchase value, lead value). `N/A` across the board is not acceptable.
3. **Campaign objective visible in the contract:** "Maximize Conversions" vs "Maximize Traffic" vs "Maximize Conversion Value" is a one-line decision that should be spelled out, not hidden behind a product name.
4. **Data export parity:** any metric shown in the vendor dashboard is available in a daily-granularity CSV export on request (ideally an API). No more lifetime-only exports.
5. **Per-market configurability** with a written record: demographic dials, geo, keyword additions, negatives, landing-page URL changes. Changes are logged.
6. **Landing-page URL per ad group** (or per keyword), not per campaign. This is a Quality Score hygiene baseline.
7. **GBP integration** as a default, not an optional. Any local business vendor that doesn't wire GBP is leaving the highest-intent map-pack traffic on the table.
8. **Offline conversion upload support** so revenue from booking systems (MindBody, Staylist, Gift Up, etc.) can feed back into Google Ads for Smart Bidding.
9. **Clean disengagement:** what you get if the relationship ends — and by when. The current `EulerityData/` export is a configuration archive, which is better than nothing but far from a full account history.

---

## 9. Eulerity's specific shortfalls at Spavia West Plano (for a franchisor memo)

Ordered by impact, each traceable to evidence in the export or the screenshots.

1. **Campaign objective is Maximize Traffic & Drive Engagement, not Maximize Conversions.** The owner paid for clicks, not bookings. Over 1,463 days of FTVO Massage spend ($103k), no conversion-objective optimization was applied. This is the single most important finding.
2. **No conversion signal piped into the campaigns.** `Facebook Leads: Total = N/A` on every row. GA4 is read via a `pageTitle contains "West Plano"` heuristic against a shared corporate property, not a per-location property. Smart bidding had nothing to optimize against even if the campaign type had been changed.
3. **Google Business Profile was not connected on any campaign.** GBP is the highest-intent local channel for a day spa (directions, calls, map pack). Leaving it unconnected is hard to defend.
4. **Gift-card purchase tracking was absent.** The gift-card campaigns were activated and deactivated on schedule but produced no vendor-side revenue attribution. This is directly relevant to the $88k/yr gift-card revenue decline we are trying to reverse.
5. **Seasonal coverage was incomplete.** Of the four Spavia-relevant gift-card seasons (Mother's Day, Father's Day, Winter Holiday, Valentine's), only Winter Holiday 2025 and Valentine's 2026 ran during the most recent export window. Mother's Day and Father's Day appear to have been absent or not yet launched at the time of disengagement. Given Mother's Day is a top-2 gift-card revenue season (see the playbook), this is a material gap.
6. **Default landing page per campaign.** All FTVO Massage keywords pointed to `/first-visit-offer` regardless of ad-group intent. Our own QS audit after bringing the account in-house found LP Experience "below average" on all massage keywords precisely because of this mismatch.
7. **Negative keyword list is identical across campaigns.** The same ~200 generic negatives protect every campaign; no location-specific waste terms are in evidence.
8. **Ad-strength opacity.** We have no record of whether Eulerity's RSAs were rated Poor/Average/Good/Excellent. Our own post-handover audit found all 15 RSAs in the account rated "Poor" — suggesting ad-strength was not an operational priority.
9. **No customer-match remarketing.** Spavia has a MindBody guest database. Eulerity does not appear to have used it as a remarketing audience seed, leaving a very high-ROI lever untouched.
10. **Call-tracking data was not exported.** Vendor call volume, duration, and booking attribution are not in the CSV. The owner paid for call tracking and cannot audit it post-disengagement.
11. **Fee-vs-media split is not visible.** `Budgeted Spend: Total = $103,354.98` on FTVO Massage is a lump sum. The owner cannot see what share went to media vs. vendor fee without separate invoice records.
12. **Attribution of the 2019→2025 gift-card revenue decline.** The vendor's own data cannot confirm or refute whether the decline correlates with anything the vendor did or didn't do. That is the central strategic question and the export answers none of it.

None of these are sabotage. They are consequences of a **templated omnichannel managed-service model** meeting a **location with a specific conversion question**. It is reasonable for the franchisor to conclude that the vendor is a fit for some locations and not others, and to ask the vendor to evolve the product, or to permit per-location carve-outs to DIY operators.

---

## 10. The DIY tooling and workflow (how we're doing it)

This section is deliberately detailed because the value of the DIY approach is inseparable from the toolchain that makes it feasible.

### 10.1 The editor + model layer

- **Cursor IDE** as the primary editing environment. Treated like a combined text editor + agent host + terminal. PowerShell is the shell; UTF-8 (BOM for Markdown) is the encoding rule.
- **Claude (Opus)** via Cursor's agent runtime. Used for analysis, cross-file reasoning, and generating evaluation docs. Model choice is tracked; large analysis jobs use longer-context-capable variants.
- **Agent transcripts** stored as JSONL at `agent-transcripts/<uuid>/<uuid>.jsonl`. Recent evaluations are cite-able in future sessions (e.g., today's Eulerity evaluation is one transcript; the April 15–16 live-data review is another). The transcript history is the institutional memory of the project.
- **`.cursor/rules/`** files for project-scoped agent behavior. Example: `google-ads-generated-imports.mdc` embeds the import discipline so any future agent spinning up an import knows the rules without being told.
- **`AGENTS.md`** at each repo root as the master operating doc. Includes encoding rules, "do not modify raw exports," UTF-16 handling guidance, and pointers to the other decisions docs.

### 10.2 The repo structure (per-account)

One git repo per Google Ads account. Observable pattern:

- `AGENTS.md` — agent operating rules.
- `DECISIONS-ImportFile.md` (or `DECISIONS.md`) — durable decisions log, appended per session.
- `Import-Best-Practices.md` (in the Sugar Hill repo) — the Shape A/Shape B import reference, the 30-char / 90-char RSA limits, the `Row Type` enum, the `enums.json` pointer.
- `exports/` — immutable, dated, time-stamped Google Ads Editor TSV (or web-UI CSV) snapshots. Never edited in place. Example: `2026-04-17 2337 SearchTerms17th.csv`.
- `imports/` (Spavia) or `generated/` (Sugar Hill) — outbound TSV files produced by builders, ready to import via Editor → Account → Import → From file.
- `scripts/` — Python utilities: `build_mothersday_import.py`, `_compare_import_export.py`, `validate_import.py`, `synthesize_ads.py`, `generate_display_campaigns_import.py`, `merge_guests.py`.
- `GuestLists/` (Sugar Hill) — customer-match pipeline: reservations CSV → segmented outputs (`gads_all_guests.csv`, `gads_high_value.csv`, `gads_recent_90d.csv`, `gads_lapsed_6mo.csv`, `gads_repeat_guests.csv`, `gads_texas_guests.csv`) uploaded to Google Ads Audience Manager for Customer Match remarketing.
- `reference/` — snapshots of documentation like the Google Ads CSV column list, so future agents don't have to re-derive it.
- `temp/` — scratch evaluations that graduate into committed docs once finalized.

### 10.3 The CSV discipline layer (non-obvious, high-value)

Google Ads Editor imports are notoriously fragile. The tooling encodes the rules so agents don't repeat mistakes:

- **`scripts/enums.json`** (Sugar Hill) — source of truth for every valid enum value (`Campaign Type`, `Bid Strategy Type`, `Row Type`, `Criterion Type`, `Networks`, `Ad rotation`, etc.). Any import builder consults this file.
- **`scripts/validate_import.py`** — validator that loads `enums.json` and checks a generated file before it's presented to a human. Bad files fail fast.
- **Shape A vs Shape B** (documented in `Import-Best-Practices.md`): Shape A uses a `Row Type` column for mixed entities (campaigns + ad groups + ads + keywords in one file); Shape B mirrors the Editor export for single-entity files (shared negative keyword lists need this). The tooling enforces the distinction.
- **`generated/templates/`** — header-only templates for each shape (`template-shape-a-full-campaign.csv`, `template-shape-b-shared-list-keywords.csv`, `template-shape-b-shared-list-apply.csv`, `template-shape-b-negative-keywords.csv`). New import builders are expected to copy one of these, not invent a header.
- **Encoding discipline:** Google Ads web UI exports are **UTF-16 LE with BOM**; Editor exports are typically UTF-8 or UTF-16. Scripts that read UI exports open with `encoding='utf-16'`; scripts that write new imports use UTF-8 without BOM. Markdown and docs use UTF-8 with BOM.
- **EU political ads** discipline: every campaign row must have `Doesn't have EU political ads`. A forgotten column here silently breaks imports.
- **Character-limit discipline:** headline ≤ 30 chars, description ≤ 90 chars, path ≤ 15 chars. Validators catch borderline cases before they fail in Editor.
- **`#Original` column pattern** for modifying existing entities without creating duplicates (e.g., `Keyword#Original` = old text, `Keyword` = same text, `Final URL` = new URL).
- **Import-order rules** for multi-file batches (campaigns before apply-files; keyword-list before apply-file).

This discipline means an agent can say "generate a Mother's Day import" and the output is a valid Editor TSV on the first try — not after 5 rounds of "Ambiguous row type" errors.

### 10.4 The analytical workflow

A typical week looks like:

1. **Export in the morning** — run a Google Ads Editor export (TSV) and a web-UI search-terms export (UTF-16 CSV). Save both under `exports/` with an ISO-style timestamped filename.
2. **Open a Cursor session, point the agent at the new export and the playbook.** Agent reads the playbook (`2026-spavia-google-ads-playbook.md`), the last decisions log, and the new export. Produces a summary keyed to the playbook's metrics (impressions, CTR, CPC, impression share, QS, ad strength, conversions).
3. **Agent produces per-area evaluation docs** in `exports/<date>/EVALUATION-*.md`: strategy & structure, landing pages & QS, negatives, ad copy & sitelinks, and a cross-check against the prior decisions log. Each eval doc is versioned in git.
4. **Human reviews and merges decisions** into the master decisions doc (`spavia-google-ads-decisions-<date>.md`). New TODOs are appended, completed ones are checked off.
5. **Agent generates the next import file** (e.g., new negatives, URL swaps, ad-copy updates) using the builder scripts. Validator runs. Human imports via Editor.
6. **Next export captures the result.** Loop.

The meta-pattern is: **exports are the memory, evaluations are the thinking, imports are the action, and the decisions log is the audit trail.** Everything is git-tracked.

### 10.5 Mass-update capability

A specific DIY advantage that the vendor blueprint cannot match:

- **Keyword migrations at scale.** The outgoing Eulerity ~1,003-term negative list was migrated into a Shared Library list via a single shape-B CSV built from the export. One import, done in minutes.
- **RSA rewrites across all ad groups.** When the April 12 audit found all 15 RSAs rated Poor, a single builder script produced replacement RSAs for the four worst ad groups (Anna, Allen, Celina, Monthly in the Sugar Hill analogue; similar pattern applied for Spavia). Pause-old-RSA / import-new-RSA as one batch.
- **Landing-page URL swaps by ad group.** Changing Massage Near Me's Final URL from `/first-visit-offer` to `/massage` is a one-line edit in a Shape A file with the `#Original` column. Applied once, validated, imported.
- **Seasonal campaign builds.** `build_mothersday_import.py` generates the full-account Editor CSV for a seasonal campaign by taking a reference export and applying intentional edits (new ad group, new keywords, new sitelinks, new budgets). The alternative — hand-editing a 200-column wide TSV — is error-prone enough that we wrote a playbook (`DECISIONS-ImportFile.md`) specifically to stop agents from trying it.
- **Customer-match audience rebuilds.** Sugar Hill has `GuestLists/sugar-hill-guest-merge/` producing segmented customer-match CSVs from the Staylist reservation export. The same pattern will apply to Spavia's MindBody export when we are ready to build a Customer Match list.

None of these are possible inside the Eulerity UI.

### 10.6 Reporting capability

- **Per-export evaluation docs** in markdown are the output format. They're readable, diffable, and pasteable into a franchisor email.
- **Per-decision logs** are cumulative. Any question of the form "when did we change X and why" is answerable by grep.
- **Per-session agent transcripts** provide a conversation-level audit trail. They can be cited from future sessions.
- **Side-by-side comparison of exports** is straightforward (csv diff, keyword inventory comparison, status diff). Example utility: `_compare_import_export.py`.
- **Dashboards** are deliberately not in scope yet — the incremental value of a live dashboard is low when the account is under weekly human review anyway. If needed, a Looker Studio dashboard on GA4 + Google Ads + QBO would be the natural next step.

### 10.7 Costs of this approach

To keep the report honest:

- **Setup cost.** The tooling took real effort to build (import discipline, enums, templates, validators, playbooks). A franchisee starting from zero can't replicate this in a weekend.
- **Operating cost.** ~2–4 hours/week of a human's attention during the first 60 days of a new account, tapering to ~1 hour/week once the negatives list and ad-copy work is stable.
- **Skill dependency.** If the person doing this leaves, the repo remains but interpretation is not fully automatic. Decisions logs and playbooks mitigate this but don't eliminate it.
- **Cursor/Claude dependency.** The tooling is much less pleasant without an agent-capable IDE. A franchisee who doesn't use Cursor or equivalent will lose the mass-update advantage.

These costs are real, and they explain why a vendor blueprint still makes sense for many operators.

---

## 11. Actionable takeaways

### 11.1 For the Spavia West Plano account (this repo)

1. **Harvest the ~700 negatives** from `keywords-by-keyword.csv` into `Master Negatives`. Dedupe, preserve match type, add to Shared Library. Estimated effort: 1 hour.
2. **Archive the `EulerityData/` folder as historical** and delete the three `(1)` duplicates to tidy the folder. Low priority.
3. **Recreate the Mother's Day 2026 seasonal campaign** we would have inherited. Already in flight per `mothersday/mothers-day-gift-card-playbook.md`; this report just confirms there's no vendor artifact to merge in.
4. **Ask Eulerity (in writing) for the time-series CSV** of Clicks, Ads Displayed, CTR, and Budget at daily granularity. Screenshots confirm the data exists in their UI. Use it to reconstruct a monthly spend-vs-revenue reconciliation against QBO P&L for 2022–2026. This is necessary to answer the gift-card decline question.
5. **Ask Eulerity for any call-tracking recordings/logs** tied to the West Plano proxy number `+1 469 960 4367`. Even a CSV of call volume by day by campaign would materially improve the post-mortem.
6. **Verify GBP, Facebook lead forms, and GA4 property** are correctly wired in our own account — do not assume Eulerity's configuration carried over.
7. **Close the gift-card conversion gap.** Either franchise-platform engineering adds a `purchase` event on `/gift-cards`, or we implement offline conversion upload from QBO.

### 11.2 For the franchisor conversation

1. Use the **12-item shortfall list in §9** as the spine of the memo. Each item is traceable to evidence.
2. Propose a **hybrid model** (§8.3) rather than a binary "fire Eulerity" — it leaves room for locations where the blueprint still fits.
3. Offer the **vendor-contractual checklist in §8.4** as a neutral framework for evaluating any future vendor (not just Eulerity).
4. Share **our own evaluation docs** (`exports/2026-04-12 EOD/EVALUATION-*.md`, `spavia-google-ads-decisions-2026-04-12.md`) as evidence of what per-market optimization looks like when it's running. These are the receipts.

### 11.3 For other franchisees (self-serve evaluation)

1. Run Eulerity's CSV export against the **§3.7 absence checklist**. If your export also lacks conversions, per-keyword performance, time series, and search terms, you are in the same boat.
2. Check the **campaign type** in your own Eulerity UI. If it reads `Maximize Traffic & Drive Engagement`, your campaigns are not conversion-optimized regardless of what the dashboard headline numbers look like.
3. Compare your **`Default Landing Page` per campaign** to the actual franchise site URL tree. If you see one URL per campaign but your site has service-specific pages, Quality Score is probably leaving money on the table.
4. Check **GBP connection status**. If `Not Connected`, the single highest-intent local channel is off.
5. Compare **vendor fee ÷ total ad spend** over the last 12 months. If the fee is a large share, the hybrid model in §8.3 is especially attractive.

---

## 12. Appendices

### 12.1 File hash reference

Duplicate-file pairs verified via SHA-256 (full hashes truncated for readability):

- `Connections.csv` / `Connections (1).csv` — 2,930 bytes, `CD727BF9B0EA1CA59055BDD01163DA2D5D9B250AE66E671A0860187C568A3D94`
- `Distribution.csv` / `Distribution (1).csv` — 1,368 bytes, `F742B2C44E785F174383488DF93CBCB34118BA39E45CCCC221DF96A20803A372`
- `Performance.csv` / `Performance (1).csv` — 1,605 bytes, `3A5967875974B91F80139D472D695226BD286C42953EE2A9D99B1A5D6D5D0A3D`

### 12.2 Eulerity UI metrics inventory (from screenshots)

Time-series views that exist in the Eulerity dashboard but were **not** in the CSV export:

| Metric | Date window shown | Value | Lifetime | Last 30 days | Yesterday |
|---|---|---:|---:|---:|---:|
| Ads Displayed | 11/4/2025 – 4/17/2026 | 420,140 | 6,933,595 | 44,968 | 0 |
| Clicks | 11/4/2025 – 4/1/2026 | 9,582 | 134,919 | 1,443 | 0 |
| CTR | 11/4/2025 – 4/1/2026 | 2.361% | 1.946% | 3.209% | 0% |
| Advertising Budget | 4/11/2026 – 4/17/2026 | $0.00 | $103,354.98 | $1,656.74 | $0.00 |

(Each metric has a `Download CSV` button in the UI. These are the datasets to request from Eulerity in writing per §11.1.)

### 12.3 Eulerity audience segment inventory (from screenshots)

Attached to Spavia – West Plano campaigns:

- **In-Market (11 segments observed):** Gifts & Occasions, Personalized Gifts, Gift Baskets, Valentine's Day Items & Decor, Beauty & Personal Care, Skin Care Products, Spas & Beauty Services, Anti-Aging Skin Care Products, Christmas Shopping, Online Christmas Shopping.
- **Affinity (4 segments observed):** Health & Fitness Buffs, Beauty Mavens, Yoga Lovers, Beauty & Wellness.
- **Scope:** each segment is labeled "For Google Display & Google Search Campaigns", "Only Google Display", or "Only Google Search Campaigns".

### 12.4 Eulerity creative inventory (from screenshots)

- **6 Omni Ads** (static image posts) deployed, all created Sep 11, 2025.
- **Example ad (Facebook preview):**
  - Social Text: *"New to Spavia? Enjoy a personalized massage and receive a special welcome offer designed just for first-time guests. Offer available Mon–Thurs, expires 4.30.2026"*
  - Category: Brand Awareness.
  - CTA: Book Now.
  - Landing Page: `https://planotx.spaviadayspa.com/first-visit-offer?esc=6c2cd6d8-7dc4-4949-9f76-ce5038c265ee`
  - Status: No Subscription (post-disengagement).
  - Ad-level metrics (from Dynamic Ad Preview modal): 7-day 0 ads / 0 clicks / 0% CTR; 30-day 2,414 / 126 / 5.22%; 90-day 11,247 / 558 / 4.96%.
- **Example Responsive Search Ad (same asset):**
  - Headlines: "Limited-Time Spa Offer Today", "Exclusive Offer for New Guests", "Special Spa Offer", "Relaxation Starts at Spavia", "First Time Massage".
  - Descriptions: "New to Spavia? Book a massage and receive a limited-time first visit offer.", "Enjoy your first massage at Spavia with a special offer for new guests.", "Your first massage comes with an exclusive offer. Book your treatment today.", "Book your massage today and receive an exclusive offer for first-time guests."

### 12.5 Related documents in this repo

- `imports/2026-04-09 FirstTake/2026-spavia-google-ads-playbook.md`
- `spavia-google-ads-decisions-2026-04-12.md`
- `exports/2026-04-12 EOD/EVALUATION-strategy-and-structure.md`
- `exports/2026-04-12 EOD/EVALUATION-negative-keywords.md`
- `exports/2026-04-12 EOD/EVALUATION-landing-pages-and-quality-score.md`
- `exports/2026-04-12 EOD/EVALUATION-ad-copy-and-sitelinks.md`
- `exports/2026-04-12 EOD/EVALUATION-crosscheck-decisions-2026-04-12.md`
- `temp/KEYWORDS-evaluation.md`
- `mothersday/mothers-day-gift-card-playbook.md`
- `AGENTS.md`, `DECISIONS-ImportFile.md`

### 12.6 Related documents in the sibling account (`sugarhill-googleads-localdata/`)

Referenced for tooling context only:

- `AGENTS.md`, `DECISIONS.md`, `Import-Best-Practices.md`
- `scripts/enums.json`, `scripts/validate_import.py`, `scripts/generate_display_campaigns_import.py`, `scripts/synthesize_ads*.py`
- `generated/templates/` — shape-A and shape-B import templates
- `GuestLists/sugar-hill-guest-merge/` — customer-match pipeline pattern
- `generated/2026-04-15 DisplayAds/2026-04-15 sugar-hill-display-campaigns.md` — display-campaign playbook pattern

### 12.7 Change log for this document

| Date | Note |
|---|---|
| 2026-04-18 | Initial "everything" report. Inputs: Eulerity CSV export; 8 UI screenshots; in-repo playbooks, decisions logs, and evaluation docs; sibling account tooling scan. |
