from src.graph.workflow import agentforge_graph


def main():
    initial_state = {
        "task": (
            "Investigate why a software application's "
            "checkout endpoint is experiencing high latency."
        ),
        "messages": [],
        "findings": [],
        "hypotheses": [],
        "tool_results": [],
        "test_results": [],
        "iteration": 0,
        "max_iterations": 3,
        "status": "started",
    }

    result = agentforge_graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("                 AGENTFORGE")
    print("=" * 60)

    print(f"\nStatus: {result.get('status')}")
    print(f"Current Agent: {result.get('current_agent')}")
    print(f"Current Step: {result.get('current_step')}")

    print("\nPLAN")
    print("-" * 60)

    for index, step in enumerate(result.get("plan", []), start=1):
        print(f"{index}. {step}")

    print("\nEXECUTION LOG")
    print("-" * 60)

    for message in result.get("messages", []):
        print(f"• {message}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
