# GenAI Usage Log — COMP3011 Coursework 2

This log documents all use of Generative AI tools throughout the development of this project,
as required by the GREEN category GenAI policy for this assessment.

**Tool used:** Claude Code (claude-sonnet-4-6) via CLI
**Purpose:** Pair programming, concept explanation, code scaffolding

---

## How to read this log

Each session entry records:
- **Date** — when the session occurred
- **What I asked** — the prompt or question posed to the AI
- **What was generated** — a summary of the AI's output
- **What I changed / rejected** — any modifications made before accepting, or reasons for rejection
- **Reflection** — what this interaction meant for my learning or development process

---

## Session Log

### Session 1 — 2026-03-28

**What I asked:**
How to activate claude-flow for the terminal, and then: explain the full coursework brief and create a phased implementation plan targeting 80–100.

**What was generated:**
- Explanation of how to run claude-flow via `npx`
- Full reading of the PDF brief
- A 6-phase implementation plan covering: scaffolding, crawler, indexer, search, testing, polish
- Identification of three "novel contributions": BM25 ranking, adaptive politeness controller, query co-occurrence suggestions
- A grading breakdown table with effort priorities

**What I changed / rejected:**
- Asked AI to step back from planning and give a conceptual lesson before implementation
- Requested infrastructure-only Phase 1 (no business logic) so I could understand the shape of the system first

**Reflection:**
The AI's initial plan was reasonable but moved too fast into implementation. Asking for a conceptual explanation first was more useful — the BM25 explanation from first principles (TF saturation, length normalisation) gave me genuine understanding rather than just code to copy. I could then evaluate whether the proposed novel features were genuinely interesting or just complexity for its own sake.

The adaptive politeness controller concept was not something I'd have thought of independently; I now understand why it's a meaningful improvement over a fixed sleep. The BM25 maths makes sense at the formula level but I'll need to implement it step by step to fully internalise it.

---

### Session 2 — 2026-03-28

**What I asked:**
Before implementing anything, I asked for a foundational lesson covering: how web scraping works, what an inverted index is, what TF-IDF is and its limitations, and specifically how BM25 and the adaptive politeness controller are genuinely novel rather than just extra complexity.

**What was generated:**
A structured breakdown covering:
- Web scraping as an automated HTTP client using BFS link discovery
- Inverted index structure: `word → {url → {freq, positions}}` (posting lists)
- TF-IDF from first principles: TF × IDF, and why it fails (unbounded TF growth)
- BM25 formula with k1 and b parameters explained — TF saturation and document length normalisation
- Adaptive politeness via Exponential Moving Average (EMA): `delay = max(6.0, EMA_latency × factor)`
- Query co-occurrence suggestions via bigram window counting
- A comparison table showing complexity cost vs capability gain for each novel feature

**What I changed / rejected:**
Nothing was rejected — this was a pure learning session with no code generated. I evaluated the explanations against what I already knew and found:
- The BFS/inverted index explanations matched the lecture material, confirming accuracy
- BM25 was new to me and the formula made sense once explained incrementally
- The adaptive politeness idea is genuinely creative — I wouldn't have made this connection independently

**Reflection:**
This session was more valuable than immediately jumping to code. Understanding *why* BM25 is better than TF-IDF (not just that it is) means I can explain it confidently in the video and defend the design choice. The AI correctly identified that just knowing a formula isn't the same as understanding it — the explanation built up from the flaw in TF-IDF to the BM25 fix, which is the right pedagogical order.

One limitation: the AI explained BM25 using the formula but couldn't show me *live* how scores change with different inputs. That's something I'll need to experiment with myself when implementing it.

---

### Session 3 — 2026-03-28

**What I asked:**
Implement Phase 1 of the plan: project infrastructure only — no business logic. Set up UV project, create all module stubs with typed interfaces, a working CLI REPL, and stub test files. Explicitly asked to avoid implementing any novel features at this stage.

**What was generated:**
- `pyproject.toml` — UV project with `requests`, `beautifulsoup4`, `pytest`, `pytest-cov` as dependencies
- `src/crawler.py` — `Crawler` class with typed method stubs and docstrings; `NotImplementedError` bodies
- `src/indexer.py` — `Indexer` class with `Posting` TypedDict and `InvertedIndex` type alias; stubs for `add_page`, `save`, `load`, `_tokenise`, `_extract_text`
- `src/search.py` — `SearchEngine` class with stubs for `print_word`, `find`, `_normalise_term`, `_intersect`
- `src/main.py` — **Fully working** REPL loop using Python `match` statement; dispatches all 4 commands with "not implemented yet" messages and inline TODO comments showing Phase 2/3 wiring
- `tests/test_crawler.py`, `test_indexer.py`, `test_search.py` — stub test files with 5 passing init tests and TODO comments for future phases
- `data/.gitkeep` — preserves the data directory in git
- `docs/genai_log.md` — this file, with Session 1 pre-filled

**What I changed / rejected:**
- The AI initially attempted `pip install pdfplumber` to read the brief PDF — I corrected this to use `uv` instead. The AI accepted the correction immediately and saved it as a persistent memory rule.
- I rejected the formal plan-approval step (ExitPlanMode) and told the AI to just implement then stop. The AI accepted this and saved it as a workflow preference.
- I reviewed all generated stubs before accepting. The type signatures looked reasonable. The `InvertedIndex = dict[str, dict[str, Posting]]` type alias is a clean, readable way to express the nested structure.

**Reflection:**
The stub-first approach was the right call. Seeing all the interfaces laid out before any logic is filled in makes the data flow obvious: `Crawler` yields `(url, html)` tuples → `Indexer.add_page()` consumes them → `SearchEngine` queries the resulting index. I can see where the seams are before getting lost in implementation details.

The AI used Python's `match` statement for the CLI dispatcher — I hadn't considered that. It's cleaner than a chain of `if/elif` and I understand why it's the right choice here. This is an example of the AI suggesting a better pattern than I'd have reached for by default.

All 5 stub tests passed on first run without modification. The test structure uses pytest classes and `tmp_path` fixtures — patterns I recognise from labs.

<!-- Add new sessions below this line -->
