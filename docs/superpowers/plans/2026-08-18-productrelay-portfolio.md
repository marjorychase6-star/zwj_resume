# ProductRelay Featured Portfolio Project Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the published ProductRelay project as the first and visually featured project on the existing personal portfolio, using the verified real product screenshot and public GitHub URL.

**Architecture:** Extend the existing single-file portfolio with one modifier class instead of redesigning the project system. Reuse the product repository's reviewed screenshot as a static asset, add a deterministic HTML/CSS contract test, and gate the final portfolio push on responsive browser review and user approval.

**Tech Stack:** Static HTML/CSS/JavaScript, Python `unittest`, browser responsive inspection, Git/GitHub.

## Global Constraints

- Portfolio repository root: `/Users/zevvv/vibe_coding/my job/zwj_resume_repo`.
- This plan starts only after the ProductRelay publication plan has produced a verified public repository and final screenshot.
- Preserve all existing project content and links; insert ProductRelay before PromptVault and shift the existing order without rewriting it.
- Use `https://github.com/marjorychase6-star/product-relay` exactly.
- Use the exact reviewed screenshot bytes from the product repository; do not substitute a concept image.
- Do not push until the user approves the local responsive preview.
- Never force-push or rewrite the portfolio remote history.

---

## Task 1: Add failing portfolio structure and asset tests

**Files:**
- Modify: `.gitignore`
- Create: `tests/test_productrelay_portfolio.py`

- [ ] **Step 1: Ignore local operating-system and preview artifacts**

Append:

```gitignore
.DS_Store
.superpowers/
```

- [ ] **Step 2: Create a dependency-free portfolio contract test**

Create `tests/test_productrelay_portfolio.py`:

```python
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
IMAGE = ROOT / "static" / "images" / "projects" / "productrelay-workspace.webp"
REPOSITORY_URL = "https://github.com/marjorychase6-star/product-relay"


class ProductRelayPortfolioTest(unittest.TestCase):
    def test_productrelay_is_the_first_project(self) -> None:
        projects = HTML.index('id="projects"')
        productrelay = HTML.index("ProductRelay — AI Product Execution Partner", projects)
        promptvault = HTML.index("PromptVault", projects)
        self.assertLess(productrelay, promptvault)

    def test_featured_card_has_real_asset_and_safe_link(self) -> None:
        self.assertIn('class="project-card project-card--featured"', HTML)
        self.assertIn('src="static/images/projects/productrelay-workspace.webp"', HTML)
        self.assertIn('alt="ProductRelay workspace with lifecycle navigation and AI assistant"', HTML)
        self.assertIn(f'href="{REPOSITORY_URL}"', HTML)
        self.assertIn('target="_blank" rel="noopener noreferrer"', HTML)
        self.assertTrue(IMAGE.is_file())

    def test_featured_layout_has_desktop_and_mobile_rules(self) -> None:
        self.assertIn(".project-card--featured", HTML)
        self.assertIn("grid-template-columns: minmax(0, 3fr) minmax(18rem, 2fr)", HTML)
        mobile = HTML.index("@media (max-width: 768px)")
        self.assertIn(".project-card--featured", HTML[mobile:])
        self.assertIn("grid-template-columns: 1fr", HTML[mobile:])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the contract test and confirm the expected failures**

Run:

```bash
python -m unittest tests.test_productrelay_portfolio -v
```

Expected: tests fail because the ProductRelay card, image, and modifier CSS do not exist.

- [ ] **Step 4: Commit the red test and ignore rules**

```bash
git add .gitignore tests/test_productrelay_portfolio.py
git commit -m "test(portfolio): define ProductRelay featured card contract"
```

## Task 2: Add the real screenshot and featured ProductRelay card

**Files:**
- Create: `static/images/projects/productrelay-workspace.webp`
- Modify: `index.html`

- [ ] **Step 1: Copy and verify the reviewed product screenshot**

Copy from:

```text
/Users/zevvv/vibe_coding/Hermes/pm-hermes/docs/assets/productrelay-workspace.webp
```

to:

```text
/Users/zevvv/vibe_coding/my job/zwj_resume_repo/static/images/projects/productrelay-workspace.webp
```

Then compare SHA-256 hashes:

```bash
shasum -a 256 "/Users/zevvv/vibe_coding/Hermes/pm-hermes/docs/assets/productrelay-workspace.webp" static/images/projects/productrelay-workspace.webp
```

Expected: both hashes are identical.

- [ ] **Step 2: Add the featured desktop layout**

Place these rules alongside the existing project-card rules in `index.html`:

```css
.project-card--featured {
    display: grid;
    grid-template-columns: minmax(0, 3fr) minmax(18rem, 2fr);
    align-items: stretch;
}

.project-card--featured .project-image {
    height: auto;
    min-height: 32rem;
}

.project-card--featured .project-image img {
    height: 100%;
    object-fit: cover;
    object-position: center;
}

.project-card--featured .project-body {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
```

Inside the existing `@media (max-width: 768px)` block, add:

```css
.project-card--featured {
    grid-template-columns: 1fr;
}

.project-card--featured .project-image {
    min-height: 0;
    aspect-ratio: 16 / 10;
}
```

- [ ] **Step 3: Insert ProductRelay before the existing PromptVault card**

Use the existing project-card child class names and this content:

```html
<article class="project-card project-card--featured">
    <div class="project-image">
        <img src="static/images/projects/productrelay-workspace.webp"
             alt="ProductRelay workspace with lifecycle navigation and AI assistant">
    </div>
    <div class="project-body">
        <h3 class="project-title">ProductRelay — AI Product Execution Partner</h3>
        <p class="project-description">面向独立产品经理的本地 AI 产品工作台，把资料、需求、PRD、原型和交付串联为可追踪流程。</p>
        <ul class="project-features">
            <li>从真实资料到结构化交付的完整产品生命周期</li>
            <li>手动确认与自动执行两种 AI 协作模式</li>
            <li>有来源、有版本、可审计的 AI 操作</li>
            <li>本地数据存储与系统钥匙串密钥管理</li>
        </ul>
        <a class="project-link"
           href="https://github.com/marjorychase6-star/product-relay"
           target="_blank" rel="noopener noreferrer">View on GitHub</a>
    </div>
</article>
```

Do not change the content or order inside the existing cards.

- [ ] **Step 4: Run the structural tests**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit the featured card**

```bash
git add index.html static/images/projects/productrelay-workspace.webp
git commit -m "feat(portfolio): feature ProductRelay as the lead project"
```

## Task 3: Perform real responsive browser acceptance

**Files:**
- Modify: `index.html` only if a tested layout defect is found.

- [ ] **Step 1: Start the local static preview**

Run:

```bash
python -m http.server 4173 --directory "/Users/zevvv/vibe_coding/my job/zwj_resume_repo"
```

Open `http://localhost:4173/#projects` in the in-app browser.

- [ ] **Step 2: Inspect the required widths**

At 320, 375, 768, 1100, and 1440 px widths, verify:

- ProductRelay is the first card;
- 1100/1440 px use the intended 60/40 screenshot-text layout;
- 320/375/768 px stack screenshot above text;
- there is no horizontal overflow, clipped button, overlapping copy, or unreadable screenshot;
- existing project cards, navigation, and interactions remain intact.

Use browser measurements to confirm `document.documentElement.scrollWidth <= window.innerWidth` at each required width.

- [ ] **Step 3: Verify semantics and the external link**

Confirm the screenshot has the exact descriptive alt text, the GitHub action is keyboard-focusable, and opening it resolves to the public ProductRelay repository in a new tab without affecting the portfolio tab.

- [ ] **Step 4: Re-run automated checks after any visual fix**

```bash
python -m unittest discover -s tests -v
git diff --check
git status --short
```

Expected: tests pass, no whitespace errors, and only deliberate portfolio changes are present. If a CSS fix was required, commit it as:

```bash
git add index.html tests/test_productrelay_portfolio.py
git commit -m "fix(portfolio): refine ProductRelay responsive layout"
```

- [ ] **Step 5: Present the local preview for user approval**

Show the user the local page and a concise summary of desktop/mobile acceptance. Stop here until the user explicitly approves publishing the portfolio update.

## Task 4: Push the approved portfolio update and verify publication

**Files:**
- External state: `https://github.com/marjorychase6-star/zwj_resume`

- [ ] **Step 1: Confirm remote, branch, commits, and user approval**

```bash
git remote -v
git status --short
git log --oneline origin/main..main
```

Expected: `origin` is `https://github.com/marjorychase6-star/zwj_resume.git`, the worktree is clean, ProductRelay commits are visible, and the user has approved the local preview.

- [ ] **Step 2: Push normally**

```bash
git push origin main
```

Expected: a normal fast-forward push succeeds; no force option is used.

- [ ] **Step 3: Verify remote content and hosted page**

```bash
gh repo view marjorychase6-star/zwj_resume --json url,defaultBranchRef
gh api repos/marjorychase6-star/zwj_resume/pages
```

Open the returned Pages URL, wait for the new commit to deploy if needed, and verify the same first-card layout, image, and public ProductRelay link. Report both final URLs and the deployed commit SHA.
