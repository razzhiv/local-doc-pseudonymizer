from __future__ import annotations

import pseudonymize
from examples.golden_demo.create_demo_docx import build_demo_docx
from html_review_report import build_html_review_report, write_html_review_report


def basic_rules() -> dict:
    return {
        "manual_hide": [],
        "manual_allow": [],
        "public_orgs": [],
        "private_org_markers": [],
    }


def configure_isolated_runtime(tmp_path, monkeypatch) -> None:
    output_dir = tmp_path / "output"
    anon_dir = output_dir / "anonymized"
    reports_dir = output_dir / "reports"
    feedback_dir = tmp_path / "feedback"

    anon_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    feedback_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(pseudonymize, "OUTPUT_DIR", str(output_dir))
    monkeypatch.setattr(pseudonymize, "ANON_DIR", str(anon_dir))
    monkeypatch.setattr(pseudonymize, "REPORTS_DIR", str(reports_dir))
    monkeypatch.setattr(pseudonymize, "FEEDBACK_DIR", str(feedback_dir))
    monkeypatch.setattr(pseudonymize, "FEEDBACK_CASES_PATH", str(feedback_dir / "cases.jsonl"))


def test_html_review_report_generated_from_golden_synthetic_demo(tmp_path, monkeypatch):
    configure_isolated_runtime(tmp_path, monkeypatch)

    source_docx = build_demo_docx(tmp_path / "golden_synthetic_client_matter.docx")
    project_dictionary = pseudonymize.empty_project_dictionary()
    file_report, _ = pseudonymize.process_docx(
        str(source_docx),
        source_docx.name,
        project_dictionary,
        basic_rules(),
    )

    report = {"files": {source_docx.name: file_report}}
    html_path = write_html_review_report(
        report,
        tmp_path / "output" / "reports" / "review_report_demo.html",
        project_dictionary=project_dictionary,
        generated_at="2026-06-01 12:00:00",
    )
    html = html_path.read_text(encoding="utf-8")

    assert html_path.exists()
    assert '<html lang="ru">' in html
    assert "BeforeSending — отчёт проверки документа" in html
    assert "Важное предупреждение" in html
    assert "снижает риск раскрытия данных" in html
    assert "Краткая сводка" in html
    assert "Категории найденных данных" in html
    assert "Найденные замены" in html
    assert "Что требует ручной проверки" in html
    assert "Пропущенные / skipped findings" in html
    assert "Чеклист перед отправкой" in html
    assert "Безопасная очистка локальных артефактов" in html
    assert "Ограничения" in html
    assert "Техническая информация" in html
    assert "ФИО / персона (PERSON)" in html
    assert "ИНН (INN)" in html
    assert "[INN_1]" in html


def test_html_review_report_has_no_external_network_resources():
    html = build_html_review_report(
        {
            "files": {
                "synthetic.docx": {
                    "summary": {"EMAIL": 1},
                    "status": "processed",
                    "warnings": [],
                    "replacements": [
                        {
                            "file": "synthetic.docx",
                            "block": "paragraph_1",
                            "type": "EMAIL",
                            "original": "case@example.test",
                            "token": "[EMAIL_1]",
                            "method": "regex_email",
                        }
                    ],
                    "skipped": [],
                    "review_cases": [],
                }
            }
        },
        project_dictionary={"tokens": {"[EMAIL_1]": {"type": "EMAIL", "value": "case@example.test"}}},
        generated_at="2026-06-01 12:00:00",
    )
    lower = html.lower()

    assert "Email / электронная почта (EMAIL)" in html
    assert "Подозрительных или спорных кейсов для ручной проверки нет." in html
    assert "Пропущенные находки не записаны." in html
    assert "Предупреждений обработки нет." in html

    for forbidden in ["http://", "https://", "<script", "<link", "@import", "url(", " href=", " src="]:
        assert forbidden not in lower


def test_html_review_report_escapes_special_values():
    unsafe_value = "<script>alert(\"x\")</script> & case@example.test"
    html = build_html_review_report(
        {
            "files": {
                "demo<unsafe>.docx": {
                    "summary": {"EMAIL": 1},
                    "status": "processed",
                    "warnings": ["Check <warning> & confirm"],
                    "replacements": [
                        {
                            "file": "demo<unsafe>.docx",
                            "block": "paragraph_1",
                            "type": "EMAIL",
                            "original": unsafe_value,
                            "token": "[EMAIL_1]",
                            "method": "manual<&>",
                            "comment": "quoted \"value\"",
                        }
                    ],
                    "skipped": [],
                    "review_cases": [],
                }
            }
        },
        project_dictionary={"tokens": {"[EMAIL_1]": {"type": "EMAIL", "value": unsafe_value}}},
        generated_at="2026-06-01 12:00:00",
    )

    assert unsafe_value not in html
    assert "demo&lt;unsafe&gt;.docx" in html
    assert "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt; &amp; case@example.test" in html
    assert "manual&lt;&amp;&gt;" in html
    assert "Check &lt;warning&gt; &amp; confirm" in html
