# Documentation

This folder contains public documentation for the BeforeSending / local-doc-pseudonymizer MVP.

Start here:

- `positioning.md` - what the project is and is not.
- `windows_quickstart.md` - practical Windows quickstart, local project-folder workflow, synthetic demo, restore flow, and cleanup helper.
- `limitations.md` - detection, DOCX, PDF and compliance limitations.
- `supported_entities.md` - experimental entity coverage.
- `token_dictionary_security.md` - why the token dictionary is sensitive.
- `vault_design.md` - Sprint 1.8 docs-only design for a future encrypted vault boundary.
- `safe_bug_reports.md` - how to report issues without leaking real data.
- `review_workflow.md` - controlled human-review and regression loop.
- `demo_walkthrough.md` - golden synthetic end-to-end demo, including the Russian-first local HTML review report.
- `synthetic_regression.md` - regression test workflow and Sprint 1.6 synthetic quality metrics dashboard.
- `synthetic_regression_report_latest.md` - latest generated synthetic regression report.
- `release_checklist.md` - public-repo hygiene checklist.
- `release_artifacts.md` - clean release ZIP/artifact guidance and hygiene checker.
- `licensing.md` - practical licensing notes.

Local HTML review reports are generated under ignored `output/reports/review_report_*.html` during the demo/workflow. They are Russian-first, self-contained, and intended for local browser review only. Synthetic quality metrics reports are generated under ignored `output/reports/quality_metrics_*`. Treat any report as a sensitive local artifact when it is based on real documents; quality metrics should be generated only from the synthetic regression corpus.

The current MVP uses plaintext token dictionaries. The Sprint 1.8 vault design documents a possible future password-based encrypted vault, but no encrypted vault mode exists yet.

Do not add real personal data, real documents, token dictionaries, production review reports or screenshots containing confidential information to this repository.
