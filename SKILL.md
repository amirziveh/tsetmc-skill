---
name: tsetmc
description: "Reverse-engineer and use the TSETMC (Tehran Stock Exchange) API ecosystem — three API surfaces (CDN REST JSON, old tsev2 CSV, and ParTree HTML), 50+ endpoints for instrument data, price history, indices, client types, order books, shareholders, and messages."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [iran, tsetmc, tse, stock-exchange, iranian-stock, financial-data, reverse-engineering, securities, stock-market, bourse]
---

# TSETMC (Tehran Stock Exchange) Data API

Use this skill when you need to fetch data from TSETMC (https://www.tsetmc.com / https://old.tsetmc.com) — the Tehran Securities Exchange Technology Management Co. This covers stocks (بورس), OTC (فرابورس), futures, ETFs, indices, and all Iranian securities data.

## When to use

- User needs stock prices, indices, or trading data from the Tehran Stock Exchange
- Need to search for Iranian symbols (نمادها) by Persian name
- Need historical price data, client type (حقیقی-حقوقی), order book, shareholder info
- Need to understand the TSETMC API ecosystem (which endpoints work, which are deprecated)
- Building an Iranian market data pipeline or monitoring tool

## Three API Surfaces

TSETMC has **three** distinct API backends, each with different characteristics:

### 1. 🆕 CDN REST API (`https://cdn.tsetmc.com/api/`) — JSON
- Modern JSON REST API. ~30 endpoints.
- **Base**: `https://cdn.tsetmc.com/api/`
- **Response pattern**: every endpoint wraps data in a single-key object like `{"instrumentSearch": [...]}` or `{"instrumentInfo": {...}}`
- **Requires `insCode`** — a 15-20 digit numeric instrument code (not the Persian symbol name)
- **Headers**: **`User-Agent` header is REQUIRED** — without it, endpoints return empty arrays `{"closingPriceDaily":[]}` even when data exists. Use `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36`.
- **Status**: Mostly active. **⚠️ GEO-BLOCKED as of July 2026** — CDN returns HTTP 303→403 redirect from outside Iran. All TSETMC API surfaces now require an Iran-based proxy server. Previously worked globally; geo-block appears to have been added in 2026. `ClosingPriceDailyList` returns ALL daily prices in one call (verified: 4,602 records for فولاد from 2007-03-11 to 2026-07-20). Endpoints known empty/deprecated: `MarketOverview`, `IndexB1LastAll`, `ClosingPriceGetMarketMap`, `SectorsSummary`, `GetInstrumentHistory/{insCode}/{date}` (shares endpoint — use `GetInstrument` or `GetClosingPriceDailyList` instead).

### 2. 🏚 Old TSEv2 CSV API (`http://old.tsetmc.com/tsev2/data/`) — Delimited text
- ASP.NET-style HTTP handlers returning CSV/semicolon-delimited text.
- ~15 endpoints. More reliable for historical data.
- **Base**: `http://old.tsetmc.com/tsev2/data/`
- **Response pattern**: semicolon (`;`) row separator, comma (`,`) field separator. First field is often an instrument code.
- These are older but often more complete (MarketWatchInit gives all live prices, ClientTypeAll gives all client types).
- **Note:** uses plain HTTP, not HTTPS.

### 3. 📄 ParTree HTML (`http://old.tsetmc.com/Loader.aspx?ParTree=...`) — HTML + embedded JS
- ASP.NET WebForms pages with data embedded in JavaScript variables.
- ~15 ParTree codes. Best for raw instrument info (all fields parsed from JS variables).
- The `ParTree=151311&i={insCode}` page has complete instrument data embedded in JS variables like `InsCode`, `LVal18AFC`, `DEven`, `BaseVol`, `ZTitad`, `CIsin`, etc.
- Also used for members-only reference data (industry codes, board codes).

### 4. 📈 Members Chart API (`https://members.tsetmc.com/tsev2/chart/data/`) — CSV
- `Financial.aspx?i={insCode}&t=ph&a=0|1` — Price history (adjusted or unadjusted)
- `IndexFinancial.aspx?i={idxCode}&t=ph` — Index financial data

## Key Concepts

### Instrument Codes (insCode)
Every traded instrument has a 15-20 digit numeric code. This is the primary identifier for all API calls. Examples:
- **فولاد (Mobarakeh Steel)**: `46348559193224090`
- **شپنا (Esfahan Oil Refinery)**: `7745894403636165`

To find an `insCode` by Persian symbol name, use the search endpoint.

### Flow (بازار / تابلو)
A numeric code indicating which market the instrument trades on:

| Code | Persian | English |
|------|---------|---------|
| 0 | عمومی | General (includes both بورس and OTC) |
| 1 | بورس | TSE Main Board |
| 2 | فرابورس | OTC / Iran Fara Bourse |
| 3 | آتی / مشتقه | Futures / Derivatives |
| 4 | پایه | UTP / Unlisted (بازار پایه) |
| 6 | انرژی | Energy Exchange |
| 7 | کالا | Mercantile / Commodities |
| 18 | ETF صندوق‌ها | ETFs |
| 19 | حرفه‌ای | Professional |

### yVal (نوع دارایی / Asset Type)
`yVal` field in instrument info indicates the asset type. Common values:
- `300` — سهام (Stock)
- `301` — حق تقدم (Preemptive Right)

See `references/flow-and-yval-codes.md` for the complete list of yVal, flow, cgrValCot, and cEtaval codes.

## Complete Endpoint Reference

See `references/api-endpoints.md` for the full catalog with URLs, parameters, response shapes, and example outputs for every endpoint across all three API surfaces (~50+ endpoints).

## Workflows

### Workflow 1: Search + Get Instrument Info

```python
import urllib.request, json

def search_symbol(query: str) -> list[dict]:
    """Search for instruments by Persian symbol name."""
    url = f"https://cdn.tsetmc.com/api/Instrument/GetInstrumentSearch/{urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("instrumentSearch", [])

def instrument_info(ins_code: str) -> dict:
    """Get full instrument info including EPS, sector, thresholds."""
    url = f"https://cdn.tsetmc.com/api/Instrument/GetInstrumentInfo/{ins_code}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("instrumentInfo", {})

# Example: find فولاد
results = search_symbol("فولاد")
# results[0] = {
#   "insCode": "46348559193224090",
#   "lVal30": "فولاد مباركه اصفهان",
#   "lVal18AFC": "فولاد",
#   "flow": 1,  # بورس
#   ...
# }

info = instrument_info(results[0]["insCode"])
```

### Workflow 2: Get Market Watch (All Live Prices)

```python
import urllib.request

def market_watch_init() -> str:
    """Get all live prices in CSV format."""
    url = "http://old.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0"
    resp = urllib.request.urlopen(url)
    return resp.read().decode("utf-8")

# Response is split by @ into 5 parts:
# 1. Handle message (notification IDs)
# 2. Market state (index values, volumes)
# 3. Price rows (semicolon-separated, 26 columns each)
# 4. Best limit rows
# 5. Reference ID (for polling updates)

raw = market_watch_init()
handle_msg, market_state, price_rows, best_limits, refid = raw.split("@")
```

The 26 columns per price row (comma-separated):
`ins_code, isin, l18, l30, heven, pf, pc, pl, tno, tvol, tval, pmin, pmax, py, eps, bvol, visitcount, flow, cs, tmax, tmin, z, yval, predtran, buyop, cgrvalcot`

### Workflow 3: Get Last Trading Day

```python
def last_trading_day() -> str:
    """Get the most recent trading day in YYYYMMDD format."""
    url = "http://service.tsetmc.com/tsev2/data/TseClient2.aspx?t=LastPossibleDeven"
    resp = urllib.request.urlopen(url)
    return resp.read().decode("utf-8")  # e.g. "20260712;20260712"
```

### Workflow 4: Daily Price History

The CDN API (`GetClosingPriceDailyList`) returns **all historical daily prices in one JSON response** — no pagination needed. Each response is typically 0.2–1.5 MB depending on stock age.

**Sample verified (July 2026):** فولاد مبارکه (insCode `46348559193224090`) returned **4,599 records** from 20070311 to 20260719, ~1,560 KB JSON.

**Scaling estimate for full universe (409 stocks):**
- Raw JSON: ~200–400 MB total
- Processed parquet (daily prices): ~50 MB
- Processed parquet (monthly returns): ~3 MB

```python
# Old API (more reliable)
def price_history_csv(ins_code: str, top: int = 100) -> str:
    """Get price history as CSV-like text.
    Columns: date, pmax, pmin, pc, pl, pf, py, tval, tvol, tno
    """
    url = f"http://old.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={ins_code}&Top={top}&A=0"
    resp = urllib.request.urlopen(url)
    return resp.read().decode("utf-8")

# New CDN API (all history, no pagination)
def closing_price_daily(ins_code: str, n: int = 0) -> list:
    """Get daily closing prices. n=0 for all history.
    Returns up to ~4,600 records per stock for major companies.
    Each record has: dEven (date), pClosing, pDrCotVal (last trade),
    priceMin, priceMax, priceYesterday, priceFirst,
    qTotTran5J (volume), qTotCap (value), zTotTran (trades),
    priceChange, iClose, yClose, last.
    ~0.2-1.5 MB JSON per stock.
    """
    url = f"https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/{ins_code}/{n}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("closingPriceDaily", [])
```

### Workflow 5: Historical Shares Outstanding (Market Cap)

Two complementary approaches — use Share Change events for full price adjustment + shares timeline, use InstrumentHistory for point-in-time lookups.

#### Method A: Share Change Events (preferred for price adjustment + shares panel)

```python
def share_changes(ins_code: str) -> list[dict]:
    \"\"\"Get ALL share change events (splits, capital increases, rights issues).
    Returns list of {dEven, numberOfShareOld, numberOfShareNew}.
    
    Use this to:
    1. Build historical shares as a step function
    2. Compute price adjustment factors for split-adjusted returns
    
    NOTE: API often returns DUPLICATE entries for the same event.
    Always deduplicate by (dEven, numberOfShareOld, numberOfShareNew).
    \"\"\"
    url = f\"https://cdn.tsetmc.com/api/Instrument/GetInstrumentShareChange/{ins_code}\"
    req = urllib.request.Request(url, headers={\"User-Agent\": \"Mozilla/5.0\"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    changes = data.get(\"instrumentShareChange\", [])
    # Deduplicate
    seen = set()
    unique = []
    for c in changes:
        key = (c[\"dEven\"], c[\"numberOfShareOld\"], c[\"numberOfShareNew\"])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique

# Example: فرآور share changes
changes = share_changes(\"408934423224097\")
# [{dEven: 20250712, old: 660000000.0, new: 5000000000.0}, ...]

# --- Price adjustment factor ---
# For a date D, adj_factor = product of (old/new) for ALL changes AFTER D
# adjusted_price = raw_price * adj_factor
# This makes pre-split prices comparable to the most recent share count.
def adj_factor(changes: list, date_int: int) -> float:
    factor = 1.0
    for c in reversed(changes):
        if date_int < c[\"dEven\"]:
            old, new = c[\"numberOfShareOld\"], c[\"numberOfShareNew\"]
            if new and new > 0 and old and old > 0:
                factor *= (old / new)
    return factor

# --- Shares at date ---
def shares_at(changes: list, current_shares: float, date_int: int) -> float:
    if not changes:
        return current_shares
    shares = current_shares
    for c in reversed(changes):
        if date_int >= c[\"dEven\"]:
            shares = c[\"numberOfShareNew\"] or shares
            break
    else:
        shares = changes[0][\"numberOfShareOld\"] or shares
    return shares
```

#### Method B: Point-in-time lookup (single date)

```python
def historical_shares(ins_code: str, date: str) -> float:
    \"\"\"Get total shares outstanding at a specific Gregorian date (YYYYMMDD).
    Combine with closing price for market cap: pClosing * zTitad.
    Works from ~2009 onward; earlier dates may return 500.\"\"\"
    url = f\"https://cdn.tsetmc.com/api/Instrument/GetInstrumentHistory/{ins_code}/{date}\"
    req = urllib.request.Request(url, headers={\"User-Agent\": \"Mozilla/5.0\"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data[\"instrumentHistory\"][\"zTitad\"]
```

### Workflow 6: Dividend Per Share (for Total Returns)

```python
def dps_history(symbol: str) -> list[dict]:
    \"\"\"Get dividend per share history for a Persian symbol.
    Returns list of {fiscal_year, meeting_date, dps} dicts.\"\"\"
    import urllib.parse
    url = f\"http://old.tsetmc.com/tsev2/data/DPSData.aspx?s={urllib.parse.quote(symbol)}\"
    req = urllib.request.Request(url, headers={\"User-Agent\": \"Mozilla/5.0\"})
    resp = urllib.request.urlopen(req)
    raw = resp.read().decode(\"utf-8\")
    records = []
    seen = set()
    for row in raw.split(\";\"):
        cols = row.split(\"@\")
        if len(cols) >= 7 and cols[6]:
            dps = cols[6].strip()
            try:
                dps_val = float(dps)
                if dps_val > 0:
                    key = (cols[2], dps_val)  # (fiscal_year, dps)
                    if key not in seen:
                        seen.add(key)
                        records.append({\"fy\": cols[2], \"meeting\": cols[1], \"dps\": dps_val})
                    except ValueError:
                        pass
    return records

# Then for total return: add DPS to price in the month of the meeting date
```

### Workflow 7: Total-Return Adjusted Prices (PREFERRED for return calculation)

`GetPriceAdjustList` returns **total-return adjusted** price events — every ex-dividend and split date with both an adjusted (`pClosing`) and unadjusted (`pClosingNotAdjusted`) closing price. The ratio = `(price_before_meeting - DPS) / price_before_meeting` — verified by exact DPS cross-reference (16/16 events matched for فرآور, July 2026).

**⚠️ PARTIAL COVERAGE — must combine with `GetInstrumentShareChange` (see Workflow 7b below).** `GetPriceAdjustList` captures both stock splits AND cash dividend payouts in a single cumulative factor, which is more complete than share-change-only adjustment. **However, it misses ~45% of capital increase events.** In a 392-stock universe (July 2026 audit), `GetPriceAdjustList` had 5,837 events but `GetInstrumentShareChange` found 2,147 events — 1,122 (52.3%) of which were NOT covered by `GetPriceAdjustList`. Example: قصفها had a 155× capital increase (195M → 30.19B shares) on 2024-09-30 that `GetPriceAdjustList` completely missed, producing a false -99.4% monthly return. **Use Workflow 7b (combined) as the authoritative method.**

```python
def price_adjustments(ins_code: str) -> list[dict]:
    \"\"\"Get total-return adjustment events (splits + dividends).
    Returns list of {dEven, pClosing (adjusted), pClosingNotAdjusted (raw)}.
    Checked_verified: ratio = (price_before_meeting - pure_dps) / price_before_meeting
    — matches R365 DPS data exactly.\"\"\"
    url = f\"https://cdn.tsetmc.com/api/ClosingPrice/GetPriceAdjustList/{ins_code}\"
    req = urllib.request.Request(url, headers={\"User-Agent\": \"Mozilla/5.0\"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get(\"priceAdjust\", [])

# --- Building adjusted price series from PriceAdjustList ---
# At each adjustment event date D:
#   ratio = pClosing / pClosingNotAdjusted (typically <1, captures dividend+split)
# For any price at date T, cumulative adj_factor = product(ratio_i for all events_i where D_i > T)
# adjusted_price = raw_price * cumulative_adj_factor
# This produces total-return adjusted prices comparable across the full history.

adjustments = price_adjustments(\"408934423224097\")  # فرآور
# Sort by date, then for each raw price, multiply by product of all future ratios:
events = sorted(adjustments, key=lambda x: x['dEven'])
ratios = [(a['dEven'], a['pClosing'] / a['pClosingNotAdjusted']) for a in events if a['pClosingNotAdjusted']]

def adj_factor(date_int: int) -> float:
    \"\"\"Cumulative adjustment factor = product of ratios for ALL events AFTER date_int.\"\"\"
    factor = 1.0
    for d, r in reversed(ratios):
        if date_int < d:
            factor *= r
    return factor

# --- Key advantage over GetInstrumentShareChange ---
# GetInstrumentShareChange only adjusts for share count changes (splits/capital increases).
# GetPriceAdjustList adjusts for BOTH splits AND cash dividends.
# In practice: 7.4% of monthly returns differed by >0.1% between the two methods.
# The difference captures the monthly dividend yield (~0.2%/month for Iran).
# For factor construction, total-return adjusted prices are essential.
```

**Sample data (فرآور, July 2026):** 16 adjustment events from 2010-05-08 to 2025-07-21. Some events coincide with share changes (splits), others are pure dividend adjustments. The 5,837 total events across 392 stocks average ~15 per stock.

### Workflow 7b: Combined Total-Return Adjusted Prices (AUTHORITATIVE)

**Problem:** Neither API alone is complete:
- `GetPriceAdjustList` covers dividends + ~55% of splits but misses ~45% of capital increases
- `GetInstrumentShareChange` covers all capital increases but misses dividend adjustments

**Solution:** Merge both event streams, deduplicating by 7-day proximity window (54.9% overlap).

```python
def combined_adjusted_prices(ins_code: str, prices: list, current_shares: float):
    """Build total-return adjusted prices combining both TSETMC APIs.
    
    Steps:
    1. Download events from GetPriceAdjustList (dividends + some splits)
    2. Download events from GetInstrumentShareChange (all capital increases)
    3. For each share change, skip if a PriceAdjustList event exists within ±7 days
    4. Merge remaining events into a single timeline
    5. For each price date, cumulative_factor = product of all future event ratios
    6. adjusted_price = raw_price * cumulative_factor
    """
    # Method 1 events: PriceAdjustList
    ts_events = price_adjustments(ins_code)
    ts_ratios = [(a['dEven'], a['pClosing'] / a['pClosingNotAdjusted']) 
                 for a in ts_events if a.get('pClosingNotAdjusted')]
    ts_dates = set(d for d, _ in ts_ratios)
    
    # Method 2 events: InstrumentShareChange (deduplicated, pre-IPO filtered)
    sc_events = share_changes(ins_code)  # already deduplicated per Workflow 5
    sc_ratios = []
    for c in sc_events:
        old_s = c['numberOfShareOld']
        new_s = c['numberOfShareNew']
        if old_s < 1000:  # skip pre-IPO placeholders
            continue
        # Skip if PriceAdjustList already covers this event (within 7 days)
        if any(abs(c['dEven'] - ad) <= 7 for ad in ts_dates):
            continue
        sc_ratios.append((c['dEven'], old_s / new_s))
    
    # Merge: for each date, product of all ratios
    from collections import defaultdict
    by_date = defaultdict(lambda: 1.0)
    for d, r in ts_ratios:
        by_date[d] *= r
    for d, r in sc_ratios:
        by_date[d] *= r
    merged = sorted(by_date.items())
    
    # Apply: for each price, cumulative factor = product of all future ratios
    for p in prices:
        dEven = p['dEven']
        factor = 1.0
        for ev_date, ev_ratio in reversed(merged):
            if dEven < ev_date:
                factor *= ev_ratio
        p['pClosing_adj'] = p['pClosing'] * factor
    
    return prices

# VERIFIED (July 2026, 392 stocks):
# - قصفها Oct 2024: was -99.4% (TSETMC-only missed 155x split), now -6.58% ✅
# - غسالم Aug 2013: was 3861% (double-counting before dedup), now 296% ✅
# - 194 extreme >100% returns remain (genuine trading-halt→resume price gaps)
# - Filter qTotTran5J==0 days (261K halt days, 17% of all records) before returns
```

**See `references/price-adjustment-verification.md` for the full audit methodology, cross-validation results, and the round-by-round debugging that led to this solution.**

### Workflow 8: Client Type (حقیقی-حقوقی)

```python
def client_type_history(ins_code: str) -> list[dict]:
    url = f"https://cdn.tsetmc.com/api/ClientType/GetClientTypeHistory/{ins_code}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("clientType", [])

# Fields: recDate, insCode, buy_I_Volume, buy_N_Volume, buy_I_Value, buy_N_Value,
#          sell_I_Volume, sell_N_Volume, ...
# I = حقیقی (individual/natural person), N = حقوقی (legal/institutional)
```

### Workflow 9: All Client Types (Summary)

```python
def all_client_types() -> str:
    """Get today's client type summary for all instruments. CSV-like."""
    url = "http://old.tsetmc.com/tsev2/data/ClientTypeAll.aspx"
    resp = urllib.request.urlopen(url)
    return resp.read().decode("utf-8")
# Format: ins_code,n_buy_count,l_buy_count,n_buy_volume,l_buy_volume,...
# semicolon-separated rows
```

### Workflow 10: Market Messages / Announcements

```python
def messages(flow: int = 0, top: int = 10) -> list[dict]:
    url = f"https://cdn.tsetmc.com/api/Msg/GetMsgByFlow/{flow}/{top}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("msg", [])
```

### Workflow 11: Trade Top Lists (Most Visited, Top Gainers, etc.)

```python
def trade_top(category: str, flow: int = 1, top: int = 10) -> list[dict]:
    \"\"\"Categories: MostVisited, ETF, MostTradedETF, PClosingTopETF, PClosingBtmETF, CommodityFund\"\"\"
    url = f"https://cdn.tsetmc.com/api/ClosingPrice/GetTradeTop/{category}/{flow}/{top}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("tradeTop", [])
```

### Workflow 12: Index History

```python
def index_last_state() -> list[dict]:
    \"\"\"Get latest state of all indices.\"\"\"
    url = "https://cdn.tsetmc.com/api/Index/GetIndexB1LastAll/All/1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read()).get("indexB1", [])

def index_daily_history(index_code: str) -> list[dict]:
    \"\"\"Get daily history for a specific index.\"\"\"
    url = f"https://cdn.tsetmc.com/api/Index/GetIndexB2History/{index_code}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read()).get("indexB2", [])
```

### Workflow 13: Fund/ETF Data

```python
def funds(fund_type: str = "6") -> list[dict]:
    \"\"\"Get fund list by type. Types: 6=Stock, 7=Mixed, 4=Fixed, 5=Commodity, 14=REIT, 17=Fund\"\"\"
    url = f"https://cdn.tsetmc.com/api/Fund/GetFunds/{fund_type}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read()).get("funds", [])

def etf_info(ins_code: str) -> dict:
    \"\"\"Get ETF redemption NAV data.\"\"\"
    url = f"https://cdn.tsetmc.com/api/Fund/GetETFByInsCode/{ins_code}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read()).get("etf", {})
```

### Workflow 14: Codal Report Discovery (Global, No Rate Limit)

The CDN API includes a Codal proxy that works globally with **no rate limiting** — it bypasses CODAL's geo-restriction and 429 block entirely.

```python
def codal_prepared_data(ins_code: str, n: int = 500) -> list[dict]:
    \"\"\"Get CODAL report metadata for an instrument. Returns filings with:
    - id, symbol, name, title, tracingNo (numeric TracingNo)
    - hasHtmlReport (0/1/2), hasExcelReport (0/1), hasPDFReport (0/1/2)
    - attachmentID, contentType, fileName, fileExtension
    - publishDateTime_Gregorian (ISO format)
    
    LIMITATION: Returns TracingNo but NOT LetterSerial. To get 
    the LetterSerial (needed for Excel downloads), use the CODAL 
    search API search_by_tracing_no() function with the tracingNo.
    \"\"\"
    url = f\"https://cdn.tsetmc.com/api/Codal/GetPreparedDataByInsCode/{n}/{ins_code}\"
    req = urllib.request.Request(url, headers={\"User-Agent\": \"Mozilla/5.0\"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read()).get(\"preparedData\", [])

# Example: find parent-company annual reports with Excel for فولاد
reports = codal_prepared_data(\"46348559193224090\")
parent_reports = [r for r in reports 
    if \"(شرکت\" not in r.get(\"title\", \"\") 
    and \"صورت\" in r.get(\"title\", \"\")
    and \"سال مالی\" in r.get(\"title\", \"\")
    and r.get(\"hasExcelReport\") == 1]
for r in sorted(parent_reports, key=lambda x: x[\"tracingNo\"], reverse=True):
    print(f\"  {r['title'][:60]} tn={r['tracingNo']}\")
```

### Workflow 15: Codal Publisher Info

```python
def codal_publisher(symbol: str) -> dict:
    \"\"\"Get company info from Codal (address, managers, ISIC, etc.).\"\"\"
    url = f\"https://cdn.tsetmc.com/api/Codal/GetCodalPublisherBySymbol/{urllib.parse.quote(symbol)}\"
    req = urllib.request.Request(url, headers={\"User-Agent\": \"Mozilla/5.0\"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read()).get(\"codalPublisher\", {})
```

### Workflow 16: Instrument Identity

```python
def instrument_identity(ins_code: str) -> dict:
    \"\"\"Get instrument identity data (sector, sub-sector, ISIN, etc.).\"\"\"
    url = f"https://cdn.tsetmc.com/api/Instrument/GetInstrumentIdentity/{ins_code}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read()).get("instrumentIdentity", {})
```

## Pitfalls

- **Market hours matter** — Many CDN API endpoints return empty arrays `[]` when the market is closed. The old CSV-based endpoints (MarketWatchInit, ClientTypeAll) return data regardless. Always have a fallback.
- **`insCode` is NOT the ISIN** — The 15-20 digit `insCode` is different from the ISIN (e.g., `IRO1FOLD0001`). Use search to find `insCode` by symbol name.
- **Plain HTTP for old API** — `old.tsetmc.com` and `service.tsetmc.com` use plain HTTP, not HTTPS. Some Python libraries/security tools may block mixed content.
- **Geo-restriction on old.tsetmc.com** — While the CDN API (`cdn.tsetmc.com`) was previously accessible globally, **as of July 2026 the CDN is also geo-blocked** (returns HTTP 303→403 from outside Iran). **All TSETMC API surfaces now require an Iran-based proxy.** The old CSV API surfaces (`old.tsetmc.com`, `members.tsetmc.com`, `service.tsetmc.com`) remain geo-restricted as before.
- **User-Agent header is REQUIRED** — without a browser User-Agent, the CDN API silently returns empty arrays `{"closingPriceDaily":[]}` even when data exists. Always set `-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'` in curl, or `headers={"User-Agent": "Mozilla/5.0"}` in Python.
- **CDN API endpoint status varies** — Most CDN endpoints work, but some are unreliable. **Confirmed working (July 2026, when accessible):** `ClosingPriceDailyList` (returns ALL daily prices, verified ~4,602 records for فولاد at ~1.5 MB — one call, no pagination), `Instrument/GetInstrument` (returns zTitad shares outstanding), `InstrumentSearch`, `InstrumentInfo`, `InstrumentIdentity`, `ClientTypeHistory`, `GetPriceAdjustList`, `Codal/GetPreparedDataByInsCode`, `Msg/GetMsgByFlow`, `Fund/GetFunds`. Known empty/deprecated: `MarketOverview`, `IndexB1LastAll`, `ClosingPriceGetMarketMap`, `SectorsSummary`, `GetInstrumentHistory/{insCode}/{date}` (shares endpoint — use `GetInstrument` or `GetClosingPriceDailyList` instead).
- **Persian Unicode normalization** — Search queries in Persian need URL encoding. The server handles standard UTF-8 Persian text (ی vs ي normalization may matter).
- **Rate limiting** — TSETMC doesn't document rate limits but aggressive polling (faster than 1 req/sec) may result in dropped connections. Use 0.5-1s delays between historical data requests.
- **MarketWatchPlus polling** — The live market watch uses a polling pattern with `heven` (incremented in 5s intervals) and `refid` (incremented in 25s intervals). The response format changes dynamically.
- **BestLimits empty outside trading hours** — Order book data (`BestLimits`) shows empty arrays when the market is closed. This is normal.
- **MarketWatchInit is incomplete** — `MarketWatchInit` does NOT return all active TSE stocks. Some major stocks (e.g., فولاد Mobarakeh Steel) are absent even though they trade actively (yVal=300, flow=1). To build a complete stock universe, you must merge MarketWatchInit with TSETMC Search results from CODAL company symbols. See `references/building-stock-universe.md` for the complete pipeline.
- **Trading halt placeholder prices (CRITICAL for returns)** — TSETMC uses `pClosing=1000` (or `pClosing=1.0`) with `qTotTran5J=0` (zero volume) as a placeholder during trading halts. These are NOT real market prices. If you compute returns from raw prices, they produce extreme fake returns (e.g., 50,000% in a month) when trading resumes at a real price. **Always filter `qTotTran5J == 0` days before computing returns.** In a 1.5M-day dataset, 261K days (17%) were halt days — removing them eliminated most extreme-return artifacts.
- **`GetInstrumentShareChange` returns duplicates** — The API frequently returns the same event 2–3 times. Always deduplicate by `(dEven, numberOfShareOld, numberOfShareNew)` before building adjustment factors, or you'll apply the same factor multiple times and destroy the price series.
- **Raw prices from `GetClosingPriceDailyList` are UNADJUSTED** — 67% of stocks (263/391) have price discontinuities from capital increases/splits. Three methods to adjust, in order of completeness:
  1. **AUTHORITATIVE: Combined adjustment (Workflow 7b)** — Merges `GetPriceAdjustList` (dividends + some splits, 5,837 events) with `GetInstrumentShareChange` (all capital increases, 2,147 events). Deduplicates by 7-day window to avoid double-counting (54.9% overlap between the two APIs). Produces complete total-return adjusted prices.
  2. **`GetPriceAdjustList` only** — Returns adjusted/raw price pairs at each dividend event, useful for building total-return series. However, it misses ~45% of capital increase events. Each record has `pClosing` (adjusted) and `pClosingNotAdjusted` (raw). Verified by exact DPS cross-reference (16/16 events matched for فرآور, July 2026). See Workflow 7 for the recipe.
  3. **`GetInstrumentShareChange` only** — Returns share change events (no dividend adjustment). Compute `adj_factor(date) = product(old/new for all changes after date)`, then `adjusted_price = raw_price × adj_factor`. Only adjusts for splits, misses ~0.2%/month dividend yield. Always use Method 1 (combined) for production work.
- **`GetInstrumentHistory/{insCode}/{date}` is deprecated/empty** — Returns nothing for many instruments. Use `GetInstrumentShareChange` + current `GetInstrument` (zTitad) to build the full shares timeline instead.

## Complementary Libraries (for reference)

The open-source ecosystem has already reverse-engineered most of these endpoints:

| Library | Stars | Language | Highlights |
|---------|-------|----------|------------|
| `ghodsizadeh/tehran-stocks` | ⭐464 | Python | ORM-based, SQLite/PostgreSQL storage, bulk download |
| `Glyphack/pytse-client` | ⭐304 | Python | Async, Ticker class, client types, shareholders |
| `5j9/tsetmc` | ⭐31 | Python | Async+sync, Polars DataFrames, full API coverage, well-typed |
| `shahradelahi/tsetmc-client` | ⭐165 | TypeScript | Node.js client |

## Support Files

- `references/api-endpoints.md` — Complete endpoint catalog with ~50+ endpoints across all three API surfaces, request/response schemas, and example JSON
- `references/data-schemas.md` — Typed dict definitions for all API response types (InstrumentInfo, ClosingPriceInfo, ClientType, ShareHolder, MarketState, Search, LiveData, etc.)
- `references/flow-and-yval-codes.md` — Market flow codes, yVal asset type codes, cgrValCot market group codes, cEtaval instrument status codes, and other enumeration values
- `references/building-stock-universe.md` — End-to-end pipeline for constructing a clean stock universe from CODAL + TSETMC: batch search, dual-source merge, dedup by normalized ticker, sector enrichment, fund filtering, and quality audit.
- `references/instrument-versioning.md` — The "3" suffix pattern: how TSETMC creates new instrument records after capital increases, creating duplicate entries per company. How to deduplicate when cross-referencing with CODAL.
- `references/price-adjustment-verification.md` — Audit methodology for the combined price adjustment method (Workflow 7b): cross-validation results, round-by-round debugging, and verification of the merged GetPriceAdjustList + GetInstrumentShareChange approach.
- `templates/python-client.py` — Full Python client class with 40+ methods covering all three API surfaces, using only stdlib
- `templates/pytse-client-usage.md` — Quick usage patterns for the pytse-client package (async, Pandas-based)
- `templates/tsetmc-package-usage.md` — Quick usage patterns for the tsetmc (5j9) package (async+sync, Polars-based, full coverage)