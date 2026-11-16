from pathlib import Path


def _active_source(path: str) -> str:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return "\n".join(line for line in lines if not line.lstrip().startswith("#"))


def test_chatbot_uses_langchain_1x_imports_and_invoke() -> None:
    source = Path("modules/chatbot.py").read_text(encoding="utf-8")
    for line in (
        "from langchain_openai import ChatOpenAI",
        "from langchain_classic.chains import ConversationalRetrievalChain",
        "from langchain_core.prompts import PromptTemplate",
        "from langchain_core.globals import set_verbose",
        "set_verbose(False)",
    ):
        assert line in source
    assert "import langchain\n" not in source and "langchain.verbose" not in source
    active = _active_source("modules/chatbot.py")
    assert "chain.invoke(chain_input)" in active and "chain.invoke(query)" in active
    assert "chain(chain_input)" not in active.replace("chain.invoke(chain_input)", "")
    assert "chain.run(query)" not in active


def test_embedder_uses_langchain_1x_imports() -> None:
    source = Path("modules/embedder.py").read_text(encoding="utf-8")
    assert "from langchain_openai import OpenAIEmbeddings" in source
    assert "from langchain_text_splitters import RecursiveCharacterTextSplitter" in source
    active = _active_source("modules/embedder.py")
    assert "langchain.embeddings.openai" not in active and "langchain.text_splitter" not in active


def test_youtube_page_uses_langchain_1x_imports() -> None:
    source = Path("pages/3_Robby-Youtube.py").read_text(encoding="utf-8")
    assert "from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate" in source
    assert "from langchain_openai import ChatOpenAI" in source
    active = _active_source("pages/3_Robby-Youtube.py")
    assert "langchain.prompts" not in active and "langchain_community.chat_models" not in active
    # LangChain 1.x chat models aren't callable: the summary must use invoke().
    assert "llm.invoke(" in active and "llm(" not in active


def test_evaluator_uses_langchain_classic_import() -> None:
    assert "from langchain_classic.evaluation import load_evaluator" in Path("filename.py").read_text(encoding="utf-8")
    assert "langchain.evaluation" not in _active_source("filename.py")


def test_test_embedder_uses_langchain_text_splitters() -> None:
    source = Path("tests/test_embedder.py").read_text(encoding="utf-8")
    assert "from langchain_text_splitters import RecursiveCharacterTextSplitter" in source
    assert "from langchain.text_splitter import" not in _active_source("tests/test_embedder.py")
