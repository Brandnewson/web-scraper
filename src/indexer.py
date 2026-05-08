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
import re
from pathlib import Path
from typing import TypedDict

from bs4 import BeautifulSoup


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
        text = self._extract_text(html)
        tokens = self._tokenise(text)

        for position, token in enumerate(tokens):
            if token not in self._index:
                self._index[token] = {}
            if url not in self._index[token]:
                self._index[token][url] = {"freq": 0, "positions": []}
            self._index[token][url]["freq"] += 1
            self._index[token][url]["positions"].append(position)

    def save(self) -> None:
        """Serialise the current index to self.index_path as JSON."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self._index, f, indent=2)

    def load(self) -> None:
        """Load a previously saved index from self.index_path."""
        if not self.index_path.exists():
            raise FileNotFoundError(
                f"No index found at '{self.index_path}'. Run 'build' first."
            )
        with open(self.index_path, encoding="utf-8") as f:
            self._index = json.load(f)

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
        - Strip non-alphabetic characters
        - Split on whitespace
        - Discard single-character tokens
        """
        lowered = text.lower()
        cleaned = re.sub(r"[^a-z\s]", "", lowered)
        return [token for token in cleaned.split() if len(token) > 1]

    def _extract_text(self, html: str) -> str:
        """Extract visible text content from raw HTML using BeautifulSoup."""
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.find_all(["script", "style"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)
