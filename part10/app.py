#!/usr/bin/env python3
"""
Part 10 starter.

WHAT'S NEW IN PART 10
You will write two classes without detailed instructions! This is a refactoring, we are not adding new functionality 🙄.
"""

# ToDo 0: You will need to move and change some imports
from typing import List
import time

from .constants import BANNER, HELP
from .models import SearchResult, SearchEngine
from .file_utilities import load_sonnets, Configuration, user_commands


def print_results(
        query: str,
        results: List[SearchResult],
        highlight: bool,
        hl_mode: str,
        query_time_ms: float | None = None,
) -> None:
    total_docs = len(results)
    matched = [r for r in results if r.matches > 0]

    line = f'{len(matched)} out of {total_docs} sonnets contain "{query}".'
    if query_time_ms is not None:
        line += f" Your query took {query_time_ms:.2f}ms."
    print(line)

    for idx, r in enumerate(matched, start=1):
        r.print_result(idx, highlight, total_docs, hl_mode)


# ---------- CLI loop ----------

def main() -> None:
    print(BANNER)
    # ToDo 0: Depending on how your imports look, you may need to adapt the call to load_config()
    config = Configuration.load_config()

    # Load sonnets (from cache or API)
    start = time.perf_counter()
    # ToDo 0: Depending on how your imports look, you may need to adapt the call to load_sonnets()
    sonnets = load_sonnets()
    search_engine = SearchEngine(sonnets)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"Loading sonnets took: {elapsed:.3f} [ms]")

    print(f"Loaded {len(sonnets)} sonnets.")

    while True:
        try:
            query = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not query:
            continue

        # commands
        if query.startswith(":"):
            if query == ":quit":
                print("Bye.")
                break

            if query == ":help":
                print(HELP)
                continue

        executed_command = False
        for cmd in user_commands:
            if cmd.update_setting(query, config):
                executed_command = True
                break

        if not executed_command:
            print("Unknown command. Type :help for commands.")

        if executed_command:
            continue
        start = time.perf_counter()
        # ToDo 1: Extract the search - basically everything until the end of the time measurement in a new class.
        #  Find a good name for that class. Make this class encapsulate our list of sonnets!
        combined_results = search_engine.search(query, config.search_mode)
        # Initialize elapsed_ms to contain the number of milliseconds the query evaluation took
        elapsed_ms = (time.perf_counter() - start) * 1000

        # ToDo 0: You will need to pass the new setting, the highlight_mode to print_results and use it there
        print_results(query, combined_results, config.highlight, config.hl_mode, elapsed_ms)


if __name__ == "__main__":
    main()
