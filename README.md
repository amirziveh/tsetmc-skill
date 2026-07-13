[![GitHub](https://img.shields.io/badge/agent-hermes_%7C_claude_%7C_cursor_%7C_opencode_%7C_copilot_%7C_windsurf-blue)](https://github.com/amirziveh/tsetmc-skill)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/amirziveh/tsetmc-skill)](https://github.com/amirziveh/tsetmc-skill/commits)

# TSETMC Skill — Tehran Stock Exchange Data for AI Agents

A universal, reverse-engineered API reference for the Tehran Stock Exchange (TSETMC / tsetmc.com). **Works natively with every major AI coding agent** — no plugins, no SDKs, just markdown.

Covers **three API surfaces** with ~50+ endpoints for instrument data, price history, indices, client types, order books, shareholders, messages, and more.

## What's inside

| Directory | Contents | Any agent? |
|-----------|----------|-----------|
| `references/` | Full API endpoint catalog, data schemas, field dictionary, flow/code tables | ✅ Yes — plain markdown |
| `templates/` | Python client (stdlib-only), usage guides for pytse-client & tsetmc packages | ✅ Yes — plain code |
| `SKILL.md` | Hermes Agent skill (installable via `hermes skills install`) | ✅ Hermes |
| `CLAUDE.md` | Claude Code project hook | ✅ Claude Code |
| `.cursorrules` | Cursor AI project hook | ✅ Cursor |
| `.opencode.md` | OpenCode project hook | ✅ OpenCode |
| `.windsurfrules` | Windsurf project hook | ✅ Windsurf |
| `.github/copilot-instructions.md` | GitHub Copilot project hook | ✅ Copilot |
| `generate-configs.py` | Auto-generates all agent hooks from references/ | ✅ Developer tool |

## Quick start

### Any AI agent
Point your agent to this repo's root. It will automatically pick up the relevant config file and gain access to all TSETMC API knowledge.

### Hermes Agent
```bash
hermes skills tap add amirziveh/tsetmc-skill
hermes skills install tsetmc
```

### Python (any environment)
```python
from tsetmc_client import TsetmcClient  # or copy templates/python-client.py

client = TsetmcClient()
results = client.search_symbol("فولاد")
info = client.instrument_info(results[0]["insCode"])
```

## API surfaces

| Surface | Base URL | Format | Status |
|---------|----------|--------|--------|
| **CDN REST API** | `https://cdn.tsetmc.com/api/` | JSON | ✅ Active |
| **Old TSEv2** | `http://old.tsetmc.com/tsev2/data/` | CSV/delimited | ✅ Active |
| **ParTree HTML** | `http://old.tsetmc.com/Loader.aspx` | HTML + JS | ✅ Active |
| **Members Chart** | `https://members.tsetmc.com/tsev2/chart/data/` | CSV | ✅ Active |
| **Service** | `http://service.tsetmc.com/tsev2/data/` | Text | ✅ Active |

## License

MIT — free to use, modify, and distribute. All data is from public APIs of the Tehran Securities Exchange Technology Management Co.