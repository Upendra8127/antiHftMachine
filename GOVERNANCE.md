# Project Governance & Decision-Making Model

The **antiHftMachine** project adheres to an open-source governance model aligned with the guidelines of the **Cloud Native Computing Foundation (CNCF)** and the **Linux Foundation**.

---

## 1. Principles
- **Openness**: The project is open to participation, contribution, and feedback from any individual or organization.
- **Transparency**: Discussions, roadmap prioritization, issues, and code reviews occur in public repositories.
- **Meritocracy**: Influence and leadership are earned through sustained, high-quality technical and community contributions.

---

## 2. Roles and Responsibilities

### Contributors
Contributors submit issues, pull requests, participate in discussions, and improve documentation.
- Must sign off on all commits using Developer Certificate of Origin (DCO 1.1).
- Adhere to the Contributor Covenant Code of Conduct.

### Maintainers
Maintainers possess write and release permissions for the repository.
- **Project Lead / Core Maintainer**: `@Upendra8127`
- Responsibilities:
  - Review and merge pull requests adhering to quality and security standards.
  - Coordinate vulnerability remediation per `SECURITY.md`.
  - Maintain the release roadmap and publish SemVer releases.

---

## 3. Decision-Making & Lazy Consensus
To balance agility with consensus:
- **Routine Changes**: Bug fixes, docs, and minor optimizations proceed with the approval of at least one maintainer.
- **Lazy Consensus**: For non-breaking technical decisions, a proposal is posted in GitHub Discussions or a PR. If no objections are raised within **72 hours**, lazy consensus is achieved, and the proposal is adopted.
- **Major Architectural Changes (RFC Process)**:
  - Major shifts in pipeline architecture, machine learning models, or data models require an RFC (Request for Comments) issue template.
  - Discussion period: Minimum 7 days.
  - Maintainers vote with a simple majority required for adoption.

---

## 4. Conflict Resolution
In the event of unresolved technical disagreements:
1. Contributors seek common ground via technical benchmarks and objective data.
2. If disagreement persists, the Core Maintainer (`@Upendra8127`) serves as final arbiter.
