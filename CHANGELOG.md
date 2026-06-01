# CHANGELOG

## 2026-06-02 - Sprint 1.8 - Encrypted vault design spike

### Added

- Added `docs/vault_design.md` documenting the sensitive boundary for token dictionaries, raw extracted text, reports, runtime artifacts, public issue safety, and a possible future encrypted vault.
- Expanded `docs/token_dictionary_security.md` with report/log boundaries, cleanup wording, future vault constraints, and public-claim limits.
- Updated README, docs index, STATUS, and ROADMAP with short pointers to the Sprint 1.8 design.

### Safety notes

- Documentation-only design spike; no production encryption was implemented.
- Recognizer rules, detection behavior, pseudonymization behavior, and restore behavior were not changed.
- No crypto dependencies, GUI, OCR, PDF table extraction, packaging, installer, cloud storage, AI automation integration, real documents, generated reports, dictionaries, screenshots, ZIPs, or token maps were added.
- The current MVP still uses plaintext token dictionaries and must not be described as cryptographically protected.

## 2026-06-01 - Sprint 1.7 - Russian-first HTML review report / review UX localization

### Changed

- Localized the self-contained HTML review report so Russian-speaking reviewers see Russian-first section titles, summary cards, warnings, table headers, checklist, cleanup guidance, limitations, empty states, and technical notes.
- Added Russian display labels for detected-data categories while preserving stable technical codes such as `PERSON`, `INN`, and `OCR_SUSPECT_INN` in the report.
- Kept existing report paths and filenames under `output/reports/review_report_*.html` and `output/reports/review_report_latest.html`.
- Updated README, review workflow, demo walkthrough, docs index, status notes, and HTML report tests for the localized review UX.

### Safety notes

- Display-only localization; recognizer rules and detection behavior were not changed.
- The HTML report remains self-contained with inline CSS and no external CSS, JavaScript, CDN, or network resources.
- The report remains a local human-review aid for pseudonymization / reversible masking / risk reduction, not a guarantee of anonymization, regulatory compliance, DLP coverage, or zero leakage.
- No OCR, PDF table extraction, GUI, encrypted vault, packaging, installer, real documents, or real personal data were added.

## 2026-06-01 - Sprint 1.6 - Quality metrics dashboard / categories

### Added

- Added `quality_metrics.py` to aggregate strict synthetic regression results into a machine-readable quality metrics JSON report and a Russian-first Markdown report.
- Added explicit, extensible category metadata for synthetic regression visibility, including stable English category IDs and optional Russian display names.
- Added `python run_regression_tests.py quality-metrics`, which runs strict synthetic regression and writes:
  - `output/reports/quality_metrics_<timestamp>.json`
  - `output/reports/quality_metrics_latest.json`
  - `output/reports/quality_metrics_<timestamp>.md`
  - `output/reports/quality_metrics_latest.md`
- Added pytest coverage for category aggregation, failure summarization, UTF-8 Russian Markdown, latest-file writing, and category derivation.

### Changed

- Strict regression results now include lightweight synthetic case metadata needed by the quality dashboard.
- Updated README, docs, and status notes for Sprint 1.6.

### Safety notes

- Synthetic regression data only.
- The dashboard is engineering visibility, not a compliance score, anonymization guarantee, or proof that false negatives are impossible.
- No OCR, GUI, vault/encryption, packaging, PDF table extraction, or recognizer-rule rewrite.
- Generated runtime reports remain under ignored `output/reports/` and are not intended for commit.

## 2026-06-01 - Sprint 1.5 - Review UX v0.1 / HTML review report

### Added

- Added a self-contained local HTML review report generated under `output/reports/review_report_*.html` and `output/reports/review_report_latest.html`.
- Added summary counts, category/token counts, findings/replacements, manual review cases, skipped findings, warnings, checklist, cleanup guidance, and local-artifact safety notes.
- Added pytest coverage for synthetic HTML generation, safety warning text, category/count output, offline-only HTML, and escaping of special values.

### Changed

- `pseudonymize.py` now writes the HTML review report alongside the existing JSON, DOCX, and Markdown reports.
- Updated demo/docs/status notes for the HTML review report.

### Safety notes

- Synthetic fixtures only.
- No OCR, PDF table extraction, GUI, vault/encryption, recognizer rewrite, packaging, installer, or compliance-positioning change.
- No generated dictionary, runtime input/output/review/to_decode artifact, cache, virtual environment, or private file is intended for commit.

## 2026-06-01 — Sprint 1.4 — Golden synthetic demo + release-ready story

### Added

- Added `examples/golden_demo/` with a safe synthetic client/legal/business scenario.
- Added a committed text fixture, a disposable DOCX generator, and a safe masked preview for the demo.
- Added `docs/demo_walkthrough.md` covering the demo story, run commands, expected outputs, review checklist, restore flow, cleanup, and limitations.
- Added a lightweight pytest smoke test that generates the demo DOCX in a temporary directory and verifies the expected tokenized story.

### Changed

- Updated `STATUS.md` and `docs/README.md` to point to the golden synthetic demo.

### Safety notes

- Synthetic data only.
- No OCR, PDF table extraction, GUI, vault/encryption, recognizer rewrite, packaging, or compliance-positioning change.
- No generated dictionary, runtime input/output/review/to_decode artifact, cache, virtual environment, or private file is intended for commit.

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

## 2026-05-03 — v0.1-alpha released

- Published GitHub repository: `razzhiv/local-doc-pseudonymizer`.
- Published pre-release: `v0.1-alpha — experimental MVP`.
- GitHub Actions synthetic regression passed.
- Current baseline:

```text
PASS 27 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 29
Blocking errors: 0
```

Remaining known gaps:

- INN with spaces.
- INN with OCR-letter substitution.

## 2026-05-04 — Sprint 0.6 — INN normalization and OCR-suspect handling

### Changed

- Added controlled handling for spaced/hyphenated INN values near an explicit `ИНН` label.
- Added controlled OCR-suspect handling for INN-like values near an explicit `ИНН` label.
- Reused existing `OCR_SUSPECT_INN` taxonomy; no new token type was added.
- Added negative guard tests for service-like numbers without an explicit `ИНН` label.

### Closed known gaps

- `test_inn_spaced_known_gap_001`
- `test_inn_ocr_letter_known_gap_001`

### Regression result

```text
PASS 34 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 34
Blocking errors: 0
```

### Safety notes

- No broad long-number detector was added.
- Service-number contexts remain protected by regression tests.
- No OCR engine, GUI, encrypted vault, or release work was added.

## 2026-05-05 — Sprint 0.7 — public baseline alignment

### Changed

- Updated GitHub Actions to run the actual strict synthetic regression command: `python run_regression_tests.py run-strict`.
- Aligned README and public documentation with the Sprint 0.6 baseline.
- Removed stale wording that listed the two Sprint 0.6 INN cases as current XFAIL gaps.

### Regression baseline

```text
PASS 34 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 34
Blocking errors: 0
```

### Notes

- No new core detection behavior was added in this cleanup step.
- INN with spaces and INN OCR-letter substitution remain documented as former synthetic XFAIL cases fixed in Sprint 0.6.
## 2026-05-06 — Sprint 0.7.1 — regression entrypoint cleanup

### Changed

- Regression tests now load `pseudonymize.py` directly instead of the legacy `1_anonymize.py` compatibility wrapper.
- Updated operational messages and comments to refer to `pseudonymize.py`.
- `1_anonymize.py` remains available as a legacy compatibility entrypoint.

### Regression

- PASS 34 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 34
- Blocking errors: 0

## 2026-05-30 — Sprint 0.8 through Sprint 1.2 checkpoint

### Added / changed

- Sprint 0.8 — PDF safe handling.
- Sprint 0.9 — DOCX table-aware context.
- Sprint 1.0 — document-level regression tests.
- Sprint 1.1 — Russian recognition quality pack v1.
- Sprint 1.2 — minimal label-driven English profile.

### Regression baseline

```text
PASS 52 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 52
Document-level pytest: 5 passed
```

### Notes

- Synthetic baseline increased from 34 to 44 cases in Sprint 1.1.
- Synthetic baseline increased from 44 to 52 cases in Sprint 1.2.
- No OCR support was added.

## 2026-05-31 — release/docs hygiene checkpoint

### Changed

- Aligned README, STATUS, ROADMAP and VERSION_NOTE with the post-Sprint-1.2 baseline.
- Updated `docs/review_workflow.md` from the older 34-case baseline to the current 52-case baseline.
- Updated `docs/synthetic_regression_report_latest.md` with a fresh 52-case report.
- Added `docs/release_checklist.md` for public-repository safety checks.
- Expanded `docs/positioning.md` and `docs/token_dictionary_security.md` with clearer scope, reporting and dictionary-risk notes.

### Verified

```text
python -m py_compile pseudonymize.py
python run_regression_tests.py run-strict
python -m pytest -q tests/test_document_level_regression.py
```

Result:

```text
PASS 52 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 52
Document-level pytest: 5 passed
```

### Safety notes

- No real personal data was added.
- No new core detection behavior was added in this docs/release hygiene checkpoint.
- Future false negatives should continue to be rewritten into synthetic regression cases before rule changes.

## 2026-06-01 — Sprint 1.3 — Russian recognition quality pack v2

### Added

- Added 18 synthetic regression cases for Russian legal/business recognition quality:
  - address details and postal indexes;
  - passport phrasing and division codes;
  - mixed реквизиты blocks;
  - table-like labels;
  - private organizations/IP;
  - court, contract and reference-number negative guards.
- Added a seed-safe embedded extension in `run_regression_tests.py` so `seed-extended` recreates the full 70-case corpus.

### Changed

- Added narrow label/context-driven rules for address-detail tails, abbreviated passport/division labels, slash-pair requisites, abbreviated birth-date and phone labels, and IP person-name preservation.
- Added a service-context guard for `Справка №` passport-like reference numbers.

### Verified

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
Document-level pytest: 5 passed
```

### Safety notes

- Synthetic data only.
- No PDF table extraction, OCR, GUI, encrypted vault, packaging, positioning or compliance behavior was changed.
