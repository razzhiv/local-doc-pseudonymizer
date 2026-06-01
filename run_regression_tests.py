from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from quality_metrics import get_case_category_ids, write_quality_metrics_reports

ROOT = Path(__file__).resolve().parent
ANONYMIZER_PATH = ROOT / "pseudonymize.py"
EXPECTED_DIR = ROOT / "expected"
REPORTS_DIR = ROOT / "output" / "reports"
REGRESSION_CASES_PATH = EXPECTED_DIR / "regression_cases.jsonl"
LAST_RESULTS_PATH = EXPECTED_DIR / "regression_last_results.json"

PLACEHOLDERS = {
    "<DIGITS_10>": "4723456789",
    "<DIGITS_12>": "473254765214",
    "<DIGITS_13>": "4732547652143",
    "<INN_12_SPACED>": "473 254 765 214",
    "<DIGITS_12_SPACED>": "473 254 765 214",
    "<INN_12_OCR_LETTER>": "47325476521З",
    "<OGRN_13>": "1027700132195",
    "<OGRNIP_15>": "304500116000157",
    "<BIK_9>": "044525225",
    "<PHONE_RU>": "+7 921 123-45-67",
    "<PHONE_RU_SPACED>": "8 912 345 10 04",
    "<CARD_16_GROUPED>": "4111 1111 1111 1111",
    "<ACCOUNT_20>": "40702810900000000001",
    "<CORR_ACCOUNT_20>": "30101810400000000225",
    "<PASSPORT_SERIES_NUMBER>": "1234 567890",
}

CORE_TESTS: List[Dict[str, Any]] = [{'test_id': 'test_valid_inn_12_001',
  'description': 'Валидный 12-значный ИНН рядом с меткой ИНН должен скрываться как INN.',
  'source': 'canonical_synthetic',
  'safe_context': 'ИНН: <DIGITS_12>',
  'test_input': 'ИНН: 473254765214',
  'expected_contains': ['ИНН: [INN_1]'],
  'expected_not_contains': ['473254765214', '[OCR_SUSPECT_INN_1]'],
  'expected_replacement_types': ['INN'],
  'expected_skipped_reasons': [],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_ocr_suspect_inn_13_001',
  'description': '13 цифр рядом с меткой ИНН не должны считаться валидным ИНН, но должны скрываться как '
                 'OCR_SUSPECT_INN.',
  'source': 'canonical_synthetic',
  'safe_context': 'ИНН: <DIGITS_13>',
  'test_input': 'ИНН: 4732547652143',
  'expected_contains': ['ИНН: [OCR_SUSPECT_INN_1]'],
  'expected_not_contains': ['4732547652143', '[INN_1]', '[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': ['OCR_SUSPECT_INN'],
  'expected_skipped_reasons': [],
  'expected_status': 'SUSPECT_ENTITY',
  'expected_policy_action': 'MASK_AND_REVIEW',
  'test_type': 'suspect_positive'},
 {'test_id': 'test_act_13_digits_negative_001',
  'description': "13 цифр после 'АКТ №' — служебный номер, не ИНН, не телефон и не карта.",
  'source': 'canonical_synthetic',
  'safe_context': 'АКТ № <DIGITS_13>',
  'test_input': 'АКТ № 4732547652143',
  'expected_contains': ['АКТ № 4732547652143'],
  'expected_not_contains': ['[OCR_SUSPECT_INN_1]', '[INN_1]', '[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_certificate_13_digits_negative_001',
  'description': "13 цифр после 'Сертификат:' — служебный номер, не ИНН, не телефон и не карта.",
  'source': 'canonical_synthetic',
  'safe_context': 'Сертификат: <DIGITS_13>',
  'test_input': 'Сертификат: 4732547652143',
  'expected_contains': ['Сертификат: 4732547652143'],
  'expected_not_contains': ['[OCR_SUSPECT_INN_1]', '[INN_1]', '[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_phone_ru_positive_001',
  'description': 'Обычный российский телефон должен скрываться как PHONE.',
  'source': 'canonical_synthetic',
  'safe_context': 'Телефон: <PHONE_RU>',
  'test_input': 'Телефон: +7 921 123-45-67',
  'expected_contains': ['Телефон: [PHONE_1]'],
  'expected_not_contains': ['+7 921 123-45-67'],
  'expected_replacement_types': ['PHONE'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'}]

EXTENDED_TESTS: List[Dict[str, Any]] = [{'test_id': 'test_valid_inn_10_001',
  'description': '10-значный ИНН рядом с меткой ИНН должен скрываться как INN.',
  'source': 'extended_synthetic',
  'safe_context': 'ИНН: <DIGITS_10>',
  'test_input': 'ИНН: 4723456789',
  'expected_contains': ['ИНН: [INN_1]'],
  'expected_not_contains': ['4723456789', '[OCR_SUSPECT_INN_1]'],
  'expected_replacement_types': ['INN'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_ogrn_13_positive_001',
  'description': 'ОГРН 13 цифр рядом с меткой ОГРН должен скрываться как OGRN.',
  'source': 'extended_synthetic',
  'safe_context': 'ОГРН: <OGRN_13>',
  'test_input': 'ОГРН: 1027700132195',
  'expected_contains': ['ОГРН: [OGRN_1]'],
  'expected_not_contains': ['1027700132195'],
  'expected_replacement_types': ['OGRN'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_ogrnip_15_positive_001',
  'description': 'ОГРНИП 15 цифр рядом с меткой ОГРНИП должен скрываться как OGRNIP.',
  'source': 'extended_synthetic',
  'safe_context': 'ОГРНИП: <OGRNIP_15>',
  'test_input': 'ОГРНИП: 304500116000157',
  'expected_contains': ['ОГРНИП: [OGRNIP_1]'],
  'expected_not_contains': ['304500116000157'],
  'expected_replacement_types': ['OGRNIP'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_bik_9_positive_001',
  'description': 'БИК 9 цифр рядом с меткой БИК должен скрываться как BIK.',
  'source': 'extended_synthetic',
  'safe_context': 'БИК: <BIK_9>',
  'test_input': 'БИК: 044525225',
  'expected_contains': ['БИК: [BIK_1]'],
  'expected_not_contains': ['044525225'],
  'expected_replacement_types': ['BIK'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_account_20_positive_001',
  'description': '20-значная последовательность должна скрываться как ACCOUNT.',
  'source': 'extended_synthetic',
  'safe_context': 'Расчетный счет: <ACCOUNT_20>',
  'test_input': 'Расчетный счет: 40702810900000000001',
  'expected_contains': ['Расчетный счет: [ACCOUNT_1]'],
  'expected_not_contains': ['40702810900000000001'],
  'expected_replacement_types': ['ACCOUNT'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_corr_account_20_positive_001',
  'description': '20-значный корреспондентский счет должен скрываться как ACCOUNT.',
  'source': 'extended_synthetic',
  'safe_context': 'Корреспондентский счет: <CORR_ACCOUNT_20>',
  'test_input': 'Корреспондентский счет: 30101810400000000225',
  'expected_contains': ['Корреспондентский счет: [ACCOUNT_1]'],
  'expected_not_contains': ['30101810400000000225'],
  'expected_replacement_types': ['ACCOUNT'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_passport_plain_positive_001',
  'description': 'Паспортная серия и номер в формате 1234 567890 должны скрываться как PASSPORT.',
  'source': 'extended_synthetic',
  'safe_context': 'Паспорт <PASSPORT_SERIES_NUMBER>',
  'test_input': 'Паспорт 1234 567890',
  'expected_contains': ['Паспорт [PASSPORT_1]'],
  'expected_not_contains': ['1234 567890'],
  'expected_replacement_types': ['PASSPORT'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_appeal_number_13_digits_negative_001',
  'description': "13 цифр после 'Номер обращения' — служебный номер, не ИНН, не телефон и не карта.",
  'source': 'extended_synthetic',
  'safe_context': 'Номер обращения <DIGITS_13>',
  'test_input': 'Номер обращения 4732547652143',
  'expected_contains': ['Номер обращения 4732547652143'],
  'expected_not_contains': ['[OCR_SUSPECT_INN_1]', '[INN_1]', '[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_act_phone_like_negative_001',
  'description': 'Номер акта, похожий на телефон, не должен скрываться как PHONE.',
  'source': 'extended_synthetic',
  'safe_context': 'АКТ № 89123451004',
  'test_input': 'АКТ № 89123451004',
  'expected_contains': ['АКТ № 89123451004'],
  'expected_not_contains': ['[PHONE_1]', '[INN_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_certificate_phone_like_negative_001',
  'description': 'Номер сертификата, похожий на телефон, не должен скрываться как PHONE.',
  'source': 'extended_synthetic',
  'safe_context': 'Сертификат: <PHONE_RU_SPACED>',
  'test_input': 'Сертификат: 8 912 345 10 04',
  'expected_contains': ['Сертификат: 8 912 345 10 04'],
  'expected_not_contains': ['[PHONE_1]', '[INN_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_inn_spaced_known_gap_001',
  'description': 'Sprint 0.6: ИНН с пробелами рядом с явной меткой ИНН должен скрываться как INN.',
  'source': 'sprint_0_6_synthetic',
  'safe_context': 'ИНН: <INN_12_SPACED>',
  'test_input': 'ИНН: 473 254 765 214',
  'expected_contains': ['ИНН: [INN_1]'],
  'expected_not_contains': ['473 254 765 214'],
  'expected_replacement_types': ['INN'],
  'expected_skipped_reasons': [],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive',
  'fixed_in': 'Sprint 0.6 — INN normalization and OCR-suspect handling'},
 {'test_id': 'test_inn_ocr_letter_known_gap_001',
  'description': 'Sprint 0.6: OCR-буква З вместо цифры 3 рядом с меткой ИНН должна попадать в suspect/review, а не в '
                 'валидный INN.',
  'source': 'sprint_0_6_synthetic',
  'safe_context': 'ИНН: <INN_12_OCR_LETTER>',
  'test_input': 'ИНН: 47325476521З',
  'expected_contains': ['ИНН: [OCR_SUSPECT_INN_1]'],
  'expected_not_contains': ['47325476521З', '[INN_1]'],
  'expected_replacement_types': ['OCR_SUSPECT_INN'],
  'expected_skipped_reasons': [],
  'expected_status': 'SUSPECT_ENTITY',
  'expected_policy_action': 'MASK_AND_REVIEW',
  'test_type': 'suspect_positive',
  'fixed_in': 'Sprint 0.6 — INN normalization and OCR-suspect handling'},
 {'test_id': 'test_passport_context_positive_001',
  'description': "Паспортная серия и номер рядом с явной меткой 'Паспорт:' должны скрываться как PASSPORT.",
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'Паспорт: <PASSPORT_SERIES_NUMBER>',
  'test_input': 'Паспорт: 4012 345678 выдан отделом МВД России.',
  'expected_contains': ['[PASSPORT_1]'],
  'expected_not_contains': ['4012 345678', '[INN_1]', '[PHONE_1]'],
  'expected_replacement_types': ['PASSPORT'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_passport_service_number_negative_001',
  'description': '10 цифр после АКТ № — служебный номер и не должен маскироваться как PASSPORT.',
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'АКТ № <DIGITS_10>',
  'test_input': 'АКТ № 4012345678 от 10.01.2026 подписан сторонами.',
  'expected_contains': ['АКТ № 4012345678'],
  'expected_not_contains': ['[PASSPORT_1]', '[INN_1]', '[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow',
  'fixed_in': 'Sprint 0.5 controlled fix: passport vs service number'},
 {'test_id': 'test_act_phone_like_11_digits_negative_001',
  'description': "Phone-like номер после 'АКТ №' не должен скрываться как PHONE, CARD или INN.",
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'АКТ № <PHONE_LIKE_11_DIGITS>',
  'test_input': 'АКТ № 89211234567 от 10.01.2026 составлен после осмотра.',
  'expected_contains': ['АКТ № 89211234567'],
  'expected_not_contains': ['[PHONE_1]', '[CARD_1]', '[INN_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_certificate_phone_like_plus7_negative_001',
  'description': 'Номер сертификата в формате +7 не должен автоматически считаться телефоном в контексте '
                 "'Сертификат:'.",
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'Сертификат: <PHONE_LIKE_PLUS7>',
  'test_input': 'Сертификат: +79211234567 зарегистрирован в журнале.',
  'expected_contains': ['Сертификат: +79211234567'],
  'expected_not_contains': ['[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_appeal_phone_like_negative_001',
  'description': 'Номер обращения, похожий на телефон, не должен скрываться как PHONE, CARD или INN.',
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'Номер обращения <PHONE_LIKE_11_DIGITS>',
  'test_input': 'Номер обращения 89211234567 зарегистрирован 10 апреля 2026 года.',
  'expected_contains': ['Номер обращения 89211234567'],
  'expected_not_contains': ['[PHONE_1]', '[CARD_1]', '[INN_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_birth_date_positive_001',
  'description': 'Дата рождения должна скрываться текущим типом DATE_BIRTH.',
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'Дата рождения: <DATE_DD_MM_YYYY>',
  'test_input': 'Дата рождения: 01.02.1980.',
  'expected_contains': ['Дата рождения: [DATE_BIRTH_1]'],
  'expected_not_contains': ['01.02.1980'],
  'expected_replacement_types': ['DATE_BIRTH'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive',
  'note': 'Адаптировано под фактическую taxonomy текущего ядра: DATE_BIRTH вместо BIRTH_DATE.'},
 {'test_id': 'test_contract_date_negative_001',
  'description': 'Обычная договорная дата не должна скрываться как чувствительная дата.',
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'Договор заключён <DATE_DD_MM_YYYY>',
  'test_input': 'Договор заключён 21.01.2025 между сторонами.',
  'expected_contains': ['Договор заключён 21.01.2025'],
  'expected_not_contains': ['[BIRTH_DATE_1]', '[PASSPORT_DATE_1]', '[REG_DATE_1]', '[MED_DATE_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_passport_issue_date_positive_001',
  'description': 'Дата выдачи паспорта должна скрываться текущим типом DATE_DOC_ISSUE.',
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'Паспорт выдан <DATE_DD_MM_YYYY>',
  'test_input': 'Паспорт выдан 10.03.2010 отделом МВД России.',
  'expected_contains': ['Паспорт выдан [DATE_DOC_ISSUE_1]'],
  'expected_not_contains': ['10.03.2010'],
  'expected_replacement_types': ['DATE_DOC_ISSUE'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive',
  'note': 'Адаптировано под фактическую taxonomy текущего ядра: DATE_DOC_ISSUE вместо PASSPORT_DATE.'},
 {'test_id': 'test_private_org_ooo_positive_001',
  'description': 'Частная организация с маркером ООО должна скрываться как ORG_PRIVATE.',
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'ООО <ORG_NAME>',
  'test_input': 'Договор заключён с ООО Ромашка на выполнение работ.',
  'expected_contains': ['[ORG_PRIVATE_1]'],
  'expected_not_contains': ['Ромашка'],
  'expected_replacement_types': ['ORG_PRIVATE'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_public_org_ifns_negative_001',
  'description': 'ИФНС России должна оставаться как публичный орган, а не скрываться как частная организация.',
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'ИФНС России № <NUMBER>',
  'test_input': 'Документ направлен в ИФНС России № 10 по Санкт-Петербургу.',
  'expected_contains': ['ИФНС России № 10'],
  'expected_not_contains': ['[ORG_PRIVATE_1]', '[PERSON_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_account_20_with_context_positive_001',
  'description': '20-значный расчётный счёт с банковским контекстом должен скрываться как ACCOUNT.',
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'Расчетный счет <ACCOUNT_20>',
  'test_input': 'Расчетный счет 40702810900000000001 открыт в банке.',
  'expected_contains': ['[ACCOUNT_1]'],
  'expected_not_contains': ['40702810900000000001', '[CARD_1]', '[PHONE_1]'],
  'expected_replacement_types': ['ACCOUNT'],
  'expected_status': 'VALID_ENTITY',
  'expected_policy_action': 'MASK_CONFIDENTLY',
  'test_type': 'valid_positive'},
 {'test_id': 'test_uid_20_digits_negative_001',
  'description': '20-значный УИД — служебный идентификатор и не должен маскироваться как ACCOUNT.',
  'source': 'sprint_0_5_synthetic_batch_1',
  'safe_context': 'УИД <DIGITS_20>',
  'test_input': 'УИД 12345678901234567890 указан в квитанции.',
  'expected_contains': ['УИД 12345678901234567890'],
  'expected_not_contains': ['[ACCOUNT_1]', '[CORR_ACCOUNT_1]', '[CARD_1]', '[PHONE_1]'],
  'expected_replacement_types': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow',
  'fixed_in': 'Sprint 0.5 controlled fix: UID vs 20-digit account'},
 {'test_id': 'test_act_spaced_inn_like_negative_001',
  'description': 'Sprint 0.6 guard: spaced 12-digit service number after АКТ № must not be treated as INN without '
                 'explicit ИНН label.',
  'source': 'sprint_0_6_synthetic',
  'safe_context': 'АКТ № <DIGITS_12_SPACED>',
  'test_input': 'АКТ № 473 254 765 214',
  'expected_contains': ['АКТ № 473 254 765 214'],
  'expected_not_contains': ['[INN_1]', '[OCR_SUSPECT_INN_1]', '[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_skipped_reasons': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_certificate_spaced_inn_like_negative_001',
  'description': 'Sprint 0.6 guard: spaced 12-digit service number after Сертификат must not be treated as INN without '
                 'explicit ИНН label.',
  'source': 'sprint_0_6_synthetic',
  'safe_context': 'Сертификат: <DIGITS_12_SPACED>',
  'test_input': 'Сертификат: 473 254 765 214',
  'expected_contains': ['Сертификат: 473 254 765 214'],
  'expected_not_contains': ['[INN_1]', '[OCR_SUSPECT_INN_1]', '[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_skipped_reasons': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_appeal_spaced_inn_like_negative_001',
  'description': 'Sprint 0.6 guard: spaced 12-digit appeal number must not be treated as INN without explicit ИНН '
                 'label.',
  'source': 'sprint_0_6_synthetic',
  'safe_context': 'Номер обращения <DIGITS_12_SPACED>',
  'test_input': 'Номер обращения 473 254 765 214 зарегистрирован.',
  'expected_contains': ['Номер обращения 473 254 765 214 зарегистрирован.'],
  'expected_not_contains': ['[INN_1]', '[OCR_SUSPECT_INN_1]', '[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_skipped_reasons': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_act_ocr_letter_inn_like_negative_001',
  'description': 'Sprint 0.6 guard: OCR-like value after АКТ № must not be treated as OCR_SUSPECT_INN without explicit '
                 'ИНН label.',
  'source': 'sprint_0_6_synthetic',
  'safe_context': 'АКТ № <INN_12_OCR_LETTER>',
  'test_input': 'АКТ № 47325476521З',
  'expected_contains': ['АКТ № 47325476521З'],
  'expected_not_contains': ['[OCR_SUSPECT_INN_1]', '[INN_1]', '[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_skipped_reasons': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
  'expected_policy_action': 'ALLOW',
  'test_type': 'negative_allow'},
 {'test_id': 'test_certificate_ocr_letter_inn_like_negative_001',
  'description': 'Sprint 0.6 guard: OCR-like value after Сертификат must not be treated as OCR_SUSPECT_INN without '
                 'explicit ИНН label.',
  'source': 'sprint_0_6_synthetic',
  'safe_context': 'Сертификат: <INN_12_OCR_LETTER>',
  'test_input': 'Сертификат: 47325476521З',
  'expected_contains': ['Сертификат: 47325476521З'],
  'expected_not_contains': ['[OCR_SUSPECT_INN_1]', '[INN_1]', '[PHONE_1]', '[CARD_1]'],
  'expected_replacement_types': [],
  'expected_skipped_reasons': [],
  'expected_status': 'SKIPPED_BY_ALLOW',
 'expected_policy_action': 'ALLOW',
 'test_type': 'negative_allow'}]

ADDITIONAL_EXTENDED_TESTS_JSONL = """
{"test_id": "test_snils_spaces_positive_001", "description": "Sprint 1.1: СНИЛС с пробелами должен скрываться как SNILS.", "source": "sprint_1_1_quality_pack", "safe_context": "СНИЛС: <SNILS_SPACED>", "test_input": "СНИЛС: 123 456 789 00", "expected_contains": ["СНИЛС: [SNILS_1]"], "expected_not_contains": ["123 456 789 00"], "expected_replacement_types": ["SNILS"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_passport_series_number_separated_positive_001", "description": "Sprint 1.1: паспортные серия и номер в раздельных полях должны скрываться как PASSPORT.", "source": "sprint_1_1_quality_pack", "safe_context": "Паспорт РФ: серия <PASSPORT_SERIES> № <PASSPORT_NUMBER>", "test_input": "Паспорт РФ: серия 1234 № 567890 выдан отделом МВД.", "expected_contains": ["Паспорт РФ: серия [PASSPORT_1] выдан"], "expected_not_contains": ["1234", "567890"], "expected_replacement_types": ["PASSPORT"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_division_code_spaced_context_positive_001", "description": "Sprint 1.1: код подразделения с пробелом должен скрываться как DIVISION_CODE.", "source": "sprint_1_1_quality_pack", "safe_context": "Код подразделения: <DIVISION_CODE_SPACED>", "test_input": "Код подразделения: 780 001.", "expected_contains": ["Код подразделения: [DIVISION_CODE_1]."], "expected_not_contains": ["780 001"], "expected_replacement_types": ["DIVISION_CODE"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_bik_spaced_positive_001", "description": "Sprint 1.1: БИК с пробелами должен скрываться как BIK рядом с явной меткой.", "source": "sprint_1_1_quality_pack", "safe_context": "БИК: <BIK_SPACED>", "test_input": "БИК: 044 525 225", "expected_contains": ["БИК: [BIK_1]"], "expected_not_contains": ["044 525 225"], "expected_replacement_types": ["BIK"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_kpp_spaced_positive_001", "description": "Sprint 1.1: КПП с пробелами должен скрываться как KPP рядом с явной меткой.", "source": "sprint_1_1_quality_pack", "safe_context": "КПП: <KPP_SPACED>", "test_input": "КПП: 770 801 001", "expected_contains": ["КПП: [KPP_1]"], "expected_not_contains": ["770 801 001"], "expected_replacement_types": ["KPP"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_ogrn_spaced_positive_001", "description": "Sprint 1.1: ОГРН с пробелами должен скрываться как OGRN рядом с явной меткой.", "source": "sprint_1_1_quality_pack", "safe_context": "ОГРН: <OGRN_SPACED>", "test_input": "ОГРН: 102 770 013 2195", "expected_contains": ["ОГРН: [OGRN_1]"], "expected_not_contains": ["102 770 013 2195"], "expected_replacement_types": ["OGRN"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_private_org_quoted_positive_001", "description": "Sprint 1.1: частная организация с префиксом и названием в кавычках должна скрывать название.", "source": "sprint_1_1_quality_pack", "safe_context": "ООО «<ORG_NAME>»", "test_input": "Договор заключён с ООО «Ромашка-Сервис» на выполнение работ.", "expected_contains": ["ООО [ORG_PRIVATE_1]"], "expected_not_contains": ["Ромашка-Сервис"], "expected_replacement_types": ["ORG_PRIVATE"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_registration_date_one_digit_day_positive_001", "description": "Sprint 1.1: дата регистрации с однозначным днём должна скрываться как DATE_REGISTRATION.", "source": "sprint_1_1_quality_pack", "safe_context": "Дата регистрации по месту жительства: <DATE_D_M_YYYY>", "test_input": "Дата регистрации по месту жительства: 5.03.2020.", "expected_contains": ["Дата регистрации по месту жительства: [DATE_REGISTRATION_1]."], "expected_not_contains": ["5.03.2020"], "expected_replacement_types": ["DATE_REGISTRATION"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_address_index_after_address_label_positive_001", "description": "Sprint 1.1: индекс и адресный хвост после метки адреса должны скрываться, город сохраняется.", "source": "sprint_1_1_quality_pack", "safe_context": "Адрес регистрации: <POST_INDEX>, г. Санкт-Петербург, <ADDRESS_TAIL>", "test_input": "Адрес регистрации: 190000, г. Санкт-Петербург, Невский проспект, д. 10, кв. 5.", "expected_contains": ["Адрес регистрации: [POST_INDEX_1], г. Санкт-Петербург, [ADDRESS_DETAIL_1]."], "expected_not_contains": ["190000", "д. 10", "кв. 5"], "expected_replacement_types": ["POST_INDEX", "ADDRESS_DETAIL"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_mobile_phone_context_positive_001", "description": "Sprint 1.1: мобильный телефон без +7/8 рядом с явной меткой должен скрываться как PHONE.", "source": "sprint_1_1_quality_pack", "safe_context": "Мобильный: <PHONE_LOCAL_MOBILE>", "test_input": "Мобильный: 921 123-45-67.", "expected_contains": ["Мобильный: [PHONE_1]."], "expected_not_contains": ["921 123-45-67"], "expected_replacement_types": ["PHONE"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_en_full_name_context_positive_001", "description": "Sprint 1.2: English Full name label should mask a Latin person name as PERSON.", "source": "sprint_1_2_english_minimal_profile", "safe_context": "Full name: <PERSON_EN>", "test_input": "Full name: John Smith.", "expected_contains": ["Full name: [PERSON_1]."], "expected_not_contains": ["John Smith"], "expected_replacement_types": ["PERSON"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_en_passport_no_positive_001", "description": "Sprint 1.2: English passport label should mask Russian passport-style number as PASSPORT.", "source": "sprint_1_2_english_minimal_profile", "safe_context": "Passport No.: <PASSPORT_RU>", "test_input": "Passport No.: 1234 567890 issued by authority.", "expected_contains": ["Passport No.: [PASSPORT_1] issued"], "expected_not_contains": ["1234", "567890"], "expected_replacement_types": ["PASSPORT"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_en_tax_id_positive_001", "description": "Sprint 1.2: English Tax ID / TIN label should mask a 12-digit INN as INN.", "source": "sprint_1_2_english_minimal_profile", "safe_context": "Tax ID: <INN_12>", "test_input": "Tax ID: 473254765214.", "expected_contains": ["Tax ID: [INN_1]."], "expected_not_contains": ["473254765214"], "expected_replacement_types": ["INN"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_en_tax_id_spaced_positive_001", "description": "Sprint 1.2: English Tax ID label should mask a spaced 12-digit INN as INN.", "source": "sprint_1_2_english_minimal_profile", "safe_context": "Tax ID: <INN_12_SPACED>", "test_input": "Tax ID: 473 254 765 214.", "expected_contains": ["Tax ID: [INN_1]."], "expected_not_contains": ["473 254 765 214"], "expected_replacement_types": ["INN"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_en_dob_positive_001", "description": "Sprint 1.2: English date of birth label should mask DD.MM.YYYY as DATE_BIRTH.", "source": "sprint_1_2_english_minimal_profile", "safe_context": "Date of birth: <DATE_DD_MM_YYYY>", "test_input": "Date of birth: 01.02.1980.", "expected_contains": ["Date of birth: [DATE_BIRTH_1]."], "expected_not_contains": ["01.02.1980"], "expected_replacement_types": ["DATE_BIRTH"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_en_phone_context_positive_001", "description": "Sprint 1.2: English phone/mobile label should mask a local mobile-like number as PHONE.", "source": "sprint_1_2_english_minimal_profile", "safe_context": "Phone: <PHONE_LOCAL_MOBILE>", "test_input": "Phone: 921 123-45-67.", "expected_contains": ["Phone: [PHONE_1]."], "expected_not_contains": ["921 123-45-67"], "expected_replacement_types": ["PHONE"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_en_address_detail_positive_001", "description": "Sprint 1.2: English address label should mask postal index and street/building/apartment tail while keeping city context.", "source": "sprint_1_2_english_minimal_profile", "safe_context": "Registered address: <POST_INDEX>, Saint Petersburg, <ADDRESS_TAIL_EN>", "test_input": "Registered address: 190000, Saint Petersburg, Nevsky Prospect, building 10, apartment 5.", "expected_contains": ["Registered address: [POST_INDEX_1], Saint Petersburg, [ADDRESS_DETAIL_1]."], "expected_not_contains": ["190000", "building 10", "apartment 5"], "expected_replacement_types": ["POST_INDEX", "ADDRESS_DETAIL"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_en_private_org_llc_positive_001", "description": "Sprint 1.2: English private organization prefix LLC should preserve legal form and mask organization name.", "source": "sprint_1_2_english_minimal_profile", "safe_context": "LLC <ORG_NAME_EN>", "test_input": "Contract signed with LLC Romashka Service.", "expected_contains": ["LLC [ORG_PRIVATE_1]"], "expected_not_contains": ["Romashka Service"], "expected_replacement_types": ["ORG_PRIVATE"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_address_registration_building_parts_positive_001", "description": "Sprint 1.3: registration address with корпус, строение, помещение and office details should mask postal index and address tail.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Адрес регистрации: 123456, г. Тестоград, Учебный проспект, д. 10, корп. 2, стр. 1, пом. 5, офис 7.", "test_input": "Адрес регистрации: 123456, г. Тестоград, Учебный проспект, д. 10, корп. 2, стр. 1, пом. 5, офис 7.", "expected_contains": ["Адрес регистрации: [POST_INDEX_1], г. Тестоград, [ADDRESS_DETAIL_1]."], "expected_not_contains": ["123456", "д. 10", "корп. 2", "стр. 1", "пом. 5", "офис 7"], "expected_replacement_types": ["POST_INDEX", "ADDRESS_DETAIL"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_residence_place_house_apartment_positive_001", "description": "Sprint 1.3: place of residence line with house and apartment should hide the detailed address portion.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Место жительства: г. Тестоград, дом 10, квартира 5.", "test_input": "Место жительства: г. Тестоград, дом 10, квартира 5.", "expected_contains": ["Место жительства: г. Тестоград, [ADDRESS_DETAIL_1]."], "expected_not_contains": ["дом 10", "квартира 5"], "expected_replacement_types": ["ADDRESS_DETAIL"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_object_location_premises_office_positive_001", "description": "Sprint 1.3: object location line with premises, office and корпус should hide location details.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Место нахождения объекта: г. Тестоград, помещение 12-Н, офис 4, корпус 1.", "test_input": "Место нахождения объекта: г. Тестоград, помещение 12-Н, офис 4, корпус 1.", "expected_contains": ["Место нахождения объекта: г. Тестоград, [ADDRESS_DETAIL_1]."], "expected_not_contains": ["помещение 12-Н", "офис 4", "корпус 1"], "expected_replacement_types": ["ADDRESS_DETAIL"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_postal_index_label_positive_001", "description": "Sprint 1.3: explicit postal index label should mask a six-digit index.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Почтовый индекс: 123456.", "test_input": "Почтовый индекс: 123456.", "expected_contains": ["Почтовый индекс: [POST_INDEX_1]."], "expected_not_contains": ["123456"], "expected_replacement_types": ["POST_INDEX"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_passport_identity_document_phrase_positive_001", "description": "Sprint 1.3: identity-document phrasing with passport number, issue date and division code should be masked.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Документ, удостоверяющий личность: паспорт РФ 1122 334455, дата выдачи 10.03.2010, код подразделения 770-777.", "test_input": "Документ, удостоверяющий личность: паспорт РФ 1122 334455, дата выдачи 10.03.2010, код подразделения 770-777.", "expected_contains": ["паспорт РФ [PASSPORT_1]", "дата выдачи [DATE_DOC_ISSUE_1]", "код подразделения [DIVISION_CODE_1]"], "expected_not_contains": ["1122 334455", "10.03.2010", "770-777"], "expected_replacement_types": ["PASSPORT", "DATE_DOC_ISSUE", "DIVISION_CODE"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_passport_identity_separated_series_number_positive_001", "description": "Sprint 1.3: identity-document phrasing with separated серия and номер should mask the passport number.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Документ, удостоверяющий личность: серия 1122 номер 334455.", "test_input": "Документ, удостоверяющий личность: серия 1122 номер 334455.", "expected_contains": ["Документ, удостоверяющий личность: серия [PASSPORT_1]."], "expected_not_contains": ["1122", "334455"], "expected_replacement_types": ["PASSPORT"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_passport_abbrev_series_number_positive_001", "description": "Sprint 1.3: abbreviated сер. № passport phrasing should mask passport number and issue date.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Паспорт РФ: сер. 1122 № 334455 выдан 10.03.2010.", "test_input": "Паспорт РФ: сер. 1122 № 334455 выдан 10.03.2010.", "expected_contains": ["Паспорт РФ: сер. [PASSPORT_1] выдан [DATE_DOC_ISSUE_1]."], "expected_not_contains": ["1122", "334455", "10.03.2010"], "expected_replacement_types": ["PASSPORT", "DATE_DOC_ISSUE"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_division_code_abbrev_positive_001", "description": "Sprint 1.3: abbreviated код подр. label should mask a separated division code.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Код подр.: 770 777.", "test_input": "Код подр.: 770 777.", "expected_contains": ["Код подр.: [DIVISION_CODE_1]."], "expected_not_contains": ["770 777"], "expected_replacement_types": ["DIVISION_CODE"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_requisites_inn_kpp_slash_pair_positive_001", "description": "Sprint 1.3: mixed ИНН/КПП slash label should mask both values narrowly by context.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Реквизиты: ИНН/КПП 772345678901 / 771234567.", "test_input": "Реквизиты: ИНН/КПП 772345678901 / 771234567.", "expected_contains": ["Реквизиты: ИНН/КПП [INN_1] / [KPP_1]."], "expected_not_contains": ["772345678901", "771234567"], "expected_replacement_types": ["INN", "KPP"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_requisites_ogrn_ogrnip_slash_pair_positive_001", "description": "Sprint 1.3: mixed ОГРН/ОГРНИП slash label should mask both values narrowly by context.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Реквизиты: ОГРН/ОГРНИП 1122334455667 / 315123456789012.", "test_input": "Реквизиты: ОГРН/ОГРНИП 1122334455667 / 315123456789012.", "expected_contains": ["Реквизиты: ОГРН/ОГРНИП [OGRN_1] / [OGRNIP_1]."], "expected_not_contains": ["1122334455667", "315123456789012"], "expected_replacement_types": ["OGRN", "OGRNIP"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_bank_requisites_abbrev_accounts_positive_001", "description": "Sprint 1.3: abbreviated р/с, к/с and spaced БИК in a requisites block should be masked.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Банковские реквизиты: р/с 40702810000000000002, к/с 30101810000000000003, БИК 044 000 999.", "test_input": "Банковские реквизиты: р/с 40702810000000000002, к/с 30101810000000000003, БИК 044 000 999.", "expected_contains": ["[ACCOUNT_1]", "[ACCOUNT_2]", "БИК [BIK_1]"], "expected_not_contains": ["40702810000000000002", "30101810000000000003", "044 000 999"], "expected_replacement_types": ["ACCOUNT", "BIK"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_table_like_labels_compact_positive_001", "description": "Sprint 1.3: compact table-like labels should provide enough context for common Russian personal and business fields.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "ФИО: Иванов Иван Иванович; Дата рожд.: 01.02.1980; Адрес рег.: 123456, г. Тестоград, Учебный проспект, д. 10; Сер. № 1122 334455; Тел.: 921 123-45-67; р/с 40702810000000000002.", "test_input": "ФИО: Иванов Иван Иванович; Дата рожд.: 01.02.1980; Адрес рег.: 123456, г. Тестоград, Учебный проспект, д. 10; Сер. № 1122 334455; Тел.: 921 123-45-67; р/с 40702810000000000002.", "expected_contains": ["[PERSON_1]", "[DATE_BIRTH_1]", "[POST_INDEX_1]", "[ADDRESS_DETAIL_1]", "[PASSPORT_1]", "[PHONE_1]", "[ACCOUNT_1]"], "expected_not_contains": ["Иванов Иван Иванович", "01.02.1980", "123456", "д. 10", "1122 334455", "921 123-45-67", "40702810000000000002"], "expected_replacement_types": ["PERSON", "DATE_BIRTH", "POST_INDEX", "ADDRESS_DETAIL", "PASSPORT", "PHONE", "ACCOUNT"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_private_org_ao_quoted_positive_001", "description": "Sprint 1.3: private АО name in quotes should preserve legal form and mask the name.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "АО «Северный Вектор»", "test_input": "Договор заключен с АО «Северный Вектор» на поставку.", "expected_contains": ["АО [ORG_PRIVATE_1]"], "expected_not_contains": ["Северный Вектор"], "expected_replacement_types": ["ORG_PRIVATE"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_private_org_pao_unquoted_positive_001", "description": "Sprint 1.3: private ПАО unquoted synthetic name should preserve legal form and mask the name.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "ПАО Синтетик Проект", "test_input": "Акционер: ПАО Синтетик Проект владеет долей.", "expected_contains": ["ПАО [ORG_PRIVATE_1]"], "expected_not_contains": ["Синтетик Проект"], "expected_replacement_types": ["ORG_PRIVATE"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_ip_person_positive_001", "description": "Sprint 1.3: ИП should preserve the business form and mask the following synthetic person name.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "ИП Иванов Иван Иванович", "test_input": "Исполнитель: ИП Иванов Иван Иванович оказывает услуги.", "expected_contains": ["ИП [PERSON_1]"], "expected_not_contains": ["Иванов Иван Иванович"], "expected_replacement_types": ["PERSON"], "expected_status": "VALID_ENTITY", "expected_policy_action": "MASK_CONFIDENTLY", "test_type": "valid_positive"}
{"test_id": "test_public_authority_court_case_negative_001", "description": "Sprint 1.3 guard: public court name and arbitration-style case number should remain visible under current allow policy.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Арбитражный суд города Тестбурга; дело № А40-123456/2026", "test_input": "Документ направлен в Арбитражный суд города Тестбурга; дело № А40-123456/2026 оставлено без движения.", "expected_contains": ["Арбитражный суд города Тестбурга", "дело № А40-123456/2026"], "expected_not_contains": ["[ORG_PRIVATE_1]", "[PERSON_1]", "[PASSPORT_1]", "[INN_1]", "[PHONE_1]"], "expected_replacement_types": [], "expected_status": "SKIPPED_BY_ALLOW", "expected_policy_action": "ALLOW", "test_type": "negative_allow"}
{"test_id": "test_contract_number_slash_negative_001", "description": "Sprint 1.3 guard: slash-style contract number should not be over-masked as INN, phone, card or passport.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Договор № 772345678901/26", "test_input": "Договор № 772345678901/26 от 21.01.2025 заключен сторонами.", "expected_contains": ["Договор № 772345678901/26", "21.01.2025"], "expected_not_contains": ["[INN_1]", "[PHONE_1]", "[CARD_1]", "[PASSPORT_1]"], "expected_replacement_types": [], "expected_status": "SKIPPED_BY_ALLOW", "expected_policy_action": "ALLOW", "test_type": "negative_allow"}
{"test_id": "test_reference_passport_like_number_negative_001", "description": "Sprint 1.3 guard: reference document number shaped like a passport should not be over-masked without passport context.", "source": "sprint_1_3_russian_recognition_quality_pack_v2", "safe_context": "Справка № 1122 334455", "test_input": "Справка № 1122 334455 выдана для внутреннего учета.", "expected_contains": ["Справка № 1122 334455"], "expected_not_contains": ["[PASSPORT_1]", "[INN_1]", "[PHONE_1]", "[CARD_1]"], "expected_replacement_types": [], "expected_status": "SKIPPED_BY_ALLOW", "expected_policy_action": "ALLOW", "test_type": "negative_allow"}
""".strip()

ADDITIONAL_EXTENDED_TESTS: List[Dict[str, Any]] = [
    json.loads(line)
    for line in ADDITIONAL_EXTENDED_TESTS_JSONL.splitlines()
    if line.strip()
]

def ensure_dirs() -> None:
    EXPECTED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Ошибка JSON в {path}, строка {line_no}: {e}")
    return rows


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def backup_existing(path: Path) -> None:
    if path.exists() and path.stat().st_size > 0:
        backup = path.with_name(f"{path.stem}_backup_{now_stamp()}{path.suffix}")
        shutil.copy2(path, backup)
        print(f"Сделан backup: {backup.relative_to(ROOT)}")


def seed_cases(extended: bool = False) -> None:
    ensure_dirs()
    backup_existing(REGRESSION_CASES_PATH)
    tests = CORE_TESTS + ((EXTENDED_TESTS + ADDITIONAL_EXTENDED_TESTS) if extended else [])
    created_at = datetime.now().isoformat(timespec="seconds")
    rows = []
    for item in tests:
        row = dict(item)
        row["created_at"] = created_at
        rows.append(row)
    write_jsonl(REGRESSION_CASES_PATH, rows)
    mode = "extended" if extended else "core"
    print(f"Записаны {mode} regression cases: {REGRESSION_CASES_PATH.relative_to(ROOT)}")
    print(f"Количество тестов: {len(rows)}")
    if extended:
        known_gaps = sum(1 for x in rows if x.get("expected_fail"))
        print(f"Из них known gaps / expected fail: {known_gaps}")


def resolve_placeholders(text: str) -> str:
    result = text or ""
    for placeholder, value in PLACEHOLDERS.items():
        result = result.replace(placeholder, value)
    return result


def load_anonymizer_module():
    if not ANONYMIZER_PATH.exists():
        raise FileNotFoundError(
            f"Не найден {ANONYMIZER_PATH}. Положите run_regression_tests.py в корень проекта рядом с pseudonymize.py."
        )
    spec = importlib.util.spec_from_file_location("anonymizer_under_test", ANONYMIZER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Не удалось загрузить pseudonymize.py как модуль.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_one_test(anonymizer, case: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
    test_id = case.get("test_id", "unknown_test")
    raw_input = case.get("test_input") or case.get("input") or case.get("safe_context") or ""
    test_input = resolve_placeholders(str(raw_input))
    result_metadata = {
        "test_id": test_id,
        "description": case.get("description", ""),
        "source": case.get("source", ""),
        "test_type": case.get("test_type", ""),
        "filename": "synthetic_regression.txt",
        "category_ids": get_case_category_ids(case),
        "expected_replacement_types": list(case.get("expected_replacement_types", []) or []),
        "expected_status": case.get("expected_status", ""),
        "expected_policy_action": case.get("expected_policy_action", ""),
        "gap_reason": case.get("gap_reason", ""),
    }
    project_dictionary = anonymizer.empty_project_dictionary()
    file_report = {
        "summary": defaultdict(int),
        "warnings": [],
        "replacements": [],
        "skipped": [],
    }
    try:
        output = anonymizer.anonymize_text_block(
            test_input,
            "synthetic_regression.txt",
            test_id,
            project_dictionary,
            file_report,
            rules,
        )
    except Exception as e:
        return {
            **result_metadata,
            "passed": False,
            "expected_fail": bool(case.get("expected_fail")),
            "outcome": "ERROR",
            "error": f"Exception during anonymization: {e}",
            "input": test_input,
            "output": None,
            "checks": [],
        }

    checks = []
    passed = True
    for expected in case.get("expected_contains", []) or []:
        expected_resolved = resolve_placeholders(str(expected))
        ok = expected_resolved in output
        checks.append({"check": "expected_contains", "value": expected_resolved, "ok": ok})
        if not ok:
            passed = False

    for forbidden in case.get("expected_not_contains", []) or []:
        forbidden_resolved = resolve_placeholders(str(forbidden))
        ok = forbidden_resolved not in output
        checks.append({"check": "expected_not_contains", "value": forbidden_resolved, "ok": ok})
        if not ok:
            passed = False

    actual_replacement_types = [x.get("type") for x in file_report.get("replacements", [])]
    for expected_type in case.get("expected_replacement_types", []) or []:
        ok = expected_type in actual_replacement_types
        checks.append({
            "check": "expected_replacement_type",
            "value": expected_type,
            "actual": actual_replacement_types,
            "ok": ok,
        })
        if not ok:
            passed = False

    expected_replacement_types = case.get("expected_replacement_types", None)
    if expected_replacement_types == []:
        ok = len(actual_replacement_types) == 0
        checks.append({"check": "expected_no_replacements", "actual": actual_replacement_types, "ok": ok})
        if not ok:
            passed = False

    actual_skipped_reasons = [x.get("reason") for x in file_report.get("skipped", [])]
    for expected_reason in case.get("expected_skipped_reasons", []) or []:
        ok = expected_reason in actual_skipped_reasons
        checks.append({
            "check": "expected_skipped_reason",
            "value": expected_reason,
            "actual": actual_skipped_reasons,
            "ok": ok,
        })
        if not ok:
            passed = False

    expected_fail = bool(case.get("expected_fail"))
    if passed and expected_fail:
        outcome = "XPASS"
    elif (not passed) and expected_fail:
        outcome = "XFAIL"
    elif passed:
        outcome = "PASS"
    else:
        outcome = "FAIL"

    return {
        **result_metadata,
        "passed": passed,
        "expected_fail": expected_fail,
        "outcome": outcome,
        "input": test_input,
        "output": output,
        "actual_replacements": file_report.get("replacements", []),
        "actual_skipped": file_report.get("skipped", []),
        "checks": checks,
    }


def run_tests(include_known_gaps_as_failures: bool = False) -> Dict[str, Any] | None:
    ensure_dirs()
    cases = read_jsonl(REGRESSION_CASES_PATH)
    if not cases:
        print("Нет regression cases. Сначала выполните: python run_regression_tests.py seed")
        return

    print("Загрузка текущего pseudonymize.py для тестов...")
    anonymizer = load_anonymizer_module()
    rules = anonymizer.load_all_rules()

    results = []
    for case in cases:
        result = run_one_test(anonymizer, case, rules)
        results.append(result)
        outcome = result["outcome"]
        print(f"{outcome:5} {result['test_id']}")
        if outcome in ["FAIL", "ERROR"] or (include_known_gaps_as_failures and outcome == "XFAIL") or outcome == "XPASS":
            print(f"      input : {result.get('input')}")
            print(f"      output: {result.get('output')}")
            if result.get("gap_reason"):
                print(f"      gap   : {result.get('gap_reason')}")
            failed_checks = [c for c in result.get("checks", []) if not c.get("ok")]
            for check in failed_checks[:8]:
                print(f"      failed: {check}")

    counters = {"PASS": 0, "FAIL": 0, "XFAIL": 0, "XPASS": 0, "ERROR": 0}
    for r in results:
        counters[r["outcome"]] = counters.get(r["outcome"], 0) + 1

    blocking_failed = counters.get("FAIL", 0) + counters.get("ERROR", 0)
    if include_known_gaps_as_failures:
        blocking_failed += counters.get("XFAIL", 0)

    payload = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "total": len(results),
        "pass": counters.get("PASS", 0),
        "fail": counters.get("FAIL", 0),
        "xfail": counters.get("XFAIL", 0),
        "xpass": counters.get("XPASS", 0),
        "error": counters.get("ERROR", 0),
        "blocking_failed": blocking_failed,
        "results": results,
    }

    with LAST_RESULTS_PATH.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    report_path = REPORTS_DIR / f"regression_report_{now_stamp()}.md"
    write_markdown_report(report_path, payload)

    print("")
    print(
        f"Итого: PASS {payload['pass']} / FAIL {payload['fail']} / "
        f"XFAIL {payload['xfail']} / XPASS {payload['xpass']} / ERROR {payload['error']} / TOTAL {payload['total']}"
    )
    print(f"Блокирующих ошибок: {payload['blocking_failed']}")
    print(f"JSON результат: {LAST_RESULTS_PATH.relative_to(ROOT)}")
    print(f"MD отчёт: {report_path.relative_to(ROOT)}")
    return payload


def write_markdown_report(path: Path, payload: Dict[str, Any]) -> None:
    lines = []
    lines.append("# Regression report")
    lines.append("")
    lines.append(f"Дата: {payload['created_at']}")
    lines.append(f"Всего тестов: {payload['total']}")
    lines.append(f"PASS: {payload['pass']}")
    lines.append(f"FAIL: {payload['fail']}")
    lines.append(f"XFAIL / known gaps: {payload['xfail']}")
    lines.append(f"XPASS / unexpectedly fixed: {payload['xpass']}")
    lines.append(f"ERROR: {payload['error']}")
    lines.append(f"Блокирующих ошибок: {payload['blocking_failed']}")
    lines.append("")

    for result in payload["results"]:
        outcome = result.get("outcome", "UNKNOWN")
        lines.append(f"## {outcome} — {result['test_id']}")
        lines.append("")
        if result.get("description"):
            lines.append(result["description"])
            lines.append("")
        if result.get("gap_reason"):
            lines.append(f"**Known gap:** {result['gap_reason']}")
            lines.append("")
        lines.append("**Input:**")
        lines.append("")
        lines.append("```text")
        lines.append(str(result.get("input", "")))
        lines.append("```")
        lines.append("")
        lines.append("**Output:**")
        lines.append("")
        lines.append("```text")
        lines.append(str(result.get("output", "")))
        lines.append("```")
        lines.append("")

        failed_checks = [c for c in result.get("checks", []) if not c.get("ok")]
        if failed_checks:
            lines.append("**Failed checks:**")
            lines.append("")
            for check in failed_checks:
                lines.append(f"- `{check.get('check')}`: `{check.get('value', '')}`; actual: `{check.get('actual', '')}`")
            lines.append("")

        if result.get("actual_replacements"):
            lines.append("**Actual replacements:**")
            lines.append("")
            for r in result["actual_replacements"]:
                lines.append(f"- {r.get('type')}: `{r.get('original')}` → `{r.get('token')}` ({r.get('method')})")
            lines.append("")

        if result.get("actual_skipped"):
            lines.append("**Actual skipped:**")
            lines.append("")
            for r in result["actual_skipped"]:
                lines.append(f"- {r.get('type')}: `{r.get('original')}` — {r.get('reason')}")
            lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def show_status() -> None:
    ensure_dirs()
    files = [REGRESSION_CASES_PATH, LAST_RESULTS_PATH]
    print("Статус regression-контура:")
    for path in files:
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        print(f"- {path.relative_to(ROOT)}: {'есть' if exists else 'нет'}, {size} байт")
    rows = read_jsonl(REGRESSION_CASES_PATH)
    if rows:
        known_gaps = sum(1 for x in rows if x.get("expected_fail"))
        print(f"Тестов: {len(rows)}; known gaps: {known_gaps}")


def main() -> None:
    command = sys.argv[1].strip().lower() if len(sys.argv) > 1 else "help"
    print("=== REGRESSION TEST TOOL v3 / synthetic corpus ===")

    if command == "seed":
        seed_cases(extended=False)
    elif command in ["seed-extended", "seed_extended", "seed_extended_tests"]:
        seed_cases(extended=True)
    elif command == "run":
        run_tests(include_known_gaps_as_failures=False)
    elif command == "run-strict":
        run_tests(include_known_gaps_as_failures=True)
    elif command in ["quality-metrics", "quality_metrics"]:
        payload = run_tests(include_known_gaps_as_failures=True)
        if payload is not None:
            paths = write_quality_metrics_reports(
                payload,
                REPORTS_DIR,
                source_results_path=LAST_RESULTS_PATH.relative_to(ROOT),
            )
            print(f"Quality metrics JSON: {paths['json'].relative_to(ROOT)}")
            print(f"Quality metrics latest JSON: {paths['json_latest'].relative_to(ROOT)}")
            print(f"Quality metrics MD: {paths['markdown'].relative_to(ROOT)}")
            print(f"Quality metrics latest MD: {paths['markdown_latest'].relative_to(ROOT)}")
    elif command == "status":
        show_status()
    else:
        print("Команды:")
        print("  python run_regression_tests.py seed")
        print("  python run_regression_tests.py seed-extended")
        print("  python run_regression_tests.py run")
        print("  python run_regression_tests.py run-strict")
        print("  python run_regression_tests.py quality-metrics")
        print("  python run_regression_tests.py status")


if __name__ == "__main__":
    main()
