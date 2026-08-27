import re
from pathlib import Path


WORKSPACE = Path("demo_target").resolve()


def load_repository_text() -> str:
    """Load all readable source files into one searchable corpus."""

    chunks = []

    for path in WORKSPACE.rglob("*"):
        if not path.is_file():
            continue

        try:
            content = path.read_text()
        except UnicodeDecodeError:
            continue

        relative = path.relative_to(WORKSPACE)

        chunks.append(
            f"\n--- FILE: {relative} ---\n{content}"
        )

    return "\n".join(chunks)


def verify_claims(claim_text: str) -> dict:
    """Verify important factual claims against repository contents."""

    repository = load_repository_text()

    checks = []

    # Detect claims involving technologies that may be hallucinated.
    suspicious_terms = [
        "flask",
        "blueprint",
        "request.form",
        "cursor.execute",
        "select *",
        "endpoint",
    ]

    for term in suspicious_terms:
        if term.lower() in claim_text.lower():
            present = term.lower() in repository.lower()

            checks.append(
                {
                    "claim": term,
                    "supported": present,
                }
            )

    # Verify important concrete code patterns.
    expected_patterns = [
        "get_product(",
        "calculate_shipping(",
        "time.sleep(0.08)",
        "time.sleep(0.3)",
        "for product_id in cart",
    ]

    for pattern in expected_patterns:
        if pattern.lower() in claim_text.lower():
            present = pattern.lower() in repository.lower()

            checks.append(
                {
                    "claim": pattern,
                    "supported": present,
                }
            )

    if not checks:
        return {
            "supported": True,
            "score": 1.0,
            "checks": [],
            "reason": "No directly verifiable concrete claims detected.",
        }

    supported = sum(
        check["supported"]
        for check in checks
    )

    score = supported / len(checks)

    return {
        "supported": score >= 0.75,
        "score": round(score, 2),
        "checks": checks,
        "reason": (
            "Claims are sufficiently grounded in repository contents."
            if score >= 0.75
            else
            "One or more concrete claims are not supported "
            "by repository contents."
        ),
    }
