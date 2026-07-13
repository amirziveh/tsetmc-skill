#!/usr/bin/env python3
"""
generate-configs.py — Auto-generate all agent config files from the references/.

Run this whenever you update references/*.md. It keeps all 6 agent configs in sync
with a single source of truth: references/REFERENCE_NAMES and references/ENDPOINTS.

Usage:
    python3 generate-configs.py          # Generate all agent configs
    python3 generate-configs.py --check  # Verify configs are up-to-date (CI)
"""

import os
import sys
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent

# ── Source of Truth ────────────────────────────────────────────────

REFERENCE_FILES = [
    "references/api-endpoints.md",
    "references/data-schemas.md",
    "references/flow-and-yval-codes.md",
    "references/tsetmc-api-endpoints.md",
    "references/tsetmc-field-dictionary.md",
]

TEMPLATE_FILES = [
    "templates/python-client.py",
    "templates/pytse-client-usage.md",
    "templates/tsetmc-package-usage.md",
]

API_SURFACES = [
    ("CDN API (JSON)", "https://cdn.tsetmc.com/api/", "JSON"),
    ("Old API (CSV)", "http://old.tsetmc.com/tsev2/data/", "CSV/delimited"),
    ("Service", "http://service.tsetmc.com/tsev2/data/", "Text"),
]

KEY_ENDPOINTS: list[dict[str, str]] = [
    {"method": "GET", "path": "/Instrument/GetInstrumentSearch/{query}", "desc": "Search symbols"},
    {"method": "GET", "path": "/Instrument/GetInstrumentInfo/{insCode}", "desc": "Instrument info"},
    {"method": "GET", "path": "/ClosingPrice/GetClosingPriceDailyList/{insCode}/{days}", "desc": "Price history"},
    {"method": "GET", "path": "/ClientType/GetClientTypeHistory/{insCode}", "desc": "Client types"},
    {"method": "GET", "path": "/Shareholder/GetInstrumentShareHolderLast/{insCode}", "desc": "Shareholders"},
    {"method": "GET", "path": "/Msg/GetMsgByFlow/{flow}/{top}", "desc": "Messages"},
    {"method": "GET", "path": "/ClosingPrice/GetTradeTop/{category}/{flow}/{top}", "desc": "Trade top lists"},
    {"method": "GET", "path": "/Index/GetIndexB2History/{code}", "desc": "Index history"},
    {"method": "GET", "path": "/Fund/GetFunds/{type}", "desc": "Fund list"},
    {"method": "GET", "path": "/Codal/GetCodalPublisherBySymbol/{symbol}", "desc": "Codal publisher"},
]

PROJECT_DESC = "TSETMC (Tehran Stock Exchange) API ecosystem — reverse-engineered"

# ── Agent config templates ─────────────────────────────────────────

def _ref_list() -> str:
    return "\n".join(f"- `{f}`" for f in REFERENCE_FILES + TEMPLATE_FILES)

def _api_list() -> str:
    return "\n".join(f"- **{name}**: `{url}` — {fmt}" for name, url, fmt in API_SURFACES)

def _endpoint_list() -> str:
    return "\n".join(f"- `{e['method']} {e['path']}` — {e['desc']}" for e in KEY_ENDPOINTS)


def claude_md() -> str:
    return f"""# {PROJECT_DESC}

## Key Files

{_ref_list()}

## Quick Reference

### API Surfaces
{_api_list()}

### Key Endpoints
{_endpoint_list()}

### Notes
- insCode is a 15-20 digit numeric instrument code (not the Persian symbol name)
- Dates use Gregorian YYYYMMDD (field: dEven)
- Times use HHMMSS without leading zeros (field: hEven)
- Some CDN endpoints return empty when market is closed; fall back to old API
- Rate limit: 0.5-1s between calls for batch operations

Read the files in `references/` for full documentation before writing API calls.
"""


def cursor_rules() -> str:
    return f"""# {PROJECT_DESC}

## Key Files
{_ref_list()}

## API Surfaces
{_api_list()}

## Key Endpoints
{_endpoint_list()}

See references/*.md for full documentation.
"""


def opencode_md() -> str:
    return f"""# {PROJECT_DESC}

## Key Files
{_ref_list()}

## API Surfaces
{_api_list()}

## Key Endpoints
{_endpoint_list()}

For full details, read the files in references/.
"""


def windsurf_rules() -> str:
    return f"""# {PROJECT_DESC}

## Key Files
{_ref_list()}

## API Surfaces
{_api_list()}

## Key Endpoints
{_endpoint_list()}

See references/*.md for full documentation.
"""


def copilot_instructions() -> str:
    return f"""# {PROJECT_DESC}

## Key Files
{_ref_list()}

## API Surfaces
{_api_list()}

## Key Endpoints
{_endpoint_list()}

See references/ for full documentation.
"""


def codify_md() -> str:
    return f"""# {PROJECT_DESC}

## Key Files
{_ref_list()}

## API Surfaces
{_api_list()}

## Key Endpoints
{_endpoint_list()}

See references/*.md for full documentation.
"""

# ── Config map ─────────────────────────────────────────────────────

AGENT_CONFIGS: list[dict[str, Any]] = [
    {"path": "CLAUDE.md", "content": claude_md(), "agents": ["Claude Code"]},
    {"path": ".cursorrules", "content": cursor_rules(), "agents": ["Cursor"]},
    {"path": ".opencode.md", "content": opencode_md(), "agents": ["OpenCode"]},
    {"path": ".windsurfrules", "content": windsurf_rules(), "agents": ["Windsurf"]},
    {"path": ".github/copilot-instructions.md", "content": copilot_instructions(), "agents": ["GitHub Copilot"]},
    {"path": "CODIFY.md", "content": codify_md(), "agents": ["Codify"]},
]

# ── Generate ───────────────────────────────────────────────────────

def generate_all() -> list[str]:
    """Write all agent config files. Returns list of written paths."""
    written = []
    for cfg in AGENT_CONFIGS:
        path = REPO_ROOT / cfg["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(cfg["content"])
        written.append(str(path.relative_to(REPO_ROOT)))
    return written


def check_all() -> bool:
    """Verify all config files match generated content. Returns True if OK."""
    ok = True
    for cfg in AGENT_CONFIGS:
        path = REPO_ROOT / cfg["path"]
        expected = cfg["content"]
        if not path.exists():
            print(f"MISSING: {cfg['path']} (for {', '.join(cfg['agents'])})")
            ok = False
        elif path.read_text() != expected:
            print(f"STALE: {cfg['path']} (for {', '.join(cfg['agents'])}) — run generate-configs.py")
            ok = False
        else:
            print(f"OK:     {cfg['path']}")
    return ok


# ── Main ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--check" in sys.argv:
        print("Checking agent configs...")
        sys.exit(0 if check_all() else 1)
    else:
        written = generate_all()
        print(f"Generated {len(written)} agent config(s):")
        for w in written:
            print(f"  ✅ {w}")
        print(f"\nDone. Source: {len(REFERENCE_FILES)} reference files, {len(KEY_ENDPOINTS)} key endpoints.")
        print("Run 'python3 generate-configs.py --check' to verify in CI.")