# TSETMC Instrument Versioning: The "3" Suffix Pattern

## What It Is

When an Iranian company undergoes a capital increase (افزایش سرمایه), stock split, or other major corporate action, TSETMC **does not update the existing instrument record in place**. Instead, it creates a **new instrument record** with a modified `lVal18AFC` (Persian ticker) — typically the base ticker followed by a digit suffix like "3".

## Examples

| Company | Base Ticker (CODAL) | Post-Change Ticker (TSETMC) |
|---------|---------------------|------------------------------|
| Tehran Stock Exchange | بورس | بورس3 |
| Saipa | خساپا | خساپا3 |
| Tamin Petroleum & Petrochemical Investment | وتامين | وتامين3 |
| Iran Khodro | خودرو | خودرو3 |

## How It Manifests in the APIs

### MarketWatchInit
The `l30` field still shows the original company name (e.g. "بورس اوراق بهادار تهران"), but the `l18` (English name) ends with "3" (e.g. "بورس3").

### CDN Search API
Searching by the **base ticker** symbol (e.g. "بورس") returns the CURRENT instrument record — this has a **different `insCode`** than the post-change record. Both records exist simultaneously with different insCodes.

### GetInstrumentInfo / GetInstrumentIdentity
These work with both insCodes. The `lVal18AFC` field returns the ticker as registered for that specific instrument version.

## Impact on Stock Universe Construction

When building a stock universe by cross-referencing CODAL with TSETMC:

1. **CODAL lists companies by their BASE ticker** (e.g. "بورس") — the `sy` field is always the base symbol
2. **MarketWatchInit may have the POST-CHANGE version** (e.g. "بورس3") for the same company
3. **Searching TSETMC by base ticker** returns the current record — which has a **different insCode** than the MW post-change record
4. **Both insCodes are valid** and both point to the same underlying company

### Handling in Practice

```
MW stock:    insCode=A, l18="بورس3",    l30="بورس اوراق بهادار تهران"
Search API:  insCode=B, lVal18AFC="بورس", lVal30="بورس اوراق بهادار تهران"

Both A and B → same company. Keep ONE (prefer the non-"3" version).
```

**Dedup strategy:** strip trailing "3" from ticker symbols before deduplicating, then keep the non-"3" version when both exist.

## Which insCode to Use for Data Collection

- **Price data:** Either works — TSETMC returns trading data for both. The post-change ("3") version may have shorter price history (only since the capital change).
- **Shares outstanding:** Use the version's `zTitad`. The base (current) version typically has the most up-to-date data.
- **Market cap:** Price × shares — either works, but the base version's shares count is the total for the company.

## Frequency

From the real data (333 stocks deduped from 566 MarketWatchInit entries):
- ~200 stocks appeared with "3" suffix duplicates
- After dedup, 333 unique base tickers remained
- This means roughly 1 in 3 active TSE stocks has a "3"-suffixed counterpart
