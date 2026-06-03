from __future__ import annotations

import argparse
import csv
import random
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = ROOT / "data" / "images" / "local_dataset"
RAW_ROOT = LOCAL_ROOT / "raw" / "stanford_dogs"
DEFAULT_OUTPUT_ROOT = LOCAL_ROOT / "splits" / "stanford_dogs_first_baseline"
SELECTION_REPORT = ROOT / "reports" / "stanford_dogs_baseline_class_selection.csv"
MANIFEST = ROOT / "reports" / "stanford_dogs_baseline_subset_manifest.csv"
SUMMARY = ROOT / "reports" / "stanford_dogs_baseline_subset_summary.md"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def normalize(value: str) -> str:
    value = value.strip()
    if "-" in value and re.match(r"^n\d+", value):
        value = value.split("-", 1)[1]
    value = value.lower().replace("_", " ").replace("-", " ")
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def slug(value: str) -> str:
    return normalize(value).replace(" ", "_")


def image_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(
        path for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def read_selection_rows() -> list[dict[str, str]]:
    if not SELECTION_REPORT.exists():
        return []
    with SELECTION_REPORT.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def is_selected(row: dict[str, str]) -> bool:
    include_value = row.get("include_in_first_baseline", "").strip().lower()
    return include_value in {"yes", "true", "selected", "selected_for_first_baseline"}


def selected_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if is_selected(row)]


def find_candidate_folder(row: dict[str, str]) -> Path | None:
    # Prefer explicit local paths written by Step 16/18 reports.
    explicit_paths = row.get("local_class_paths", "")
    for raw_part in explicit_paths.split(";"):
        part = raw_part.strip()
        if not part:
            continue
        path = ROOT / part
        if path.exists() and image_files(path):
            return path

    # Fallback: match by normalized display name.
    display = row.get("preferred_display_name", "") or row.get("candidate_id", "")
    target = normalize(display)
    if not target:
        return None

    for folder in sorted(RAW_ROOT.rglob("*")):
        if folder.is_dir() and normalize(folder.name) == target and image_files(folder):
            return folder

    return None


def split_for_index(index: int, total: int, train_ratio: float, validation_ratio: float) -> str:
    if total <= 0:
        return "train"
    train_count = int(total * train_ratio)
    validation_count = int(total * validation_ratio)

    if total >= 3:
        train_count = max(1, train_count)
        validation_count = max(1, validation_count)
        if train_count + validation_count >= total:
            validation_count = 1
            train_count = max(1, total - 2)
    else:
        train_count = max(1, total - 1)
        validation_count = 0

    if index < train_count:
        return "train"
    if index < train_count + validation_count:
        return "validation"
    return "test"


def safe_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def write_empty_outputs(reason: str) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "row_id", "source_dataset", "label", "display_name", "split",
            "source_relative_path", "split_relative_path", "original_class_folder",
            "filename", "copied",
        ])
        writer.writeheader()

    SUMMARY.write_text(
        "# Stanford Dogs Baseline Image Subset Summary\n\n"
        f"No image subset rows were prepared. Reason: {reason}\n\n"
        "This is acceptable in a clean repository before local image data is downloaded/extracted.\n"
        "Actual image files must remain local-only and must not be committed to GitHub.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a local Stanford Dogs baseline image subset.")
    parser.add_argument("--max-per-class", type=int, default=80)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train-ratio", type=float, default=0.70)
    parser.add_argument("--validation-ratio", type=float, default=0.15)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--no-reset", action="store_true", help="Do not clear the previous local subset before copying.")
    args = parser.parse_args()

    rows = read_selection_rows()
    selected = selected_rows(rows)

    if not rows:
        write_empty_outputs("missing selection report")
        print("Stanford Dogs baseline subset preparation completed")
        print("Prepared rows: 0")
        print("Reason: missing selection report")
        print(f"Manifest: {MANIFEST}")
        print(f"Summary:  {SUMMARY}")
        return

    if not selected:
        write_empty_outputs("no selected first-baseline classes in selection report")
        print("Stanford Dogs baseline subset preparation completed")
        print("Prepared rows: 0")
        print("Reason: no selected first-baseline classes")
        print(f"Manifest: {MANIFEST}")
        print(f"Summary:  {SUMMARY}")
        return

    output_root = args.output_root
    if output_root.exists() and not args.no_reset:
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)
    manifest_rows: list[dict[str, str]] = []
    skipped: list[str] = []

    for row in selected:
        display_name = row.get("preferred_display_name", "") or row.get("candidate_id", "unknown")
        label = slug(display_name)
        class_folder = find_candidate_folder(row)
        if class_folder is None:
            skipped.append(display_name)
            continue

        files = image_files(class_folder)
        rng.shuffle(files)
        selected_files = files[: max(0, args.max_per_class)]

        for index, source in enumerate(selected_files):
            split = split_for_index(index, len(selected_files), args.train_ratio, args.validation_ratio)
            destination_name = f"{class_folder.name}__{source.name}"
            destination = output_root / split / label / destination_name
            safe_copy(source, destination)

            manifest_rows.append({
                "row_id": str(len(manifest_rows) + 1),
                "source_dataset": "Stanford Dogs / ImageNet Dogs",
                "label": label,
                "display_name": display_name,
                "split": split,
                "source_relative_path": str(source.relative_to(ROOT)),
                "split_relative_path": str(destination.relative_to(ROOT)),
                "original_class_folder": str(class_folder.relative_to(ROOT)),
                "filename": source.name,
                "copied": "true",
            })

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "row_id", "source_dataset", "label", "display_name", "split",
        "source_relative_path", "split_relative_path", "original_class_folder",
        "filename", "copied",
    ]
    with MANIFEST.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    by_label = Counter(row["label"] for row in manifest_rows)
    by_split = Counter(row["split"] for row in manifest_rows)
    by_label_split: dict[str, Counter[str]] = defaultdict(Counter)
    for row in manifest_rows:
        by_label_split[row["label"]][row["split"]] += 1

    lines = [
        "# Stanford Dogs Baseline Image Subset Summary",
        "",
        f"Output root: `{output_root}`",
        f"Selection report: `{SELECTION_REPORT}`",
        f"Manifest: `{MANIFEST}`",
        f"Max images per class: {args.max_per_class}",
        f"Random seed: {args.seed}",
        f"Prepared image rows: {len(manifest_rows)}",
        f"Skipped selected classes: {len(skipped)}",
        "",
        "## Counts by label",
        "",
        "| Label | Count |",
        "|---|---:|",
    ]
    for label, count in sorted(by_label.items()):
        lines.append(f"| {label} | {count} |")

    lines.extend(["", "## Counts by split", "", "| Split | Count |", "|---|---:|"])
    for split in ["train", "validation", "test"]:
        lines.append(f"| {split} | {by_split.get(split, 0)} |")

    lines.extend(["", "## Counts by label and split", "", "| Label | Train | Validation | Test |", "|---|---:|---:|---:|"])
    for label in sorted(by_label_split):
        split_counts = by_label_split[label]
        lines.append(
            f"| {label} | {split_counts.get('train', 0)} | {split_counts.get('validation', 0)} | {split_counts.get('test', 0)} |"
        )

    if skipped:
        lines.extend(["", "## Skipped selected classes", ""])
        for item in skipped:
            lines.append(f"- {item}")

    lines.extend([
        "",
        "## Responsible boundary",
        "",
        "This subset supports a future educational visual-similarity baseline only.",
        "It does not prove breed, pedigree, genetic origin, registry status, certification or veterinary condition.",
        "Actual image files are local-only and must not be committed to GitHub.",
    ])
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Stanford Dogs baseline image subset preparation completed")
    print(f"Selected classes from report: {len(selected)}")
    print(f"Prepared image rows: {len(manifest_rows)}")
    print(f"Skipped selected classes: {len(skipped)}")
    print(f"Output root: {output_root}")
    print(f"Manifest: {MANIFEST}")
    print(f"Summary:  {SUMMARY}")
    print("Note: copied images are local-only and must not be committed to GitHub.")


if __name__ == "__main__":
    main()
