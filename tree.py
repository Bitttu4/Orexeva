from pathlib import Path

IGNORE = {
    ".git",
    ".venv",
    "__pycache__",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".DS_Store",
    "Thumbs.db",
}


def build_tree(directory: Path, prefix: str = "") -> None:
    entries = [
        entry
        for entry in sorted(
            directory.iterdir(),
            key=lambda e: (e.is_file(), e.name.lower())
        )
        if entry.name not in IGNORE
    ]

    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        print(prefix + connector + entry.name)

        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            build_tree(entry, prefix + extension)


if __name__ == "__main__":
    root = Path(".").resolve()
    print(root.name)
    build_tree(root)