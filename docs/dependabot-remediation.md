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
  `EXPECTED` in `tests/test_requirements.py`, which every piece updates to its pins.
- **Never in scope**: `playground/`, the notebooks, `Gallery/`, `.devcontainer/`,
  `.github/`, and alerts in packages a piece doesn't name.

## Facts the plan must not guess

Read from the code and issue #4 on 2026-11-16. Use these exactly.

- Open alerts after piece 1, 120 in 10 packages (current → upgrade to): torch 2.1.0 →
  2.13.0 (12, critical); sentence-transformers 2.2.2 → 5.6.0 (1, critical); pypdf 3.9.0
  → 6.21.4 (68, high); transformers 4.46.3 → 5.10.0 (18, high); werkzeug 2.0.3 → 3.1.9
  (10, high); flask 2.0.2 → 3.1.3 (2, high); langchain 0.2.11 → 1.3.9 (2, high);
  langchain-community 0.2.10 → 0.3.27 (2, high); streamlit 1.31.1 → 1.54.0 (3, medium);
  requests 2.32.3 → 2.33.0 (2, medium).
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

## Piece 1: Test baseline and unused packages

The app has a smoke-test suite, and the packages it never imports are gone.

- Remove `pandasai`, `playwright` and `pytube` from `requirements.txt`, and the
  PandasAI mention from `streamlit_app.py`. Add `pandas==2.3.3` and `python-dotenv==1.2.4`.
- Pin `st-pages` to the newest release that still exports every name in the Facts.
- Add `embeddings/` to `.gitignore`.
- `tests/conftest.py`: repository root on `sys.path`; an autouse fixture sets
  `OPENAI_API_KEY=sk-test` and removes `embeddings/*.pkl` files a test created.
- `tests/test_imports.py`: every module in `modules/` imports.
- `tests/test_pages.py`: `AppTest.from_file(path, default_timeout=60).run()` has no
  exception for `streamlit_app.py` and each `pages/*.py`, without user input.
- `tests/test_similarity.py`: identical sentences score above 0.99; "a cat sits on
  the mat" scores higher against "a cat is sitting on a mat" than against "stock
  prices fell today".
- `tests/test_flask.py`: `GET /` returns 200.
- `tests/test_embedder.py`: `playground/sample_documents/wales-in-world.pdf` loaded with `PyPDFLoader`, split with
  `RecursiveCharacterTextSplitter(chunk_size=1000)`, and stored with
  `FAISS.from_documents(docs, FakeEmbeddings(size=8))` answers
  `similarity_search("Wales", k=3)` with 3 documents.

## Piece 2: Flask, Streamlit and pypdf

Flask, Streamlit and pypdf are on fixed versions.

- `flask==3.1.3` or later, `streamlit==1.54.0` or later, `pypdf==6.21.4` or later,
  `werkzeug==3.1.9` or later, `requests==2.33.0` or later; `streamlit-chat` too if the
  new Streamlit needs it. `pyarrow` may then move to the newest release.
- If the pinned `st-pages` doesn't work with the new Streamlit, remove it: in
  `streamlit_app.py` build the menu with `st.navigation` from `st.Page` entries with
  the same paths, titles and icons as the `show_pages` list, `download.py` and
  `refresh.py` left out of the menu; delete every `hide_pages` call and import.
- Delete the two Werkzeug IDs and their comment from `.trivyignore`.
- Fix only what else the upgrades break (`flask_app.py`, `modules/history.py`).
- `tests/test_pdf.py`: `PyPDFLoader` loads each sample PDF with at least one page
  of non-empty text.

## Piece 3: LangChain 1.x

LangChain is on fixed versions and the `openai==0.27.7` client is gone.

- `langchain==1.3.9` or later; `langchain-community` at the newest release
  compatible with it (0.3.27 or later); add `langchain-openai`,
  `langchain-text-splitters` and `langchain-classic` at compatible versions; remove
  the `openai` pin (`langchain-openai` brings a current one); add `rapidfuzz` if
  `load_evaluator("string_distance")` needs it.
- In LangChain 1.x the legacy chains and evaluators live in `langchain_classic`:
  `ConversationalRetrievalChain` from `langchain_classic.chains`, `load_evaluator`
  from `langchain_classic.evaluation`. `ChatOpenAI` and `OpenAIEmbeddings` come from
  `langchain_openai`; `RecursiveCharacterTextSplitter` from `langchain_text_splitters`;
  prompts from `langchain_core.prompts`. Replace `langchain.verbose = False` with
  `set_verbose(False)` from `langchain_core.globals`, and `chain(chain_input)` with
  `chain.invoke(chain_input)`. Keep the chain's arguments.
- `tests/test_chatbot.py`: with `modules.chatbot.ChatOpenAI` patched to return
  `FakeListChatModel(responses=["hi"])` and a FAISS store built with `FakeEmbeddings`,
  `conversational_chat("q")` returns text starting with `hi` and appends `("q", "hi")`
  to `st.session_state["history"]`.

## Piece 4: Torch and sentence-transformers

Similarity scoring runs on fixed versions of torch and sentence-transformers.

- `torch==2.13.0` or later (from the CPU index), `sentence-transformers==5.6.0` or
  later; `transformers==5.10.0` or later and `huggingface-hub` at a version they accept. Delete the six transformers IDs and their comment from `.trivyignore`.
- Loading must stay local: `SentenceTransformer('./all-MiniLM-L6-v2')`, no download.
  If the new versions refuse `pytorch_model.bin`, add a `model.safetensors` converted
  from it, delete the `.bin`, and say so in the build log.
- `tests/test_cli.py`: `python app/__main__.py "a cat" "a cat"` prints a
  `Sentence Transformers:` line with a value above 0.99; with one argument it exits 1.
