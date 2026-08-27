from src.graph.state import AgentForgeState


def planner_node(state: AgentForgeState) -> AgentForgeState:
    task = state.get("task", "")

    plan = [
        "Understand the engineering problem",
        "Inspect the target repository",
        "Collect evidence",
        "Identify root-cause candidates",
        "Propose a solution",
        "Verify the solution",
    ]

    return {
        **state,
        "plan": plan,
        "current_agent": "planner",
        "current_step": "repository_inspection",
        "status": "planning_complete",
        "messages": [
            *state.get("messages", []),
            f"Planner created a plan for: {task}",
        ],
    }
