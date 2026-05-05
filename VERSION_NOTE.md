# VERSION NOTE — Sprint 0.6

Project: BeforeSending / local-doc-pseudonymizer
Date: 2026-05-04
Scope: controlled mini-sprint, synthetic-only regression

## Sprint 0.6 — INN normalization and OCR-suspect handling

Implemented controlled handling for two previously known INN gaps:

- spaced/hyphenated INN values near an explicit `ИНН` label are normalized for detection and masked as `INN`;
- OCR-like INN values near an explicit `ИНН` label are masked as `OCR_SUSPECT_INN` and kept in the suspect/review path.

The existing `OCR_SUSPECT_INN` taxonomy is reused. No OCR engine was added.

## Verified regression result

```text
PASS 34 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 34
Blocking errors: 0
```

Validated with:

```bash
python3 run_regression_tests.py run
python3 run_regression_tests.py run-strict
```

Latest verified report:

```text
output/reports/regression_report_2026-05-04_00-08-07.md
```

## Safety notes

- No real documents or real personal data are included in this snapshot/bundle.
- No broad long-number detector was added.
- Service-number contexts remain protected by new negative regression tests.
- `1_anonymize.py` remains a legacy compatibility wrapper around `pseudonymize.py`.
