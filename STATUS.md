# Status

Date: 2026-06-02
Project: BeforeSending / local-doc-pseudonymizer
Status: `v0.2-alpha candidate` with Sprint 1.9 Windows quickstart packaging, local cleanup helper, and release hygiene. Not a production security or compliance product.

## Current verified baseline

```text
Synthetic regression: PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
Pytest smoke/document/report/quality/release-hygiene tests: 17 passed
Quality metrics dashboard: generated from strict synthetic regression results
```

Validated with:

```bash
python -m py_compile pseudonymize.py html_review_report.py quality_metrics.py run_regression_tests.py
python run_regression_tests.py run-strict
python run_regression_tests.py quality-metrics
python -m pytest -q
python tools/check_release_hygiene.py
git diff --check
```

On Windows, use the repository virtual environment if available:

```powershell
.\.venv\Scripts\python.exe -m py_compile pseudonymize.py html_review_report.py quality_metrics.py run_regression_tests.py
.\.venv\Scripts\python.exe run_regression_tests.py run-strict
.\.venv\Scripts\python.exe run_regression_tests.py quality-metrics
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools\check_release_hygiene.py
git diff --check
```

## Completed checkpoints

- Sprint 0.8 - PDF safe handling.
- Sprint 0.9 - DOCX table-aware context.
- Sprint 1.0 - document-level regression tests.
- Sprint 1.1 - Russian recognition quality pack v1.
- Sprint 1.2 - minimal label-driven English profile.
- Sprint 1.3 - Russian recognition quality pack v2.
- Sprint 1.4 - golden synthetic demo and release-ready walkthrough.
- Sprint 1.5 - local self-contained HTML review report for human-in-the-loop review.
- Sprint 1.6 - quality metrics dashboard for synthetic regression categories.
- Sprint 1.7 - Russian-first HTML review report UX for local human review.
- Sprint 1.8 - encrypted vault boundary design spike for future token dictionary protection.
- Sprint 1.9 - Windows quickstart packaging, folder-based batch scripts, and release hygiene checker.
- Release/docs hygiene checkpoint - README, STATUS, ROADMAP, limitations, supported entities, issue safety, token dictionary warnings and release checklist aligned.

## Current scope

Supported:

- DOCX documents.
- PDFs with an extractable text layer.
- Local reversible token dictionary.
- JSON, DOCX, Markdown, and Russian-first self-contained HTML review reports.
- Synthetic quality metrics JSON and Russian Markdown reports under ignored `output/reports/`.
- Human review workflow.
- Synthetic text-block regression tests.
- Generated document-level regression fixtures.
- Golden synthetic end-to-end demo fixture and walkthrough.
- Basic DOCX table row/column label context.
- Minimal label-driven English profile for common personal-data fields.
- Expanded label-driven Russian recognition coverage for legal/business synthetic cases.
- Windows-first folder workflow through `scripts/setup_windows.bat`, `scripts/prepare_documents_windows.bat`, `scripts/restore_documents_windows.bat`, and `scripts/run_demo_windows.bat`.
- Local cleanup helper through `scripts/cleanup_local_windows.bat` for generated environment/runtime folders inside one project copy.
- Release hygiene checker for tracked trees and extracted release artifacts.

Not supported:

- OCR.
- Scanned PDFs.
- Photos or embedded images.
- Secure PDF redaction.
- Encrypted local vault.
- GUI review app.
- Desktop app / app-like launcher.
- Production installer or system-wide Windows installation.
- Full system uninstaller.
- Enterprise DLP features.
- Legal or regulatory compliance guarantees.

## Safety posture

Do not store real personal data in this repository.

HTML review reports generated from real documents are sensitive local artifacts because they can include original values, tokens, review context, warnings, cleanup paths, and technical review notes. Do not upload, publish, commit, or share generated reports unless they are verified synthetic and intended for release.

Quality metrics reports are intended only for synthetic regression results. They provide engineering visibility by category, not a compliance score, anonymization guarantee, or proof that false negatives are impossible.

Sprint 1.8 adds documentation for a future password-based encrypted vault boundary. It is design-only: the current MVP still writes plaintext token dictionaries, and there is no cryptographic protection, secure deletion, persistent vault session, daemon, or "remember password" feature.

Sprint 1.9 adds Windows quickstart scripts, a local cleanup helper, and a release hygiene checker. It is a local project-folder workflow, not a desktop app, production installer, system-wide install, or full uninstaller. It does not change recognizer behavior, add encryption, add OCR, or make release artifacts safe by itself; public artifacts should still be created from a clean tracked state.

After Sprint 1.9, the next product-direction decision is pending and should be made in a separate strategy session: app-like launcher design spike vs local desktop launcher MVP. Neither direction is chosen yet.

For future false negatives or false positives:

1. Collect only the structure of the miss.
2. Rewrite the case into synthetic data.
3. Add the synthetic case as a regression test.
4. Change detection rules narrowly.
5. Run the full verification commands above.

## Next candidates

Choose one track at a time:

1. v0.2-alpha release note / tag preparation after one more clean verification pass.
2. Manual Windows smoke test from a fresh folder or extracted `git archive` ZIP.
3. Separate strategy session for app-like launcher design spike vs local desktop launcher MVP.
4. Future encrypted vault implementation planning, only after design review, crypto library selection, and synthetic-only test design.
5. PDF table extraction experiment for simple text-layer tables.
