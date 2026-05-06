# Roadmap

## v0.1.1-alpha public baseline alignment

Status: current cleanup branch after Sprint 0.6.

Goals:

- keep the public repository GitHub-safe;
- make GitHub Actions run the actual strict synthetic regression command;
- align public documentation with the Sprint 0.6 regression baseline;
- keep the regression baseline green;
- avoid new core behavior changes in this cleanup sprint.

Non-goals:

- no OCR;
- no GUI;
- no encrypted vault;
- no compliance claims;
- no real-data corpus;
- no new detection rules.

## Current status

BeforeSending is an experimental local-first MVP focused on DOCX and text-layer PDF documents.

Current regression baseline:

```text
PASS 34 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 34
Blocking errors: 0
```

Current public synthetic XFAIL cases: none.

Closed in Sprint 0.6:

- INN with spaces;
- INN with OCR-letter substitution.

## v0.1-alpha

Focus:

- local DOCX / text-layer PDF processing;
- reversible token dictionary;
- synthetic regression corpus;
- human-in-the-loop review workflow;
- safe GitHub documentation;
- no real data in public repository.

## Sprint 0.6 completed

INN normalization and OCR-suspect handling:

- spaced/hyphenated INN values near an explicit `ИНН` label are masked as `INN`;
- OCR-like INN values near an explicit `ИНН` label are masked as `OCR_SUSPECT_INN`;
- service-number contexts remain protected by negative regression tests.

## Later

Possible future work:

- DOCX/PDF end-to-end synthetic tests;
- desktop GUI;
- encrypted local vault;
- visual review;
- OCR and scanned document handling;
- safer PDF redaction;
- policy profiles;
- Obsidian / local knowledge workflow integrations;
- team workflow and audit trail;
- B2B / on-prem deployment.
