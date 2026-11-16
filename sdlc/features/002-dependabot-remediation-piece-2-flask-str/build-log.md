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
