from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from src.graph.state import AgentForgeState

from src.agents.planner import planner_node
from src.agents.evaluator import evaluator_node

from src.graph.nodes import (
    repository_agent_node,
    evidence_node,
    performance_agent_node,
    claim_verification_node,
    solution_node,
    verification_agent_node,
)


def evaluation_router(
    state: AgentForgeState,
) -> str:

    """
    Continue into solution generation after evaluation.

    Evaluation measures evidence quality. It should not
    prevent AgentForge from producing an engineering
    recommendation.
    """

    return "solution"


def report_node(
    state: AgentForgeState,
) -> AgentForgeState:

    evaluation = state.get(
        "evaluation",
        {},
    )

    report = f"""
============================================================
                    AGENTFORGE REPORT
============================================================

TASK
----
{state.get("task", "")}

REPOSITORY
----------
{state.get("repository_url") or state.get("repository_path", "")}

STATUS
------
{state.get("status", "")}

EVALUATION
----------
Decision: {evaluation.get("status")}
Score: {evaluation.get("score")}
Reason: {evaluation.get("reason")}

VERIFIED EVIDENCE
-----------------
"""

    for result in state.get(
        "tool_results",
        [],
    ):
        report += (
            "\n"
            + str(
                result.get(
                    "result",
                    "",
                )
            )
        )

    report += """

PERFORMANCE ANALYSIS
--------------------
"""

    performance = state.get(
        "performance",
        {},
    )

    if performance:

        analysis = performance.get(
            "analysis",
            {},
        )

        report += (
            "\nBenchmark: "
            + str(
                performance.get(
                    "benchmark",
                    "",
                )
            )
        )

        report += (
            "\nFindings: "
            + str(
                performance.get(
                    "findings_count",
                    0,
                )
            )
        )

        for key, value in analysis.items():

            report += (
                f"\n{key}: {value}"
            )

    else:

        report += (
            "\nNo performance analysis available."
        )

    report += """

SOLUTION
--------
"""

    report += str(
        state.get(
            "solution",
            "No solution was generated.",
        )
    )

    verification = state.get(
        "verification_results",
        {},
    )

    report += """

VERIFICATION
------------
"""

    report += str(
        verification
    )

    report += """

============================================================
"""

    return {
        **state,

        "final_report": report,

        "current_agent": "reporter",
        "current_step": "complete",

        "status": "completed",

        "messages": [
            *state.get(
                "messages",
                [],
            ),
            "Final engineering report generated.",
        ],
    }


def build_graph():

    graph = StateGraph(
        AgentForgeState
    )

    graph.add_node(
        "planner",
        planner_node,
    )

    graph.add_node(
        "repository_agent",
        repository_agent_node,
    )

    graph.add_node(
        "evidence",
        evidence_node,
    )

    graph.add_node(
        "performance",
        performance_agent_node,
    )

    graph.add_node(
        "claim_verification",
        claim_verification_node,
    )

    graph.add_node(
        "evaluator",
        evaluator_node,
    )

    graph.add_node(
        "solution",
        solution_node,
    )

    graph.add_node(
        "verification",
        verification_agent_node,
    )

    graph.add_node(
        "report",
        report_node,
    )

    graph.add_edge(
        START,
        "planner",
    )

    graph.add_edge(
        "planner",
        "repository_agent",
    )

    graph.add_edge(
        "repository_agent",
        "evidence",
    )

    graph.add_edge(
        "evidence",
        "performance",
    )

    graph.add_edge(
        "performance",
        "claim_verification",
    )

    graph.add_edge(
        "claim_verification",
        "evaluator",
    )

    graph.add_conditional_edges(
        "evaluator",
        evaluation_router,
        {
            "solution": "solution",
        },
    )

    graph.add_edge(
        "solution",
        "verification",
    )

    graph.add_edge(
        "verification",
        "report",
    )

    graph.add_edge(
        "report",
        END,
    )

    return graph.compile()


agentforge_graph = build_graph()
