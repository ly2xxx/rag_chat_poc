<!-- sdlc stage=spec model=deepseek-v4.1-flash:cloud from=intent.md,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#done,docs/dependabot-remediation.md#piece-2@5ec8f9c -->
## Summary
This change updates the Python dependency pins for Flask, Streamlit, pypdf, Werkzeug and requests to the approved fixed versions, while preserving the existing Flask and Streamlit page behaviour and menu. It also removes the two Werkzeug `.trivyignore` entries owned by this piece and adds an offline PDF-loader regression test.

## Behaviour
1. Given `requirements.txt`, when non-comment package lines are read, then every line is pinned with exactly one `==` and contains no version range, environment marker or extra specifier.
2. Given the lowest-satisfying-pin assumption, when `requirements.txt` is read, then it contains `flask==3.1.3`, `streamlit==1.54.0`, `pypdf==6.21.4`, `werkzeug==3.1.9` and `requests==2.33.0`.
3. Given `requirements.txt`, when `tests/test_requirements.py::test_exact_order_and_pins` runs, then the ordered package lines equal `EXPECTED`, with `pandas==2.3.3` and `python-dotenv==1.2.4` still last.
4. Given `requirements.txt`, when read as bytes, then it still starts with the UTF-8 BOM and every line ending is CRLF.
5. Given `requirements.txt`, when `tests/test_requirements.py::test_no_cuda_packages` runs, then no package name contains `cuda`, `cudnn`, `cublas` or `nccl`.
6. Given `streamlit-chat` is present, when `requirements.txt` is read, then it remains `streamlit-chat==0.0.2.2` unless Streamlit 1.54.0 requires a different exact pin, and any changed pin is recorded in `EXPECTED`.
7. Given `pyarrow` is present, when `requirements.txt` is read, then it is pinned with `==` to the newest version compatible with the other pins, and that exact pin is recorded in `EXPECTED`.
8. Given `st-pages==0.5.0` remains compatible with Streamlit 1.54.0, when `streamlit_app.py` is read, then its existing `show_pages([...])` menu is unchanged and still omits `download.py` and `refresh.py`.
9. Given `st-pages==0.5.0` is incompatible and removed, when `streamlit_app.py` is read, then it contains no `st_pages` import and no `hide_pages` import or call, and builds the menu with `st.navigation` and `st.Page` entries preserving the existing paths, titles and icons except `download.py` and `refresh.py`.
10. Given `st-pages==0.5.0` is removed, when every file under `pages/` is read, then no file imports or calls `hide_pages`, including `pages/0_Keywords-Research-beta.py`, `pages/2_Robby-Chat-web.py`, `pages/3_Robby-Youtube.py` and `pages/4_Text-Similarity-beta.py`.
11. Given `.trivyignore`, when compared with its pre-change content, then the two Werkzeug CVE entries and their comment are absent and every other line is unchanged.
12. Given the updated dependency pins, when `tests/test_flask.py::test_get_root_returns_200` runs, then `GET /` returns status 200.
13. Given the updated dependency pins, when `tests/test_pages.py::test_streamlit_file_runs_without_exception` runs for every path in `APP_PATHS`, then each app completes with `len(app.exception) == 0`.
14. Given the updated dependency pins, when `tests/test_imports.py::test_every_module_imports` runs, then every `modules/*.py` module except `__init__.py` imports successfully.
15. Given the upgraded dependencies, when `flask_app.py` and `modules/history.py` are inspected, then `index()`, `streamlit()` and every existing `ChatHistory` method keep their current names, parameters and return behaviour.
16. Given `playground/sample_documents/scotland_welcome_to_our_life.pdf` and `playground/sample_documents/wales-in-world.pdf`, when `tests/test_pdf.py` runs, then `PyPDFLoader(path).load()` returns at least one document whose `page_content.strip()` is non-empty for each PDF.
17. Given `playground/sample_documents/` contains no PDF files, when `tests/test_pdf.py` runs, then it fails with an assertion that at least one sample PDF was found.
18. Given the earlier piece 1 tests except `EXPECTED`, when pytest runs from the repository root, then they pass unchanged.

## Interfaces
- **`requirements.txt`** — change only existing pin lines. The required pins are `flask==3.1.3`, `streamlit==1.54.0`, `pypdf==6.21.4`, `werkzeug==3.1.9` and `requests==2.33.0`. `pyarrow==25.0.0`, `streamlit-chat==0.0.2.2` and `st-pages==0.5.0` may change or be removed only as allowed by the design; exact unresolved values are listed under Open questions.
- **`streamlit_app.py`** — no new local functions or signature changes. Existing `paypal_donation_button()` and `generate_thumbnail(image_path, thumbnail_size=(500, 500))` remain unchanged. If the `st-pages` fallback is used, replace the `show_pages([...])` call with `st.navigation` over `st.Page` entries, and remove the `hide_pages` import and call; no local API is added.
- **`pages/0_Keywords-Research-beta.py`, `pages/2_Robby-Chat-web.py`, `pages/3_Robby-Youtube.py`, `pages/4_Text-Similarity-beta.py`** — if the `st-pages` fallback is used, remove the `from st_pages import hide_pages` import and the `hide_pages(["down", "ref"])` call. No function signatures change.
- **`.trivyignore`** — remove the two Werkzeug CVE entries and their comment. No code interface.
- **`flask_app.py`** — keep `index()` and `streamlit()` unchanged; modify only if the upgraded Flask/Werkzeug forces it. No new names or signature changes.
- **`modules/history.py`** — keep `class ChatHistory` and its existing method signatures unchanged: `__init(self)`, `default_greeting(self)`, `default_prompt(self, topic)`, `initialize_user_history(self)`, `initialize_assistant_history(self, uploaded_file)`, `initialize(self, uploaded_file)`, `reset(self, uploaded_file)`, `append(self, mode, message)`, `generate_messages(self, container)`, `load(self)`, `save(self)`. Modify only if the upgraded dependencies force it.
- **`tests/test_requirements.py`** — update `EXPECTED: list[str]` to the exact ordered package lines. Keep `_package_lines() -> list[str]` and the existing test function signatures unchanged, except for the `EXPECTED` values.
- **`tests/test_pdf.py`** — new pytest module with `def test_sample_pdfs_have_non_empty_text() -> None:`; the function name is a proposed name because the intent does not specify one. It must use `PyPDFLoader` and local sample PDFs only.

## Out of scope
- Dependabot alerts or upgrades for packages this piece does not name, including torch, sentence-transformers, transformers, langchain and langchain-community.
- Modifying `playground/`, the notebooks, `Gallery/`, `.devcontainer/`, `.github/`, or the pipeline’s install command; `tests/test_pdf.py` may only read the existing sample PDFs.
- Adding CUDA packages or changing the CPU-only torch setup.
- Refactoring, new features, changing page titles/widgets/behaviour, deleting `download.py` or `refresh.py`, or removing `st-pages` when it remains compatible.
- Rewriting earlier tests beyond updating `EXPECTED`, or adding tests unrelated to PDF loading.
- Other `.trivyignore` entries, including the transformer IDs from piece 1.

## Open questions
- The two Werkzeug CVE IDs and their comment text are not named in the facts; assumption: they are the existing `.trivyignore` entries whose comments say this piece removes them, and no other lines change.
- The exact `pyarrow` target and whether `streamlit-chat` must change are not fixed by the facts; assumption: use the newest compatible `pyarrow` pin and change `streamlit-chat` only if Streamlit 1.54.0 requires it, recording both in `EXPECTED`.
- The exact PDF test function name is not given; assumption: `test_sample_pdfs_have_non_empty_text() -> None`.
- The eight `Page(path, name, icon)` values are not reproduced in the provided facts; assumption: preserve the values already present in `streamlit_app.py`.
- If `st-pages` is removed, `tests/test_requirements.py::test_st_pages_exports` cannot pass unchanged, which conflicts with “existing tests still pass” except `EXPECTED`; assumption: removing or skipping that test is permitted only as the forced consequence of the approved fallback.
- Installability with the approved Python 3.11 command requires the network and is a CI pipeline gate, not a network-free pytest criterion.
