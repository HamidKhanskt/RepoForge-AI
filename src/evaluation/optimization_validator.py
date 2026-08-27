import os
import re


def _collect_repository_files(repository_root: str) -> list[str]:
    files = []

    for root, _, filenames in os.walk(repository_root):
        if ".venv" in root:
            continue

        for filename in filenames:
            path = os.path.join(root, filename)

            if path.startswith("./"):
                path = path[2:]

            files.append(path)

    return files


def _collect_python_functions(
    repository_root: str,
) -> list[str]:

    functions = []

    for root, _, filenames in os.walk(repository_root):
        if ".venv" in root:
            continue

        for filename in filenames:
            if not filename.endswith(".py"):
                continue

            path = os.path.join(root, filename)

            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
            except (OSError, UnicodeDecodeError):
                continue

            matches = re.findall(
                r"^\s*(?:async\s+)?def\s+([A-Za-z_]\w*)\s*\(",
                content,
                re.MULTILINE,
            )

            functions.extend(matches)

    return sorted(set(functions))


def _extract_file_references(
    optimization: str,
) -> list[str]:

    return sorted(
        set(
            re.findall(
                r"(?:[\w.-]+/)*[\w.-]+\."
                r"(?:py|js|ts|tsx|jsx|java|go|rs)",
                optimization,
            )
        )
    )


def _extract_function_references(
    optimization: str,
) -> list[str]:

    candidates = re.findall(
        r"\b([A-Za-z_]\w*)\s*\(",
        optimization,
    )

    ignored = {
        "if",
        "for",
        "while",
        "return",
        "print",
        "str",
        "int",
        "float",
        "list",
        "dict",
        "set",
        "len",
        "range",
        "async",
        "await",
    }

    return sorted(
        set(
            candidate
            for candidate in candidates
            if candidate not in ignored
        )
    )


def validate_optimization(
    optimization: str,
    repository_root: str = ".",
) -> dict:
    """
    Deterministically validate an LLM-generated optimization.

    Validation checks:

    1. Referenced files exist.
    2. Referenced functions exist.
    3. Unsupported async/await strategies are rejected.
    """

    files = _collect_repository_files(
        repository_root
    )

    functions = _collect_python_functions(
        repository_root
    )

    optimization_lower = optimization.lower()

    referenced_files = _extract_file_references(
        optimization
    )

    nonexistent_files = [
        path
        for path in referenced_files
        if path not in files
    ]

    referenced_functions = _extract_function_references(
        optimization
    )

    nonexistent_functions = [
        function
        for function in referenced_functions
        if function not in functions
    ]

    checks = []

    # ---------------------------------------------------------
    # FILE EXISTENCE
    # ---------------------------------------------------------

    if nonexistent_files:
        checks.append(
            {
                "check": "file_existence",
                "passed": False,
                "details": (
                    "Referenced files do not exist: "
                    + ", ".join(nonexistent_files)
                ),
            }
        )
    else:
        checks.append(
            {
                "check": "file_existence",
                "passed": True,
                "details": "Referenced files exist.",
            }
        )

    # ---------------------------------------------------------
    # FUNCTION EXISTENCE
    # ---------------------------------------------------------

    if nonexistent_functions:
        checks.append(
            {
                "check": "function_existence",
                "passed": False,
                "details": (
                    "Referenced functions do not exist: "
                    + ", ".join(nonexistent_functions)
                ),
            }
        )
    else:
        checks.append(
            {
                "check": "function_existence",
                "passed": True,
                "details": "Referenced functions exist.",
            }
        )

    # ---------------------------------------------------------
    # ASYNC STRATEGY
    # ---------------------------------------------------------

    if "async/await" in optimization_lower:

        checks.append(
            {
                "check": "async_strategy",
                "passed": False,
                "details": (
                    "Optimization proposes async/await. "
                    "The repository currently uses synchronous "
                    "functions and blocking time.sleep calls."
                ),
            }
        )

    # ---------------------------------------------------------
    # FINAL DECISION
    # ---------------------------------------------------------

    passed = all(
        check["passed"]
        for check in checks
    )

    return {
        "valid": passed,
        "checks": checks,
        "referenced_files": referenced_files,
        "referenced_functions": referenced_functions,
        "nonexistent_files": nonexistent_files,
        "nonexistent_functions": nonexistent_functions,
        "decision": (
            "accepted"
            if passed
            else "rejected"
        ),
    }