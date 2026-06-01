# Roadmap

BeforeSending is an experimental local-first document pseudonymization / reversible masking / risk-reduction MVP.

It is focused on preparing DOCX and text-layer PDF documents before external AI/SaaS use, contractor sharing or other third-party processing.

## Current checkpoint — v0.2-alpha candidate

Status: release/docs hygiene checkpoint after Sprint 1.6.

Current verified baseline:

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
Pytest: 13 passed
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

## v0.2-alpha candidate goals

A `v0.2-alpha` tag should be considered only after:

- a clean final verification pass;
- a GitHub Actions run on the target public repository;
- review that the public tree contains no real documents, dictionaries, reports, archives or generated private working files;
- confirmation that dependency licenses have been reviewed for the versions actually used;
- a release note that clearly says experimental MVP / not compliance / not DLP / manual review required.

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

### Track C — product/release packaging

Possible focus:

- clean `v0.2-alpha` release note;
- public example walkthrough using synthetic data only;
- installer/CLI polish;
- screenshots generated only from synthetic examples;
- dependency pinning / license review.

## Later / out of current scope

Possible future work:

- desktop GUI;
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
