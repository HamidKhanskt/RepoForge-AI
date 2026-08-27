from typing import TypedDict, Any


class AgentForgeState(TypedDict, total=False):
    # User request
    task: str

    # Repository
    repository_url: str
    repository_path: str
    repository_name: str
    repository_commit: str
    repository_files: list[str]
    repository_scan: dict[str, Any]

    # Planning
    plan: list[str]
    current_step: str

    # Research / evidence
    findings: list[dict]
    hypotheses: list[dict]
    evidence: str
    tool_results: list[dict]

    # Performance
    benchmark: dict[str, Any]
    performance_results: dict[str, Any]

    # Optimization
    proposed_solution: dict
    optimization: str
    optimization_validation: dict[str, Any]

    # Verification
    test_results: list[dict]
    verification_results: dict[str, Any]
    evaluation: dict[str, Any]
    claim_verification: dict[str, Any]

    # Final output
    solution: str
    final_report: str

    # Runtime
    current_agent: str
    status: str
    iteration: int
    max_iterations: int
    messages: list[str]
