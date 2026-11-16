<!-- sdlc stage=plan model=deepseek-v4.1-flash:cloud from=intent.md,spec.md,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#done,docs/dependabot-remediation.md#piece-3@89e279a -->
## Approach
Make the smallest forced migration: update the ordered pins while preserving BOM/CRLF, move every named live import and chatbot invocation to the approved LangChain 1.x paths, then add focused offline tests for source expectations, the chat chain, the evaluator page, and the explicit regression set.

## Coverage

| Done when (intent.md) | Spec behaviours | Phase |
| :-- | :-- | :-- |
| `requirements.txt` keeps its UTF-8 BOM and CRLF line endings, removes `openai==0.27.7`, changes the named pins in place, adds the new pins before `pandas`, and installs with the pipeline’s Python 3.11 command. | 1, 2, 3 | Phase 1 |
| Live imports and calls are updated as approved: `modules/chatbot.py` uses `langchain_openai`, `langchain_classic.chains`, `langchain_core.prompts`, `set_verbose(False)` and `invoke`; `modules/embedder.py`, `pages/3_Robby-Youtube.py`, `filename.py`, and `tests/test_embedder.py` use their approved LangChain 1.x import paths. | 4, 5, 6, 7, 8, 9, 10, 11 | Phase 1 |
| `tests/test_chatbot.py` runs offline with `OfflineFakeChat` and `FakeEmbeddings`, returns an answer starting with `hi`, records history as `[("q", "hi")]`, and does not download a tokenizer or use the network. | 12, 13 | Phase 2 |
| `tests/test_evaluator.py` runs `filename.py` through `AppTest` without exception; after entering `abc` and `abd` and clicking the button, a markdown element contains “Similarity score”. | 14, 15 | Phase 3 |
| `tests/test_requirements.py` `EXPECTED` matches the new ordered pins, and every earlier test not explicitly changed by this piece still passes. | 1, 2, 16 | Phase 1, Phase 3 |
| The existing tests still pass. | 4, 11, 16 | Phase 3 |

## Phase 1: Pins and LangChain 1.x import/call migration
<!-- phase: 1 -->
<!-- targets: requirements.txt, modules/chatbot.py, modules/embedder.py, pages/3_Robby-Youtube.py, filename.py, tests/test_requirements.py, tests/test_embedder.py, tests/test_langchain_migration.py -->
<!-- frozen: tests/conftest.py, tests/test_conftest.py, tests/test_flask.py, tests/test_imports.py, tests/test_navigation.py, tests/test_pages.py, tests/test_pdf.py, tests/test_similarity.py, tests/test_trivyignore.py, modules/similarity.py, modules/utils.py, streamlit_app.py, flask_app.py -->

**Goal:** After this phase, the approved LangChain 1.x pins and all named live import/call changes are present, and the pin/source/import tests pass offline.

**Changes:**
- `requirements.txt`: preserve the leading UTF-8 BOM and CRLF line breaks. Keep the existing comment line `# pywin32==308`. Remove `openai==0.27.7`. Change `langchain==0.2.11` to `langchain==1.5.0`, `langchain-community==0.2.10` to `langchain-community==0.4.2`, and `tiktoken==0.4.0` to `tiktoken==0.14.0`. Insert before `pandas==2.3.3`, in this exact order: `langchain-openai==1.8.0`, `langchain-text-splitters==1.1.3`, `langchain-classic==1.0.8`, `rapidfuzz==3.14.6`. The final non-comment package lines must equal:
```text
langchain==1.5.0
langchain-community==0.4.2
pdfplumber==0.11.4
pypdf==6.21.4
streamlit==1.54.0
streamlit-chat==0.0.2.2
tiktoken==0.14.0
youtube-transcript-api==0.6.0
faiss-cpu==1.9.0
requests==2.33.0
bs4==0.0.2
flask==3.1.3
sentence-transformers==2.2.2
torch==2.1.0
pyarrow==25.0.0
transformers==4.46.3
huggingface-hub==0.25.2
werkzeug==3.1.9
langchain-openai==1.8.0
langchain-text-splitters==1.1.3
langchain-classic==1.0.8
rapidfuzz==3.14.6
pandas==2.3.3
python-dotenv==1.2.4
```
  Write bytes as `b"\xef\xbb\xbf" + "\r\n".join(updated_lines).encode("utf-8")` so BOM and CRLF remain.
- `modules/chatbot.py`: keep all existing class/function signatures: `class Chatbot`, `def __init__(self, model_name, temperature, vectors)`, `def conversational_chat(self, query)`, `def count_tokens_chain(chain, query)`. Replace live imports with:
```python
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from langchain_core.globals import set_verbose
```
  Remove `import langchain` and `langchain.verbose = False`; call `set_verbose(False)` at module import exactly once. In `conversational_chat`, change `result = chain(chain_input)` to `result = chain.invoke(chain_input)`. In `count_tokens_chain`, change `result = chain.run(query)` to `result = chain.invoke(query)`. Leave the commented-out async block untouched.
- `modules/embedder.py`: keep all `Embedder` method names and parameters unchanged. Replace `from langchain.embeddings.openai import OpenAIEmbeddings` with `from langchain_openai import OpenAIEmbeddings`; replace `from langchain.text_splitter import RecursiveCharacterTextSplitter` with `from langchain_text_splitters import RecursiveCharacterTextSplitter`. Leave commented-out lines untouched.
- `pages/3_Robby-Youtube.py`: keep `def get_youtube_id(url)` and all widgets/behaviour unchanged. Replace `from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate` with `from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate`; replace `from langchain_community.chat_models import ChatOpenAI` with `from langchain_openai import ChatOpenAI`. Do not change the existing `llm(...)` call in this phase.
- `filename.py`: keep all widgets/behaviour unchanged. Replace `from langchain.evaluation import load_evaluator` with `from langchain_classic.evaluation import load_evaluator`.
- `tests/test_requirements.py`: keep `EXPECTED` as the module-level constant name and replace its value with:
```python
EXPECTED = [
    "langchain==1.5.0",
    "langchain-community==0.4.2",
    "pdfplumber==0.11.4",
    "pypdf==6.21.4",
    "streamlit==1.54.0",
    "streamlit-chat==0.0.2.2",
    "tiktoken==0.14.0",
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
    "langchain-openai==1.8.0",
    "langchain-text-splitters==1.1.3",
    "langchain-classic==1.0.8",
    "rapidfuzz==3.14.6",
    "pandas==2.3.3",
    "python-dotenv==1.2.4",
]
```
- `tests/test_embedder.py`: keep `def test_wales_pdf_returns_three_similarity_documents() -> None` unchanged. Replace `from langchain.text_splitter import RecursiveCharacterTextSplitter` with `from langchain_text_splitters import RecursiveCharacterTextSplitter`.
- `tests/test_langchain_migration.py`: new file. Add helper:
```python
from pathlib import Path


def _active_source(path: str) -> str:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return "\n".join(line for line in lines if not line.lstrip().startswith("#"))
```
  Add tests using exact string assertions:
  - `test_chatbot_uses_langchain_1x_imports_and_invoke`: read `modules/chatbot.py`; assert the three new `langchain_openai` / `langchain_classic.chains` / `langchain_core.prompts` imports and `from langchain_core.globals import set_verbose` are present; assert `set_verbose(False)` is present; assert `"import langchain"` and `"langchain.verbose"` are absent from the full source; use `_active_source("modules/chatbot.py")` and assert `"chain.invoke(chain_input)"` and `"chain.invoke(query)"` are present, while `"chain(chain_input)"` and `"chain.run(query)"` are absent.
  - `test_embedder_uses_langchain_1x_imports`: assert `from langchain_openai import OpenAIEmbeddings` and `from langchain_text_splitters import RecursiveCharacterTextSplitter` are in `modules/embedder.py`; assert `"langchain.embeddings.openai"` and `"langchain.text_splitter"` are absent from `_active_source("modules/embedder.py")`.
  - `test_youtube_page_uses_langchain_1x_imports`: assert `from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate` and `from langchain_openai import ChatOpenAI` are in `pages/3_Robby-Youtube.py`; assert `"langchain.prompts"` and `"langchain_community.chat_models"` are absent from `_active_source("pages/3_Robby-Youtube.py")`.
  - `test_evaluator_uses_langchain_classic_import`: assert `from langchain_classic.evaluation import load_evaluator` is in `filename.py`; assert `"langchain.evaluation"` is absent from `_active_source("filename.py")`.
  - `test_test_embedder_uses_langchain_text_splitters`: assert `from langchain_text_splitters import RecursiveCharacterTextSplitter` is in `tests/test_embedder.py`; assert `"from langchain.text_splitter import"` is absent from `_active_source("tests/test_embedder.py")`.

**Definition of done:**
- [ ] `tests/test_requirements.py`, test `test_requirements_keeps_utf8_bom_and_crlf`: proves spec behaviour 1; reads `requirements.txt` bytes and asserts `raw.startswith(b"\xef\xbb\xbf")` and `raw.count(b"\n") == raw.count(b"\r\n")`. No teardown needed.
- [ ] `tests/test_requirements.py`, test `test_exact_order_and_pins`: proves spec behaviour 2; asserts `_package_lines() == EXPECTED`. No teardown needed.
- [ ] `tests/test_requirements.py`, test `test_no_cuda_packages`: proves spec behaviour 3; rejects package names containing `cuda`, `cudnn`, `cublas`, or `nccl`. No teardown needed.
- [ ] `tests/test_imports.py`, test `test_every_module_imports`: proves spec behaviour 4; parametrized import of every `modules/*.py` module. Relies on `tests/conftest.py` autouse fixture for repo root and API-key environment; no additional teardown.
- [ ] `tests/test_langchain_migration.py`, test `test_chatbot_uses_langchain_1x_imports_and_invoke`: proves spec behaviours 5 and 6; source-string assertions described above, with full-line comments ignored only for old-call absence checks. No teardown needed.
- [ ] `tests/test_langchain_migration.py`, test `test_embedder_uses_langchain_1x_imports`: proves spec behaviour 7; assertions described above. No teardown needed.
- [ ] `tests/test_langchain_migration.py`, test `test_youtube_page_uses_langchain_1x_imports`: proves spec behaviour 8; assertions described above. No teardown needed.
- [ ] `tests/test_langchain_migration.py`, test `test_evaluator_uses_langchain_classic_import`: proves spec behaviour 9; assertions described above. No teardown needed.
- [ ] `tests/test_langchain_migration.py`, test `test_test_embedder_uses_langchain_text_splitters`: proves spec behaviour 10; assertions described above. No teardown needed.
- [ ] `tests/test_embedder.py`, test `test_wales_pdf_returns_three_similarity_documents`: proves spec behaviour 11; keeps the existing PDF/FAISS/similarity-search body unchanged and returns three similarity documents. Relies on `tests/conftest.py` autouse cleanup for `embeddings/*.pkl`; no additional teardown.

**Verify:**
```bash
python -m pytest tests/test_requirements.py tests/test_imports.py tests/test_langchain_migration.py tests/test_embedder.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 2: Offline chatbot chain test
<!-- phase: 2 -->
<!-- targets: tests/test_chatbot.py -->
<!-- frozen: requirements.txt, modules/chatbot.py, modules/embedder.py, pages/3_Robby-Youtube.py, filename.py, tests/test_requirements.py, tests/test_embedder.py, tests/test_langchain_migration.py, tests/conftest.py, tests/test_conftest.py, tests/test_flask.py, tests/test_imports.py, tests/test_navigation.py, tests/test_pages.py, tests/test_pdf.py, tests/test_similarity.py, tests/test_trivyignore.py -->

**Goal:** Prove the migrated chat chain works offline with fake chat/embeddings, returns an answer starting with `hi`, and records `[("q", "hi")]` without tokenizer or network access.

**Changes:**
- `tests/test_chatbot.py`: new test file. Use these exact imports and helper class:
```python
import streamlit as st
from langchain_community.embeddings.fake import FakeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from modules.chatbot import Chatbot


class OfflineFakeChat(FakeListChatModel):
    def get_num_tokens(self, text: str) -> int:
        return len(text.split())


def _build_vectors() -> FAISS:
    return FAISS.from_texts(
        ["alpha document", "beta document", "gamma document"],
        FakeEmbeddings(size=8),
    )
```
  Add `test_offline_fake_chat_counts_words`: instantiate `OfflineFakeChat(responses=["hi"])`; assert `get_num_tokens("") == 0` and `get_num_tokens("one two three") == 3`.
  Add `test_conversational_chat_returns_hi_and_records_history(monkeypatch)`: patch `"modules.chatbot.ChatOpenAI"` to `lambda **kwargs: OfflineFakeChat(responses=["hi"])`; set `st.session_state["history"] = []`; call `Chatbot(model_name="test-model", temperature=0.0, vectors=_build_vectors()).conversational_chat("q")`; assert the returned string starts with `"hi"` and `st.session_state["history"] == [("q", "hi")]`. Put the assertion body in `try/finally` and reset `st.session_state["history"] = []` in `finally`.

**Definition of done:**
- [ ] `tests/test_chatbot.py`, test `test_offline_fake_chat_counts_words`: proves spec behaviour 12; `OfflineFakeChat.get_num_tokens("")` returns `0` and word text returns `len(text.split())`. No teardown needed.
- [ ] `tests/test_chatbot.py`, test `test_conversational_chat_returns_hi_and_records_history`: proves spec behaviour 13; uses `FAISS.from_texts([...], FakeEmbeddings(size=8))`, monkeypatches `modules.chatbot.ChatOpenAI` to the fake, sets `st.session_state["history"] = []`, asserts `answer.startswith("hi")` and history equals `[("q", "hi")]`. Teardown resets `st.session_state["history"] = []` in `finally`.
- [ ] The test avoids tokenizer download because `OfflineFakeChat.get_num_tokens` overrides token counting; no real OpenAI key, network, or GPU is used.

**Verify:**
```bash
python -m pytest tests/test_chatbot.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 3: Evaluator AppTest and explicit regression
<!-- phase: 3 -->
<!-- targets: tests/test_evaluator.py -->
<!-- frozen: requirements.txt, modules/chatbot.py, modules/embedder.py, pages/3_Robby-Youtube.py, filename.py, tests/test_requirements.py, tests/test_embedder.py, tests/test_langchain_migration.py, tests/test_chatbot.py, tests/conftest.py, tests/test_conftest.py, tests/test_flask.py, tests/test_imports.py, tests/test_navigation.py, tests/test_pages.py, tests/test_pdf.py, tests/test_similarity.py, tests/test_trivyignore.py -->

**Goal:** Prove `filename.py` loads and renders a similarity score through `AppTest`, and prove the explicit regression set still passes.

**Changes:**
- `tests/test_evaluator.py`: new test file with exact imports and tests:
```python
from streamlit.testing.v1 import AppTest


def test_evaluator_page_loads_without_exception() -> None:
    at = AppTest.from_file("filename.py", default_timeout=60).run()
    assert len(at.exception) == 0


def test_evaluator_click_renders_similarity_score() -> None:
    at = AppTest.from_file("filename.py", default_timeout=60).run()
    assert len(at.exception) == 0
    at.text_input[0].set_value("abc")
    at.text_input[1].set_value("abd")
    at.button[0].click()
    at.run()
    assert len(at.exception) == 0
    assert any("Similarity score" in markdown.value for markdown in at.markdown)
```
  No production code changes in this phase.

**Definition of done:**
- [ ] `tests/test_evaluator.py`, test `test_evaluator_page_loads_without_exception`: proves spec behaviour 14; `AppTest.from_file("filename.py", default_timeout=60).run()` has `len(at.exception) == 0`. No server or teardown needed.
- [ ] `tests/test_evaluator.py`, test `test_evaluator_click_renders_similarity_score`: proves spec behaviour 15; loads `filename.py`, sets `text_input[0]` to `"abc"`, `text_input[1]` to `"abd"`, clicks `button[0]`, reruns, asserts no exception, and asserts at least one `at.markdown` element value contains `"Similarity score"`. No server or teardown needed.
- [ ] The explicit regression command below also proves spec behaviour 16 and that every earlier test file, including unchanged existing tests, still passes.

**Verify:**
```bash
python -m pytest tests/test_evaluator.py tests/test_chatbot.py tests/test_requirements.py tests/test_imports.py tests/test_embedder.py tests/test_langchain_migration.py tests/test_conftest.py tests/test_flask.py tests/test_navigation.py tests/test_pages.py tests/test_pdf.py tests/test_similarity.py tests/test_trivyignore.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Risks
- Upgrading LangChain 1.x changes transitive NumPy to 2.x and may expose torch 2.1 compatibility issues; Phase 1’s `tests/test_embedder.py` and Phase 3’s explicit regression run catch this.
- `ConversationalRetrievalChain` can try to load a GPT-2 tokenizer for `max_tokens_limit`; Phase 2’s `OfflineFakeChat.get_num_tokens` override and test catch any accidental tokenizer/network access.
- The evaluator import could remain on the removed `langchain.evaluation` path; Phase 1’s source test catches the import, and Phase 3’s `AppTest` catches runtime failure.
- The page-3 import migration could leave `langchain_community.chat_models` or old prompt imports; Phase 1’s source test catches this before the regression run.
- The source-inspection checks must ignore full-line comments to preserve the approved “leave commented-out code alone” rule; Phase 1’s helper and tests make that explicit, and Phase 3 re-runs the same checks.

## Open questions
- Commented-out code conflict: the approved design says leave commented-out lines alone, while spec behaviours 6–9 say the inspected source does not contain old imports/calls. Assumption: source-inspection tests strip full-line comments and assert old strings are absent only from active code.
- Issue #4 lists lower minimum versions than the approved piece pins for `langchain` and `langchain-community`. Assumption: the approved higher pins satisfy the “at least” rule.

## Hand back
When every phase is built and its Verify block passes:
1. Create `sdlc/features/003-dependabot-remediation-piece-3-langchain/build-log.md` with one section per phase, in order. Head each
   one `## Phase <n>: <title>`, then list the files changed, the Verify command
   you ran and its result, and any deviation from this plan (or "none").
2. Commit it and push it to `feature/003-dependabot-remediation-piece-3-langchain`.

Commit only this plan's targets and `build-log.md`. Leave every other file alone,
including other features' documents under `sdlc/features/`, even for formatting;
verification fails on any file outside the targets.

The pipeline waits for this file. Once it has a section for every phase, it
verifies the whole branch and opens the pull request.

