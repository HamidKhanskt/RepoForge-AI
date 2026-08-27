from pathlib import Path
from typing import Any


def benchmark_repository(
    repository_path: str,
    repository_files: list[str] | None = None,
) -> dict[str, Any]:
    """
    Perform repository-level performance analysis.

    This function intentionally does NOT invent runtime benchmark
    numbers. It reports static performance evidence discovered by
    the repository scanner.

    Runtime benchmarking is only appropriate when AgentForge has
    a known executable benchmark target.
    """

    files = repository_files or []

    checkout_available = any(
        file.endswith("app/checkout.py")
        for file in files
    )

    if checkout_available:
        return {
            "available": False,
            "type": "runtime_benchmark_not_implemented",
            "repository_path": repository_path,
            "message": (
                "Repository contains a checkout target, "
                "but no generic runtime benchmark was executed."
            ),
        }

    return {
        "available": False,
        "type": "static_only",
        "repository_path": repository_path,
        "message": (
            "Runtime performance benchmark skipped: "
            "repository does not contain a supported "
            "runtime benchmark target."
        ),
    }


def benchmark_checkout(
    sizes: list[int] | None = None,
    runs: int = 3,
    repository_path: str | None = None,
) -> dict[str, Any]:
    """
    Backward-compatible checkout benchmark.

    AgentForge no longer relies on this function for generic
    repository analysis.
    """

    if not repository_path:
        raise ValueError(
            "repository_path is required for checkout benchmarking."
        )

    raise FileNotFoundError(
        "No supported checkout runtime benchmark is configured "
        "for this repository."
    )


def prioritize_findings(findings):
    """Prioritize performance findings by likely engineering impact."""
    high_value = {
        "tavily_search",
        "requests.get",
        "requests.post",
        "httpx.get",
        "httpx.post",
        "urllib.request",
        "execute",
        "executemany",
        "fetchone",
        "fetchall",
        "query",
    }

    low_value = {
        "float",
        "int",
        "str",
        "len",
        "round",
        "isinstance",
        "print",
    }

    for finding in findings:
        evidence = str(finding.get("evidence", "")).lower()
        kind = str(finding.get("type", "")).lower()

        if any(name.lower() in evidence for name in high_value):
            finding["priority"] = "critical"
            finding["priority_score"] = 95
            finding["impact"] = "Repeated external or I/O-bound operation."
        elif kind == "repeated_function_call":
            finding["priority"] = "high"
            finding["priority_score"] = 70
            finding["impact"] = "Repeated function invocation."
        elif any(name.lower() in evidence for name in low_value):
            finding["priority"] = "low"
            finding["priority_score"] = 20
            finding["impact"] = "Lightweight repeated operation."
        else:
            finding["priority"] = "medium"
            finding["priority_score"] = 50
            finding["impact"] = "Potential optimization requiring runtime validation."

    return sorted(
        findings,
        key=lambda x: x.get("priority_score", 0),
        reverse=True,
    )

