# Positioning

BeforeSending is a local-first document pseudonymization / reversible masking / risk-reduction tool.

It focuses on preparing Russian-language legal, tax and business documents before sharing them with external services, contractors, or other third parties.

## What this project is

- A local-first document pseudonymization tool.
- A risk-reduction utility for preparing documents before external sharing.
- A reversible token-based masking workflow using a local dictionary.
- A human-review-oriented workflow with replacement reports.
- A tool focused on Russian legal, tax and business documents.
- A synthetic-regression-driven improvement loop.

## What this project is not

It is not:

- a guarantee that documents are automatically safe;
- legal advice or a compliance tool;
- a DLP system or enterprise security platform;
- an OCR engine;
- a tool for scanned PDFs or images in v0.1/v0.2 candidate;
- a substitute for human review;
- a promise that no personal or confidential data remains in the output.

## Similar tools and adjacent categories

Adjacent categories include:

- generic PII detection SDKs;
- enterprise data-control tools;
- browser privacy extensions;
- external-service privacy proxies;
- redaction APIs;
- OCR / document intelligence tools.

BeforeSending is narrower: it is a document-first workflow for local DOCX/text-layer PDF preparation with reversible token mapping, replacement reports, human review and synthetic regression tests.

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

This is useful when the practical risk appears before a document is sent to an external service, contractor, client intake process or other external processing path.

## Scope of v0.1-alpha / v0.2-alpha candidate

Supported:

- DOCX;
- text-layer PDFs;
- reversible token dictionary;
- synthetic regression tests;
- document-level regression tests;
- replacement reports;
- human review tooling;
- basic DOCX table context;
- minimal label-driven English profile.

Not supported:

- OCR;
- scanned PDFs;
- images;
- secure PDF redaction;
- protected dictionary storage beyond plaintext local files;
- enterprise workflow;
- legal or regulatory assurance.

## Known limitations

See:

```text
docs/limitations.md
```

## Responsible reporting of missed detections

Missed detections should be reported only as synthetic examples.

A safe report preserves the structure of the problem but replaces every real value with fictional data.

Do not include real personal data, confidential documents, real INNs, passport numbers, addresses, contracts, screenshots, token dictionaries or review reports.

## No real personal data in issues

Use synthetic examples only.

Issues, pull requests or discussions containing real personal or confidential data may be removed or edited to protect privacy.
