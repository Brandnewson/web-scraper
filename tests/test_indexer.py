"""
test_indexer.py — Tests for the Indexer class
"""

import json
from pathlib import Path

import pytest

from src.indexer import Indexer


class TestIndexerInit:
    def test_indexer_instantiates(self, tmp_path: Path) -> None:
        indexer = Indexer(index_path=tmp_path / "index.json")
        assert indexer.index_path == tmp_path / "index.json"

    def test_index_starts_empty(self, tmp_path: Path) -> None:
        indexer = Indexer(index_path=tmp_path / "index.json")
        assert indexer.index == {}


class TestTokenise:
    def test_lowercases(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        assert "hello" in indexer._tokenise("HELLO World")

    def test_strips_punctuation(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        tokens = indexer._tokenise("hello, world!")
        assert "hello" in tokens
        assert "world" in tokens

    def test_discards_single_chars(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        tokens = indexer._tokenise("a big cat")
        assert "a" not in tokens
        assert "big" in tokens

    def test_empty_string_returns_empty_list(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        assert indexer._tokenise("") == []


class TestAddPage:
    def test_records_frequency(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        html = "<html><body>wisdom wisdom wisdom</body></html>"
        indexer.add_page("https://example.com/", html)
        assert indexer.index["wisdom"]["https://example.com/"]["freq"] == 3

    def test_records_positions(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        # Tokens after filtering single chars: ["the", "cat", "sat"]
        html = "<html><body>the cat sat</body></html>"
        indexer.add_page("https://example.com/", html)
        positions = indexer.index["cat"]["https://example.com/"]["positions"]
        assert isinstance(positions, list)
        assert len(positions) == 1

    def test_case_insensitive(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        html = "<html><body>Wisdom WISDOM wisdom</body></html>"
        indexer.add_page("https://example.com/", html)
        assert indexer.index["wisdom"]["https://example.com/"]["freq"] == 3

    def test_multiple_pages(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        indexer.add_page("https://example.com/1", "<body>life is short</body>")
        indexer.add_page("https://example.com/2", "<body>life is long</body>")
        assert len(indexer.index["life"]) == 2


class TestSaveLoad:
    def test_save_creates_json_file(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        indexer.add_page("https://example.com/", "<body>hello world</body>")
        indexer.save()
        assert (tmp_path / "index.json").exists()

    def test_load_restores_index(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        indexer.add_page("https://example.com/", "<body>wisdom</body>")
        indexer.save()

        indexer2 = Indexer(tmp_path / "index.json")
        indexer2.load()
        assert "wisdom" in indexer2.index

    def test_save_load_roundtrip_preserves_data(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "index.json")
        html = "<body>the quick brown fox</body>"
        indexer.add_page("https://example.com/", html)
        indexer.save()

        indexer2 = Indexer(tmp_path / "index.json")
        indexer2.load()
        assert indexer2.index == indexer.index

    def test_load_raises_if_no_file(self, tmp_path: Path) -> None:
        indexer = Indexer(tmp_path / "missing.json")
        with pytest.raises(FileNotFoundError):
            indexer.load()
