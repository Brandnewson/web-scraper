"""
search.py — Query engine

Responsibilities:
  - Implement the `print` command: display a word's posting list
  - Implement the `find` command: retrieve and rank pages for a query
  - Handle edge cases: unknown words, empty queries, multi-word queries

Ranking strategy (Phase 3+): Okapi BM25
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.indexer import InvertedIndex


class SearchEngine:
    """
    Query interface over a loaded inverted index.

    Parameters
    ----------
    index : InvertedIndex
        The in-memory inverted index built by Indexer.
    """

    def __init__(self, index: "InvertedIndex") -> None:
        self._index = index

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def print_word(self, word: str) -> None:
        """
        Print the posting list for a single word to stdout.

        Example output:
            "nonsense" found in 2 pages:
              https://quotes.toscrape.com/page/1/  freq=1  positions=[14]
              https://quotes.toscrape.com/page/3/  freq=2  positions=[5, 22]
        """
        raise NotImplementedError("TODO: Phase 3 — implement print_word")

    def find(self, query: str) -> list[str]:
        """
        Find pages containing all query terms, ranked by relevance.

        Parameters
        ----------
        query : str
            One or more space-separated search terms.

        Returns
        -------
        list[str]
            Ordered list of URLs (most relevant first).
            Empty list if no pages match or query is blank.
        """
        raise NotImplementedError("TODO: Phase 3 — implement ranked multi-term find")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _normalise_term(self, term: str) -> str:
        """Lowercase and strip punctuation from a single query term."""
        raise NotImplementedError("TODO: Phase 3 — implement term normalisation")

    def _intersect(self, term_urls: list[set[str]]) -> set[str]:
        """
        Return the intersection of multiple posting-list URL sets.
        Used for multi-word AND queries.
        """
        raise NotImplementedError("TODO: Phase 3 — implement set intersection")
