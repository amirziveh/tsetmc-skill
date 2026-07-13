# TSETMC (Tehran Stock Exchange) API ecosystem — reverse-engineered

## Key Files

- `references/api-endpoints.md`
- `references/data-schemas.md`
- `references/flow-and-yval-codes.md`
- `references/tsetmc-api-endpoints.md`
- `references/tsetmc-field-dictionary.md`
- `templates/python-client.py`
- `templates/pytse-client-usage.md`
- `templates/tsetmc-package-usage.md`

## Quick Reference

### API Surfaces
- **CDN API (JSON)**: `https://cdn.tsetmc.com/api/` — JSON
- **Old API (CSV)**: `http://old.tsetmc.com/tsev2/data/` — CSV/delimited
- **Service**: `http://service.tsetmc.com/tsev2/data/` — Text

### Key Endpoints
- `GET /Instrument/GetInstrumentSearch/{query}` — Search symbols
- `GET /Instrument/GetInstrumentInfo/{insCode}` — Instrument info
- `GET /ClosingPrice/GetClosingPriceDailyList/{insCode}/{days}` — Price history
- `GET /ClientType/GetClientTypeHistory/{insCode}` — Client types
- `GET /Shareholder/GetInstrumentShareHolderLast/{insCode}` — Shareholders
- `GET /Msg/GetMsgByFlow/{flow}/{top}` — Messages
- `GET /ClosingPrice/GetTradeTop/{category}/{flow}/{top}` — Trade top lists
- `GET /Index/GetIndexB2History/{code}` — Index history
- `GET /Fund/GetFunds/{type}` — Fund list
- `GET /Codal/GetCodalPublisherBySymbol/{symbol}` — Codal publisher

### Notes
- insCode is a 15-20 digit numeric instrument code (not the Persian symbol name)
- Dates use Gregorian YYYYMMDD (field: dEven)
- Times use HHMMSS without leading zeros (field: hEven)
- Some CDN endpoints return empty when market is closed; fall back to old API
- Rate limit: 0.5-1s between calls for batch operations

Read the files in `references/` for full documentation before writing API calls.
