from src.evaluation.optimization_validator import (
    validate_optimization,
)


MAX_OPTIMIZATION_ATTEMPTS = 3


def optimization_validator_node(state):
    optimization = state.get(
        "optimization",
        "",
    )

    attempts = state.get(
        "optimization_attempts",
        0,
    )

    attempts += 1

    validation = validate_optimization(
        optimization,
        ".",
    )

    return {
        "optimization_validation": validation,
        "optimization_attempts": attempts,
        "current_agent": "optimization_validator",
        "status": (
            "optimization_accepted"
            if validation["valid"]
            else "optimization_rejected"
        ),
    }


def optimization_router(state):
    validation = state.get(
        "optimization_validation",
        {},
    )

    attempts = state.get(
        "optimization_attempts",
        0,
    )

    if validation.get("valid"):
        return "accepted"

    if attempts >= MAX_OPTIMIZATION_ATTEMPTS:
        return "failed"

    return "retry"
