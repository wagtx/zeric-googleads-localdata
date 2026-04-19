# Spavia West Plano — Google Ads Audit & Decisions Log

**Date:** 2026-04-12
**Context:** First ~12 hours of live data from newly restructured campaigns (launched 2026-04-11). Analysis of Google Ads Editor export + performance stats export from the Google Ads web UI.

---

## Account Structure (as launched)

| Campaign | Type | Budget | Bid Strategy | Networks |
|---|---|---|---|---|
| 2026-Search - Massage & Spa | Search | $30/day | Maximize Conversions | Search only |
| 2026-Search - Facials & Skincare | Search | $12/day | Maximize Conversions | Search only |
| 2026-Search - Waxing | Search | $5/day | Maximize Clicks (cap $3) | Search only |
| 2026-Search - Gift Cards (Mother's Day) | Search | $5/day | Manual CPC | Search only |
| 2026-PMAX - First Visit Offer | PMAX | $10/day | Maximize Conversions | All |

All Search campaigns targeting 10mi radius from spa. Gift Cards at 20mi (intentional — gift buyers don't need to be local).

---

## Quality Score Analysis

**Average QS across scored keywords: 3.9/10.** Only 20 of 121 keywords have enough data for a QS. Brand terms at QS 10, everything else dragging.

### QS by ad group (worst to best)

- **Massage Near Me:** QS 1-2. All three components failing. Biggest spend ad group.
- **Couple's Massage:** QS 1-3. LP "below average" on all scored keywords.
- **Facials:** QS 3-5. LP is "above average" on `/skin-care` — best non-brand LP score.
- **Day Spa:** QS 3-8. "day spa plano" at QS 8 is the non-brand star.
- **Deep Tissue / Hot Stone:** QS 4-5. LP "average", Ad Relevance "average".
- **Mother's Day Gift:** QS 3-5. LP "below average" on `/gift-cards` (thin content page).
- **Brand:** QS 10. Perfect across the board.

### QS component patterns

- **Expected CTR:** "Below average" on 17 of 20 scored keywords. Universal problem. Driven by ad copy not matching search intent tightly enough + "Poor" ad strength on all 15 RSAs.
- **Landing Page Experience:** "Below average" on 10 of 20. Worst on massage keywords pointing to `/first-visit-offer` instead of `/massage`. Franchisor controls the CMS so page content can't be edited — only the URL we point to.
- **Ad Relevance:** "Below average" on 10 of 20. Headlines lean toward generic spa language ("Relax And Unwind") rather than mirroring the search query directly.

---

## 12-Hour Performance Data

### Campaign performance

| Campaign | Impr | Clicks | Cost | CTR | Avg CPC | Search IS | Lost to Rank | Lost to Budget |
|---|---|---|---|---|---|---|---|---|
| Massage & Spa | 367 | 28 | $51.09 | 7.6% | $1.82 | 10.5% | 75.9% | 13.7% |
| Gift Cards | 32 | 4 | $6.00 | 12.5% | $1.50 | 10.0% | 16.3% | 78.9% |
| Facials & Skincare | 16 | 3 | $3.55 | 18.8% | $1.18 | 10.3% | 81.3% | 8.4% |
| PMAX - First Visit | 12 | 3 | $2.80 | 25.0% | $0.93 | 12.4% | 61.8% | 25.8% |
| Waxing | 0 | 0 | $0.00 | — | — | 10.0% | 90.0% | 0% |

### Key findings

- **~10% impression share across all non-brand ad groups.** Losing ~75-80% to rank (QS drag), not budget.
- **Massage Near Me + Couple's Massage consumed 81% of the Massage & Spa budget** ($41.44 of $51.09) despite being the lowest QS ad groups.
- **Couple's Massage is the most expensive click at $2.52 avg CPC** — QS tax in action.
- **Gift Cards is budget-starved, not rank-starved.** 79% lost to budget vs 16% to rank. The $5/day budget is the bottleneck with Mother's Day approaching.
- **Waxing got zero impressions.** 90% lost to rank. Needs monitoring — may be volume or cap issue.
- **Zero conversions across the board** — but conversion tracking wasn't properly configured until this session (see below).
- **Maximize Conversions was running blind** with no conversion signal. Effectively spending like uncapped Maximize Clicks.

### Bright spots

- Deep Tissue: 23% CTR, $1.69 CPC
- Facials: 27% CTR, $1.18 CPC
- "therapeutic massage near me": 3/3 clicks (100% CTR)
- "hydrafacial near me": 2/3 clicks (67% CTR)
- Brand: 72.5% IS, $0.38 CPC, 0% lost to rank

---

## Decisions Made

### 1. Conversion Tracking — Fixed

**Problem:** Two GA4 conversion actions were imported into Google Ads ("Booking_Complete" and "Conversion") but showed "No recent conversions" — name mismatch with actual GA4 events. The old Healcode UA import was still set as Primary. Multiple overlapping phone call actions all set as Primary, which would cause double-counting.

**Actions taken:**
- Imported the GA4 `purchase` event as a new conversion action: "Spavia Day Spa - West Plano - GA4 (web) purchase"
- Set as Primary action under the Purchases goal
- Demoted old Healcode UA action to Secondary (observe only)
- Set conversion value to **"Use the same value for each conversion" = $119** (weighted avg of top-booked services; GA4 passes `value: 0` explicitly so the "default" fallback wouldn't apply)
- Old "Booking_Complete" and "Conversion" GA4 imports should be cleaned up/removed

**Still needed:**
- Audit the Contacts goal — multiple phone call actions (Calls from ads, Clicks to call, Trackable Phone Calls, Leads) all set as Primary. Should keep only one clean phone call action as Primary, demote rest to Secondary.
- Gift card purchases have ZERO tracking. Need to determine where the transaction completes (on-domain vs third-party) and instrument accordingly.

### 2. Landing Page URL Change — Decided, Not Yet Implemented

**Decision:** Change Massage Near Me ad group Final URL from `/first-visit-offer` to `/massage`.

**Rationale:** LP experience is "below average" on all massage keywords. The `/first-visit-offer` page is a promotional page, not service content. Google wants the LP to match the search intent. The $30-off hook moves to a sitelink instead. Day Spa ad group pointing to homepage gets QS 6-8 with LP "average" — confirms the franchise CMS can deliver decent scores when the page matches.

### 3. Ad Copy — Improvements Needed, Not Yet Implemented

**Problems identified:**
- All 15 RSAs rated "Poor" ad strength
- Most ads have only 8 headlines and 2 descriptions (Google recommends 15 and 4)
- Headlines are too generic — "Relax And Unwind", "Your Relaxation Awaits" don't mirror search queries
- No pin strategy visible — Google may be showing irrelevant headlines in position 1

**Recommendations:**
- Bulk up all RSAs toward 12-15 headlines and 4 descriptions
- Mirror search query language in H1 (e.g., "Massage In West Plano — $30 Off" for Massage Near Me)
- Consider pinning the most keyword-relevant headline to position 1
- Keep positions 2-3 unpinned for variety/testing

### 4. Sitelinks — Structure is Clean

**Finding:** Initial analysis of the Editor export incorrectly flagged ~98 "account-level" sitelinks. Eric confirmed via the Google Ads UI that there are 68 total sitelinks: 4 on PMAX, 64 on ad groups, zero at account level. The export includes historical/removed items without clear level designation.

**Status:** Ad group sitelinks are well-curated — 4 per ad group, contextually relevant, correct `planotx.` URLs, proper descriptions. No action needed.

**Gap:** Waxing ad groups (Brazilian, Waxing, Bikini Wax) are missing a First Visit - $30 Off sitelink. Add to all three. Do NOT add to Gift Cards campaign (off-intent for gift buyers).

### 5. Negative Keywords — Needed Immediately

**Status:** Zero negative keywords in the account. Need to start reviewing search terms report and build a shared negative list before irrelevant clicks waste budget. Priority negatives for massage queries: massage gun, massage chair, massage school, massage therapy school, massage license, asian massage, happy ending, etc.

### 6. Gift Cards Campaign — Budget + Bids

**Decision:** Increase Gift Cards budget (from $5/day) — it's the only campaign where more budget directly translates to more impressions (79% lost to budget, only 16% to rank). Mother's Day is ~3 weeks out.

**Decision:** Set actual Max CPC bids on Gift Cards keywords. Currently all blank on Manual CPC. First page bid estimates range from $0.72 (spa gift for mom) to $7.59 (spa gift certificate). Set bids in the $2-3 range for gift card terms, $1-2 for Mother's Day terms.

### 7. Bid Strategy — Watch and Evaluate

**Current state:** Maximize Conversions now has a valid conversion signal (GA4 purchase). Give it 2-3 weeks to collect data. The account gets ~6 purchases/day across all traffic sources; Google Ads-attributed conversions will be a subset of that.

**Watch for:** If still at zero Google Ads conversions after 7 days, there may be a GCLID passthrough issue on the franchise CMS (click ID needs to survive through to booking confirmation). If so, consider stepping back to Maximize Clicks temporarily to accumulate data.

**Waxing:** Leave Maximize Clicks with $3 cap for now. Monitor whether it picks up impressions.

**Gift Cards:** Manual CPC is correct since gift card purchases aren't tracked.

---

## Outstanding Items / Next Steps

1. **Implement Massage Near Me LP change** (`/first-visit-offer` → `/massage`)
2. **Add First Visit sitelink** to all three Waxing ad groups
3. **Set Gift Cards keyword bids** and increase daily budget
4. **Audit Contacts conversion goal** — demote duplicate phone call actions to Secondary
5. **Build negative keyword list** from search terms report
6. **Bulk up RSA headlines/descriptions** across all ad groups
7. **Investigate gift card purchase tracking** — where does the transaction complete?
8. **Monitor for GCLID passthrough** — verify Google Ads is attributing conversions after 7 days
9. **Remove or clean up** old "Booking_Complete" and "Conversion" GA4 imports that show "No recent conversions"
10. **Re-evaluate bid strategy** at 2-3 week mark based on conversion volume
