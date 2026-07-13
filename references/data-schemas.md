# TSETMC Data Schemas

Typed dict definitions for all API response shapes. Fields documented with Persian names where available.

---

## InstrumentInfo
```python
class InstrumentInfo(TypedDict):
    eps: Eps                              # EPS data
    sector: Sector                        # Industry sector
    staticThreshold: StaticThreshold      # Daily price limits
    minWeek: float                        # 52-week low
    maxWeek: float                        # 52-week high
    minYear: float                        # Year low
    maxYear: float                        # Year high
    qTotTran5JAvg: float                  # 5-day avg trade volume
    kAjCapValCpsIdx: str                 # Free float percentage (string!)
    dEven: int                           # Date (YYYYMMDD)
    topInst: int                         # Instrument type code
    faraDesc: str                        # Fara Bourse description
    contractSize: int                    # Contract size
    nav: float                           # NAV (for funds)
    underSupervision: int                # Under supervision flag
    etfIssuedUnit: float                 # ETF issued units
    etfUnitDeven: int                    # ETF unit date
    cValMne: str | None                  # English symbol
    lVal18: str | None                   # English name (18 chars)
    cSocCSAC: str | None                 # Company ISIC code
    lSoc30: str | None                   # Company name
    yMarNSC: str | None                  # Market code
    yVal: str                            # Instrument type (300=stock)
    insCode: str                         # Instrument code
    lVal30: str                          # Persian name (30 chars)
    lVal18AFC: str                       # Persian symbol (18 chars)
    flow: int                            # Market flow code
    cIsin: str                           # Company ISIN
    zTitad: float                        # Total issued shares (تعداد سهام)
    baseVol: int                         # Base volume (حجم مبنا)
    instrumentID: str                    # Instrument ISIN
    cgrValCot: str                       # Market group code
    cComVal: str                         # Company code
    lastDate: int                        # Last trade date
    sourceID: int                        # Data source ID
    flowTitle: str                       # Market name in Persian
    cgrValCotTitle: str                  # Market group name in Persian

class Eps(TypedDict):
    epsValue: float | None              # EPS value
    estimatedEPS: str | None            # Estimated EPS (P/E ratio numerator)
    sectorPE: float                     # Sector P/E ratio
    psr: float                          # P/S ratio

class Sector(TypedDict):
    dEven: int                          # Date
    cSecVal: str                        # Industry group code
    lSecVal: str                        # Industry group name (e.g. "فلزات اساسي")

class StaticThreshold(TypedDict):
    insCode: None
    dEven: int
    hEven: int
    psGelStaMax: float                  # Daily max price limit (قیمت حداکثر)
    psGelStaMin: float                  # Daily min price limit (قیمت حداقل)
```

## Identity
```python
class Identity(TypedDict):
    sector: Sector                        # Industry sector
    subSector: SubSector                  # Sub-sector
    cValMne: str                         # English symbol
    lVal18: str                          # English name
    cSocCSAC: str                        # ISIC code
    lSoc30: str                          # Company name
    yMarNSC: str                         # Market/NSC code
    yVal: str                            # Instrument type
    insCode: str                         # Instrument code
    lVal30: str                          # Persian full name
    lVal18AFC: str                       # Persian symbol
    flow: int                            # Market flow
    cIsin: str                           # Company ISIN
    zTitad: float                        # Total shares
    baseVol: int                         # Base volume
    instrumentID: str                    # Instrument ISIN
    cgrValCot: str                       # Market group
    cComVal: str                         # Company code
    lastDate: int                        # Last date
    sourceID: int                        # Source

class SubSector(TypedDict):
    dEven: int
    cSecVal: None
    cSoSecVal: int                       # Sub-sector code
    lSoSecVal: str                       # Sub-sector name
```

## ClosingPriceInfo / ClosingPrice
```python
class ClosingPriceInfo(TypedDict):
    instrumentState: InstrumentState | None  # Market status
    instrument: dict | None                  # Embedded instrument info
    lastHEven: int                           # Last trade time
    finalLastDate: int                       # Last date with trade
    nvt: float                               # ? 
    mop: int                                 # Market operation type
    pRedTran: float                          # Redemption price
    thirtyDayClosingHistory: list | None     # 30-day history
    priceChange: float                       # Price change from yesterday
    priceMin: float                          # Day low
    priceMax: float                          # Day high
    priceYesterday: float                    # Previous close
    priceFirst: float                        # Opening price
    last: bool                               # Last price (unclear)
    id: int
    insCode: str
    dEven: int                              # Date
    hEven: int                              # Time
    pClosing: float                         # Closing price (قیمت پایانی)
    iClose: bool                            # Closed?
    yClose: bool                            # Yesterday closed?
    pDrCotVal: float                        # Last trade price (آخرین معامله)
    zTotTran: float                         # Total trades
    qTotTran5J: float                       # 5-day avg volume
    qTotCap: float                          # Market cap

class InstrumentState(TypedDict):
    idn: int
    dEven: int
    hEven: int
    insCode: None
    lVal18AFC: None
    lVal30: None
    cEtaval: str                            # Status code
    realHeven: int                          # Real time
    underSupervision: int
    cEtavalTitle: str                       # Status name (e.g. "مجاز", "متوقف")
```

## ClientType / ClientTypeOnDate
```python
class ClientType(TypedDict):
    buy_I_Volume: float                    # Natural persons buy volume
    buy_N_Volume: float                    # Legal persons buy volume
    buy_DDD_Volume: float                  # ? (often 0)
    buy_CountI: int                        # Natural persons buy count
    buy_CountN: int                        # Legal persons buy count
    buy_CountDDD: int                      # ?
    sell_I_Volume: float                   # Natural persons sell volume
    sell_N_Volume: float                   # Legal persons sell volume
    sell_CountI: int                       # Natural persons sell count
    sell_CountN: int                       # Legal persons sell count

class ClientTypeOnDate(TypedDict):
    recDate: int                           # Date (YYYYMMDD)
    insCode: str                           # Instrument code
    buy_I_Volume: float                    # Natural buy volume
    buy_N_Volume: float                    # Legal buy volume
    buy_I_Value: float                     # Natural buy value (Rial)
    buy_N_Value: float                     # Legal buy value
    buy_N_Count: int
    sell_I_Volume: float
    buy_I_Count: float
    sell_N_Volume: float
    sell_I_Value: float
    sell_N_Value: float
    sell_N_Count: int
    sell_I_Count: int
```

## ShareHolder
```python
class ShareHolder(TypedDict):
    shareHolderID: int                     # Internal ID
    shareHolderName: str | None            # Shareholder name
    cIsin: str                             # Company ISIN
    dEven: int                             # Date
    numberOfShares: float                  # Shares held (تعداد سهام)
    perOfShares: float                     # Percentage (درصد مالکیت)
    change: int                            # Direction of change
    changeAmount: float                    # Amount of change
    shareHolderShareID: int                # Unique ID for this holding
```

## MarketOverview
```python
class MarketOverview(TypedDict):
    indexChange: float                     # Index change
    indexEqualWeightedChange: float        # Equal-weight index change
    indexEqualWeightedLastValue: float     # Equal-weight index value
    indexLastValue: float                  # Main index value
    lastDataDEven: int                     # Last data date
    lastDataHEven: int                     # Last data time
    marketActivityDEven: int               # Activity date
    marketActivityHEven: int               # Activity time
    marketActivityQTotCap: float           # Total market cap
    marketActivityQTotTran: float          # Total trade volume
    marketActivityTimestamp: datetime      # Activity timestamp
    marketActivityZTotTran: int            # Total trades count
    marketState: str                       # Market state code
    marketStateTitle: str                  # Market state text
    marketValue: float                     # Market value
    marketValueBase: float                 # Market value base
```

## Search
```python
class Search(TypedDict):
    insCode2: str                          # Secondary insCode
    insCode3: str                          # Tertiary insCode
    insCode4: str                          # Quaternary insCode
    insCode: str                           # Primary insCode
    lVal30: str                            # Full Persian name
    lVal18AFC: str                         # Persian symbol
    flow: int                              # Market flow
    cIsin: None
    zTitad: float                          # Total shares
    baseVol: int                           # Base volume
    instrumentID: None
    cgrValCot: str                         # Market group code
    cComVal: None
    lastDate: int
    sourceID: int
    flowTitle: str                         # Market name
    cgrValCotTitle: str                    # Group name
```

## LiveData (from instinfofast/instinfodata)
```python
class LiveData(TypedDict, total=False):
    best_limits: pl.LazyFrame               # Order book
    market_state: MarketState               # Market state
    nav: int                                # NAV (for ETFs)
    nav_datatime: datetime
    pc: int                                 # Closing price (قیمت پایانی)
    pf: int                                 # First price (قیمت اولین معامله)
    pl: int                                 # Last trade price (آخرین معامله)
    pmax: int                               # Day max
    pmin: int                               # Day min
    py: int                                 # Yesterday close
    status: str                             # Status text
    timestamp: datetime                     # Data timestamp
    tno: int                                # Trades count
    tval: int                                # Trade value (Rial)
    tvol: int                                # Trade volume
```

## MarketState
```python
class MarketState(TypedDict, total=False):
    datetime: datetime                      # Timestamp
    tse_status: str                         # TSE market status (باز/بسته)
    tse_index: float                        # TSE index value
    tse_index_change: float | None          # Index change points
    tse_index_change_percent: float | None  # Index change %
    tse_value: float | None                  # TSE value
    tse_tvol: float                         # TSE trade volume
    tse_tval: float                         # TSE trade value
    tse_tno: float                          # TSE trades count
    fb_status: str                          # Fara Bourse status
    fb_tvol: float                          # FB trade volume
    fb_tval: float                          # FB trade value
    fb_tno: int                             # FB trades count
    derivatives_status: str                 # Derivatives status
    derivatives_tval: float                 # Derivatives value
    derivatives_tvol: float                 # Derivatives volume
    derivatives_tno: int                    # Derivatives count
```

## Message
```python
class Message(TypedDict):
    tseMsgIdn: int                         # Message ID
    dEven: int                             # Date
    hEven: int                             # Time
    tseTitle: str                          # Title in Persian
    tseDesc: str                           # Description in Persian
    flow: int                              # Market flow
```

## CodalPublisher
```python
class CodalPublisher(TypedDict):
    id: int
    symbol: str
    displaySymbol: str
    name: str
    isic: str                              # ISIC code
    reportingType: str
    executiveManager: str
    address: str
    telNo: str
    faxNo: str
    activitySubject: str
    officeAddress: str
    shareOfficeAddress: str
    website: str
    email: str
    state: str
    companyType: str
    stateName: str | None
```

## ETF
```python
class ETF(TypedDict):
    insCode: str
    deven: int                             # Date
    hEven: int                             # Time
    pRedTran: float                        # Redemption price (قیمت ابطال)
    pSubTran: float                        # Subscription price (قیمت صدور)
    iClose: int                            # Closing price
```

## MarketWatchInit
```python
class MarketWatchInit(TypedDict):
    prices: pl.DataFrame | None            # 26-column price data
    best_limits: pl.DataFrame | None       # Order book data
    market_state: MarketState | None       # Market state
    refid: int                             # Reference ID for polling
```

## Key Stats (InstValue)
Common `n` values for `InstValue.aspx?t=a`:
| n | Meaning |
|---|---------|
| is12 | P/E (TTM) |
| is13 | P/E (current year) |
| is14 | P/S |
| is15 | EPS |
| is24 | Volume weighted average |
| is25 | Free float % |
| is26 | Market cap / Net income |