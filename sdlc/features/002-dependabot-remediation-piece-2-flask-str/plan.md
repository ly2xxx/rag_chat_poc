<!-- sdlc stage=plan model=deepseek-v4.1-flash:cloud from=intent.md,spec.md,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#done,docs/dependabot-remediation.md#piece-2@8101db1 -->
## Approach
Make the smallest change that satisfies every “Done when” item: update the named dependency pins in place while preserving `requirements.txt` bytes, remove only the two Werkzeug `.trivyignore` blocks, add the required `PyPDFLoader` sample-PDF test, and upgrade Streamlit while keeping the existing `st-pages` menu if the existing compatibility test proves it still works. Only if an upgraded Flask/Streamlit import or API actually breaks do we touch `flask_app.py` or `modules/history.py`, and then only to restore the existing signatures and behaviour.

## Coverage

| Done when (intent.md) | Spec behaviours | Phase |
| :-- | :-- | :-- |
| `requirements.txt` keeps every line pinned with `==`, uses at least the named fixed versions, preserves order/BOM/CRLF, and `EXPECTED` matches. | 1, 2, 3, 4, 5, 6, 7, 18 | 1, 2, 3 |
| The Streamlit menu shows the same visible paths, titles and icons as the existing `show_pages` list with `download.py` and `refresh.py` omitted; if `st-pages` is removed, native `st.navigation`/`st.Page` is used and all `hide_pages` calls/imports are gone. | 8 (9–10 remain conditional; this plan retains `st-pages==0.5.0` and proves compatibility in Phase 3) | 3 |
| `.trivyignore` no longer contains the two Werkzeug IDs or their comment, and no other ignores change. | 11 | 1 |
| Any additional code changes forced by the upgrades are limited to `flask_app.py` and `modules/history.py` and preserve titles, widgets and behaviour. | 15 | 3 |
| `tests/test_pdf.py` loads each sample PDF in `playground/sample_documents/` with `PyPDFLoader` and asserts at least one page of non-empty text. | 16, 17 | 2 |
| The existing tests still pass. | 12, 13, 14, 18 | 1, 2, 3 |

## Phase 1: Flask, Werkzeug, requests and Werkzeug ignore removal
<!-- phase: 1 -->
<!-- targets: requirements.txt, .trivyignore, tests/test_requirements.py, tests/test_trivyignore.py -->
<!-- frozen: tests/conftest.py, tests/test_conftest.py, tests/test_flask.py, tests/test_imports.py, tests/test_pages.py, tests/test_embedder.py, tests/test_similarity.py, streamlit_app.py, pages/*.py -->

**Goal:** The Flask, Werkzeug and requests pins are fixed, the Werkzeug `.trivyignore` blocks are gone, and the requirements file is proven to be exactly pinned with BOM and CRLF endings.

**Changes:**
- `requirements.txt`: change only these three existing lines in place, preserving the existing order, UTF-8 BOM (`EF BB BF`) and CRLF endings:
  - `requests==2.32.3` → `requests==2.33.0`
  - `flask==2.0.2` → `flask==3.1.3`
  - `werkzeug==2.0.3` → `werkzeug==3.1.9`
  Keep `pypdf==3.9.0`, `streamlit==1.31.1`, `streamlit-chat==0.0.2.2`, `st-pages==0.5.0` and `pyarrow==25.0.0` unchanged in this phase. Do not reorder lines or remove the `# pywin32==308` comment.
- `.trivyignore`: remove exactly the two Werkzeug blocks whose comment mentions `werkzeug` and `piece 2`/`002`, together with the CVE ID line(s) immediately following each such comment. Preserve every other line exactly, including order and final newline.
- `tests/test_requirements.py`: update `EXPECTED` only for the three lines above. Keep all existing test function signatures and bodies unchanged except `EXPECTED`. Add two tests:
  - `def test_requirements_utf8_bom_and_crlf() -> None:` read `Path("requirements.txt").read_bytes()`; assert it starts with `b"\xef\xbb\xbf"`, ends with `b"\r\n"`, and after removing all `b"\r\n"` there is no remaining `b"\n"` or `b"\r"`.
  - `def test_every_package_line_has_exactly_one_pin() -> None:` for each line from `_package_lines()`, assert `line.count("==") == 1` and that none of `">="`, `"<="`, `"~="`, `"!="`, `";"`, `"["` appears in the line.
- `tests/test_trivyignore.py`: new file. Use `APPROVED_TAG = "sdlc/002-dependabot-remediation-piece-2-flask-str/approved"`. Implement `_approved_lines() -> list[str]` using `subprocess.run(["git", "show", f"{APPROVED_TAG}:.trivyignore"], check=True, capture_output=True, text=True).stdout.splitlines()`. Implement `_remove_werkzeug_blocks(lines: list[str]) -> list[str]` that walks comment-led blocks and drops a block when its comment lower-cases contains both `"werkzeug"` and either `"piece 2"` or `"002"`. Add `def test_werkzeug_ignores_removed_and_no_other_changes() -> None:` that asserts `_remove_werkzeug_blocks(approved) != approved`, then asserts `actual == expected` for `Path(".trivyignore").read_text().splitlines()`, and finally asserts no remaining line lower-cases contains `"werkzeug"`.

**Definition of done:**
- [ ] `tests/test_requirements.py`, test `test_requirements_utf8_bom_and_crlf`: proves spec behaviour 4 with the byte-level BOM/CRLF assertions above.
- [ ] `tests/test_requirements.py`, test `test_every_package_line_has_exactly_one_pin`: proves spec behaviour 1; every package line has exactly one `==` and no range/marker/extra specifier.
- [ ] `tests/test_requirements.py`, test `test_exact_order_and_pins`: proves spec behaviour 3 for the Phase 1 `EXPECTED`, with `pandas==2.3.3` and `python-dotenv==1.2.4` still last.
- [ ] `tests/test_trivyignore.py`, test `test_werkzeug_ignores_removed_and_no_other_changes`: proves spec behaviour 11 by comparing the current file against the approved-tag baseline with only the Werkzeug blocks removed.
- [ ] `tests/test_flask.py::test_get_root_returns_200`: proves spec behaviour 12 with `flask==3.1.3` and `werkzeug==3.1.9`; `GET /` returns status 200 using the existing `app.test_client()` context manager.

**Verify:**
```bash
python -m pytest tests/test_requirements.py tests/test_trivyignore.py tests/test_flask.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 2: pypdf upgrade and PDF loader regression
<!-- phase: 2 -->
<!-- targets: requirements.txt, tests/test_requirements.py, tests/test_pdf.py -->
<!-- frozen: .trivyignore, tests/test_trivyignore.py, tests/conftest.py, tests/test_conftest.py, tests/test_flask.py, tests/test_imports.py, tests/test_pages.py, tests/test_embedder.py, tests/test_similarity.py, streamlit_app.py, pages/*.py -->

**Goal:** `pypdf` is pinned at the fixed version and every sample PDF loads through `PyPDFLoader` with at least one non-empty page of text.

**Changes:**
- `requirements.txt`: change only `pypdf==3.9.0` → `pypdf==6.21.4`, preserving order, BOM and CRLF. No other lines change.
- `tests/test_requirements.py`: update only the `pypdf` entry in `EXPECTED` to `"pypdf==6.21.4"`. Keep all existing tests, including `test_st_pages_exports`, unchanged.
- `tests/test_pdf.py`: new pytest module using the existing LangChain loader import path:
```python
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

SAMPLE_DOCUMENTS = Path("playground/sample_documents")


def test_sample_pdfs_have_non_empty_text() -> None:
    pdf_paths = sorted(SAMPLE_DOCUMENTS.glob("*.pdf"))
    assert pdf_paths, f"No sample PDFs found in {SAMPLE_DOCUMENTS}"
    for pdf_path in pdf_paths:
        documents = PyPDFLoader(str(pdf_path)).load()
        assert documents, f"{pdf_path} produced no documents"
        assert any(document.page_content.strip() for document in documents), (
            f"{pdf_path} produced no page with non-empty text"
        )
```
No server, thread or mock teardown is needed; `PyPDFLoader` reads local files only.

**Definition of done:**
- [ ] `tests/test_pdf.py`, test `test_sample_pdfs_have_non_empty_text`: proves spec behaviours 16 and 17; it fails with the explicit “No sample PDFs found” assertion when `playground/sample_documents/` has no PDFs, and otherwise asserts `PyPDFLoader(path).load()` returns documents with at least one `page_content.strip()` for every sample PDF.
- [ ] `tests/test_requirements.py::test_exact_order_and_pins`: proves the Phase 2 `EXPECTED` includes `pypdf==6.21.4` in the original order.
- [ ] `tests/test_requirements.py::test_requirements_utf8_bom_and_crlf` and `test_every_package_line_has_exactly_one_pin`: prove the pypdf edit did not damage the file format.
- [ ] `tests/test_embedder.py::test_wales_pdf_returns_three_similarity_documents`: proves the existing `PyPDFLoader`/FAISS path still works with `pypdf==6.21.4`.

**Verify:**
```bash
python -m pytest tests/test_requirements.py tests/test_pdf.py tests/test_embedder.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 3: Streamlit 1.54 compatibility and forced fixes
<!-- phase: 3 -->
<!-- targets: requirements.txt, tests/test_requirements.py, flask_app.py, modules/history.py -->
<!-- frozen: .trivyignore, tests/test_trivyignore.py, tests/test_pdf.py, tests/conftest.py, tests/test_conftest.py, tests/test_flask.py, tests/test_imports.py, tests/test_pages.py, tests/test_embedder.py, tests/test_similarity.py, streamlit_app.py, pages/*.py -->

**Goal:** Streamlit is pinned at `1.54.0`, the existing `st-pages` menu and all existing page/import/Flask tests still pass, and any forced compatibility edit is confined to `flask_app.py` or `modules/history.py` without changing their public signatures.

**Changes:**
- `requirements.txt`: change only `streamlit==1.31.1` → `streamlit==1.54.0`. Keep `st-pages==0.5.0`, `streamlit-chat==0.0.2.2` and `pyarrow==25.0.0` unchanged. Preserve order, BOM and CRLF.
- `tests/test_requirements.py`: update only the `streamlit` entry in `EXPECTED` to `"streamlit==1.54.0"`. The final ordered `EXPECTED` must be:
```python
EXPECTED = [
    "langchain==0.2.11",
    "openai==0.27.7",
    "langchain-community==0.2.10",
    "pdfplumber==0.11.4",
    "pypdf==6.21.4",
    "streamlit==1.54.0",
    "streamlit-chat==0.0.2.2",
    "tiktoken==0.4.0",
    "youtube-transcript-api==0.6.0",
    "faiss-cpu==1.9.0",
    "requests==2.33.0",
    "bs4==0.0.2",
    "st-pages==0.5.0",
    "flask==3.1.3",
    "sentence-transformers==2.2.2",
    "torch==2.1.0",
    "pyarrow==25.0.0",
    "transformers==4.46.3",
    "huggingface-hub==0.25.2",
    "werkzeug==3.1.9",
    "pandas==2.3.3",
    "python-dotenv==1.2.4",
]
```
Keep `test_st_pages_exports` in place; it must still pass because this plan retains `st-pages==0.5.0`.
- `flask_app.py`: no change is planned. If and only if `tests/test_flask.py` or `tests/test_imports.py` fails because Flask/Werkzeug 3.1 removed or moved an import/API, make the minimal import/API adjustment only. Keep `def index()` and `def streamlit()` with the same names, no parameters, and the same return behaviour.
- `modules/history.py`: no change is planned. If and only if `tests/test_imports.py` or `tests/test_pages.py` fails because Streamlit 1.54 or `streamlit-chat==0.0.2.2` removed an API used by `ChatHistory`, make the minimal compatibility adjustment only. Keep `class ChatHistory` and every existing method name and signature exactly as listed in the spec: `__init__`, `default_greeting`, `default_prompt`, `initialize_user_history`, `initialize_assistant_history`, `initialize`, `reset`, `append`, `generate_messages`, `load`, `save`.

**Definition of done:**
- [ ] `tests/test_requirements.py::test_exact_order_and_pins`: proves the final ordered pins match `EXPECTED`, including `streamlit==1.54.0` and retained `st-pages==0.5.0`.
- [ ] `tests/test_requirements.py::test_requirements_utf8_bom_and_crlf` and `test_every_package_line_has_exactly_one_pin`: prove the Streamlit edit preserved BOM, CRLF and exact pin formatting.
- [ ] `tests/test_requirements.py::test_st_pages_exports`: proves `st-pages==0.5.0` still exports `hide_pages`, `show_pages_from_config`, `add_page_title`, `show_pages`, `Page` and `Section` under Streamlit 1.54.0.
- [ ] `tests/test_pages.py::test_streamlit_file_runs_without_exception`: proves spec behaviour 13 for every path in `APP_PATHS`; each `AppTest.from_file(str(app_path), default_timeout=60).run()` leaves `len(app.exception) == 0`.
- [ ] `tests/test_imports.py::test_every_module_imports`: proves spec behaviour 14; every `modules/*.py` except `__init__.py` imports successfully with the upgraded dependencies.
- [ ] `tests/test_flask.py::test_get_root_returns_200`: proves spec behaviour 12 still holds after the Streamlit upgrade.
- [ ] If `flask_app.py` or `modules/history.py` was edited, `tests/test_flask.py` and `tests/test_imports.py` prove the public names, call signatures and existing behaviour are preserved.

**Verify:**
```bash
python -m pytest tests/test_requirements.py tests/test_imports.py tests/test_pages.py tests/test_flask.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Risks
- `st-pages==0.5.0` may not be compatible with Streamlit 1.54.0. Phase 3’s `test_st_pages_exports` and `test_pages.py` checks would catch this. If they fail, stop and revise to the approved `st.navigation`/`st.Page` fallback rather than retrying the same pin.
- `streamlit-chat==0.0.2.2` may not be compatible with Streamlit 1.54.0. Phase 3’s `test_imports.py` and `test_pages.py` checks would catch this. The exact replacement pin is not in the facts, so a failure requires a plan revision.
- `pypdf==6.21.4` may break `langchain_community.document_loaders.PyPDFLoader` from `langchain-community==0.2.10`. Phase 2’s `tests/test_pdf.py` and `tests/test_embedder.py` would catch this.
- Editing `requirements.txt` can lose the UTF-8 BOM or CRLF endings. Phase 1, 2 and 3 requirements-format tests would catch this.
- `.trivyignore` block boundaries may differ from the assumed comment-above layout. Phase 1’s `tests/test_trivyignore.py` compares against the approved tag and would catch an incorrect removal or an accidental change.
- `pyarrow==25.0.0` may interact with the new Streamlit/NumPy stack. Phase 3’s `test_pages.py` and `test_imports.py` would catch an import/runtime failure.
- The existing `tests/test_pages.py` uses a 60-second default timeout and runs every page; Phase 3 may be slower than earlier phases, but still runs only the prescribed files.

## Open questions
- `.trivyignore` Werkzeug CVE IDs and exact comment text are not named in the facts. Assumption: the two blocks are comment-led blocks whose comment mentions `werkzeug` and `piece 2`/`002`; the new test encodes that assumption and compares against the approved tag.
- Whether `st-pages==0.5.0` works with Streamlit 1.54.0 is not established by the facts. Assumption: it remains compatible, so `streamlit_app.py` and `pages/*.py` stay unchanged and `test_st_pages_exports` remains. Phase 3 proves this. If it fails, the approved native-navigation fallback is not implemented in this plan and requires a plan revision.
- Whether `streamlit-chat==0.0.2.2` works with Streamlit 1.54.0 is not established by the facts. Assumption: it remains compatible; if not, the exact replacement pin is unknown and requires a plan revision.
- `pyarrow==25.0.0` is retained. The design permits moving it to a newer compatible release, but no newer target is named; retaining the existing pin is the smallest change.
- The PDF test function name is not specified by the intent. Assumption: `test_sample_pdfs_have_non_empty_text() -> None`, as stated in the spec’s Open questions.
- Exact `Page(path, name, icon)` values in `streamlit_app.py` are not reproduced in the facts. They are not needed in this plan because `st-pages` is retained; if a later revision uses the fallback, preserve the values from the existing file rather than inventing them.

## Hand back
When every phase is built and its Verify block passes:
1. Create `sdlc/features/002-dependabot-remediation-piece-2-flask-str/build-log.md` with one section per phase, in order. Head each
   one `## Phase <n>: <title>`, then list the files changed, the Verify command
   you ran and its result, and any deviation from this plan (or "none").
2. Commit it and push it to `feature/002-dependabot-remediation-piece-2-flask-str`.

Commit only this plan's targets and `build-log.md`. Leave every other file alone,
including other features' documents under `sdlc/features/`, even for formatting;
verification fails on any file outside the targets.

The pipeline waits for this file. Once it has a section for every phase, it
verifies the whole branch and opens the pull request.

