# Version note — v0.2-alpha candidate checkpoint

Project: BeforeSending / local-doc-pseudonymizer
Date: 2026-06-01
Scope: release/docs hygiene checkpoint after Sprint 1.6
Status: historical candidate note, not a final release tag by itself and not a current roadmap

## Summary

This historical checkpoint aligned the public documentation and release hygiene around the post-Sprint-1.6 baseline.

The project remains an experimental local-first pseudonymization / reversible masking / risk-reduction tool. It is not a guarantee that documents are automatically safe, not a compliance tool, and not a DLP system.

## Current verified baseline

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
Pytest: 13 passed
Quality metrics dashboard: generated from strict synthetic regression results
```

Validated with:

```bash
python -m py_compile pseudonymize.py html_review_report.py quality_metrics.py run_regression_tests.py
python run_regression_tests.py run-strict
python run_regression_tests.py quality-metrics
python -m pytest -q
```

## Included since earlier public baseline

- Sprint 0.8 — PDF safe handling.
- Sprint 0.9 — DOCX table-aware context.
- Sprint 1.0 — document-level regression tests.
- Sprint 1.1 — Russian recognition quality pack v1.
- Sprint 1.2 — minimal label-driven English profile.
- Sprint 1.3 - Russian recognition quality pack v2.
- Sprint 1.4 - golden synthetic demo and release-ready walkthrough.
- Sprint 1.5 - local HTML review report.
- Sprint 1.6 - synthetic quality metrics dashboard.
- Release/docs hygiene alignment.

## Documentation aligned

- `README.md`.
- `STATUS.md`.
- `ROADMAP.md`.
- `CHANGELOG.md`.
- `docs/limitations.md`.
- `docs/supported_entities.md`.
- `docs/review_workflow.md`.
- `docs/synthetic_regression.md`.
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
- quality metrics reports not generated from verified synthetic regression only;
- feedback files generated from real data;
- screenshots with personal or confidential data;
- private manual rule files.

New recognition improvements should be made only through synthetic regression cases.
