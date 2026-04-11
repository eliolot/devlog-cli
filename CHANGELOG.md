 # Changelog

 All notable changes to 'devlog-cli' will be documented in this file.

 The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
 and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Planned: 'add' command to create new log entries
- Planned: 'today' command to view today's notes
- Planned: 'search' command to search notes by keywork
- Planned: 'stats' command to view usage statistics
- Planned: 'export' command to export notes in Markdown or JSON

---

## [0.1.0] - 2026-04-11

### Added
- Initial project structure with src-layout
- 'LogEntry' model with Pydantic v2 validation
- Full test suite with pytest (11 tests, 100% coverage on models)
- Ruff for linting and formatting
- Mypy with strict type checking
- Pre-commit hooks for code quality
- GitHub Actions CI/CD with test matrix on ubuntu and windows
- Professional README with usage examples

[Unreleased]: https://github.com/eliolot/devlog-cli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/eliolot/devlog-cli/releases/tag/v0.1.0
