# Price Adjustment Verification — Full Audit Methodology

## Context

This document records the round-by-round debugging process for building
correctly adjusted prices from TSETMC APIs, conducted during a
research project (July 2026).

## Round 1: Share-Change-Only Adjustment

**Method:** Used `GetInstrumentShareChange` to compute `adj_factor(date) = product(old/new for all changes after date)`, then `adjusted_price = raw_price × adj_factor`.

**Result:** 365/392 stocks adjusted. Fixed the immediate split problem but:
- Missing dividend adjustments (~0.2%/month)
- API returns duplicate entries — must deduplicate by `(dEven, numberOfShareOld, numberOfShareNew)`
- Pre-IPO placeholder shares (old=1) create false market caps for provincial water companies

## Round 2: TSETMC Official Adjusted Prices

**Discovery:** Found `GetPriceAdjustList` API by inspecting the JavaScript bundle loaded by the TSETMC frontend (`main.*.js`).

**API endpoint:** `http://cdn.tsetmc.com/api/ClosingPrice/GetPriceAdjustList/{inscode}`

**Response:** `{"priceAdjust": [{dEven, pClosing, pClosingNotAdjusted, ...}]}`

**Cross-validation:** Verified every adjustment ratio against R365 DPS data for فرآور:
- TSETMC ratio = `pClosing / pClosingNotAdjusted`
- Expected ratio = `(price_before_meeting - DPS) / price_before_meeting`
- **All 16/16 events matched exactly** — confirming TSETMC adjustments are total-return (split + dividend)

**Difference vs share-change-only:** 7.4% of monthly returns differed by >0.1%. The -0.20%/month average difference = monthly dividend yield captured by TSETMC but not by share changes alone.

## Round 3: CRITICAL — TSETMC PriceAdjustList Missing 45% of Events

**Trigger:** قصفها showed -99.4% return in October 2024 — clearly a data error.

**Investigation:**
- قصفها had a 155× capital increase on 2024-09-30: 195M → 30.19B shares
- `GetInstrumentShareChange` caught this event ✅
- `GetPriceAdjustList` did NOT have any event on 2024-09-30 ❌
- The price dropped from 152,800 → 1,047 (exactly 152,800/155 ≈ 986, matching the split ratio)

**Full audit across 392 stocks:**
- Total share changes from `GetInstrumentShareChange`: 2,147 events
- Events NOT covered by `GetPriceAdjustList` (within 7-day window): 1,122 (52.3%)
- Coverage rate: 47.7%
- Conclusion: `GetPriceAdjustList` is NOT complete and cannot be used alone

**Examples of uncovered events:**
- آباد 20240312: 240M → 10.68B shares (44.5×)
- آسیا 20201221: 2.3B → 24.1B shares (10.5×)
- آپ 20210801: 2.65B → 5.55B shares (2.1×)

## Round 4: Combined Adjustment (Final Solution)

**Method:** Merge both event streams, deduplicating by 7-day proximity window.

**Deduplication logic:**
- For each share change event from `GetInstrumentShareChange`:
  - If a `GetPriceAdjustList` event exists within ±7 days → skip (already covered)
  - Otherwise → include the share change ratio (old/new)
- Merge with all `GetPriceAdjustList` ratios
- For each price date: cumulative_factor = product of all future merged ratios

**Overlap analysis (7-day window):**
- Share changes WITH TSETMC adjustment nearby: 1,173 (54.9%)
- Share changes WITHOUT (unique to InstrumentShareChange): 964 (45.1%)

**Verification:**
- قصفها Oct 2024: -99.4% → -6.58% ✅
- غسالم Aug 2013: 296% (same as TSETMC-only, no double-counting) ✅
- 194 extreme returns >100% remain (genuine trading halt → resume price gaps)
- Mean monthly return: 3.46%, Stdev: 19.68%

## Round 5: Deep Quality Audit

### Issues checked:
1. **Zero returns with >5 trading days** (506 cases): NOT A BUG — stock closed at same adjusted price on consecutive month-ends. The `first_close` field in monthly CSV is informational (first day of month), NOT used in the return formula (`last_close_this / last_close_prev - 1`).
2. **Non-monotonic adjustment factors** (359 stocks): EXPECTED — factor increases at each dividend event then resets.
3. **Factors >1.0** (10 stocks): From pClosing=1 halt days → TSETMC applies reverse adjustment. Correctly handled by vol=0 filter.
4. **Pre-IPO placeholder shares (=1)** (12 rows, 10 provincial water companies): Must exclude market cap where shares <1000.
5. **Negative book equity** (157 cases): Genuine distressed firms (اروند, اسیاتک). Fama-French model handles naturally.
6. **Accounting identity violations** (TA≠TL+TE): 3/9,888 = 0.03%, all from 1993.

### TSETMC Chart API date encoding
The `GetChartData` endpoint returns dates as negative 64-bit integers. Decoding:
- `dEven / 86400` = days from Unix epoch (1970-01-01)
- Negative values are pre-1970 dates
- These map to Gregorian years ~1381-1406, which in Shamsi = 2002-2026

### Recommended filters for factor construction:
1. Min 3 trading days per month (removes 3,052 thin obs, 3.9%)
2. Winsorize at 1st/99th percentile
3. Exclude market cap with shares <1000 (pre-IPO placeholders)
4. Start sample from 2003 (risk-free rate coverage)
5. Exclude negative book equity for BE/ME sorting (157 obs)

## API Discovery Technique

To find undocumented TSETMC API endpoints, inspect the JavaScript bundle loaded by the TSETMC frontend (the `main.*.js` file). Extract API paths with a regex like `api/[A-Za-z/]+`.

This reveals all API paths the frontend uses, including:
- `api/ClosingPrice/GetPriceAdjustList/` — adjustment events
- `api/ClosingPrice/GetPriceAdjustByFlow/` — adjustments by flow
- `api/ClosingPrice/GetChartData/` — chart data
- `api/ClosingPrice/GetMarketCap/` — market cap data
- And 30+ more endpoints

The JS hash can be found in the HTML source of any TSETMC page.
