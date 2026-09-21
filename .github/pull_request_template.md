## Pull Request Description

### Summary of Changes
<!-- Provide a clear, technical explanation of what was changed and why -->

---

## Type of Change
- [ ] `feat`: New feature or capability
- [ ] `fix`: Bug fix
- [ ] `perf`: Performance optimization
- [ ] `refactor`: Code refactoring without functional changes
- [ ] `docs`: Documentation updates
- [ ] `test`: Adding or correcting tests
- [ ] `chore`: Maintenance, CI, or dependency updates

---

## Contributor Verification & Compliance Checklist

### 1. Developer Certificate of Origin (DCO 1.1) & Commits
- [ ] All commits are signed off with `git commit -s` (DCO 1.1 compliant).
- [ ] Pull Request title adheres to the **Conventional Commits 1.0.0** format (e.g., `feat(nlp): add sector entity disambiguation`).

### 2. Testing & Quality Baseline
- [ ] Automated test suite runs with zero errors: `npm test`.
- [ ] New functionality includes corresponding unit or statistical tests.
- [ ] Code adheres to `.editorconfig` formatting and ESLint standards.

### 3. Cross-Browser & Performance Verification
- [ ] Verified on Chrome / Chromium.
- [ ] Verified on Firefox.
- [ ] Verified on Edge / Safari.
- [ ] Rendering performance verified (solid 60 FPS, no layout thrashing).
- [ ] Memory footprint verified (< 15MB client-side heap growth).
- [ ] Zero runtime dependencies maintained on the client side.
- [ ] Accessibility: WCAG AA contrast and keyboard navigability verified.
