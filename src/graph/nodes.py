from src.graph.state import AgentForgeState

from src.tools.repository import load_repository
from src.tools.scanner import (
    scan_repository,
    format_scan_results,
)

from src.evaluation.claim_verifier import verify_claims


def repository_agent_node(
    state: AgentForgeState,
) -> AgentForgeState:

    repository_url = state.get(
        "repository_url",
        "",
    )

    repository_path = state.get(
        "repository_path",
        "",
    )

    if repository_url:
        repository = load_repository(
            repository_url
        )

        repository_path = repository[
            "repository_path"
        ]

    if not repository_path:
        raise ValueError(
            "AgentForge requires repository_url "
            "or repository_path."
        )

    scan = scan_repository(
        repository_path
    )

    evidence = format_scan_results(
        scan
    )

    finding = {
        "agent": "repository_agent",
        "content": evidence,
    }

    return {
        **state,

        "repository_path": repository_path,

        "repository_name": state.get(
            "repository_name",
            repository_url.split("/")[-1].replace(
                ".git",
                "",
            )
            if repository_url
            else "",
        ),

        "repository_files": scan.get(
            "files",
            [],
        ),

        "repository_scan": scan,

        "evidence": evidence,

        "findings": [
            *state.get(
                "findings",
                [],
            ),
            finding,
        ],

        "tool_results": [
            *state.get(
                "tool_results",
                [],
            ),
            {
                "tool": "dynamic_repository_scanner",
                "result": scan,
            },
        ],

        "current_agent": "repository_agent",
        "current_step": "claim_verification",
        "status": "repository_investigation_complete",

        "messages": [
            *state.get(
                "messages",
                [],
            ),
            "Repository loaded and dynamically analyzed.",
        ],
    }


def evidence_node(
    state: AgentForgeState,
) -> AgentForgeState:

    return {
        **state,

        "current_agent": "evidence_inspector",
        "current_step": "performance",
        "status": "evidence_collection_complete",

        "messages": [
            *state.get(
                "messages",
                [],
            ),
            "Dynamic repository evidence is available.",
        ],
    }


def claim_verification_node(
    state: AgentForgeState,
) -> AgentForgeState:

    findings = state.get(
        "findings",
        [],
    )

    claim_text = "\n".join(
        str(
            finding.get(
                "content",
                "",
            )
        )
        for finding in findings
    )

    verification = verify_claims(
        claim_text
    )

    return {
        **state,

        "claim_verification": verification,

        "current_agent": "claim_verifier",
        "current_step": "evaluation",

        "status": (
            "claims_verified"
            if verification["supported"]
            else "claims_rejected"
        ),

        "messages": [
            *state.get(
                "messages",
                [],
            ),
            (
                "Claim verification score: "
                f"{verification['score']:.2f}"
            ),
        ],
    }


def performance_agent_node(
    state: AgentForgeState,
) -> AgentForgeState:

    from src.tools.performance import (
        benchmark_repository,
    )

    repository_path = state.get(
        "repository_path",
        "",
    )

    repository_files = state.get(
        "repository_files",
        [],
    )

    try:

        benchmark = benchmark_repository(
            repository_path=repository_path,
            repository_files=repository_files,
        )

        return {
            **state,

            "performance": benchmark,

            "performance_results": benchmark,

            "findings": [
                *state.get(
                    "findings",
                    [],
                ),
                {
                    "agent": "performance_agent",
                    "content": benchmark,
                },
            ],

            "tool_results": [
                *state.get(
                    "tool_results",
                    [],
                ),
                {
                    "tool": "dynamic_performance_analysis",
                    "result": benchmark,
                },
            ],

            "current_agent": "performance_agent",
            "current_step": "solution",
            "status": "performance_complete",

            "messages": [
                *state.get(
                    "messages",
                    [],
                ),
                "Dynamic performance analysis completed.",
            ],
        }

    except Exception as exc:

        return {
            **state,

            "performance": None,

            "current_agent": "performance_agent",
            "current_step": "solution",
            "status": "performance_skipped",

            "messages": [
                *state.get(
                    "messages",
                    [],
                ),
                (
                    "Runtime performance benchmark skipped: "
                    f"{type(exc).__name__}: {exc}"
                ),
            ],
        }


def solution_node(
    state: AgentForgeState,
) -> AgentForgeState:

    from src.agents.solution_agent import (
        solution_agent,
    )

    repository_scan = state.get(
        "repository_scan",
        {},
    )

    performance_findings = repository_scan.get(
        "performance_findings",
        [],
    )

    evidence = state.get(
        "evidence",
        "",
    )

    benchmark = state.get(
        "performance",
        None,
    )

    prompt = f"""
You are a senior software performance engineer.

Analyze ONLY the verified repository evidence below.

REPOSITORY:
{state.get("repository_url") or state.get("repository_path")}

FILES:
{state.get("repository_files", [])}

STATIC PERFORMANCE FINDINGS:
{performance_findings}

REPOSITORY EVIDENCE:
{evidence}

RUNTIME PERFORMANCE DATA:
{benchmark}

STRICT RULES:

1. Never invent facts.

2. Never claim a database bottleneck unless the evidence
   explicitly identifies database operations as the cause.

3. Never claim an API bottleneck unless the evidence
   explicitly identifies an API operation.

4. Never claim recursion unless recursion appears in the evidence.

5. Never claim measured latency, speedup, percentage improvement,
   or benchmark results unless runtime benchmark data exists.

6. Static analysis proves that a pattern exists.
   It does NOT prove that the pattern is the dominant runtime
   bottleneck.

7. A function called inside a loop may be an optimization
   opportunity, but describe it as a potential performance risk
   unless runtime measurements confirm the impact.

8. Prioritize high-severity findings.

9. Recommendations must correspond directly to observed findings.

10. If no runtime benchmark exists, explicitly state:

"Runtime performance impact was not experimentally measured."

Produce exactly these sections:

OBSERVED EVIDENCE

ROOT CAUSE / PERFORMANCE RISK

PROPOSED SOLUTION

WHY IT SHOULD HELP

TRADEOFFS

IMPLEMENTATION PLAN

VERIFICATION STATUS

Keep the recommendation concise, technical, and evidence-grounded.
"""

    result = solution_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        }
    )

    final_message = result[
        "messages"
    ][-1]

    return {
        **state,

        "solution": final_message.content,

        "current_agent": "solution_agent",
        "current_step": "verification",
        "status": "solution_generated",

        "messages": [
            *state.get(
                "messages",
                [],
            ),
            (
                "Solution agent generated an "
                "evidence-grounded recommendation."
            ),
        ],
    }


def verification_agent_node(
    state: AgentForgeState,
) -> AgentForgeState:

    from src.tools.verification import verify_repository

    try:

        verification = verify_repository()

    except Exception as exc:

        verification = {
            "tests": {
                "passed": False,
                "return_code": -1,
                "stdout": "",
                "stderr": str(exc),
            },
            "verification_status": "failed",
        }

    passed = (
        verification.get(
            "verification_status"
        )
        == "passed"
    )

    return {
        **state,

        "verification_results": verification,

        "current_agent": "verification_agent",
        "current_step": "report",

        "status": (
            "verification_passed"
            if passed
            else "verification_failed"
        ),

        "messages": [
            *state.get(
                "messages",
                [],
            ),
            (
                "Verification tests "
                + (
                    "passed."
                    if passed
                    else "failed."
                )
            ),
        ],
    }
