"""
test_crawler.py — Tests for the Crawler class
"""

from unittest.mock import MagicMock, patch

import pytest

from src.crawler import Crawler


class TestNormaliseUrl:
    def test_strips_fragment(self) -> None:
        crawler = Crawler("https://quotes.toscrape.com/")
        assert crawler._normalise_url("https://quotes.toscrape.com/page/1/#top") == \
            "https://quotes.toscrape.com/page/1"

    def test_strips_trailing_slash(self) -> None:
        crawler = Crawler("https://quotes.toscrape.com/")
        assert crawler._normalise_url("https://quotes.toscrape.com/page/1/") == \
            "https://quotes.toscrape.com/page/1"

    def test_preserves_root_slash(self) -> None:
        crawler = Crawler("https://quotes.toscrape.com/")
        result = crawler._normalise_url("https://quotes.toscrape.com/")
        assert result == "https://quotes.toscrape.com/"

    def test_lowercases_scheme_and_host(self) -> None:
        crawler = Crawler("https://quotes.toscrape.com/")
        result = crawler._normalise_url("HTTPS://Quotes.ToScrape.Com/page/1/")
        assert result == "https://quotes.toscrape.com/page/1"


class TestFetch:
    def test_returns_html_on_200(self) -> None:
        crawler = Crawler("https://quotes.toscrape.com/")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>hello</html>"

        with patch("src.crawler.requests.get", return_value=mock_response):
            result = crawler._fetch("https://quotes.toscrape.com/")

        assert result == "<html>hello</html>"

    def test_returns_none_on_404(self) -> None:
        crawler = Crawler("https://quotes.toscrape.com/")
        mock_response = MagicMock()
        mock_response.status_code = 404

        with patch("src.crawler.requests.get", return_value=mock_response):
            result = crawler._fetch("https://quotes.toscrape.com/missing")

        assert result is None

    def test_returns_none_on_network_error(self) -> None:
        import requests as req
        crawler = Crawler("https://quotes.toscrape.com/")

        with patch("src.crawler.requests.get", side_effect=req.RequestException("timeout")):
            result = crawler._fetch("https://quotes.toscrape.com/")

        assert result is None


class TestExtractLinks:
    def test_returns_absolute_links(self) -> None:
        crawler = Crawler("https://quotes.toscrape.com/")
        html = '<a href="/page/2/">next</a>'
        links = crawler._extract_links("https://quotes.toscrape.com/", html)
        assert "https://quotes.toscrape.com/page/2" in links

    def test_filters_external_links(self) -> None:
        crawler = Crawler("https://quotes.toscrape.com/")
        html = '<a href="https://external.com/other">other</a>'
        links = crawler._extract_links("https://quotes.toscrape.com/", html)
        assert links == []

    def test_ignores_tags_without_href(self) -> None:
        crawler = Crawler("https://quotes.toscrape.com/")
        html = "<a>no href here</a>"
        links = crawler._extract_links("https://quotes.toscrape.com/", html)
        assert links == []


class TestCrawl:
    def test_yields_url_and_html(self) -> None:
        """Crawl yields (url, html) tuples for each discovered page."""
        crawler = Crawler("https://quotes.toscrape.com/", politeness_seconds=0)

        page1_html = '<html><body><a href="/page/2/">next</a></body></html>'
        page2_html = "<html><body>last page</body></html>"

        responses = {
            "https://quotes.toscrape.com/": page1_html,
            "https://quotes.toscrape.com/page/2": page2_html,
        }

        def fake_fetch(url: str) -> str | None:
            return responses.get(url)

        crawler._fetch = fake_fetch  # type: ignore[method-assign]
        results = list(crawler.crawl())

        urls = [url for url, _ in results]
        assert "https://quotes.toscrape.com/" in urls
        assert "https://quotes.toscrape.com/page/2" in urls

    def test_does_not_revisit_pages(self) -> None:
        """Each URL is fetched at most once."""
        crawler = Crawler("https://quotes.toscrape.com/", politeness_seconds=0)

        # Page 1 links back to itself
        html = '<html><body><a href="/">home</a></body></html>'
        fetch_counts: dict[str, int] = {}

        def fake_fetch(url: str) -> str | None:
            fetch_counts[url] = fetch_counts.get(url, 0) + 1
            return html

        crawler._fetch = fake_fetch  # type: ignore[method-assign]
        list(crawler.crawl())

        assert fetch_counts.get("https://quotes.toscrape.com/", 0) == 1
