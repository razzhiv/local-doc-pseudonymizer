from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


CATEGORY_DEFINITIONS: list[dict[str, str]] = [
    {
        "id": "passport",
        "display_name_ru": "Паспортные данные",
        "description_ru": "Паспортные номера, коды подразделений и связанные паспортные даты.",
    },
    {
        "id": "inn",
        "display_name_ru": "ИНН",
        "description_ru": "ИНН, подозрительные значения и варианты с OCR-искажениями.",
    },
    {
        "id": "snils",
        "display_name_ru": "СНИЛС",
        "description_ru": "СНИЛС и его синтетические форматные варианты.",
    },
    {
        "id": "ogrn",
        "display_name_ru": "ОГРН",
        "description_ru": "ОГРН юридических лиц.",
    },
    {
        "id": "ogrnip",
        "display_name_ru": "ОГРНИП",
        "description_ru": "ОГРНИП индивидуальных предпринимателей.",
    },
    {
        "id": "kpp",
        "display_name_ru": "КПП",
        "description_ru": "Коды постановки на учет.",
    },
    {
        "id": "bank_details",
        "display_name_ru": "Банковские реквизиты",
        "description_ru": "Расчетные счета, корреспондентские счета и БИК.",
    },
    {
        "id": "phone",
        "display_name_ru": "Телефоны",
        "description_ru": "Телефонные номера и проверки похожих служебных номеров, которые не должны маскироваться.",
    },
    {
        "id": "address",
        "display_name_ru": "Адреса",
        "description_ru": "Адресные детали и почтовые индексы.",
    },
    {
        "id": "birth_or_sensitive_dates",
        "display_name_ru": "Даты рождения и чувствительные даты",
        "description_ru": "Даты рождения, выдачи документов и регистрационные даты.",
    },
    {
        "id": "general_dates_negative",
        "display_name_ru": "Обычные даты: не маскировать",
        "description_ru": "Проверки, где обычные даты не должны маскироваться.",
    },
    {
        "id": "persons",
        "display_name_ru": "Физические лица",
        "description_ru": "ФИО и персональные имена в синтетических кейсах.",
    },
    {
        "id": "private_orgs",
        "display_name_ru": "Частные организации",
        "description_ru": "Синтетические названия коммерческих организаций и ИП-контекст.",
    },
    {
        "id": "public_authorities_negative",
        "display_name_ru": "Публичные органы: не маскировать",
        "description_ru": "Проверки для судов, ИФНС и других публичных органов, которые должны оставаться видимыми.",
    },
    {
        "id": "contract_numbers_negative",
        "display_name_ru": "Договорные и служебные номера: не маскировать",
        "description_ru": "Проверки для номеров актов, договоров, обращений, справок и UID, которые не должны маскироваться.",
    },
    {
        "id": "case_numbers_negative",
        "display_name_ru": "Судебные номера дел: не маскировать",
        "description_ru": "Проверки для номеров судебных дел и похожих ссылочных номеров, которые должны оставаться видимыми.",
    },
    {
        "id": "english_minimal",
        "display_name_ru": "Минимальный англоязычный профиль",
        "description_ru": "Минимальный англоязычный профиль по явным текстовым меткам.",
    },
    {
        "id": "docx_tables_or_structure",
        "display_name_ru": "DOCX таблицы и структура",
        "description_ru": "Кейсы, связанные с табличными/структурными контекстами DOCX.",
    },
    {
        "id": "pdf_text_layer",
        "display_name_ru": "PDF с текстовым слоем",
        "description_ru": "Кейсы, связанные с PDF, где доступен извлекаемый текстовый слой.",
    },
]

CATEGORY_IDS = tuple(item["id"] for item in CATEGORY_DEFINITIONS)
CATEGORY_ID_SET = set(CATEGORY_IDS)
CATEGORY_ORDER = {category_id: index for index, category_id in enumerate(CATEGORY_IDS)}

ENTITY_CATEGORY_IDS: dict[str, tuple[str, ...]] = {
    "PASSPORT": ("passport",),
    "DIVISION_CODE": ("passport",),
    "INN": ("inn",),
    "OCR_SUSPECT_INN": ("inn",),
    "SNILS": ("snils",),
    "OGRN": ("ogrn",),
    "OGRNIP": ("ogrnip",),
    "KPP": ("kpp",),
    "ACCOUNT": ("bank_details",),
    "BIK": ("bank_details",),
    "PHONE": ("phone",),
    "POST_INDEX": ("address",),
    "ADDRESS_DETAIL": ("address",),
    "DATE_BIRTH": ("birth_or_sensitive_dates",),
    "DATE_DOC_ISSUE": ("passport", "birth_or_sensitive_dates"),
    "DATE_REGISTRATION": ("birth_or_sensitive_dates",),
    "PERSON": ("persons",),
    "ORG_PRIVATE": ("private_orgs",),
}

SPECIFIC_TEST_CATEGORY_IDS: dict[str, tuple[str, ...]] = {
    "test_act_13_digits_negative_001": ("contract_numbers_negative", "inn", "phone"),
    "test_certificate_13_digits_negative_001": ("contract_numbers_negative", "inn", "phone"),
    "test_appeal_number_13_digits_negative_001": ("contract_numbers_negative", "inn"),
    "test_act_phone_like_negative_001": ("contract_numbers_negative", "phone"),
    "test_certificate_phone_like_negative_001": ("contract_numbers_negative", "phone"),
    "test_passport_service_number_negative_001": ("contract_numbers_negative", "passport"),
    "test_act_phone_like_11_digits_negative_001": ("contract_numbers_negative", "phone"),
    "test_certificate_phone_like_plus7_negative_001": ("contract_numbers_negative", "phone"),
    "test_appeal_phone_like_negative_001": ("contract_numbers_negative", "phone"),
    "test_contract_date_negative_001": ("contract_numbers_negative", "general_dates_negative"),
    "test_public_org_ifns_negative_001": ("public_authorities_negative",),
    "test_uid_20_digits_negative_001": ("contract_numbers_negative", "bank_details"),
    "test_act_spaced_inn_like_negative_001": ("contract_numbers_negative", "inn"),
    "test_certificate_spaced_inn_like_negative_001": ("contract_numbers_negative", "inn"),
    "test_appeal_spaced_inn_like_negative_001": ("contract_numbers_negative", "inn"),
    "test_act_ocr_letter_inn_like_negative_001": ("contract_numbers_negative", "inn"),
    "test_certificate_ocr_letter_inn_like_negative_001": ("contract_numbers_negative", "inn"),
    "test_public_authority_court_case_negative_001": (
        "public_authorities_negative",
        "case_numbers_negative",
    ),
    "test_contract_number_slash_negative_001": (
        "contract_numbers_negative",
        "inn",
        "phone",
        "passport",
    ),
    "test_reference_passport_like_number_negative_001": (
        "contract_numbers_negative",
        "passport",
    ),
    "test_table_like_labels_compact_positive_001": ("docx_tables_or_structure",),
}

NEGATIVE_CONTRACT_NUMBER_KEYWORDS = (
    "act_",
    "certificate_",
    "appeal_",
    "contract_number",
    "service_number",
    "uid_",
    "reference_",
)


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return list(value)
    return [value]


def _unique_in_category_order(category_ids: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for category_id in category_ids:
        if category_id not in CATEGORY_ID_SET or category_id in seen:
            continue
        seen.add(category_id)
        result.append(category_id)
    return sorted(result, key=lambda item: CATEGORY_ORDER[item])


def get_case_category_ids(case_or_result: dict[str, Any]) -> list[str]:
    """Return stable category IDs for a synthetic regression case/result."""
    explicit = case_or_result.get("category_ids")
    if explicit is None and case_or_result.get("category_id"):
        explicit = [case_or_result.get("category_id")]
    if explicit is not None:
        return _unique_in_category_order(str(item) for item in _as_list(explicit))

    category_ids: list[str] = []
    test_id = str(case_or_result.get("test_id", ""))
    test_id_lower = test_id.lower()

    for entity_type in _as_list(case_or_result.get("expected_replacement_types")):
        category_ids.extend(ENTITY_CATEGORY_IDS.get(str(entity_type), ()))

    source = str(case_or_result.get("source", ""))
    if source == "sprint_1_2_english_minimal_profile":
        category_ids.append("english_minimal")

    category_ids.extend(SPECIFIC_TEST_CATEGORY_IDS.get(test_id, ()))

    if "public_authority" in test_id_lower or "public_org" in test_id_lower or "ifns" in test_id_lower:
        category_ids.append("public_authorities_negative")

    if "court_case" in test_id_lower or "case_number" in test_id_lower:
        category_ids.append("case_numbers_negative")

    test_type = str(case_or_result.get("test_type", ""))
    if test_type.startswith("negative"):
        if any(keyword in test_id_lower for keyword in NEGATIVE_CONTRACT_NUMBER_KEYWORDS):
            category_ids.append("contract_numbers_negative")
        if "date" in test_id_lower:
            category_ids.append("general_dates_negative")
        if "phone" in test_id_lower or "plus7" in test_id_lower:
            category_ids.append("phone")
        if "inn" in test_id_lower or "13_digits" in test_id_lower:
            category_ids.append("inn")
        if "passport" in test_id_lower:
            category_ids.append("passport")
        if "20_digits" in test_id_lower or "account" in test_id_lower or "uid_" in test_id_lower:
            category_ids.append("bank_details")

    return _unique_in_category_order(category_ids)


def _is_negative_case(result: dict[str, Any]) -> bool:
    test_type = str(result.get("test_type", ""))
    if test_type.startswith("negative"):
        return True
    return result.get("expected_replacement_types") == []


def _is_success(result: dict[str, Any]) -> bool:
    return str(result.get("outcome", "")).upper() == "PASS"


def _rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator, 4)


def _percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def _category_percent(category: dict[str, Any]) -> str:
    if int(category.get("total_cases", 0)) == 0:
        return "н/д"
    return _percent(float(category.get("success_rate", 0.0)))


def _short(value: Any, limit: int = 180) -> str:
    text = str(value).replace("\r", " ").replace("\n", " ").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _summarize_failed_check(check: dict[str, Any]) -> dict[str, str]:
    check_name = str(check.get("check", "unknown_check"))
    value = _short(check.get("value", ""))
    actual = check.get("actual")

    if check_name == "expected_contains":
        return {
            "check": check_name,
            "expected": f"output contains `{value}`",
            "actual": "missing_from_output",
        }
    if check_name == "expected_not_contains":
        return {
            "check": check_name,
            "expected": f"output does not contain `{value}`",
            "actual": "present_in_output",
        }
    if check_name == "expected_replacement_type":
        return {
            "check": check_name,
            "expected": f"replacement type `{value}`",
            "actual": _short(actual),
        }
    if check_name == "expected_no_replacements":
        return {
            "check": check_name,
            "expected": "no replacements",
            "actual": _short(actual),
        }
    if check_name == "expected_skipped_reason":
        return {
            "check": check_name,
            "expected": f"skipped reason `{value}`",
            "actual": _short(actual),
        }
    return {
        "check": check_name,
        "expected": value or check_name,
        "actual": _short(actual),
    }


def _build_failure_entry(result: dict[str, Any]) -> dict[str, Any]:
    failed_checks = [
        _summarize_failed_check(check)
        for check in result.get("checks", [])
        if not check.get("ok")
    ]
    if result.get("error") and not failed_checks:
        failed_checks.append(
            {
                "check": "exception",
                "expected": "synthetic case completes without exception",
                "actual": _short(result.get("error")),
            }
        )

    expected = "; ".join(item["expected"] for item in failed_checks) or "PASS"
    actual = "; ".join(item["actual"] for item in failed_checks) or str(result.get("outcome", "UNKNOWN"))

    return {
        "test_id": result.get("test_id", "unknown_test"),
        "filename": result.get("filename", "synthetic_regression.txt"),
        "category_ids": get_case_category_ids(result),
        "outcome": str(result.get("outcome", "UNKNOWN")),
        "expected": expected,
        "actual": actual,
        "failed_checks": failed_checks,
    }


def build_quality_metrics_payload(
    regression_payload: dict[str, Any],
    *,
    generated_at: str | None = None,
    source_results_path: str | Path | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now().isoformat(timespec="seconds")
    results = list(regression_payload.get("results", []))
    category_stats: dict[str, dict[str, Any]] = {}
    uncategorized_cases: list[str] = []

    for category in CATEGORY_DEFINITIONS:
        category_stats[category["id"]] = {
            "id": category["id"],
            "display_name_ru": category["display_name_ru"],
            "description_ru": category["description_ru"],
            "total_cases": 0,
            "passed_cases": 0,
            "failed_cases": 0,
            "positive_cases": 0,
            "negative_cases": 0,
            "success_rate": 0.0,
        }

    for result in results:
        category_ids = get_case_category_ids(result)
        if not category_ids:
            uncategorized_cases.append(str(result.get("test_id", "unknown_test")))
            continue

        success = _is_success(result)
        negative_case = _is_negative_case(result)
        for category_id in category_ids:
            stats = category_stats[category_id]
            stats["total_cases"] += 1
            if success:
                stats["passed_cases"] += 1
            else:
                stats["failed_cases"] += 1
            if negative_case:
                stats["negative_cases"] += 1
            else:
                stats["positive_cases"] += 1

    for stats in category_stats.values():
        stats["success_rate"] = _rate(stats["passed_cases"], stats["total_cases"])

    passed_cases = sum(1 for result in results if _is_success(result))
    failed_cases = len(results) - passed_cases
    outcome_counts = Counter(str(result.get("outcome", "")).upper() for result in results)
    failures = [_build_failure_entry(result) for result in results if not _is_success(result)]
    known_gaps = [
        {
            "test_id": result.get("test_id", "unknown_test"),
            "category_ids": get_case_category_ids(result),
            "outcome": str(result.get("outcome", "UNKNOWN")),
            "gap_reason": result.get("gap_reason", ""),
        }
        for result in results
        if result.get("expected_fail") or str(result.get("outcome", "")).upper() in {"XFAIL", "XPASS"}
    ]

    source_path = str(source_results_path) if source_results_path is not None else ""
    return {
        "schema_version": 1,
        "report_type": "quality_metrics",
        "generated_at": generated_at,
        "source_results_path": source_path,
        "corpus": {
            "id": "synthetic_regression",
            "display_name": "Synthetic regression corpus",
            "synthetic_only": True,
        },
        "summary": {
            "total_cases": len(results),
            "passed_cases": passed_cases,
            "failed_cases": failed_cases,
            "success_rate": _rate(passed_cases, len(results)),
            "pass": int(regression_payload.get("pass", outcome_counts.get("PASS", 0))),
            "fail": int(regression_payload.get("fail", outcome_counts.get("FAIL", 0))),
            "xfail": int(regression_payload.get("xfail", outcome_counts.get("XFAIL", 0))),
            "xpass": int(regression_payload.get("xpass", outcome_counts.get("XPASS", 0))),
            "error": int(regression_payload.get("error", outcome_counts.get("ERROR", 0))),
            "blocking_failed": int(regression_payload.get("blocking_failed", failed_cases)),
        },
        "categories": [category_stats[category_id] for category_id in CATEGORY_IDS],
        "failures": failures,
        "known_gaps": known_gaps,
        "uncategorized_cases": uncategorized_cases,
        "security": {
            "synthetic_only_required": True,
            "must_not_include_real_documents": True,
            "must_not_include_real_pii": True,
            "must_not_include_token_dictionaries": True,
            "must_not_include_runtime_artifacts_from_real_data": True,
        },
        "limitations": {
            "engineering_visibility_only": True,
            "not_compliance_score": True,
            "not_anonymization_guarantee": True,
            "false_negatives_still_possible": True,
        },
    }


def _md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", "<br>")


def build_quality_metrics_markdown(metrics: dict[str, Any]) -> str:
    summary = metrics.get("summary", {})
    lines: list[str] = []

    lines.append("# Отчёт о качестве синтетической регрессии")
    lines.append("")
    lines.append("## Краткая сводка")
    lines.append("")
    lines.append(f"* Всего уникальных тестовых кейсов: {summary.get('total_cases', 0)}")
    lines.append(f"* Успешно: {summary.get('passed_cases', 0)}")
    lines.append(f"* С ошибками: {summary.get('failed_cases', 0)}")
    lines.append(f"* Доля успешных: {_percent(float(summary.get('success_rate', 0.0)))}")
    lines.append(f"* Дата формирования: {metrics.get('generated_at', '')}")
    lines.append("* Корпус: только синтетические данные")
    lines.append("")

    lines.append("## Категории качества")
    lines.append("")
    lines.append(
        "Категории могут пересекаться: один синтетический кейс может относиться сразу к нескольким категориям. "
        "Поэтому сумма значений в колонке «Кейсов в категории» может быть выше общего числа уникальных тестовых кейсов."
    )
    lines.append("")
    lines.append("| Категория | ID категории | Кейсов в категории | Успешно | С ошибками | Требуется маскирование | Не должно маскироваться | Доля успешных |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for category in metrics.get("categories", []):
        lines.append(
            "| "
            f"{_md_escape(category.get('display_name_ru', ''))} | "
            f"`{_md_escape(category.get('id', ''))}` | "
            f"{category.get('total_cases', 0)} | "
            f"{category.get('passed_cases', 0)} | "
            f"{category.get('failed_cases', 0)} | "
            f"{category.get('positive_cases', 0)} | "
            f"{category.get('negative_cases', 0)} | "
            f"{_category_percent(category)} |"
        )
    lines.append("")

    lines.append("## Ошибки")
    lines.append("")
    failures = metrics.get("failures", [])
    if not failures:
        lines.append("Ошибок не обнаружено.")
    else:
        for failure in failures:
            category_ids = ", ".join(f"`{item}`" for item in failure.get("category_ids", [])) or "нет категории"
            lines.append(
                "- "
                f"`{_md_escape(failure.get('test_id', 'unknown_test'))}`; "
                f"файл: `{_md_escape(failure.get('filename', ''))}`; "
                f"категории: {category_ids}; "
                f"статус: `{_md_escape(failure.get('outcome', 'UNKNOWN'))}`; "
                f"ожидалось: {_md_escape(failure.get('expected', ''))}; "
                f"получено: {_md_escape(failure.get('actual', ''))}."
            )
    lines.append("")

    lines.append("## Известные пробелы")
    lines.append("")
    known_gaps = metrics.get("known_gaps", [])
    if not known_gaps:
        lines.append("Известных пробелов не отмечено в этом запуске.")
    else:
        for gap in known_gaps:
            category_ids = ", ".join(f"`{item}`" for item in gap.get("category_ids", [])) or "нет категории"
            reason = gap.get("gap_reason") or "причина не указана"
            lines.append(
                "- "
                f"`{_md_escape(gap.get('test_id', 'unknown_test'))}`; "
                f"категории: {category_ids}; "
                f"статус: `{_md_escape(gap.get('outcome', 'UNKNOWN'))}`; "
                f"причина: {_md_escape(reason)}."
            )
    lines.append("")

    lines.append("## Ограничения")
    lines.append("")
    lines.append(
        "Это инженерная оценка качества по синтетической регрессии. "
        "Она помогает видеть покрытие и ошибки по категориям, но не является гарантией анонимизации, "
        "показателем соответствия требованиям, юридическим заключением или доказательством того, "
        "что пропуски распознавания невозможны."
    )
    lines.append("")

    lines.append("## Безопасность")
    lines.append("")
    lines.append(
        "Формируйте этот отчёт только по синтетическим тестам. "
        "Не включайте реальные документы, реальные персональные данные, "
        "словари токенов или рабочие артефакты, полученные из реальных данных."
    )
    lines.append("")

    return "\n".join(lines)


def write_quality_metrics_reports(
    regression_payload: dict[str, Any],
    reports_dir: str | Path,
    *,
    generated_at: str | None = None,
    timestamp: str | None = None,
    source_results_path: str | Path | None = None,
) -> dict[str, Path]:
    now = datetime.now()
    generated_at = generated_at or now.isoformat(timespec="seconds")
    timestamp = timestamp or now.strftime("%Y-%m-%d_%H-%M-%S")
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)

    metrics = build_quality_metrics_payload(
        regression_payload,
        generated_at=generated_at,
        source_results_path=source_results_path,
    )
    markdown = build_quality_metrics_markdown(metrics)

    json_path = reports_path / f"quality_metrics_{timestamp}.json"
    latest_json_path = reports_path / "quality_metrics_latest.json"
    markdown_path = reports_path / f"quality_metrics_{timestamp}.md"
    latest_markdown_path = reports_path / "quality_metrics_latest.md"

    json_text = json.dumps(metrics, ensure_ascii=False, indent=2)
    json_path.write_text(json_text + "\n", encoding="utf-8")
    latest_json_path.write_text(json_text + "\n", encoding="utf-8")
    markdown_path.write_text(markdown, encoding="utf-8")
    latest_markdown_path.write_text(markdown, encoding="utf-8")

    return {
        "json": json_path,
        "json_latest": latest_json_path,
        "markdown": markdown_path,
        "markdown_latest": latest_markdown_path,
    }
