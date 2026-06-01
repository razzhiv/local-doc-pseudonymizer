from __future__ import annotations

import json

from quality_metrics import (
    build_quality_metrics_markdown,
    build_quality_metrics_payload,
    get_case_category_ids,
    write_quality_metrics_reports,
)


def test_quality_metrics_aggregates_stable_json_categories():
    regression_payload = {
        "created_at": "2026-06-01T12:00:00",
        "total": 3,
        "pass": 1,
        "fail": 1,
        "xfail": 1,
        "xpass": 0,
        "error": 0,
        "blocking_failed": 2,
        "results": [
            {
                "test_id": "custom_inn_positive",
                "outcome": "PASS",
                "passed": True,
                "test_type": "valid_positive",
                "category_ids": ["inn"],
                "expected_replacement_types": ["INN"],
                "checks": [],
            },
            {
                "test_id": "custom_contract_negative",
                "outcome": "FAIL",
                "passed": False,
                "test_type": "negative_allow",
                "category_ids": ["contract_numbers_negative", "inn"],
                "expected_replacement_types": [],
                "filename": "synthetic_regression.txt",
                "checks": [
                    {
                        "check": "expected_not_contains",
                        "value": "[INN_1]",
                        "ok": False,
                    }
                ],
                "input": "synthetic input should not be copied to metrics failures",
                "output": "synthetic output should not be copied to metrics failures",
            },
            {
                "test_id": "custom_birth_date_gap",
                "outcome": "XFAIL",
                "passed": False,
                "expected_fail": True,
                "gap_reason": "synthetic gap",
                "test_type": "valid_positive",
                "category_ids": ["birth_or_sensitive_dates"],
                "expected_replacement_types": ["DATE_BIRTH"],
                "checks": [
                    {
                        "check": "expected_replacement_type",
                        "value": "DATE_BIRTH",
                        "actual": [],
                        "ok": False,
                    }
                ],
            },
        ],
    }

    metrics = build_quality_metrics_payload(
        regression_payload,
        generated_at="2026-06-01T12:01:00",
        source_results_path="expected/regression_last_results.json",
    )

    assert metrics["schema_version"] == 1
    assert metrics["report_type"] == "quality_metrics"
    assert metrics["source_results_path"] == "expected/regression_last_results.json"
    assert metrics["corpus"]["synthetic_only"] is True
    assert metrics["summary"]["total_cases"] == 3
    assert metrics["summary"]["passed_cases"] == 1
    assert metrics["summary"]["failed_cases"] == 2
    assert metrics["summary"]["success_rate"] == 0.3333

    categories = {item["id"]: item for item in metrics["categories"]}
    assert categories["inn"]["display_name_ru"] == "ИНН"
    assert categories["inn"]["total_cases"] == 2
    assert categories["inn"]["passed_cases"] == 1
    assert categories["inn"]["failed_cases"] == 1
    assert categories["inn"]["positive_cases"] == 1
    assert categories["inn"]["negative_cases"] == 1
    assert categories["contract_numbers_negative"]["total_cases"] == 1
    assert categories["birth_or_sensitive_dates"]["total_cases"] == 1

    assert len(metrics["failures"]) == 2
    assert "input" not in metrics["failures"][0]
    assert "output" not in metrics["failures"][0]
    assert metrics["failures"][0]["expected"] == "output does not contain `[INN_1]`"
    assert metrics["failures"][0]["actual"] == "present_in_output"
    assert metrics["known_gaps"] == [
        {
            "test_id": "custom_birth_date_gap",
            "category_ids": ["birth_or_sensitive_dates"],
            "outcome": "XFAIL",
            "gap_reason": "synthetic gap",
        }
    ]


def test_quality_metrics_category_derivation_is_explicit_and_extensible():
    assert get_case_category_ids(
        {
            "test_id": "test_en_phone_context_positive_001",
            "source": "sprint_1_2_english_minimal_profile",
            "test_type": "valid_positive",
            "expected_replacement_types": ["PHONE"],
        }
    ) == ["phone", "english_minimal"]

    assert get_case_category_ids(
        {
            "test_id": "test_public_authority_court_case_negative_001",
            "test_type": "negative_allow",
            "expected_replacement_types": [],
        }
    ) == ["public_authorities_negative", "case_numbers_negative"]

    assert get_case_category_ids(
        {
            "test_id": "future_case",
            "category_ids": ["pdf_text_layer"],
        }
    ) == ["pdf_text_layer"]


def test_quality_metrics_markdown_is_russian_first_without_failures():
    metrics = build_quality_metrics_payload(
        {
            "created_at": "2026-06-01T12:00:00",
            "total": 1,
            "pass": 1,
            "fail": 0,
            "xfail": 0,
            "xpass": 0,
            "error": 0,
            "blocking_failed": 0,
            "results": [
                {
                    "test_id": "custom_passport_positive",
                    "outcome": "PASS",
                    "passed": True,
                    "test_type": "valid_positive",
                    "category_ids": ["passport"],
                    "expected_replacement_types": ["PASSPORT"],
                    "checks": [],
                }
            ],
        },
        generated_at="2026-06-01T12:02:00",
    )

    markdown = build_quality_metrics_markdown(metrics)

    assert markdown.startswith("# Отчёт о качестве синтетической регрессии")
    assert "## Краткая сводка" in markdown
    assert "* Корпус: только синтетические данные" in markdown
    assert "Категории могут пересекаться" in markdown
    assert "сумма значений в колонке «Кейсов в категории» может быть выше" in markdown
    assert "| Категория | ID категории | Кейсов в категории | Успешно | С ошибками | Требуется маскирование | Не должно маскироваться | Доля успешных |" in markdown
    assert "| PDF с текстовым слоем | `pdf_text_layer` | 0 | 0 | 0 | 0 | 0 | н/д |" in markdown
    assert "Минимальный англоязычный профиль" in markdown
    assert "Ошибок не обнаружено." in markdown
    assert "## Известные пробелы" in markdown
    assert "Известных пробелов не отмечено в этом запуске." in markdown
    assert "инженерная оценка качества" in markdown
    assert "показателем соответствия требованиям" in markdown
    assert "пропуски распознавания невозможны" in markdown
    assert "не является гарантией анонимизации" in markdown
    assert "только по синтетическим тестам" in markdown
    assert "Positive" not in markdown
    assert "Negative" not in markdown
    assert "Known gaps" not in markdown
    assert "compliance score" not in markdown
    assert "false negative" not in markdown


def test_quality_metrics_reports_are_written_as_utf8_latest_files(tmp_path):
    regression_payload = {
        "created_at": "2026-06-01T12:00:00",
        "total": 1,
        "pass": 1,
        "fail": 0,
        "xfail": 0,
        "xpass": 0,
        "error": 0,
        "blocking_failed": 0,
        "results": [
            {
                "test_id": "custom_address_positive",
                "outcome": "PASS",
                "passed": True,
                "test_type": "valid_positive",
                "category_ids": ["address"],
                "expected_replacement_types": ["ADDRESS_DETAIL"],
                "checks": [],
            }
        ],
    }

    paths = write_quality_metrics_reports(
        regression_payload,
        tmp_path,
        generated_at="2026-06-01T12:03:00",
        timestamp="2026-06-01_12-03-00",
        source_results_path="expected/regression_last_results.json",
    )

    assert paths["json"].name == "quality_metrics_2026-06-01_12-03-00.json"
    assert paths["json_latest"].name == "quality_metrics_latest.json"
    assert paths["markdown"].name == "quality_metrics_2026-06-01_12-03-00.md"
    assert paths["markdown_latest"].name == "quality_metrics_latest.md"

    payload = json.loads(paths["json_latest"].read_text(encoding="utf-8"))
    assert payload["categories"][0]["display_name_ru"] == "Паспортные данные"
    assert payload["summary"]["success_rate"] == 1.0
    markdown = paths["markdown_latest"].read_text(encoding="utf-8")
    assert "Отчёт о качестве синтетической регрессии" in markdown
    assert "Кейсов в категории" in markdown
