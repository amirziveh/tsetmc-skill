"""TSETMC API Client — Complete Python Implementation

A full-featured client for all three TSETMC API surfaces.
Uses only stdlib (urllib, json, csv) — no external dependencies.

Usage:
    client = TsetmcClient()
    info = client.instrument_info("46348559193224090")
    prices = client.price_history("46348559193224090", top=100)
"""

import csv
import json
import io
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Optional

# ── API Base URLs ──────────────────────────────────────────────────

CDN_API = "https://cdn.tsetmc.com/api/"
OLD_API = "http://old.tsetmc.com/tsev2/data/"
OLD_PAGE = "http://old.tsetmc.com/Loader.aspx"
SERVICE_API = "http://service.tsetmc.com/tsev2/data/"
MEMBERS_API = "https://members.tsetmc.com/tsev2/chart/data/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
}


class TsetmcClient:
    """TSETMC API client covering all three API surfaces."""

    def __init__(self, delay: float = 0.2):
        self.delay = delay  # seconds between calls to avoid rate limiting

    def _request_json(self, url: str) -> dict:
        """Make a JSON API request to the CDN API."""
        time.sleep(self.delay)
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())

    def _request_text(self, url: str) -> str:
        """Make a plain text request (old API)."""
        time.sleep(self.delay)
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")

    # ── Instrument ──────────────────────────────────────────────

    def search_symbol(self, query: str) -> list[dict]:
        """Search for instruments by Persian or English name."""
        url = CDN_API + f"Instrument/GetInstrumentSearch/{urllib.parse.quote(query)}"
        return self._request_json(url).get("instrumentSearch", [])

    def instrument_info(self, ins_code: str) -> dict:
        """Get full instrument info (EPS, sector, thresholds, ISIN, etc.)."""
        url = CDN_API + f"Instrument/GetInstrumentInfo/{ins_code}"
        return self._request_json(url).get("instrumentInfo", {})

    def instrument_identity(self, ins_code: str) -> dict:
        """Get instrument identity data (sector, sub-sector, full names)."""
        url = CDN_API + f"Instrument/GetInstrumentIdentity/{ins_code}"
        return self._request_json(url).get("instrumentIdentity", {})

    def instrument_history(self, ins_code: str, date: str) -> dict:
        """Get instrument history for a specific date (YYYYMMDD)."""
        url = CDN_API + f"Instrument/GetInstrumentHistory/{ins_code}/{date}"
        return self._request_json(url).get("instrumentHistory", {})

    # ── Closing Price ───────────────────────────────────────────

    def closing_price_daily(self, ins_code: str, days: int = 0) -> list[dict]:
        """Get daily closing price history. days=0 returns all."""
        url = CDN_API + f"ClosingPrice/GetClosingPriceDailyList/{ins_code}/{days}"
        return self._request_json(url).get("closingPriceDaily", [])

    def closing_price_info(self, ins_code: str) -> dict:
        """Get current closing price info snapshot."""
        url = CDN_API + f"ClosingPrice/GetClosingPriceInfo/{ins_code}"
        return self._request_json(url).get("closingPriceInfo", {})

    def closing_price_daily_for_date(self, ins_code: str, date: str) -> dict:
        """Get closing price for a specific date (YYYYMMDD)."""
        url = CDN_API + f"ClosingPrice/GetClosingPriceDaily/{ins_code}/{date}"
        return self._request_json(url).get("closingPriceDaily", {})

    def closing_price_history(self, ins_code: str, date: str) -> list[dict]:
        """Get intraday closing price history for a date."""
        url = CDN_API + f"ClosingPrice/GetClosingPriceHistory/{ins_code}/{date}"
        return self._request_json(url).get("closingPriceHistory", [])

    def trade_top(self, category: str, flow: int = 1, top: int = 10) -> list[dict]:
        """Get trade top lists.
        Categories: MostVisited, ETF, MostTradedETF, PClosingTopETF, PClosingBtmETF, CommodityFund
        """
        url = CDN_API + f"ClosingPrice/GetTradeTop/{category}/{flow}/{top}"
        return self._request_json(url).get("tradeTop", [])

    def price_adjust_list(self, ins_code: str) -> list[dict]:
        """Get price adjustment history (splits, capital increases)."""
        url = CDN_API + f"ClosingPrice/GetPriceAdjustList/{ins_code}"
        return self._request_json(url).get("priceAdjust", [])

    def related_companies(self, cs: str) -> dict:
        """Get related companies in the same industry group."""
        url = CDN_API + f"ClosingPrice/GetRelatedCompany/{cs}"
        return self._request_json(url)

    # ── Market Data ─────────────────────────────────────────────

    def market_overview(self, flow: int = 1) -> dict:
        """Get market overview (may return empty when market closed)."""
        url = CDN_API + f"MarketData/GetMarketOverview/{flow}"
        return self._request_json(url).get("marketOverview", {})

    def instrument_state(self, ins_code: str, date: str) -> list[dict]:
        """Get intraday instrument status history."""
        url = CDN_API + f"MarketData/GetInstrumentState/{ins_code}/{date}"
        return self._request_json(url).get("instrumentState", [])

    # ── Trade ───────────────────────────────────────────────────

    def trades(self, ins_code: str) -> list[dict]:
        """Get current day's trades. May be empty before/after hours."""
        url = CDN_API + f"Trade/GetTrade/{ins_code}"
        return self._request_json(url).get("trade", [])

    def trade_history(self, ins_code: str, date: str) -> list[dict]:
        """Get historical trades for a specific day (YYYYMMDD)."""
        url = CDN_API + f"Trade/GetTradeHistory/{ins_code}/{date}/true"
        return self._request_json(url).get("tradeHistory", [])

    # ── Client Type (حقیقی-حقوقی) ───────────────────────────────

    def client_type(self, ins_code: str) -> dict:
        """Get current day's client type snapshot. Zeros outside hours."""
        url = CDN_API + f"ClientType/GetClientType/{ins_code}/1/0"
        return self._request_json(url).get("clientType", {})

    def client_type_history(self, ins_code: str) -> list[dict]:
        """Get full client type history for an instrument."""
        url = CDN_API + f"ClientType/GetClientTypeHistory/{ins_code}"
        return self._request_json(url).get("clientType", [])

    def client_type_all(self) -> list[dict]:
        """Get all instruments' client type data (experimental API)."""
        url = CDN_API + "ClientType/GetClientTypeAll"
        return self._request_json(url).get("clientTypeAllDto", [])

    # ── Best Limits (Order Book) ────────────────────────────────

    def best_limits(self, ins_code: str) -> list[dict]:
        """Get current best buy/sell limits. Empty outside trading hours."""
        url = CDN_API + f"BestLimits/{ins_code}"
        return self._request_json(url).get("bestLimits", [])

    def best_limits_history(self, ins_code: str, date: str) -> list[dict]:
        """Get historical best limits for a specific date (YYYYMMDD)."""
        url = CDN_API + f"BestLimits/{ins_code}/{date}"
        return self._request_json(url).get("bestLimitsHistory", [])

    # ── Shareholder ─────────────────────────────────────────────

    def shareholders(self, ins_code: str) -> list[dict]:
        """Get current major shareholders."""
        url = CDN_API + f"Shareholder/GetInstrumentShareHolderLast/{ins_code}"
        return self._request_json(url).get("shareHolder", [])

    def shareholders_on_date(self, ins_code: str, date: str) -> list[dict]:
        """Get shareholders on a specific date (YYYYMMDD)."""
        url = CDN_API + f"Shareholder/{ins_code}/{date}"
        return self._request_json(url).get("shareShareholder", [])

    def shareholder_history(self, ins_code: str, holder_id: int, days: int = 90) -> list[dict]:
        """Get share change history for a specific holder."""
        url = CDN_API + f"Shareholder/GetShareHolderHistory/{ins_code}/{holder_id}/{days}"
        return self._request_json(url).get("shareHolder", [])

    def shareholder_companies(self, share_id: int) -> list[dict]:
        """Get all companies held by a specific shareholder."""
        url = CDN_API + f"Shareholder/GetShareHolderCompanyList/{share_id}"
        return self._request_json(url).get("shareHolderShare", [])

    # ── Index ───────────────────────────────────────────────────

    def index_last_state(self) -> list[dict]:
        """Get latest state of all indices."""
        url = CDN_API + "Index/GetIndexB1LastAll/All/1"
        return self._request_json(url).get("indexB1", [])

    def index_last_day(self, code: str) -> list[dict]:
        """Get intraday index ticks for last trading day."""
        url = CDN_API + f"Index/GetIndexB1LastDay/{code}"
        return self._request_json(url).get("indexB1", [])

    def index_daily_history(self, code: str) -> list[dict]:
        """Get daily index history."""
        url = CDN_API + f"Index/GetIndexB2History/{code}"
        return self._request_json(url).get("indexB2", [])

    # ── Fund / ETF ──────────────────────────────────────────────

    def funds(self, fund_type: str = "6") -> list[dict]:
        """Get fund list by type. Types: 4=Fixed, 5=Commodity, 6=Stock, 7=Mixed, 14=REIT, 17=Fund"""
        url = CDN_API + f"Fund/GetFunds/{fund_type}"
        return self._request_json(url).get("funds", [])

    def etf_info(self, ins_code: str) -> dict:
        """Get ETF redemption NAV data."""
        url = CDN_API + f"Fund/GetETFByInsCode/{ins_code}"
        return self._request_json(url).get("etf", {})

    # ── Messages ────────────────────────────────────────────────

    def messages(self, flow: int = 0, top: int = 10) -> list[dict]:
        """Get market announcements."""
        url = CDN_API + f"Msg/GetMsgByFlow/{flow}/{top}"
        return self._request_json(url).get("msg", [])

    def messages_by_instrument(self, ins_code: str) -> list[dict]:
        """Get messages specific to an instrument."""
        url = CDN_API + f"Msg/GetMsgByInsCode/{ins_code}"
        return self._request_json(url).get("msg", [])

    def search_messages(self, date: str, term: str) -> list[dict]:
        """Search messages by Jalali date YYYY-mm-dd and keyword."""
        url = CDN_API + f"Msg/GetMsgByDevenAndLVal18AFC/{date}/{term}"
        return self._request_json(url).get("msg", [])

    # ── Codal ───────────────────────────────────────────────────

    def codal_publisher(self, symbol: str) -> dict:
        """Get company publisher info from Codal."""
        url = CDN_API + f"Codal/GetCodalPublisherBySymbol/{urllib.parse.quote(symbol)}"
        return self._request_json(url).get("codalPublisher", {})

    # ── Old API (Legacy) ────────────────────────────────────────

    def market_watch_all(self) -> str:
        """Get full market snapshot (old API). Returns @-separated text."""
        return self._request_text(OLD_API + "MarketWatchInit.aspx?h=0&r=0")

    def parse_market_watch(self, raw: str) -> dict:
        """Parse MarketWatchInit response into sections."""
        parts = raw.split("@")
        if len(parts) < 5:
            return {"error": f"Expected 5 parts, got {len(parts)}"}
        return {
            "messages": parts[0],
            "market_state": parts[1],
            "prices": parts[2],
            "best_limits": parts[3],
            "refid": int(parts[4]) if parts[4].strip() else 0,
        }

    def last_trading_day(self) -> str:
        """Get last trading day as YYYYMMDD (service API)."""
        return self._request_text(SERVICE_API + "TseClient2.aspx?t=LastPossibleDeven").split(";")[0]

    def old_price_history(self, ins_code: str, top: int = 100) -> list[dict]:
        """Get price history via old API (more reliable than CDN version)."""
        text = self._request_text(
            OLD_API + f"InstTradeHistory.aspx?i={ins_code}&Top={top}&A=0"
        )
        rows = text.rstrip(";").split(";")
        result = []
        for row in rows:
            fields = row.split("@")
            if len(fields) >= 10:
                result.append({
                    "date": fields[0],
                    "pmax": fields[1],
                    "pmin": fields[2],
                    "pc": fields[3],
                    "pl": fields[4],
                    "pf": fields[5],
                    "py": fields[6],
                    "tval": fields[7],
                    "tvol": fields[8],
                    "tno": fields[9],
                })
        return result

    def old_client_type(self, ins_code: str) -> list[dict]:
        """Get client type history via old API."""
        text = self._request_text(OLD_API + f"clienttype.aspx?i={ins_code}")
        reader = csv.DictReader(
            io.StringIO(text.replace(";", "\n")),
            fieldnames=["date", "n_buy_count", "l_buy_count", "n_sell_count",
                        "l_sell_count", "n_buy_volume", "l_buy_volume",
                        "n_sell_volume", "l_sell_volume", "n_buy_value",
                        "l_buy_value", "n_sell_value", "l_sell_value"],
        )
        return list(reader)


# ── Example Usage ─────────────────────────────────────────────────

if __name__ == "__main__":
    client = TsetmcClient(delay=0.3)

    # 1. Search for فولاد
    results = client.search_symbol("فولاد")
    if results:
        code = results[0]["insCode"]
        print(f"Found: {results[0]['lVal30']} → {code}")

        # 2. Get instrument info
        info = client.instrument_info(code)
        print(f"EPS: {info.get('eps', {}).get('estimatedEPS')}")
        print(f"Sector PE: {info.get('eps', {}).get('sectorPE')}")
        print(f"Total shares: {info.get('zTitad')}")

        # 3. Get shareholders
        holders = client.shareholders(code)
        print(f"\nTop shareholders ({len(holders)}):")
        for h in holders[:5]:
            print(f"  {h['shareHolderName']}: {h['perOfShares']}%")

        # 4. Get today's messages
        msgs = client.messages(flow=0, top=5)
        print(f"\nRecent announcements: {len(msgs)}")
        for m in msgs[:3]:
            print(f"  [{m['dEven']}] {m['tseTitle']}")