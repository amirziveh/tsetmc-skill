# pytse-client Usage Guide

A popular async Python library for TSETMC data (⭐304 on GitHub).

## Installation

```bash
pip install pytse-client
```

## Basic Usage

### Search & Get a Ticker

```python
import asyncio
from pytse_client import Ticker

async def get_data():
    ticker = Ticker("فولاد")

    # Get instrument info
    info = await ticker.get_ticker_info()
    print(f"Name: {info['name']}")
    print(f"Symbol: {info['symbol']}")

    # Get price history as DataFrame
    history = await ticker.get_ticker_history()
    print(history.head())
    # Columns: date, open, high, low, close, volume

    # Get client types (حقیقی-حقوقی)
    client_types = await ticker.get_client_types()
    print(client_types.head())

asyncio.run(get_data())
```

### Download All Data

```python
from pytse_client import download_all

download_all(write_to_csv=True, base_path="./stock_data")
```

## Key Features

- **Async/await** — fast parallel downloads
- **Pandas DataFrames** — easy analysis
- **Symbol → Ticker resolution** — automatic insCode lookup
- **Client types** — natural vs legal person data
- **Shareholders** — major shareholder history
- **CSV export** — save data to files