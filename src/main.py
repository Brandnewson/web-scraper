"""
main.py — CLI entry point

Provides an interactive REPL with four commands:
  build  — crawl the site and build the index
  load   — load a previously built index from disk
  print  — print the posting list for a word
  find   — find pages containing a query phrase
  quit   — exit the shell
"""

from __future__ import annotations

from pathlib import Path

from src.crawler import Crawler
from src.indexer import Indexer
from src.search import SearchEngine

# Configuration constants
TARGET_URL = "https://quotes.toscrape.com/"
INDEX_PATH = Path("data/index.json")
POLITENESS_SECONDS = 6.0

HELP_TEXT = """\
Commands:
  build              Crawl the site and build the inverted index
  load               Load the index from disk
  print <word>       Print the posting list for a word
  find <query...>    Find pages containing all query terms
  help               Show this message
  quit               Exit
"""


def run_shell() -> None:
    """Start the interactive CLI shell."""
    indexer = Indexer(index_path=INDEX_PATH)
    search: SearchEngine | None = None

    print("Search Engine Tool — COMP3011 Coursework 2")
    print('Type "help" for available commands.\n')

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not raw:
            continue

        parts = raw.split()
        command, *args = parts

        match command.lower():
            case "build":
                print("build: not implemented yet")
                # TODO Phase 2:
                #   crawler = Crawler(TARGET_URL, POLITENESS_SECONDS)
                #   for url, html in crawler.crawl():
                #       indexer.add_page(url, html)
                #   indexer.save()
                #   search = SearchEngine(indexer.index)

            case "load":
                print("load: not implemented yet")
                # TODO Phase 2:
                #   indexer.load()
                #   search = SearchEngine(indexer.index)

            case "print":
                if not args:
                    print("Usage: print <word>")
                else:
                    print(f"print '{args[0]}': not implemented yet")
                    # TODO Phase 3:
                    #   if search is None: print("Run 'build' or 'load' first")
                    #   else: search.print_word(args[0])

            case "find":
                if not args:
                    print("Usage: find <query terms...>")
                else:
                    query = " ".join(args)
                    print(f"find '{query}': not implemented yet")
                    # TODO Phase 3:
                    #   if search is None: print("Run 'build' or 'load' first")
                    #   else: results = search.find(query); ...

            case "help":
                print(HELP_TEXT)

            case "quit" | "exit" | "q":
                print("Bye.")
                break

            case _:
                print(f"Unknown command: '{command}'. Type 'help' for usage.")


if __name__ == "__main__":
    run_shell()
