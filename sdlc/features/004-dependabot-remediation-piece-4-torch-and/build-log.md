# Build log: 004-dependabot-remediation-piece-4-torch-and

## Phase 1: Update the four pins in place

**Status:** passed

**Files changed:** `requirements.txt`, `tests/test_requirements.py`

`sentence-transformers==5.6.0`, `torch==2.13.0`, `transformers==5.23.0` and
`huggingface-hub==2.4.0` replace the old pins in place (BOM and CRLF kept); `EXPECTED`
follows at the same indices.

**Commands:**
- `uv pip install -r requirements.txt` (Python 3.11; torch from PyPI here, as the CPU index
  isn't reachable from this sandbox): exit 0.
- `sdlc_stage.py verify --feature 004-dependabot-remediation-piece-4-torch-and --phase 1`
  (runs `python -m pytest tests/test_requirements.py -v`): exit 0, 7 passed.

**Deviations:** none.

## Phase 2: Delete `.trivyignore` and its test

**Status:** passed

**Files changed:** `.trivyignore` (deleted), `tests/test_trivyignore.py` (deleted),
`tests/test_requirements.py`

The last accepted IDs (transformers 4.46.3) are fixed by phase 1, so the ignore file and its
test are gone, and `test_trivyignore_absent` keeps the file from coming back.

**Commands:**
- `sdlc_stage.py verify --feature 004-dependabot-remediation-piece-4-torch-and --phase 2`
  (runs `python -m pytest tests/test_requirements.py -v`, `test ! -e .trivyignore`,
  `test ! -e tests/test_trivyignore.py`): exit 0, 8 passed.

**Deviations:** none.
