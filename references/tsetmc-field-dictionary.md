# TSETMC Field Dictionary

> Meanings of common fields in TSETMC API responses across all three API surfaces.

## Instrument Fields

### Core Identification

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `insCode` | کد instrument | Instrument Code | 15-20 digit numeric — primary key for all API calls |
| `cIsin` | کد ISIN | ISIN Code | e.g. `IRO1FOLD0009` (12 chars) |
| `instrumentID` | شناسه instrument | Instrument ID | e.g. `IRO1FOLD0001` — often same as ISIN |
| `lVal30` | نام 30 حرفی | Name (30 chars) | Full Persian name e.g. `فولاد مباركه اصفهان` |
| `lVal18AFC` | نماد 18 حرفی | Symbol (18 chars) | Ticker symbol e.g. `فولاد` |
| `lVal18` | نام لاتین | Latin Name | English name e.g. `S*Mobarakeh Steel` |
| `cValMne` | — | — | Usually null |

### Market Info

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `flow` | جریان / بازار | Flow/Market | 0=General, 1=Bourse, 2=FaraBourse, 4=Payeh, 18=ETF, etc. |
| `flowTitle` | عنوان بازار | Market Title | e.g. `بازار بورس` |
| `cgrValCot` | کد گروه | Group Code | e.g. `N1` |
| `cgrValCotTitle` | عنوان گروه | Group Title | e.g. `بازار اول (تابلوی اصلی) بورس` |
| `cComVal` | کد شرکت | Company Code | e.g. `1` |
| `sourceID` | منبع | Source ID | 0 or 1 |
| `lastDate` | آخرین تاریخ | Last Date | 0 or a date |

### Trading Info

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `dEven` | تاریخ روز | Date | Gregorian date as integer: `YYYYMMDD` (e.g. `20260713`) |
| `hEven` | ساعت | Time | As integer: `HHMMSS` (e.g. `93000` = 09:30:00) |
| `zTitad` | تعداد سهام | Total Shares | Total outstanding shares (float, often large) |
| `baseVol` | حجم مبنا | Base Volume | Minimum volume for price calculation |
| `qTotTran5JAvg` | میانگین حجم 5 روز | 5-Day Avg Volume | Usually 0 in current data |
| `qTotTran5J` | حجم 5 روز | 5-Day Total Volume | Inclosing price info |
| `qTotCap` | ارزش بازار | Market Cap | Market capitalization |

### Price Fields

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `pClosing` | قیمت پایانی | Closing Price | Official closing price |
| `pDrCotVal` | آخرین معامله | Last Trade Price | Price of most recent trade |
| `priceChange` | تغییر | Price Change | Difference from yesterday's close |
| `priceMin` | کمترین | Daily Min | Today's minimum price |
| `priceMax` | بیشترین | Daily Max | Today's maximum price |
| `priceYesterday` | قیمت دیروز | Yesterday Close | Previous trading day's closing price |
| `priceFirst` | اولین قیمت | Open Price | Today's opening price |
| `pRedTran` | قیمت مجاز | Allowed Price | Current allowed trading price |
| `nvt` | — | — | Net value traded? |

### Static Thresholds (حدود مجاز قیمت)

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `psGelStaMax` | حداکثر قیمت مجاز | Max Allowed | e.g. 2682.0 (toman) — +5% from reference |
| `psGelStaMin` | حداقل قیمت مجاز | Min Allowed | e.g. 2526.0 — -5% from reference |

### EPS & Valuation

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `eps.epsValue` | EPS | EPS Value | Current EPS (often null) |
| `eps.estimatedEPS` | EPS برآوردی | Estimated EPS | e.g. `389` (toman per share) |
| `eps.sectorPE` | P/E صنعت | Sector P/E | e.g. 11.06 |
| `eps.psr` | P/S | PSR Ratio | Price-to-sales ratio |
| `estimatedEPS` | EPS برآوردی | Estimated EPS | (same, in ParTree format) |
| `SectorPE` | P/E صنعت | Sector P/E | (same, in ParTree format) |
| `PSR` | P/S | PSR | (same, in ParTree format) |

### Supply/Demand Info

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `zd` | حجم تقاضا | Demand Volume | At a specific price level |
| `qd` | تعداد تقاضا | Demand Count | Number of orders at demand side |
| `pd` | قیمت تقاضا | Demand Price | Bid price |
| `zo` | حجم عرضه | Supply Volume | At a specific price level |
| `qo` | تعداد عرضه | Supply Count | Number of orders at supply side |
| `po` | قیمت عرضه | Supply Price | Ask price |

### NAV & ETF

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `nav` | NAV | Net Asset Value | For ETFs only |
| `nav_datetime` | زمان NAV | NAV Time | Jalali datetime |
| `etfIssuedUnit` | واحدهای منتشر شده | Issued Units | ETF unit count |
| `etfUnitDeven` | تاریخ واحدها | Unit Date | ETF unit date |
| `contractSize` | حجم قرارداد | Contract Size | For futures/options |

### Week/Year Price Range

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `minWeek` | کمترین هفته | 52-Week Low | (often 0) |
| `maxWeek` | بیشترین هفته | 52-Week High | (often 0) |
| `minYear` | کمترین سال | Year Low | e.g. 2010.0 |
| `maxYear` | بیشترین سال | Year High | e.g. 4490.0 |

### Free Float

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `kAjCapValCpsIdx` | درصد شناور | Free Float % | e.g. `36` means 36% free float |

### Sector

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `sector.cSecVal` | کد صنعت | Industry Code | e.g. `27` (فلزات اساسی) |
| `sector.lSecVal` | نام صنعت | Industry Name | e.g. `فلزات اساسي` |
| `cgrValCot` | کد گروه | Market Board Code | e.g. `N1` = بازار اول تابلو اصلی |

### Instrument State

| Field | Persian | English | Notes |
|-------|---------|---------|-------|
| `cEtaval` | کد وضعیت | Status Code | e.g. `A` (مجاز/Allowed), `B` (ممنوع/Blocked) |
| `cEtavalTitle` | عنوان وضعیت | Status Title | e.g. `مجاز`, `ممنوع`, `متوقف` |
| `underSupervision` | زیر نظارت | Under Supervision | 0 or 1 |

## Live Data (instinfofast) Fields

From the old API price info section (16 comma-separated values):

| Index | Variable | Persian | English |
|-------|----------|---------|---------|
| 0 | `time` | زمان | Last trade time (HHMMSS) |
| 1 | `status` | وضعیت | Instrument status |
| 2 | `pl` | آخرین قیمت | Last price |
| 3 | `pc` | قیمت پایانی | Closing price |
| 4 | `pf` | اولین قیمت | Open/First price |
| 5 | `py` | قیمت دیروز | Yesterday's close |
| 6 | `pmin` | کمترین | Today's minimum |
| 7 | `pmax` | بیشترین | Today's maximum |
| 8 | `tno` | تعداد معاملات | Number of trades |
| 9 | `tvol` | حجم معاملات | Trade volume |
| 10 | `tval` | ارزش معاملات | Trade value (Rial) |
| 11 | — | — | CSS/style info (ignored) |
| 12 | `info_date` | تاریخ اطلاعات | Date (YYYYMMDD) |
| 13 | `last_info_time` | زمان اطلاعات | Time (HHMMSS) |
| 14 | `nav_date` | تاریخ NAV | NAV date (Jalali) |
| 15 | `nav` | NAV | Net asset value (ETFs) |

## Client Type Fields

`I` = حقیقی (individual/natural person)
`N` = حقوقی (legal/institutional/corporate)
`DDD` = (some third category, used internally)

| Field | Persian | English |
|-------|---------|---------|
| `buy_I_Volume` | حجم خرید حقیقی | Individual buy volume |
| `buy_N_Volume` | حجم خرید حقوقی | Legal buy volume |
| `buy_I_Value` | ارزش خرید حقیقی | Individual buy value |
| `buy_N_Value` | ارزش خرید حقوقی | Legal buy value |
| `buy_CountI` | تعداد خرید حقیقی | Individual buy count |
| `buy_CountN` | تعداد خرید حقوقی | Legal buy count |
| `sell_I_Volume` | حجم فروش حقیقی | Individual sell volume |
| `sell_N_Volume` | حجم فروش حقوقی | Legal sell volume |
| `sell_I_Value` | ارزش فروش حقیقی | Individual sell value |
| `sell_N_Value` | ارزش فروش حقوقی | Legal sell value |
| `sell_CountI` | تعداد فروش حقیقی | Individual sell count |
| `sell_CountN` | تعداد فروش حقوقی | Legal sell count |

## Shareholder Fields

| Field | Persian | English |
|-------|---------|---------|
| `shareHolderName` | نام سهامدار | Shareholder name |
| `numberOfShares` | تعداد سهام | Number of shares |
| `perOfShares` | درصد | Percentage ownership |
| `change` | تغییر | Change direction (1=up) |
| `changeAmount` | مقدار تغییر | Change amount |
| `dEven` | تاریخ | Date (YYYYMMDD) |
| `cIsin` | کد ISIN | Company ISIN |
| `shareHolderShareID` | کد سهامدار | Shareholder ID (for history query) |

## Instrument History & Closing Price

| Field | Meaning | Notes |
|-------|---------|-------|
| `zTotTran` | Total volume | Cumulative volume |
| `iClose` | Is closing? | Boolean |
| `yClose` | Is yesterday closing? | Boolean |
| `last` | Is last data? | Boolean |
| `mop` | Market operation? | Integer |
| `thirtyDayClosingHistory` | 30-day history | Array or null |

## Market State Fields

From the old API market state section:

| Index | Meaning | Notes |
|-------|---------|-------|
| 0 | Datetime | Jalali `MM/DD/YYYY HH:MM:SS` |
| 1 | TSE Status | `بازار بسته`, `بازار باز`, etc. |
| 2 | TSE Index | شاخص کل |
| 3 | TSE Index Change | e.g. `(88883.33) 1.76%` or empty |
| 4 | TSE Value | ارزش بازار |
| 5 | TSE Total Volume | حجم کل |
| 6 | TSE Total Value | ارزش کل |
| 7 | TSE Total Trades | تعداد کل معاملات |
| 8 | FaraBourse Status | وضعیت فرابورس |
| 9 | FB Total Volume | حجم فرابورس |
| 10 | FB Total Value | ارزش فرابورس |
| 11 | FB Total Trades | تعداد فرابورس |
| 12 | Derivatives Status | وضعیت مشتقه |
| 13 | Derivatives Volume | حجم مشتقه |
| 14 | Derivatives Value | ارزش مشتقه |
| 15 | Derivatives Trades | تعداد مشتقه |
| 16 | Extra | Sometimes present |

## yVal (Asset Type) Codes

| Code | Meaning |
|------|---------|
| `300` | سهام (Stock) |
| `301` | حق تقدم (Preemptive Right) |
| `302` | واحد سرمایه‌گذاری صندوق (Fund Unit) |
| Others | ETF, debt securities, etc. |

## Flow (Trading Market) Codes

| Code | Meaning |
|------|---------|
| `0` | عمومی (General) |
| `1` | بورس (TSE Main) |
| `2` | فرابورس (OTC) |
| `4` | بازار پایه (UTP/Payeh) |
| `18` | ETF صندوق‌ها |
| `19` | بازار حرفه‌ای (Professional) |