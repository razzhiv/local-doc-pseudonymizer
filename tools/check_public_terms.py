from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


TEXT_SUFFIXES = {
    "",
    ".bat",
    ".cfg",
    ".css",
    ".csv",
    ".gitattributes",
    ".gitignore",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsonl",
    ".md",
    ".ps1",
    ".py",
    ".rst",
    ".sh",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

BINARY_SUFFIXES = {
    ".7z",
    ".bin",
    ".bmp",
    ".ckpt",
    ".doc",
    ".docx",
    ".gif",
    ".gz",
    ".ico",
    ".jpeg",
    ".jpg",
    ".model",
    ".ods",
    ".odt",
    ".onnx",
    ".pdf",
    ".png",
    ".pt",
    ".pth",
    ".rar",
    ".tar",
    ".vec",
    ".xls",
    ".xlsx",
    ".zip",
}

SKIP_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
}

SKIP_PREFIXES = (
    "output/reports/",
    "review/reports/",
)

COMPLIANCE_EXEMPT_BASENAMES = {
    "license",
    "notice",
    "third_party_licenses.md",
}


def _phrase(*parts: str) -> str:
    return "".join(parts)


PRIVATE_PRODUCT_TERMS = (
    _phrase("Before", "Sending", " ", "Pro"),
    _phrase("Quote", " ", "Desk"),
    _phrase("Quote", " ", "Desk", " ", "Lite"),
    _phrase("AI", " ", "automation"),
    _phrase("AI", " ", "Case", " ", "Desk"),
    _phrase("Shared", " ", "Review", " ", "Component"),
    _phrase("commercial", " ", "workflow"),
    _phrase("manager", " ", "workspace"),
    _phrase("Integration", " ", "Boundary"),
    _phrase("B10", "-", "B19"),
    _phrase("Level", " ", "0"),
    _phrase("Level", " ", "1"),
    _phrase("Level", " ", "2"),
    _phrase("Level", " ", "3"),
    _phrase("Level", " ", "4"),
    _phrase("Sales", " ", "Workflow", " ", "Performance", " ", "Layer"),
)

PRIVATE_TERM_RULES = tuple(
    (term, re.compile(rf"(?<![\w-]){re.escape(term)}(?![\w-])", re.IGNORECASE))
    for term in PRIVATE_PRODUCT_TERMS
)

PROMISE_CUE_RE = re.compile(
    r"\b("
    r"coming\s+soon|"
    r"future\s+(?:support|version|release|work|roadmap)|"
    r"in\s+the\s+future|"
    r"planned|"
    r"plans?\s+to|"
    r"roadmap|"
    r"will\s+(?:add|build|include|introduce|provide|ship|support)|"
    r"we\s+will|"
    r"upcoming"
    r")\b",
    re.IGNORECASE,
)

DLP_PATTERN = re.escape(_phrase("d", "lp"))
COMPLIANCE_PATTERN = re.escape(_phrase("com", "pliance"))

RISKY_PUBLIC_SCOPE_RE = re.compile(
    rf"\b("
    r"add/remove\s+programs|"
    r"ai\s+automation|"
    r"app(?:lication)?\s+interface|"
    r"commercial\s+workflow|"
    r"desktop(?:-style)?\s+(?:app|application)|"
    rf"{DLP_PATTERN}|"
    r"encrypted\s+vault|"
    r"enterprise\s+security|"
    r"gui(?:\s+app)?|"
    r"integration(?:s)?|"
    r"launcher|"
    r"manager\s+workspace|"
    r"production\s+(?:installer|security|vault)|"
    r"protected\s+dictionary[-\s]+storage|"
    r"secure\s+storage|"
    r"system-wide\s+(?:install|installation)|"
    r"vault"
    r")\b",
    re.IGNORECASE,
)

COMPLIANCE_CLAIM_RE = re.compile(
    rf"\b("
    r"complete\s+anonymization|"
    rf"{COMPLIANCE_PATTERN}(?:\s+tool)?|"
    rf"{DLP_PATTERN}(?:\s+system)?|"
    r"guaranteed\s+anonymization|"
    r"zero[-\s]+leakage"
    r")\b",
    re.IGNORECASE,
)

NEGATIVE_DISCLAIMER_RE = re.compile(
    r"\b("
    r"do\s+not\s+(?:claim|describe|imply|include|present|promise|treat)|"
    r"does\s+not\s+(?:claim|commit|include|provide|replace|support)|"
    r"is\s+not\s+(?:a|an|automatically|included|provided|supported)|"
    r"it\s+is\s+not\s+(?:a|an)|"
    r"must\s+not\s+(?:claim|imply|include)|"
    r"no\s+(?:committed|protected|production|public)|"
    r"not\s+(?:a|an|automatically|committed|currently|included|provided|publicly|supported)|"
    r"not\s+in|"
    r"should\s+not\s+(?:be|claim|include)"
    r")\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class PublicTermFinding:
    path: str
    line: int
    label: str
    reason: str
    excerpt: str


def normalize_public_path(path: str | Path) -> str:
    normalized = str(path).replace("\\", "/").strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized.strip("/")


def _path_parts(path: str) -> tuple[str, ...]:
    return tuple(part for part in PurePosixPath(path).parts if part not in ("", "."))


def is_public_text_path(path: str | Path) -> bool:
    rel_path = normalize_public_path(path)
    if not rel_path:
        return False

    lower_path = rel_path.lower()
    if any(lower_path.startswith(prefix) for prefix in SKIP_PREFIXES):
        return False

    parts = tuple(part.lower() for part in _path_parts(rel_path))
    if any(part in SKIP_DIR_NAMES for part in parts):
        return False

    suffix = PurePosixPath(lower_path).suffix
    if suffix in BINARY_SUFFIXES:
        return False

    return suffix in TEXT_SUFFIXES


def _looks_binary(data: bytes) -> bool:
    return b"\0" in data[:4096]


def read_public_text_file(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None

    if _looks_binary(data):
        return None

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")


def _is_negative_disclaimer(line: str) -> bool:
    return bool(NEGATIVE_DISCLAIMER_RE.search(line))


def _starts_negative_list_context(line: str) -> bool:
    stripped = line.strip().lower()
    return (
        stripped.endswith(" is not:")
        or stripped.endswith(" are not:")
        or stripped.endswith(" do not claim:")
        or stripped.startswith("do not claim:")
        or stripped.startswith("do not include:")
        or stripped.startswith("public documentation and release notes should not claim:")
    )


def _is_markdown_list_item(line: str) -> bool:
    return line.lstrip().startswith(("- ", "* "))


def _is_compliance_exempt_path(path: str) -> bool:
    return PurePosixPath(normalize_public_path(path).lower()).name in COMPLIANCE_EXEMPT_BASENAMES


def _clean_excerpt(line: str) -> str:
    excerpt = " ".join(line.strip().split())
    if len(excerpt) > 140:
        return excerpt[:137] + "..."
    return excerpt


def analyze_text(path: str, text: str) -> list[PublicTermFinding]:
    findings: list[PublicTermFinding] = []
    negative_list_context = 0

    for line_number, line in enumerate(text.splitlines(), start=1):
        line_is_negative = _is_negative_disclaimer(line) or (
            negative_list_context > 0 and _is_markdown_list_item(line)
        )

        for term, pattern in PRIVATE_TERM_RULES:
            if pattern.search(line):
                findings.append(
                    PublicTermFinding(
                        path=path,
                        line=line_number,
                        label=term,
                        reason="forbidden private/product term",
                        excerpt=_clean_excerpt(line),
                    )
                )

        has_promise = PROMISE_CUE_RE.search(line)
        has_risky_scope = RISKY_PUBLIC_SCOPE_RE.search(line)
        if has_promise and has_risky_scope and not line_is_negative:
            findings.append(
                PublicTermFinding(
                    path=path,
                    line=line_number,
                    label=has_risky_scope.group(0),
                    reason="public roadmap or product-scope promise",
                    excerpt=_clean_excerpt(line),
                )
            )

        compliance_claim = COMPLIANCE_CLAIM_RE.search(line)
        if compliance_claim and not line_is_negative and not _is_compliance_exempt_path(path):
            findings.append(
                PublicTermFinding(
                    path=path,
                    line=line_number,
                    label=compliance_claim.group(0),
                    reason="public security positioning claim",
                    excerpt=_clean_excerpt(line),
                )
            )

        stripped = line.strip()
        if _starts_negative_list_context(line):
            negative_list_context = 20
        elif not stripped:
            negative_list_context = max(0, negative_list_context - 1)
        elif negative_list_context > 0:
            negative_list_context -= 1

    return findings


def iter_tracked_paths(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"could not list tracked files with git: {exc}") from exc

    raw_paths = result.stdout.split(b"\0")
    return [raw_path.decode("utf-8", errors="replace") for raw_path in raw_paths if raw_path]


def iter_tracked_public_text_paths(root: Path) -> list[str]:
    return [path for path in iter_tracked_paths(root) if is_public_text_path(path)]


def analyze_tracked_public_text(root: Path) -> list[PublicTermFinding]:
    findings: list[PublicTermFinding] = []

    for rel_path in iter_tracked_public_text_paths(root):
        text = read_public_text_file(root / rel_path)
        if text is None:
            continue
        findings.extend(analyze_text(rel_path, text))

    return findings


def format_findings(findings: Iterable[PublicTermFinding]) -> list[str]:
    lines: list[str] = []
    for finding in findings:
        lines.append(f"- {finding.path}:{finding.line}: {finding.reason}: {finding.label}")
        if finding.excerpt:
            lines.append(f"  {finding.excerpt}")
    return lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check git-tracked public text files for private/product terms, "
            "public roadmap promises, and over-strong security claims."
        )
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to check. Default: current directory.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    if not root.exists():
        parser.error(f"--root does not exist: {root}")
    if not (root / ".git").exists():
        parser.error(f"--root must be a git working tree: {root}")

    try:
        paths = iter_tracked_public_text_paths(root)
        findings = analyze_tracked_public_text(root)
    except RuntimeError as exc:
        print(f"Public terms check ERROR: {exc}", file=sys.stderr)
        return 2

    if findings:
        print(f"Public terms check FAILED for {root}.")
        print()
        for line in format_findings(findings):
            print(line)
        print()
        print("Use public maintenance wording, synthetic-only examples, and negative disclaimers")
        print("instead of private product names, roadmap promises, or broad security claims.")
        return 1

    print(f"Public terms check passed for {root} ({len(paths)} tracked public text files checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
