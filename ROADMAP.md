# Roadmap

## Current status

BeforeSending is an experimental local-first MVP focused on DOCX and text-layer PDF documents.

Current regression baseline:

```text
PASS 27 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 29
```

Remaining known gaps:

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

## Mini-sprint 0.6 candidate

INN normalization and OCR-suspect handling:

- INN with spaces;
- INN with OCR-letter substitution;
- positive and negative regression tests before active core changes.

## Later

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
