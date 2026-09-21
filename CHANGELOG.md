# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-09-21

### Added
- **Dynamic Entity Extraction**: Integrated spaCy Named Entity Recognition (`en_core_web_sm`) to dynamically detect organizations in incoming headlines without relying on a static ticker list.
- **Conglomerate Disambiguation**: Added automatic context heuristic with `[See Manually for Clarification]` warning badge for multi-arm groups (Adani, Tata, Bajaj, Birla, Mahindra, Godrej).
- **Explicit Signal Actionability**: Transformed raw sentiment labels into explicit `BUY POSITION`, `SELL POSITION`, and `HOLD` actionable guidance.
- **Source Linkage**: Added direct hyperlink previews (`Read Source →`) for every detected alert.
- **Timeframe Filtering**: Implemented UI filters for 1-hour, 4-hour, 24-hour, 7-day, and 30-day historical exploration.
- **OpenSSF & Enterprise Governance Suite**: Added `GOVERNANCE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `ROADMAP.md`, and `CITATION.cff`.
- **CSPRNG Fairness & Automated Testing**: Added `frontend/src/utils/crypto.js` and Node.js native test suite with a 10,000-spin Pearson Chi-Square test.
- **GitHub Automation Suite**: Complete suite of issue forms, PR templates, Dependabot, Discussions templates, and GitHub Actions workflows (CI, CodeQL, Scorecard, Lighthouse, Stale, Welcome).

### Changed
- Refactored backend ingestion loop to prevent GIL contention and optimize SQLite database concurrency using WAL mode.
- Upgraded frontend to modern dark glassmorphic responsive design.

### Fixed
- Fixed Python bytecode caching corruption during unexpected process terminations.
- Fixed CORS headers and host binding to support both localhost and remote container networks.

---

## [1.0.0] - 2026-07-01

### Added
- Initial proof-of-concept pipeline for NIFTY 500 corporate announcements.
- Integrated HuggingFace FinBERT sentiment classifier.
- Pre-sentiment anti-manipulation filtering for spam phrases and keyword density.
- SQLite persistence layer for `signals` and `signal_performance` tables.
- React frontend dashboard with global KPI cards and confidence/impact sliders.
