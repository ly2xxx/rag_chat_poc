# Dependabot remediation

Clear the Dependabot alerts on `ly2xxx/rag_chat_poc` (`requirements.txt`) without
breaking the Streamlit app. It is built in 4 pieces, one SDLC feature each, in order.
Each piece builds on the code the earlier ones merged: extend those files and tests,
never redesign them.

## Rules for every piece

- **Alerts**: the source of truth is the open issue labelled `dependabot` (#4), kept
  up to date by `.github/workflows/dependabot-monitor.yml`. A piece fixes only the
  packages it names, and upgrades each to at least the package's **Upgrade to**
  version there, never a lower one.
- **Pins**: every line in `requirements.txt` is pinned with `==`. Keep the file's
  order; add new lines at the end. Every pin must install on Python 3.11 with the
  pipeline's install command.
- **Install**: the pipeline runs Python 3.11 and installs with
  `uv pip install --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt`
  (CPU-only torch). Don't add CUDA packages.
- **Code changes**: only what an upgrade forces (moved imports, removed APIs). No
  refactoring, no new features. Keep each page's title, widgets and behaviour.
- **Tests**: pytest, in `tests/`, named `test_<area>.py`, run from the repository
  root. Pages are tested with `streamlit.testing.v1.AppTest`. Tests never use the
  network, a real OpenAI key or a GPU: use fake models and embeddings, and the local
  model in `all-MiniLM-L6-v2/`. Earlier pieces' tests pass unchanged, except
  `EXPECTED` in `tests/test_requirements.py`, which every piece updates to its pins, and
  tests a piece section says to change or delete.
- **Never in scope**: `playground/`, the notebooks, `Gallery/`, `.devcontainer/`,
  `.github/`, and alerts in packages a piece doesn't name.

## Facts the plan must not guess

Read from the code and issue #4 on 2026-11-16. Use these exactly.

- Open alerts after piece 4: none.
- `pandasai`, `playwright` and `pytube` are imported nowhere; `streamlit_app.py` line
  236 mentions PandasAI in a comment. `modules/utils.py` imports `pandas` and `dotenv`,
  which aren't in `requirements.txt`: with the current pins they resolve to
  `pandas==2.3.3` and `python-dotenv==1.2.4`.
- `streamlit_app.py` imports `hide_pages, show_pages_from_config, add_page_title,
  show_pages, Page, Section` from `st_pages` (unpinned, `>=0.4.3`). It calls
  `add_page_title()`, `show_pages_from_config()`, then `show_pages([...])` with eight
  `Page(path, name, icon)` entries (this list is what the menu shows), then
  `hide_pages(["down", "ref"])`. Pages 0, 2 and 4 also call `hide_pages(["down", "ref"])`.
- `modules/utils.py`: `Utilities.load_api_key()` returns `OPENAI_API_KEY` when `.env`
  exists and the variable is set, else a sidebar text input's value.
- `modules/similarity.py`: `SimilarityScorer().score(a, b)` loads
  `SentenceTransformer('./all-MiniLM-L6-v2')` (a `pytorch_model.bin`) and returns
  `util.pytorch_cos_sim(...)[0][0].item()`. `app/__main__.py` prints
  `Sentence Transformers: <float>` for two arguments, else exits 1.
- `modules/chatbot.py`: `Chatbot(model_name, temperature, vectors).conversational_chat(query)`
  builds `ChatOpenAI` (`langchain_community.chat_models`) and
  `ConversationalRetrievalChain.from_llm(...)`, calls `chain(chain_input)` with
  `{"question", "chat_history": st.session_state["history"]}`, appends `(query, answer)`
  to that history and returns the answer plus a query-time line. It sets
  `langchain.verbose = False` at import.
- `modules/embedder.py`: imports `OpenAIEmbeddings` from `langchain.embeddings.openai`,
  `RecursiveCharacterTextSplitter` from `langchain.text_splitter`, and `CSVLoader`,
  `PyPDFLoader`, `TextLoader`, `FAISS` from `langchain_community`. `Embedder()` creates
  `embeddings/` in the working directory and caches `<name>.pkl` files there.
- `pages/3_Robby-Youtube.py`: `ChatOpenAI` from `langchain_community.chat_models`,
  prompts from `langchain.prompts`. `filename.py`: `load_evaluator("string_distance")`.
- `requirements.txt` pins `openai==0.27.7`, starts with a UTF-8 byte-order mark and
  uses CRLF line endings; keep both.
- `.trivyignore` accepts 8 CVEs in piece 1's `transformers==4.46.3` and
  `werkzeug==2.0.3` pins, each commented with the piece that removes it.
- `flask_app.py`: `GET /` renders `templates/flask_index.html`.
- Sample PDFs: `playground/sample_documents/*.pdf` (read-only fixtures).

## Done

- **Piece 1** (#13): `tests/` holds the smoke suite, 32 tests: `conftest.py` (repo root on
  `sys.path`, `OPENAI_API_KEY=sk-test`, removes `embeddings/*.pkl` a test created),
  `test_requirements.py` (exact ordered pin list in `EXPECTED`: update it with every pin
  change), `test_conftest.py`, `test_imports.py`, `test_pages.py` (`AppTest`, every page),
  `test_similarity.py`, `test_flask.py`, `test_embedder.py`. pandasai, playwright and pytube
  are gone; every line is pinned with `==`. Interim pins a fresh install needs:
  `pyarrow==25.0.0` (NumPy < 2), `transformers==4.46.3` and `huggingface-hub==0.25.2`
  (sentence-transformers 2.2.2, torch 2.1), `werkzeug==2.0.3` (Flask 2.0.2).
- **Piece 2** (#22): `flask==3.1.3`, `werkzeug==3.1.9`, `requests==2.33.0`,
  `pypdf==6.21.4`, `streamlit==1.54.0`; `st-pages` is gone. `streamlit_app.py` defines
  `generate_thumbnail()` and `home()` (all home content, starting with `st.title("🏠 Home")`),
  then `MENU` and `HIDDEN` (`st.Page` lists), `page = st.navigation(MENU + HIDDEN,
  position="hidden")`, sidebar `st.page_link` per `MENU` item, `page.run()`. Tests added:
  `test_navigation.py` (sidebar links via `at.sidebar.get("page_link")`), `test_pdf.py`,
  `test_trivyignore.py` (expects 6 IDs: update it when piece 4 empties `.trivyignore`),
  and `test_requirements_keeps_utf8_bom_and_crlf`. `.trivyignore` keeps only the six
  transformers IDs.
- **Piece 3** (#28): `langchain==1.5.0`, `langchain-community==0.4.2`, `langchain-classic==1.0.8`,
  `langchain-openai==1.8.0`, `langchain-text-splitters==1.1.3`, `tiktoken==0.14.0`,
  `rapidfuzz==3.14.6`; no `openai` pin (NumPy is now 2.x). Imports as listed in the old
  piece 3 section; `chain.invoke(...)` everywhere; page 3 calls `llm.invoke(...)` (1.x chat
  models aren't callable). Tests added: `test_langchain_migration.py` (source checks),
  `test_chatbot.py` (`OfflineFakeChat`), `test_evaluator.py` (`filename.py` under `AppTest`).
- **Piece 4** (#34): `torch==2.13.0`, `sentence-transformers==5.6.0`, `transformers==5.23.0`,
  `huggingface-hub==2.4.0`; no code change. `.trivyignore` and `tests/test_trivyignore.py` are
  gone (`test_trivyignore_absent` guards it). Tests added: `test_cli.py`,
  `test_similarity_scores.py` (exact scores 1.0, 0.984, 0.079).
- **Result:** no open Dependabot alerts (issue #4 closed by the monitor, 2026-11-16 23:15 UTC);
  whole suite 51 passed on `main`.

## Piece 1: Test baseline and unused packages

Built; see Done.

## Piece 2: Flask, Streamlit and pypdf

Built; see Done.

## Piece 3: LangChain 1.x

Built; see Done.

## Piece 4: Torch and sentence-transformers

Built; see Done.
