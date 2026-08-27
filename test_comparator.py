from pprint import pprint

from src.tools.comparator import compare_benchmarks


def main():
    print("=" * 70)
    print("                 PERFORMANCE COMPARATOR")
    print("=" * 70)

    before = {
        "results": [
            {"cart_size": 1, "average_seconds": 0.40},
            {"cart_size": 10, "average_seconds": 1.10},
            {"cart_size": 20, "average_seconds": 2.00},
        ]
    }

    after = {
        "results": [
            {"cart_size": 1, "average_seconds": 0.32},
            {"cart_size": 10, "average_seconds": 0.55},
            {"cart_size": 20, "average_seconds": 0.75},
        ]
    }

    result = compare_benchmarks(
        before,
        after,
    )

    pprint(result)


if __name__ == "__main__":
    main()
