from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = ROOT / "data" / "images" / "local_dataset"
CANDIDATE_DOWNLOADS = LOCAL_ROOT / "downloads" / "stanford_dogs"
CANDIDATE_RAW = LOCAL_ROOT / "raw" / "stanford_dogs"
REPORT_FILE = ROOT / "reports" / "stanford_dogs_local_inspection.md"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def count_images(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS)


def find_class_like_dirs(path: Path) -> list[Path]:
    if not path.exists():
        return []
    result = []
    for child in sorted(path.iterdir()):
        if child.is_dir():
            image_count = count_images(child)
            nested_dirs = [p for p in child.iterdir() if p.is_dir()] if child.exists() else []
            if image_count > 0 or nested_dirs:
                result.append(child)
    return result


def main() -> None:
    download_exists = CANDIDATE_DOWNLOADS.exists()
    raw_exists = CANDIDATE_RAW.exists()
    download_images = count_images(CANDIDATE_DOWNLOADS)
    raw_images = count_images(CANDIDATE_RAW)
    class_dirs = find_class_like_dirs(CANDIDATE_RAW)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Stanford Dogs Local Dataset Inspection",
        "",
        f"Downloads folder: `{CANDIDATE_DOWNLOADS}`",
        f"Downloads folder exists: {download_exists}",
        f"Raw folder: `{CANDIDATE_RAW}`",
        f"Raw folder exists: {raw_exists}",
        f"Image files under downloads: {download_images}",
        f"Image files under raw: {raw_images}",
        f"Top-level class-like directories under raw: {len(class_dirs)}",
        "",
    ]

    if class_dirs:
        lines.append("## Candidate class folders")
        lines.append("")
        for item in class_dirs[:50]:
            lines.append(f"- {item.name}: {count_images(item)} image files")
        if len(class_dirs) > 50:
            lines.append(f"- ... {len(class_dirs) - 50} additional folders omitted from the quick report")
    else:
        lines.extend([
            "No local Stanford Dogs class folders were detected yet.",
            "",
            "This is acceptable before the dataset has been downloaded/extracted.",
            "Step 15 only provides the local download and inspection guide.",
        ])

    lines.extend([
        "",
        "## Responsible boundary",
        "",
        "This inspection does not prove label quality, breed origin, pedigree, registry status, or model accuracy.",
    ])

    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Stanford Dogs local inspection completed")
    print(f"Downloads exists: {download_exists}")
    print(f"Raw exists: {raw_exists}")
    print(f"Raw image files counted: {raw_images}")
    print(f"Candidate class folders: {len(class_dirs)}")
    print(f"Report: {REPORT_FILE}")
    print("Note: zero images/classes is acceptable before the dataset is downloaded locally.")


if __name__ == "__main__":
    main()
