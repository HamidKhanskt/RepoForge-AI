from pprint import pprint

from src.agents.optimizer import optimizer_node


def main():

    state = {
        "task": (
            "Investigate why a checkout endpoint "
            "has high latency."
        ),
        "evidence": """
Finding 1:
get_product() is called inside the product iteration loop.

Finding 2:
get_product() contains an 80ms blocking database delay.

Finding 3:
calculate_shipping() contains a 300ms blocking delay.
""",
        "benchmark": {
            "scaling": "approximately_linear",
            "baseline_seconds": 0.3029,
            "estimated_per_item_seconds": 0.0843,
            "largest_cart_seconds": 1.9894,
            "bottleneck_candidate": (
                "per-product database calls"
            ),
            "severity": "high",
        },
    }

    result = optimizer_node(state)

    print("=" * 70)
    print("                    OPTIMIZATION AGENT")
    print("=" * 70)

    pprint(result)


if __name__ == "__main__":
    main()
