from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any


CATEGORY_LABELS = {
    "ACCOUNT": "Банковский счёт",
    "ADDRESS_DETAIL": "Адрес / часть адреса",
    "BIK": "БИК",
    "CADASTRAL": "Кадастровый номер",
    "CARD": "Банковская карта",
    "COORDS": "Координаты",
    "COURT_CASE": "Судебное дело",
    "COURT_MATERIAL": "Судебный материал",
    "COURT_UID": "Судебный идентификатор",
    "DATE_BIRTH": "Дата рождения",
    "DATE_DOC_ISSUE": "Дата выдачи документа",
    "DATE_REGISTRATION": "Дата регистрации",
    "DIVISION_CODE": "Код подразделения",
    "EMAIL": "Email / электронная почта",
    "INN": "ИНН",
    "KPP": "КПП",
    "MEDICAL_DATE": "Медицинская дата",
    "MESSENGER_LINK": "Ссылка на мессенджер",
    "OCR_SUSPECT_INN": "Подозрение на ИНН с OCR-ошибкой",
    "OGRN": "ОГРН",
    "OGRNIP": "ОГРНИП",
    "ORG": "Организация",
    "ORG_PRIVATE": "Частная организация",
    "PASSPORT": "Паспорт",
    "PERSON": "ФИО / персона",
    "PHONE": "Телефон",
    "POST_INDEX": "Почтовый индекс",
    "SNILS": "СНИЛС",
    "TEXT": "Текст",
    "TRACK": "Трек-номер",
    "USERNAME": "Имя пользователя",
}

FILE_STATUS_LABELS = {
    "processed": "Обработан",
    "processed_text_layer": "Обработан текстовый слой",
    "partially_processed_text_layer": "Частично обработан текстовый слой",
    "not_processed_no_text_layer": "Не обработан: нет текстового слоя",
    "processing_error": "Ошибка обработки",
    "pending": "Ожидает обработки",
}

FINDING_STATUS_LABELS = {
    "VALID_ENTITY": "Автоматически замаскировано",
    "SUSPECT_ENTITY": "Замаскировано, нужна проверка",
    "NEEDS_REVIEW": "Нужна ручная проверка",
    "MANUAL_CONFIRMED": "Подтверждено ручным правилом",
}

POLICY_ACTION_LABELS = {
    "ALLOW": "Оставить без замены",
    "MASK_AND_REVIEW": "Замаскировать и проверить",
    "MASK_CONFIDENTLY": "Замаскировать",
    "REVIEW_ONLY": "Только проверить",
}

RECOMMENDED_DECISION_LABELS = {
    "accept": "Принять",
    "add_to_manual_allow": "Добавить в разрешения",
    "add_to_manual_hide": "Добавить в ручное скрытие",
    "create_candidate_rule": "Создать кандидатное правило",
    "expand_valid_inn_to_13_digits": "Проверить идею расширения правила ИНН",
    "hide_as_suspect": "Оставить скрытым как подозрительное",
    "hide_once": "Скрыть один раз",
    "leave_unmasked": "Оставить без маскирования",
    "reject_case": "Отклонить кейс",
}

SKIP_REASON_LABELS = {
    "inside_long_digit_sequence": "Внутри длинной цифровой последовательности",
    "manual_allow_org_context": "Контекст организации есть в разрешениях",
    "manual_allow_text": "Текст найден в ручных разрешениях",
    "non_card_document_number_context": "Похоже на номер документа, не карту",
    "service_number_context": "Служебный номер по контексту",
}


def _text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _html(value: Any, default: str = "") -> str:
    return escape(_text(value, default), quote=True)


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _iter_files(report: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    files = report.get("files", {}) if isinstance(report, dict) else {}
    if not isinstance(files, dict):
        return []
    return [(str(name), data if isinstance(data, dict) else {}) for name, data in files.items()]


def _all_items(files: list[tuple[str, dict[str, Any]]], key: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for filename, data in files:
        for item in data.get(key, []) or []:
            if not isinstance(item, dict):
                continue
            row = dict(item)
            row.setdefault("file", filename)
            row.setdefault("file_name", filename)
            rows.append(row)
    return rows


def _entity_type_from_token(token: str) -> str:
    match = re.match(r"^\[([A-Z_]+)_\d+\]$", token or "")
    return match.group(1) if match else ""


def _dictionary_counts(project_dictionary: dict[str, Any] | None) -> Counter:
    counts: Counter = Counter()
    if not isinstance(project_dictionary, dict):
        return counts

    tokens = project_dictionary.get("tokens", {})
    if not isinstance(tokens, dict):
        return counts

    for token, metadata in tokens.items():
        entity_type = ""
        if isinstance(metadata, dict):
            entity_type = _text(metadata.get("type"))
        entity_type = entity_type or _entity_type_from_token(str(token))
        if entity_type:
            counts[entity_type] += 1
    return counts


def _summary_counts(files: list[tuple[str, dict[str, Any]]]) -> Counter:
    counts: Counter = Counter()
    for _, data in files:
        summary = data.get("summary", {}) or {}
        if not isinstance(summary, dict):
            continue
        for entity_type, count in summary.items():
            counts[str(entity_type)] += _int(count)
    return counts


def _replacement_token_counts(replacements: list[dict[str, Any]]) -> tuple[Counter, dict[str, set[str]]]:
    counts: Counter = Counter()
    tokens_by_type: dict[str, set[str]] = defaultdict(set)
    for row in replacements:
        entity_type = _text(row.get("type")) or _entity_type_from_token(_text(row.get("token")))
        token = _text(row.get("token"))
        if entity_type:
            counts[entity_type] += 1
            if token:
                tokens_by_type[entity_type].add(token)
    return counts, tokens_by_type


def _label_with_code(value: Any, labels: dict[str, str]) -> str:
    code = _text(value)
    if not code:
        return ""
    label = labels.get(code)
    return f"{label} ({code})" if label else code


def _category_label(value: Any) -> str:
    return _label_with_code(value, CATEGORY_LABELS)


def _section_title(title: str, subtitle: str = "") -> str:
    subtitle_html = f"<p class=\"section-subtitle\">{_html(subtitle)}</p>" if subtitle else ""
    return f"<section><h2>{_html(title)}</h2>{subtitle_html}"


def _empty(message: str) -> str:
    return f"<p class=\"empty\">{_html(message)}</p>"


def _count_card(label: str, value: int | str, hint: str = "") -> str:
    hint_html = f"<span>{_html(hint)}</span>" if hint else ""
    return (
        "<div class=\"count-card\">"
        f"<strong>{_html(value)}</strong>"
        f"<label>{_html(label)}</label>"
        f"{hint_html}"
        "</div>"
    )


def _table(headers: list[str], rows: list[list[Any]], empty_message: str) -> str:
    if not rows:
        return _empty(empty_message)

    head = "".join(f"<th>{_html(header)}</th>" for header in headers)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{_html(value)}</td>" for value in row)
        body_rows.append(f"<tr>{cells}</tr>")
    body = "\n".join(body_rows)
    return (
        "<div class=\"table-wrap\">"
        "<table>"
        f"<thead><tr>{head}</tr></thead>"
        f"<tbody>{body}</tbody>"
        "</table>"
        "</div>"
    )


def build_html_review_report(
    report: dict[str, Any],
    project_dictionary: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> str:
    """Build a self-contained local HTML review report from pseudonymizer report data."""
    files = _iter_files(report)
    replacements = _all_items(files, "replacements")
    skipped = _all_items(files, "skipped")
    review_cases = _all_items(files, "review_cases")
    generated_at = generated_at or _now_string()

    summary_counts = _summary_counts(files)
    replacement_counts, replacement_tokens_by_type = _replacement_token_counts(replacements)
    dictionary_counts = _dictionary_counts(project_dictionary)
    warning_count = sum(len(data.get("warnings", []) or []) for _, data in files)

    all_categories = sorted(set(summary_counts) | set(replacement_counts) | set(dictionary_counts))
    category_rows = []
    for entity_type in all_categories:
        category_rows.append(
            [
                _category_label(entity_type),
                summary_counts.get(entity_type, 0),
                len(replacement_tokens_by_type.get(entity_type, set())),
                dictionary_counts.get(entity_type, 0),
            ]
        )

    file_rows = []
    for filename, data in files:
        status = data.get("status", "processed")
        summary_total = sum(_int(v) for v in (data.get("summary", {}) or {}).values())
        file_rows.append(
            [
                filename,
                _label_with_code(status, FILE_STATUS_LABELS),
                summary_total,
                len(data.get("replacements", []) or []),
                len(data.get("review_cases", []) or []),
                len(data.get("skipped", []) or []),
                len(data.get("warnings", []) or []),
            ]
        )

    replacement_rows = []
    for row in replacements:
        replacement_rows.append(
            [
                row.get("file") or row.get("file_name", ""),
                row.get("block", ""),
                _category_label(row.get("type", "")),
                row.get("token", ""),
                row.get("method", ""),
                _label_with_code(row.get("status", ""), FINDING_STATUS_LABELS),
                _label_with_code(row.get("policy_action", ""), POLICY_ACTION_LABELS),
                row.get("review_reason", ""),
                row.get("original", ""),
                row.get("comment", ""),
            ]
        )

    review_rows = []
    for row in review_cases:
        review_rows.append(
            [
                row.get("case_id", ""),
                row.get("file_name") or row.get("file", ""),
                row.get("block", ""),
                _label_with_code(row.get("status", ""), FINDING_STATUS_LABELS),
                _category_label(row.get("entity_type_expected") or row.get("entity_type_detected", "")),
                _label_with_code(row.get("policy_action", ""), POLICY_ACTION_LABELS),
                row.get("review_reason", ""),
                row.get("safe_context", ""),
                _label_with_code(row.get("recommended_decision", ""), RECOMMENDED_DECISION_LABELS),
            ]
        )

    skipped_rows = []
    for row in skipped:
        skipped_rows.append(
            [
                row.get("file") or row.get("file_name", ""),
                row.get("block", ""),
                _category_label(row.get("type", "")),
                row.get("method", ""),
                _label_with_code(row.get("reason", ""), SKIP_REASON_LABELS),
                row.get("original", ""),
                row.get("context", ""),
            ]
        )

    warning_rows = []
    for filename, data in files:
        for warning in data.get("warnings", []) or []:
            warning_rows.append([filename, warning])

    checklist = [
        "Убедиться, что в запуск попал нужный набор документов и среди них нет лишних файлов.",
        "Открыть каждый подготовленный файл и проверить, что прямые идентификаторы заменены токенами.",
        "Проверить таблицу замен на пропуски, неверные срабатывания и чрезмерное маскирование.",
        "Разобрать все строки со статусом suspect / needs review до передачи документа третьим лицам.",
        "Отдельно просмотреть изображения, сканы, колонтитулы, таблицы и нестандартное форматирование.",
        "Хранить подходящий словарь токенов локально только пока требуется обратное восстановление.",
        "Удалить локальные артефакты после завершения проверки и восстановления.",
    ]

    cleanup_paths = [
        "input/*",
        "output/anonymized/*",
        "output/project_dictionary.json",
        "output/anonymization_report.json",
        "output/anonymization_report.docx",
        "output/reports/report_*.md",
        "output/reports/review_report_*.html",
        "output/reports/review_report_latest.html",
        "review/review_cases.xlsx",
        "feedback/cases.jsonl",
        "to_decode/*",
        "output/restored/*",
    ]

    css = """
    body {
        margin: 0;
        background: #f6f7f9;
        color: #1b2430;
        font: 14px/1.5 Arial, Helvetica, sans-serif;
    }
    main {
        max-width: 1180px;
        margin: 0 auto;
        padding: 32px 20px 56px;
    }
    header {
        margin-bottom: 20px;
    }
    h1 {
        margin: 0 0 6px;
        font-size: 30px;
        line-height: 1.15;
        letter-spacing: 0;
    }
    h2 {
        margin: 0 0 12px;
        font-size: 20px;
        letter-spacing: 0;
    }
    h3 {
        margin: 18px 0 8px;
        font-size: 15px;
        letter-spacing: 0;
    }
    p {
        margin: 0 0 12px;
    }
    section {
        margin-top: 22px;
    }
    code {
        background: #eef1f4;
        border: 1px solid #dce2e8;
        border-radius: 4px;
        padding: 1px 4px;
        font-family: Consolas, "Courier New", monospace;
        font-size: 13px;
    }
    .meta {
        color: #5d6978;
    }
    .warning {
        border: 2px solid #9b351f;
        background: #fff4ef;
        color: #35140c;
        padding: 14px 16px;
        border-radius: 6px;
        margin: 18px 0 22px;
    }
    .warning strong {
        display: block;
        margin-bottom: 6px;
        font-size: 16px;
    }
    .counts {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 10px;
        margin: 14px 0 6px;
    }
    .count-card {
        background: #ffffff;
        border: 1px solid #dce2e8;
        border-radius: 6px;
        padding: 12px;
    }
    .count-card strong {
        display: block;
        font-size: 24px;
        line-height: 1;
    }
    .count-card label {
        display: block;
        margin-top: 6px;
        color: #2f3b49;
        font-weight: 700;
    }
    .count-card span {
        display: block;
        margin-top: 4px;
        color: #687586;
        font-size: 12px;
    }
    .section-subtitle,
    .empty {
        color: #5d6978;
    }
    .table-wrap {
        overflow-x: auto;
        border: 1px solid #dce2e8;
        border-radius: 6px;
        background: #ffffff;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        min-width: 760px;
    }
    th,
    td {
        border-bottom: 1px solid #e7ebef;
        padding: 8px 10px;
        text-align: left;
        vertical-align: top;
        overflow-wrap: anywhere;
    }
    th {
        background: #edf2f7;
        color: #26313f;
        font-weight: 700;
        white-space: nowrap;
    }
    tr:last-child td {
        border-bottom: 0;
    }
    td {
        white-space: pre-wrap;
    }
    .checklist,
    .cleanup {
        background: #ffffff;
        border: 1px solid #dce2e8;
        border-radius: 6px;
        padding: 12px 16px;
    }
    .checklist label {
        display: block;
        margin: 8px 0;
    }
    .checklist input {
        margin-right: 8px;
    }
    .cleanup ul,
    .limitations ul {
        margin: 8px 0 0;
        padding-left: 20px;
    }
    footer {
        margin-top: 30px;
        color: #687586;
        font-size: 12px;
    }
    """

    html_parts = [
        "<!doctype html>",
        "<html lang=\"ru\">",
        "<head>",
        "<meta charset=\"utf-8\">",
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        "<title>BeforeSending — отчёт проверки документа</title>",
        f"<style>{css}</style>",
        "</head>",
        "<body>",
        "<main>",
        "<header>",
        "<h1>BeforeSending — отчёт проверки документа</h1>",
        f"<p class=\"meta\">Сформировано локально: {_html(generated_at)}</p>",
        "</header>",
        "<div class=\"warning\">",
        "<strong>Важное предупреждение</strong>",
        "<p>Этот отчёт является локальным рабочим артефактом проверки. Если документ содержит реальные персональные, банковские, договорные или иные чувствительные данные, сам отчёт тоже может быть чувствительным.</p>",
        "<p>BeforeSending снижает риск раскрытия данных, но не гарантирует полную анонимизацию, юридическое соответствие 152-ФЗ/GDPR/HIPAA или отсутствие пропусков. Перед передачей документа третьим лицам результат необходимо проверить вручную.</p>",
        "</div>",
        _section_title("Краткая сводка"),
        "<div class=\"counts\">",
        _count_card("Файлы", len(files), "Документы в этом отчёте"),
        _count_card("Замены", len(replacements), "Найденные значения, заменённые токенами"),
        _count_card("Ручная проверка", len(review_cases), "Подозрительные или спорные строки"),
        _count_card("Пропущено", len(skipped), "Разрешённые или отфильтрованные находки"),
        _count_card("Предупреждения", warning_count, "Замечания обработки"),
        "</div>",
        "</section>",
        _section_title("Файлы"),
        _table(
            ["Файл", "Статус", "Всего находок", "Строк замен", "Ручная проверка", "Пропущено", "Предупреждения"],
            file_rows,
            "В отчёте нет файлов.",
        ),
        "</section>",
        _section_title("Категории найденных данных", "Счётчик токенов из словаря показывается, если словарь проекта передан в отчёт."),
        _table(
            ["Категория", "Всего находок", "Уникальные токены замен", "Токены в словаре"],
            category_rows,
            "Категории найденных данных отсутствуют.",
        ),
        "</section>",
        _section_title("Найденные замены", "В этом разделе могут быть исходные значения. Если обрабатывались реальные документы, считайте его чувствительным."),
        _table(
            [
                "Файл",
                "Блок",
                "Категория",
                "Токен",
                "Метод",
                "Статус",
                "Действие",
                "Причина проверки",
                "Исходное значение",
                "Комментарий",
            ],
            replacement_rows,
            "Строки замен отсутствуют.",
        ),
        "</section>",
        _section_title("Что требует ручной проверки"),
        _table(
            [
                "ID кейса",
                "Файл",
                "Блок",
                "Статус",
                "Категория",
                "Действие",
                "Причина",
                "Безопасный контекст",
                "Рекомендация",
            ],
            review_rows,
            "Подозрительных или спорных кейсов для ручной проверки нет.",
        ),
        "</section>",
        _section_title("Пропущенные / skipped findings"),
        _table(
            ["Файл", "Блок", "Категория", "Метод", "Причина", "Исходное значение", "Контекст"],
            skipped_rows,
            "Пропущенные находки не записаны.",
        ),
        "</section>",
        _section_title("Предупреждения"),
        _table(["Файл", "Предупреждение"], warning_rows, "Предупреждений обработки нет."),
        "</section>",
        _section_title("Чеклист перед отправкой"),
        "<div class=\"checklist\">",
        "\n".join(
            f"<label><input type=\"checkbox\">{_html(item)}</label>"
            for item in checklist
        ),
        "</div>",
        "</section>",
        _section_title("Безопасная очистка локальных артефактов"),
        "<div class=\"cleanup\">",
        "<p>После проверки удалите локальные артефакты, которые больше не нужны. Словарь токенов храните только пока требуется обратное восстановление.</p>",
        "<ul>",
        "\n".join(f"<li><code>{_html(path)}</code></li>" for path in cleanup_paths),
        "</ul>",
        "</div>",
        "</section>",
        _section_title("Ограничения"),
        "<div class=\"limitations\">",
        "<ul>",
        "<li>Автоматическое обнаружение может пропускать чувствительные значения и может маскировать безопасный текст.</li>",
        "<li>Ручная проверка обязательна перед передачей подготовленного документа третьим лицам или внешним сервисам.</li>",
        "<li>OCR, проверка сканов и изображений, интерфейс приложения, защищённое хранилище словарей, установщик и юридические/регуляторные заверения не входят в этот отчёт.</li>",
        "<li>Псевдонимизированный документ вместе со словарём токенов может быть обратимо восстановлен, поэтому словарь нужно хранить как чувствительный локальный артефакт.</li>",
        "</ul>",
        "</div>",
        "</section>",
        _section_title("Техническая информация"),
        _table(
            ["Параметр", "Значение"],
            [
                ["Генератор", "Локальный HTML-отчёт BeforeSending"],
                ["Язык интерфейса", "Русский интерфейс, технические коды сохранены в скобках"],
                ["Формат", "Самодостаточный HTML с inline CSS, без внешних CSS/JS/CDN"],
                ["Пути отчётов", "output/reports/review_report_*.html; output/reports/review_report_latest.html"],
                ["Логика обнаружения", "Используются готовые данные отчёта; правила распознавания здесь не изменяются"],
            ],
            "Техническая информация недоступна.",
        ),
        "</section>",
        "<footer>Сформировано локальным HTML-отчётом BeforeSending.</footer>",
        "</main>",
        "</body>",
        "</html>",
    ]
    return "\n".join(html_parts)


def write_html_review_report(
    report: dict[str, Any],
    path: str | Path,
    project_dictionary: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_html_review_report(report, project_dictionary=project_dictionary, generated_at=generated_at),
        encoding="utf-8",
    )
    return output_path
