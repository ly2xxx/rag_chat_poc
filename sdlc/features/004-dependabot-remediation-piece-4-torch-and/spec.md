<!-- sdlc stage=spec model=deepseek-v4.1-flash:cloud from=intent.md,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#done,docs/dependabot-remediation.md#piece-4@2cb3383 -->
## Summary
Updates the four vulnerable dependency pins in `requirements.txt` to the approved fixed versions and removes the obsolete `.trivyignore` CVEs plus their test. Adds CLI and requirements-suite checks proving offline similarity scoring still works and that the CVE suppression file is gone, with no application-code or model-file changes.

## Behaviour
1. Given `requirements.txt`, when its package lines are read, then `sentence-transformers==5.6.0`, `torch==2.13.0`, `transformers==5.23.0` and `huggingface-hub==2.4.0` replace their previous pins in place, and every other package line is unchanged.
2. Given `requirements.txt`, when its package lines are read, then every non-comment line is pinned with `==` and no package name contains `cuda`, `cudnn`, `cublas` or `nccl`.
3. Given `requirements.txt`, when its bytes are read, then the UTF-8 BOM and CRLF line endings remain present.
4. Given the local `all-MiniLM-L6-v2/` model, when `SimilarityScorer().score("The quick brown fox jumps over the lazy dog.", "The quick brown fox jumps over the lazy dog.")` runs without network access or model conversion, then the score is `1.0` to three decimal places.
5. Given the local `all-MiniLM-L6-v2/` model, when `SimilarityScorer().score("a cat sits on the mat", "a cat is sitting on a mat")` runs, then the score is `0.984` to three decimal places.
6. Given the local `all-MiniLM-L6-v2/` model, when `SimilarityScorer().score("a cat sits on the mat", "stock prices fell today")` runs, then the score is `0.079` to three decimal places.
7. Given `app/__main__.py` and the two arguments `"a cat"` and `"a cat"`, when run via `subprocess.run([sys.executable, "app/__main__.py", "a cat", "a cat"])`, then stdout contains a line beginning `Sentence Transformers:` whose parsed float value is greater than `0.99`.
8. Given `app/__main__.py` and exactly one argument, when run, then the process exits with code `1`.
9. Given the repository root, when `tests/test_requirements.py` runs, then it asserts `.trivyignore` does not exist.
10. Given the repository root, when the test suite is collected, then `tests/test_trivyignore.py` is absent.
11. Given the full pytest suite run from the repository root without network access, secrets or a GPU, then all tests pass.

## Interfaces

### `requirements.txt`
Change these lines in place, preserving order, UTF-8 BOM and CRLF line endings; all other package lines remain unchanged:
- `sentence-transformers==5.6.0`
- `torch==2.13.0`
- `transformers==5.23.0`
- `huggingface-hub==2.4.0`

The pipeline install command remains:
`uv pip install --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt`

### `tests/test_requirements.py`
Update the module constant `EXPECTED` so the four lines above replace the old pins at their existing relative positions; all other `EXPECTED` entries remain unchanged. Add one test asserting `Path(".trivyignore").exists()` is `False`; the approved design does not name this test function. Existing `_package_lines() -> list[str]` remains unchanged.

### `tests/test_cli.py` (new file)
Add a new test module containing tests that invoke `app/__main__.py` with `subprocess.run([sys.executable, "app/__main__.py", "a cat", "a cat"])` and assert stdout contains a `Sentence Transformers:` line whose parsed float is greater than `0.99`, and that exactly one argument exits with code `1`. The approved design does not name these test functions.

### Deletions
- Delete `.trivyignore`.
- Delete `tests/test_trivyignore.py`.

### Unchanged application interfaces
- `app/__main__.py`: `compare_with_model(text1: str, text2: str)` is unchanged.
- `modules/similarity.py`: `SimilarityScorer.__init__(self)` and `SimilarityScorer.score(self, text1, text2)` are unchanged.

## Out of scope
Application-code changes; no changes to `app/`, `modules/`, `pages/`, `streamlit_app.py`, `filename.py` or `flask_app.py` behaviour.
Converting or downloading the local model, or changing anything under `all-MiniLM-L6-v2/`.
Refactoring, new features, page titles, widgets or page behaviour.
CUDA packages.
`playground/`, notebooks, `Gallery/`, `.devcontainer/` and `.github/`.
Dependabot alerts in packages not named by this piece.

## Open questions
- The approved design does not name the new test functions in `tests/test_cli.py` or the new `.trivyignore`-absence test in `tests/test_requirements.py`; assumption: descriptive function names may be chosen, with the file locations and assertions fixed by this spec.
- The approved Done states the full pin set installs on Python 3.11 with the pipeline command; no offline test can reproduce a network install. Assumption: the automated requirements checks cover the exact pins and absence of CUDA package names, while installation success remains the pipeline’s install-command check.
