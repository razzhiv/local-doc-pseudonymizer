# Roadmap

BeforeSending is an experimental local-first document pseudonymization / reversible masking / risk-reduction MVP.

It is focused on preparing DOCX and text-layer PDF documents before external AI/SaaS use, contractor sharing or other third-party processing.

## Current checkpoint - v0.2-alpha candidate / Sprint 1.9 Windows quickstart packaging

Status: Sprint 1.9 Windows quickstart, local project-folder workflow, setup/demo/prepare/restore/cleanup batch scripts, and release hygiene checker.

Current verified baseline:

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
Pytest: 17 passed
```

What is now aligned:

- README positioning and warnings.
- CHANGELOG / STATUS / ROADMAP.
- `docs/limitations.md`.
- `docs/supported_entities.md`.
- `.gitignore` sensitive-file hygiene.
- token dictionary security notes.
- safe issue-reporting templates.
- latest synthetic regression report.
- synthetic quality metrics dashboard by category.
- Sprint 1.8 vault boundary design for a future password-based encrypted token dictionary vault.
- Sprint 1.9 Windows quickstart scripts and clean release artifact hygiene.
- Sprint 1.9 local cleanup helper for generated environment/runtime folders.

## v0.1-alpha — released MVP baseline

Focus:

- local DOCX / text-layer PDF processing;
- reversible token dictionary;
- replacement reports;
- human-in-the-loop review workflow;
- synthetic regression corpus;
- safe GitHub documentation;
- no real data in the public repository.

## Completed controlled sprints

### Sprint 0.8 — PDF safe handling

PDFs without an extractable text layer no longer silently produce an empty anonymized DOCX.

### Sprint 0.9 — DOCX table-aware context

DOCX table cells are processed with row/column label context.

### Sprint 1.0 — document-level regression tests

Added generated DOCX/PDF pytest coverage for document workflows.

### Sprint 1.1 — Russian recognition quality pack v1

Expanded the synthetic baseline from 34 to 44 cases.

### Sprint 1.2 — minimal English profile

Added a minimal label-driven English profile and expanded the synthetic baseline from 44 to 52 cases.

### Sprint 1.3 - Russian recognition quality pack v2

Expanded label-driven Russian legal/business coverage and negative guards; baseline reached 70 cases.

### Sprint 1.4 - golden synthetic demo

Added a safe end-to-end demo fixture and walkthrough.

### Sprint 1.5 - local HTML review report

Added a self-contained local HTML review report for human-in-the-loop review.

### Sprint 1.6 - quality metrics dashboard

Added synthetic-only JSON and Russian Markdown quality metrics by explicit regression categories.

### Sprint 1.7 - Russian-first HTML review report UX

Localized the self-contained local HTML review report for Russian-first human review while preserving stable technical category codes.

### Sprint 1.8 - encrypted vault boundary design spike

Documented the sensitive boundary for plaintext token dictionaries, reports, raw extracted text, runtime artifacts, public issue safety, and a possible future password-based encrypted vault.

This sprint is documentation only. It does not implement encryption or change recognizer behavior.

### Sprint 1.9 - Windows quickstart packaging

Added a Windows-first folder workflow:

- `scripts/setup_windows.bat`;
- `scripts/prepare_documents_windows.bat`;
- `scripts/restore_documents_windows.bat`;
- `scripts/run_demo_windows.bat`;
- `scripts/cleanup_local_windows.bat`.

Added `tools/check_release_hygiene.py` and release artifact documentation so public ZIPs are created from clean tracked files instead of manually zipping the working directory.

This sprint delivers Windows quickstart and a release-folder workflow, not a desktop app, production installer, system-wide installation, or full uninstaller. The cleanup helper removes generated local folders inside one project copy and is not secure deletion.

This sprint does not change recognizer behavior, add OCR, add encryption, implement a GUI, or introduce compliance/DLP claims.

## v0.2-alpha candidate goals

A `v0.2-alpha` tag should be considered only after:

- a clean final verification pass;
- a GitHub Actions run on the target public repository;
- review that the public tree contains no real documents, dictionaries, reports, archives or generated private working files;
- a manual Windows smoke test from a fresh folder or extracted release ZIP;
- confirmation that quickstart/cleanup wording does not imply a desktop app or production installer;
- confirmation that dependency licenses have been reviewed for the versions actually used;
- a release note that clearly says experimental MVP / not compliance / not DLP / manual review required.

## Product direction decision pending

After Sprint 1.9, the next product-direction decision should be made in a separate strategy session:

- app-like launcher design spike;
- local desktop launcher MVP.

Neither direction is chosen yet, and Sprint 2.0 is not decided here. Sprint 1.9 delivered Windows quickstart and release-folder workflow, not an app.

## Next technical tracks

Choose one track at a time.

### Track A - Russian recognition quality pack v3

Possible focus:

- more address variants;
- more passport phrasing;
- table labels with abbreviations;
- mixed реквизиты blocks;
- legal entity details;
- court/procedural number false positives and false negatives;
- additional negative tests to prevent over-masking.

### Track B — PDF table extraction experiment

Possible focus:

- `pdfplumber.extract_tables()`;
- simple text-layer PDF tables only;
- conversion of simple tables into DOCX tables;
- duplicate-extraction guards;
- explicit limitations;
- no OCR.

### Track C - product-release finalization

Possible focus:

- clean `v0.2-alpha` release note;
- public example walkthrough using synthetic data only;
- manual Windows smoke test from a fresh folder;
- local setup-script / CLI polish without app-installer claims;
- screenshots generated only from synthetic examples;
- dependency pinning / license review.

### Track D - future encrypted vault implementation planning

This is a later implementation-planning track after Sprint 1.8 design review, not the immediate next sprint unless separately chosen.

Possible focus:

- accept or revise `docs/vault_design.md`;
- choose a standard crypto library and dependency policy;
- design a narrow vault read/write interface;
- plan synthetic-only vault tests;
- design plaintext dictionary migration;
- update cleanup guidance without promising secure deletion;
- only then consider enabling encrypted vault mode.

## Later / out of current scope

Possible future work:

- desktop GUI or launcher only after a separate product-direction decision;
- encrypted local vault;
- visual review;
- OCR and scanned document handling;
- safer PDF redaction;
- policy profiles;
- Obsidian / local knowledge workflow integrations;
- team workflow and audit trail;
- B2B / on-prem deployment.

## Non-goals for the current MVP

- no compliance guarantee;
- no enterprise DLP claim;
- no guaranteed anonymization claim;
- no real-data corpus;
- no OCR in v0.1/v0.2 candidate;
- no broad masking rules without synthetic regression tests.
