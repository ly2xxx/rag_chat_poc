from pathlib import Path

def test_werkzeug_ignores_and_comment_removed() -> None:
    lines = [
        line.strip()
        for line in Path(".trivyignore").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert not any("werkzeug" in line.lower() for line in lines)
    cve_lines = [line for line in lines if not line.startswith("#")]
    assert len(cve_lines) == 6
