"""
test_indexer.py — Tests for the Indexer class

Phase 1: Placeholder — verifies the module imports cleanly.
Phase 2: Will add tests for tokenisation, index construction,
         case normalisation, position tracking, serialisation.
"""

from pathlib import Path

from src.indexer import Indexer


class TestIndexerInit:
    def test_indexer_instantiates(self, tmp_path: Path) -> None:
        """Indexer can be constructed with a file path."""
        index_path = tmp_path / "index.json"
        indexer = Indexer(index_path=index_path)
        assert indexer.index_path == index_path

    def test_index_starts_empty(self, tmp_path: Path) -> None:
        """A freshly created Indexer has an empty index."""
        indexer = Indexer(index_path=tmp_path / "index.json")
        assert indexer.index == {}

    # TODO Phase 2: test_tokenise_lowercases_text
    # TODO Phase 2: test_tokenise_strips_punctuation
    # TODO Phase 2: test_add_page_records_frequency
    # TODO Phase 2: test_add_page_records_positions
    # TODO Phase 2: test_save_creates_json_file
    # TODO Phase 2: test_load_restores_index
    # TODO Phase 2: test_case_insensitive_deduplication
