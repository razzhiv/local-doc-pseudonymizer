# Release / Public Repository Checklist

Use this checklist before publishing or tagging a public release.

## Verification

Run:

```bash
python -m py_compile pseudonymize.py html_review_report.py quality_metrics.py run_regression_tests.py
python run_regression_tests.py run-strict
python run_regression_tests.py quality-metrics
python -m pytest -q
```

Expected current baseline:

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
13 passed
```

## Sensitive-file check

Confirm that the public tree does not include:

- real input documents;
- real output documents;
- real PDF/DOCX/XLSX/CSV/TSV files;
- `project_dictionary.json`;
- `dictionary.json`;
- real review reports;
- generated quality metrics reports not verified as synthetic-only;
- `feedback/cases.jsonl` generated from real documents;
- screenshots containing personal or confidential data;
- ZIP/RAR/7Z archives with working materials;
- downloaded model archives, embeddings or dictionary caches;
- private manual rule files.

## Documentation check

Confirm that these files are present and aligned:

- `README.md`;
- `STATUS.md`;
- `CHANGELOG.md`;
- `ROADMAP.md`;
- `SECURITY.md`;
- `CONTRIBUTING.md`;
- `DISCLAIMER.md`;
- `docs/positioning.md`;
- `docs/limitations.md`;
- `docs/supported_entities.md`;
- `docs/token_dictionary_security.md`;
- `docs/safe_bug_reports.md`;
- `.github/ISSUE_TEMPLATE/*`;
- `.github/workflows/tests.yml`.

## Positioning check

Use:

- pseudonymization;
- reversible masking;
- risk reduction;
- document preparation;
- local-first;
- human review;
- synthetic regression tests.
- synthetic quality metrics for engineering visibility only.

Do not claim:

- guaranteed anonymization;
- zero leakage;
- legal compliance;
- 152-FZ/GDPR/HIPAA compliance;
- enterprise DLP;
- compliance score;
- OCR support for v0.1/v0.2 candidate.

## Release note check

A release note should say clearly:

- experimental MVP / alpha;
- local-first document preparation tool;
- DOCX and text-layer PDF only;
- OCR and scanned PDFs are not supported;
- token dictionary is sensitive;
- manual review is required;
- synthetic baseline, quality metrics generation, and pytest suite passed.
