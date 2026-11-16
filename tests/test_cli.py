import subprocess
import sys

PREFIX = "Sentence Transformers:"


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "app/__main__.py", *args],
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )


def test_two_arguments_print_sentence_transformers_score_above_0_99() -> None:
    result = _run_cli("a cat", "a cat")
    assert result.returncode == 0, result.stderr
    scores = [
        float(line.split(":", 1)[1].strip())
        for line in result.stdout.splitlines()
        if line.startswith(PREFIX)
    ]
    assert len(scores) == 1, result.stdout
    assert scores[0] > 0.99


def test_one_argument_exits_with_code_one() -> None:
    result = _run_cli("a cat")
    assert result.returncode == 1
