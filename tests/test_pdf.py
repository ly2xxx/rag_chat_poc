from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def test_sample_pdfs_have_non_empty_text() -> None:
    pdf_paths = sorted(Path("playground/sample_documents").glob("*.pdf"))
    assert pdf_paths, "Expected at least one sample PDF in playground/sample_documents"
    for pdf_path in pdf_paths:
        documents = PyPDFLoader(str(pdf_path)).load()
        assert any(
            document.page_content.strip() for document in documents
        ), f"No non-empty text in {pdf_path}"
