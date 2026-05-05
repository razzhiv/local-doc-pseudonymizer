# Sprint 0.6 verification — INN normalization and OCR-suspect handling

Date: 2026-05-04
Project: BeforeSending / local-doc-pseudonymizer

## Result

Sprint 0.6 was applied and verified on the attached root project.

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

## Closed known gaps

- `test_inn_spaced_known_gap_001`
- `test_inn_ocr_letter_known_gap_001`

## Implemented behavior

```text
ИНН: 473 254 765 214
→
ИНН: [INN_1]
```

```text
ИНН: 47325476521З
→
ИНН: [OCR_SUSPECT_INN_1]
```

## Guard behavior confirmed

The new logic is bound to explicit `ИНН` context. These service-like values remain unchanged:

```text
АКТ № 473 254 765 214
Сертификат: 473 254 765 214
Номер обращения 473 254 765 214 зарегистрирован.
АКТ № 47325476521З
Сертификат: 47325476521З
```

## Scope notes

- No broad regex expansion for arbitrary long numbers was added.
- No new token taxonomy was added; `OCR_SUSPECT_INN` is reused.
- OCR-like character normalization is intentionally minimal: `З/з → 3`, `О/о → 0`.
- Passport/account guards were not changed.
- No OCR engine, GUI, encrypted vault, or release work was added.
