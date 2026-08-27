from pathlib import Path
from typing import Any
import os
import shutil
import subprocess
import tempfile

from langchain_core.tools import tool


IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


def _is_url(value: str) -> bool:
    return value.startswith("https://") or value.startswith("http://")


def _clone_repository(repository_url: str) -> Path:
    temp_dir = Path(
        tempfile.mkdtemp(prefix="agentforge_repo_")
    )

    try:
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                repository_url,
                str(temp_dir),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        shutil.rmtree(temp_dir, ignore_errors=True)

        raise RuntimeError(
            "Failed to clone repository: "
            f"{repository_url}\n"
            f"{exc.stderr.strip()}"
        ) from exc

    return temp_dir


def _resolve_root(repository_root: str) -> Path:
    if not repository_root:
        raise ValueError("repository_root is required.")

    if _is_url(repository_root):
        return _clone_repository(repository_root)

    root = Path(repository_root).expanduser().resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Repository does not exist: {repository_root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Repository path is not a directory: {repository_root}"
        )

    return root


def _list_files_impl(repository_root: str = ".") -> list[str]:
    root = _resolve_root(repository_root)

    files = []

    for current_root, dirs, filenames in os.walk(root):
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORED_DIRS
        ]

        current = Path(current_root)

        for filename in filenames:
            path = current / filename
            relative = path.relative_to(root)

            files.append(str(relative))

    return sorted(files)


@tool
def list_files(repository_root: str = ".") -> list[str]:
    """List source files in a local or GitHub repository."""

    return _list_files_impl(repository_root)


def _read_file_impl(
    file_path: str,
    repository_root: str = ".",
) -> str:
    root = _resolve_root(repository_root)

    path = (root / file_path).resolve()

    try:
        path.relative_to(root)
    except ValueError:
        raise ValueError(
            "File path escapes repository root."
        )

    if not path.exists():
        raise FileNotFoundError(
            f"File does not exist: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Not a file: {file_path}"
        )

    try:
        return path.read_text(
            encoding="utf-8"
        )
    except UnicodeDecodeError:
        return "[Binary or unreadable file]"


@tool
def read_file(
    file_path: str,
    repository_root: str = ".",
) -> str:
    """Read a text file from a local or GitHub repository."""

    return _read_file_impl(
        file_path,
        repository_root,
    )


def _search_code_impl(
    query: str,
    repository_root: str = ".",
) -> list[dict[str, Any]]:
    root = _resolve_root(repository_root)

    matches = []

    for current_root, dirs, filenames in os.walk(root):
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORED_DIRS
        ]

        current = Path(current_root)

        for filename in filenames:
            path = current / filename

            try:
                text = path.read_text(
                    encoding="utf-8"
                )
            except (
                UnicodeDecodeError,
                OSError,
            ):
                continue

            for line_number, line in enumerate(
                text.splitlines(),
                start=1,
            ):
                if query.lower() in line.lower():
                    matches.append(
                        {
                            "file": str(
                                path.relative_to(root)
                            ),
                            "line": line_number,
                            "content": line.strip(),
                        }
                    )

    return matches


@tool
def search_code(
    query: str,
    repository_root: str = ".",
) -> list[dict[str, Any]]:
    """Search source code for a text query."""

    return _search_code_impl(
        query,
        repository_root,
    )


def load_repository(
    repository_root: str,
) -> dict[str, Any]:
    """
    Load a local or remote repository.

    GitHub repositories are shallow-cloned into a temporary
    directory before analysis.
    """

    root = _resolve_root(repository_root)

    files = _list_files_impl(str(root))

    contents = {}

    for filename in files:
        path = root / filename

        try:
            contents[filename] = path.read_text(
                encoding="utf-8"
            )
        except (
            UnicodeDecodeError,
            OSError,
        ):
            contents[filename] = (
                "[Binary or unreadable file]"
            )

    return {
        "repository_root": str(root),
        "repository_path": str(root),
        "source_repository": repository_root,
        "files": files,
        "contents": contents,
    }

