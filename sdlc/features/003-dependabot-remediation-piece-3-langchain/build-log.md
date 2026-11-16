# Build log: 003-dependabot-remediation-piece-3-langchain

## Phase 1: Pins and LangChain 1.x import/call migration

**Status:** passed

**Files changed:** `requirements.txt`, `modules/chatbot.py`, `modules/embedder.py`,
`pages/3_Robby-Youtube.py`, `filename.py`, `tests/test_requirements.py`,
`tests/test_embedder.py`, `tests/test_langchain_migration.py`

The plan's pins (LangChain 1.5.0, community 0.4.2, classic 1.0.8, openai 1.8.0 bindings,
text-splitters 1.1.3, tiktoken 0.14.0, rapidfuzz 3.14.6; `openai==0.27.7` removed) and the
plan's import and call changes, live code only.

**Commands:**
- `uv pip install -r requirements.txt` (Python 3.11): exit 0.
- `sdlc_stage.py verify --feature 003-dependabot-remediation-piece-3-langchain --phase 1`
  (runs `python -m pytest tests/test_requirements.py tests/test_imports.py tests/test_langchain_migration.py tests/test_embedder.py -v`):
  exit 0, 20 passed.

**Deviations:**
- `pages/3_Robby-Youtube.py`: `answer = llm(...)` becomes `answer = llm.invoke(...)`,
  although the plan says to leave the call. LangChain 1.x chat models aren't callable
  (`BaseChatModel` has no `__call__`; checked), so the summary button would raise
  `TypeError` at run time. `invoke` returns the same `AIMessage` the old call did. The
  tests can't press that button (it needs an OpenAI key and YouTube), so
  `test_youtube_page_uses_langchain_1x_imports` also asserts `llm.invoke(` is used.
- `requirements.txt` was edited in place byte for byte (BOM, CRLF and the final line
  break kept) rather than rewritten with `"\r\n".join(...)`, which would drop the last
  line break.
- `test_chatbot_uses_langchain_1x_imports_and_invoke` checks that the old
  `chain(chain_input)` is gone after removing the new `chain.invoke(chain_input)`, since
  the second string contains the first.

## Phase 2: Offline chatbot chain test

**Status:** passed

**Files changed:** `tests/test_chatbot.py`

`Chatbot.conversational_chat` runs the migrated `ConversationalRetrievalChain` with a fake
chat model whose token counter needs no download, over a FAISS store of fake embeddings.

**Commands:**
- `sdlc_stage.py verify --feature 003-dependabot-remediation-piece-3-langchain --phase 2`
  (runs `python -m pytest tests/test_chatbot.py -v`): exit 0, 2 passed. Also passes
  without `HF_HUB_OFFLINE`, as the pipeline runs it.

**Deviations:** none. The file is the plan's text.
