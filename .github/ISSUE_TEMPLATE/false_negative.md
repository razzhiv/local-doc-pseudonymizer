---
name: False negative
about: Sensitive data was not masked
title: "[False negative]: "
labels: false-negative
assignees: ""
---

> ⚠️ Do not include real personal data, confidential documents, real INNs, passport numbers, addresses, contracts, screenshots or token dictionaries. Use synthetic examples only.

> ⚠️ Не прикладывайте реальные персональные данные, реальные документы, ИНН, паспортные данные, адреса, договоры, скриншоты или словари токенов. Используйте только синтетические примеры.


## Entity type

Example: PERSON / INN / PASSPORT / ADDRESS_DETAIL / ACCOUNT / PHONE

## Synthetic input

```text
ИНН: 781 234 567 890
```

## Expected output

```text
ИНН: [INN_1]
```

## Actual output

```text
ИНН: 781 234 567 890
```

## Why this should be masked

Explain briefly using synthetic context only.
