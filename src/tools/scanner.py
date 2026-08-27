from pathlib import Path
import ast


IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
}


def discover_files(repository_path: str) -> list[str]:
    root = Path(repository_path).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Repository does not exist: {root}"
        )

    files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(
            part in IGNORED_DIRS
            for part in path.relative_to(root).parts
        ):
            continue

        files.append(
            str(path.relative_to(root))
        )

    return sorted(files)


def _python_files(root: Path) -> list[Path]:
    files = []

    for path in root.rglob("*.py"):
        if any(
            part in IGNORED_DIRS
            for part in path.relative_to(root).parts
        ):
            continue

        files.append(path)

    return sorted(files)


def scan_repository(repository_path: str) -> dict:
    """
    Dynamically inspect a repository for concrete
    performance-related code patterns.

    This scanner does not assume a particular project,
    framework, filename, or function name.
    """

    root = Path(repository_path).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Repository does not exist: {root}"
        )

    files = discover_files(str(root))
    findings = []

    for path in _python_files(root):
        try:
            source = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source)

        except (SyntaxError, OSError):
            continue

        relative = str(
            path.relative_to(root)
        )

        functions = {
            node.name: node
            for node in ast.walk(tree)
            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
        }

        # Detect blocking sleep calls.
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "sleep"
            ):
                findings.append(
                    {
                        "type": "blocking_sleep",
                        "file": relative,
                        "severity": "medium",
                        "evidence": (
                            "A blocking sleep() call was "
                            "detected."
                        ),
                    }
                )

        # Detect function calls inside loops.
        for loop in ast.walk(tree):
            if not isinstance(
                loop,
                (
                    ast.For,
                    ast.AsyncFor,
                    ast.While,
                ),
            ):
                continue

            calls = [
                node
                for node in ast.walk(loop)
                if isinstance(node, ast.Call)
            ]

            for call in calls:
                if isinstance(
                    call.func,
                    ast.Name,
                ):
                    function_name = (
                        call.func.id
                    )

                    if function_name in functions:
                        findings.append(
                            {
                                "type": "repeated_function_call",
                                "file": relative,
                                "severity": "high",
                                "function": function_name,
                                "evidence": (
                                    f"{function_name}() is "
                                    "called inside a loop."
                                ),
                            }
                        )

        # Detect repeated calls to the same function
        # within a function body.
        for function_name, function_node in functions.items():
            call_names = []

            for node in ast.walk(function_node):
                if isinstance(
                    node,
                    ast.Call,
                ) and isinstance(
                    node.func,
                    ast.Name,
                ):
                    call_names.append(
                        node.func.id
                    )

            counts = {}

            for name in call_names:
                counts[name] = (
                    counts.get(name, 0) + 1
                )

            for called_name, count in counts.items():
                if count >= 3:
                    findings.append(
                        {
                            "type": "repeated_operation",
                            "file": relative,
                            "severity": "medium",
                            "function": function_name,
                            "evidence": (
                                f"{called_name}() is called "
                                f"{count} times inside "
                                f"{function_name}()."
                            ),
                        }
                    )

    # Remove exact duplicate findings.
    unique = []
    seen = set()

    for finding in findings:
        key = tuple(
            sorted(finding.items())
        )

        if key not in seen:
            seen.add(key)
            unique.append(finding)

    return {
        "repository_path": str(root),
        "file_count": len(files),
        "files": files,
        "findings": unique,
        "finding_count": len(unique),
    }


def format_scan_results(scan: dict) -> str:
    output = [
        "DYNAMIC REPOSITORY ANALYSIS",
        "",
        f"Files discovered: {scan['file_count']}",
        f"Performance findings: {scan['finding_count']}",
        "",
    ]

    if not scan["findings"]:
        output.append(
            "No supported performance patterns detected."
        )
        return "\n".join(output)

    for index, finding in enumerate(
        scan["findings"],
        start=1,
    ):
        output.extend(
            [
                f"Finding {index}",
                f"Type: {finding['type']}",
                f"File: {finding['file']}",
                f"Severity: {finding['severity']}",
                f"Evidence: {finding['evidence']}",
                "",
            ]
        )

    return "\n".join(output)
