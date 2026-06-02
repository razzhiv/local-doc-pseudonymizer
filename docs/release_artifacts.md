# Release Artifacts

Public or shared release artifacts should be created from a clean tracked state, not by manually zipping the working directory.

Sprint 1.9 provides a Windows quickstart and release-folder workflow. It is not a desktop app, not a GUI app, not a production installer, and not a system-wide installation.

Use this positioning in release notes:

- local-first document pseudonymization;
- reversible masking;
- risk reduction;
- human review;
- synthetic regression tests;
- sensitive boundary awareness.

Do not claim guaranteed anonymization, 152-FZ/GDPR/HIPAA compliance, DLP coverage, OCR support, zero leakage, or production encrypted-vault protection.

Do not describe release ZIPs or Windows scripts as a production installer, a normal Windows app, an Add/Remove Programs installation, or a full uninstaller.

## Recommended Process

Run verification first:

```bat
.\.venv\Scripts\python.exe -m py_compile pseudonymize.py html_review_report.py quality_metrics.py run_regression_tests.py
.\.venv\Scripts\python.exe run_regression_tests.py run-strict
.\.venv\Scripts\python.exe run_regression_tests.py quality-metrics
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools\check_release_hygiene.py
git diff --check
```

Create release archives from tracked files, for example:

```bat
git archive --format zip --output BeforeSending-release.zip HEAD
```

If you inspect an extracted release folder, run:

```bat
.\.venv\Scripts\python.exe tools\check_release_hygiene.py --root path\to\extracted-release --scan-all
```

## What Must Not Be Included

The release must not include:

- `.git\`;
- `.venv\`;
- `__pycache__\`;
- `.pytest_cache\`;
- real files under `input\`, `output\`, `review\`, `to_decode\`, `restored\`, or `feedback\`;
- `project_dictionary.json`;
- `dictionary.json`;
- token maps;
- raw or extracted text artifacts;
- generated reports based on real data;
- logs or generated artifacts likely to contain real personal data;
- accidental ZIP/RAR/7Z working archives.

The committed placeholder files such as `input\README.md` and `input\.gitkeep` are allowed so users can see the folder workflow.

## Sensitive Local Boundary

Generated dictionaries, reports, raw text, logs, screenshots, and restored documents may contain original personal or confidential values. Do not upload, send, commit, archive, or publish them unless they are verified synthetic and intentionally part of a safe release story.

Masked documents are risk-reduced, not automatically safe. Manual review is still required before sharing.

## Local Cleanup

The release includes `scripts/cleanup_local_windows.bat` as a cleanup helper for generated local folders inside one project copy. It is not a system uninstaller and not secure deletion. Full removal means closing open files/windows and deleting the project folder manually.
