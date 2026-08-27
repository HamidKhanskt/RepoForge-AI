from pathlib import Path

from langchain_core.tools import tool


WORKSPACE = Path("demo_target").resolve()


@tool
def inspect_performance_patterns() -> str:
    """Inspect the target repository for performance patterns."""

    findings = []

    checkout = (
        WORKSPACE
        / "app"
        / "checkout.py"
    )

    database = (
        WORKSPACE
        / "app"
        / "database.py"
    )

    shipping = (
        WORKSPACE
        / "app"
        / "shipping.py"
    )

    if checkout.exists():

        code = checkout.read_text()

        if (
            "for product_id in cart"
            in code
            and "get_product(" in code
        ):
            findings.append(
                {
                    "type": "n_plus_one",
                    "file": "app/checkout.py",
                    "evidence": (
                        "get_product() is called "
                        "inside the product "
                        "iteration loop."
                    ),
                    "severity": "high",
                }
            )

        if "get_products(" in code:
            findings.append(
                {
                    "type": "batched_database_access",
                    "file": "app/checkout.py",
                    "evidence": (
                        "checkout() retrieves "
                        "products through a "
                        "batched get_products() "
                        "operation."
                    ),
                    "severity": "low",
                }
            )

        if "calculate_shipping(" in code:
            findings.append(
                {
                    "type": "shipping_latency",
                    "file": "app/checkout.py",
                    "evidence": (
                        "checkout() calls "
                        "calculate_shipping() "
                        "during the request."
                    ),
                    "severity": "medium",
                }
            )

    if database.exists():

        code = database.read_text()

        if "time.sleep(0.08)" in code:

            if "def get_product(" in code:
                findings.append(
                    {
                        "type": "database_latency",
                        "file": "app/database.py",
                        "evidence": (
                            "get_product() contains "
                            "a simulated 80ms "
                            "blocking database "
                            "delay."
                        ),
                        "severity": "high",
                    }
                )

            if "def get_products(" in code:
                findings.append(
                    {
                        "type": "batched_database_operation",
                        "file": "app/database.py",
                        "evidence": (
                            "get_products() performs "
                            "one simulated 80ms "
                            "database operation "
                            "for the requested "
                            "product collection."
                        ),
                        "severity": "low",
                    }
                )

    if shipping.exists():

        code = shipping.read_text()

        if "time.sleep(0.3)" in code:
            findings.append(
                {
                    "type": "external_latency",
                    "file": "app/shipping.py",
                    "evidence": (
                        "calculate_shipping() "
                        "contains a simulated "
                        "300ms blocking "
                        "external-service delay."
                    ),
                    "severity": "medium",
                }
            )

    if not findings:
        return (
            "No known performance patterns "
            "were detected."
        )

    output = [
        "DETERMINISTIC PERFORMANCE EVIDENCE"
    ]

    for index, finding in enumerate(
        findings,
        start=1,
    ):
        output.append(
            f"""
Finding {index}
Type: {finding['type']}
File: {finding['file']}
Severity: {finding['severity']}
Evidence: {finding['evidence']}
""".strip()
        )

    return "\n".join(output)
