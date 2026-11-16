import importlib.util
import os
import sys
from pathlib import Path

PROBE = Path(__file__).resolve().parents[1] / "embeddings" / "__pytest_cleanup_probe__.pkl"


def _load_conftest():
    spec = importlib.util.spec_from_file_location("sdlc_conftest", Path("tests/conftest.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_repo_root_on_sys_path() -> None:
    assert str(Path(__file__).resolve().parents[1]) in sys.path


def test_openai_api_key_is_test_key() -> None:
    assert os.environ["OPENAI_API_KEY"] == "sk-test"


def test_fixture_removes_probe_after_test() -> None:
    PROBE.parent.mkdir(exist_ok=True)
    PROBE.write_bytes(b"probe")
    assert PROBE.exists()


def test_fixture_probe_is_gone() -> None:
    assert not PROBE.exists()


def test_cleanup_handles_missing_embeddings_dir(tmp_path, monkeypatch) -> None:
    module = _load_conftest()
    monkeypatch.setattr(module, "REPO_ROOT", tmp_path)
    module._cleanup_embeddings(set())
    assert not (tmp_path / "embeddings").exists()


def test_cleanup_handles_empty_embeddings_dir(tmp_path, monkeypatch) -> None:
    (tmp_path / "embeddings").mkdir()
    module = _load_conftest()
    monkeypatch.setattr(module, "REPO_ROOT", tmp_path)
    module._cleanup_embeddings(set())
    assert (tmp_path / "embeddings").is_dir()
