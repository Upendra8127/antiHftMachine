# Security Policy

The **antiHftMachine** team takes the security of our quantitative trading infrastructure and data processing pipelines seriously. We follow the OpenSSF (Open Source Security Foundation) Coordinated Vulnerability Disclosure (CVD) best practices.

---

## 1. Supported Versions

Only the latest release version on the `main` branch receives active security patches.

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | :white_check_mark: |
| 1.x     | :x:                |
| < 1.0   | :x:                |

---

## 2. Reporting a Vulnerability

Please **DO NOT** report security vulnerabilities via public GitHub issues, discussions, or social media.

Instead, submit reports using one of the following methods:

1. **GitHub Private Vulnerability Reporting (Preferred)**:
   Navigate to the [Security Tab -> Report a Vulnerability](https://github.com/Upendra8127/antiHftMachine/security/advisories/new) on the repository.
2. **Encrypted / Direct Email**:
   Send details to [upendrayadav8127@gmail.com](mailto:upendrayadav8127@gmail.com) with the subject `[SECURITY] antiHftMachine Vulnerability Report`.

---

## 3. Vulnerability Response SLAs

We commit to the following response timeline:

| Milestone                    | SLA Commitment       |
| ---------------------------- | -------------------- |
| **Initial Acknowledgment**   | **< 24 hours**       |
| **Triage & Validation**      | **< 48 hours**       |
| **Patch & Remediation**      | **< 7 days**         |
| **Public Advisory Release**  | Coordinated post-fix |

---

## 4. Scope & Safe Harbor

### In Scope
- Remote code execution in backend pipeline.
- Cross-Site Scripting (XSS) or DOM injection in frontend UI.
- Data exfiltration or tampering of intraday financial signals.
- Insecure randomness or predictability in CSPRNG operations.
- Dependency supply-chain compromises.

### Safe Harbor
Activities conducted in good faith under this policy are considered authorized, and we will not pursue legal action against security researchers acting in compliance with this disclosure framework.
