<!-- sdlc stage=intent model=deepseek-v4.1-flash:cloud from=idea,docs/dependabot-remediation.md#rules-for-every-piece,docs/dependabot-remediation.md#facts-the-plan-must-not-guess,docs/dependabot-remediation.md#done,docs/dependabot-remediation.md#piece-4@550ef0d -->
# Intent: Dependabot remediation piece 4: torch and sentence-transformers

**Owner:** @ly2xxx · **Status:** proposed (approving the review gate approves it)

## Problem
The similarity feature still depends on torch 2.1.0 and sentence-transformers 2.2.2, which carry critical Dependabot alerts, and on transformers pins whose CVEs are currently only suppressed by `.trivyignore`. This leaves known vulnerabilities in the installed application and prevents the Dependabot remediation from reaching a clean state. Users and maintainers inherit that risk whenever the pipeline installs and runs the local similarity model.

## Outcome
Similarity scoring and the CLI run on the approved fixed versions of `torch`, `sentence-transformers`, `transformers` and `huggingface-hub`, installed with the rest of the pins on Python 3.11. The local `all-MiniLM-L6-v2` model still loads offline, the existing scoring and page behaviour is unchanged, and the last accepted transformers CVEs are no longer suppressed by `.trivyignore`.

## Done when
- `requirements.txt` changes the four pins in place and the full pin set installs on Python 3.11 with the pipeline's install command, without CUDA packages.
- The local model still loads offline and scores identical sentences 1.0, the cat paraphrase 0.984 and the stock sentence 0.079; `app/__main__.py` prints `Sentence Transformers: 1.0` for `"a cat" "a cat"`.
- `.trivyignore` and `tests/test_trivyignore.py` are deleted.
- `tests/test_cli.py` verifies that two arguments print a `Sentence Transformers:` line with a value above 0.99 and that one argument exits 1; `tests/test_requirements.py` expects the new pins and asserts `.trivyignore` does not exist.
- The existing tests still pass.

## Not in scope
Application-code changes; the approved design says none are needed. Converting or downloading the local model, or changing `all-MiniLM-L6-v2/`. Refactoring, new features, or changes to page titles, widgets or behaviour. CUDA packages. `playground/`, notebooks, `Gallery/`, `.devcontainer/`, `.github/`, and alerts in packages this piece does not name.

## Open questions
The idea names torch and sentence-transformers, while the approved piece 4 design also pins transformers and huggingface-hub and deletes the obsolete `.trivyignore`; assumption: the piece 4 design is authoritative and those changes are in scope.

## Design
Written from these approved sections, which the spec and plan stages read word for word:
- `docs/dependabot-remediation.md#rules-for-every-piece`
- `docs/dependabot-remediation.md#facts-the-plan-must-not-guess`
- `docs/dependabot-remediation.md#done`
- `docs/dependabot-remediation.md#piece-4`

