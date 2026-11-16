<!-- sdlc stage=plan model=deepseek-v4.1-flash:cloud from=intent.md,spec.md,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#piece-1@6493d6d -->
## Approach
Add the smoke-test baseline in four small phases: first make dependency and pytest bootstrap changes plus their metadata tests, then add import/page tests, then similarity/Flask tests, then the embedder test. No production module signatures change; only `requirements.txt`, `.gitignore`, and the PandasAI comment in `streamlit_app.py` change.

## Coverage

| Done when (intent.md) | Spec behaviours | Phase |
| :-- | :-- | :-- |
| `requirements.txt` no longer lists `pandasai`, `playwright` or `pytube`; it adds `pandas==2.3.3` and `python-dotenv==1.2.4`; `streamlit_app.py` no longer mentions PandasAI. | 1, 2, 3, 4, 7 | 1 |
| `st-pages` is pinned to the newest release that exports every name the app imports, and `embeddings/` is ignored by git. | 5, 6, 8 | 1 |
| `tests/conftest.py` puts the repository root on `sys.path`, sets `OPENAI_API_KEY=sk-test` for every test, and removes `embeddings/*.pkl` files created by tests. | 9, 10, 11, 12 | 1 |
| Import, page, similarity, Flask and embedder tests exist and pass: every module in `modules/` imports; `AppTest.from_file(path, default_timeout=60).run()` has no exception for `streamlit_app.py` and each `pages/*.py`; identical sentences score above 0.99 and the cat-sentence pair scores higher than the stock-price pair; `GET /` returns 200; the Wales PDF yields 3 FAISS similarity-search documents with `FakeEmbeddings(size=8)`. | 13, 14, 15, 16, 17, 18, 19, 20, 21 | 2, 3, 4 |
| The existing tests still pass. | 22 | Final suite after Phase 4 |

## Phase 1: Dependency hygiene and pytest bootstrap
<!-- phase: 1 -->
<!-- targets: requirements.txt, .gitignore, streamlit_app.py, tests/conftest.py, tests/test_requirements.py, tests/test_conftest.py -->
<!-- frozen: docs/dependabot-remediation.md, sdlc/features/001-dependabot-remediation-piece-1-test-base/intent.md, sdlc/features/001-dependabot-remediation-piece-1-test-base/spec.md -->

**Goal:** `requirements.txt` has only exact non-CUDA pins, the unused packages and PandasAI mention are gone, `embeddings/` is ignored, and `tests/conftest.py` provides the shared path/key/cleanup baseline.

**Changes:**
- `requirements.txt`: preserve the existing UTF-8 byte-order mark. Remove the exact lines `pandasai==0.2.15`, `playwright==1.42.0`, and `pytube==15.0.0`. Keep the existing comment line `# pywin32==308`. Change `st-pages>=0.4.3` to `st-pages==0.5.0`. Change unpinned lines to `pdfplumber==0.11.4`, `faiss-cpu==1.9.0`, `requests==2.32.3`, and `bs4==0.0.2`. Append `pandas==2.3.3` and `python-dotenv==1.2.4` as the final two package lines. The resulting non-comment package lines, in order, must be exactly:
  ```text
  langchain==0.2.11
  openai==0.27.7
  langchain-community==0.2.10
  pdfplumber==0.11.4
  pypdf==3.9.0
  streamlit==1.31.1
  streamlit-chat==0.0.2.2
  tiktoken==0.4.0
  youtube-transcript-api==0.6.0
  faiss-cpu==1.9.0
  requests==2.32.3
  bs4==0.0.2
  st-pages==0.5.0
  flask==2.0.2
  sentence-transformers==2.2.2
  torch==2.1.0
  pandas==2.3.3
  python-dotenv==1.2.4
  ```
- `.gitignore`: append `embeddings/` if it is not already present; do not remove existing lines.
- `streamlit_app.py`: remove every occurrence of `PandasAI` from the existing comment, changing only comment text. Do not change `paypal_donation_button()` or `generate_thumbnail(image_path, thumbnail_size=(500, 500))`.
- `tests/conftest.py`: create with:
  ```python
  import os
  import sys
  from pathlib import Path

  import pytest

  REPO_ROOT = Path(__file__).resolve().parents[1]
  if str(REPO_ROOT) not in sys.path:
      sys.path.insert(0, str(REPO_ROOT))

  def _embeddings_pkls() -> set[Path]:
      embeddings_dir = REPO_ROOT / "embeddings"
      if not embeddings_dir.is_dir():
          return set()
      return {path.resolve() for path in embeddings_dir.glob("*.pkl")}

  def _cleanup_embeddings(baseline: set[Path]) -> None:
      embeddings_dir = REPO_ROOT / "embeddings"
      if not embeddings_dir.is_dir():
          return
      for path in embeddings_dir.glob("*.pkl"):
          if path.resolve() not in baseline:
              path.unlink()

  @pytest.fixture(autouse=True)
  def _test_environment():
      baseline = _embeddings_pkls()
      os.environ["OPENAI_API_KEY"] = "sk-test"
      yield
      _cleanup_embeddings(baseline)
  ```
  `_test_environment` has no parameters and no production return value; it yields then removes only `.pkl` files absent from the per-test baseline, so pre-existing files are left alone and missing/empty `embeddings/` is a no-op.
- `tests/test_requirements.py`: create tests using a helper `_package_lines() -> list[str]` that reads `requirements.txt` with `encoding="utf-8-sig"`, strips whitespace, drops blank lines and lines whose `lstrip()` starts with `#`, and returns the remaining lines.
  - `test_removed_packages_absent`: package names from `line.split("==")[0]` contain none of `{"pandasai", "playwright", "pytube"}`.
  - `test_pandas_and_dotenv_at_end`: `_package_lines()[-2:] == ["pandas==2.3.3", "python-dotenv==1.2.4"]`.
  - `test_exact_order_and_pins`: `_package_lines()` equals the exact 18-line list above.
  - `test_no_cuda_packages`: for each package name, lower-cased name contains none of `("cuda", "cudnn", "cublas", "nccl")`.
  - `test_st_pages_exports`: executes `from st_pages import hide_pages, show_pages_from_config, add_page_title, show_pages, Page, Section`.
  - `test_gitignore_ignores_embeddings`: `"embeddings/"` is in `.gitignore` lines after stripping.
  - `test_streamlit_app_has_no_pandasai_mention`: `"PandasAI" not in Path("streamlit_app.py").read_text(encoding="utf-8")`.
- `tests/test_conftest.py`: create tests importing the conftest via:
  ```python
  import importlib.util
  from pathlib import Path

  def _load_conftest():
      spec = importlib.util.spec_from_file_location("sdlc_conftest", Path("tests/conftest.py"))
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)
      return module
  ```
  - `test_repo_root_on_sys_path`: `str(Path(__file__).resolve().parents[1]) in sys.path`.
  - `test_openai_api_key_is_test_key`: `os.environ["OPENAI_API_KEY"] == "sk-test"`.
  - `test_fixture_removes_probe_after_test`: create `embeddings/__pytest_cleanup_probe__.pkl`, assert it exists.
  - `test_fixture_probe_is_gone`: assert the same probe path does not exist; pytest file order makes this run after the creation test.
  - `test_cleanup_handles_missing_embeddings_dir(tmp_path, monkeypatch)`: load conftest, `monkeypatch.setattr(module, "REPO_ROOT", tmp_path)`, call `module._cleanup_embeddings(set())`, assert no exception and no `embeddings/` directory is created.
  - `test_cleanup_handles_empty_embeddings_dir(tmp_path, monkeypatch)`: create `tmp_path / "embeddings"`, patch `REPO_ROOT`, call `module._cleanup_embeddings(set())`, assert no exception.

**Definition of done:**
- [ ] `tests/test_requirements.py`, `test_removed_packages_absent`, `test_pandas_and_dotenv_at_end`, `test_exact_order_and_pins`, `test_no_cuda_packages`: prove spec behaviours 1–5 by parsing `requirements.txt` with `utf-8-sig`, asserting the exact ordered list, final two lines, no removed names, and no CUDA names.
- [ ] `tests/test_requirements.py`, `test_st_pages_exports`: proves spec behaviour 6 by importing all six `st_pages` names with no `ImportError`.
- [ ] `tests/test_requirements.py`, `test_gitignore_ignores_embeddings` and `test_streamlit_app_has_no_pandasai_mention`: prove spec behaviours 7–8.
- [ ] `tests/test_conftest.py`, `test_repo_root_on_sys_path` and `test_openai_api_key_is_test_key`: prove spec behaviours 9–10.
- [ ] `tests/test_conftest.py`, `test_fixture_removes_probe_after_test` followed by `test_fixture_probe_is_gone`: proves spec behaviour 11; the autouse fixture teardown removes the created `.pkl`.
- [ ] `tests/test_conftest.py`, `test_cleanup_handles_missing_embeddings_dir` and `test_cleanup_handles_empty_embeddings_dir`: prove spec behaviour 12 using `tmp_path` and `monkeypatch`; no server/thread cleanup is needed.
- [ ] The Verify command exits 0.

**Verify:**
```bash
python -m pytest tests/test_requirements.py tests/test_conftest.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 2: Import and Streamlit page smoke tests
<!-- phase: 2 -->
<!-- targets: tests/test_imports.py, tests/test_pages.py -->
<!-- frozen: docs/dependabot-remediation.md, sdlc/features/001-dependabot-remediation-piece-1-test-base/intent.md, sdlc/features/001-dependabot-remediation-piece-1-test-base/spec.md -->

**Goal:** Every `modules/*.py` module imports, and `AppTest.from_file(..., default_timeout=60).run()` records no exception for `streamlit_app.py` or any `pages/*.py`.

**Changes:**
- `tests/test_imports.py`: create:
  ```python
  import importlib
  from pathlib import Path

  import pytest

  MODULES = sorted(path for path in Path("modules").glob("*.py") if path.name != "__init__.py")

  @pytest.mark.parametrize("module_path", MODULES, ids=lambda path: path.stem)
  def test_every_module_imports(module_path: Path) -> None:
      importlib.import_module(f"modules.{module_path.stem}")
  ```
  No network or model loading is performed by import; `similarity.SimilarityScorer` is not instantiated.
- `tests/test_pages.py`: create:
  ```python
  from pathlib import Path

  import pytest
  from streamlit.testing.v1 import AppTest

  APP_PATHS = [Path("streamlit_app.py"), *sorted(Path("pages").glob("*.py"))]

  @pytest.mark.parametrize("app_path", APP_PATHS, ids=lambda path: str(path))
  def test_streamlit_file_runs_without_exception(app_path: Path) -> None:
      app = AppTest.from_file(str(app_path), default_timeout=60).run()
      assert len(app.exception) == 0
  ```
  The tests do not call buttons, upload files, or provide user input. `AppTest` runs in-process; no Streamlit server or teardown is required.

**Definition of done:**
- [ ] `tests/test_imports.py`, `test_every_module_imports` for every `modules/*.py`: proves spec behaviour 14; importing raises no exception.
- [ ] `tests/test_pages.py`, `test_streamlit_file_runs_without_exception` for `streamlit_app.py` and every `pages/*.py`: proves spec behaviours 15–16; `len(app.exception) == 0` for each path with no user interaction.
- [ ] The Verify command exits 0.

**Verify:**
```bash
python -m pytest tests/test_imports.py tests/test_pages.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 3: Similarity and Flask smoke tests
<!-- phase: 3 -->
<!-- targets: tests/test_similarity.py, tests/test_flask.py -->
<!-- frozen: docs/dependabot-remediation.md, sdlc/features/001-dependabot-remediation-piece-1-test-base/intent.md, sdlc/features/001-dependabot-remediation-piece-1-test-base/spec.md -->

**Goal:** `SimilarityScorer` returns the expected score ordering using the local model, and Flask `GET /` returns 200.

**Changes:**
- `tests/test_similarity.py`: create:
  ```python
  import pytest

  from modules.similarity import SimilarityScorer

  @pytest.fixture(scope="module")
  def scorer() -> SimilarityScorer:
      return SimilarityScorer()

  def test_identical_sentences_score_above_0_99(scorer: SimilarityScorer) -> None:
      sentence = "The quick brown fox jumps over the lazy dog."
      assert scorer.score(sentence, sentence) > 0.99

  def test_cat_variant_scores_higher_than_stock_prices(scorer: SimilarityScorer) -> None:
      cat_score = scorer.score("a cat sits on the mat", "a cat is sitting on a mat")
      stock_score = scorer.score("a cat sits on the mat", "stock prices fell today")
      assert cat_score > stock_score
  ```
  The fixture loads `./all-MiniLM-L6-v2` locally; no network, real OpenAI key, or GPU is used. No teardown is needed.
- `tests/test_flask.py`: create:
  ```python
  from flask_app import app

  def test_get_root_returns_200() -> None:
      with app.test_client() as client:
          response = client.get("/")
      assert response.status_code == 200
  ```
  The `with app.test_client()` context closes the test client after the request.

**Definition of done:**
- [ ] `tests/test_similarity.py`, `test_identical_sentences_score_above_0_99`: proves spec behaviour 17; identical sentence score is `> 0.99`.
- [ ] `tests/test_similarity.py`, `test_cat_variant_scores_higher_than_stock_prices`: proves spec behaviour 18 using the exact cat/stock sentence pair.
- [ ] `tests/test_flask.py`, `test_get_root_returns_200`: proves spec behaviour 19; Flask test client `GET /` status is `200`.
- [ ] The Verify command exits 0.

**Verify:**
```bash
python -m pytest tests/test_similarity.py tests/test_flask.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 4: Embedder smoke test
<!-- phase: 4 -->
<!-- targets: tests/test_embedder.py -->
<!-- frozen: docs/dependabot-remediation.md, sdlc/features/001-dependabot-remediation-piece-1-test-base/intent.md, sdlc/features/001-dependabot-remediation-piece-1-test-base/spec.md -->

**Goal:** The local Wales PDF produces exactly three FAISS similarity-search results using `FakeEmbeddings(size=8)`.

**Changes:**
- `tests/test_embedder.py`: create:
  ```python
  from pathlib import Path

  from langchain.text_splitter import RecursiveCharacterTextSplitter
  from langchain_community.document_loaders import PyPDFLoader
  from langchain_community.embeddings.fake import FakeEmbeddings
  from langchain_community.vectorstores import FAISS

  def test_wales_pdf_returns_three_similarity_documents() -> None:
      pdf_path = Path("playground/sample_documents/wales-in-world.pdf")
      documents = PyPDFLoader(str(pdf_path)).load()
      splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
      split_documents = splitter.split_documents(documents)
      vectors = FAISS.from_documents(split_documents, FakeEmbeddings(size=8))
      results = vectors.similarity_search("Wales", k=3)
      assert len(results) == 3
  ```
  This uses only the local fixture PDF and fake embeddings; no network, OpenAI key, or GPU is used. No file cleanup is needed because the test does not instantiate `Embedder`.

**Definition of done:**
- [ ] `tests/test_embedder.py`, `test_wales_pdf_returns_three_similarity_documents`: proves spec behaviour 20; `PyPDFLoader` loads the Wales PDF, `RecursiveCharacterTextSplitter(chunk_size=1000)` splits it, `FAISS.from_documents(..., FakeEmbeddings(size=8))` stores it, and `similarity_search("Wales", k=3)` returns exactly 3 documents.
- [ ] The Verify command exits 0.

**Verify:**
```bash
python -m pytest tests/test_embedder.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Risks
- The chosen exact pins for `pdfplumber`, `faiss-cpu`, `requests`, `bs4`, and `st-pages` may not match the newest/available releases on the pipeline index; the install step fails before tests, and Phase 1’s exact-string test catches any mismatch between the file and the plan.
- `st-pages==0.5.0` may not export all six names on the installed release; Phase 1’s `test_st_pages_exports` catches an `ImportError`.
- `AppTest` may surface a page exception caused by Streamlit or `st_pages` state; Phase 2’s page test reports the failing path.
- The local `all-MiniLM-L6-v2` model or Flask template may be missing or broken; Phase 3’s similarity/Flask tests catch that.
- `FakeEmbeddings` import path or PDF chunk count may differ from the approved facts; Phase 4’s embedder test catches that.
- The cleanup fixture could remove a pre-existing `.pkl` if baseline tracking is wrong; Phase 1’s probe test and baseline-based helper tests catch that.

## Open questions
- The exact `st-pages` release is not supplied in Facts. Assumption: pin `st-pages==0.5.0` as the newest planned release that exports all six imported names; the offline Phase 1 test verifies the export set rather than performing a network lookup.
- Exact pins for `pdfplumber`, `faiss-cpu`, `requests`, and `bs4` are not supplied in Facts. Assumption: use `pdfplumber==0.11.4`, `faiss-cpu==1.9.0`, `requests==2.32.3`, and `bs4==0.0.2`; if the pipeline index cannot resolve one, adjust the pin and the expected list in `tests/test_requirements.py` together.
- No pre-existing test files are visible in the repository snapshot. Assumption: the final `python -m pytest -q` run is the check for “existing tests still pass”; if hidden existing tests are present, they are frozen and not modified.
- The autouse fixture name and helper names are not specified. Assumption: use `_test_environment`, `_embeddings_pkls`, and `_cleanup_embeddings` as written in Phase 1.
- `FakeEmbeddings` is assumed to be importable from `langchain_community.embeddings.fake`, matching the installed `langchain-community==0.2.10`; the Phase 4 test catches any mismatch.

## Hand back
When every phase is built and its Verify block passes:
1. Create `sdlc/features/001-dependabot-remediation-piece-1-test-base/build-log.md` with one section per phase, in order. Head each
   one `## Phase <n>: <title>`, then list the files changed, the Verify command
   you ran and its result, and any deviation from this plan (or "none").
2. Commit it and push it to `feature/001-dependabot-remediation-piece-1-test-base`.

Commit only this plan's targets and `build-log.md`. Leave every other file alone,
including other features' documents under `sdlc/features/`, even for formatting;
verification fails on any file outside the targets.

The pipeline waits for this file. Once it has a section for every phase, it
verifies the whole branch and opens the pull request.

