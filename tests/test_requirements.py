from pathlib import Path

EXPECTED = [
    "langchain==0.2.11",
    "openai==0.27.7",
    "langchain-community==0.2.10",
    "pdfplumber==0.11.4",
    "pypdf==3.9.0",
    "streamlit==1.31.1",
    "streamlit-chat==0.0.2.2",
    "tiktoken==0.4.0",
    "youtube-transcript-api==0.6.0",
    "faiss-cpu==1.9.0",
    "requests==2.32.3",
    "bs4==0.0.2",
    "st-pages==0.5.0",
    "flask==2.0.2",
    "sentence-transformers==2.2.2",
    "torch==2.1.0",
    # Pins a fresh install needs with the pins above (build-log.md, Phase 1 deviations).
    "pyarrow==25.0.0",
    "transformers==4.46.3",
    "huggingface-hub==0.25.2",
    "pandas==2.3.3",
    "python-dotenv==1.2.4",
]


def _package_lines() -> list[str]:
    lines = Path("requirements.txt").read_text(encoding="utf-8-sig").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]


def test_removed_packages_absent() -> None:
    names = {line.split("==")[0] for line in _package_lines()}
    assert not names & {"pandasai", "playwright", "pytube"}


def test_pandas_and_dotenv_at_end() -> None:
    assert _package_lines()[-2:] == ["pandas==2.3.3", "python-dotenv==1.2.4"]


def test_exact_order_and_pins() -> None:
    assert _package_lines() == EXPECTED


def test_no_cuda_packages() -> None:
    for line in _package_lines():
        name = line.split("==")[0].lower()
        assert not any(word in name for word in ("cuda", "cudnn", "cublas", "nccl")), line


def test_st_pages_exports() -> None:
    from st_pages import hide_pages, show_pages_from_config, add_page_title, show_pages, Page, Section  # noqa: F401


def test_gitignore_ignores_embeddings() -> None:
    assert "embeddings/" in [line.strip() for line in Path(".gitignore").read_text().splitlines()]


def test_streamlit_app_has_no_pandasai_mention() -> None:
    assert "PandasAI" not in Path("streamlit_app.py").read_text(encoding="utf-8")
