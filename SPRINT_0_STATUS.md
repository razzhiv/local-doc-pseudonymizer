# SPRINT 0 STATUS

_Проект: локальная псевдонимизация / masking документов перед передачей в SaaS / LLM / третьим лицам_

_Статус на 2026-05-01: Sprint 0.2 и базовый Sprint 0.3 успешно пройдены._

---

## 1. Краткий итог

На текущем этапе проект перестал быть просто набором RegEx-правил внутри `1_anonymize.py` и получил первые элементы управляемого цикла улучшения ядра:

```text
synthetic case
→ review table
→ human decision
→ decisions.jsonl
→ candidate_rules.jsonl
→ regression_cases.jsonl
→ regression runner
→ PASS / FAIL report
→ controlled patch
→ повторный regression
```

Главное достижение: появилась проверяемая процедура улучшения, где новое правило не добавляется напрямую в ядро без кейса, решения человека и regression-теста.

---

## 2. Что реализовано

### 2.1. Human-in-the-loop review layer

Реализован человекочитаемый слой принятия решений через Excel:

```text
review/review_cases.xlsx
```

Человек больше не должен редактировать `decisions.jsonl` вручную.

Рабочий процесс:

```text
feedback/cases.jsonl
→ review/review_cases.xlsx
→ решения человека в таблице
→ feedback/decisions.jsonl
→ feedback/candidate_rules.jsonl
→ expected/regression_cases.jsonl
→ rules/manual_allow.txt / rules/manual_hide.txt при необходимости
```

Реализованные файлы / скрипты:

```text
review_tool.py
import_review.bat
check_review_results.bat
```

Проверенный результат:

```text
feedback/decisions.jsonl          — создаётся
feedback/candidate_rules.jsonl    — создаётся
expected/regression_cases.jsonl   — создаётся
rules/manual_allow.txt            — обновляется
```

---

### 2.2. Synthetic regression runner

Реализован исполняемый regression-контур:

```text
run_regression_tests.py
run_regression_tests.bat
seed_extended_regression_tests.bat
```

Он читает:

```text
expected/regression_cases.jsonl
```

Загружает текущий `1_anonymize.py`, прогоняет синтетические тесты и формирует:

```text
expected/regression_last_results.json
output/reports/regression_report_YYYY-MM-DD_HH-MM-SS.md
```

Поддерживаются статусы:

```text
PASS   — тест прошёл
FAIL   — блокирующая ошибка
XFAIL  — известный ожидаемый пробел
XPASS  — известный пробел неожиданно заработал
ERROR  — ошибка выполнения теста
```

---

### 2.3. Первый controlled improvement case: OCR_SUSPECT_INN

Реализован первый полный цикл улучшения ядра:

```text
Observed case:
ИНН: 4732547652143

Human decision:
Не считать 13 цифр валидным ИНН.
Скрывать как OCR_SUSPECT_INN только рядом с явной меткой ИНН.

Regression:
До патча: FAIL
После патча: PASS
```

Текущее рабочее поведение:

```text
ИНН: 473254765214
→ ИНН: [INN_1]

ИНН: 4723456789
→ ИНН: [INN_1]

ИНН: 4732547652143
→ ИНН: [OCR_SUSPECT_INN_1]

АКТ № 4732547652143
→ АКТ № 4732547652143

Сертификат: 4732547652143
→ Сертификат: 4732547652143
```

Важное архитектурное решение:

```text
13-значный ИНН не добавлен в VALID_INN.
Он выделен в отдельный suspect-класс OCR_SUSPECT_INN.
```

---

### 2.4. Исправлен конфликт INN vs PASSPORT

Расширенный synthetic corpus выявил ошибку:

```text
ИНН: 4723456789
→ ИНН: [PASSPORT_1]
```

Причина:

```text
10 цифр могут подходить под паспортный шаблон 4+6,
но при явной метке ИНН должен выигрывать тип INN.
```

После патча приоритетов:

```text
INN > PASSPORT
OCR_SUSPECT_INN > PASSPORT
```

Результат:

```text
test_valid_inn_10_001 — PASS
```

---

## 3. Текущий regression status

Последний успешный прогон расширенного synthetic corpus:

```text
PASS 15 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 17
Блокирующих ошибок: 0
```

Проходят:

```text
test_valid_inn_12_001
test_ocr_suspect_inn_13_001
test_act_13_digits_negative_001
test_certificate_13_digits_negative_001
test_phone_ru_positive_001
test_valid_inn_10_001
test_ogrn_13_positive_001
test_ogrnip_15_positive_001
test_bik_9_positive_001
test_account_20_positive_001
test_corr_account_20_positive_001
test_passport_plain_positive_001
test_appeal_number_13_digits_negative_001
test_act_phone_like_negative_001
test_certificate_phone_like_negative_001
```

Известные ожидаемые пробелы:

```text
test_inn_spaced_known_gap_001
test_inn_ocr_letter_known_gap_001
```

Они помечены как `XFAIL`, поэтому не считаются блокирующими ошибками.

---

## 4. Known gaps / backlog

### 4.1. INN with spaces

Пока не реализовано устойчивое распознавание ИНН с пробелами внутри значения:

```text
ИНН: 473 254 765 214
```

Статус:

```text
XFAIL
```

Решение на будущее:

```text
детектировать цифры с допустимыми пробелами / дефисами рядом с меткой ИНН;
нормализовать значение перед валидацией;
сохранять исходный вид при маскировании.
```

---

### 4.2. OCR-letter inside INN

Пока не реализовано подозрительное распознавание ИНН, где OCR заменил цифру на похожую букву:

```text
ИНН: 47325476521З
```

Статус:

```text
XFAIL
```

Решение на будущее:

```text
выделить отдельный suspect-класс, например OCR_SUSPECT_INN_CHAR;
не считать это VALID_INN;
маскировать в SaaS-safe режиме только при явной метке ИНН.
```

---

### 4.3. Более широкий synthetic corpus

Нужно постепенно расширять корпус вокруг опасных зон:

```text
ИНН / ОГРН / ОГРНИП
БИК / банковские счета / корреспондентские счета
паспортные данные
телефоны и phone-like false positives
номера актов / сертификатов / обращений
адресные фрагменты
даты рождения / даты выдачи паспорта / обычные юридические даты
ФИО в падежах
частные и публичные организации
```

---

## 5. Чувствительные файлы

Следующие файлы и папки потенциально чувствительны и не должны публиковаться, если содержат реальные данные:

```text
input/
output/
to_decode/
dictionary.json
output/dictionary.json
rules/manual_hide.txt
rules/manual_allow.txt
feedback/cases.jsonl
feedback/decisions.jsonl
feedback/candidate_rules.jsonl
review/review_cases.xlsx
output/reports/
corpus/real_sensitive/
```

Особенно чувствительные:

```text
dictionary.json
manual_hide.txt
review_cases.xlsx с реальными значениями
reports с original values
real_sensitive cases
```

Правило:

```text
Если файл содержит реальные ФИО, адреса, ИНН, паспорта, телефоны, банковские счета, фрагменты документов или словарь замен — он не должен уходить наружу.
```

---

## 6. Что можно показывать на GitHub

Можно публиковать только безопасный контур:

```text
README_synthetic_regression.md
CHANGELOG.md
SPRINT_0_STATUS.md
run_regression_tests.py
review_tool.py при условии, что внутри нет реальных данных
expected/regression_cases.jsonl только с синтетикой
corpus/synthetic/
пример synthetic review_cases.xlsx без реальных ПД
пример regression_report_*.md по synthetic corpus
```

Можно показывать как демонстрацию инженерного процесса:

```text
PASS / FAIL отчёты
synthetic cases
known gaps как XFAIL
candidate-rule pipeline
human-in-the-loop через Excel
```

Формулировка для публичного позиционирования:

```text
Проект использует synthetic regression corpus как безопасный публичный стенд проверки правил псевдонимизации.
Реальные документы и реальные ПД обрабатываются только локально и не входят в публичный corpus.
```

---

## 7. Что нельзя публиковать

Нельзя публиковать:

```text
реальные документы;
словарь замен dictionary.json;
ручные правила с реальными значениями;
Excel review-файлы с реальными фрагментами;
отчёты, где есть original values;
локальные sensitive cases;
любые PDF/DOCX из реального дела;
скриншоты с реальными ПД;
архивы проекта без предварительной очистки.
```

Перед публикацией GitHub-версии нужен отдельный clean export.

---

## 8. Текущий статус версий

Рабочее ядро:

```text
1_anonymize.py
```

Текущая подтверждённая версия должна быть зафиксирована через:

```text
freeze_current_anonymizer.py
freeze_current_anonymizer.bat
```

Ожидаемый результат фиксации:

```text
archive/1_anonymize_working_YYYY-MM-DD_HH-MM-SS.py
archive/working_versions_manifest.txt
```

Каждая стабильная версия должна фиксироваться после успешного regression-прогона.

---

## 9. Рекомендуемый следующий шаг

Не добавлять сразу новые правила в ядро.

Следующий безопасный шаг:

```text
Sprint 0.4 — расширение synthetic corpus без изменения ядра
```

Цель:

```text
добавить больше synthetic cases;
пометить known gaps как XFAIL;
выявить реальные пересечения типов;
не чинить всё сразу;
чинить только блокирующие FAIL по одному controlled improvement case.
```

Приоритеты для Sprint 0.4:

```text
1. Расширить phone-like false positives.
2. Добавить больше паспортных и ИНН-пересечений.
3. Добавить служебные номера актов, сертификатов, обращений.
4. Добавить адресные edge cases.
5. Добавить даты: birth/passport issue vs ordinary legal dates.
```

---

## 10. Главный вывод Sprint 0

Проект получил первый инженерный asset:

```text
human decision loop
+ synthetic regression corpus
+ PASS / FAIL runner
+ candidate rule layer
+ controlled patching
+ version freezing
```

Это основа для дальнейшего развития ядра без хаотичного переписывания RegEx.

Ключевая формула:

```text
Не каждое исключение — новое правило.
Не каждое правило — сразу в active core.
Не каждое скрытие — уверенное.
Не каждый FAIL нужно чинить немедленно.
Но каждый важный FAIL должен стать кейсом, решением, тестом и контролируемым изменением.
```

---

## 11. Sprint 0.5 — synthetic corpus expansion and hardening

_Дата контрольной точки: 2026-05-02_

Sprint 0.5 завершён как успешная фаза расширения synthetic regression corpus и controlled hardening ядра.

Главная цель Sprint 0.5 была не в публикации GitHub, не в упаковке и не в добавлении новых функций, а в безопасном расширении тестового корпуса и проверке устойчивости текущего ядра на новых synthetic edge cases.

### 11.1. Исходная контрольная точка

Перед началом Sprint 0.5 стабильный baseline был:

    PASS 15 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 17
    Блокирующих ошибок: 0

Известные XFAIL:

- `test_inn_spaced_known_gap_001`
  - ИНН с пробелами пока не распознаётся устойчиво.

- `test_inn_ocr_letter_known_gap_001`
  - ИНН с OCR-буквой вместо цифры пока не распознаётся устойчиво.

### 11.2. Batch 1 — расширение synthetic corpus

В первой партии Sprint 0.5 корпус был расширен с 17 до 29 тестов.

Добавлены synthetic guard-tests вокруг следующих зон:

- passport vs service document numbers;
- phone-like service numbers;
- birth date vs contract date;
- passport issue date;
- private organization vs public authority;
- 20-digit bank account vs УИД/service number.

После первичного добавления batch 1 были выявлены 4 FAIL:

1. `test_passport_service_number_negative_001`
   - 10 цифр после `АКТ №` ошибочно маскировались как `PASSPORT`.
   - Классификация: `FALSE_POSITIVE / CONTEXT_ERROR`.

2. `test_birth_date_positive_001`
   - Дата рождения скрывалась корректно, но тест ожидал другой тип токена.
   - Было в тесте: `BIRTH_DATE`.
   - Фактически в ядре: `DATE_BIRTH`.
   - Решение: адаптировать тест под текущую taxonomy ядра.

3. `test_passport_issue_date_positive_001`
   - Дата выдачи паспорта скрывалась корректно, но тест ожидал другой тип токена.
   - Было в тесте: `PASSPORT_DATE`.
   - Фактически в ядре: `DATE_DOC_ISSUE`.
   - Решение: адаптировать тест под текущую taxonomy ядра.

4. `test_uid_20_digits_negative_001`
   - 20 цифр после `УИД` ошибочно маскировались как `ACCOUNT`.
   - Классификация: `FALSE_POSITIVE / CONTEXT_ERROR`.

После адаптации taxonomy и перевода двух реальных weak spots в XFAIL получена стабильная промежуточная контрольная точка:

    PASS 25 / FAIL 0 / XFAIL 4 / XPASS 0 / ERROR 0 / TOTAL 29
    Блокирующих ошибок: 0

Новые XFAIL после batch 1:

- `test_passport_service_number_negative_001`
- `test_uid_20_digits_negative_001`

### 11.3. Controlled fix 1 — passport vs service number

Первый controlled improvement был выполнен для кейса:

- `test_passport_service_number_negative_001`

Проблемное поведение до исправления:

    АКТ № 4012345678 от 10.01.2026 подписан сторонами.
    →
    АКТ № [PASSPORT_1] от 10.01.2026 подписан сторонами.

Ожидаемое поведение:

    АКТ № 4012345678 от 10.01.2026 подписан сторонами.

Суть исправления:

Добавлен контекстный guard для `PASSPORT`.

10-значная последовательность не считается `PASSPORT`, если рядом есть служебный контекст, например:

- `АКТ №`
- `акт №`
- `Сертификат`
- `Номер обращения`
- `УИД`

и при этом рядом нет явного паспортного контекста, например:

- `паспорт`
- `серия`
- `выдан`
- `код подразделения`

Важно:

- passport detector не был ослаблен глобально;
- явные паспортные контексты продолжают работать;
- исправление ограничено защитой от false positive в служебных номерах.

Результат после controlled fix 1:

    PASS 26 / FAIL 0 / XFAIL 3 / XPASS 0 / ERROR 0 / TOTAL 29
    Блокирующих ошибок: 0

Тест `test_passport_service_number_negative_001` переведён из `XFAIL` в `PASS`.

Snapshot зафиксирован в папке:

    archive/working_versions/2026-05-02_sprint_0_5_fix1_passport_service/

В snapshot вошли:

- `1_anonymize.py`
- `regression_cases.jsonl`
- `regression_report_2026-05-02_23-14-29.md`
- `CHANGELOG.md`
- `VERSION_NOTE.md`
- `MANIFEST_SHA256.txt`

Чувствительные рабочие зоны в snapshot не включались:

- `input/`
- `output/anonymized/`
- `output/project_dictionary.json`
- `feedback/`
- `review/`
- `rules/manual_hide.txt`
- `rules/manual_allow.txt`

### 11.4. Controlled fix 2 — UID vs 20-digit account

Второй controlled improvement был выполнен для кейса:

- `test_uid_20_digits_negative_001`

Проблемное поведение до исправления:

    УИД 12345678901234567890 указан в квитанции.
    →
    УИД [ACCOUNT_1] указан в квитанции.

Ожидаемое поведение:

    УИД 12345678901234567890 указан в квитанции.

Суть исправления:

Добавлен контекстный guard для `ACCOUNT`.

20-значная последовательность не считается `ACCOUNT`, если рядом есть служебный контекст, например:

- `УИД`
- `UID`
- `Номер обращения`
- `АКТ №`
- `Сертификат`
- `регистрационный номер`

и при этом рядом нет явного банковского контекста, например:

- `расчётный счёт`
- `расчетный счет`
- `р/с`
- `корреспондентский счёт`
- `к/с`
- `банк`
- `счёт получателя`
- `счёт плательщика`

Важно:

- account detector не был ослаблен глобально;
- банковские реквизиты продолжают скрываться;
- исправление ограничено защитой от false positive в служебных идентификаторах.

Проверено, что после исправления продолжают проходить:

- `test_account_20_positive_001`
- `test_corr_account_20_positive_001`
- `test_account_20_with_context_positive_001`

Результат после controlled fix 2:

    PASS 27 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 29
    Блокирующих ошибок: 0

Тест `test_uid_20_digits_negative_001` переведён из `XFAIL` в `PASS`.

Snapshot зафиксирован в папке:

    archive/working_versions/2026-05-02_sprint_0_5_fix2_uid_account/

В snapshot вошли:

- `1_anonymize.py`
- `regression_cases.jsonl`
- `regression_report_2026-05-02_23-47-07.md`
- `CHANGELOG.md`
- `VERSION_NOTE.md`
- `MANIFEST_SHA256.txt`

Чувствительные рабочие зоны в snapshot не включались:

- `input/`
- `output/anonymized/`
- `output/project_dictionary.json`
- `feedback/`
- `review/`
- `rules/manual_hide.txt`
- `rules/manual_allow.txt`

### 11.5. Финальный статус Sprint 0.5

Финальная контрольная точка Sprint 0.5:

    PASS 27 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 29
    Блокирующих ошибок: 0

Что изменилось по сравнению со стартом Sprint 0.5:

    Было:
    PASS 15 / FAIL 0 / XFAIL 2 / TOTAL 17

    Стало:
    PASS 27 / FAIL 0 / XFAIL 2 / TOTAL 29

Итог:

- synthetic regression corpus расширен с 17 до 29 тестов;
- новые тесты выявили 2 реальных false positive;
- оба false positive прошли controlled improvement loop;
- оба исправления подтверждены regression runner;
- оба исправления зафиксированы snapshot-ами;
- активное ядро не менялось без regression tests;
- blocking errors отсутствуют.

### 11.6. Оставшиеся known gaps

После Sprint 0.5 остаются только два known gaps:

#### 1. INN with spaces

Тест:

- `test_inn_spaced_known_gap_001`

Проблема:

    ИНН: 473 254 765 214

пока не распознаётся устойчиво как ИНН или OCR/SUSPECT ИНН.

Предварительное направление будущего решения:

- детектировать ИНН рядом с явной меткой `ИНН`;
- разрешить пробелы/дефисы внутри значения;
- нормализовать значение перед проверкой;
- не считать служебные номера ИНН без явного контекста;
- добавить positive и negative regression tests до правки ядра.

#### 2. INN with OCR letter

Тест:

- `test_inn_ocr_letter_known_gap_001`

Проблема:

    ИНН: 47325476521З

пока не распознаётся устойчиво как OCR-suspect case.

Предварительное направление будущего решения:

- не считать такое значение валидным `INN`;
- выделить отдельный suspect-класс или расширить `OCR_SUSPECT_INN`;
- срабатывать только рядом с явной меткой `ИНН`;
- сохранять осторожную SaaS-safe логику: mask and review;
- добавить negative tests для актов, сертификатов и обращений.

### 11.7. Архитектурный вывод Sprint 0.5

Sprint 0.5 подтвердил правильность controlled improvement loop:

    synthetic case
    → regression run
    → FAIL
    → classification
    → XFAIL / known gap
    → controlled fix
    → regression confirmation
    → snapshot

Ключевой вывод:

Не каждое найденное расхождение нужно чинить сразу.  
Но каждое важное расхождение должно быть превращено в тест, классифицировано, зафиксировано и только затем исправлено через controlled patch.

Sprint 0.5 также подтвердил, что текущий synthetic corpus уже полезен как safety net:

- он выявляет false positives;
- защищает от возврата старых ошибок;
- позволяет проверять точечные изменения;
- не требует реальных персональных данных;
- подходит для будущего GitHub-safe контура.

### 11.8. Рекомендуемый следующий шаг

Sprint 0.5 можно считать закрытым как successful hardening phase.

Следующие возможные направления:

#### Вариант A — GitHub / public MVP preparation

Вернуться к оформлению GitHub-safe версии:

- README;
- DISCLAIMER;
- SECURITY.md;
- CONTRIBUTING.md;
- issue templates;
- synthetic corpus;
- clean export;
- проверка отсутствия реальных данных.

#### Вариант B — Mini-sprint 0.6: INN normalization and OCR-suspect

Отдельно заняться двумя оставшимися XFAIL:

- ИНН с пробелами;
- ИНН с OCR-буквой вместо цифры.

Важно:

Этот mini-sprint должен быть отдельной фазой, потому что он меняет не только false-positive guards, но и логику нормализации / suspect-detection для ИНН.

---

## 12. Sprint 0.7 public baseline alignment

Sprint 0.6 is treated as completed and verified.

Current public synthetic regression baseline:

```text
PASS 34 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 34
Blocking errors: 0
```

Closed known gaps:

- INN with spaces;
- INN with OCR-letter substitution.

Sprint 0.7 focuses on public baseline alignment rather than new detection behavior:

- GitHub Actions must run `python run_regression_tests.py run-strict`;
- README and public docs must show the current 34/0/0/34 baseline;
- old XFAIL wording should be kept only as historical Sprint 0.5 context;
- no new core behavior changes are included in this cleanup step.
