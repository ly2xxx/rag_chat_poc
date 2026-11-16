# Build log: 002-dependabot-remediation-piece-2-flask-str

## Phase 1: Update non-Streamlit pins

**Status:** passed

**Files changed:** `requirements.txt`, `tests/test_requirements.py`

`pypdf`, `requests`, `flask` and `werkzeug` moved to 6.21.4, 2.33.0, 3.1.3 and 3.1.9 by
byte replacement (BOM and CRLF kept); `EXPECTED` follows, and a new test checks the BOM
and CRLF.

**Commands:**
- `uv pip install -r requirements.txt` (Python 3.11 venv): exit 0.
- `sdlc_stage.py verify --feature 002-dependabot-remediation-piece-2-flask-str --phase 1`
  (runs `python -m pytest tests/test_requirements.py tests/test_flask.py tests/test_imports.py tests/test_embedder.py -v`):
  exit 0, 17 passed.

**Deviations:** none.

## Phase 2: Upgrade Streamlit and use native navigation

**Status:** passed

**Files changed:** `requirements.txt`, `streamlit_app.py`, `pages/0_Keywords-Research-beta.py`,
`pages/1_Robby-Chat-file.py`, `pages/2_Robby-Chat-web.py`, `pages/3_Robby-Youtube.py`,
`pages/4_Text-Similarity-beta.py`, `tests/test_requirements.py`, `tests/test_navigation.py`

Streamlit 1.54.0, `st-pages` removed. `streamlit_app.py` builds the menu with
`st.navigation(MENU + HIDDEN, position="hidden")` and `st.page_link` for the six visible
pages; the home content is `home()`. The five pages no longer import or call `hide_pages`;
`test_st_pages_exports` is deleted.

**Commands:**
- `uv pip uninstall st-pages && uv pip install -r requirements.txt`: exit 0.
- `sdlc_stage.py verify --feature 002-dependabot-remediation-piece-2-flask-str --phase 2`
  (runs `python -m pytest tests/test_requirements.py tests/test_navigation.py tests/test_pages.py -v`):
  first attempt 2 failed (the two test-text errors below); after the fixes: exit 0, 18 passed.

**Deviations:**
- `tests/test_navigation.py`: Streamlit 1.54's `AppTest` has no `at.sidebar.page_link`
  (`AttributeError: 'SpecialBlock' object has no attribute 'page_link'`); the test reads the
  links with `at.sidebar.get("page_link")` instead. The plan's open questions named this case.
- `tests/test_navigation.py`: the `st_pages` scan found its own function name
  (`test_no_st_pages_imports_outside_playground`), so it skips its own file; it also skips
  `.venv/`, which the pipeline creates inside the checkout.
- `streamlit_app.py`: `generate_thumbnail` was defined after the old menu calls, so moving
  that code into `home()` would have nested it. It stays a module-level function, unchanged,
  placed above `home()`, as the plan says to keep it.
