---
name: False negative
about: Sensitive data was not masked
title: "[False negative]: "
labels: false-negative
assignees: ""
---

> Safety: Do not include real personal data, confidential documents, real IDs, INNs, passports, addresses, contracts, screenshots with PII, token dictionaries, `project_dictionary.json`, `dictionary.json`, token maps, raw text, or real generated reports. Use synthetic examples only.

## Entity type

Example: PERSON / INN / PASSPORT / ADDRESS_DETAIL / ACCOUNT / PHONE

## Minimal synthetic reproduction

Provide the smallest synthetic input that reproduces the missed masking. Do not paste the original document, raw extracted text, token dictionaries, token maps, screenshots with PII, or real generated reports.

```text
INN: 123 456 789 012
```

## Expected output

```text
INN: [INN_1]
```

## Actual output

```text
INN: 123 456 789 012
```

## Why this should be masked

Explain briefly using synthetic context only.
