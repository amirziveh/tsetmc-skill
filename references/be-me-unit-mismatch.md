# B/M = 0: Unit Mismatch Between Rahavard365 BE and TSETMC ME

## The Symptom

When computing B/M = BE/ME with mixed data sources, output tables show B/M values of **0.0000** for all portfolios, even though reasonable values would be in the 0.3–1.0 range.

The `bm_proxy` column (BE/TA) looks normal (~0.3–0.8) because both book equity and total assets come from the same accounting source. It's only B/M (BE/ME) that's broken.

## Root Cause

**Unit mismatch between data sources:**

| Metric | Median Value | Unit | Source |
|--------|-------------|------|--------|
| Book Equity (BE) | **608,720** | **millions of Rials** | Rahavard365 (`view_currency_id=1`) |
| Market Cap (ME) | **259,210,028,900** | **Rials** | TSETMC (price × shares) |
| Computed B/M = BE/ME | **0.00000235** | — | → prints as `0.0000` |

Rahavard365 provides the `view_currency_id` parameter:
- `1` = millions of Rials (the default used in all downloads)
- `2` = billions of Rials

When reads BE from one CSV (which stores Rahavard365 values as-is) and ME from another (which stores TSETMC values in Rials), then divides them without converting units, you get this silent data-quality bug.

## Evidence

Computed at formation year 2015 (286 stocks):

| Stat | B/M (uncorrected) |
|------|-------------------|
| Min | 1.64e⁻⁸ |
| 25th | 5.04e⁻⁶ |
| Median | **1.43e⁻⁵** |
| 75th | 3.43e⁻⁵ |
| Max | 2.02e⁻³ |
| Fraction < 0.001 | **99.7%** |

After multiplying BE by 1,000,000 (converting from millions of Rials to Rials):
- Median B/M ≈ 0.014 — still low by US standards but realistic for an emerging market with high inflation and elevated P/E ratios.

## Why Portfolio Sorting Still Works

Portfolio sorting functions typically sort by **rank order** using percentile thresholds (e.g., 30th/70th percentiles), not by absolute B/M magnitude. Since the unit mismatch applies uniformly to all stocks (every BE is in the same unit), the relative ordering is preserved. So:

- **Factor returns → NOT affected** (sorting is correct)
- **B/M values in output tables → WRONG** (need unit conversion)

## The Fix

Convert BE to Rials before dividing by ME:

```python
# BAD: directly divides without unit conversion
bm = be / me

# FIX: convert BE from millions of Rials to Rials
BE_SCALE = 1_000_000  # Rahavard365 view_currency_id=1 = millions of Rials
bm = (be * BE_SCALE) / me if be and me and me > 0 and be > 0 else None
```

### Check your view_currency_id

Verify which currency unit was used when downloading from Rahavard365:

- `view_currency_id=1` → millions of Rials → multiply BE by **1,000,000**
- `view_currency_id=2` → billions of Rials → multiply BE by **1,000,000,000**
- If the API returned raw Rials (unlikely), no conversion needed

## Where to Apply the Fix

This fix applies anywhere B/M is computed from mixed Rahavard365 + TSETMC data. Typical locations:

- **Factor construction code** — where BE/ME is computed for portfolio sorting
- **Summary/descriptive statistics** — where B/M appears in output tables
- **Any function that reads both accounting and market data** and computes the ratio

Apply the same `BE_SCALE` factor wherever BE is combined with TSETMC market data.

## Related: Table A1 Building Block Statistics — All 3 Methods

### The Problem

A Table A1 summary may only loop over one portfolio formation method (e.g., `['2x3']`), producing stats for only that method. A complete table needs statistics for **all three** sorting methods: 2x3, 2x2, and 2x2x2x2.

### The Fix

Extend the loop range to include all three methods:

```python
# BEFORE: only one method
for method in ['2x3']:

# AFTER: all three methods
for method in ['2x3', '2x2', '2x2x2x2']:
```

This requires that factor CSV files for each method (e.g., `factors_2x3.csv`, `factors_2x2.csv`, `factors_2x2x2x2.csv`) all exist with building-block portfolio columns.

### Expected Output

| Method | Portfolios | Description |
|--------|-----------|-------------|
| 2x3 | 18 | HML(6) + RMW(6) + CMA(6) |
| 2x2 | 12 | HML(4) + RMW(4) + CMA(4) |
| 2x2x2x2 | 16 | 4×4 sort by size, B/M, OP, Inv |

### Pitfall: 2x2x2x2 Portfolio Naming

Uses different naming (`P_BHRA`, `P_SHRA`, etc.) without `HML_`/`RMW_`/`CMA_` prefixes. If your code filters columns by prefix, it will miss these portfolios. Read all `P_*` columns to handle this correctly.
