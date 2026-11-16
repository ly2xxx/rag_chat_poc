from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_PATHS = [Path("streamlit_app.py"), *sorted(Path("pages").glob("*.py"))]

@pytest.mark.parametrize("app_path", APP_PATHS, ids=lambda path: str(path))
def test_streamlit_file_runs_without_exception(app_path: Path) -> None:
    app = AppTest.from_file(str(app_path), default_timeout=60).run()
    assert len(app.exception) == 0
