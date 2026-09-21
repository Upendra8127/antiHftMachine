# Support Policy & Channels

Welcome to the **antiHftMachine** support portal. Please review the tiers below to find the appropriate channel for your inquiry.

---

## 1. Support Tiers

| Tier | Purpose | Destination |
| ---- | ------- | ----------- |
| **Tier 1: Questions, Ideas & Strategy** | General Q&A, algorithmic ideas, sentiment analysis discussions, feature brainstorming | [GitHub Discussions](https://github.com/Upendra8127/antiHftMachine/discussions) |
| **Tier 2: Bug Reports & Performance** | Reproducible software defects, parsing errors, UI crashes, memory leaks | [GitHub Issues](https://github.com/Upendra8127/antiHftMachine/issues) |
| **Tier 3: Security Vulnerabilities** | Sensitive vulnerability disclosures, authorization or data leakage bugs | [Private Vulnerability Advisory](https://github.com/Upendra8127/antiHftMachine/security/advisories) |

---

## 2. Self-Service Diagnostics

Before reporting an issue, please execute the self-diagnostic suite:

1. **Verify Backend API Health**:
   ```bash
   curl http://localhost:8000/
   ```
   Expected response: `{"message": "antiHftMachine API is running successfully!"}`

2. **Verify Frontend & Unit Tests**:
   ```bash
   npm test
   ```
   All tests in `tests/*.test.js` should pass with 0 failures.

3. **Check SQLite Database Integrity**:
   Verify that `antiHft.db` has write permissions and tables `signals` and `signal_performance` exist.
