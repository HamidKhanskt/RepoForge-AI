from typing import Any


def compare_benchmarks(
    before: dict[str, Any],
    after: dict[str, Any],
) -> dict[str, Any]:
    """Compare before/after performance measurements."""

    before_results = {
        row["cart_size"]: row["average_seconds"]
        for row in before.get("results", [])
    }

    after_results = {
        row["cart_size"]: row["average_seconds"]
        for row in after.get("results", [])
    }

    comparisons = []

    for cart_size in sorted(
        set(before_results) & set(after_results)
    ):
        before_time = before_results[cart_size]
        after_time = after_results[cart_size]

        improvement = (
            (before_time - after_time)
            / before_time
            * 100
            if before_time
            else 0
        )

        comparisons.append(
            {
                "cart_size": cart_size,
                "before_seconds": before_time,
                "after_seconds": after_time,
                "improvement_percent": round(
                    improvement,
                    2,
                ),
            }
        )

    if comparisons:
        largest = max(
            comparisons,
            key=lambda x: x["cart_size"],
        )

        overall_improvement = largest[
            "improvement_percent"
        ]
    else:
        overall_improvement = 0

    return {
        "comparisons": comparisons,
        "overall_improvement_percent": overall_improvement,
        "improved": overall_improvement > 0,
        "decision": (
            "accepted"
            if overall_improvement > 0
            else "rejected"
        ),
    }
