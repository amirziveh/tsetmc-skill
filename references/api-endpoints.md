# TSETMC API Endpoint Catalog

All endpoints across all three API surfaces. Grouped by category.

---

## 🆕 CDN REST API — `https://cdn.tsetmc.com/api/`

JSON responses wrapped in a key matching the endpoint name (e.g. `{"instrumentInfo": {...}}`).

### Instrument

#### `GET /Instrument/GetInstrumentSearch/{query}`
Search for instruments by Persian or English name.

**Params**: `query` (URL-encoded Persian text, e.g. `%D9%81%D9%88%D9%84%D8%A7%D8%AF` for فولاد)

**Response key**: `instrumentSearch`

**Schema**: `list[Search]`
```json
[{
  "insCode2": "61934586397353104",
  "insCode3": "53809308236531169",
  "insCode4": "61318276340211749",
  "insCode": "46348559193224090",
  "lVal30": "فولاد مباركه اصفهان",
  "lVal18AFC": "فولاد",
  "flow": 1,
  "cIsin": null,
  "zTitad": 0.0,
  "baseVol": 0,
  "instrumentID": null,
  "cgrValCot": "N1",
  "cComVal": null,
  "lastDate": 1,
  "sourceID": 1,
  "flowTitle": "بازار بورس",
  "cgrValCotTitle": ""
}]
```
Note: `insCode2`, `insCode3`, `insCode4` may be old/related codes. The primary one is `insCode`.

#### `GET /Instrument/GetInstrumentInfo/{insCode}`
Full instrument info: EPS, sector, thresholds, ISIN, total shares, base volume, etc.

**Response key**: `instrumentInfo`

**Schema**: `InstrumentInfo` - See `data-schemas.md`

#### `GET /Instrument/GetInstrumentIdentity/{insCode}`
Identity data: sector, sub-sector, full names.

**Response key**: `instrumentIdentity`

**Schema**: `Identity` - See `data-schemas.md`

#### `GET /Instrument/GetInstrumentHistory/{insCode}/{date}`
Instrument history for a specific date. Returns only when market was open.

**Params**: `date` = Gregorian YYYYMMDD

**Response key**: `instrumentHistory`

**Schema**: `{zTitad: float, baseVol: int}`

### Closing Price

#### `GET /ClosingPrice/GetClosingPriceDailyList/{insCode}/{n}`
Daily closing price history. **Note: May return empty for many instruments.**

**Params**: `n` = number of days (0 = all)

**Response key**: `closingPriceDaily`

**Schema**: `list[ClosingPrice]`

| Field | Type | Meaning |
|-------|------|---------|
| dEven | int | Date (YYYYMMDD) |
| hEven | int | Time (HHMMSS) |
| pClosing | float | Closing price |
| priceChange | float | Change from yesterday |
| priceMin | float | Day low |
| priceMax | float | Day high |
| priceYesterday | float | Previous close |
| priceFirst | float | Opening price |
| pDrCotVal | float | Last traded price |
| zTotTran | float | Total trades count |
| qTotTran5J | float | 5-day avg volume |
| qTotCap | float | Market cap |
| iClose | bool | Closed? |
| yClose | bool | Yesterday closed? |

#### `GET /ClosingPrice/GetClosingPriceInfo/{insCode}`
Current closing price info snapshot.

**Response key**: `closingPriceInfo`

#### `GET /ClosingPrice/GetClosingPriceDaily/{insCode}/{date}`
Closing price for a specific day.

**Response key**: `closingPriceDaily`

#### `GET /ClosingPrice/GetClosingPriceHistory/{insCode}/{date}`
Intraday closing price history for a specific date.

**Response key**: `closingPriceHistory`

#### `GET /ClosingPrice/GetTradeTop/{category}/{flow}/{top}`
Trade top lists.

**Params**:
- `category`: `MostVisited` | `ETF` | `MostTradedETF` | `PClosingTopETF` | `PClosingBtmETF` | `CommodityFund`
- `flow`: 0 | 1 | 2 | ... (see flow codes)
- `top`: max results (default 9999)

**Response key**: `tradeTop`

**Schema**: `list[ClosingPriceInfo]` — each item has an `instrument` sub-object embedded.

#### `GET /ClosingPrice/GetMarketMap?market=0&size=9999&sector=0&typeSelected=1&hEven=0`
Market map (treemap) data. **May return empty.**

**Response key**: (array directly)

#### `GET /ClosingPrice/GetPriceAdjustList/{insCode}`
Price adjustment history (splits, capital increases).

**Response key**: `priceAdjust`

#### `GET /ClosingPrice/GetMarketWatch?...`
Experimental new market watch API. Replaces MarketWatchInit.

Params: `market=0`, `industrialGroup=`, `paperTypes[0]=1&...&paperTypes[8]=9`, `showTraded`, `withBestLimits`, `hEven`, `RefID`

**Response key**: `marketwatch`

#### `GET /ClosingPrice/GetRelatedCompany/{cs}`
Related companies in the same industry group (cs = sector code).

**Response key**: `{relatedCompany: [...], relatedCompanyThirtyDayHistory: [...]}`

### Market Data

#### `GET /MarketData/GetMarketOverview/{flow}`
Market overview. **Note: May return empty.**

**Response key**: `marketOverview`

#### `GET /MarketData/GetSectorsSummary`
Industry sector summaries. **May return empty.**

**Response key**: `sectorSummeries`

#### `GET /MarketData/GetInstValueAllInstAllParam`
All instrument values (experimental new API).

**Response key**: `instValueAllInstAllParam`

#### `GET /MarketData/GetInstrumentState/{insCode}/{date}`
Intraday instrument status history.

**Response key**: `instrumentState`

### Trade

#### `GET /Trade/GetTrade/{insCode}`
Current day's trades list. **May return empty outside hours.**

**Response key**: `trade`

#### `GET /Trade/GetTradeHistory/{insCode}/{date}/true`
Historical trades for a specific day. The `true` parameter may control detail level.

**Response key**: `tradeHistory`

### Client Type (حقیقی-حقوقی)

#### `GET /ClientType/GetClientType/{insCode}/1/0`
Current day's client type snapshot.

**Response key**: `clientType`

**Schema**: `ClientType` - See data-schemas.md.
Returns zeros outside trading hours.

#### `GET /ClientType/GetClientTypeHistory/{insCode}`
Full client type history for an instrument.

**Response key**: `clientType`

**Schema**: `list[ClientTypeOnDate]` - See data-schemas.md.

#### `GET /ClientType/GetClientTypeHistory/{insCode}/{date}`
Client type data for a specific date.

**Response key**: `clientType` (single dict)

#### `GET /ClientType/GetClientTypeAll`
All instruments' client type data (experimental).

**Response key**: `clientTypeAllDto`

### Best Limits (Order Book)

#### `GET /BestLimits/{insCode}`
Current best buy/sell limits (order book). Empty outside trading hours.

**Response key**: `bestLimits`

**Schema**: `[{zd, qd, pd, po, qo, zo}]`
- zd/zo: demand/offer count
- qd/qo: demand/offer volume
- pd/po: demand/offer price

#### `GET /BestLimits/{insCode}/{date}`
Historical best limits for a specific day.

**Response key**: `bestLimitsHistory`

### Shareholder

#### `GET /Shareholder/GetInstrumentShareHolderLast/{insCode}`
Current major shareholders.

**Response key**: `shareHolder`

**Schema**: `list[ShareHolder]`
```json
[{
  "shareHolderID": 0,
  "shareHolderName": "سازمان توسعه ونوسازي معادن وصنايع معدني ايران",
  "cIsin": "IRO1FOLD0009",
  "dEven": 0,
  "numberOfShares": 323334093547.0,
  "perOfShares": 16.709,
  "change": 1,
  "changeAmount": 0.0,
  "shareHolderShareID": 83535
}]
```

#### `GET /Shareholder/{insCode}/{date}`
Shareholders on a specific date.

**Response key**: `shareShareholder`

#### `GET /Shareholder/GetShareHolderHistory/{insCode}/{shareHolderID}/{days}`
Share change history for a specific holder.

**Response key**: `shareHolder`

#### `GET /Shareholder/GetShareHolderCompanyList/{shareHolderShareID}`
All companies held by a specific shareholder.

**Response key**: `shareHolderShare`

### Index

#### `GET /Index/GetIndexB1LastAll/All/{i}`
Latest index values. **May return empty.**

**Response key**: `indexB1`

#### `GET /Index/GetIndexB1LastDay/{code}`
Intraday index ticks for the last trading day.

**Response key**: `indexB1`

#### `GET /Index/GetIndexB2History/{code}`
Daily index history.

**Response key**: `indexB2`

### Fund / ETF

#### `GET /Fund/GetFunds/{type}`
Fund list by type. Types: `4`=Fixed Income, `5`=Commodity, `6`=Stock, `7`=Mixed, `11`=Market Making, `12`=VC, `13`=Project, `14`=REIT, `16`=Private, `17`=Fund

**Response key**: `funds`

#### `GET /Fund/GetFundInDetail/{regNo}`
Detailed fund info with NAV history.

**Response key**: `fund`

#### `GET /Fund/GetETFByInsCode/{insCode}`
ETF redemption NAV data.

**Response key**: `etf`
```json
{
  "insCode": "...",
  "deven": 20260713,
  "hEven": 172700,
  "pRedTran": 100000.0,   // redemption price
  "pSubTran": 100000.0,   // subscription price
  "iClose": 100000
}
```

### Message / Announcements

#### `GET /Msg/GetMsgByFlow/{flow}/{top}`
Market announcements (TSETMC messages).

**Response key**: `msg`

**Schema**: `list[Message]`
```json
[{
  "tseMsgIdn": 268111,
  "dEven": 20260713,
  "hEven": 172724,
  "tseTitle": "عدم تاييد بخشي از معاملات در برخي از نمادهاي معاملاتي",
  "tseDesc": "به اطلاع مي‌رساند...",
  "flow": 0
}]
```

#### `GET /Msg/GetMsgByDevenAndLVal18AFC/{date}/{term}`
Search messages by date and keyword.

**Response key**: `msg`

#### `GET /Msg/GetMsgByInsCode/{insCode}`
Messages specific to an instrument.

**Response key**: `msg`

### Codal

#### `GET /Codal/GetCodalPublisherBySymbol/{symbol}`
Company publisher info from Codal system.

**Response key**: `codalPublisher`

#### `GET /Codal/GetPreparedDataByInsCode/{n}/{insCode}`
Codal filings and reports.

**Response key**: `preparedData`

---

## 🏚 Old TSEv2 CSV API — `http://old.tsetmc.com/tsev2/data/`

All responses are delimited text. Default: semicolon (`;`) row separator, comma (`,`) field separator.

### `GET /tsev2/data/MarketWatchInit.aspx?h=0&r=0`
Full market snapshot. **Most comprehensive real-time endpoint.**

Response is split by `@` into 5 parts:
1. **Handle/Messages**: comma-separated notification IDs
2. **Market State**: comma-separated — `datetime, tse_status, tse_index, tse_index_change, tse_value, tse_tvol, tse_tval, tse_tno, fb_status, fb_tvol, fb_tval, fb_tno, derivatives_status, derivatives_tvol, derivatives_tval, derivatives_tno`
3. **Price Rows**: semicolon-separated. Each row has 26 comma-separated columns:
   `ins_code, isin, l18, l30, heven, pf, pc, pl, tno, tvol, tval, pmin, pmax, py, eps, bvol, visitcount, flow, cs, tmax, tmin, z, yval, predtran, buyop, cgrvalcot`
4. **Best Limits**: semicolon-separated. `ins_code, number, zo, zd, pd, po, qd, qo`
5. **refid**: integer for polling

### `GET /tsev2/data/MarketWatchPlus.aspx?h={heven}&r={refid}`
Poll for market updates. Use `heven` and `refid` from the previous response.
- `h`: rounded to nearest 5 (e.g. `5 * (heven // 5)`)
- `r`: rounded to nearest 25

Response has same structure as MarketWatchInit but only returns delta (changed/new items).

### `GET /tsev2/data/search.aspx?skey={query}`
Search instruments by Persian name.

Response: semicolon-separated, 11 columns:
`l18, l30, ins_code, retail, compensation, wholesale, _unknown1, _unknown2, _unknown3, _unknown4, _unknown5`
Where `_unknown1` through `_unknown5` are trade type codes.

### `GET /tsev2/data/instinfofast.aspx?i={insCode}&c={cs}&e=1`
Live instrument info (same as `instinfodata.aspx`).

Response is semicolon-separated into 9 sections. First section (price info) is comma-separated:
`time, status, pl, pc, pf, py, pmin, pmax, tno, tvol, tval, _, info_datetime_date, last_info_time, nav_datetime, nav`

### `GET /tsev2/data/instinfodata.aspx?i={insCode}&c=&e=1`
Same as `instinfofast.aspx`. Use `&e=1` for ETF NAV data.

### `GET /tsev2/data/InstTradeHistory.aspx?i={insCode}&Top={N}&A={0|1}`
Historical price data. `Top` = max rows, `A` = include empty days (0=no, 1=yes).

Response: CSV-like, columns separated by `@`, rows by `;`:
`date, pmax, pmin, pc, pl, pf, py, tval, tvol, tno`

### `GET /tsev2/data/clienttype.aspx?i={insCode}`
Client type history for an instrument.

Response: CSV with columns:
`date, n_buy_count, l_buy_count, n_sell_count, l_sell_count, n_buy_volume, l_buy_volume, n_sell_volume, l_sell_volume, n_buy_value, l_buy_value, n_sell_value, l_sell_value`

### `GET /tsev2/data/ClientTypeAll.aspx`
All instruments' client type data.

Columns: `ins_code, n_buy_count, l_buy_count, n_buy_volume, l_buy_volume, n_sell_count, l_sell_count, n_sell_volume, l_sell_volume`

### `GET /tsev2/data/ClosingPriceAll.aspx`
All instruments' latest closing price data.

Response format: semicolon-separated rows. First column is instrument code (repeated for multi-row instruments). Columns: `ins_code, n, pc, pl, tno, tvol, tval, pmin, pmax, py, pf`

### `GET /tsev2/data/InstValue.aspx?t=a`
Key statistics for all instruments.

Response: semicolon-separated. `ins_code, n, value` where `n` is the stat type ID.

### `GET /tsev2/data/TradeDetail.aspx?i={insCode}`
Today's trade details.

### `GET /tsev2/data/ShareHolder.aspx?i={id_cisin}`
Shareholder history and other holdings. Response contains `#` separator: history on left, other holdings on right.

### `GET /tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i={insCode}`
Export instrument data as text.

### `GET /tsev2/data/DPSData.aspx?s={symbol}`
DPS (Dividend Per Share) history. Columns: `publish_date, meeting_date, fiscal_year, profit_or_loss_after_tax, distributable_profit, accumulated_profit_at_the_end_of_the_period, cash_earnings_per_share`

---

## 📄 ParTree HTML — `http://old.tsetmc.com/Loader.aspx?ParTree=`

### Instrument Pages

| ParTree | Description |
|---------|-------------|
| `151311&i={insCode}` | Main instrument page — all data in JS variables |
| `15131M&i={insCode}` | Identification tab (شناسه) |
| `15131V&s={symbol}` | Introduction tab (معرفی) |
| `15131T&c={cisin}` | Shareholders tab |
| `15131J&i={insCode}` | Financial index intraday |
| `15131G&i={insCode}` | Price adjustments |
| `15131W&i={insCode}` | Ombud messages |
| `15131L&top={N}` | Status changes |
| `15131I` | Major holders activity |
| `15131O` | Top industry groups |
| `151319&Flow={N}` | Price adjustments list |
| `15131F` | Filters page |

### Reference Data

| ParTree | Description |
|---------|-------------|
| `111C1417` | All symbols list (HTML table) |
| `111C1913` | Board codes (members page) |
| `111C1213` | Industry group codes |
| `111C1214` | Industrial groups overview |

---

## 📈 Members Chart API — `https://members.tsetmc.com/tsev2/chart/data/`

### `GET /tsev2/chart/data/Financial.aspx?i={insCode}&t=ph&a={0|1}`
Price history for charts. `a` = adjusted (1) or unadjusted (0).

Response: semicolon-separated CSV. Columns: `date, pmax, pmin, pf, pl, tvol, pc`

### `GET /tsev2/chart/data/IndexFinancial.aspx?i={idxCode}&t=ph`
Index financial data for charts.

---

## 🛠 Service — `http://service.tsetmc.com/tsev2/data/`

### `GET /tsev2/data/TseClient2.aspx?t=LastPossibleDeven`
Last trading day. Returns: `{date};{date}` (e.g. `20260712;20260712`)