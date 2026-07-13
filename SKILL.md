---
name: tsetmc
description: "Reverse-engineer and use the TSETMC (Tehran Stock Exchange) API ecosystem — three API surfaces (CDN REST JSON, old tsev2 CSV, and ParTree HTML), 50+ endpoints for instrument data, price history, indices, client types, order books, shareholders, and messages."
version: 1.0.0
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
- **Headers**: standard browser User-Agent. No auth needed.
- **Status**: Partially active. Some endpoints return empty data when market is closed. Others (ClosingPriceDailyList, MarketOverview, IndexB1LastAll) consistently return empty/fail — likely deprecated on the server side.

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

```python
# Old API (more reliable)
def price_history_csv(ins_code: str, top: int = 100) -> str:
    """Get price history as CSV-like text.
    Columns: date, pmax, pmin, pc, pl, pf, py, tval, tvol, tno
    """
    url = f"http://old.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={ins_code}&Top={top}&A=0"
    resp = urllib.request.urlopen(url)
    return resp.read().decode("utf-8")

# New API (sometimes empty)
def closing_price_daily(ins_code: str, n: int = 0) -> list:
    """Get daily closing prices. n=0 for all history."""
    url = f"https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/{ins_code}/{n}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("closingPriceDaily", [])
```

### Workflow 5: Shareholders

```python
def major_shareholders(ins_code: str) -> list[dict]:
    url = f"https://cdn.tsetmc.com/api/Shareholder/GetInstrumentShareHolderLast/{ins_code}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("shareHolder", [])

# Returns: [{shareHolderName, cIsin, numberOfShares, perOfShares, change, ...}, ...]
```

### Workflow 6: Client Type (حقیقی-حقوقی)

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

### Workflow 7: All Client Types (Summary)

```python
def all_client_types() -> str:
    """Get today's client type summary for all instruments. CSV-like."""
    url = "http://old.tsetmc.com/tsev2/data/ClientTypeAll.aspx"
    resp = urllib.request.urlopen(url)
    return resp.read().decode("utf-8")
# Format: ins_code,n_buy_count,l_buy_count,n_buy_volume,l_buy_volume,...
# semicolon-separated rows
```

### Workflow 8: Market Messages / Announcements

```python
def messages(flow: int = 0, top: int = 10) -> list[dict]:
    url = f"https://cdn.tsetmc.com/api/Msg/GetMsgByFlow/{flow}/{top}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("msg", [])
```

### Workflow 9: Trade Top Lists (Most Visited, Top Gainers, etc.)

```python
def trade_top(category: str, flow: int = 1, top: int = 10) -> list[dict]:
    \"\"\"Categories: MostVisited, ETF, MostTradedETF, PClosingTopETF, PClosingBtmETF, CommodityFund\"\"\"
    url = f"https://cdn.tsetmc.com/api/ClosingPrice/GetTradeTop/{category}/{flow}/{top}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("tradeTop", [])
```

### Workflow 10: Index History

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

### Workflow 11: Fund/ETF Data

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

### Workflow 12: Codal Publisher Info

```python
def codal_publisher(symbol: str) -> dict:
    \"\"\"Get company info from Codal (address, managers, ISIC, etc.).\"\"\"
    url = f"https://cdn.tsetmc.com/api/Codal/GetCodalPublisherBySymbol/{urllib.parse.quote(symbol)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read()).get("codalPublisher", {})
```

### Workflow 13: Instrument Identity

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
- **CDN API partially reliable** — Some CDN endpoints (ClosingPriceDailyList, MarketOverview, IndexB1LastAll, ClosingPriceGetMarketMap, SectorsSummary, GetInstrumentHistory) consistently return empty responses — they may be deprecated server-side. Prefer the old API equivalents for these use cases.
- **Persian Unicode normalization** — Search queries in Persian need URL encoding. The server handles standard UTF-8 Persian text (ی vs ي normalization may matter).
- **Rate limiting** — TSETMC doesn't document rate limits but aggressive polling (faster than 1 req/sec) may result in dropped connections. Use 0.5-1s delays between historical data requests.
- **MarketWatchPlus polling** — The live market watch uses a polling pattern with `heven` (incremented in 5s intervals) and `refid` (incremented in 25s intervals). The response format changes dynamically.
- **BestLimits empty outside trading hours** — Order book data (`BestLimits`) shows empty arrays when the market is closed. This is normal.

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
- `templates/python-client.py` — Full Python client class with 40+ methods covering all three API surfaces, using only stdlib
- `templates/pytse-client-usage.md` — Quick usage patterns for the pytse-client package (async, Pandas-based)
- `templates/tsetmc-package-usage.md` — Quick usage patterns for the tsetmc (5j9) package (async+sync, Polars-based, full coverage)