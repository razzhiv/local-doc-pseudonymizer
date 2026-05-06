# Synthetic regression tests

This project uses a synthetic regression corpus to verify masking behavior without using real personal or confidential data.

No real personal data should be included in public tests.

## Current baseline

```text
PASS 34 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 34
Blocking errors: 0
```

## Run tests

```bash
python run_regression_tests.py run-strict
```

or on Windows:

```bat
run_regression_tests.bat
```

## XFAIL / known gaps

Known gaps can be represented as `XFAIL` so that desired future behavior is tracked without blocking the current MVP.

Current public synthetic XFAIL cases: none.

Former XFAIL cases fixed in Sprint 0.6:

- INN with spaces;
- INN with OCR-letter substitution.

## Adding tests

New tests should be synthetic and should avoid real personal data.

Recommended structure:

- add a synthetic input case;
- define expected token behavior;
- include both positive and negative cases where possible;
- run the regression tool before changing core detection logic.

## Notes

Sprint 0.6 fixed the former INN spacing and OCR-letter substitution synthetic gaps.

The current baseline does not mean the tool has no real-world limitations. Manual review remains required before external sharing.
