from pprint import pprint

from src.graph.optimization_loop import (
    optimization_validator_node,
    optimization_router,
)


def main():

    bad_optimization = """
ROOT CAUSE
The database calls are slow.

OPTIMIZATION
Use async/await.

FILES
product.js

IMPLEMENTATION STRATEGY
Rewrite the database layer using async/await.
"""

    state = {
        "optimization": bad_optimization,
        "optimization_attempts": 0,
    }

    result = optimization_validator_node(state)

    print("=" * 70)
    print("              OPTIMIZATION RETRY CONTROLLER")
    print("=" * 70)

    pprint(result)

    state.update(result)

    print()
    print("ROUTER DECISION")
    print("-" * 70)

    print(
        optimization_router(state)
    )


if __name__ == "__main__":
    main()
