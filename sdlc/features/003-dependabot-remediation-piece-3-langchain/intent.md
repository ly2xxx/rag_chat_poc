<!-- sdlc stage=intent model=deepseek-v4.1-flash:cloud from=idea,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#done,docs/dependabot-remediation.md#piece-3@156f712 -->
# Intent: LangChain 1.x remediation

**Owner:** @ly2xxx · **Status:** proposed (approving the review gate approves it)

## Problem
The RAG chatbot still pins LangChain 0.2.x and the retired `openai==0.27.7` client. Users and maintainers cannot rely on a clean current LangChain install, and the open Dependabot alerts for LangChain remain unresolved. This leaves live code on outdated APIs and blocks the broader dependency remediation.

## Outcome
The pinned dependency set is moved to LangChain 1.x with `openai==0.27.7` removed: `langchain==1.5.0`, `langchain-community==0.4.2`, `tiktoken==0.14.0`, `langchain-openai==1.8.0`, `langchain-text-splitters==1.1.3`, `langchain-classic==1.0.8`, and `rapidfuzz==3.14.6` are pinned consistently with the existing file. Live code uses the LangChain 1.x import paths and invocation APIs while keeping each page’s title, widgets and behaviour. Offline tests cover the chat chain and evaluator with fakes, and the existing suite continues to pass.

## Done when
- `requirements.txt` keeps its UTF-8 BOM and CRLF line endings, removes `openai==0.27.7`, changes the named pins in place, adds the new pins before `pandas`, and installs with the pipeline’s Python 3.11 command.
- Live imports and calls are updated as approved: `modules/chatbot.py` uses `langchain_openai`, `langchain_classic.chains`, `langchain_core.prompts`, `set_verbose(False)` and `invoke`; `modules/embedder.py`, `pages/3_Robby-Youtube.py`, `filename.py`, and `tests/test_embedder.py` use their approved LangChain 1.x import paths.
- `tests/test_chatbot.py` runs offline with `OfflineFakeChat` and `FakeEmbeddings`, returns an answer starting with `hi`, records history as `[("q", "hi")]`, and does not download a tokenizer or use the network.
- `tests/test_evaluator.py` runs `filename.py` through `AppTest` without exception; after entering `abc` and `abd` and clicking the button, a markdown element contains “Similarity score”.
- `tests/test_requirements.py` `EXPECTED` matches the new ordered pins, and every earlier test not explicitly changed by this piece still passes.
- The existing tests still pass.

## Not in scope
Other Dependabot alerts not named by this piece, including torch, sentence-transformers and transformers, and `.trivyignore` cleanup reserved for later pieces. Refactoring, new features, changes to commented-out code, and changes to page titles, widgets or behaviour. CUDA packages, `playground/`, notebooks, `Gallery/`, `.devcontainer/`, and `.github/`.

## Open questions
- Issue #4 lists LangChain minimum upgrade versions below the approved piece pin versions (`langchain` 1.3.9 vs 1.5.0; `langchain-community` 0.3.27 vs 0.4.2). Assumption: the approved higher pins satisfy the “at least” rule.

## Design
Written from these approved sections, which the spec and plan stages read word for word:
- `docs/dependabot-remediation.md#rules-for-every-piece`
- `docs/dependabot-remediation.md#facts-the-plan-must-not-guess`
- `docs/dependabot-remediation.md#done`
- `docs/dependabot-remediation.md#piece-3`

