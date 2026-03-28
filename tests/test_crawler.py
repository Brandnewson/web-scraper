"""
test_crawler.py — Tests for the Crawler class

Phase 1: Placeholder — verifies the module imports cleanly.
Phase 2: Will add mocked HTTP tests, link extraction, BFS ordering,
         politeness window enforcement, and error handling.
"""

from src.crawler import Crawler


class TestCrawlerInit:
    def test_crawler_instantiates(self) -> None:
        """Crawler can be constructed with a seed URL."""
        crawler = Crawler(seed_url="https://quotes.toscrape.com/", politeness_seconds=6.0)
        assert crawler.seed_url == "https://quotes.toscrape.com/"
        assert crawler.politeness_seconds == 6.0

    def test_politeness_defaults_to_six_seconds(self) -> None:
        """Default politeness window is exactly 6.0 seconds."""
        crawler = Crawler(seed_url="https://quotes.toscrape.com/")
        assert crawler.politeness_seconds == 6.0

    # TODO Phase 2: test_crawl_visits_all_pages
    # TODO Phase 2: test_crawl_respects_politeness_window
    # TODO Phase 2: test_fetch_returns_none_on_404
    # TODO Phase 2: test_fetch_returns_none_on_timeout
    # TODO Phase 2: test_extract_links_returns_absolute_urls
    # TODO Phase 2: test_extract_links_stays_on_domain
    # TODO Phase 2: test_normalise_url_strips_fragment
