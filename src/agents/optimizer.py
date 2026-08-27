from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


OPTIMIZER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a senior Python performance engineer.

You are analyzing an EXISTING Python repository.

Your job is to propose ONE safe, evidence-grounded optimization.

STRICT RULES:

1. You may ONLY reference files listed under REPOSITORY FILES.
2. You may ONLY reference functions explicitly supported by EVIDENCE.
3. NEVER invent a filename.
4. NEVER invent a function.
5. NEVER invent a framework, database, API, or architecture.
6. NEVER recommend async/await unless EVIDENCE explicitly proves
   that the repository already uses an asynchronous database/API layer.
7. NEVER claim that you implemented the optimization.
8. NEVER invent benchmark numbers.
9. Use the measured bottleneck as the primary optimization target.
10. Prefer a small, realistic Python change.
11. If the evidence shows an N+1 pattern, prefer batching the database
    operation rather than introducing an unsupported architecture.
12. Every referenced file MUST appear exactly in REPOSITORY FILES.

The repository is the source of truth.

Return exactly these sections:

ROOT CAUSE
OPTIMIZATION
FILES
IMPLEMENTATION STRATEGY
EXPECTED IMPACT
RISKS
""",
        ),
        (
            "human",
            """TASK:
{task}

REPOSITORY FILES:
{repository_files}

EVIDENCE:
{evidence}

PERFORMANCE:
{benchmark}

PREVIOUS ATTEMPT:
{previous_attempt}

VALIDATION FEEDBACK:
{validation_feedback}

Produce ONE optimization proposal.

Before producing the answer, internally verify:

- Every file you mention exists in REPOSITORY FILES.
- Every function you mention is supported by EVIDENCE.
- Your recommendation addresses the measured bottleneck.
- You are not assuming an asynchronous architecture.
- You are not inventing benchmark results.

If the previous attempt was rejected, correct the exact problem
identified by the validator.
""",
        ),
    ]
)


def _discover_repository_files():
    """Return real Python source files from the target repository."""
    root = Path("app")

    if not root.exists():
        return []

    return sorted(
        str(path)
        for path in root.rglob("*.py")
        if path.is_file()
    )


def optimizer_node(state):
    task = state.get("task", "")

    evidence = state.get(
        "evidence",
        "",
    )

    benchmark = state.get(
        "benchmark",
        {},
    )

    previous_attempt = state.get(
        "optimization",
        "",
    )

    validation = state.get(
        "optimization_validation",
        {},
    )

    # Never trust an LLM-generated repository file list.
    # Discover the actual files directly from the repository.
    repository_files = _discover_repository_files()

    validation_feedback = validation.get(
        "checks",
        [],
    )

    chain = OPTIMIZER_PROMPT | llm

    result = chain.invoke(
        {
            "task": task,
            "repository_files": "\n".join(
                repository_files
            ),
            "evidence": evidence,
            "benchmark": benchmark,
            "previous_attempt": previous_attempt,
            "validation_feedback": validation_feedback,
        }
    )

    return {
        **state,
        "optimization": result.content,
        "repository_files": repository_files,
        "current_agent": "optimizer",
        "status": "optimization_generated",
    }