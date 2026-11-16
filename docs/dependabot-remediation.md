# Dependabot remediation

Clear the Dependabot alerts on `ly2xxx/rag_chat_poc` (`requirements.txt`) without
breaking the Streamlit app. It is built in 4 pieces, one SDLC feature each, in order.
Each piece builds on the code the earlier ones merged: extend those files and tests,
never redesign them.

## Rules for every piece

- **Alerts**: the source of truth is the open tracking issue labelled `dependabot`,
  kept up to date by the Dependabot monitor workflow. A piece fixes only the packages
  it names. Upgrade each to at least the **highest** `fixed` version the issue lists
  for that package, never the lowest.
- **Pins**: every line in `requirements.txt` is pinned with `==`. Keep the file's
  order; add new lines at the end with a comment saying which piece added them.
- **Code changes**: only what an upgrade forces (renamed imports, removed APIs). No
  refactoring, no new features, no UI changes. Keep each page's behaviour.
- **Tests**: pytest, in `tests/`, named `test_<area>.py`. Pages are tested with
  `streamlit.testing.v1.AppTest`. Tests never use the network, an OpenAI key or a
  GPU: use `langchain_community` fake models and embeddings, and the local model in
  `all-MiniLM-L6-v2/`. `tests/conftest.py` puts the repository root on `sys.path`.
- **Install**: the pipeline installs with
  `pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt`
  (CPU-only torch). Don't add CUDA packages.
- **Never in scope**: `playground/`, the notebooks, `Gallery/`, the devcontainer,
  the README text (except removing a dependency's mention), and alerts in packages a
  piece doesn't name.

## Facts the plan must not guess

Read from the code on 2026-11-16. Use these exactly.

- Alerts in the 2026-11-03 digest (refresh from the tracking issue before planning):
  flask 2.0.2 (fixed 2.2.5; CVE-2023-30861, CVE-2026-27205); pandasai 0.2.15 (no fix;
  CVE-2023-39660); pypdf 3.9.0 (3.17.0 and 55 more); torch 2.1.0 (2.2.0 and 3 more,
  incl. critical CVE-2025-32434); streamlit 1.31.1 (1.37.0, 1.54.0); langchain-community
  0.2.10 (0.2.19); langchain 0.2.11 (0.3.30); sentence-transformers 2.2.2 (5.6.0, critical).
- `pandasai` is not imported anywhere; `streamlit_app.py` line 236 mentions it in a
  comment. `modules/utils.py` imports `pandas` and `dotenv`, which are not in
  `requirements.txt` (they arrive with pandasai today).
- `playwright` and `pytube` are in `requirements.txt` but imported nowhere.
- `streamlit_app.py` imports `hide_pages, show_pages_from_config, add_page_title,
  show_pages, Page, Section` from `st_pages` (unpinned, `>=0.4.3`); pages 0, 2 and 4
  call `hide_pages(["down", "ref"])`. `.streamlit/pages.toml` lists the pages.
- `modules/similarity.py`: `SimilarityScorer().score(a, b)` loads
  `SentenceTransformer('./all-MiniLM-L6-v2')` (a `pytorch_model.bin`) and returns
  `util.pytorch_cos_sim(...)[0][0].item()`, a float. `app/__main__.py` does the same
  from two command-line arguments.
- `modules/chatbot.py`: `Chatbot(model_name, temperature, vectors)`;
  `conversational_chat(query)` builds `ChatOpenAI` (from `langchain_community.chat_models`)
  and `ConversationalRetrievalChain.from_llm(...)`, calls `chain(chain_input)` with
  `{"question", "chat_history": st.session_state["history"]}`, appends
  `(query, answer)` to the history and returns the answer plus a query-time line.
  It sets `langchain.verbose = False` at import.
- `modules/embedder.py` imports `OpenAIEmbeddings` from `langchain.embeddings.openai`,
  `RecursiveCharacterTextSplitter` from `langchain.text_splitter`, and `CSVLoader`,
  `PyPDFLoader`, `TextLoader`, `FAISS` from `langchain_community`.
- `pages/3_Robby-Youtube.py` imports `ChatOpenAI` from `langchain_community.chat_models`
  and prompt classes from `langchain.prompts`. `filename.py` calls
  `load_evaluator("string_distance")`. `requirements.txt` pins `openai==0.27.7`.
- `flask_app.py`: `GET /` renders `templates/flask_index.html`.
- PDFs for tests: `playground/sample_documents/*.pdf`.

## Done

Nothing yet.

## Piece 1: Test baseline and pandasai removal

The app has a smoke-test suite, and the pandasai alert is gone.

- Remove `pandasai` from `requirements.txt` and its mention in `streamlit_app.py`.
  Add `pandas` and `python-dotenv`, pinned to the versions installed today.
- Pin `st-pages` to the newest release that still exports every name in the Facts;
  the page tests prove it.
- `tests/conftest.py`: repository root on `sys.path`; an autouse fixture sets a dummy
  `OPENAI_API_KEY` and runs each test in a temporary working directory that has
  `all-MiniLM-L6-v2` linked in (the embedder creates `embeddings/`).
- `tests/test_imports.py`: every module in `modules/` imports.
- `tests/test_pages.py`: `AppTest.from_file(path).run()` raises no exception for
  `streamlit_app.py` and each file in `pages/`, without user input.
- `tests/test_similarity.py`: identical sentences score above 0.99; two unrelated
  sentences score lower than two paraphrases.
- `tests/test_flask.py`: `GET /` returns 200.
- `tests/test_embedder.py`: splitting a sample PDF and building FAISS with
  `FakeEmbeddings(size=8)` gives a store that returns 3 documents for `k=3`.

## Piece 2: Web and PDF packages

Flask, Streamlit and pypdf are on fixed versions.

- Upgrade `flask`, `streamlit` (and `streamlit-chat` if the new Streamlit needs it)
  and `pypdf` to the highest fixed versions in the tracking issue.
- Fix only what the upgrade breaks: `@st.cache_data`, `st.set_page_config`, and
  `streamlit_chat.message` in `modules/history.py`; Flask's app factory in `flask_app.py`.
- Remove the unused `playwright` and `pytube` lines.
- Piece 1's tests pass unchanged. Add `tests/test_pdf.py`: `PyPDFLoader` loads both
  sample PDFs with at least one non-empty page each.

## Piece 3: LangChain 0.3

LangChain packages are on fixed versions and the old `openai==0.27.7` client is gone.

- Upgrade `langchain` and `langchain-community` to the highest fixed versions; add
  `langchain-openai` and `langchain-text-splitters` at matching versions; remove the
  `openai` pin (langchain-openai brings a current one).
- `ChatOpenAI` and `OpenAIEmbeddings` come from `langchain_openai` in
  `modules/chatbot.py`, `modules/embedder.py` and `pages/3_Robby-Youtube.py`;
  `RecursiveCharacterTextSplitter` from `langchain_text_splitters`; prompts from
  `langchain_core.prompts`. Replace `langchain.verbose = False` with
  `langchain.globals.set_verbose(False)` and `chain(chain_input)` with
  `chain.invoke(chain_input)`. Keep `ConversationalRetrievalChain` and its arguments.
- If `load_evaluator("string_distance")` needs `rapidfuzz`, pin it.
- `tests/test_chatbot.py`: with `ChatOpenAI` patched to `FakeListChatModel(responses=["hi"])`
  and a FAISS store from `FakeEmbeddings`, `conversational_chat("q")` returns text
  starting with `hi` and appends `("q", "hi")` to `st.session_state["history"]`.

## Piece 4: Torch and sentence-transformers

Similarity scoring runs on fixed versions of torch and sentence-transformers.

- Upgrade `torch` and `sentence-transformers` to the highest fixed versions (torch
  from the CPU index), and `transformers` if they need it.
- If the new versions refuse `all-MiniLM-L6-v2/pytorch_model.bin`, add a
  `model.safetensors` converted from it and delete the `.bin`; record it in the
  build log. Don't download a model at run time.
- Piece 1's similarity tests pass unchanged. Add `tests/test_cli.py`: running
  `python app/__main__.py "a cat" "a cat"` prints a `Sentence Transformers:` line
  with a value above 0.99, and with one argument exits 1.
