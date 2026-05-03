from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent
ANONYMIZER_PATH = ROOT / "1_anonymize.py"
EXPECTED_DIR = ROOT / "expected"
REPORTS_DIR = ROOT / "output" / "reports"
REGRESSION_CASES_PATH = EXPECTED_DIR / "regression_cases.jsonl"
LAST_RESULTS_PATH = EXPECTED_DIR / "regression_last_results.json"

PLACEHOLDERS = {
    "<DIGITS_10>": "4723456789",
    "<DIGITS_12>": "473254765214",
    "<DIGITS_13>": "4732547652143",
    "<INN_12_SPACED>": "473 254 765 214",
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

CORE_TESTS: List[Dict[str, Any]] = [
    {
        "test_id": "test_valid_inn_12_001",
        "description": "Валидный 12-значный ИНН рядом с меткой ИНН должен скрываться как INN.",
        "source": "canonical_synthetic",
        "safe_context": "ИНН: <DIGITS_12>",
        "test_input": "ИНН: 473254765214",
        "expected_contains": ["ИНН: [INN_1]"],
        "expected_not_contains": ["473254765214", "[OCR_SUSPECT_INN_1]"],
        "expected_replacement_types": ["INN"],
        "expected_skipped_reasons": [],
        "expected_status": "VALID_ENTITY",
        "expected_policy_action": "MASK_CONFIDENTLY",
        "test_type": "valid_positive",
    },
    {
        "test_id": "test_ocr_suspect_inn_13_001",
        "description": "13 цифр рядом с меткой ИНН не должны считаться валидным ИНН, но должны скрываться как OCR_SUSPECT_INN.",
        "source": "canonical_synthetic",
        "safe_context": "ИНН: <DIGITS_13>",
        "test_input": "ИНН: 4732547652143",
        "expected_contains": ["ИНН: [OCR_SUSPECT_INN_1]"],
        "expected_not_contains": ["4732547652143", "[INN_1]", "[PHONE_1]", "[CARD_1]"],
        "expected_replacement_types": ["OCR_SUSPECT_INN"],
        "expected_skipped_reasons": [],
        "expected_status": "SUSPECT_ENTITY",
        "expected_policy_action": "MASK_AND_REVIEW",
        "test_type": "suspect_positive",
    },
    {
        "test_id": "test_act_13_digits_negative_001",
        "description": "13 цифр после 'АКТ №' — служебный номер, не ИНН, не телефон и не карта.",
        "source": "canonical_synthetic",
        "safe_context": "АКТ № <DIGITS_13>",
        "test_input": "АКТ № 4732547652143",
        "expected_contains": ["АКТ № 4732547652143"],
        "expected_not_contains": ["[OCR_SUSPECT_INN_1]", "[INN_1]", "[PHONE_1]", "[CARD_1]"],
        "expected_replacement_types": [],
        "expected_status": "SKIPPED_BY_ALLOW",
        "expected_policy_action": "ALLOW",
        "test_type": "negative_allow",
    },
    {
        "test_id": "test_certificate_13_digits_negative_001",
        "description": "13 цифр после 'Сертификат:' — служебный номер, не ИНН, не телефон и не карта.",
        "source": "canonical_synthetic",
        "safe_context": "Сертификат: <DIGITS_13>",
        "test_input": "Сертификат: 4732547652143",
        "expected_contains": ["Сертификат: 4732547652143"],
        "expected_not_contains": ["[OCR_SUSPECT_INN_1]", "[INN_1]", "[PHONE_1]", "[CARD_1]"],
        "expected_replacement_types": [],
        "expected_status": "SKIPPED_BY_ALLOW",
        "expected_policy_action": "ALLOW",
        "test_type": "negative_allow",
    },
    {
        "test_id": "test_phone_ru_positive_001",
        "description": "Обычный российский телефон должен скрываться как PHONE.",
        "source": "canonical_synthetic",
        "safe_context": "Телефон: <PHONE_RU>",
        "test_input": "Телефон: +7 921 123-45-67",
        "expected_contains": ["Телефон: [PHONE_1]"],
        "expected_not_contains": ["+7 921 123-45-67"],
        "expected_replacement_types": ["PHONE"],
        "expected_status": "VALID_ENTITY",
        "expected_policy_action": "MASK_CONFIDENTLY",
        "test_type": "valid_positive",
    },
]

EXTENDED_TESTS: List[Dict[str, Any]] = [
    {
        "test_id": "test_valid_inn_10_001",
        "description": "10-значный ИНН рядом с меткой ИНН должен скрываться как INN.",
        "source": "extended_synthetic",
        "safe_context": "ИНН: <DIGITS_10>",
        "test_input": "ИНН: 4723456789",
        "expected_contains": ["ИНН: [INN_1]"],
        "expected_not_contains": ["4723456789", "[OCR_SUSPECT_INN_1]"],
        "expected_replacement_types": ["INN"],
        "expected_status": "VALID_ENTITY",
        "expected_policy_action": "MASK_CONFIDENTLY",
        "test_type": "valid_positive",
    },
    {
        "test_id": "test_ogrn_13_positive_001",
        "description": "ОГРН 13 цифр рядом с меткой ОГРН должен скрываться как OGRN.",
        "source": "extended_synthetic",
        "safe_context": "ОГРН: <OGRN_13>",
        "test_input": "ОГРН: 1027700132195",
        "expected_contains": ["ОГРН: [OGRN_1]"],
        "expected_not_contains": ["1027700132195"],
        "expected_replacement_types": ["OGRN"],
        "expected_status": "VALID_ENTITY",
        "expected_policy_action": "MASK_CONFIDENTLY",
        "test_type": "valid_positive",
    },
    {
        "test_id": "test_ogrnip_15_positive_001",
        "description": "ОГРНИП 15 цифр рядом с меткой ОГРНИП должен скрываться как OGRNIP.",
        "source": "extended_synthetic",
        "safe_context": "ОГРНИП: <OGRNIP_15>",
        "test_input": "ОГРНИП: 304500116000157",
        "expected_contains": ["ОГРНИП: [OGRNIP_1]"],
        "expected_not_contains": ["304500116000157"],
        "expected_replacement_types": ["OGRNIP"],
        "expected_status": "VALID_ENTITY",
        "expected_policy_action": "MASK_CONFIDENTLY",
        "test_type": "valid_positive",
    },
    {
        "test_id": "test_bik_9_positive_001",
        "description": "БИК 9 цифр рядом с меткой БИК должен скрываться как BIK.",
        "source": "extended_synthetic",
        "safe_context": "БИК: <BIK_9>",
        "test_input": "БИК: 044525225",
        "expected_contains": ["БИК: [BIK_1]"],
        "expected_not_contains": ["044525225"],
        "expected_replacement_types": ["BIK"],
        "expected_status": "VALID_ENTITY",
        "expected_policy_action": "MASK_CONFIDENTLY",
        "test_type": "valid_positive",
    },
    {
        "test_id": "test_account_20_positive_001",
        "description": "20-значная последовательность должна скрываться как ACCOUNT.",
        "source": "extended_synthetic",
        "safe_context": "Расчетный счет: <ACCOUNT_20>",
        "test_input": "Расчетный счет: 40702810900000000001",
        "expected_contains": ["Расчетный счет: [ACCOUNT_1]"],
        "expected_not_contains": ["40702810900000000001"],
        "expected_replacement_types": ["ACCOUNT"],
        "expected_status": "VALID_ENTITY",
        "expected_policy_action": "MASK_CONFIDENTLY",
        "test_type": "valid_positive",
    },
    {
        "test_id": "test_corr_account_20_positive_001",
        "description": "20-значный корреспондентский счет должен скрываться как ACCOUNT.",
        "source": "extended_synthetic",
        "safe_context": "Корреспондентский счет: <CORR_ACCOUNT_20>",
        "test_input": "Корреспондентский счет: 30101810400000000225",
        "expected_contains": ["Корреспондентский счет: [ACCOUNT_1]"],
        "expected_not_contains": ["30101810400000000225"],
        "expected_replacement_types": ["ACCOUNT"],
        "expected_status": "VALID_ENTITY",
        "expected_policy_action": "MASK_CONFIDENTLY",
        "test_type": "valid_positive",
    },
    {
        "test_id": "test_passport_plain_positive_001",
        "description": "Паспортная серия и номер в формате 1234 567890 должны скрываться как PASSPORT.",
        "source": "extended_synthetic",
        "safe_context": "Паспорт <PASSPORT_SERIES_NUMBER>",
        "test_input": "Паспорт 1234 567890",
        "expected_contains": ["Паспорт [PASSPORT_1]"],
        "expected_not_contains": ["1234 567890"],
        "expected_replacement_types": ["PASSPORT"],
        "expected_status": "VALID_ENTITY",
        "expected_policy_action": "MASK_CONFIDENTLY",
        "test_type": "valid_positive",
    },
    {
        "test_id": "test_appeal_number_13_digits_negative_001",
        "description": "13 цифр после 'Номер обращения' — служебный номер, не ИНН, не телефон и не карта.",
        "source": "extended_synthetic",
        "safe_context": "Номер обращения <DIGITS_13>",
        "test_input": "Номер обращения 4732547652143",
        "expected_contains": ["Номер обращения 4732547652143"],
        "expected_not_contains": ["[OCR_SUSPECT_INN_1]", "[INN_1]", "[PHONE_1]", "[CARD_1]"],
        "expected_replacement_types": [],
        "expected_status": "SKIPPED_BY_ALLOW",
        "expected_policy_action": "ALLOW",
        "test_type": "negative_allow",
    },
    {
        "test_id": "test_act_phone_like_negative_001",
        "description": "Номер акта, похожий на телефон, не должен скрываться как PHONE.",
        "source": "extended_synthetic",
        "safe_context": "АКТ № 89123451004",
        "test_input": "АКТ № 89123451004",
        "expected_contains": ["АКТ № 89123451004"],
        "expected_not_contains": ["[PHONE_1]", "[INN_1]", "[CARD_1]"],
        "expected_replacement_types": [],
        "expected_status": "SKIPPED_BY_ALLOW",
        "expected_policy_action": "ALLOW",
        "test_type": "negative_allow",
    },
    {
        "test_id": "test_certificate_phone_like_negative_001",
        "description": "Номер сертификата, похожий на телефон, не должен скрываться как PHONE.",
        "source": "extended_synthetic",
        "safe_context": "Сертификат: <PHONE_RU_SPACED>",
        "test_input": "Сертификат: 8 912 345 10 04",
        "expected_contains": ["Сертификат: 8 912 345 10 04"],
        "expected_not_contains": ["[PHONE_1]", "[INN_1]", "[CARD_1]"],
        "expected_replacement_types": [],
        "expected_status": "SKIPPED_BY_ALLOW",
        "expected_policy_action": "ALLOW",
        "test_type": "negative_allow",
    },
    {
        "test_id": "test_inn_spaced_known_gap_001",
        "description": "Known gap: ИНН с пробелами должен в будущем скрываться как INN, но текущий детектор может его не поддерживать.",
        "source": "extended_synthetic_known_gap",
        "safe_context": "ИНН: <INN_12_SPACED>",
        "test_input": "ИНН: 473 254 765 214",
        "expected_contains": ["ИНН: [INN_1]"],
        "expected_not_contains": ["473 254 765 214"],
        "expected_replacement_types": ["INN"],
        "expected_status": "VALID_ENTITY",
        "expected_policy_action": "MASK_CONFIDENTLY",
        "test_type": "known_gap",
        "expected_fail": True,
        "gap_reason": "Текущий строгий INN regex, вероятно, не поддерживает разделители внутри ИНН.",
    },
    {
        "test_id": "test_inn_ocr_letter_known_gap_001",
        "description": "Known gap: OCR-буква З вместо цифры 3 рядом с меткой ИНН должна в будущем попадать в suspect/review.",
        "source": "extended_synthetic_known_gap",
        "safe_context": "ИНН: <INN_12_OCR_LETTER>",
        "test_input": "ИНН: 47325476521З",
        "expected_contains": ["ИНН: [OCR_SUSPECT_INN_1]"],
        "expected_not_contains": ["47325476521З", "[INN_1]"],
        "expected_replacement_types": ["OCR_SUSPECT_INN"],
        "expected_status": "SUSPECT_ENTITY",
        "expected_policy_action": "MASK_AND_REVIEW",
        "test_type": "known_gap",
        "expected_fail": True,
        "gap_reason": "Нужен отдельный OCR-normalization/suspect слой для букв, похожих на цифры.",
    },
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
    tests = CORE_TESTS + (EXTENDED_TESTS if extended else [])
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
            f"Не найден {ANONYMIZER_PATH}. Положите run_regression_tests.py в корень проекта рядом с 1_anonymize.py."
        )
    spec = importlib.util.spec_from_file_location("anonymizer_under_test", ANONYMIZER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Не удалось загрузить 1_anonymize.py как модуль.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_one_test(anonymizer, case: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
    test_id = case.get("test_id", "unknown_test")
    raw_input = case.get("test_input") or case.get("input") or case.get("safe_context") or ""
    test_input = resolve_placeholders(str(raw_input))
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
            "test_id": test_id,
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
        "test_id": test_id,
        "description": case.get("description", ""),
        "passed": passed,
        "expected_fail": expected_fail,
        "outcome": outcome,
        "gap_reason": case.get("gap_reason", ""),
        "input": test_input,
        "output": output,
        "expected_status": case.get("expected_status", ""),
        "expected_policy_action": case.get("expected_policy_action", ""),
        "actual_replacements": file_report.get("replacements", []),
        "actual_skipped": file_report.get("skipped", []),
        "checks": checks,
    }


def run_tests(include_known_gaps_as_failures: bool = False) -> None:
    ensure_dirs()
    cases = read_jsonl(REGRESSION_CASES_PATH)
    if not cases:
        print("Нет regression cases. Сначала выполните: python run_regression_tests.py seed")
        return

    print("Загрузка текущего 1_anonymize.py для тестов...")
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
    elif command == "status":
        show_status()
    else:
        print("Команды:")
        print("  python run_regression_tests.py seed")
        print("  python run_regression_tests.py seed-extended")
        print("  python run_regression_tests.py run")
        print("  python run_regression_tests.py run-strict")
        print("  python run_regression_tests.py status")


if __name__ == "__main__":
    main()
