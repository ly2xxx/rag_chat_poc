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

- Open alerts after piece 2, 35 in 5 packages (current → upgrade to): torch 2.1.0 →
  2.13.0 (12, critical); sentence-transformers 2.2.2 → 5.6.0 (1, critical); transformers
  4.46.3 → 5.10.0 (18, high); langchain 0.2.11 → 1.3.9 (2, high); langchain-community
  0.2.10 → 0.3.27 (2, high).
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

## Piece 1: Test baseline and unused packages

Built; see Done.

## Piece 2: Flask, Streamlit and pypdf

Built; see Done.

## Piece 3: LangChain 1.x

LangChain is on fixed versions and the `openai==0.27.7` client is gone.

- Pins, changed in place: `langchain==1.5.0`, `langchain-community==0.4.2`,
  `tiktoken==0.14.0` (`langchain-openai` needs >= 0.7); delete the `openai==0.27.7` line;
  add before `pandas`: `langchain-openai==1.8.0`, `langchain-text-splitters==1.1.3`,
  `langchain-classic==1.0.8`, `rapidfuzz==3.14.6`. They install together with every
  other pin (checked); NumPy becomes 2.x and the suite still passes on torch 2.1.
- Imports (live code only; leave commented-out lines alone):
  `modules/chatbot.py`: `ChatOpenAI` from `langchain_openai`,
  `ConversationalRetrievalChain` from `langchain_classic.chains`, `PromptTemplate` from
  `langchain_core.prompts`; replace `import langchain` / `langchain.verbose = False`
  with `from langchain_core.globals import set_verbose` / `set_verbose(False)`; the
  first `chain(chain_input)` becomes `chain.invoke(chain_input)` and `chain.run(query)`
  becomes `chain.invoke(query)`. `modules/embedder.py`: `OpenAIEmbeddings` from
  `langchain_openai`, `RecursiveCharacterTextSplitter` from `langchain_text_splitters`.
  `pages/3_Robby-Youtube.py`: prompts from `langchain_core.prompts`, `ChatOpenAI` from
  `langchain_openai`. `filename.py`: `load_evaluator` from
  `langchain_classic.evaluation`. `tests/test_embedder.py`: the splitter import from
  `langchain_text_splitters`. `ChatOpenAI(model_name=..., temperature=...)` still works.
- `tests/test_chatbot.py`: `class OfflineFakeChat(FakeListChatModel)` (from
  `langchain_core.language_models.fake_chat_models`) with `get_num_tokens(self, text)`
  returning `len(text.split())` (the chain's `max_tokens_limit` would otherwise download
  a GPT-2 tokenizer); patch `modules.chatbot.ChatOpenAI` to
  `lambda **kwargs: OfflineFakeChat(responses=["hi"])`; build FAISS with
  `FAISS.from_texts([three short texts], FakeEmbeddings(size=8))`; set
  `st.session_state["history"] = []`; `conversational_chat("q")` starts with `hi` and
  the history is `[("q", "hi")]`. `tests/test_evaluator.py`: `AppTest.from_file("filename.py")` runs with no exception;
  after `text_input[0]` "abc", `text_input[1]` "abd" and clicking `button[0]`, a markdown
  element contains "Similarity score".

## Piece 4: Torch and sentence-transformers

Similarity scoring runs on fixed versions of torch and sentence-transformers.

- `torch==2.13.0` or later (from the CPU index), `sentence-transformers==5.6.0` or
  later; `transformers==5.10.0` or later and `huggingface-hub` at a version they accept. Delete the six transformers IDs and their comment from `.trivyignore`.
- Loading must stay local: `SentenceTransformer('./all-MiniLM-L6-v2')`, no download.
  If the new versions refuse `pytorch_model.bin`, add a `model.safetensors` converted
  from it, delete the `.bin`, and say so in the build log.
- `tests/test_cli.py`: `python app/__main__.py "a cat" "a cat"` prints a
  `Sentence Transformers:` line with a value above 0.99; with one argument it exits 1.
