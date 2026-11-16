# Build log: 001-dependabot-remediation-piece-1-test-base

## Phase 1: Dependency hygiene and pytest bootstrap

**Status:** passed

**Files changed:** `requirements.txt`, `.gitignore`, `streamlit_app.py`, `tests/conftest.py`,
`tests/test_requirements.py`, `tests/test_conftest.py`

Removed `pandasai`, `playwright` and `pytube`, pinned every remaining package with `==`
(the plan's pins), dropped the PandasAI mention from `streamlit_app.py`, ignored
`embeddings/`, and added the shared test bootstrap with its own tests.

**Commands:**
- `uv venv --python 3.11 .venv && uv pip install -r requirements.txt pytest`: exit 0.
- `sdlc_stage.py verify --feature 001-dependabot-remediation-piece-1-test-base --phase 1`
  (runs `python -m pytest tests/test_requirements.py tests/test_conftest.py -v`):
  exit 0, 13 passed.

**Deviations:**
- `requirements.txt` gets four more pins, `pyarrow==25.0.0`, `transformers==4.46.3`,
  `huggingface-hub==0.25.2` and `werkzeug==2.0.3`, placed before `pandas` and
  `python-dotenv` so those stay the last two lines (spec behaviours 2 and 3).
  `test_exact_order_and_pins` expects 22 lines instead of the plan's 18. Why: these three are unpinned dependencies whose latest
  releases break a fresh install of the current pins, reproduced on Python 3.11 before
  building: pyarrow 26 needs NumPy 2 while langchain 0.2 and Streamlit 1.31 cap NumPy
  below 2 (Streamlit fails to import); transformers 4.57 needs a newer torch than 2.1
  (`torch.utils._pytree.register_pytree_node`); huggingface-hub 0.26 removed
  `cached_download`, which sentence-transformers 2.2.2 imports; Werkzeug 3 removed
  `werkzeug.urls.url_quote`, which Flask 2.0.2 imports, and only Werkzeug 2.0.x runs
  Flask 2.0.2's test client (2.1.2, 2.2.3 and 2.3.8 fail `GET /`). transformers 4.46.3 is
  the newest release that works: later ones need huggingface-hub 0.26 or torch 2.2.
  Without these pins phases 2 and 3 fail. transformers 4.46.3 and Werkzeug 2.0.3 carry
  known CVEs that were installed before too, only unpinned; pieces 2 and 4 replace them. Pieces 2 and 4 replace these pins when they upgrade Streamlit and torch.
- `test_fixture_removes_probe_after_test` writes the probe under the repository root's
  `embeddings/` (absolute path) rather than a path relative to the working directory, so it
  matches the fixture's cleanup root wherever pytest is started.
