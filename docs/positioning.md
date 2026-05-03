# Positioning

## What this project is

BeforeSending is a local-first document pseudonymization / reversible masking / risk-reduction tool.

It focuses on preparing Russian-language legal, tax and business documents before external AI/SaaS use.

## What this project is not

It is not:

- a guaranteed anonymization tool;
- a compliance solution;
- an enterprise DLP system;
- an OCR engine;
- a substitute for human review.

## Why document-first workflow matters

Many privacy tools focus on API requests, browser extensions or generic PII detection.

BeforeSending focuses on the document workflow:

```text
DOCX / text-layer PDF
→ local processing
→ reversible tokens
→ report
→ human review
→ external processing
→ optional restoration
```

## Similar tools and adjacent categories

Adjacent categories include:

- generic PII detection SDKs;
- enterprise DLP / CASB tools;
- browser privacy extensions;
- LLM privacy proxies;
- redaction APIs;
- local OCR / document tools.

## How this differs from generic PII detection SDKs

This project is not a general-purpose PII SDK.

It focuses on a narrower workflow:

```text
Russian-language legal/business documents,
local processing,
reversible token mapping,
human review,
synthetic regression testing.
```

## Scope of v0.1-alpha

Supported:

- DOCX;
- text-layer PDFs;
- reversible token dictionary;
- synthetic regression tests;
- replacement reports;
- human review tooling.

Not supported:

- OCR;
- scanned PDFs;
- images;
- secure PDF redaction;
- encrypted vault;
- enterprise workflow.

## Known limitations

See:

```text
docs/limitations.md
```

## No real personal data in issues

Use synthetic examples only.
