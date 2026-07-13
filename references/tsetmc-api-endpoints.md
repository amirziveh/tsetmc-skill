# TSETMC API Endpoints — Complete Catalog

## 1. 🆕 CDN REST API (`https://cdn.tsetmc.com/api/`)

Modern JSON REST API. Response format: each endpoint wraps data in a single-key object.

### Instrument

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `Instrument/GetInstrumentSearch/{query}` | GET | `query`: Persian/English name | `{"instrumentSearch": [...]}` | ✅ Working |
| `Instrument/GetInstrumentInfo/{insCode}` | GET | `insCode`: 15-20 digit code | `{"instrumentInfo": {...}}` | ✅ Working |
| `Instrument/GetInstrumentIdentity/{insCode}` | GET | `insCode` | `{"instrumentIdentity": {...}}` | ⚠️ Sometimes empty |
| `Instrument/GetInstrumentHistory/{insCode}/{date}` | GET | `date`: YYYYMMDD | `{"instrumentHistory": {...}}` | ⚠️ Often empty |

### Closing Price

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `ClosingPrice/GetClosingPriceDailyList/{insCode}/{n}` | GET | `n`: number of days (0=all) | `{"closingPriceDaily": [...]}` | ⚠️ Often empty |
| `ClosingPrice/GetClosingPriceInfo/{insCode}` | GET | `insCode` | `{"closingPriceInfo": {...}}` | ✅ Working |
| `ClosingPrice/GetClosingPriceDaily/{insCode}/{date}` | GET | `date`: YYYYMMDD | `{"closingPriceDaily": {...}}` | ✅ Working |
| `ClosingPrice/GetClosingPriceHistory/{insCode}/{date}` | GET | date, intraday | `{"closingPriceHistory": [...]}` | ⚠️ Often empty |
| `ClosingPrice/GetTradeTop/{category}/{flow}/{top}` | GET | category, flow, top count | `{"tradeTop": [...]}` | ✅ Working |
| `ClosingPrice/GetMarketMap?market=0&size=N&sector=0&typeSelected=1&hEven=0` | GET | Query params | `[...]` | ⚠️ Empty |
| `ClosingPrice/GetPriceAdjustList/{insCode}` | GET | insCode | `{"priceAdjust": [...]}` | ⚠️ Empty |
| `ClosingPrice/GetMarketWatch?...` | GET | Query params | `{"marketwatch": [...]}` | ✅ Working |
| `ClosingPrice/GetRelatedCompany/{cs}` | GET | cs (sector code) | `{"relatedCompany": [...]}` | ✅ Working |

### Market Data

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `MarketData/GetMarketOverview/{flow}` | GET | flow (1=TSE, 2=OTC) | `{"marketOverview": {...}}` | ⚠️ Empty |
| `MarketData/GetSectorsSummary` | GET | none | `{"sectorSummeries": [...]}` | ⚠️ Empty |
| `MarketData/GetInstValueAllInstAllParam` | GET | none | `{"instValueAllInstAllParam": [...]}` | ✅ Working |
| `MarketData/GetInstrumentState/{insCode}/{date}` | GET | insCode, date | `{"instrumentState": [...]}` | ✅ Working |

### Trade

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `Trade/GetTrade/{insCode}` | GET | insCode | `{"trade": [...]}` | ⚠️ Often empty |
| `Trade/GetTradeHistory/{insCode}/{date}/true` | GET | insCode, date | `{"tradeHistory": [...]}` | ✅ Working |

### Client Type (حقیقی-حقوقی)

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `ClientType/GetClientType/{insCode}/1/0` | GET | insCode | `{"clientType": {...}}` | ✅ Working |
| `ClientType/GetClientTypeHistory/{insCode}` | GET | insCode | `{"clientType": [...]}` | ✅ Working |
| `ClientType/GetClientTypeHistory/{insCode}/{date}` | GET | insCode, date | `{"clientType": {...}}` | ✅ Working |
| `ClientType/GetClientTypeAll` | GET | none | `{"clientTypeAllDto": [...]}` | ✅ Working |

### Best Limits (Order Book)

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `BestLimits/{insCode}` | GET | insCode | `{"bestLimits": [...]}` | ✅ Working (empty outside hours) |
| `BestLimits/{insCode}/{date}` | GET | insCode, date | `{"bestLimitsHistory": [...]}` | ✅ Working |

### Shareholder

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `Shareholder/GetInstrumentShareHolderLast/{insCode}` | GET | insCode | `{"shareHolder": [...]}` | ✅ Working |
| `Shareholder/{insCode}/{date}` | GET | insCode, date | `{"shareShareholder": [...]}` | ✅ Working |
| `Shareholder/GetShareHolderHistory/{insCode}/{shareHolderID}/{days}` | GET | 3 params | `{"shareHolder": [...]}` | ✅ Working |
| `Shareholder/GetShareHolderCompanyList/{shareHolderShareID}` | GET | shareHolderShareID | `{"shareHolderShare": [...]}` | ✅ Working |

### Index

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `Index/GetIndexB1LastAll/All/{i}` | GET | i (1=all) | `{"indexB1": [...]}` | ⚠️ Empty |
| `Index/GetIndexB1LastDay/{code}` | GET | code | `{"indexB1": [...]}` | ✅ Working |
| `Index/GetIndexB2History/{code}` | GET | code | `{"indexB2": [...]}` | ✅ Working |

### Fund

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `Fund/GetFunds/{type}` | GET | type (4,5,6,7,11,12,13,14,16,17) | `{"funds": [...]}` | ✅ Working |
| `Fund/GetFundInDetail/{regNo}` | GET | regNo | `{"fund": {...}}` | ✅ Working |
| `Fund/GetETFByInsCode/{insCode}` | GET | insCode | `{"etf": {...}}` | ✅ Working |

### Message

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `Msg/GetMsgByFlow/{flow}/{top}` | GET | flow, top count | `{"msg": [...]}` | ✅ Working |
| `Msg/GetMsgByDevenAndLVal18AFC/{date}/{term}` | GET | date (SH YYYY-mm-dd), term | `{"msg": [...]}` | ✅ Working |
| `Msg/GetMsgByInsCode/{insCode}` | GET | insCode | `{"msg": [...]}` | ✅ Working |

### Codal

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `Codal/GetCodalPublisherBySymbol/{symbol}` | GET | symbol (Persian) | `{"codalPublisher": {...}}` | ✅ Working |
| `Codal/GetPreparedDataByInsCode/{n}/{insCode}` | GET | n=number of items | `{"preparedData": [...]}` | ✅ Working |

### Market Watch (experimental)

| Endpoint | Method | Params | Returns | Status |
|----------|--------|--------|---------|--------|
| `ClosingPrice/GetMarketWatch?market=0&industrialGroup=&paperTypes[]=1...8&showTraded=false&withBestLimits=true&hEven=0&RefID=0` | GET | Complex query params | `{"marketwatch": [...]}` | ✅ Working |

---

## 2. 🏚 Old TSEv2 CSV API (`http://old.tsetmc.com/tsev2/data/`)

CSV/semicolon-delimited text responses. Semicolon (`;`) = row separator, comma (`,`) = field separator.

| Endpoint | Params | Response Format | Status |
|----------|--------|----------------|--------|
| `MarketWatchInit.aspx?h=0&r=0` | none | `msg@market_state@price_rows@best_limits@refid` — 5 parts separated by `@` | ✅ |
| `MarketWatchPlus.aspx?h=N&r=N` | heven, refid | Same format, incremental updates | ✅ |
| `instinfofast.aspx?i={insCode}&c={cs}&e=1` | insCode, cs, e | 9 parts separated by `;` | ✅ |
| `instinfodata.aspx?i={insCode}&c=&e=1` | insCode | Same as instinfofast | ✅ |
| `InstTradeHistory.aspx?i={insCode}&Top=N&A=0|1` | insCode, top, all | CSV: `date,pmax,pmin,pc,pl,pf,py,tval,tvol,tno;` | ✅ |
| `clienttype.aspx?i={insCode}` | insCode | CSV: `date,n_buy_count,l_buy_count,...;` | ✅ |
| `ClientTypeAll.aspx` | none | CSV: `ins_code,n_buy_count,l_buy_count,...;` | ✅ |
| `ClosingPriceAll.aspx` | none | CSV with ID-prefixed rows | ✅ |
| `InstValue.aspx?t=a` | none | CSV: `ins_code,key,value;` | ✅ |
| `search.aspx?skey={query}` | query | CSV: `l18,l30,ins_code,retail,compensation,wholesale,...;` | ✅ |
| `TradeDetail.aspx?i={insCode}` | insCode | Trade detail CSV | ✅ |
| `ShareHolder.aspx?i={id_cisin}` | id_cisin | `history#other_holdings` | ✅ |
| `Export-txt.aspx?t=i&a=1&b=0&i={insCode}` | insCode | TXT export | ✅ |
| `Export-txt.aspx?a=InsTrade&InsCode={insCode}&DateFrom=...&DateTo=...&b=0` | multi | CSV with headers | ✅ |
| `DPSData.aspx?s={symbol}` | symbol (Arabic) | CSV: `publish_date@meeting_date@...;` | ✅ |

### MarketWatchInit Response Format

The response is split by `@` into 5 parts:

```
part1@part2@part3@part4@part5
```

**Part 1 — Handle Messages**: Comma-separated notification IDs (`NewMsgNotification,NewInsStateNotification,NewCodalNotification`)

**Part 2 — Market State**: 16-17 comma-separated values:
```
datetime,tse_status,tse_index,tse_index_change,tse_value,tse_tvol,tse_tval,tse_tno,fb_status,fb_tvol,fb_tval,fb_tno,derivatives_status,derivatives_tvol,derivatives_tval,derivatives_tno,[extra]
```
- `datetime`: Jalali date/time in `MM/DD/YYYY HH:MM:SS` format
- `tse_status`: بازار بسته / بازار باز / ...
- `tse_index_change`: format like `(88883.33) 1.76%` or empty string before market open

**Part 3 — Price Rows**: Semicolon-separated, each row has 26 or 23 comma-separated fields:
```
ins_code, isin, l18, l30, heven, pf, pc, pl, tno, tvol, tval, pmin, pmax, py, eps, bvol, visitcount, flow, cs, tmax, tmin, z, yval, [predtran, buyop, cgrvalcot]
```
- 23 columns for some instruments, 26 for others (extra: predtran, buyop, cgrvalcot)
- 10-column entries are price updates (only: ins_code, heven, pf, pc, pl, tno, tvol, tval, pmin, pmax)

**Part 4 — Best Limits**: Semicolon-separated rows:
```
ins_code,number,zo,zd,pd,po,qd,qo
```
- `number`: limit level (1-5 for buy/sell)
- `zd`: demand volume (حجم تقاضا), `qd`: demand quantity (تعداد تقاضا), `pd`: demand price (قیمت تقاضا)
- `zo`: supply volume (حجم عرضه), `qo`: supply quantity (تعداد عرضه), `po`: supply price (قیمت عرضه)

**Part 5 — Reference ID**: Integer, used for polling increments (25s intervals)

### instinfofast/instinfodata Response Format

9 parts separated by `;`:

```
price_info;index_info;orders_info;_;_;_;_;_;_
```

**Price Info** (16-17 comma-separated fields):
```
time,status,pl,pc,pf,py,pmin,pmax,tno,tvol,tval,_,info_date,info_time,nav_date,nav
```
- `time`: HHMMSS format
- `status`: وضعیت نماد
- `pl`: آخرین قیمت (last price)
- `pc`: قیمت پایانی (closing price)
- `pf`: اولین قیمت (first price/open)
- `py`: قیمت دیروز (yesterday's close)
- `pmin/pmax`: min/max price today
- `tno`: تعداد معاملات (number of trades)
- `tvol`: حجم معاملات (volume)
- `tval`: ارزش معاملات (value)
- `nav`: خالص ارزش دارایی (NAV for ETFs, empty for stocks)

**Orders Info**: 6 comma-separated fields per level, separated by `@`:
```
zd,qd,pd,po,qo,zo@next_level...
```

---

## 3. 📄 ParTree HTML Pages (`http://old.tsetmc.com/Loader.aspx?ParTree=...`)

ASP.NET WebForms pages with data embedded in JavaScript variables. These are HTML pages that the client-side JS parses.

| ParTree | Description | Key Variables |
|---------|-------------|---------------|
| `151311&i={insCode}` | Instrument main page | `TopInst`, `LVal18AFC`, `DEven`, `LSecVal`, `CgrValCot`, `Flow`, `InstrumentID`, `InsCode`, `BaseVol`, `EstimatedEPS`, `ZTitad`, `CIsin`, `CSecVal`, `PdrCotVal`, `PClosing`, `PSGelStaMax`, `PSGelStaMin`, `Title`, `FaraDesc`, `MinWeek`, `MaxWeek`, `MinYear`, `MaxYear`, `QTotTran5JAvg`, `SectorPE`, `KAjCapValCpsIdx`, `PriceMin`, `PriceMax`, `PriceYesterday`, `ThemeCount`, `ContractSize`, `NAV`, `PSR`, `TradeHistory`, `RelatedCompanies` |
| `15131J&i={insCode}` | Financial index intraday | — |
| `15131M&i={insCode}` | Identification tab | HTML table of instrument identity |
| `15131V&s={symbol}` | Introduction tab | HTML table of company intro |
| `15131T&c={cisin}` | Shareholders tab | HTML table of major holders |
| `15131I` | Major holders activity | HTML table |
| `15131O` | Top industry groups | HTML table |
| `15131G&i={insCode}` | Price adjustments | HTML table |
| `15131W&i={insCode}` | Ombud messages | HTML table |
| `15131L&top=N` | Status changes | HTML table |
| `111C1417` | All symbols list | HTML table of all symbols |
| `111C1913` | Board codes (members) | HTML table |
| `111C1213` | Industry group codes (members) | HTML table |
| `111C1214` | Industrial groups overview (members) | HTML table |
| `151319&Flow=N` | Price adjustments list | HTML table |

### ParTree Variable Extraction (Regex)

For the instrument main page (`151311`), the key variables are embedded in JavaScript. The following regex extracts them all:

```python
import re

pattern = re.compile(
    "TopInst='(?P<TopInst>[^,]*)',"
    "LVal18AFC='[^,]*',"
    "DEven='(?P<DEven>[^,]*)',"
    "LSecVal='(?P<LSecVal>[^,]*)',"
    "CgrValCot='(?P<CgrValCot>[^,]*)',"
    "Flow='(?P<Flow>[^,]*)',"
    "InstrumentID='(?P<InstrumentID>[^,]*)',"
    "InsCode='(?P<InsCode>[^,]*)',"
    'BaseVol=(?P<BaseVol>[^,]*),'
    "EstimatedEPS='(?P<EstimatedEPS>[^,]*)',"
    'ZTitad=(?P<ZTitad>[^,]*),'
    "CIsin='(?P<CIsin>[^,]*)',"
    "LVal18AFC='(?P<LVal18AFC>[^,]*)',"
    "CSecVal='(?P<CSecVal>[^,]*)',"
    "PdrCotVal='(?P<PdrCotVal>[^,]*)',"
    "PClosing='(?P<PClosing>[^,]*)',"
    "PSGelStaMax='(?P<PSGelStaMax>[^,]*)',"
    "PSGelStaMin='(?P<PSGelStaMin>[^,]*)',"
    "Title='(?P<Title>[^,]*)',"
    "FaraDesc ='(?P<FaraDesc>[^,]*)',"
    "MinWeek='(?P<MinWeek>[^,]*)',"
    "MaxWeek='(?P<MaxWeek>[^,]*)',"
    "MinYear='(?P<MinYear>[^,]*)',"
    "MaxYear='(?P<MaxYear>[^,]*)',"
    "QTotTran5JAvg='(?P<QTotTran5JAvg>[^,]*)',"
    "SectorPE='(?P<SectorPE>[^,]*)',"
    "KAjCapValCpsIdx='(?P<KAjCapValCpsIdx>[^,]*)',"
    'PriceMin=(?P<PriceMin>[^,]*),'
    'PriceMax=(?P<PriceMax>[^,]*),'
    'PriceYesterday=(?P<PriceYesterday>[^;]*);'
    "ThemeCount='(?P<ThemeCount>[^;]*)';"
    "ContractSize='(?P<ContractSize>[^;]*)';"
    "NAV='(?P<NAV>[^;]*)';"
    "PSR='(?P<PSR>[^;]*)';"
)
```

---

## 4. 📈 Members Chart API (`https://members.tsetmc.com/tsev2/chart/data/`)

| Endpoint | Params | Response | Status |
|----------|--------|----------|--------|
| `Financial.aspx?i={insCode}&t=ph&a=0` | insCode, t=ph, a=0/1 | CSV: `date,pmax,pmin,pf,pl,tvol,pc;` (unadjusted) | ✅ |
| `Financial.aspx?i={insCode}&t=ph&a=1` | insCode, t=ph, a=1 | Same format (adjusted for dividends) | ✅ |
| `IndexFinancial.aspx?i={idxCode}&t=ph` | idxCode, t=ph | Index financial data | ✅ |

---

## 5. Simple Service Endpoint (`http://service.tsetmc.com/tsev2/data/`)

| Endpoint | Params | Response | Status |
|----------|--------|----------|--------|
| `TseClient2.aspx?t=LastPossibleDeven` | t=LastPossibleDeven | `YYYYMMDD;YYYYMMDD` | ✅ |

---

## Domain Summary

| Domain | Purpose | Protocol |
|--------|---------|----------|
| `https://cdn.tsetmc.com/api/` | Modern REST API (JSON) | HTTPS |
| `http://old.tsetmc.com/tsev2/data/` | Old data handlers (CSV) | HTTP |
| `http://old.tsetmc.com/Loader.aspx` | HTML pages (ParTree) | HTTP |
| `https://members.tsetmc.com/tsev2/chart/data/` | Chart data (CSV) | HTTPS |
| `http://service.tsetmc.com/tsev2/data/` | Simple service endpoints | HTTP |
| `https://www.tsetmc.com/` | Main SPA website | HTTPS |