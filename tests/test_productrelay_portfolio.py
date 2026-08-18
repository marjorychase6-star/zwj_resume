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
        self.assertIn('class="project-card project-card--featured reveal"', HTML)
        self.assertIn('src="static/images/projects/productrelay-workspace.webp"', HTML)
        self.assertIn(
            'alt="ProductRelay workspace with lifecycle navigation and AI assistant"',
            HTML,
        )
        self.assertIn(f'href="{REPOSITORY_URL}"', HTML)
        self.assertIn('target="_blank" rel="noopener noreferrer"', HTML)
        self.assertTrue(IMAGE.is_file())

    def test_featured_layout_has_desktop_and_mobile_rules(self) -> None:
        self.assertIn(".project-card--featured", HTML)
        self.assertIn("grid-template-columns: minmax(0, 3fr) minmax(18rem, 2fr)", HTML)
        self.assertIn(
            ".project-card--featured .project-image {\n      height: auto;\n      min-height: 0;\n      aspect-ratio: 16 / 10;",
            HTML,
        )
        mobile = HTML.index("@media (max-width: 768px)")
        self.assertIn(".project-card--featured", HTML[mobile:])
        self.assertIn("grid-template-columns: 1fr", HTML[mobile:])

    def test_mobile_rules_prevent_existing_card_overflow(self) -> None:
        mobile = HTML.index("@media (max-width: 768px)")
        self.assertIn(
            ".about-card {\n        padding: 24px;\n        min-width: 0;",
            HTML[mobile:],
        )


if __name__ == "__main__":
    unittest.main()
