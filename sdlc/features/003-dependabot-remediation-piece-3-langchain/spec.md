<!-- sdlc stage=spec model=deepseek-v4.1-flash:cloud from=intent.md,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#done,docs/dependabot-remediation.md#piece-3@9db5a65 -->
## Summary
Move the pinned dependencies to the approved LangChain 1.x set, remove `openai==0.27.7`, and update the live imports and invocation APIs named by piece 3 while preserving existing page titles, widgets and behaviour. Add offline tests for the chat chain and evaluator, update `tests/test_requirements.py` expectations, and keep the existing suite passing.

## Behaviour
1. Given `requirements.txt`, when it is read as raw bytes, then it starts with the UTF-8 BOM `b"\xef\xbb\xbf"` and every line break is CRLF.
2. Given `requirements.txt`, when `tests/test_requirements.py` extracts its non-comment, non-empty package lines, then they equal the updated `EXPECTED` ordered list in Interfaces.
3. Given `requirements.txt`, when package names are checked, then no package name contains `cuda`, `cudnn`, `cublas` or `nccl`.
4. Given the repository root, when `tests/test_imports.py` imports every `modules/*.py` module, then no module raises an exception.
5. Given `modules/chatbot.py`, when its source is inspected, then it imports `ChatOpenAI` from `langchain_openai`, `ConversationalRetrievalChain` from `langchain_classic.chains`, `PromptTemplate` from `langchain_core.prompts`, and `set_verbose` from `langchain_core.globals`, calls `set_verbose(False)`, and contains no `import langchain` or `langchain.verbose`.
6. Given `modules/chatbot.py`, when its source is inspected, then it contains `chain.invoke(chain_input)` and `chain.invoke(query)` and does not contain `chain(chain_input)` or `chain.run(query)`.
7. Given `modules/embedder.py`, when its source is inspected, then it imports `OpenAIEmbeddings` from `langchain_openai` and `RecursiveCharacterTextSplitter` from `langchain_text_splitters`, and does not use `langchain.embeddings.openai` or `langchain.text_splitter`.
8. Given `pages/3_Robby-Youtube.py`, when its source is inspected, then it imports prompts from `langchain_core.prompts` and `ChatOpenAI` from `langchain_openai`, and does not use `langchain.prompts` or `langchain_community.chat_models`.
9. Given `filename.py`, when its source is inspected, then it imports `load_evaluator` from `langchain_classic.evaluation` and does not use `langchain.evaluation`.
10. Given `tests/test_embedder.py`, when its source is inspected, then `RecursiveCharacterTextSplitter` is imported from `langchain_text_splitters` and not from `langchain.text_splitter`.
11. Given `tests/test_embedder.py`, when `test_wales_pdf_returns_three_similarity_documents` runs, then it passes and returns three similarity documents.
12. Given `OfflineFakeChat`, when `get_num_tokens(text)` is called, then it returns `len(text.split())`, including `0` for an empty string.
13. Given `tests/test_chatbot.py` patches `modules.chatbot.ChatOpenAI` to `lambda **kwargs: OfflineFakeChat(responses=["hi"])`, builds FAISS with `FAISS.from_texts([three short texts], FakeEmbeddings(size=8))`, and sets `st.session_state["history"] = []`, when `conversational_chat("q")` is called, then the returned string starts with `hi` and `st.session_state["history"] == [("q", "hi")]`.
14. Given `tests/test_evaluator.py` runs `AppTest.from_file("filename.py")` with empty text inputs, when the page loads, then no exception is raised.
15. Given the same `AppTest` run, when `text_input[0]` is set to `abc`, `text_input[1]` is set to `abd`, and `button[0]` is clicked, then a markdown element contains `Similarity score`.
16. Given the repository root, when the full pytest suite runs without network access, a real OpenAI key or a GPU, then every earlier test not explicitly changed by this piece passes and the new tests pass.

## Interfaces
**requirements.txt**  
The non-comment package lines, in order, become:
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
`openai==0.27.7` is removed. Existing comment lines are not package lines and are not added to `EXPECTED`.

**tests/test_requirements.py**  
`EXPECTED` remains the existing module-level constant name; its value becomes the same ordered list shown for `requirements.txt`.

**modules/chatbot.py**  
Import and call changes only; existing signatures remain unchanged:
- `ChatOpenAI` from `langchain_openai`
- `ConversationalRetrievalChain` from `langchain_classic.chains`
- `PromptTemplate` from `langchain_core.prompts`
- `set_verbose` from `langchain_core.globals`, called as `set_verbose(False)`
- existing `class Chatbot` with `def __init__(self, model_name, temperature, vectors)` and `def conversational_chat(self, query)`
- existing `def count_tokens_chain(chain, query)`

**modules/embedder.py**  
Import changes only; existing signatures remain unchanged:
- `OpenAIEmbeddings` from `langchain_openai`
- `RecursiveCharacterTextSplitter` from `langchain_text_splitters`
- existing `class Embedder` methods keep their current names and parameters.

**pages/3_Robby-Youtube.py**  
Import changes only; existing `def get_youtube_id(url)` remains unchanged:
- prompts from `langchain_core.prompts`
- `ChatOpenAI` from `langchain_openai`

**filename.py**  
Import change only:
- `load_evaluator` from `langchain_classic.evaluation`

**tests/test_embedder.py**  
Import change only; existing `def test_wales_pdf_returns_three_similarity_documents() -> None` remains unchanged:
- `RecursiveCharacterTextSplitter` from `langchain_text_splitters`

**tests/test_chatbot.py**  
New test file adds:
```python
class OfflineFakeChat(FakeListChatModel):
    def get_num_tokens(self, text)
```
`FakeListChatModel` is imported from `langchain_core.language_models.fake_chat_models`; `get_num_tokens` returns `len(text.split())`. Test function names are not specified by the approved design.

**tests/test_evaluator.py**  
New test file uses `streamlit.testing.v1.AppTest` with `AppTest.from_file("filename.py")`; no new production interface is added.

## Out of scope
Other Dependabot alerts not named by this piece, including `torch`, `sentence-transformers` and `transformers`, and `.trivyignore` cleanup reserved for later pieces. Refactoring, new features, changes to commented-out code, and changes to page titles, widgets or behaviour. CUDA packages, `playground/`, notebooks, `Gallery/`, `.devcontainer/`, and `.github/`.

## Open questions
Issue #4 lists LangChain minimum upgrade versions below the approved piece pin versions (`langchain` 1.3.9 vs 1.5.0; `langchain-community` 0.3.27 vs 0.4.2). Assumption: the approved higher pins satisfy the “at least” rule.
