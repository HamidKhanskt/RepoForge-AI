from pprint import pprint

from src.evaluation.optimization_validator import (
    validate_optimization,
)


def run_test(name, optimization):

    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    result = validate_optimization(
        optimization,
        ".",
    )

    pprint(result)

    return result


def main():

    # ---------------------------------------------------------
    # BAD FILE
    # ---------------------------------------------------------

    bad_file = """
ROOT CAUSE
The checkout endpoint is slow.

OPTIMIZATION
Modify the checkout implementation.

FILES
product.js

IMPLEMENTATION STRATEGY
Rewrite the product logic.
"""

    run_test(
        "BAD FILE TEST",
        bad_file,
    )

    # ---------------------------------------------------------
    # BAD FUNCTION
    # ---------------------------------------------------------

    bad_function = """
ROOT CAUSE
get_product() is called repeatedly.

OPTIMIZATION
Use fetch_products() to batch all database calls.

FILES
app/checkout.py
app/database.py

IMPLEMENTATION STRATEGY
Replace repeated get_product() calls with fetch_products().
"""

    run_test(
        "BAD FUNCTION TEST",
        bad_function,
    )

    # ---------------------------------------------------------
    # VALID OPTIMIZATION
    # ---------------------------------------------------------

    valid = """
ROOT CAUSE
The checkout endpoint calls get_product() inside
the product iteration loop, creating per-product
database latency.

OPTIMIZATION
Reduce the number of repeated database calls by
changing the checkout data-access strategy while
preserving the existing synchronous architecture.

FILES
app/checkout.py
app/database.py

IMPLEMENTATION STRATEGY
Modify checkout() so product retrieval is performed
through a batched database operation supported by
the existing repository implementation.

EXPECTED IMPACT
Reduce the approximately 0.084 second per-item
overhead measured by the performance benchmark.

RISKS
The implementation must preserve checkout totals
and product ordering.
"""

    run_test(
        "VALID OPTIMIZATION TEST",
        valid,
    )


if __name__ == "__main__":
    main()