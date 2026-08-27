from src.tools.repository import (
    list_files,
    read_file,
    search_code,
)


def main():
    print("\n=== FILES ===")
    print(
        list_files.invoke(
            {"repository_root": "."}
        )
    )

    print("\n=== CHECKOUT.PY ===")
    print(
        read_file.invoke(
            {
                "file_path": "app/checkout.py",
                "repository_root": ".",
            }
        )
    )

    print("\n=== SEARCH: get_product ===")
    print(
        search_code.invoke(
            {
                "query": "get_product",
                "repository_root": ".",
            }
        )
    )


if __name__ == "__main__":
    main()
