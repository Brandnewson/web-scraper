"""
test_search.py — Tests for the SearchEngine class

Phase 1: Placeholder — verifies the module imports cleanly.
Phase 3: Will add tests for print_word, find (single/multi-word),
         empty queries, unknown words, ranking order.
"""

from src.search import SearchEngine


class TestSearchEngineInit:
    def test_search_engine_instantiates(self) -> None:
        """SearchEngine can be constructed with an empty index."""
        engine = SearchEngine(index={})
        assert engine._index == {}

    # TODO Phase 3: test_print_word_known_word
    # TODO Phase 3: test_print_word_unknown_word
    # TODO Phase 3: test_find_single_term_returns_pages
    # TODO Phase 3: test_find_multi_term_returns_intersection
    # TODO Phase 3: test_find_unknown_term_returns_empty_list
    # TODO Phase 3: test_find_empty_query_returns_empty_list
    # TODO Phase 3: test_find_results_are_ranked
    # TODO Phase 3: test_find_case_insensitive
