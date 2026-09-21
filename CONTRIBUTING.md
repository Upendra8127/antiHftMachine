# Contributing to antiHftMachine

Thank you for your interest in contributing to **antiHftMachine**! This document details the guidelines for development, commit standards, and community interaction.

---

## 1. Developer Certificate of Origin (DCO 1.1)
All contributions to this project must be certified under the Developer Certificate of Origin (DCO 1.1).

By adding a `Signed-off-by` line to your commit message, you certify that:
- You authored the code, or
- You have rights to submit the work under the open-source license, or
- It is provided directly by someone who certified it.

Sign off commits using git CLI:
```bash
git commit -s -m "feat(pipeline): add adaptive volatility filter"
```

---

## 2. Conventional Commits 1.0.0
We enforce the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

Commit message format:
```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Allowed Types:
- `feat`: A new user-facing feature or enhancement.
- `fix`: A bug fix.
- `docs`: Documentation-only changes.
- `perf`: A code change that improves performance.
- `test`: Adding missing tests or correcting existing tests.
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `chore`: Maintenance tasks, dependencies, tooling.

---

## 3. Engineering Baseline & Code Standards

### Pure Web & Zero-Dependency Rule
- Client-side libraries and utility logic must strictly avoid heavy runtime dependencies. Use vanilla ES6+, HTML5 Canvas, Web Audio API, and native browser Web APIs.
- Randomness for critical sampling or financial simulations must employ `getCryptoRandom()` backed by CSPRNG entropy (`crypto.getRandomValues`).

### Security & Sanitization
- Never insert raw user-controlled content using `innerHTML` or `dangerouslySetInnerHTML`. Always use sanitized text nodes or React JSX bindings.

---

## 4. Local Development Workflow

1. Clone the repository:
   ```bash
   git clone https://github.com/Upendra8127/antiHftMachine.git
   cd antiHftMachine
   ```

2. Run automated test suite:
   ```bash
   npm test
   ```

3. Code formatting & linting:
   ```bash
   npm run format:check
   npm run lint
   ```

4. Create a topic branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```

5. Commit with DCO sign-off:
   ```bash
   git commit -s -m "feat(sentiment): integrate multi-lingual sentiment heuristics"
   ```

6. Open a Pull Request on GitHub using the PR template.
