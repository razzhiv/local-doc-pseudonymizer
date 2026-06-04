# Release / Public Repository Checklist

Use this checklist before publishing or tagging a public release.

## Verification

Run:

```bash
python -m py_compile pseudonymize.py html_review_report.py quality_metrics.py run_regression_tests.py
python run_regression_tests.py run-strict
python run_regression_tests.py quality-metrics
python -m pytest -q
python tools/check_release_hygiene.py
python tools/check_public_terms.py
git diff --check
```

Expected current baseline:

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
20 passed
```

On Windows with the repository virtual environment:

```bat
.\.venv\Scripts\python.exe -m py_compile pseudonymize.py html_review_report.py quality_metrics.py run_regression_tests.py
.\.venv\Scripts\python.exe run_regression_tests.py run-strict
.\.venv\Scripts\python.exe run_regression_tests.py quality-metrics
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools\check_release_hygiene.py
.\.venv\Scripts\python.exe tools\check_public_terms.py
git diff --check
```

Create public/release artifacts from a clean tracked state, preferably with `git archive` or an equivalent tracked-file export. Do not manually ZIP the working directory.

For a full artifact guide, see `docs/release_artifacts.md`.

Confirm Sprint 1.9 wording describes a Windows quickstart / local setup script / release-folder workflow. It must not imply a desktop app, GUI app, production installer, system-wide installation, Add/Remove Programs entry, or full uninstaller.

## Sensitive-file check

Confirm that the public tree does not include:

- real input documents;
- real output documents;
- real files under `input/`, `output/`, `review/`, `to_decode/`, `restored/`, or `feedback/`;
- real PDF/DOCX/XLSX/CSV/TSV files;
- `project_dictionary.json`;
- `dictionary.json`;
- token maps;
- raw or extracted text artifacts;
- real review reports;
- logs or generated artifacts likely to contain real personal data;
- generated quality metrics reports not verified as synthetic-only;
- `feedback/cases.jsonl` generated from real documents;
- screenshots containing personal or confidential data;
- ZIP/RAR/7Z archives with working materials;
- downloaded model archives, embeddings or dictionary caches;
- private manual rule files.

## Public wording check

Run `python tools/check_public_terms.py` from the repository root. The check scans git-tracked public text files for forbidden private/product terms, public roadmap promises, and over-strong security claims.

Confirm that public docs, issue templates, PR templates, release notes, and examples do not include private terms or product roadmap promises. They should not claim GUI/app/launcher/integration/vault commitments, compliance, DLP, zero-leakage, or guaranteed anonymization.

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

- that automated masking removes all sensitive data;
- legal or regulatory assurance;
- enterprise security governance;
- a safety score;
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
