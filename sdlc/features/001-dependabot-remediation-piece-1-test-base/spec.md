<!-- sdlc stage=spec model=deepseek-v4.1-flash:cloud from=intent.md,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#piece-1@90bc5d5 -->
## Summary
This piece adds a pytest smoke-test baseline under `tests/` for module imports, Streamlit pages, similarity scoring, Flask, and the embedder. It removes unused PandasAI, Playwright, and PyTube dependencies, adds pinned `pandas` and `python-dotenv`, pins `st-pages` to a compatible release, ignores generated `embeddings/`, and removes the PandasAI mention from `streamlit_app.py`. The change is for maintainers running dependency remediation on Python 3.11 with the CPU-only install path.

## Behaviour
1. Given `requirements.txt`, when its package lines are inspected, then `pandasai`, `playwright`, and `pytube` do not appear.
2. Given `requirements.txt`, when its trailing package lines are inspected, then `pandas==2.3.3` and `python-dotenv==1.2.4` are present at the end.
3. Given `requirements.txt`, when compared with its prior version, then all existing non-removed lines keep their relative order and new package lines are appended at the end.
4. Given `requirements.txt`, when each non-comment package line is parsed, then it uses `==` and no line names a CUDA-specific package.
5. Given `requirements.txt`, when the `st-pages` line is parsed, then it is an exact `==` pin.
6. Given the pinned `st-pages` package is installed, when Python imports `hide_pages`, `show_pages_from_config`, `add_page_title`, `show_pages`, `Page`, and `Section` from `st_pages`, then no `ImportError` occurs.
7. Given `streamlit_app.py`, when its text is searched, then `PandasAI` does not occur.
8. Given `.gitignore`, when its lines are read, then `embeddings/` is present.
9. Given the test suite is run from the repository root, when a test reads `sys.path`, then the repository root path is present.
10. Given any test in `tests/`, when it reads `os.environ["OPENAI_API_KEY"]`, then the value is `sk-test`.
11. Given a test creates `embeddings/<name>.pkl`, when the autouse fixture tears down, then that `.pkl` file no longer exists.
12. Given the `embeddings/` directory is missing or contains no `.pkl` files, when the cleanup fixture runs, then it completes without error.
13. Given `tests/`, when its contents are listed, then `conftest.py`, `test_imports.py`, `test_pages.py`, `test_similarity.py`, `test_flask.py`, and `test_embedder.py` exist.
14. Given every Python module file under `modules/`, when each module is imported in a test, then no exception is raised.
15. Given `streamlit_app.py`, when `AppTest.from_file("streamlit_app.py", default_timeout=60).run()` is called without user input, then no exception is recorded.
16. Given each `pages/*.py` path, when `AppTest.from_file(path, default_timeout=60).run()` is called without user input, then no exception is recorded for that path.
17. Given two identical sentences, when `SimilarityScorer().score(sentence, sentence)` is called, then the returned score is greater than `0.99`.
18. Given `"a cat sits on the mat"`, `"a cat is sitting on a mat"`, and `"stock prices fell today"`, when `SimilarityScorer().score` is called for the cat-variant pair and the stock-price pair, then the cat-variant score is greater than the stock-price score.
19. Given `flask_app.app`, when a test client sends `GET /`, then the response status code is `200`.
20. Given `playground/sample_documents/wales-in-world.pdf`, when loaded with `PyPDFLoader`, split with `RecursiveCharacterTextSplitter(chunk_size=1000)`, stored with `FAISS.from_documents(docs, FakeEmbeddings(size=8))`, and queried with `similarity_search("Wales", k=3)`, then exactly 3 documents are returned.
21. Given the test suite is run with no network, no real OpenAI key, and no GPU, when pytest completes, then it exits successfully.
22. Given the tests that existed before this piece, when the full pytest suite runs, then those tests still pass unchanged.

## Interfaces

**`requirements.txt`**
- Remove `pandasai==0.2.15`, `playwright==1.42.0`, and `pytube==15.0.0`.
- Change `st-pages>=0.4.3` to an exact `st-pages==` pin for the newest release that exports all six names imported by `streamlit_app.py`; the exact version is unresolved in Facts (see Open questions).
- Append `pandas==2.3.3` and `python-dotenv==1.2.4` at the end.
- Every remaining non-comment package line must use `==`; exact pins for currently unpinned `pdfplumber`, `faiss-cpu`, `requests`, and `bs4` are unresolved in Facts (see Open questions).

**`.gitignore`**
- Add the line `embeddings/`.

**`streamlit_app.py`**
- Remove the `PandasAI` mention from the existing comment. No signature changes to:
  - `def paypal_donation_button()`
  - `def generate_thumbnail(image_path, thumbnail_size=(500, 500))`

**`tests/conftest.py`**
- Add pytest configuration that puts the repository root on `sys.path`.
- Add an autouse pytest fixture with no parameters and no production return value; it sets `OPENAI_API_KEY=sk-test` for every test and removes `embeddings/*.pkl` files created by tests. The fixture name is not specified by Facts (see Open questions).

**New pytest modules**
- `tests/test_imports.py`: imports every module under `modules/`.
- `tests/test_pages.py`: uses `AppTest.from_file(path, default_timeout=60).run()` for `streamlit_app.py` and each `pages/*.py`.
- `tests/test_similarity.py`: exercises `SimilarityScorer().score(text1, text2)` through the criteria above.
- `tests/test_flask.py`: exercises `flask_app.app` with a Flask test client and `GET /`.
- `tests/test_embedder.py`: exercises `PyPDFLoader`, `RecursiveCharacterTextSplitter(chunk_size=1000)`, `FAISS.from_documents(docs, FakeEmbeddings(size=8))`, and `similarity_search("Wales", k=3)`.
- No production API signatures change in `modules/`, `app/__main__.py`, `flask_app.py`, or the pages.

## Out of scope
- Upgrades for Dependabot alerts in packages this piece does not name, including `torch`, `sentence-transformers`, `pypdf`, `flask`, `langchain`, `langchain-community`, and `streamlit`.
- Refactoring, new application features, or changes to page titles, widgets, or behaviour.
- CUDA packages or any non-CPU torch installation path.
- `playground/`, the notebooks, `Gallery/`, `.devcontainer/`, and `.github/`.
- Cleaning unused packages beyond `pandasai`, `playwright`, and `pytube`.
- Changing `modules/utils.py: Utilities.load_api_key()` behaviour or real OpenAI integration.
- Modifying tests that existed before this piece.

## Open questions
- The exact `st-pages` version is not supplied in Facts. Assumption: pin the newest release that exports all six imported names; the offline test verifies the export set, not a network lookup for newest.
- Exact pins for currently unpinned `pdfplumber`, `faiss-cpu`, `requests`, and `bs4` are not supplied in Facts, while every line must use `==`. Assumption: those pins must be supplied with the implementation; this spec does not invent versions.
- The autouse fixture name and individual pytest function names are not specified. Assumption: use pytest’s default `test_*` discovery and keep the fixture internal to `tests/conftest.py`.
- Cleanup scope for pre-existing `embeddings/*.pkl` files is not explicit. Assumption: remove only files created during the test session and leave pre-existing files alone.
- Installability of every pin on Python 3.11 with the pipeline install command cannot be proven by offline pytest. Assumption: the pipeline install step validates installation; pytest verifies exact pins and the absence of CUDA package names.
