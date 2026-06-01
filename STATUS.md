# Status

Date: 2026-06-01
Project: BeforeSending / local-doc-pseudonymizer
Status: `v0.2-alpha candidate` documentation and release-hygiene checkpoint. Not a production security or compliance product.

## Current verified baseline

```text
Synthetic regression: PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
Document-level pytest: 5 passed
```

Validated with:

```bash
python -m py_compile pseudonymize.py
python run_regression_tests.py run-strict
python -m pytest -q tests/test_document_level_regression.py
```

On Windows, use the repository virtual environment if available:

```powershell
.\.venv\Scripts\python.exe -m py_compile pseudonymize.py
.\.venv\Scripts\python.exe run_regression_tests.py run-strict
.\.venv\Scripts\python.exe -m pytest -q tests/test_document_level_regression.py
```

## Completed checkpoints

- Sprint 0.8 — PDF safe handling.
- Sprint 0.9 — DOCX table-aware context.
- Sprint 1.0 — document-level regression tests.
- Sprint 1.1 — Russian recognition quality pack v1.
- Sprint 1.2 — minimal label-driven English profile.
- Sprint 1.3 — Russian recognition quality pack v2.
- Release/docs hygiene checkpoint — README, STATUS, ROADMAP, limitations, supported entities, issue safety, token dictionary warnings and release checklist aligned.

## Current scope

Supported:

- DOCX documents.
- PDFs with an extractable text layer.
- Local reversible token dictionary.
- Replacement reports.
- Human review workflow.
- Synthetic text-block regression tests.
- Generated document-level regression fixtures.
- Basic DOCX table row/column label context.
- Minimal label-driven English profile for common personal-data fields.
- Expanded label-driven Russian recognition coverage for legal/business synthetic cases.

Not supported:

- OCR.
- Scanned PDFs.
- Photos or embedded images.
- Secure PDF redaction.
- Encrypted local vault.
- Enterprise DLP features.
- Legal or regulatory compliance guarantees.

## Safety posture

Do not store real personal data in this repository.

For future false negatives or false positives:

1. Collect only the structure of the miss.
2. Rewrite the case into synthetic data.
3. Add the synthetic case as a regression test.
4. Change detection rules narrowly.
5. Run the full verification commands above.

## Next candidates

Choose one track at a time:

1. PDF table extraction experiment for simple text-layer tables.
2. v0.2-alpha release note / tag preparation after one more clean verification pass.
