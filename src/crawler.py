"""
crawler.py — Web crawler for quotes.toscrape.com

Responsibilities:
  - Fetch pages via HTTP
  - Discover links (BFS)
  - Enforce a politeness window between requests
  - Return raw page content for indexing
"""

from __future__ import annotations

import time
from collections import deque
from typing import Iterator
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


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
        self._seed_netloc = urlparse(seed_url).netloc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def crawl(self) -> Iterator[tuple[str, str]]:
        """
        Crawl the site starting from seed_url using BFS.

        Yields
        ------
        tuple[str, str]
            (url, html_content) for each successfully fetched page.
        """
        normalised_seed = self._normalise_url(self.seed_url)
        self._queue.append(normalised_seed)
        self._visited.add(normalised_seed)

        while self._queue:
            url = self._queue.popleft()

            html = self._fetch(url)
            if html is None:
                continue

            yield url, html

            for link in self._extract_links(url, html):
                if link not in self._visited:
                    self._visited.add(link)
                    self._queue.append(link)

            time.sleep(self.politeness_seconds)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _fetch(self, url: str) -> str | None:
        """
        Fetch a single URL and return its HTML content.

        Returns None on any network or HTTP error.
        """
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
            return None
        except requests.RequestException:
            return None

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
        soup = BeautifulSoup(html, "html.parser")
        links: list[str] = []

        for tag in soup.find_all("a", href=True):
            absolute = urljoin(base_url, tag["href"])
            normalised = self._normalise_url(absolute)
            if urlparse(normalised).netloc == self._seed_netloc:
                links.append(normalised)

        return links

    def _normalise_url(self, url: str) -> str:
        """Strip fragments and trailing slashes for consistent deduplication."""
        parsed = urlparse(url)
        # Lowercase scheme and host; strip fragment; clean up path
        path = parsed.path.rstrip("/") or "/"
        normalised = parsed._replace(
            scheme=parsed.scheme.lower(),
            netloc=parsed.netloc.lower(),
            path=path,
            fragment="",
        )
        return normalised.geturl()
