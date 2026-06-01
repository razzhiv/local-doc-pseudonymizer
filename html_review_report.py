from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any


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
                entity_type,
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
                status,
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
                row.get("type", ""),
                row.get("token", ""),
                row.get("method", ""),
                row.get("status", ""),
                row.get("policy_action", ""),
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
                row.get("status", ""),
                row.get("entity_type_expected") or row.get("entity_type_detected", ""),
                row.get("policy_action", ""),
                row.get("review_reason", ""),
                row.get("safe_context", ""),
                row.get("recommended_decision", ""),
            ]
        )

    skipped_rows = []
    for row in skipped:
        skipped_rows.append(
            [
                row.get("file") or row.get("file_name", ""),
                row.get("block", ""),
                row.get("type", ""),
                row.get("method", ""),
                row.get("reason", ""),
                row.get("original", ""),
                row.get("context", ""),
            ]
        )

    warning_rows = []
    for filename, data in files:
        for warning in data.get("warnings", []) or []:
            warning_rows.append([filename, warning])

    checklist = [
        "Confirm the source fixture or document set is intended for this review run.",
        "Open each pseudonymized output and verify direct identifiers were replaced with tokens.",
        "Inspect replacement rows for over-masking and missed context.",
        "Review any suspect or needs-review cases before sharing output externally.",
        "Check images, scans, headers, footers, tables, and unusual formatting manually.",
        "Keep the matching token dictionary local if restoration is still needed.",
        "Delete generated local artifacts when review and restoration are complete.",
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
        "<html lang=\"en\">",
        "<head>",
        "<meta charset=\"utf-8\">",
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        "<title>BeforeSending HTML Review Report</title>",
        f"<style>{css}</style>",
        "</head>",
        "<body>",
        "<main>",
        "<header>",
        "<h1>BeforeSending HTML Review Report</h1>",
        f"<p class=\"meta\">Generated locally: {_html(generated_at)}</p>",
        "</header>",
        "<div class=\"warning\">",
        "<strong>Sensitive local artifact</strong>",
        "<p>Reports, token dictionaries, pseudonymized output, restored output, review files, and screenshots based on real documents can contain personal or confidential data. Keep them local. Do not upload, publish, commit, or share them unless they are verified synthetic and intended for release.</p>",
        "<p>This report supports pseudonymization / masking / risk reduction. It is not guaranteed anonymization, legal compliance, or an enterprise DLP control.</p>",
        "</div>",
        _section_title("Summary"),
        "<div class=\"counts\">",
        _count_card("Files", len(files), "Input documents in this report"),
        _count_card("Replacements", len(replacements), "Detected values replaced by tokens"),
        _count_card("Review cases", len(review_cases), "Suspect or needs-review rows"),
        _count_card("Skipped", len(skipped), "Allowed or filtered findings"),
        _count_card("Warnings", warning_count, "Processing caveats"),
        "</div>",
        "</section>",
        _section_title("Files"),
        _table(
            ["File", "Status", "Summary count", "Replacement rows", "Review cases", "Skipped", "Warnings"],
            file_rows,
            "No files were present in the report.",
        ),
        "</section>",
        _section_title("Category And Token Counts", "Dictionary token counts are shown when a project dictionary is provided."),
        _table(
            ["Category", "Summary count", "Unique replacement tokens", "Dictionary tokens"],
            category_rows,
            "No category counts were available.",
        ),
        "</section>",
        _section_title("Findings And Replacements", "Original values may appear here. Treat this section as sensitive when real documents were processed."),
        _table(
            [
                "File",
                "Block",
                "Type",
                "Token",
                "Method",
                "Status",
                "Policy action",
                "Review reason",
                "Original value",
                "Comment",
            ],
            replacement_rows,
            "No replacement rows were available.",
        ),
        "</section>",
        _section_title("Manual Review Cases"),
        _table(
            [
                "Case ID",
                "File",
                "Block",
                "Status",
                "Type",
                "Policy action",
                "Reason",
                "Safe context",
                "Recommended decision",
            ],
            review_rows,
            "No suspect or needs-review cases were generated.",
        ),
        "</section>",
        _section_title("Skipped Findings"),
        _table(
            ["File", "Block", "Type", "Method", "Reason", "Original value", "Context"],
            skipped_rows,
            "No skipped findings were recorded.",
        ),
        "</section>",
        _section_title("Warnings"),
        _table(["File", "Warning"], warning_rows, "No processing warnings were recorded."),
        "</section>",
        _section_title("Manual Review Checklist"),
        "<div class=\"checklist\">",
        "\n".join(
            f"<label><input type=\"checkbox\">{_html(item)}</label>"
            for item in checklist
        ),
        "</div>",
        "</section>",
        _section_title("Cleanup Guidance"),
        "<div class=\"cleanup\">",
        "<p>After review, remove generated local artifacts that are no longer needed. Keep the token dictionary only while restoration is required.</p>",
        "<ul>",
        "\n".join(f"<li><code>{_html(path)}</code></li>" for path in cleanup_paths),
        "</ul>",
        "</div>",
        "</section>",
        _section_title("Limitations"),
        "<div class=\"limitations\">",
        "<ul>",
        "<li>Automated detection can miss sensitive values and can over-mask safe text.</li>",
        "<li>Manual review remains required before sharing any prepared document with a third party or external AI/SaaS tool.</li>",
        "<li>OCR, scanned image review, GUI review, vault/encryption, installer packaging, and compliance guarantees are outside this report.</li>",
        "<li>Pseudonymized output plus its token dictionary can be reversible and must be handled as sensitive local data.</li>",
        "</ul>",
        "</div>",
        "</section>",
        "<footer>Generated by BeforeSending local HTML review report.</footer>",
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
