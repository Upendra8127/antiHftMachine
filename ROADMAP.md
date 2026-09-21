# Product Roadmap: antiHftMachine

This living roadmap details the development journey, current capabilities, and planned innovations for the antiHftMachine platform.

---

## Completed Milestones

### Milestone 1: Core Foundation & Prototyping (v1.0.0)
- [x] Initial architecture for NIFTY 500 corporate announcement ingestion.
- [x] Integration of pre-trained financial sentiment transformer (FinBERT).
- [x] Rule-based anti-manipulation heuristics (keyword blacklist, mention density filter).
- [x] Local SQLite persistence layer (`signals` & `signal_performance`).
- [x] Basic React dark-mode dashboard with KPI metrics.

### Milestone 2: Dynamic Entity Recognition & V2 Architecture (v2.0.0)
- [x] Replaced static 500 list with dynamic spaCy Named Entity Recognition (`ORG` extraction).
- [x] Direct source preview hyperlinks (`Read Source →`).
- [x] Multi-arm conglomerate disambiguation with manual inspection flag (`⚠️ See Manually for Clarification`).
- [x] Explicit directional signals: `BUY POSITION`, `SELL POSITION`, `HOLD`.
- [x] End-of-Day (EOD) actual return calculation using historical market data.
- [x] Client-side timeframe filters (1h, 4h, 24h, 7d, 30d).
- [x] OpenSSF & Tier-1 Open Source Governance and automated testing suite.

---

## Current Release: v2.0.0 (Production Candidate)
- [x] Zero-dependency Node.js test runner with CSPRNG Pearson Chi-Square validation.
- [x] Fully automated GitHub Actions matrix (CI, CodeQL, Scorecard, Lighthouse, Stale, Welcome).

---

## Future Horizons

### Horizon 1: Real-Time Broker Webhooks (Q4 2026)
- [ ] Direct integration with Zerodha Kite Connect and Upstox Webhooks.
- [ ] Sub-second low-latency message streaming via WebSocket / Server-Sent Events (SSE).
- [ ] Order book depth analysis to detect institutional iceberg orders.

### Horizon 2: Advanced Deep Learning & Multi-Modal Models (Q1 2027)
- [ ] Fine-tuned domain-specific LoRA adapters on Indian corporate disclosures.
- [ ] Audio transcription of quarterly earnings calls with real-time sentiment scoring.
- [ ] Cross-asset correlation graph neural network (GNN) across NIFTY sectors.

### Horizon 3: Enterprise Cloud & High-Availability (Q2 2027)
- [ ] Distributed Celery + Redis task queue with fault-tolerant workers.
- [ ] TimescaleDB / ClickHouse migration for high-frequency tick data storage.
- [ ] Multi-region automated failover and Prometheus/Grafana monitoring dashboard.
