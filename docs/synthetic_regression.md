# Synthetic regression tests

This project uses a synthetic regression corpus to verify masking behavior without using real personal or confidential data.

No real personal data should be included in public tests.

## Current baseline

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
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

## Quality metrics dashboard

Sprint 1.6 adds a synthetic-only quality metrics dashboard over strict regression results:

```bash
python run_regression_tests.py quality-metrics
```

This command runs the strict text-block regression suite and then writes ignored runtime reports:

- `output/reports/quality_metrics_<timestamp>.json`
- `output/reports/quality_metrics_latest.json`
- `output/reports/quality_metrics_<timestamp>.md`
- `output/reports/quality_metrics_latest.md`

The JSON is machine-readable and keeps English field names plus stable English category IDs. Russian display names are included as optional values. The Markdown report is Russian-first and shows a category matrix with totals, passed cases, failures, positive/negative case counts, and success rate.

Initial category IDs include `passport`, `inn`, `snils`, `ogrn`, `ogrnip`, `kpp`, `bank_details`, `phone`, `address`, `birth_or_sensitive_dates`, `general_dates_negative`, `persons`, `private_orgs`, `public_authorities_negative`, `contract_numbers_negative`, `case_numbers_negative`, `english_minimal`, `docx_tables_or_structure`, and `pdf_text_layer`.

The dashboard is for engineering visibility only. It is not a safety score, not proof that all sensitive data has been removed, and not proof that false negatives are impossible. It must be generated only from synthetic tests and must not include real documents, real personal data, token dictionaries, or runtime artifacts from real data.

## XFAIL / known gaps

Known gaps can be represented as `XFAIL` so that desired behavior is tracked without blocking the current MVP.

Current public synthetic XFAIL cases: none.

Former XFAIL cases fixed in Sprint 0.6:

- INN with spaces;
- INN with OCR-letter substitution.

Sprint 1.1 adds the first recognition quality pack for common synthetic false negatives: spaced SNILS, separated passport series/number, spaced BIK/KPP/OGRN, quoted private organizations, address index context, one-digit sensitive dates, and mobile phone context.

Sprint 1.2 adds a minimal English profile for explicit English labels such as Full name, Passport No., Tax ID / TIN, Date of birth, Phone, Registered address, and LLC/Ltd-style private organization prefixes.

Sprint 1.3 adds a second Russian recognition quality pack for synthetic legal/business cases: address details, passport phrasing, mixed requisites, table-like labels, private organizations/IP, and negative service-number guards.

## Adding tests

New tests should be synthetic and should avoid real personal data.

Recommended structure for text-block detection rules:

- add a synthetic input case;
- define expected token behavior;
- include `category_ids` when a new case does not fit the existing quality metrics category derivation;
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
