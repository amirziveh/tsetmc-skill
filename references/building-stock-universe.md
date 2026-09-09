# Building a Complete Iranian Stock Universe from CODAL + TSETMC

## Why This Is Needed

Neither CODAL nor TSETMC alone gives a complete list of exchange-traded common stocks:

- **CODAL `/v1/companies`** — 5,388 entries, but most are NOT stocks (water authorities, auditors, funds, bonds). Filtering to `st=0` + short symbols gives ~519 candidates.
- **TSETMC `MarketWatchInit`** — 566 active instruments with yVal=300, but **incomplete** — major stocks like فولاد (Mobarakeh Steel) are missing from its output.

A dual-source merge is required to capture all stocks.

## Step-by-Step Pipeline

### 1. Fetch CODAL Companies

```python
import urllib.request, json
# Must run from inside Iran (codal.ir is geo-restricted)
url = "https://search.codal.ir/api/search/v1/companies"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=30)
companies = json.loads(resp.read())
```

### 2. Filter to Exchange-Listed Candidates

Real stocks have:
- `st=0` (TSE Bourse) or `st=1` (Fara Bourse)
- Symbol length ≤ 8 Persian characters (filters out water authorities, auditors, etc.)

```python
candidates = [c for c in companies if c.get("st") == 0 and len(c.get("sy", "").strip()) <= 8]
# This yields ~519 companies (from 5,388 total)
```

**Why symbol length works:** Non-trading entities registered with CODAL (regional water departments, auditing firms, holding shells) use their full Persian company name as the `sy` field — often 15-40+ characters.

### 3. Batch-Search Each Candidate on TSETMC

The CDN search API (`cdn.tsetmc.com`) is accessible globally. Use the CODAL `sy` (ticker symbol) as the query:

```python
import urllib.parse, time

def search_tsetmc(symbol):
    url = "https://cdn.tsetmc.com/api/Instrument/GetInstrumentSearch/" + urllib.parse.quote(symbol)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    return data.get("instrumentSearch", [])

# Batch in parallel groups of ~170 with 0.1s delay between calls
# Rate limit: undocumented, but 0.1-0.3s delays work for 500+ calls
```

**Result**: ~518/519 symbols found. The ~1 not-found is typically a fund, not a stock.

### 4. Fetch MarketWatchInit Data

```python
url = "http://old.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0"
# geo-restricted — use Iran proxy if outside Iran
resp = urllib.request.urlopen(url)
raw = resp.read().decode("utf-8")
parts = raw.split("@")
price_rows = parts[2]
```

Parse the 26-column rows. Filter to `yVal=300` (stock) and `flow=1` (TSE):

```python
stocks = []
for row in price_rows.split(";"):
    cols = row.split(",")
    if len(cols) >= 24 and cols[22] == "300" and cols[17] == "1":
        stocks.append(cols)  # insCode at cols[0], l30 at cols[3], l18 at cols[2]
```

### 5. Merge and Deduplicate

Two sources → 700+ candidate entries. Deduplicate by normalized ticker:

```python
import re

def normalize_ticker(t):
    t = t.strip()
    t = t.replace("\u064a", "\u06cc")  # Arabic Yeh -> Persian Yeh
    t = re.sub(r'[23]$', '', t)        # Strip "2" or "3" suffixes (old symbols)
    return t
```

**Dedup rules:**
1. Strip trailing "3" (post-capital-change version) and "2" (legacy symbol)
2. When two entries share the same normalized ticker, keep the non-"3"/non-"2" version
3. Prefer entries with a CODAL match (more metadata)

### 6. Fetch Sector Info

For each unique stock, fetch instrument identity to get sector classification:

```python
def get_sector(ins_code):
    url = f"https://cdn.tsetmc.com/api/Instrument/GetInstrumentIdentity/{ins_code}"
    resp = urllib.request.urlopen(url)
    data = json.loads(resp.read())
    identity = data.get("instrumentIdentity", {})
    sector = identity.get("sector", {})
    return sector.get("lSecVal", "")  # Persian sector name
```

### 7. Filter Out Funds / Non-Equity

Remove entries where:
- `sector_name == "صندوق سرمایه گذاری قابل معامله"` (ETFs)
- Company name starts with "صندوق" or "بخشی" (fund tranches)
- `flow` is not 1 (Fara Bourse or commodity instruments)

### 8. Quality Audit Checklist

| Check | What to verify |
|-------|---------------|
| Duplicate tickers | Use Counter — should be 0 |
| Duplicate insCodes | Should be 0 |
| Major stocks present | فولاد, شپنا, فملی, خودرو, وبصادر, شبندر, حكشتی, كگل, كچاد |
| Persian Yeh normalization | No Arabic Yeh (ي) in tickers — all should be ی |
| Sector coverage | 35-45 distinct sectors normal |
| Numeric suffixes | No "2" or "3" ending tickers remaining |
| Fund infiltration | Spot-check 10 random entries — none should be funds |

## Expected Results (TSE, 2025 data)

| Metric | Value |
|--------|-------|
| Total stocks | ~400-410 |
| From CODAL | ~310-330 |
| MW-only (not in CODAL) | ~80-100 |
| Industry sectors | ~41 |
| CODAL match rate | ~75-80% |
| Correctly excluded funds/ETFs | ~100-110 |

## Key Pitfalls

- **MarketWatchInit is incomplete**: Don't rely on it as the sole source. Always merge with CODAL search results.
- **CODAL st=0 ≠ stock**: Many TSE-registered entities are funds. The symbol-length filter and sector-name filter catch most.
- **"3" and "2" suffixes**: ~1 in 3 active TSE stocks has a "3"-suffixed duplicate. Always normalize.
- **Persian/Arabic Yeh**: CODAL uses both ي (Arabic Yeh) and ی (Persian Yeh) inconsistently. Normalize before matching.
- **Rate limits**: TSETMC CDN API tolerates 0.1s delays for batch searches; CODAL API will 429 after ~45 requests at 0.8s delays.
