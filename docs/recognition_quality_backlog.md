# Recognition Quality Backlog

Use this file format for collecting future false negatives and false positives safely.

Do not paste real personal data, real documents, screenshots, contracts, addresses, passport numbers, INNs, token dictionaries or confidential fragments.

Convert every real example into a synthetic example before sharing it in issues, chats or commits.

## How to collect a case

```md
### Case title

Type: false_negative / false_positive / formatting_gap
Area: passport / SNILS / address / phone / organization / bank details / date / other
Source: synthetic_rewrite_of_real_pattern / synthetic_manual_case

Synthetic input:
```text
СНИЛС заявителя: 123 456 789 00
```

Expected output:
```text
СНИЛС заявителя: [SNILS_1]
```

What happened now:
```text
СНИЛС заявителя: 123 456 789 00
```

Notes:
- no real personal data;
- structure preserved;
- values are fictional.
```

## Good synthetic examples

```text
Паспорт РФ: серия 1234 № 567890 выдан отделом МВД.
СНИЛС: 123 456 789 00.
Адрес регистрации: 190000, г. Санкт-Петербург, Невский проспект, д. 10, кв. 5.
БИК: 044 525 225.
ООО «Ромашка-Сервис».
```

## Bad examples

Do not include:

- real names;
- real passport data;
- real INNs / SNILS / bank details;
- real addresses;
- real contracts or claims;
- screenshots with personal data;
- token dictionaries;
- outputs created from real documents.

## Workflow

1. Collect a synthetic case.
2. Add it to the regression corpus.
3. Confirm that the case fails or documents the current gap.
4. Change detection rules narrowly.
5. Run strict regression and document-level tests.
6. Commit only synthetic cases and code/docs changes.


## English profile notes

Sprint 1.2 adds only a minimal, label-driven English profile. Future backlog items should prefer synthetic examples with explicit labels and clear expected behavior, for example `Full name: John Smith` or `Tax ID: 473254765214`.

This is not a full multilingual NER layer.
