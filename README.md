# devlog-cli

> A fast, minimal CLI tool to keep a developer journal from your terminal.

[![Tests](https://github.com/TUO_USERNAME/devlog-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/eliolot/devlog-cli/actions/workflows/tests.yml)
[![Lint](https://github.com/TUO_USERNAME/devlog-cli/actions/workflows/lint.yml/badge.svg)](https://github.com/eliolot/devlog-cli/actions/workflows/lint.yml)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is devlog?

`devlog` lets you capture what you're working on without leaving the terminal.
Notes are stored locally in a JSON file in your home directory — no cloud,
no account, no tracking.

```bash
devlog add "fixed the async race condition in the parser" --tag python --tag bugfix
devlog today
devlog search "async"
devlog stats
devlog export --format md > weekly-report.md
```

---

## Installation

**Requirements**: Python 3.13+

```bash
pip install devlog-cli
```

Or install from source:

```bash
git clone https://github.com/eliolot/devlog-cli.git
cd devlog-cli
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -e ".[dev]"
pre-commit install
```

---

## Usage

### Add a note
```bash
devlog add "what you did or learned"
devlog add "studied design patterns" --tag python --tag architecture
```

### View today's notes
```bash
devlog today
```

### Search notes
```bash
devlog search "keyword"
```

### View stats
```bash
devlog stats
```

### Export notes
```bash
devlog export --format md > report.md
devlog export --format json > backup.json
```

---

## Development

### Setup

```bash
git clone https://github.com/eliolot/devlog-cli.git
cd devlog-cli
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -e ".[dev]"
pre-commit install
```

### Run tests

```bash
pytest
```

### Run linter

```bash
ruff check .
ruff format .
```

---

## License

MIT © eliolot
