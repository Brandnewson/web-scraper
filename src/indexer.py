"""
indexer.py — Inverted index builder

Responsibilities:
  - Tokenise page text (lowercase, strip punctuation)
  - Build a positional inverted index from crawled pages
  - Serialise / deserialise the index to/from JSON

Index structure:
  {
    "word": {
      "https://example.com/page": {
        "freq": 3,
        "positions": [4, 17, 42]
      }
    }
  }
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict


class Posting(TypedDict):
    """A single entry in a posting list."""
    freq: int
    positions: list[int]


# The full index type: word -> url -> posting
InvertedIndex = dict[str, dict[str, Posting]]


class Indexer:
    """
    Builds and persists a positional inverted index.

    Parameters
    ----------
    index_path : Path
        File path where the index is saved and loaded from.
    """

    def __init__(self, index_path: Path) -> None:
        self.index_path = index_path
        self._index: InvertedIndex = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_page(self, url: str, html: str) -> None:
        """
        Tokenise the text content of a page and add it to the index.

        Parameters
        ----------
        url : str
            The page's URL (used as the document identifier).
        html : str
            Raw HTML — text will be extracted before indexing.
        """
        raise NotImplementedError("TODO: Phase 2 — extract text, tokenise, update index")

    def save(self) -> None:
        """Serialise the current index to self.index_path as JSON."""
        raise NotImplementedError("TODO: Phase 2 — implement JSON serialisation")

    def load(self) -> None:
        """Load a previously saved index from self.index_path."""
        raise NotImplementedError("TODO: Phase 2 — implement JSON deserialisation")

    @property
    def index(self) -> InvertedIndex:
        """Read-only access to the current index state."""
        return self._index

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _tokenise(self, text: str) -> list[str]:
        """
        Normalise and tokenise a string.

        - Lowercase
        - Strip punctuation
        - Split on whitespace
        - Return list of tokens (preserving order for position tracking)
        """
        raise NotImplementedError("TODO: Phase 2 — implement tokeniser")

    def _extract_text(self, html: str) -> str:
        """Extract visible text content from raw HTML using BeautifulSoup."""
        raise NotImplementedError("TODO: Phase 2 — implement text extraction")
