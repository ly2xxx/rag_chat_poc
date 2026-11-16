# Dependabot remediation: status

Design: [`docs/dependabot-remediation.md`](../../docs/dependabot-remediation.md) · Alerts: issue #4 · Base branch: `main` · State: in progress

| Piece | Feature | Issue | Pull request | Alerts closed | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1: Test baseline and unused packages | `001-dependabot-remediation-piece-1-test-base` | #6, #12 | #13 | 4 (pandasai); 30 now visible in new pins: transformers 18, werkzeug 10, requests 2 | merged |
| 2: Flask, Streamlit and pypdf | `002-dependabot-remediation-piece-2-flask-str` | #15, #17 | #22 | pending the monitor rerun | merged |
| 3: LangChain 1.x | | | | | planned |
| 4: Torch and sentence-transformers | | | | | planned |

Status is one of: `planned`, `building` (the run has started), `in review` (the
pipeline's pull request is open), `merged`.

## Next

Record the alerts piece 2 closed (the monitor reruns 10 minutes after #22), then start piece 3.

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
