<!-- sdlc stage=plan model=deepseek-v4.1-flash:cloud from=intent.md,spec.md,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#done,docs/dependabot-remediation.md#piece-4@db462df -->
## Approach
Write the four replacement pins into `requirements.txt` in place, mirroring them in `EXPECTED` in `tests/test_requirements.py`; delete the now-obsolete `.trivyignore` and its test while asserting the file stays gone; then add `tests/test_cli.py` and `tests/test_similarity_scores.py` that prove the local `all-MiniLM-L6-v2` model still loads offline with the new stack, scores 1.0 / 0.984 / 0.079, and that `app/__main__.py` prints a score above 0.99 for two arguments and exits 1 for one. No application code, model files, or page behaviour change.

## Coverage

| Done when (intent.md) | Spec behaviours | Phase |
| :-- | :-- | :-- |
| `requirements.txt` changes the four pins in place and the full pin set installs on Python 3.11 with the pipeline's install command, without CUDA packages. | 1, 2, 3 | Phase 1 (install itself is proven by the verify job's install step, see Open questions) |
| The local model still loads offline and scores identical sentences 1.0, the cat paraphrase 0.984 and the stock sentence 0.079; `app/__main__.py` prints `Sentence Transformers: 1.0` for `"a cat" "a cat"`. | 4, 5, 6, 7 | Phase 3 |
| `.trivyignore` and `tests/test_trivyignore.py` are deleted. | 9, 10 | Phase 2 |
| `tests/test_cli.py` verifies that two arguments print a `Sentence Transformers:` line with a value above 0.99 and that one argument exits 1; `tests/test_requirements.py` expects the new pins and asserts `.trivyignore` does not exist. | 1, 7, 8, 9 | Phase 1 (pins), Phase 2 (absence test), Phase 3 (`test_cli.py`) |
| The existing tests still pass. | 11 | Phase 1, Phase 2, Phase 3 (whole suite in final verification) |

## Phase 1: Update the four pins in place
<!-- phase: 1 -->
<!-- targets: requirements.txt, tests/test_requirements.py -->
<!-- frozen: app/__main__.py, modules/similarity.py, tests/conftest.py, tests/test_chatbot.py, tests/test_conftest.py, tests/test_embedder.py, tests/test_evaluator.py, tests/test_flask.py, tests/test_imports.py, tests/test_langchain_migration.py, tests/test_navigation.py, tests/test_pages.py, tests/test_pdf.py, tests/test_similarity.py, tests/test_trivyignore.py -->

**Goal:** `requirements.txt` carries `sentence-transformers==5.6.0`, `torch==2.13.0`, `transformers==5.23.0` and `huggingface-hub==2.4.0` at their old positions, with every other line, the UTF-8 BOM and the CRLF endings unchanged, and `EXPECTED` matches it.

**Changes:**
- `requirements.txt`: replace exactly the line `sentence-transformers==2.2.2` with `sentence-transformers==5.6.0`, `torch==2.1.0` with `torch==2.13.0`, `transformers==4.46.3` with `transformers==5.23.0`, and `huggingface-hub==0.25.2` with `huggingface-hub==2.4.0`. Keep all other non-comment lines and the `# pywin32==308` comment in the same order; add, remove, rename or reorder nothing else. Preserve the file's leading UTF-8 BOM (bytes `EF BB BF`, so `﻿langchain==1.5.0` stays the first line) and its CRLF (`\r\n`) terminators on every line.
- `tests/test_requirements.py`: change the `EXPECTED` list only — replace `"sentence-transformers==2.2.2"` with `"sentence-transformers==5.6.0"`, `"torch==2.1.0"` with `"torch==2.13.0"`, `"transformers==4.46.3"` with `"transformers==5.23.0"`, and `"huggingface-hub==0.25.2"` with `"huggingface-hub==2.4.0"`, each at the same index as before. Leave the `# Pins a fresh install needs...` comment, `_package_lines() -> list[str]`, and all other `EXPECTED` entries and test functions untouched.

**Definition of done:**
- [ ] `tests/test_requirements.py`, test `test_exact_order_and_pins` (its `EXPECTED` data is extended — this is the phase's test change): proves spec behaviour 1 by asserting `_package_lines() == EXPECTED` with the four new pins at their original indices; no fixtures, no teardown.
- [ ] `tests/test_requirements.py`, test `test_no_cuda_packages`: proves behaviour 2 — for each `_package_lines()` entry it lowercases the name before `==` and asserts `not any(word in name for word in ("cuda", "cudnn", "cublas", "nccl"))`.
- [ ] `tests/test_requirements.py`, test `test_requirements_keeps_utf8_bom_and_crlf`: proves behaviour 3 — reads `Path("requirements.txt").read_bytes()`, asserts `raw.startswith(b"\xef\xbb\xbf")` and `raw.count(b"\n") == raw.count(b"\r\n")`.
- [ ] `tests/test_requirements.py`, tests `test_removed_packages_absent` and `test_pandas_and_dotenv_at_end`: prove the rest of the pin set is unchanged — no `pandasai`/`playwright`/`pytube`, and the last two entries remain `pandas==2.3.3`, `python-dotenv==1.2.4`.
- [ ] Observable check outside pytest: the PR's verify job runs `uv pip install --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt` on Python 3.11 before pytest; a resolver failure fails the PR before the block below.

**Verify:**
```bash
python -m pytest tests/test_requirements.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 2: Delete `.trivyignore` and its test
<!-- phase: 2 -->
<!-- targets: .trivyignore, tests/test_trivyignore.py, tests/test_requirements.py -->
<!-- frozen: requirements.txt, app/__main__.py, modules/similarity.py, tests/conftest.py, tests/test_chatbot.py, tests/test_conftest.py, tests/test_embedder.py, tests/test_evaluator.py, tests/test_flask.py, tests/test_imports.py, tests/test_langchain_migration.py, tests/test_navigation.py, tests/test_pages.py, tests/test_pdf.py, tests/test_similarity.py -->

**Goal:** `.trivyignore` and `tests/test_trivyignore.py` no longer exist, and a test in `tests/test_requirements.py` fails if `.trivyignore` ever returns.

**Changes:**
- Delete `.trivyignore` (the whole file, its six transformers CVE IDs and its comments).
- Delete `tests/test_trivyignore.py` (its only test, `test_werkzeug_ignores_and_comment_removed`).
- `tests/test_requirements.py`: append exactly this test after `test_requirements_keeps_utf8_bom_and_crlf`, reusing the module's existing `from pathlib import Path` import; change nothing else:

```python
def test_trivyignore_absent() -> None:
    assert Path(".trivyignore").exists() is False
```

**Definition of done:**
- [ ] `tests/test_requirements.py`, test `test_trivyignore_absent`: proves spec behaviour 9 and intent item 3 — asserts `Path(".trivyignore").exists() is False`; no fixture or teardown.
- [ ] `tests/test_trivyignore.py` is absent, so pytest can no longer collect it (spec behaviour 10): proved in Verify by `test ! -e tests/test_trivyignore.py`.
- [ ] `.trivyignore` is absent: proved by the new test and by `test ! -e .trivyignore`.
- [ ] No remaining file under `tests/` reads `.trivyignore` — `tests/test_similarity.py`, `tests/test_pages.py` and the rest are untouched, so pytest cannot fail on a missing file.

**Verify:**
```bash
python -m pytest tests/test_requirements.py -v
test ! -e .trivyignore
test ! -e tests/test_trivyignore.py
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Phase 3: Prove offline scoring and CLI behaviour on the new stack
<!-- phase: 3 -->
<!-- targets: tests/test_cli.py, tests/test_similarity_scores.py -->
<!-- frozen: requirements.txt, app/__main__.py, modules/similarity.py, tests/conftest.py, tests/test_chatbot.py, tests/test_conftest.py, tests/test_embedder.py, tests/test_evaluator.py, tests/test_flask.py, tests/test_imports.py, tests/test_langchain_migration.py, tests/test_navigation.py, tests/test_pages.py, tests/test_pdf.py, tests/test_requirements.py, tests/test_similarity.py -->

**Goal:** With the Phase 1 pins installed, the local `all-MiniLM-L6-v2` model loads offline and scores exactly 1.0, 0.984 and 0.079, and `app/__main__.py` prints a `Sentence Transformers:` score above 0.99 for two arguments and exits 1 for one.

**Changes:**
- New file `tests/test_cli.py`:

```python
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
```

- New file `tests/test_similarity_scores.py`:

```python
import pytest

from modules.similarity import SimilarityScorer


@pytest.fixture(scope="module")
def scorer() -> SimilarityScorer:
    return SimilarityScorer()


def test_identical_sentences_score_one(scorer: SimilarityScorer) -> None:
    sentence = "The quick brown fox jumps over the lazy dog."
    assert round(scorer.score(sentence, sentence), 3) == 1.0


def test_cat_paraphrase_scores_0_984(scorer: SimilarityScorer) -> None:
    score = scorer.score("a cat sits on the mat", "a cat is sitting on a mat")
    assert round(score, 3) == 0.984


def test_cat_vs_stock_prices_scores_0_079(scorer: SimilarityScorer) -> None:
    score = scorer.score("a cat sits on the mat", "stock prices fell today")
    assert round(score, 3) == 0.079
```

**Definition of done:**
- [ ] `tests/test_cli.py`, test `test_two_arguments_print_sentence_transformers_score_above_0_99`: proves spec behaviour 7 and the CLI half of intent item 2 — runs `subprocess.run([sys.executable, "app/__main__.py", "a cat", "a cat"])` from the repository root with `capture_output=True, text=True, timeout=600, check=False`, asserts return code 0, exactly one stdout line begins with `Sentence Transformers:`, and `float(line.split(":", 1)[1].strip()) > 0.99`. `subprocess.run` waits for the child, so no process teardown is needed.
- [ ] `tests/test_cli.py`, test `test_one_argument_exits_with_code_one`: proves behaviour 8 — same call with the single argument `"a cat"` returns `1`.
- [ ] `tests/test_similarity_scores.py`, test `test_identical_sentences_score_one`: proves behaviour 4 — module-scoped `SimilarityScorer` fixture (no files created; `tests/conftest.py`'s autouse `_test_environment` already sets `OPENAI_API_KEY=sk-test` and restores `embeddings/*.pkl`) and `round(score, 3) == 1.0`.
- [ ] `tests/test_similarity_scores.py`, test `test_cat_paraphrase_scores_0_984`: proves behaviour 5 — `round(score, 3) == 0.984`.
- [ ] `tests/test_similarity_scores.py`, test `test_cat_vs_stock_prices_scores_0_079`: proves behaviour 6 — `round(score, 3) == 0.079`.
- [ ] The model path is the local `./all-MiniLM-L6-v2` directory (both `modules/similarity.py` and `app/__main__.py`), so these tests use no network, no API key and no GPU.

**Verify:**
```bash
python -m pytest tests/test_cli.py tests/test_similarity_scores.py -v
```

**Attempt budget:** 3 failed attempts, then stop and revise this plan instead of retrying.

## Risks
- **The pin edit rewrites line endings or drops the BOM:** caught by Phase 1's `test_requirements_keeps_utf8_bom_and_crlf` (and by `test_exact_order_and_pins` if the pin text is wrong).
- **Pytest resolution picks a CUDA wheel:** the verify job forces the CPU extra index in the install command; Phase 1's `test_no_cuda_packages` only checks the names written in `requirements.txt`, so a transitively pulled CUDA package would pass the file test — the install command's `download.pytorch.org/whl/cpu` index is the real guard.
- **New torch/transformers/sentence-transformers combinations fail to import or to load `pytorch_model.bin`:** caught by all three Phase 3 tests and, on the final whole-suite run, by `tests/test_pages.py` and `tests/test_similarity.py`.
- **Exact scores drift (0.984 / 0.079) under the new stack:** caught by Phase 3's exact-score tests; per the attempt budget, stop and revise the plan rather than loosening the assertion.
- **`.trivyignore` deleted while `tests/test_trivyignore.py` survives:** would raise `FileNotFoundError` in any wider collection; Phase 2 deletes both in one change and its `test ! -e tests/test_trivyignore.py` check fails the PR if the test survives.
- **CLI stdout carries extra model-loading lines:** Phase 3 parses only lines beginning with `Sentence Transformers:` and asserts exactly one match.
- **Slow CPU model load exceeds a subprocess timeout:** the CLI test uses `timeout=600`; existing `AppTest` checks use 60s.
- **Phase 1 and Phase 2 both edit `tests/test_requirements.py`:** Phase 1's block is re-run on the finished branch, where the absence test is already present and `.trivyignore` is gone, so the block still passes.

## Open questions
- The approved design does not name the new test functions; assumption: the descriptive names listed in Phases 2 and 3 are accepted, with file locations and assertions fixed as written.
- Done-when #1's "installs on Python 3.11 with the pipeline's install command" cannot be reproduced by an offline pytest command; assumption (matching the spec's Open questions): the verify job's `uv pip install ... -r requirements.txt` step before pytest is the install proof, while Phase 1's tests prove the exact pins, absence of CUDA names and the BOM/CRLF bytes.
- The exact score assertions are added in a new `tests/test_similarity_scores.py` instead of changing `tests/test_similarity.py`, to honour the rule that earlier pieces' tests pass unchanged; assumption: adding a test file is in scope and changing `tests/test_similarity.py` is not.
- Available wheels: assumption that `torch==2.13.0`, `sentence-transformers==5.6.0`, `transformers==5.23.0` and `huggingface-hub==2.4.0` resolve with the CPU extra index, as the approved design says "checked"; if the install step fails, the plan must be revised rather than a pin lowered.

## Hand back
When every phase is built and its Verify block passes:
1. Create `sdlc/features/004-dependabot-remediation-piece-4-torch-and/build-log.md` with one section per phase, in order. Head each
   one `## Phase <n>: <title>`, then list the files changed, the Verify command
   you ran and its result, and any deviation from this plan (or "none").
2. Commit it and push it to `feature/004-dependabot-remediation-piece-4-torch-and`.

Commit only this plan's targets and `build-log.md`. Leave every other file alone,
including other features' documents under `sdlc/features/`, even for formatting;
verification fails on any file outside the targets.

The pipeline waits for this file. Once it has a section for every phase, it
verifies the whole branch and opens the pull request.

