# ProductRelay Brand Migration and Public Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the product to ProductRelay, preserve compatibility with existing local data, create a safe public-release artifact, capture a real product screenshot, and publish the repository at `https://github.com/marjorychase6-star/product-relay`.

**Architecture:** Treat branding as a user-facing boundary instead of a whole-repository text replacement. Rename distribution metadata, console entry points, active UI copy, and current documentation while preserving the internal `pm` package, persisted identifiers, database format, and the vendored `third_party/hermes_agent` snapshot. Add release checks that block secrets, local data, personal paths, or missing attribution before any remote repository is created.

**Tech Stack:** Python 3.11+, Click, pytest, Ruff, React, TypeScript, Vitest, Vite, GitHub CLI, Pillow/WebP.

## Global Constraints

- Product repository root: `/Users/zevvv/vibe_coding/Hermes/pm-hermes`.
- Preserve the user's modified `.DS_Store`; never stage, overwrite, or delete it.
- Do not mechanically replace text inside `third_party/hermes_agent`.
- Keep the Python import package `pm`, database schema, WebSocket command protocol, MIME types, UUID namespaces, database filename, and existing data format unchanged.
- The new public commands are `product-relay`, `product-relay-ui`, and `product-relay-server`; do not retain old command aliases.
- Prefer `PRODUCT_RELAY_DATA_DIR`; keep `PM_HERMES_DATA_DIR` as a documented compatibility fallback.
- Never create the GitHub repository until every local quality and security gate passes.
- Never force-push or rewrite existing remote history.

---

## Task 1: Lock the ProductRelay compatibility contract with failing tests

**Files:**
- Create: `tests/test_product_brand.py`
- Modify: `tests/e2e/test_clean_install.py`
- Modify: `tests/test_app_context.py`

- [ ] **Step 1: Add a focused brand contract test**

Create `tests/test_product_brand.py` with assertions for package metadata, all three console scripts, current user-facing source files, and intentional compatibility identifiers:

```python
from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
VISIBLE_FILES = (
    ROOT / "README.md",
    ROOT / "pm" / "cli.py",
    ROOT / "pm" / "services" / "assistant_context.py",
    ROOT / "ui" / "webapp" / "src" / "app" / "AppShell.tsx",
    ROOT / "ui" / "webapp" / "src" / "features" / "onboarding" / "Onboarding.tsx",
)


def test_distribution_and_public_commands_use_productrelay() -> None:
    assert PYPROJECT["project"]["name"] == "product-relay"
    assert set(PYPROJECT["project"]["scripts"]) == {
        "product-relay",
        "product-relay-ui",
        "product-relay-server",
    }


def test_current_user_facing_sources_use_productrelay() -> None:
    for path in VISIBLE_FILES:
        content = path.read_text(encoding="utf-8")
        assert "ProductRelay" in content, path
        assert "pm-hermes" not in content, path


def test_stable_internal_boundaries_are_not_renamed() -> None:
    app_context = (ROOT / "pm" / "app_context.py").read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'database=data / "pm-hermes.db"' in app_context
    assert '"pm"' in pyproject
    assert '"third_party/hermes_agent"' in pyproject
```

- [ ] **Step 2: Update the clean-install entry-point expectation**

In `tests/e2e/test_clean_install.py`, replace the old subset assertion with the exact public command set:

```python
assert set(scripts) == {
    "product-relay",
    "product-relay-ui",
    "product-relay-server",
}
```

Update the README environment-variable assertion so it requires both the preferred and compatibility names:

```python
assert "PRODUCT_RELAY_DATA_DIR" in readme
assert "PM_HERMES_DATA_DIR" in readme
```

- [ ] **Step 3: Add preferred and legacy data-root tests**

Add to `tests/test_app_context.py`:

```python
def test_productrelay_data_dir_is_preferred(monkeypatch, tmp_path) -> None:
    preferred = tmp_path / "preferred"
    legacy = tmp_path / "legacy"
    monkeypatch.setenv("PRODUCT_RELAY_DATA_DIR", str(preferred))
    monkeypatch.setenv("PM_HERMES_DATA_DIR", str(legacy))
    assert AppPaths.from_environment().data == preferred.resolve()


def test_legacy_data_dir_remains_supported(monkeypatch, tmp_path) -> None:
    legacy = tmp_path / "legacy"
    monkeypatch.delenv("PRODUCT_RELAY_DATA_DIR", raising=False)
    monkeypatch.setenv("PM_HERMES_DATA_DIR", str(legacy))
    assert AppPaths.from_environment().data == legacy.resolve()
```

- [ ] **Step 4: Run the focused tests and confirm they fail for the intended reasons**

Run:

```bash
python -m pytest tests/test_product_brand.py tests/test_app_context.py tests/e2e/test_clean_install.py -q
```

Expected: failures mention the old distribution name, missing ProductRelay commands/copy, and unsupported preferred data-root variable—not import or syntax errors.

- [ ] **Step 5: Commit the red tests**

```bash
git add tests/test_product_brand.py tests/test_app_context.py tests/e2e/test_clean_install.py
git commit -m "test(brand): define ProductRelay release contract"
```

## Task 2: Rename distribution metadata, CLI, and the preferred data-root variable

**Files:**
- Modify: `pyproject.toml`
- Modify: `pm/__init__.py`
- Modify: `pm/cli.py`
- Modify: `pm/app_context.py`
- Create: `LICENSE`

- [ ] **Step 1: Update package metadata and console scripts**

Use this public package contract in `pyproject.toml`:

```toml
[project]
name = "product-relay"
description = "A local-first AI product execution partner for independent product managers."
license = "MIT"

[project.scripts]
product-relay = "pm.cli:main"
product-relay-ui = "ui.app:run"
product-relay-server = "pm.transport.websocket:main"
```

Keep the current version, dependencies, `pm` wheel package, and `third_party/hermes_agent` force-include unchanged.

- [ ] **Step 2: Rename CLI-facing text**

Update `pm/__init__.py` and `pm/cli.py` so help and `info` output use:

```text
ProductRelay <version>
Desktop workspace: product-relay-ui
```

The full-product launch hint must reference `product-relay-ui`.

- [ ] **Step 3: Add the preferred environment variable without breaking existing data**

Change `AppPaths.from_environment()` in `pm/app_context.py` to resolve explicit roots in this order:

```python
configured = os.environ.get("PRODUCT_RELAY_DATA_DIR") or os.environ.get(
    "PM_HERMES_DATA_DIR"
)
```

Keep the existing default platform data path and `pm-hermes.db` filename so an in-place upgrade continues to find existing projects. Explain that those are compatibility identifiers in the architecture documentation rather than silently migrating user data.

- [ ] **Step 4: Add the root MIT license**

Create `LICENSE` with the standard MIT text and:

```text
Copyright (c) 2026 Zevvv
```

Do not modify `third_party/hermes_agent/LICENSE`.

- [ ] **Step 5: Run the focused backend contract tests**

Run:

```bash
python -m pytest tests/test_product_brand.py tests/test_app_context.py tests/e2e/test_clean_install.py -q
```

Expected: package, command, and environment-variable tests pass; visible-copy assertions may still fail until Task 3.

- [ ] **Step 6: Commit the package and compatibility migration**

```bash
git add pyproject.toml pm/__init__.py pm/cli.py pm/app_context.py LICENSE
git commit -m "feat(brand): rename package and CLI to ProductRelay"
```

## Task 3: Rename active product UI and assistant messaging

**Files:**
- Modify: `ui/webapp/src/app/AppShell.tsx`
- Modify: `ui/webapp/src/app/AppShell.test.tsx`
- Modify: `ui/webapp/src/features/onboarding/Onboarding.tsx`
- Modify: `ui/webapp/src/features/onboarding/Onboarding.test.tsx`
- Modify: `pm/services/assistant_context.py`
- Modify: `pm/services/settings.py`
- Modify: `pm/transport/websocket.py`

- [ ] **Step 1: Add visible-brand UI assertions**

Extend the existing component tests so the rendered shell and onboarding screen contain `ProductRelay` and do not contain `pm-hermes`:

```ts
expect(screen.getByText("ProductRelay")).toBeInTheDocument()
expect(screen.queryByText(/pm-hermes/i)).not.toBeInTheDocument()
```

Use the component's existing render helpers and provider wrappers rather than creating a second test harness.

- [ ] **Step 2: Run the UI tests to establish the red state**

Run:

```bash
npm --prefix ui/webapp test -- --run src/app/AppShell.test.tsx src/features/onboarding/Onboarding.test.tsx
```

Expected: assertions fail because the current UI still renders the old name.

- [ ] **Step 3: Replace current product-facing copy**

Update only ProductRelay-owned strings:

```text
pm-hermes                     -> ProductRelay
pm-hermes product assistant   -> ProductRelay product assistant
pm-hermes connection test     -> ProductRelay connection test
```

Update WebSocket startup logging to `ProductRelay server ...`. Preserve protocol values, session identifiers, export MIME types, and any migration/compatibility explanations.

- [ ] **Step 4: Run focused UI and backend tests**

Run:

```bash
npm --prefix ui/webapp test -- --run src/app/AppShell.test.tsx src/features/onboarding/Onboarding.test.tsx
python -m pytest tests/test_product_brand.py tests/services/test_assistant_service.py tests/transport/test_assistant_websocket.py -q
```

Expected: all focused tests pass.

- [ ] **Step 5: Commit the active product copy**

```bash
git add ui/webapp/src/app/AppShell.tsx ui/webapp/src/app/AppShell.test.tsx ui/webapp/src/features/onboarding/Onboarding.tsx ui/webapp/src/features/onboarding/Onboarding.test.tsx pm/services/assistant_context.py pm/services/settings.py pm/transport/websocket.py
git commit -m "feat(ui): apply ProductRelay brand across active surfaces"
```

## Task 4: Rewrite current documentation for public visitors

**Files:**
- Modify: `README.md`
- Modify: `docs/architecture.md`
- Modify: `docs/user-guide.md`
- Modify: `docs/hermes-upstream.md`
- Modify: `docs/PLAN.md`

- [ ] **Step 1: Replace the README with the public ProductRelay structure**

The first screen must use this content order:

```markdown
# ProductRelay

> Your AI partner from insight to delivery.

ProductRelay is a local-first AI product execution partner for independent product managers.

![ProductRelay workspace](docs/assets/productrelay-workspace.webp)

## What it does
## Workflow
## AI collaboration modes
## Security and local data
## Requirements
## Install and run
## Hermes runtime attribution
## Current limitations
## License
```

Document the three new commands. Use `PRODUCT_RELAY_DATA_DIR` in normal examples and identify `PM_HERMES_DATA_DIR` as the compatibility fallback for existing installations. Do not claim cloud sync, collaboration, or functionality that is not implemented.

- [ ] **Step 2: Update maintained documentation**

Use `ProductRelay` in titles and current descriptions. In `docs/architecture.md`, include a compatibility note equivalent to:

```markdown
`pm` imports, `pm-hermes.db`, persisted MIME/UUID identifiers, and the legacy data-directory environment variable remain stable implementation identifiers so existing local workspaces continue to open.
```

Keep `Hermes` names intact wherever the text refers to the upstream harness or its vendored path.

- [ ] **Step 3: Verify current documentation and attribution**

Run:

```bash
python -m pytest tests/test_product_brand.py tests/e2e/test_clean_install.py tests/runtime/test_hermes_vendor.py -q
```

Expected: all tests pass, including root docs, package commands, and Hermes provenance.

- [ ] **Step 4: Commit public documentation**

```bash
git add README.md docs/architecture.md docs/user-guide.md docs/hermes-upstream.md docs/PLAN.md
git commit -m "docs: present ProductRelay for public release"
```

## Task 5: Add a reproducible public-release safety gate

**Files:**
- Modify: `.gitignore`
- Create: `scripts/audit_public_release.py`
- Create: `tests/test_public_release.py`

- [ ] **Step 1: Expand ignored local-only files**

Add these entries without removing existing data exclusions:

```gitignore
.DS_Store
.idea/
.vscode/
.pytest_cache/
.ruff_cache/
```

- [ ] **Step 2: Write pure audit functions and failing tests first**

Create tests for forbidden tracked paths, sensitive content, personal absolute paths, and required release files. The public functions must accept explicit path lists/text mappings so tests use temporary fixtures instead of mutating Git state:

```python
def audit_paths(paths: list[str]) -> list[str]: ...
def audit_texts(texts: dict[str, str]) -> list[str]: ...
def audit_repository(root: Path) -> list[str]: ...
```

Required blocked examples:

```python
FORBIDDEN_PATHS = (
    ".DS_Store",
    ".env",
    "workspace.db",
    "attachments/private.pdf",
    "backups/backup.db",
    "exports/project.zip",
)
FORBIDDEN_TEXT = (
    "-----BEGIN PRIVATE KEY-----",
    "/Users/zevvv/private",
    "sk-live_abcdefghijklmnopqrstuvwxyz123456",
)
```

- [ ] **Step 3: Run the new tests and confirm the module is missing**

Run:

```bash
python -m pytest tests/test_public_release.py -q
```

Expected: collection fails because `scripts.audit_public_release` does not exist.

- [ ] **Step 4: Implement the audit command**

The script must:

1. get tracked paths with `git ls-files -z`;
2. reject tracked databases, keys, env files, attachments, backups, exports, logs, caches, IDE metadata, and `.DS_Store`;
3. inspect text files outside `third_party/` for private-key headers and personal absolute paths;
4. inspect non-test, non-historical product-owned text for live-key-shaped values;
5. require root `LICENSE`, `third_party/hermes_agent/LICENSE`, and `third_party/hermes_agent/UPSTREAM.md`;
6. print every finding and exit non-zero if any finding exists.

Use compiled regexes with conservative live-key shapes; do not flag documented variable names or empty placeholders merely because they contain `API_KEY`.

- [ ] **Step 5: Run tests and the real repository audit**

Run:

```bash
python -m pytest tests/test_public_release.py -q
python scripts/audit_public_release.py
```

Expected: tests pass and the real audit prints `Public release audit passed.`. If it reports tracked local files or sensitive text, remove those items from the release content and rerun; never weaken a rule to hide a real finding.

- [ ] **Step 6: Commit the release gate**

```bash
git add .gitignore scripts/audit_public_release.py tests/test_public_release.py
git commit -m "chore(release): add public repository safety audit"
```

## Task 6: Capture and integrate the real ProductRelay workspace screenshot

**Files:**
- Create: `docs/assets/productrelay-workspace.webp`
- Modify: `README.md`

- [ ] **Step 1: Build and start a clean demonstration workspace**

Use an isolated temporary data root and never use the user's real workspace:

```bash
npm --prefix ui/webapp run build
PRODUCT_RELAY_DATA_DIR=/private/tmp/productrelay-demo product-relay-server
```

If the packaged command is not installed in the current environment, run the repository's documented development server entry with the same environment variable.

- [ ] **Step 2: Prepare the screenshot scene in the real browser UI**

Create the built-in complete sample project, open its product overview or structured artifact, keep the lifecycle navigation visible, open the right-side AI assistant, and ensure the manual/automatic mode control is visible. Use only synthetic sample content. Confirm no API key, local path, notification, or developer console appears.

- [ ] **Step 3: Capture and convert the image**

Capture at approximately 1600×1000 CSS pixels and save the final image as `docs/assets/productrelay-workspace.webp`. Preserve the full three-column workspace, crop browser chrome, and use a WebP quality setting that keeps interface text crisp.

- [ ] **Step 4: Verify dimensions, format, and size**

Run:

```bash
python -c "from pathlib import Path; from PIL import Image; p=Path('docs/assets/productrelay-workspace.webp'); im=Image.open(p); print(im.format, im.size, p.stat().st_size)"
```

Expected: `WEBP`, a ratio near 16:10, readable UI text, and a file small enough for a portfolio page (target under 600 KB; hard ceiling 1 MB).

- [ ] **Step 5: Verify README rendering and audit the binary path**

Confirm the README image path resolves locally, visually inspect the image, and rerun:

```bash
python scripts/audit_public_release.py
```

Expected: audit passes and the screenshot contains only demo content.

- [ ] **Step 6: Commit the screenshot**

```bash
git add docs/assets/productrelay-workspace.webp README.md
git commit -m "docs: add ProductRelay workspace preview"
```

## Task 7: Run the complete local release candidate gate

**Files:**
- Verify only; modify a failing source and its test together if the gate finds a defect.

- [ ] **Step 1: Run all backend checks**

```bash
python -m pytest -q
python -m ruff check pm ui tests scripts
```

Expected: all tests pass and Ruff reports no errors.

- [ ] **Step 2: Run all frontend checks**

```bash
npm --prefix ui/webapp test -- --run
npm --prefix ui/webapp run lint
npm --prefix ui/webapp run build
```

Expected: all Vitest tests, lint, type checks, and production build pass.

- [ ] **Step 3: Validate the distributable wheel and console entry points**

```bash
python -m pytest tests/e2e/test_clean_install.py -q
product-relay --help
product-relay info
```

Expected: clean-install checks pass; both CLI calls exit zero and display ProductRelay commands/copy.

- [ ] **Step 4: Re-run public audit and inspect repository state**

```bash
python scripts/audit_public_release.py
git status --short
git log --oneline -8
```

Expected: audit passes. The only pre-existing uncommitted item may be the user's `.DS_Store`; it remains unstaged. No source or release artifact is left uncommitted.

## Task 8: Create and verify the public GitHub repository

**Files:**
- External state: `https://github.com/marjorychase6-star/product-relay`

- [ ] **Step 1: Verify authentication, repository name, and clean release state**

```bash
gh auth status
gh repo view marjorychase6-star/product-relay --json nameWithOwner,visibility,defaultBranchRef
git remote -v
git status --short
```

Expected: GitHub authentication is valid, the target repository does not yet exist, no `origin` is configured, and only the ignored/untracked user-owned `.DS_Store` may remain. If the repository already exists, stop and request direction instead of overwriting it.

- [ ] **Step 2: Create the public repository and push `main` normally**

```bash
gh repo create marjorychase6-star/product-relay --public --source=. --remote=origin --push --description "A local-first AI product execution partner for independent product managers."
```

Expected: repository creation succeeds, `origin` targets the new repository, and local `main` tracks `origin/main`.

- [ ] **Step 3: Add repository topics and verify public presentation**

```bash
gh repo edit marjorychase6-star/product-relay --add-topic product-management,ai-agent,local-first,prd,productivity
gh repo view marjorychase6-star/product-relay --json url,visibility,description,repositoryTopics,licenseInfo,defaultBranchRef
```

Expected: URL is `https://github.com/marjorychase6-star/product-relay`, visibility is `PUBLIC`, default branch is `main`, description/topics are present, and MIT license is detected.

- [ ] **Step 4: Check the public README as an unauthenticated page**

Open the repository URL in a browser and verify the ProductRelay name, tagline, screenshot, install commands, security model, limitations, MIT license, and Hermes attribution render correctly. Do not proceed to the portfolio plan until this check passes.
