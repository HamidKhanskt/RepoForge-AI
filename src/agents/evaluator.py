from src.graph.state import AgentForgeState


def evaluator_node(state: AgentForgeState) -> AgentForgeState:
    claim_verification = state.get(
        "claim_verification",
        {},
    )

    tool_results = state.get(
        "tool_results",
        [],
    )

    claim_score = claim_verification.get(
        "score",
        0.0,
    )

    # Deterministic evidence is considered independently
    # from LLM-generated claims.
    has_deterministic_evidence = any(
        result.get("tool") == "inspect_performance_patterns"
        and result.get("result")
        for result in tool_results
    )

    if has_deterministic_evidence:
        evidence_score = 1.0
    else:
        evidence_score = claim_score

    if evidence_score >= 0.75:
        decision = "accepted"
        status = "evaluation_passed"
        next_step = "solution"

        reason = (
            "Investigation contains sufficient "
            "verified repository evidence."
        )

    else:
        decision = "rejected"
        status = "evaluation_failed"
        next_step = "report"

        reason = (
            "Investigation does not contain sufficient "
            "verified evidence."
        )

    evaluation = {
        "status": decision,
        "score": evidence_score,
        "claim_score": claim_score,
        "deterministic_evidence": has_deterministic_evidence,
        "reason": reason,
    }

    return {
        **state,
        "evaluation": evaluation,
        "current_agent": "evaluator",
        "current_step": next_step,
        "status": status,
        "messages": [
            *state.get("messages", []),
            f"Evaluator score: {evidence_score:.2f}",
            f"Evaluator decision: {decision}",
        ],
    }
