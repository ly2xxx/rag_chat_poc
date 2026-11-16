<!-- sdlc stage=intent model=deepseek-v4.1-flash:cloud from=idea,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#piece-1@439ae0e -->
# Intent: Dependabot remediation piece 1 — test baseline

**Owner:** @ly2xxx · **Status:** proposed (approving the review gate approves it)

## Problem
The maintainers of `rag_chat_poc` face 94 open Dependabot alerts across 8 packages, but the repository has no smoke-test baseline proving the app still works. Dependency remediation is therefore risky, and unused packages in `requirements.txt` add noise and false confidence about what the app needs. The cost is slower, less trustworthy upgrades and no clear signal of breakage.

## Outcome
The repository has a pytest smoke-test baseline under `tests/` covering module imports, Streamlit pages, similarity scoring, Flask, and the embedder. `requirements.txt` reflects only packages the app uses, pins the added runtime dependencies, and pins `st-pages` to a version that still exports every name the app imports. Generated `embeddings/` files are ignored by git, and every pin installs on Python 3.11 with the pipeline’s install command and no CUDA packages.

## Done when
- `requirements.txt` no longer lists `pandasai`, `playwright` or `pytube`; it adds `pandas==2.3.3` and `python-dotenv==1.2.4`; `streamlit_app.py` no longer mentions PandasAI.
- `st-pages` is pinned to the newest release that exports every name the app imports, and `embeddings/` is ignored by git.
- `tests/conftest.py` puts the repository root on `sys.path`, sets `OPENAI_API_KEY=sk-test` for every test, and removes `embeddings/*.pkl` files created by tests.
- Import, page, similarity, Flask and embedder tests exist and pass: every module in `modules/` imports; `AppTest.from_file(path, default_timeout=60).run()` has no exception for `streamlit_app.py` and each `pages/*.py`; identical sentences score above 0.99 and the cat-sentence pair scores higher than the stock-price pair; `GET /` returns 200; the Wales PDF yields 3 FAISS similarity-search documents with `FakeEmbeddings(size=8)`.
- The existing tests still pass.

## Not in scope
Upgrades for alerts in packages this piece does not name; refactoring or new features; CUDA packages; `playground/`, the notebooks, `Gallery/`, `.devcontainer/`, and `.github/`.

## Open questions
None.

## Design
Written from these approved sections, which the spec and plan stages read word for word:
- `docs/dependabot-remediation.md#rules-for-every-piece`
- `docs/dependabot-remediation.md#facts-the-plan-must-not-guess`
- `docs/dependabot-remediation.md#piece-1`

