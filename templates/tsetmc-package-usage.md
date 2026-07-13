# tsetmc (5j9) Package Usage Guide

An async+sync Python library for TSETMC with full API coverage, Polars DataFrames, and well-typed responses (⭐31 on GitHub).

## Installation

```bash
pip install tsetmc
```

## Basic Usage (Async)

### Create an Instrument

```python
import asyncio
from tsetmc import Instrument

async def main():
    # By symbol name
    inst = await Instrument.from_search("فولاد")
    print(f"Code: {inst.code}")

    # By insCode directly
    inst2 = Instrument("46348559193224090")

    # Get instrument info
    info = await inst.info()
    print(f"Sector: {info['sector']['lSecVal']}")
    print(f"EPS: {info['eps']['estimatedEPS']}")
    print(f"PE: {info['eps']['sectorPE']}")
    print(f"Total shares: {info['zTitad']}")

asyncio.run(main())
```

### Price History

```python
import asyncio
from tsetmc import Instrument

async def main():
    inst = Instrument("46348559193224090")  # فولاد

    # Daily closing prices (returns Polars LazyFrame)
    df = await inst.daily_closing_price(n=0)  # n=0 = all history
    collected = df.collect()
    print(collected.head(10))
    # Columns: date, priceChange, priceMin, priceMax, priceYesterday,
    #          priceFirst, pClosing, zTotTran, qTotTran5J, qTotCap, ...

    # Get price history (adjusted for capital changes)
    # Returns: date, pmax, pmin, pf, pl, tvol, pc
    adj_df = await inst.price_history(adjusted=True)

asyncio.run(main())
```

### Client Types

```python
import asyncio
from tsetmc import Instrument

async def main():
    inst = Instrument("46348559193224090")

    # Full history as LazyFrame
    ct = await inst.client_type_history()
    print(ct.collect().head())

    # For a specific date
    ct_date = await inst.client_type_history(date=20260713)
    print(f"Natural buy: {ct_date['buy_I_Volume']}")
    print(f"Legal buy: {ct_date['buy_N_Volume']}")

asyncio.run(main())
```

### Shareholders

```python
import asyncio
from tsetmc import Instrument

async def main():
    inst = Instrument("46348559193224090")

    # Current major holders
    holders = await inst.share_holders()
    for h in holders:
        print(f"{h['shareHolderName']}: {h['perOfShares']}% ({h['numberOfShares']:,.0f} shares)")

    # History of a specific holder
    if holders:
        holder_id = holders[0]['shareHolderShareID']
        history = await inst.share_holder_history(holder_id, days=90)
        print(history.collect())

asyncio.run(main())
```

### Live Data

```python
import asyncio
from tsetmc import Instrument

async def main():
    inst = await Instrument.from_search("فولاد")

    # Live price + order book
    live = await inst.live_data(general=True, best_limits=True, market_state=True)
    print(f"Last: {live['pl']}")
    print(f"Close: {live['pc']}")
    print(f"Status: {live['status']}")
    print(f"Best limits: {live['best_limits'].collect()}")

asyncio.run(main())
```

### Identity & Codal

```python
import asyncio
from tsetmc import Instrument

async def main():
    inst = Instrument("46348559193224090")

    # Identity data
    identity = await inst.identity()
    print(f"ISIN: {identity['instrumentID']}")

    # Codal publisher info
    publisher = await inst.publisher()
    print(f"CEO: {publisher['executiveManager']}")
    print(f"Website: {publisher['website']}")

    # Recent Codal filings
    codal = await inst.codal(n=5)
    for c in codal:
        print(f"  {c['title']}")

asyncio.run(main())
```

### Market Overview

```python
import asyncio
from tsetmc.general import market_overview, trade_top, messages
from tsetmc import Flow

async def main():
    # Market overview
    overview = await market_overview(flow=Flow.BOURSE)
    print(f"Index: {overview['indexLastValue']}")
    print(f"State: {overview['marketStateTitle']}")

    # Most visited symbols
    top = await trade_top(category="MostVisited", flow=1, top=10)
    print(top.collect())

    # Recent announcements
    msgs = await messages(flow=0, top=5)
    print(msgs.collect())

asyncio.run(main())
```

### Indices

```python
import asyncio
from tsetmc.indices import Index

async def main():
    # TSE index code
    idx = Index("32097828799138982")

    # Daily history
    history = await idx.history()
    print(history.collect().tail(10))

    # Last day intraday
    last_day = await idx.last_day_history()
    print(last_day.collect())

    # Companies in the index
    companies = await idx.companies()
    print(companies['indexCompany'].collect())

asyncio.run(main())
```

### Funds / ETFs

```python
import asyncio
from tsetmc.funds import funds, FundType

async def main():
    # Stock funds
    stock_funds = await funds(FundType.STOCK)
    print(stock_funds.collect())

    # ETFs
    from tsetmc.funds import etfs, most_traded_etfs
    etf_list = await etfs(top=10)
    print(etf_list.collect())

asyncio.run(main())
```

### Market Watch (Real-time)

```python
import asyncio
from tsetmc.market_watch import market_watch_init

async def main():
    mwi = await market_watch_init(prices=True, best_limits=True, market_state=True)
    print(f"Index: {mwi['market_state']['tse_index']}")
    print(f"Ref ID: {mwi['refid']}")
    print(f"Prices: {mwi['prices'].collect()}")
    print(f"Best limits: {mwi['best_limits'].collect()}")

asyncio.run(main())
```

## Sync API

The `tsetmc` package also has a sync API under `tsetmc.sync`:

```python
from tsetmc.sync import Instrument

inst = Instrument("46348559193224090")
info = inst.info()
print(info['lVal30'])
print(info['eps']['sectorPE'])
```

## Key Features

- **Polars LazyFrames** — efficient, lazy evaluation
- **Full API coverage** — 40+ endpoints, all three surfaces
- **Well-typed** — TypedDicts for every response
- **Sync + Async** — both APIs available
- **Dataset** — built-in symbol lookup table (CSV-based)
- **Market Watch** — real-time pollable market data
- **Indices** — full index history support
- **Funds/ETFs** — dedicated fund data methods
- **Codal integration** — publisher info and filings
- **Price adjustments** — adjusted closing prices for splits/capital increases