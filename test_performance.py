from src.tools.performance import benchmark_checkout


def main():
    print("=" * 70)
    print("                 PERFORMANCE AGENT")
    print("=" * 70)

    result = benchmark_checkout(
        sizes=[1, 5, 10, 20],
        runs=3,
    )

    print()
    print("BENCHMARK RESULTS")
    print("-" * 70)

    for row in result["results"]:
        print(
            f"Cart size: {row['cart_size']:>2} | "
            f"Average: {row['average_seconds']:.4f}s | "
            f"Min: {row['min_seconds']:.4f}s | "
            f"Max: {row['max_seconds']:.4f}s"
        )

    analysis = result["analysis"]

    print()
    print("AUTOMATED ANALYSIS")
    print("-" * 70)

    print(
        f"Scaling:                 "
        f"{analysis['scaling']}"
    )

    print(
        f"Baseline latency:        "
        f"{analysis['baseline_seconds']:.4f}s"
    )

    print(
        f"Per-item overhead:       "
        f"{analysis['estimated_per_item_seconds']:.4f}s"
    )

    print(
        f"Largest-cart latency:    "
        f"{analysis['largest_cart_seconds']:.4f}s"
    )

    print(
        f"Runtime increase:        "
        f"{analysis['time_increase_seconds']:.4f}s"
    )

    print(
        f"Bottleneck candidate:    "
        f"{analysis['bottleneck_candidate']}"
    )

    print(
        f"Severity:                "
        f"{analysis['severity']}"
    )


if __name__ == "__main__":
    main()
