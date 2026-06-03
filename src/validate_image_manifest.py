"""Validate the image dataset manifest used by the visual similarity plan.

This script intentionally does not train an image model. It checks whether the
manifest contains the required columns and reports the planned class coverage.

Usage:
    python src/validate_image_manifest.py
    python src/validate_image_manifest.py --manifest data/image_dataset_manifest_example.csv
    python src/validate_image_manifest.py --check-files
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


REQUIRED_COLUMNS = [
    "image_id",
    "dataset_source",
    "source_reference",
    "local_relative_path",
    "breed_label",
    "split",
    "license_or_terms_checked",
    "permission_status",
    "view_type",
    "age_stage",
    "notes",
]

VALID_SPLITS = {"train", "validation", "test"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate image dataset manifest structure.")
    parser.add_argument(
        "--manifest",
        default="data/image_dataset_manifest_example.csv",
        help="Path to the image manifest CSV file.",
    )
    parser.add_argument(
        "--check-files",
        action="store_true",
        help="Also check whether local image paths exist. Disabled by default because the current repository does not commit images.",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Manifest file not found: {path}")

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        return list(reader)


def validate_rows(rows: list[dict[str, str]], check_files: bool) -> None:
    if not rows:
        raise ValueError("Manifest has no data rows.")

    invalid_splits = sorted({row["split"] for row in rows if row["split"] not in VALID_SPLITS})
    if invalid_splits:
        raise ValueError(f"Invalid split values: {invalid_splits}")

    empty_required_values = []
    for row_number, row in enumerate(rows, start=2):
        for column in REQUIRED_COLUMNS:
            if not row.get(column, "").strip():
                empty_required_values.append((row_number, column))

    if empty_required_values:
        raise ValueError(f"Empty required values found: {empty_required_values[:10]}")

    if check_files:
        missing_files = [row["local_relative_path"] for row in rows if not Path(row["local_relative_path"]).exists()]
        if missing_files:
            raise FileNotFoundError(
                "Some image files listed in the manifest do not exist. "
                "This is expected for the example manifest. Missing examples: "
                f"{missing_files[:5]}"
            )


def print_summary(rows: list[dict[str, str]], manifest: Path) -> None:
    breed_counts = Counter(row["breed_label"] for row in rows)
    split_counts = Counter(row["split"] for row in rows)
    source_counts = Counter(row["dataset_source"] for row in rows)

    print("Image manifest validation: PASS")
    print(f"Manifest: {manifest}")
    print(f"Rows: {len(rows)}")
    print("\nRows by breed label:")
    for label, count in sorted(breed_counts.items()):
        print(f"- {label}: {count}")

    print("\nRows by split:")
    for split, count in sorted(split_counts.items()):
        print(f"- {split}: {count}")

    print("\nRows by dataset source:")
    for source, count in sorted(source_counts.items()):
        print(f"- {source}: {count}")

    print("\nNote: This validates manifest structure only. It does not prove dataset quality or train an image model.")


def main() -> None:
    args = parse_args()
    manifest = Path(args.manifest)
    rows = load_rows(manifest)
    validate_rows(rows, check_files=args.check_files)
    print_summary(rows, manifest)


if __name__ == "__main__":
    main()
