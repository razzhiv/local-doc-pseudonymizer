# Synthetic Regression

The public repository uses synthetic regression cases only.

No real personal data should be included in public tests.

## Current baseline

```text
PASS 27 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 29
```

## Run tests

```bash
python run_regression_tests.py
```

or on Windows:

```bat
run_regression_tests.bat
```

## XFAIL

Known gaps are represented as `XFAIL` so that desired future behavior is tracked without blocking the current MVP.

Current XFAIL:

- INN with spaces;
- INN with OCR-letter substitution.

## Adding tests

New tests should be synthetic and should avoid real personal data.

Each improvement should include:

- a positive case;
- a negative case;
- regression confirmation.
