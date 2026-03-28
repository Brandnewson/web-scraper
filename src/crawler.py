"""
crawler.py — Web crawler for quotes.toscrape.com

Responsibilities:
  - Fetch pages via HTTP
  - Discover links (BFS)
  - Enforce a politeness window between requests
  - Return raw page content for indexing
"""

from __future__ import annotations

from collections import deque
from typing import Iterator


class Crawler:
    """
    BFS web crawler.

    Parameters
    ----------
    seed_url : str
        The starting URL to crawl from.
    politeness_seconds : float
        Minimum delay between successive HTTP requests.
        Must be >= 6.0 per the brief.
    """

    def __init__(self, seed_url: str, politeness_seconds: float = 6.0) -> None:
        self.seed_url = seed_url
        self.politeness_seconds = politeness_seconds
        self._visited: set[str] = set()
        self._queue: deque[str] = deque()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def crawl(self) -> Iterator[tuple[str, str]]:
        """
        Crawl the site starting from seed_url.

        Yields
        ------
        tuple[str, str]
            (url, html_content) for each successfully fetched page.
        """
        raise NotImplementedError("TODO: Phase 2 — implement BFS crawl loop")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _fetch(self, url: str) -> str | None:
        """
        Fetch a single URL and return its HTML content.

        Returns None on any network or HTTP error.
        """
        raise NotImplementedError("TODO: Phase 2 — implement HTTP fetch with error handling")

    def _extract_links(self, base_url: str, html: str) -> list[str]:
        """
        Parse HTML and return all absolute, in-domain links.

        Parameters
        ----------
        base_url : str
            Used to resolve relative hrefs.
        html : str
            Raw HTML content of the page.
        """
        raise NotImplementedError("TODO: Phase 2 — implement link extraction with BeautifulSoup")

    def _normalise_url(self, url: str) -> str:
        """Strip fragments and trailing slashes for consistent deduplication."""
        raise NotImplementedError("TODO: Phase 2 — implement URL normalisation")
