# Synthetic regression tests

This project uses a synthetic regression corpus to verify masking behavior without using real personal or confidential data.

No real personal data should be included in public tests.

## Current baseline

```text
PASS 44 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 44
Blocking errors: 0
```

## Run tests

Text-block synthetic regression suite:

```bash
python run_regression_tests.py run-strict
```

or on Windows:

```bat
run_regression_tests.bat
```

Document-level regression suite for generated DOCX/PDF fixtures:

```bash
python -m pytest -q tests/test_document_level_regression.py
```

The document-level suite generates synthetic files during the test run. It does not store real or fixture DOCX/PDF files in the repository.

## XFAIL / known gaps

Known gaps can be represented as `XFAIL` so that desired future behavior is tracked without blocking the current MVP.

Current public synthetic XFAIL cases: none.

Former XFAIL cases fixed in Sprint 0.6:

- INN with spaces;
- INN with OCR-letter substitution.

Sprint 1.1 adds the first recognition quality pack for common synthetic false negatives: spaced SNILS, separated passport series/number, spaced BIK/KPP/OGRN, quoted private organizations, address index context, one-digit sensitive dates, and mobile phone context.

## Adding tests

New tests should be synthetic and should avoid real personal data.

Recommended structure for text-block detection rules:

- add a synthetic input case;
- define expected token behavior;
- include both positive and negative cases where possible;
- run the regression tool before changing core detection logic.

Recommended structure for document-level behavior:

- generate DOCX/PDF fixtures inside pytest using synthetic values only;
- avoid committing generated DOCX/PDF files;
- assert both output content and processing status;
- include safe-failure tests for unsupported inputs such as image-only PDFs.

## Notes

Sprint 0.6 fixed the former INN spacing and OCR-letter substitution synthetic gaps.

The current baseline does not mean the tool has no real-world limitations. Manual review remains required before external sharing.
