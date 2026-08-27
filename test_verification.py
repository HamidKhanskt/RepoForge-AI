from pprint import pprint

from src.tools.verification import verify_repository


def main():
    print("=" * 70)
    print("                 VERIFICATION AGENT")
    print("=" * 70)

    result = verify_repository()

    print()
    print("VERIFICATION RESULTS")
    print("-" * 70)

    pprint(result)


if __name__ == "__main__":
    main()
