from pathlib import Path


REQUIRED_EXAMPLES = (
    "spe login",
    "spe play",
    "spe pause",
)

DOC_FILES = (
    Path("wiki/en/commands.md"),
    Path("wiki/de/commands.md"),
)


def main() -> int:
    missing = []
    for file_path in DOC_FILES:
        content = file_path.read_text(encoding="utf-8").lower()
        for example in REQUIRED_EXAMPLES:
            if example not in content:
                missing.append(f"{file_path}: missing '{example}'")

    if missing:
        print("Localized docs check failed:")
        for issue in missing:
            print(f"- {issue}")
        return 1

    print("Localized docs check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
