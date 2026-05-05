# Regression report

Дата: 2026-05-04T00:08:07
Всего тестов: 34
PASS: 34
FAIL: 0
XFAIL / known gaps: 0
XPASS / unexpectedly fixed: 0
ERROR: 0
Блокирующих ошибок: 0

## PASS — test_valid_inn_12_001

Валидный 12-значный ИНН рядом с меткой ИНН должен скрываться как INN.

**Input:**

```text
ИНН: 473254765214
```

**Output:**

```text
ИНН: [INN_1]
```

**Actual replacements:**

- INN: `473254765214` → `[INN_1]` (regex_inn_context)

## PASS — test_ocr_suspect_inn_13_001

13 цифр рядом с меткой ИНН не должны считаться валидным ИНН, но должны скрываться как OCR_SUSPECT_INN.

**Input:**

```text
ИНН: 4732547652143
```

**Output:**

```text
ИНН: [OCR_SUSPECT_INN_1]
```

**Actual replacements:**

- OCR_SUSPECT_INN: `4732547652143` → `[OCR_SUSPECT_INN_1]` (regex_inn_ocr_suspect)

## PASS — test_act_13_digits_negative_001

13 цифр после 'АКТ №' — служебный номер, не ИНН, не телефон и не карта.

**Input:**

```text
АКТ № 4732547652143
```

**Output:**

```text
АКТ № 4732547652143
```

## PASS — test_certificate_13_digits_negative_001

13 цифр после 'Сертификат:' — служебный номер, не ИНН, не телефон и не карта.

**Input:**

```text
Сертификат: 4732547652143
```

**Output:**

```text
Сертификат: 4732547652143
```

## PASS — test_phone_ru_positive_001

Обычный российский телефон должен скрываться как PHONE.

**Input:**

```text
Телефон: +7 921 123-45-67
```

**Output:**

```text
Телефон: [PHONE_1]
```

**Actual replacements:**

- PHONE: `+7 921 123-45-67` → `[PHONE_1]` (regex_phone_federal)

## PASS — test_valid_inn_10_001

10-значный ИНН рядом с меткой ИНН должен скрываться как INN.

**Input:**

```text
ИНН: 4723456789
```

**Output:**

```text
ИНН: [INN_1]
```

**Actual replacements:**

- INN: `4723456789` → `[INN_1]` (regex_inn_context)

## PASS — test_ogrn_13_positive_001

ОГРН 13 цифр рядом с меткой ОГРН должен скрываться как OGRN.

**Input:**

```text
ОГРН: 1027700132195
```

**Output:**

```text
ОГРН: [OGRN_1]
```

**Actual replacements:**

- OGRN: `1027700132195` → `[OGRN_1]` (regex_ogrn_context)

## PASS — test_ogrnip_15_positive_001

ОГРНИП 15 цифр рядом с меткой ОГРНИП должен скрываться как OGRNIP.

**Input:**

```text
ОГРНИП: 304500116000157
```

**Output:**

```text
ОГРНИП: [OGRNIP_1]
```

**Actual replacements:**

- OGRNIP: `304500116000157` → `[OGRNIP_1]` (regex_ogrnip_context)

## PASS — test_bik_9_positive_001

БИК 9 цифр рядом с меткой БИК должен скрываться как BIK.

**Input:**

```text
БИК: 044525225
```

**Output:**

```text
БИК: [BIK_1]
```

**Actual replacements:**

- BIK: `044525225` → `[BIK_1]` (regex_bik_context)

## PASS — test_account_20_positive_001

20-значная последовательность должна скрываться как ACCOUNT.

**Input:**

```text
Расчетный счет: 40702810900000000001
```

**Output:**

```text
Расчетный счет: [ACCOUNT_1]
```

**Actual replacements:**

- ACCOUNT: `40702810900000000001` → `[ACCOUNT_1]` (regex_20_digits)

## PASS — test_corr_account_20_positive_001

20-значный корреспондентский счет должен скрываться как ACCOUNT.

**Input:**

```text
Корреспондентский счет: 30101810400000000225
```

**Output:**

```text
Корреспондентский счет: [ACCOUNT_1]
```

**Actual replacements:**

- ACCOUNT: `30101810400000000225` → `[ACCOUNT_1]` (regex_20_digits)

## PASS — test_passport_plain_positive_001

Паспортная серия и номер в формате 1234 567890 должны скрываться как PASSPORT.

**Input:**

```text
Паспорт 1234 567890
```

**Output:**

```text
Паспорт [PASSPORT_1]
```

**Actual replacements:**

- PASSPORT: `1234 567890` → `[PASSPORT_1]` (regex_passport)

## PASS — test_appeal_number_13_digits_negative_001

13 цифр после 'Номер обращения' — служебный номер, не ИНН, не телефон и не карта.

**Input:**

```text
Номер обращения 4732547652143
```

**Output:**

```text
Номер обращения 4732547652143
```

## PASS — test_act_phone_like_negative_001

Номер акта, похожий на телефон, не должен скрываться как PHONE.

**Input:**

```text
АКТ № 89123451004
```

**Output:**

```text
АКТ № 89123451004
```

**Actual skipped:**

- PHONE: `89123451004` — service_number_context

## PASS — test_certificate_phone_like_negative_001

Номер сертификата, похожий на телефон, не должен скрываться как PHONE.

**Input:**

```text
Сертификат: 8 912 345 10 04
```

**Output:**

```text
Сертификат: 8 912 345 10 04
```

**Actual skipped:**

- PHONE: `8 912 345 10 04` — service_number_context

## PASS — test_inn_spaced_known_gap_001

Sprint 0.6: ИНН с пробелами рядом с явной меткой ИНН должен скрываться как INN.

**Input:**

```text
ИНН: 473 254 765 214
```

**Output:**

```text
ИНН: [INN_1]
```

**Actual replacements:**

- INN: `473 254 765 214` → `[INN_1]` (regex_inn_context_spaced)

## PASS — test_inn_ocr_letter_known_gap_001

Sprint 0.6: OCR-буква З вместо цифры 3 рядом с меткой ИНН должна попадать в suspect/review, а не в валидный INN.

**Input:**

```text
ИНН: 47325476521З
```

**Output:**

```text
ИНН: [OCR_SUSPECT_INN_1]
```

**Actual replacements:**

- OCR_SUSPECT_INN: `47325476521З` → `[OCR_SUSPECT_INN_1]` (regex_inn_ocr_suspect_char)

## PASS — test_passport_context_positive_001

Паспортная серия и номер рядом с явной меткой 'Паспорт:' должны скрываться как PASSPORT.

**Input:**

```text
Паспорт: 4012 345678 выдан отделом МВД России.
```

**Output:**

```text
Паспорт: [PASSPORT_1] выдан отделом МВД России.
```

**Actual replacements:**

- PASSPORT: `4012 345678` → `[PASSPORT_1]` (regex_passport)

## PASS — test_passport_service_number_negative_001

10 цифр после АКТ № — служебный номер и не должен маскироваться как PASSPORT.

**Input:**

```text
АКТ № 4012345678 от 10.01.2026 подписан сторонами.
```

**Output:**

```text
АКТ № 4012345678 от 10.01.2026 подписан сторонами.
```

**Actual skipped:**

- PASSPORT: `4012345678` — service_number_context

## PASS — test_act_phone_like_11_digits_negative_001

Phone-like номер после 'АКТ №' не должен скрываться как PHONE, CARD или INN.

**Input:**

```text
АКТ № 89211234567 от 10.01.2026 составлен после осмотра.
```

**Output:**

```text
АКТ № 89211234567 от 10.01.2026 составлен после осмотра.
```

**Actual skipped:**

- PHONE: `89211234567` — service_number_context

## PASS — test_certificate_phone_like_plus7_negative_001

Номер сертификата в формате +7 не должен автоматически считаться телефоном в контексте 'Сертификат:'.

**Input:**

```text
Сертификат: +79211234567 зарегистрирован в журнале.
```

**Output:**

```text
Сертификат: +79211234567 зарегистрирован в журнале.
```

**Actual skipped:**

- PHONE: `+79211234567` — service_number_context

## PASS — test_appeal_phone_like_negative_001

Номер обращения, похожий на телефон, не должен скрываться как PHONE, CARD или INN.

**Input:**

```text
Номер обращения 89211234567 зарегистрирован 10 апреля 2026 года.
```

**Output:**

```text
Номер обращения 89211234567 зарегистрирован 10 апреля 2026 года.
```

**Actual skipped:**

- PHONE: `89211234567` — service_number_context

## PASS — test_birth_date_positive_001

Дата рождения должна скрываться текущим типом DATE_BIRTH.

**Input:**

```text
Дата рождения: 01.02.1980.
```

**Output:**

```text
Дата рождения: [DATE_BIRTH_1].
```

**Actual replacements:**

- DATE_BIRTH: `01.02.1980` → `[DATE_BIRTH_1]` (regex_date_birth)

## PASS — test_contract_date_negative_001

Обычная договорная дата не должна скрываться как чувствительная дата.

**Input:**

```text
Договор заключён 21.01.2025 между сторонами.
```

**Output:**

```text
Договор заключён 21.01.2025 между сторонами.
```

## PASS — test_passport_issue_date_positive_001

Дата выдачи паспорта должна скрываться текущим типом DATE_DOC_ISSUE.

**Input:**

```text
Паспорт выдан 10.03.2010 отделом МВД России.
```

**Output:**

```text
Паспорт выдан [DATE_DOC_ISSUE_1] отделом МВД России.
```

**Actual replacements:**

- DATE_DOC_ISSUE: `10.03.2010` → `[DATE_DOC_ISSUE_1]` (regex_date_doc_issue)

## PASS — test_private_org_ooo_positive_001

Частная организация с маркером ООО должна скрываться как ORG_PRIVATE.

**Input:**

```text
Договор заключён с ООО Ромашка на выполнение работ.
```

**Output:**

```text
Договор заключён с ООО [ORG_PRIVATE_1] на выполнение работ.
```

**Actual replacements:**

- ORG_PRIVATE: `Ромашка` → `[ORG_PRIVATE_1]` (natasha_org_private)

## PASS — test_public_org_ifns_negative_001

ИФНС России должна оставаться как публичный орган, а не скрываться как частная организация.

**Input:**

```text
Документ направлен в ИФНС России № 10 по Санкт-Петербургу.
```

**Output:**

```text
Документ направлен в ИФНС России № 10 по Санкт-Петербургу.
```

## PASS — test_account_20_with_context_positive_001

20-значный расчётный счёт с банковским контекстом должен скрываться как ACCOUNT.

**Input:**

```text
Расчетный счет 40702810900000000001 открыт в банке.
```

**Output:**

```text
Расчетный счет [ACCOUNT_1] открыт в банке.
```

**Actual replacements:**

- ACCOUNT: `40702810900000000001` → `[ACCOUNT_1]` (regex_20_digits)

## PASS — test_uid_20_digits_negative_001

20-значный УИД — служебный идентификатор и не должен маскироваться как ACCOUNT.

**Input:**

```text
УИД 12345678901234567890 указан в квитанции.
```

**Output:**

```text
УИД 12345678901234567890 указан в квитанции.
```

**Actual skipped:**

- ACCOUNT: `12345678901234567890` — service_number_context

## PASS — test_act_spaced_inn_like_negative_001

Sprint 0.6 guard: spaced 12-digit service number after АКТ № must not be treated as INN without explicit ИНН label.

**Input:**

```text
АКТ № 473 254 765 214
```

**Output:**

```text
АКТ № 473 254 765 214
```

## PASS — test_certificate_spaced_inn_like_negative_001

Sprint 0.6 guard: spaced 12-digit service number after Сертификат must not be treated as INN without explicit ИНН label.

**Input:**

```text
Сертификат: 473 254 765 214
```

**Output:**

```text
Сертификат: 473 254 765 214
```

## PASS — test_appeal_spaced_inn_like_negative_001

Sprint 0.6 guard: spaced 12-digit appeal number must not be treated as INN without explicit ИНН label.

**Input:**

```text
Номер обращения 473 254 765 214 зарегистрирован.
```

**Output:**

```text
Номер обращения 473 254 765 214 зарегистрирован.
```

## PASS — test_act_ocr_letter_inn_like_negative_001

Sprint 0.6 guard: OCR-like value after АКТ № must not be treated as OCR_SUSPECT_INN without explicit ИНН label.

**Input:**

```text
АКТ № 47325476521З
```

**Output:**

```text
АКТ № 47325476521З
```

## PASS — test_certificate_ocr_letter_inn_like_negative_001

Sprint 0.6 guard: OCR-like value after Сертификат must not be treated as OCR_SUSPECT_INN without explicit ИНН label.

**Input:**

```text
Сертификат: 47325476521З
```

**Output:**

```text
Сертификат: 47325476521З
```
