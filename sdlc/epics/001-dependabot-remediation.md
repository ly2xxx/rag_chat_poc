# Dependabot remediation: status

Design: [`docs/dependabot-remediation.md`](../../docs/dependabot-remediation.md) · Alerts: issue #4 · Base branch: `main` · State: in progress

| Piece | Feature | Issue | Pull request | Alerts closed | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1: Test baseline and unused packages | `001-dependabot-remediation-piece-1-test-base` | #6, #12 | #13 | pending the monitor rerun | merged |
| 2: Flask, Streamlit and pypdf | | | | | planned |
| 3: LangChain 1.x | | | | | planned |
| 4: Torch and sentence-transformers | | | | | planned |

Status is one of: `planned`, `building` (the run has started), `in review` (the
pipeline's pull request is open), `merged`.

## Next

Record the alerts piece 1 closed (the monitor reruns 10 minutes after #13), then start piece 2.

## Deviations and follow-ups

Piece 1 (details in its `build-log.md`):
- Four interim pins beyond the plan, so a fresh install works: `pyarrow==25.0.0`,
  `transformers==4.46.3`, `huggingface-hub==0.25.2`, `werkzeug==2.0.3`;
  `test_exact_order_and_pins` expects 22 lines, not the plan's 18.
- The security scan blocked the first build run on 8 HIGH CVEs in the transformers and
  Werkzeug pins. The owner accepted them until pieces 2 and 4: `.trivyignore` (#11),
  then a `start: build` run (#12) opened #13.
- Review concern left as it is: `test_fixture_probe_is_gone` depends on test order (the
  plan's own design).
