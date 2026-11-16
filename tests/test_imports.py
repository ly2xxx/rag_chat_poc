import importlib
from pathlib import Path

import pytest

MODULES = sorted(path for path in Path("modules").glob("*.py") if path.name != "__init__.py")

@pytest.mark.parametrize("module_path", MODULES, ids=lambda path: path.stem)
def test_every_module_imports(module_path: Path) -> None:
    importlib.import_module(f"modules.{module_path.stem}")
