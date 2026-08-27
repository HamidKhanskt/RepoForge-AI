from src.agents.repository_agent import repository_agent


def main():
    result = repository_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Investigate the demo repository. "
                        "Look for potential performance problems "
                        "in the checkout implementation. "
                        "Use the repository tools and provide "
                        "evidence for your findings."
                    ),
                }
            ]
        }
    )

    print("\n" + "=" * 70)
    print("              REPOSITORY AGENT")
    print("=" * 70)

    for message in result["messages"]:
        print(f"\n[{message.type}]")

        if isinstance(message.content, str):
            print(message.content)

        elif message.content:
            print(message.content)

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
