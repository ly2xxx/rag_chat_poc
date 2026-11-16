<!-- sdlc stage=plan model=deepseek-v4.1-flash:cloud from=intent.md,spec.md,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#done,docs/dependabot-remediation.md#piece-2@18a8e42 -->
## Approach
Move the non-Streamlit pins first so Flask, Werkzeug, requests and pypdf are proven without touching navigation, then upgrade Streamlit and replace the failing `st-pages` menu with the exact native `st.navigation`/`st.Page`/`st.page_link` structure while removing every `hide_pages` use, then delete only the Werkzeug `.trivyignore` block, and finally add the PDF-loader regression test. `flask_app.py` and `modules/history.py` stay frozen because the design checked they need no change.

## Coverage

| Done when (intent.md) | Spec behaviours | Phase |
| :-- | :-- | :-- |
| `requirements.txt` keeps every line pinned with `==`, uses at least the named fixed versions, stays installable, preserves order/BOM/CRLF, and `EXPECTED` matches. | 1–7; installability enforced by the verify job | 1, 2 |
| The Streamlit menu shows the same visible paths, titles and icons as the existing `show_pages` list, omits `download.py` and `refresh.py`, uses native navigation after removing `st-pages`, and has no `hide_pages` calls or imports. | 8–10 | 2 |
| `.trivyignore` no longer contains the two Werkzeug IDs or their comment, and no other ignores change. | 11 | 3 |
| Any additional code changes forced by upgrades are limited to `flask_app.py` and `modules/history.py` and preserve titles, widgets and behaviour. | 12, 15 | 1, 2; both files frozen, design says no changes needed |
| `tests/test_pdf.py` loads each sample PDF in `playground/sample_documents/` with `PyPDFLoader` and asserts non-empty text. | 16, 17 | 4 |
| The existing tests still pass. | 18 | 1–4; final `python -m pytest -q` |

## Phase 1: Update non-Streamlit pins

<!-- phase: 1 -->
<!-- targets: requirements.txt, tests/test_requirements.py -->
<!-- frozen: flask_app.py, modules/history.py, streamlit_app.py, pages/0_Keywords-Research-beta.py, pages/1_Robby-Chat-file.py, pages/2_Robby-Chat-web.py, pages/3_Robby-Youtube.py, pages/4_Text-Similarity-beta.py, tests/conftest.py, tests/test_conftest.py, tests/test_embedder.py, tests/test_flask.py, tests/test_imports.py, tests/test_pages.py, tests/test_similarity.py -->

**Goal:** Flask, Werkzeug, requests and pypdf move to the approved floors, while Streamlit and `st-pages` remain untouched and Flask plus PDF loading still work.

**Changes:**
- `requirements.txt`: read as bytes and replace exactly one occurrence of each:
  - `b"pypdf==3.9.0"` → `b"pypdf==6.21.4"`
  - `b"requests==2.32.3"` → `b"requests==2.33.0"`
  - `b"flask==2.0.2"` → `b"flask==3.1.3"`
  - `b"werkzeug==2.0.3"` → `b"werkzeug==3.1.9"`
  Do not reorder lines, remove `st-pages==0.5.0`, or change `streamlit==1.31.1`, `streamlit-chat==0.0.2.2`, or `pyarrow==25.0.0`. Write the bytes back so the UTF-8 BOM and CRLF endings remain.
- `tests/test_requirements.py`: update `EXPECTED` to exactly this interim ordered list:
  ```python
  EXPECTED = [
      "langchain==0.2.11",
      "openai==0.27.7",
      "langchain-community==0.2.10",
      "pdfplumber==0.11.4",
      "pypdf==6.21.4",
      "streamlit==1.31.1",
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
  Add `test_requirements_keeps_utf8_bom_and_crlf() -> None` that reads `Path("requirements.txt").read_bytes()`, asserts `raw.startswith(b"\xef\xbb\xbf")`, and asserts `raw.count(b"\n") == raw.count(b"\r\n")`.

**Definition of done:**
- [ ] `tests/test_requirements.py`, test `test_exact_order_and_pins`: `_package_lines()` equals the interim `EXPECTED` list above, proving the new non-Streamlit pins and preserved order.
- [ ] `tests/test_requirements.py`, test `test_requirements_keeps_utf8_bom_and_crlf`: asserts BOM and every LF is part of CRLF, proving spec behaviour 4 after byte edits.
- [ ] `tests/test_flask.py`, existing test `test_get_root_returns_200`: `GET /` still returns 200 with Flask 3.1.3/Werkzeug 3.1.9.
- [ ] `tests/test_embedder.py`, existing test `test_wales_pdf_returns_three_similarity_documents`: `PyPDFLoader` still loads the local PDF under pypdf 6.21.4.
- [ ] `tests/test_imports.py`, existing test `test_every_module_imports`: every `modules/*.py` module still imports, including `modules/history.py`.

**Verify:**
```bash
python -m pytest tests/test_requirements.py tests/test_flask.py tests/test_imports.py tests/test_embedder.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 2: Upgrade Streamlit and use native navigation

<!-- phase: 2 -->
<!-- targets: requirements.txt, streamlit_app.py, pages/0_Keywords-Research-beta.py, pages/1_Robby-Chat-file.py, pages/2_Robby-Chat-web.py, pages/3_Robby-Youtube.py, pages/4_Text-Similarity-beta.py, tests/test_requirements.py, tests/test_navigation.py -->
<!-- frozen: flask_app.py, modules/history.py, pages/download.py, pages/refresh.py, tests/conftest.py, tests/test_conftest.py, tests/test_embedder.py, tests/test_flask.py, tests/test_imports.py, tests/test_pages.py, tests/test_similarity.py, .trivyignore -->

**Goal:** Streamlit 1.54.0 runs without `st-pages`, the visible menu has the expected six links, hidden `download.py` and `refresh.py` stay hidden, and all pages run without exceptions.

**Changes:**
- `requirements.txt`: read as bytes, replace exactly one `b"streamlit==1.31.1"` with `b"streamlit==1.54.0"`, and remove exactly one `b"st-pages==0.5.0\r\n"`. Preserve BOM and CRLF.
- `tests/test_requirements.py`: replace `EXPECTED` with exactly:
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
  Delete the `test_st_pages_exports` function. Keep `test_requirements_keeps_utf8_bom_and_crlf`.
- `streamlit_app.py`: remove the `st_pages` import. Remove `add_page_title()`, `show_pages_from_config()`, `show_pages([...])`, and `hide_pages(...)`. Move all remaining top-level UI code that followed those calls into `def home() -> None:` whose first statement is `st.title("🏠 Home")`. Keep `paypal_donation_button()` and `generate_thumbnail(image_path, thumbnail_size=(500, 500))` unchanged. Append exactly this navigation shape, copying each existing visible icon string from the old `show_pages` entries:
  ```python
  MENU = [
      st.Page(home, title="Home", icon="🏠", default=True),
      st.Page("pages/0_Keywords-Research-beta.py", title="Keywords-Research", icon=<existing icon>),
      st.Page("pages/1_Robby-Chat-file.py", title="Robby-Chat-file", icon=<existing icon>),
      st.Page("pages/2_Robby-Chat-web.py", title="Robby-Chat-web", icon=<existing icon>),
      st.Page("pages/3_Robby-Youtube.py", title="Robby-Summary-youtube", icon=<existing icon>),
      st.Page("pages/4_Text-Similarity-beta.py", title="Text-Similarity-score(beta)", icon=<existing icon>),
  ]
  HIDDEN = [
      st.Page("pages/download.py", title="down", icon=":material/download:"),
      st.Page("pages/refresh.py", title="ref", icon=":material/refresh:"),
  ]
  page = st.navigation(MENU + HIDDEN, position="hidden")
  with st.sidebar:
      for item in MENU:
          st.page_link(item)
  page.run()
  ```
- `pages/0_Keywords-Research-beta.py`, `pages/1_Robby-Chat-file.py`, `pages/2_Robby-Chat-web.py`, `pages/3_Robby-Youtube.py`, `pages/4_Text-Similarity-beta.py`: remove `from st_pages import hide_pages` and `hide_pages(["down", "ref"])` wherever present. Change nothing else.
- `tests/test_navigation.py`: new pytest module with:
  ```python
  from pathlib import Path
  from streamlit.testing.v1 import AppTest

  EXPECTED_LINKS = [
      "Home",
      "Keywords-Research",
      "Robby-Chat-file",
      "Robby-Chat-web",
      "Robby-Summary-youtube",
      "Text-Similarity-score(beta)",
  ]

  def test_home_menu_has_visible_page_links() -> None:
      at = AppTest.from_file("streamlit_app.py", default_timeout=60).run()
      assert len(at.exception) == 0
      assert [title.value for title in at.title] == ["🏠 Home"]
      assert [link.proto.label for link in at.sidebar.page_link] == EXPECTED_LINKS

  def test_text_similarity_page_switches_without_exception() -> None:
      at = AppTest.from_file("streamlit_app.py", default_timeout=60).run()
      at.switch_page("pages/4_Text-Similarity-beta.py").run()
      assert len(at.exception) == 0

  def test_no_st_pages_imports_outside_playground() -> None:
      needle = "st_" + "pages"
      offenders = [
          str(path)
          for path in Path(".").rglob("*.py")
          if "playground" not in path.parts
          and needle in path.read_text(encoding="utf-8", errors="ignore")
      ]
      assert offenders == []
  ```

**Definition of done:**
- [ ] `tests/test_requirements.py`, test `test_exact_order_and_pins`: final `EXPECTED` above, with `streamlit==1.54.0` and no `st-pages`.
- [ ] `tests/test_requirements.py`, test `test_requirements_keeps_utf8_bom_and_crlf`: still proves BOM and CRLF after the Streamlit/`st-pages` byte edits.
- [ ] `tests/test_navigation.py`, test `test_home_menu_has_visible_page_links`: `AppTest` loads `streamlit_app.py`, has no exception, shows title `"🏠 Home"`, and exactly six sidebar page links with labels `Home`, `Keywords-Research`, `Robby-Chat-file`, `Robby-Chat-web`, `Robby-Summary-youtube`, `Text-Similarity-score(beta)`.
- [ ] `tests/test_navigation.py`, test `test_text_similarity_page_switches_without_exception`: `switch_page("pages/4_Text-Similarity-beta.py")` runs with `len(at.exception) == 0` after `hide_pages` removal.
- [ ] `tests/test_navigation.py`, test `test_no_st_pages_imports_outside_playground`: no `.py` file outside `playground/` contains the contiguous string `st_pages`, including page 1 and the hidden pages.
- [ ] `tests/test_pages.py`, existing test `test_streamlit_file_runs_without_exception`: every path in `APP_PATHS` completes with `len(app.exception) == 0` under Streamlit 1.54.0.

**Verify:**
```bash
python -m pytest tests/test_requirements.py tests/test_navigation.py tests/test_pages.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 3: Remove Werkzeug trivy ignores

<!-- phase: 3 -->
<!-- targets: .trivyignore, tests/test_trivyignore.py -->
<!-- frozen: requirements.txt, streamlit_app.py, pages/0_Keywords-Research-beta.py, pages/1_Robby-Chat-file.py, pages/2_Robby-Chat-web.py, pages/3_Robby-Youtube.py, pages/4_Text-Similarity-beta.py, pages/download.py, pages/refresh.py, flask_app.py, modules/history.py, tests/conftest.py, tests/test_conftest.py, tests/test_embedder.py, tests/test_flask.py, tests/test_imports.py, tests/test_navigation.py, tests/test_pages.py, tests/test_requirements.py, tests/test_similarity.py -->

**Goal:** `.trivyignore` loses only the Werkzeug comment and its two CVE entries, leaving six non-comment CVE lines and no Werkzeug reference.

**Changes:**
- `.trivyignore`: find the single comment line whose text names Werkzeug and says this piece removes it. Remove that comment line and the two immediately following non-comment CVE lines. Preserve every other line and the existing line endings byte-for-byte.
- `tests/test_trivyignore.py`: add:
  ```python
  from pathlib import Path

  def test_werkzeug_ignores_and_comment_removed() -> None:
      lines = [
          line.strip()
          for line in Path(".trivyignore").read_text(encoding="utf-8").splitlines()
          if line.strip()
      ]
      assert not any("werkzeug" in line.lower() for line in lines)
      cve_lines = [line for line in lines if not line.startswith("#")]
      assert len(cve_lines) == 6
  ```

**Definition of done:**
- [ ] `tests/test_trivyignore.py`, test `test_werkzeug_ignores_and_comment_removed`: no line contains `werkzeug` case-insensitively, and exactly six non-comment CVE lines remain, proving the Werkzeug comment plus two IDs were removed and no other CVE lines were added or removed.

**Verify:**
```bash
python -m pytest tests/test_trivyignore.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 4: Add PDF loader regression

<!-- phase: 4 -->
<!-- targets: tests/test_pdf.py -->
<!-- frozen: requirements.txt, streamlit_app.py, pages/0_Keywords-Research-beta.py, pages/1_Robby-Chat-file.py, pages/2_Robby-Chat-web.py, pages/3_Robby-Youtube.py, pages/4_Text-Similarity-beta.py, pages/download.py, pages/refresh.py, .trivyignore, flask_app.py, modules/history.py, tests/conftest.py, tests/test_conftest.py, tests/test_embedder.py, tests/test_flask.py, tests/test_imports.py, tests/test_navigation.py, tests/test_pages.py, tests/test_requirements.py, tests/test_similarity.py, tests/test_trivyignore.py -->

**Goal:** Every local sample PDF loads with `PyPDFLoader` and yields at least one page of non-empty text.

**Changes:**
- `tests/test_pdf.py`: add:
  ```python
  from pathlib import Path
  from langchain_community.document_loaders import PyPDFLoader

  def test_sample_pdfs_have_non_empty_text() -> None:
      pdf_paths = sorted(Path("playground/sample_documents").glob("*.pdf"))
      assert pdf_paths, "Expected at least one sample PDF in playground/sample_documents"
      for pdf_path in pdf_paths:
          documents = PyPDFLoader(str(pdf_path)).load()
          assert any(
              document.page_content.strip() for document in documents
          ), f"No non-empty text in {pdf_path}"
  ```

**Definition of done:**
- [ ] `tests/test_pdf.py`, test `test_sample_pdfs_have_non_empty_text`: asserts at least one `playground/sample_documents/*.pdf` exists, then for each PDF asserts `PyPDFLoader(path).load()` returns at least one document whose `page_content.strip()` is non-empty.

**Verify:**
```bash
python -m pytest tests/test_pdf.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Risks

- pypdf 6.21.4 may change `PyPDFLoader` behaviour; Phase 1’s `tests/test_embedder.py` check catches it.
- Flask 3.1.3/Werkzeug 3.1.9 may expose a compatibility problem; Phase 1’s `tests/test_flask.py` and `tests/test_imports.py` checks catch it.
- Streamlit 1.54.0 may change `AppTest`, `st.Page`, `st.navigation`, or sidebar page-link behaviour; Phase 2’s `tests/test_navigation.py` and `tests/test_pages.py` checks catch it.
- A page may still import or call `hide_pages`; Phase 2’s `test_no_st_pages_imports_outside_playground` catches it.
- BOM or CRLF may be lost during byte edits; Phase 1 and Phase 2’s `test_requirements_keeps_utf8_bom_and_crlf` catch it.
- `.trivyignore` may have a different comment/entry layout than expected; Phase 3’s count and Werkzeug-text assertions catch it.
- Sample PDFs may be absent or empty; Phase 4’s `test_sample_pdfs_have_non_empty_text` catches both.

## Open questions

- Exact visible `Page(..., icon=...)` strings are not reproduced in the provided facts. Assumption: copy the existing icon string for each visible page from the current `show_pages([...])` call in `streamlit_app.py`; do not translate them. Phase 2’s menu test checks labels and execution, not icon glyph equality.
- Exact Werkzeug CVE IDs and comment text are not named in the facts. Assumption: remove the single comment line naming Werkzeug and its two immediately following CVE lines; Phase 3 asserts no Werkzeug text remains and six non-comment CVE lines remain.
- `flask_app.py` and `modules/history.py` need no changes per the approved design, so this plan freezes them. If a forced compatibility change appears, Phase 1 checks fail and the plan must be revised rather than editing them silently.
- `tests/test_navigation.py` assumes Streamlit 1.54’s `AppTest` exposes sidebar page links as `at.sidebar.page_link` with `link.proto.label`. If the 1.54 testing accessor differs, Phase 2 fails and this plan should be revised.

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

