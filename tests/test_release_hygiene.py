from __future__ import annotations

from pathlib import Path

from tools.check_release_hygiene import analyze_paths, iter_all_paths


def reasons(paths: list[str]) -> list[str]:
    return [finding.reason for finding in analyze_paths(paths)]


def test_allows_runtime_folder_placeholders():
    assert analyze_paths(
        [
            "input/.gitkeep",
            "input/README.md",
            "output/.gitkeep",
            "output/README.md",
            "review/.gitkeep",
            "to_decode/README.md",
            "feedback/.gitkeep",
        ]
    ) == []


def test_flags_sensitive_runtime_files_and_dictionaries():
    findings = analyze_paths(
        [
            "input/client.docx",
            "output/project_dictionary.json",
            "feedback/cases.jsonl",
            "rules/manual_hide.txt",
        ]
    )

    assert {finding.path for finding in findings} >= {
        "input/client.docx",
        "output/project_dictionary.json",
        "feedback/cases.jsonl",
        "rules/manual_hide.txt",
    }
    assert any("runtime working folder" in finding.reason for finding in findings)
    assert any("sensitive local file name" in finding.reason for finding in findings)


def test_flags_generated_reports_archives_logs_and_token_maps():
    findings = analyze_paths(
        [
            "output/reports/review_report_latest.html",
            "release.zip",
            "run.log",
            "token_map.json",
            "raw_text_dump.txt",
        ]
    )
    joined = "\n".join(finding.reason for finding in findings)

    assert "generated report artifact" in joined
    assert "working archive" in joined
    assert "log file" in joined
    assert "token map artifact" in joined
    assert "raw/extracted text artifact" in joined


def test_full_scan_flags_cache_directory_without_descending(tmp_path: Path):
    (tmp_path / ".venv" / "Scripts").mkdir(parents=True)
    (tmp_path / ".venv" / "Scripts" / "python.exe").write_text("local", encoding="utf-8")
    (tmp_path / "input").mkdir()
    (tmp_path / "input" / "README.md").write_text("placeholder", encoding="utf-8")
    (tmp_path / "input" / "real.pdf").write_bytes(b"%PDF-1.4")

    scanned = iter_all_paths(tmp_path)
    findings = analyze_paths(scanned)

    assert ".venv" in scanned
    assert ".venv/Scripts/python.exe" not in scanned
    assert any(finding.path == ".venv" for finding in findings)
    assert any(finding.path == "input/real.pdf" for finding in findings)
