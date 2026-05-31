# Version note — v0.2-alpha candidate checkpoint

Project: BeforeSending / local-doc-pseudonymizer
Date: 2026-05-31
Scope: release/docs hygiene checkpoint after Sprint 1.2
Status: candidate note, not a final release tag by itself

## Summary

This checkpoint aligns the public documentation and release hygiene around the current post-Sprint-1.2 baseline.

The project remains an experimental local-first pseudonymization / reversible masking / risk-reduction tool. It is not a guaranteed anonymization solution, not a legal compliance product and not an enterprise DLP system.

## Current verified baseline

```text
PASS 52 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 52
Document-level pytest: 5 passed
```

Validated with:

```bash
python -m py_compile pseudonymize.py
python run_regression_tests.py run-strict
python -m pytest -q tests/test_document_level_regression.py
```

## Included since earlier public baseline

- Sprint 0.8 — PDF safe handling.
- Sprint 0.9 — DOCX table-aware context.
- Sprint 1.0 — document-level regression tests.
- Sprint 1.1 — Russian recognition quality pack v1.
- Sprint 1.2 — minimal label-driven English profile.
- Release/docs hygiene alignment.

## Documentation aligned

- `README.md`.
- `STATUS.md`.
- `ROADMAP.md`.
- `CHANGELOG.md`.
- `docs/limitations.md`.
- `docs/supported_entities.md`.
- `docs/review_workflow.md`.
- `docs/token_dictionary_security.md`.
- `docs/safe_bug_reports.md`.
- `docs/synthetic_regression_report_latest.md`.
- `.github/ISSUE_TEMPLATE/*`.

## Safety notes

Do not commit, upload or share:

- real input documents;
- real output documents;
- token dictionaries;
- review reports based on real data;
- feedback files generated from real data;
- screenshots with personal or confidential data;
- private manual rule files.

Future recognition improvements should be made only through synthetic regression cases.
