from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


RUNTIME_DIRS = {
    "feedback",
    "input",
    "output",
    "restored",
    "review",
    "to_decode",
}

SAFE_RUNTIME_PLACEHOLDERS = {
    f"{folder}/.gitkeep" for folder in RUNTIME_DIRS
} | {
    f"{folder}/README.md" for folder in RUNTIME_DIRS
}

FORBIDDEN_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
}

FORBIDDEN_BASENAMES = {
    "dictionary.json",
    "manual_allow.txt",
    "manual_hide.txt",
    "private_org_markers.txt",
    "project_dictionary.json",
    "public_orgs.txt",
}

ARCHIVE_SUFFIXES = {".7z", ".rar", ".zip"}
DOCUMENT_SUFFIXES = {
    ".csv",
    ".doc",
    ".docx",
    ".ods",
    ".odt",
    ".pdf",
    ".rtf",
    ".tsv",
    ".xls",
    ".xlsx",
}
LOG_SUFFIXES = {".log"}

REPORT_PREFIXES = (
    "anonymization_report",
    "quality_metrics_",
    "regression_report_",
    "report_",
    "review_report_",
)

RAW_TEXT_MARKERS = (
    "extracted_text",
    "extracted-text",
    "original_text",
    "original-text",
    "raw_text",
    "raw-text",
    "source_text",
    "source-text",
)

TOKEN_MAP_MARKERS = (
    "token_map",
    "token-map",
    "token_maps",
    "token-maps",
    "tokens_map",
    "tokens-map",
)


@dataclass(frozen=True)
class Finding:
    path: str
    reason: str


def normalize_release_path(path: str | Path) -> str:
    normalized = str(path).replace("\\", "/").strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized.strip("/")


def _path_parts(path: str) -> tuple[str, ...]:
    return tuple(part for part in PurePosixPath(path).parts if part not in ("", "."))


def analyze_path(path: str | Path) -> list[Finding]:
    rel_path = normalize_release_path(path)
    if not rel_path:
        return []

    if rel_path in SAFE_RUNTIME_PLACEHOLDERS:
        return []

    parts = _path_parts(rel_path)
    lower_parts = tuple(part.lower() for part in parts)
    basename = lower_parts[-1]
    suffix = PurePosixPath(basename).suffix
    stem = PurePosixPath(basename).stem
    findings: list[Finding] = []

    for part in lower_parts:
        if part in FORBIDDEN_DIR_NAMES:
            findings.append(Finding(rel_path, f"forbidden local/cache directory: {part}/"))

    if lower_parts[0] in RUNTIME_DIRS:
        findings.append(
            Finding(rel_path, f"runtime working folder content must not be in release: {lower_parts[0]}/")
        )

    if basename in FORBIDDEN_BASENAMES:
        findings.append(Finding(rel_path, f"sensitive local file name: {basename}"))

    if suffix in ARCHIVE_SUFFIXES:
        findings.append(Finding(rel_path, f"working archive must not be in release: *{suffix}"))

    if suffix in DOCUMENT_SUFFIXES:
        findings.append(Finding(rel_path, f"document/spreadsheet artifact must be reviewed before release: *{suffix}"))

    if suffix in LOG_SUFFIXES:
        findings.append(Finding(rel_path, f"log file may contain sensitive runtime data: *{suffix}"))

    if basename.startswith(REPORT_PREFIXES):
        findings.append(Finding(rel_path, "generated report artifact must not be released from the working tree"))

    if suffix in {".json", ".jsonl", ".txt", ".md"} and any(marker in stem for marker in TOKEN_MAP_MARKERS):
        findings.append(Finding(rel_path, "token map artifact may contain reversible original values"))

    if suffix in {".txt", ".md"} and any(marker in stem for marker in RAW_TEXT_MARKERS):
        findings.append(Finding(rel_path, "raw/extracted text artifact may contain original document text"))

    return findings


def analyze_paths(paths: Iterable[str | Path]) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[Finding] = set()
    for path in paths:
        for finding in analyze_path(path):
            if finding not in seen:
                seen.add(finding)
                findings.append(finding)
    return findings


def iter_tracked_paths(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"could not list tracked files with git: {exc}") from exc

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def iter_all_paths(root: Path) -> list[str]:
    paths: list[str] = []

    for current_root, dirnames, filenames in os.walk(root):
        current = Path(current_root)

        for dirname in list(dirnames):
            rel_dir = normalize_release_path((current / dirname).relative_to(root))
            if dirname.lower() in FORBIDDEN_DIR_NAMES:
                paths.append(rel_dir)
                dirnames.remove(dirname)

        for filename in filenames:
            paths.append(normalize_release_path((current / filename).relative_to(root)))

    return paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check that a tracked tree or extracted release artifact does not include "
            "local runtime data, token dictionaries, caches, reports, or working archives."
        )
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository or release-artifact root to check. Default: current directory.",
    )
    parser.add_argument(
        "--scan-all",
        action="store_true",
        help="Scan every file under --root. Use this for extracted release artifacts.",
    )
    parser.add_argument(
        "--tracked",
        action="store_true",
        help="Scan git-tracked files. This is the default when --root contains .git.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    if not root.exists():
        parser.error(f"--root does not exist: {root}")

    use_tracked = args.tracked or (not args.scan_all and (root / ".git").exists())

    if use_tracked:
        paths = iter_tracked_paths(root)
        mode = "git-tracked files"
    else:
        paths = iter_all_paths(root)
        mode = "all files"

    findings = analyze_paths(paths)
    if findings:
        print(f"Release hygiene check FAILED for {root} ({mode}).")
        print()
        for finding in findings:
            print(f"- {finding.path}: {finding.reason}")
        print()
        print("Create public artifacts from a clean tracked state, for example with git archive,")
        print("and keep local runtime folders, dictionaries, reports, logs, caches, and archives out.")
        return 1

    print(f"Release hygiene check passed for {root} ({mode}, {len(paths)} paths checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
