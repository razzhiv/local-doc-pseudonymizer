---
name: False positive
about: Safe data was masked incorrectly
title: "[False positive]: "
labels: false-positive
assignees: ""
---

> ⚠️ Do not include real personal data, confidential documents, real INNs, passport numbers, addresses, contracts, screenshots or token dictionaries. Use synthetic examples only.

> ⚠️ Не прикладывайте реальные персональные данные, реальные документы, ИНН, паспортные данные, адреса, договоры, скриншоты или словари токенов. Используйте только синтетические примеры.


## Entity type detected

Example: PASSPORT / ACCOUNT / PHONE / CARD

## Synthetic input

```text
АКТ № 4012345678 от 10.01.2026
```

## Expected output

```text
АКТ № 4012345678 от 10.01.2026
```

## Actual output

```text
АКТ № [PASSPORT_1] от 10.01.2026
```

## Why this should not be masked

Explain briefly using synthetic context only.
