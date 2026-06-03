from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = ROOT / "data" / "images" / "local_dataset"
RAW_ROOT = LOCAL_ROOT / "raw" / "stanford_dogs"
DOWNLOAD_ROOT = LOCAL_ROOT / "downloads" / "stanford_dogs"
CANDIDATES_FILE = ROOT / "data" / "stanford_dogs_baseline_class_candidates.csv"
REPORT_MD = ROOT / "reports" / "stanford_dogs_real_class_inspection.md"
REPORT_CSV = ROOT / "reports" / "stanford_dogs_real_class_inspection.csv"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def normalize(value: str) -> str:
    value = value.strip()
    if "-" in value and re.match(r"^n\d+", value):
        value = value.split("-", 1)[1]
    value = value.lower().replace("_", " ").replace("-", " ")
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def count_images(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS)


def class_folder_candidates() -> list[Path]:
    roots = [RAW_ROOT, RAW_ROOT / "Images", DOWNLOAD_ROOT / "Images"]
    found: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for child in root.iterdir():
            if child.is_dir() and count_images(child) > 0:
                found.append(child)
    unique: list[Path] = []
    seen = set()
    for path in sorted(found, key=lambda p: str(p)):
        key = str(path.resolve())
        if key not in seen:
            unique.append(path)
            seen.add(key)
    return unique


def read_candidates() -> list[dict[str, str]]:
    if not CANDIDATES_FILE.exists():
        return []
    with CANDIDATES_FILE.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def candidate_aliases(row: dict[str, str]) -> set[str]:
    raw = row.get("expected_stanford_label_aliases", "")
    aliases = {normalize(part) for part in raw.split("|") if part.strip()}
    aliases.add(normalize(row.get("preferred_display_name", "")))
    return {item for item in aliases if item}


def main() -> None:
    folders = class_folder_candidates()
    candidates = read_candidates()
    normalized_folders = [(path, normalize(path.name), count_images(path)) for path in folders]

    rows: list[dict[str, str]] = []
    for path, norm, image_count in normalized_folders:
        matched_targets = []
        for candidate in candidates:
            if norm in candidate_aliases(candidate):
                matched_targets.append(candidate.get("preferred_display_name", ""))
        rows.append({
            "local_class_folder": str(path.relative_to(ROOT)),
            "folder_name": path.name,
            "normalized_label": norm,
            "image_count": str(image_count),
            "matched_project_targets": "; ".join(item for item in matched_targets if item),
            "usable_for_first_baseline": "yes_if_reviewed" if matched_targets else "possible_other_class_or_ignore",
        })

    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with REPORT_CSV.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
            writer.writeheader(); writer.writerows(rows)
    else:
        with REPORT_CSV.open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["local_class_folder", "folder_name", "normalized_label", "image_count", "matched_project_targets", "usable_for_first_baseline"])

    matched_rows = [row for row in rows if row["matched_project_targets"]]
    lines = [
        "# Stanford Dogs Real Class Inspection",
        "",
        f"Raw root: `{RAW_ROOT}`",
        f"Download root: `{DOWNLOAD_ROOT}`",
        f"Class folders with images detected: {len(rows)}",
        f"Class folders matching project target candidates: {len(matched_rows)}",
        "",
    ]
    if rows:
        lines.extend([
            "## Detected class folders",
            "",
            "| Folder | Normalized label | Images | Matched project target | Decision |",
            "|---|---|---:|---|---|",
        ])
        for row in rows[:120]:
            lines.append(f"| `{row['folder_name']}` | {row['normalized_label']} | {row['image_count']} | {row['matched_project_targets'] or '-'} | {row['usable_for_first_baseline']} |")
    else:
        lines.extend([
            "No local Stanford Dogs class folders with images were detected yet.",
            "",
            "This is acceptable before `images.tar` is downloaded and extracted locally.",
        ])
    lines.extend([
        "",
        "## Responsible boundary",
        "",
        "This inspection only reports local folder evidence. It does not prove label quality, breed origin, pedigree, registry status, certificate status, or model accuracy.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Stanford Dogs real class inspection completed")
    print(f"Raw root: {RAW_ROOT}")
    print(f"Class folders with images detected: {len(rows)}")
    print(f"Matched project candidate folders: {len(matched_rows)}")
    print(f"CSV report: {REPORT_CSV}")
    print(f"Markdown report: {REPORT_MD}")
    if not rows:
        print("Note: zero folders is acceptable before images.tar is downloaded and extracted locally.")


if __name__ == "__main__":
    main()
