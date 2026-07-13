# Installation Guide

## Hermes Agent

```bash
# Add the tap
hermes skills tap add amirziveh/tsetmc-skill

# Install the skill
hermes skills install tsetmc

# Use it
skill_view(name="tsetmc")
```

## Claude Code

Open Claude Code in the project root. It auto-reads `CLAUDE.md`.

```bash
cd path/to/tsetmc-skill
claude
# → "I see you're working with TSETMC API. References are in references/"
```

## Cursor

Open the project folder in Cursor. It auto-reads `.cursorrules`.
Ask: *"How do I search for a stock symbol on TSETMC?"*

## OpenCode

OpenCode auto-reads `.opencode.md` from the project root.

## Windsurf

Windsurf auto-reads `.windsurfrules` from the project root.

## GitHub Copilot

Copilot reads `.github/copilot-instructions.md` — no setup needed once the
project is opened.

## Any agent without native config support

Point the agent directly to the markdown files:
```
Read references/api-endpoints.md and references/data-schemas.md
for the complete TSETMC API reference.
```

## Python (any environment, no pip needed)

The stdlib-only client works everywhere:

```bash
# Copy the client
cp templates/python-client.py my_project/

# Edit and use
python3 my_project/tsetmc_client.py
```

## Keeping updated

When `references/*.md` changes, regenerate all agent configs:

```bash
python3 generate-configs.py
# Or check in CI:
python3 generate-configs.py --check
```