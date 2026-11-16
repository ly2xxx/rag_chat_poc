# Dependabot remediation: status

Design: [`docs/dependabot-remediation.md`](../../docs/dependabot-remediation.md) · Alerts: issue #4 · Base branch: `main` · State: complete

| Piece | Feature | Issue | Pull request | Alerts closed | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1: Test baseline and unused packages | `001-dependabot-remediation-piece-1-test-base` | #6, #12 | #13 | 4 (pandasai); 30 now visible in new pins: transformers 18, werkzeug 10, requests 2 | merged |
| 2: Flask, Streamlit and pypdf | `002-dependabot-remediation-piece-2-flask-str` | #15, #17 | #22 | 85 (flask 2, werkzeug 10, requests 2, streamlit 3, pypdf 68); none new | merged |
| 3: LangChain 1.x | `003-dependabot-remediation-piece-3-langchain` | #24 | #28 | 4 (langchain 2, langchain-community 2); none new | merged |
| 4: Torch and sentence-transformers | `004-dependabot-remediation-piece-4-torch-and` | #30 | #34 | 31 (torch 12, transformers 18, sentence-transformers 1); none new | merged |

Status is one of: `planned`, `building` (the run has started), `in review` (the
pipeline's pull request is open), `merged`.

## Next

Complete. No open Dependabot alerts: the monitor closed issue #4 on 2026-11-16 at 23:15 UTC
(94 at the start; 120 after piece 1 made pinned packages visible; 35, 31, then 0). Whole
suite on `main`: 51 passed. `.trivyignore` is gone.

Closing checklist (what the checks couldn't cover):
- Run the YouTube summary page once with a real OpenAI key: piece 3 changed its call to
  `llm.invoke(...)`, and no test can press that button (it needs OpenAI and YouTube).
- Run the chat pages (file, web) once with a real OpenAI key: tests use fake models and
  embeddings, so the real `langchain_openai` calls (and the new `openai` 3.x client) are
  untested.
- Look at the app once in a browser: the sidebar menu is now `st.navigation` (six links;
  `down` and `ref` reachable by URL only), checked under `AppTest` only.
- Any `embeddings/*.pkl` saved before the upgrade were pickled with LangChain 0.2 objects
  and may not load under 1.x; delete and regenerate them if loading fails.
- Local installs: `requirements.txt` now needs Python 3.10+ (3.11 in the pipeline); use the
  CPU torch index on machines without a GPU, as `.github/workflows/sdlc.yml` does.

## Deviations and follow-ups

Piece 1 (details in its `build-log.md`):
- Four interim pins beyond the plan, so a fresh install works: `pyarrow==25.0.0`,
  `transformers==4.46.3`, `huggingface-hub==0.25.2`, `werkzeug==2.0.3`;
  `test_exact_order_and_pins` expects 22 lines, not the plan's 18.
- The security scan blocked the first build run on 8 HIGH CVEs in the transformers and
  Werkzeug pins. The owner accepted them until pieces 2 and 4: `.trivyignore` (#11),
  then a `start: build` run (#12) opened #13.
- `requests==2.32.3` (the plan's pin for a package that was unpinned) is older than the
  release a fresh install used to get: 2 alerts. Piece 2 now upgrades it to 2.33.0.
- Review concern left as it is: `test_fixture_probe_is_gone` depends on test order (the
  plan's own design).

Piece 2 (details in its `build-log.md`):
- The first plan (#15) assumed `st-pages` kept working on Streamlit 1.54 and froze the
  files the fix needs; it can't import there. The design was made definite from a
  prototype (#16) and the feature replanned (#17).
- `tests/test_navigation.py` reads links with `at.sidebar.get("page_link")` (the plan's
  `at.sidebar.page_link` doesn't exist) and its `st_pages` scan skips its own file and
  `.venv/`. `generate_thumbnail` stays a module-level function.
- The hidden pages `down` and `ref` use Material icons; `st.Page` rejects `⤓` and `🔁`.
- Review concerns left as they are: one extra blank line removed from `.trivyignore`; the
  `.trivyignore` and menu tests check counts and labels, not each ID and icon.

Piece 3 (details in its `build-log.md`):
- Designed from a prototype install (#23), so the plan held: `tiktoken` had to move with
  `langchain-openai`, and the chatbot test needs an offline token counter.
- `pages/3_Robby-Youtube.py`: `llm(...)` became `llm.invoke(...)` against the plan's text,
  because LangChain 1.x chat models aren't callable; the summary button (needs an OpenAI
  key and YouTube) can't be tested here. Needs one manual run: closing checklist.
- Review concerns left as they are: `count_tokens_chain` (unused) now calls
  `chain.invoke(query)` with a string; the build log wrongly says `chain(chain_input)` is a
  substring of `chain.invoke(chain_input)` (the test is still correct).

Piece 4 (details in its `build-log.md`):
- None in the code; built as planned from a prototype install. The exact-score tests passed
  on the pipeline's CPU torch build as well as locally.
