# ProductRelay Deferred Release Work

**Recorded:** 2026-08-18
**Reason for pause:** Prioritize publishing the personal portfolio before the remaining ProductRelay release hardening work.

## Current product state

- Product worktree: `/Users/zevvv/vibe_coding/Hermes/pm-hermes/.worktrees/productrelay-release`
- Branch: `codex/productrelay-release`
- Last verified commit: `872233c` (`docs: add ProductRelay workspace preview`)
- The branch has not been merged into product `main` and no ProductRelay GitHub repository has been created or pushed.
- The latest screenshot is a real synthetic-demo capture at `docs/assets/productrelay-workspace.webp` (1600×1000 WebP). It is used by the portfolio card, but still shows the legacy `PH` mark because the final branding fix was intentionally deferred.

## Completed before the pause

- Product package and public CLI names changed to `product-relay`, `product-relay-ui`, and `product-relay-server`.
- Preferred `PRODUCT_RELAY_DATA_DIR` with `PM_HERMES_DATA_DIR` compatibility fallback.
- Public README, architecture/user docs, root MIT license, and Hermes attribution were added/updated.
- A Git-index-based public-release audit and regression tests were added.
- Initial release gate passed: backend 292 passed / 5 skipped, frontend 66 passed, lint/build, clean-install wheel/CLI, and audit passed.

## Required work before merging or publishing ProductRelay

1. Replace remaining visible legacy/placeholder branding in `ui/app.py`, `ui/webapp/index.html`, and `ui/webapp/src/app/AppShell.tsx`: ProductRelay desktop/window/browser titles and `PR` mark; then recapture the screenshot.
2. Extend the release audit to recognize supported-provider credentials (including OpenAI `sk-proj-…` values) and non-placeholder `API_KEY`, `TOKEN`, `SECRET`, and `PASSWORD` assignments.
3. Block tracked local runtime artifacts that can bypass `.gitignore`, including `.pm-hermes-data`, virtual environments, `__pycache__`, `.pyc`, SQLite `.sqlite`/`.sqlite3` files and `-wal`, `-shm`, `-journal` sidecars.
4. Replace README's `git clone <repository-url>` with `git clone https://github.com/marjorychase6-star/product-relay.git`.
5. Validate staged Hermes `LICENSE` and `UPSTREAM.md` contents/modes, not only their paths; keep scanning all tracked content safely and avoid broad test/vendor exemptions.
6. Optimize the index audit with batched blob access while retaining raw-byte checks for private-key headers, credential-shaped strings, and personal paths.
7. Re-run the full release gate, conduct final review, merge to product `main`, create the public `marjorychase6-star/product-relay` repository, and then verify the portfolio link resolves.

## Resume references

- [Confirmed design](../specs/2026-08-18-productrelay-portfolio-publication-design.md)
- [Product publication plan](../plans/2026-08-18-productrelay-publication.md)
- [Portfolio plan](../plans/2026-08-18-productrelay-portfolio.md)
- Product progress ledger: `/Users/zevvv/vibe_coding/Hermes/pm-hermes/.worktrees/productrelay-release/.superpowers/sdd/progress.md`
