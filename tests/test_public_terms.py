from __future__ import annotations

from tools.check_public_terms import analyze_text


def _joined(parts: list[str]) -> str:
    return "".join(parts)


def test_forbidden_private_term_fixture_fails():
    private_term = _joined(["Before", "Sending", " ", "Pro"])
    findings = analyze_text("fixture.md", f"This public page promotes {private_term}.")

    assert len(findings) == 1
    assert findings[0].reason == "forbidden private/product term"


def test_safe_public_wording_and_negative_disclaimers_pass():
    text = "\n".join(
        [
            "This repository is in minimal public maintenance mode.",
            "It is not a GUI app, not a production installer, and not a system-wide installation.",
            "No protected dictionary storage feature is provided or publicly committed.",
            "Use synthetic examples only for bug reports, tests, and documentation.",
        ]
    )

    assert analyze_text("safe.md", text) == []


def test_external_ai_saas_wording_passes():
    text = "\n".join(
        [
            "Prepare documents before external AI/SaaS use.",
            "Review files manually before sending them to external AI services.",
        ]
    )

    assert analyze_text("safe_external_services.md", text) == []


def test_public_roadmap_promise_fixture_fails():
    risky_text = _joined(
        [
            "Public ",
            "road",
            "map: encrypted ",
            "vault",
            " is coming ",
            "soon.",
        ]
    )

    findings = analyze_text("promise.md", risky_text)

    assert len(findings) == 1
    assert findings[0].reason == "public roadmap or product-scope promise"
