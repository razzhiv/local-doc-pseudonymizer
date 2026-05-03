# CHANGELOG

## 2026-05-01 — Sprint 0.2 / controlled improvement loop

### Added

- Добавлен человекочитаемый human-in-the-loop слой через Excel review table.
- Добавлены файлы feedback loop:
  - `feedback/cases.jsonl`
  - `feedback/decisions.jsonl`
  - `feedback/candidate_rules.jsonl`
  - `expected/regression_cases.jsonl`
- Добавлен regression runner для синтетических тестов.
- Добавлен отдельный тип `OCR_SUSPECT_INN`.

### Changed

- 13-значное значение рядом с меткой `ИНН` больше не считается валидным ИНН.
- Такое значение скрывается как `OCR_SUSPECT_INN` и должно попадать в review.
- Служебные номера вида `АКТ № <DIGITS_13>` и `Сертификат: <DIGITS_13>` не должны маскироваться как ИНН, телефон или карта.

### Verified

Базовый synthetic regression run:

```text
PASS  test_valid_inn_12_001
PASS  test_ocr_suspect_inn_13_001
PASS  test_act_13_digits_negative_001
PASS  test_certificate_13_digits_negative_001
PASS  test_phone_ru_positive_001

Итого: PASS 5 / FAIL 0 / TOTAL 5
```

## 2026-05-01 — Sprint 0.3 / synthetic corpus hardening

### Planned / in progress

- Расширение synthetic regression set вокруг опасных зон:
  - ИНН 10/12/13 цифр;
  - ИНН с пробелами;
  - OCR-искажения ИНН;
  - ОГРН / ОГРНИП;
  - БИК;
  - 20-значные счета;
  - паспортные серии/номера;
  - служебные номера актов, сертификатов, обращений;
  - phone false positives.
- Введение статуса `XFAIL` для known gaps, чтобы фиксировать желаемое поведение без превращения backlog в блокирующие ошибки.


## 2026-05-02 — Sprint 0.5 batch 1: synthetic corpus expansion

### Added

- Expanded synthetic regression corpus from 17 to 29 cases.
- Added guard-tests for:
  - passport vs service document numbers;
  - phone-like service numbers;
  - birth date vs contract date;
  - passport issue date;
  - private organization vs public authority;
  - 20-digit bank account vs УИД/service number.

### Regression result

- PASS: 25
- FAIL: 0
- XFAIL: 4
- XPASS: 0
- ERROR: 0
- TOTAL: 29
- Blocking errors: 0

Previous baseline:

- PASS: 15
- FAIL: 0
- XFAIL: 2
- TOTAL: 17

New expanded baseline:

- PASS: 25
- FAIL: 0
- XFAIL: 4
- TOTAL: 29

### New known gaps

#### `test_passport_service_number_negative_001`

Input:

`АКТ № 4012345678 от 10.01.2026 подписан сторонами.`

Current behavior:

`АКТ № [PASSPORT_1] от 10.01.2026 подписан сторонами.`

Problem:

10 digits after `АКТ №` may currently be detected as `PASSPORT`.

Classification:

`FALSE_POSITIVE / CONTEXT_ERROR`

Candidate fix:

Add service-number context guard before passport masking.

Do not detect 10 digits as `PASSPORT` after contexts such as:

- `АКТ №`
- `акт №`
- `Сертификат:`
- `сертификат:`
- `Номер обращения`
- `УИД`

unless there is an explicit passport context nearby, such as:

- `паспорт`
- `серия`
- `выдан`
- `код подразделения`

Current status:

`XFAIL`

---

#### `test_uid_20_digits_negative_001`

Input:

`УИД 12345678901234567890 указан в квитанции.`

Current behavior:

`УИД [ACCOUNT_1] указан в квитанции.`

Problem:

20 digits after `УИД` may currently be detected as `ACCOUNT`.

Classification:

`FALSE_POSITIVE / CONTEXT_ERROR`

Candidate fix:

Add service-number context guard before account masking.

Do not detect 20-digit sequences as `ACCOUNT` after contexts such as:

- `УИД`
- `Номер обращения`
- `АКТ №`
- `Сертификат`
- `сертификат`

unless there is an explicit banking context nearby, such as:

- `расчётный счёт`
- `расчетный счет`
- `р/с`
- `счёт`
- `счет`
- `корреспондентский счёт`
- `к/с`
- `банк`

Current status:

`XFAIL`

### Notes

- No active core changes were made in this step.
- Two token taxonomy mismatches were resolved in tests:
  - `BIRTH_DATE` → `DATE_BIRTH`
  - `PASSPORT_DATE` → `DATE_DOC_ISSUE`
- The new synthetic corpus file was successfully accepted by `run_regression_tests.py`.
- There were no JSONL format errors.
- There were no blocking regression errors after converting the two newly discovered weak spots to `XFAIL`.

### Next recommended controlled improvement

Candidate:

`test_passport_service_number_negative_001`

Goal:

Move this test from `XFAIL` to `PASS`.

Expected target after fix:

- PASS: 26
- FAIL: 0
- XFAIL: 3
- XPASS: 0
- ERROR: 0
- TOTAL: 29

Important:

Do not weaken passport detection globally. The fix should be context-based: service-number contexts should block accidental `PASSPORT` masking, while explicit passport contexts should continue to work.

## 2026-05-02 — Sprint 0.5 controlled fix 1: passport vs service number

### Fixed

- Fixed false positive detection where a 10-digit service document number after `АКТ №` could be incorrectly masked as `PASSPORT`.

### Case

Regression test:

`test_passport_service_number_negative_001`

Input:

`АКТ № 4012345678 от 10.01.2026 подписан сторонами.`

Previous behavior:

`АКТ № [PASSPORT_1] от 10.01.2026 подписан сторонами.`

Expected behavior:

`АКТ № 4012345678 от 10.01.2026 подписан сторонами.`

### Change

Added a context guard for `PASSPORT` false positives.

A 10-digit sequence is not treated as `PASSPORT` when it appears near service-number contexts such as:

- `АКТ №`
- `акт №`
- `Сертификат`
- `Номер обращения`
- `УИД`

unless there is an explicit passport context nearby, such as:

- `паспорт`
- `серия`
- `выдан`
- `код подразделения`

### Regression result

After the fix:

- PASS: 26
- FAIL: 0
- XFAIL: 3
- XPASS: 0
- ERROR: 0
- TOTAL: 29
- Blocking errors: 0

### Result

`test_passport_service_number_negative_001` moved from `XFAIL` to `PASS`.

### Remaining known gaps

- `test_inn_spaced_known_gap_001`
  - INN with spaces is not yet reliably detected.

- `test_inn_ocr_letter_known_gap_001`
  - INN with OCR letter substitution is not yet reliably detected.

- `test_uid_20_digits_negative_001`
  - 20 digits after `УИД` may still be incorrectly detected as `ACCOUNT`.

### Notes

- Passport detection was not weakened globally.
- Explicit passport contexts continue to work.
- The fix is context-based and limited to service-number false positives.

## 2026-05-02 — Sprint 0.5 controlled fix 2: UID vs 20-digit account

### Fixed

- Fixed false positive detection where a 20-digit service identifier after `УИД` could be incorrectly masked as `ACCOUNT`.

### Case

Regression test:

`test_uid_20_digits_negative_001`

Input:

`УИД 12345678901234567890 указан в квитанции.`

Previous behavior:

`УИД [ACCOUNT_1] указан в квитанции.`

Expected behavior:

`УИД 12345678901234567890 указан в квитанции.`

### Change

Added a context guard for `ACCOUNT` false positives.

A 20-digit sequence is not treated as `ACCOUNT` when it appears near service-number contexts such as:

- `УИД`
- `UID`
- `Номер обращения`
- `АКТ №`
- `Сертификат`
- `регистрационный номер`

unless there is an explicit banking context nearby, such as:

- `расчётный счёт`
- `расчетный счет`
- `р/с`
- `корреспондентский счёт`
- `к/с`
- `банк`
- `счёт получателя`
- `счёт плательщика`

### Regression result

After the fix:

- PASS: 27
- FAIL: 0
- XFAIL: 2
- XPASS: 0
- ERROR: 0
- TOTAL: 29
- Blocking errors: 0

### Result

`test_uid_20_digits_negative_001` moved from `XFAIL` to `PASS`.

### Remaining known gaps

- `test_inn_spaced_known_gap_001`
  - INN with spaces is not yet reliably detected.

- `test_inn_ocr_letter_known_gap_001`
  - INN with OCR letter substitution is not yet reliably detected.

### Notes

- Account detection was not weakened globally.
- Explicit banking contexts continue to work.
- The fix is context-based and limited to service-number false positives.

## 2026-05-03 — GitHub export v2.2 self-test

### Verified

Built GitHub-safe clean export:

```text
github_export_v2/
github_export_v2.zip
```

Export builder completed successfully.

Export audit passed.

Public documentation skeleton was included:

- `README.md`
- `LICENSE`
- `NOTICE`
- `THIRD_PARTY_LICENSES.md`
- `DISCLAIMER.md`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `ROADMAP.md`
- `docs/*`
- `.github/ISSUE_TEMPLATE/*`
- `.github/workflows/tests.yml`

### Regression self-test from clean export

Regression was run from inside `github_export_v2`.

Result:

```text
PASS 27 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 29
Blocking errors: 0
```

### Notes

- The clean export is self-contained for synthetic regression testing.
- Generated runtime output under `github_export_v2/output/` should not be committed.
- `expected/regression_last_results.json` is generated by regression runs and does not need to be committed.
- The public repository should keep `output/` as a template working folder only.
- Before final `git add`, rebuild a fresh clean export or remove generated runtime files created by the self-test.

## 2026-05-03 — Public cleanup before GitHub v1

### Changed

- Added public entrypoint:

```text
pseudonymize.py
```

- Added public token restoration entrypoint:

```text
restore_tokens.py
```

- Kept legacy compatibility entrypoints:

```text
1_anonymize.py
2_deanonymize.py
```

- Added public Windows batch launchers:

```text
pseudonymize.bat
restore_tokens.bat
```

- Updated legacy batch launchers to call the new public entrypoints.

### Added

- Added restore-token smoke test:

```text
run_restore_tokens_smoke_test.py
run_restore_tokens_smoke_test.bat
```

- Added cleanup report:

```text
PUBLIC_CLEANUP_BEFORE_GITHUB_REPORT.md
```

- Created backup before cleanup:

```text
archive/public_cleanup_v1/2026-05-03_12-47-12/
```

### Verified

Synthetic regression after public cleanup:

```text
PASS 27 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 29
Blocking errors: 0
```

Restore-token smoke test:

```text
PASS: restore smoke test succeeded.
```

### Notes

- `pseudonymize.py` is now the preferred public entrypoint.
- `restore_tokens.py` is now the preferred public token restoration entrypoint.
- `1_anonymize.py` and `2_deanonymize.py` remain as compatibility wrappers.
- Public docs were partially updated to prefer the new names.
- GitHub export builder was updated to include the new public entrypoints.

## 2026-05-03 — v0.1-alpha polish preparation

### Changed

- Added explicit `v0.1-alpha / experimental MVP` release status to README.
- Clarified that the current public release is an experimental local-first MVP, not production security/compliance software.
- Added a short `v0.1-alpha polish` section to ROADMAP.

### Regression status

No core behavior changes were made.

Current synthetic regression baseline remains:

```text
PASS 27 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 29
Blocking errors: 0
```

### Notes

- INN with spaces and INN OCR-letter substitution remain known XFAIL gaps.
- Those gaps are intentionally deferred to a separate mini-sprint.
- This polish step is intended to prepare the repository for a future `v0.1-alpha` tag/release.

