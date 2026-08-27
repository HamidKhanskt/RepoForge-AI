import subprocess
import sys
from typing import Any


def run_tests() -> dict[str, Any]:
    """Run the repository test suite and capture the result."""

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    return {
        "passed": process.returncode == 0,
        "return_code": process.returncode,
        "stdout": process.stdout[-4000:],
        "stderr": process.stderr[-2000:],
    }


def verify_repository() -> dict[str, Any]:
    """Run automated repository verification."""

    tests = run_tests()

    return {
        "tests": tests,
        "verification_status": (
            "passed"
            if tests["passed"]
            else "failed"
        ),
    }
