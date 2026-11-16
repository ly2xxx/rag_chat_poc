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


def test_offline_fake_chat_counts_words() -> None:
    model = OfflineFakeChat(responses=["hi"])
    assert model.get_num_tokens("") == 0
    assert model.get_num_tokens("one two three") == 3


def test_conversational_chat_returns_hi_and_records_history(monkeypatch) -> None:
    monkeypatch.setattr("modules.chatbot.ChatOpenAI", lambda **kwargs: OfflineFakeChat(responses=["hi"]))
    st.session_state["history"] = []
    try:
        answer = Chatbot(model_name="test-model", temperature=0.0, vectors=_build_vectors()).conversational_chat("q")
        assert answer.startswith("hi")
        assert st.session_state["history"] == [("q", "hi")]
    finally:
        st.session_state["history"] = []
