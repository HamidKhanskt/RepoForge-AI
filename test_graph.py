import sys

from src.graph.workflow import agentforge_graph


def main():

    if len(sys.argv) < 2:
        print()
        print("=" * 70)
        print("                    AGENTFORGE")
        print("=" * 70)
        print()
        print("Usage:")
        print()
        print(
            "PYTHONPATH=. python test_graph.py "
            "<github_repository_url>"
        )
        print()
        return

    repository_url = sys.argv[1]

    print()
    print("=" * 70)
    print("                    AGENTFORGE")
    print("=" * 70)

    print()
    print("REPOSITORY")
    print("-" * 70)
    print(repository_url)

    result = agentforge_graph.invoke(
        {
            "task": (
                "Investigate this repository for "
                "performance problems and identify "
                "evidence-grounded optimization opportunities."
            ),
            "repository_url": repository_url,
        }
    )

    print()
    print("STATUS")
    print("-" * 70)
    print(result.get("status", "unknown"))

    print()
    print("FILES DISCOVERED")
    print("-" * 70)

    files = result.get("repository_files", [])

    if files:
        for file in files:
            print(file)
    else:
        print("No repository files discovered.")

    print()
    print("DYNAMIC EVIDENCE")
    print("-" * 70)

    scan = result.get("repository_scan", {})

    if scan:
        print("DYNAMIC REPOSITORY ANALYSIS")
        print()
        print(
            f"Files discovered: "
            f"{len(result.get('repository_files', []))}"
        )

        findings = scan.get(
            "performance_findings",
            scan.get("findings", []),
        )

        print(
            f"Performance findings: "
            f"{len(findings)}"
        )

        for index, finding in enumerate(
            findings,
            start=1,
        ):
            print()
            print(f"Finding {index}")
            print(
                f"Type: "
                f"{finding.get('type', 'unknown')}"
            )
            print(
                f"File: "
                f"{finding.get('file', 'unknown')}"
            )
            print(
                f"Severity: "
                f"{finding.get('severity', 'unknown')}"
            )
            print(
                f"Evidence: "
                f"{finding.get('evidence', 'unknown')}"
            )
    else:
        evidence = result.get(
            "evidence",
            "",
        )

        if evidence:
            print(evidence)
        else:
            print(
                "No dynamic repository evidence available."
            )

    print()
    print("PERFORMANCE")
    print("-" * 70)

    performance = result.get(
        "performance",
        result.get(
            "performance_results",
            None,
        ),
    )

    if performance:
        print(performance)
    else:
        print(
            "No runtime performance benchmark "
            "was performed."
        )
        print()
        print(
            "Static performance evidence was "
            "available from repository analysis."
        )

    print()
    print("CLAIM VERIFICATION")
    print("-" * 70)

    claim_verification = result.get(
        "claim_verification"
    )

    if claim_verification:
        print(claim_verification)
    else:
        print(
            "No claim verification results available."
        )

    print()
    print("EVALUATION")
    print("-" * 70)

    evaluation = result.get(
        "evaluation"
    )

    if evaluation:
        print(evaluation)
    else:
        print(
            "No evaluation results available."
        )

    print()
    print("SOLUTION")
    print("-" * 70)

    solution = result.get(
        "solution",
        "",
    )

    if solution:
        print(solution)
    else:
        print(
            "No solution was generated."
        )

    print()
    print("VERIFICATION")
    print("-" * 70)

    verification = result.get(
        "verification_results"
    )

    if verification:
        print(verification)
    else:
        print(
            "No verification results available."
        )

    print()
    print("EXECUTION LOG")
    print("-" * 70)

    execution_log = result.get(
        "execution_log",
        [],
    )

    if execution_log:
        for event in execution_log:
            print(f"• {event}")
    else:
        for message in result.get(
            "messages",
            [],
        ):
            print(f"• {message}")

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
