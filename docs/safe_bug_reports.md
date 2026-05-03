# Safe Bug Reports

## Do not include real personal data

Do not include real personal data, confidential documents, real INNs, passport numbers, addresses, contracts, screenshots or token dictionaries.

Use synthetic examples only.

## How to report a false negative

A false negative means sensitive data was not masked.

Use this format:

```text
Input:
ИНН: 781 234 567 890

Expected:
ИНН: [INN_1]

Actual:
ИНН: 781 234 567 890
```

## How to report a false positive

A false positive means safe data was masked incorrectly.

Use this format:

```text
Input:
АКТ № 4012345678 от 10.01.2026

Expected:
АКТ № 4012345678 от 10.01.2026

Actual:
АКТ № [PASSPORT_1] от 10.01.2026
```

## Bad examples

Do not submit:

- real contract fragments;
- real passport data;
- real addresses;
- real bank accounts;
- screenshots with personal data;
- `project_dictionary.json`;
- reports with original values.

## Good examples

Use fictional but structurally similar values:

```text
Иванов Иван Иванович
770000000000
г. Примерск, ул. Тестовая, д. 1
АКТ № 4012345678
УИД 12345678901234567890
```

## What may be removed or edited

Issues, pull requests or discussions containing real personal or confidential data may be removed or edited to protect privacy.
