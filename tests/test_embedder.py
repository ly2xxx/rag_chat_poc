from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.fake import FakeEmbeddings
from langchain_community.vectorstores import FAISS

def test_wales_pdf_returns_three_similarity_documents() -> None:
    pdf_path = Path("playground/sample_documents/wales-in-world.pdf")
    documents = PyPDFLoader(str(pdf_path)).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    split_documents = splitter.split_documents(documents)
    vectors = FAISS.from_documents(split_documents, FakeEmbeddings(size=8))
    results = vectors.similarity_search("Wales", k=3)
    assert len(results) == 3
