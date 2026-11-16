<!-- sdlc stage=intent model=deepseek-v4.1-flash:cloud from=idea,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#done,docs/dependabot-remediation.md#piece-2@c5b2a0b -->
# Intent: Dependabot remediation piece 2: Flask, Streamlit and pypdf

**Owner:** @ly2xxx · **Status:** proposed (approving the review gate approves it)

## Problem
The repository still carries open Dependabot alerts for Flask, Streamlit and pypdf, with related pinned Werkzeug and requests versions keeping those alerts and unsupported packages in place. That leaves maintainers and users exposed to known dependency issues and makes a clean Python 3.11 install and test run harder to trust.

## Outcome
Flask, Streamlit, pypdf, Werkzeug and requests are pinned at or above the approved fixed versions, with `streamlit-chat` and `pyarrow` changed only as the design allows, while the existing Flask and Streamlit app behaviour, page titles and widgets are preserved. If the pinned `st-pages` cannot work with the new Streamlit, the menu is built with native Streamlit navigation using the same visible paths, titles and icons, with `download.py` and `refresh.py` left out, and `.trivyignore` no longer carries the Werkzeug ignores removed by this piece. The work most likely lands in `requirements.txt`, `streamlit_app.py`, `.trivyignore`, `flask_app.py`, `modules/history.py` and a new `tests/test_pdf.py`.

## Done when
- `requirements.txt` keeps every line pinned with `==`, uses at least `flask==3.1.3`, `streamlit==1.54.0`, `pypdf==6.21.4`, `werkzeug==3.1.9` and `requests==2.33.0` (with `streamlit-chat` and `pyarrow` changed only as the design allows), stays installable with the approved Python 3.11 command, preserves its order, UTF-8 BOM and CRLF endings, and the ordered `EXPECTED` list in `tests/test_requirements.py` matches the file.
- The Streamlit menu shows the same visible paths, titles and icons as the existing `show_pages` list with `download.py` and `refresh.py` omitted; if `st-pages` is removed, the same menu is built with `st.navigation` and `st.Page`, and all `hide_pages` calls and imports are gone.
- `.trivyignore` no longer contains the two Werkzeug IDs or their comment, and no other ignores are changed.
- Any additional code changes forced by the upgrades are limited to `flask_app.py` and `modules/history.py` and preserve the pages' titles, widgets and behaviour.
- `tests/test_pdf.py` loads each sample PDF in `playground/sample_documents/` with `PyPDFLoader` and asserts at least one page of non-empty text.
- The existing tests still pass.

## Not in scope
- Dependabot alerts or upgrades for packages this piece does not name, including torch, sentence-transformers, transformers, langchain and langchain-community.
- `playground/`, the notebooks, `Gallery/`, `.devcontainer/`, `.github/`, and the pipeline's install command.
- Adding CUDA packages or changing the CPU-only torch setup.
- Refactoring, new features, changing page titles/widgets/behaviour, deleting `download.py` or `refresh.py`, or removing `st-pages` when it remains compatible.
- Rewriting earlier tests beyond updating `EXPECTED`, or adding tests unrelated to PDF loading.
- Other `.trivyignore` entries, including the transformer IDs from piece 1.

## Open questions
- Exact final pins are only bounded by “or later”; assume use the lowest versions that satisfy each named floor, moving `pyarrow` to the newest compatible release and changing `streamlit-chat` only if the upgraded Streamlit requires it.
- Whether the pinned `st-pages` works with Streamlit 1.54.0 is unknown; assume it is checked first, and the native `st.navigation`/`st.Page` fallback is used only if it fails.
- The two Werkzeug IDs are not named in the idea; assume they are the existing `.trivyignore` entries whose comments say this piece removes them, leaving other ignores untouched.

## Design
Written from these approved sections, which the spec and plan stages read word for word:
- `docs/dependabot-remediation.md#rules-for-every-piece`
- `docs/dependabot-remediation.md#facts-the-plan-must-not-guess`
- `docs/dependabot-remediation.md#done`
- `docs/dependabot-remediation.md#piece-2`

