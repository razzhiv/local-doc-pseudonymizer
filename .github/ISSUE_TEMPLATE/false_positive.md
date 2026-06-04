---
name: False positive
about: Safe data was masked incorrectly
title: "[False positive]: "
labels: false-positive
assignees: ""
---

> Safety: Do not include real personal data, confidential documents, real IDs, INNs, passports, addresses, contracts, screenshots with PII, token dictionaries, `project_dictionary.json`, `dictionary.json`, token maps, raw text, or real generated reports. Use synthetic examples only.

## Entity type detected

Example: PASSPORT / ACCOUNT / PHONE / CARD

## Minimal synthetic reproduction

Provide the smallest synthetic input that reproduces the over-masking. Do not paste the original document, raw extracted text, token dictionaries, token maps, screenshots with PII, or real generated reports.

```text
Act number 4012345678 dated 10.01.2026
```

## Expected output

```text
Act number 4012345678 dated 10.01.2026
```

## Actual output

```text
Act number [PASSPORT_1] dated 10.01.2026
```

## Why this should not be masked

Explain briefly using synthetic context only.
