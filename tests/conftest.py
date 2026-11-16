import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

def _embeddings_pkls() -> set[Path]:
    embeddings_dir = REPO_ROOT / "embeddings"
    if not embeddings_dir.is_dir():
        return set()
    return {path.resolve() for path in embeddings_dir.glob("*.pkl")}

def _cleanup_embeddings(baseline: set[Path]) -> None:
    embeddings_dir = REPO_ROOT / "embeddings"
    if not embeddings_dir.is_dir():
        return
    for path in embeddings_dir.glob("*.pkl"):
        if path.resolve() not in baseline:
            path.unlink()

@pytest.fixture(autouse=True)
def _test_environment():
    baseline = _embeddings_pkls()
    os.environ["OPENAI_API_KEY"] = "sk-test"
    yield
    _cleanup_embeddings(baseline)
