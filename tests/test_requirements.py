from pathlib import Path

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
    "sentence-transformers==5.6.0",
    "torch==2.13.0",
    # Pins a fresh install needs with the pins above (build-log.md, Phase 1 deviations).
    "pyarrow==25.0.0",
    "transformers==5.23.0",
    "huggingface-hub==2.4.0",
    "werkzeug==3.1.9",
    "langchain-openai==1.8.0",
    "langchain-text-splitters==1.1.3",
    "langchain-classic==1.0.8",
    "rapidfuzz==3.14.6",
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



def test_gitignore_ignores_embeddings() -> None:
    assert "embeddings/" in [line.strip() for line in Path(".gitignore").read_text().splitlines()]


def test_streamlit_app_has_no_pandasai_mention() -> None:
    assert "PandasAI" not in Path("streamlit_app.py").read_text(encoding="utf-8")


def test_requirements_keeps_utf8_bom_and_crlf() -> None:
    raw = Path("requirements.txt").read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf")
    assert raw.count(b"\n") == raw.count(b"\r\n")
