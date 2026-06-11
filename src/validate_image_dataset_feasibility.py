"""Validate image dataset feasibility planning files.

This script intentionally validates metadata only. It does not download images,
train a model, or check private/local image files.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEASIBILITY = ROOT / "data" / "image_dataset_feasibility_matrix.csv"
TARGET_CLASSES = ROOT / "data" / "molossoid_visual_target_classes.csv"
IMAGES_DIR = ROOT / "data" / "images"

FEASIBILITY_COLUMNS = {
    "dataset_name",
    "source_type",
    "public_page_url",
    "approximate_classes",
    "approximate_images",
    "annotations",
    "use_case",
    "target_class_check_required",
    "license_terms_check_required",
    "repository_policy",
    "stage12_decision",
}

TARGET_COLUMNS = {
    "class_slug",
    "display_name",
    "role",
    "use_in_stage12",
    "dataset_availability_status",
    "minimum_images_for_baseline",
    "comments",
}

ALLOWED_REPOSITORY_POLICY = {"do_not_commit_downloaded_images"}
ALLOWED_AVAILABILITY_STATUS = {
    "must_verify_from_dataset_metadata",
    "requires_design_not_single_breed_dataset",
}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def require_columns(rows: list[dict[str, str]], required: set[str], name: str) -> None:
    if not rows:
        raise ValueError(f"{name} must contain at least one data row")
    actual = set(rows[0].keys())
    missing = sorted(required - actual)
    if missing:
        raise ValueError(f"{name} is missing columns: {missing}")


def validate_feasibility(rows: list[dict[str, str]]) -> None:
    require_columns(rows, FEASIBILITY_COLUMNS, "image_dataset_feasibility_matrix.csv")
    if len(rows) < 4:
        raise ValueError("Expected at least four public dataset candidates")
    for row in rows:
        if not row["public_page_url"].startswith("https://"):
            raise ValueError(f"Dataset URL must be https: {row['dataset_name']}")
        if row["repository_policy"] not in ALLOWED_REPOSITORY_POLICY:
            raise ValueError(f"Unsafe repository policy for {row['dataset_name']}: {row['repository_policy']}")
        if row["target_class_check_required"].lower() != "yes":
            raise ValueError(f"Target class check must be required for {row['dataset_name']}")
        if row["license_terms_check_required"].lower() != "yes":
            raise ValueError(f"License/terms check must be required for {row['dataset_name']}")


def validate_targets(rows: list[dict[str, str]]) -> None:
    require_columns(rows, TARGET_COLUMNS, "molossoid_visual_target_classes.csv")
    slugs = {row["class_slug"] for row in rows}
    required_targets = {"cane_corso", "dogo_argentino", "presa_canario", "other_unknown"}
    missing = sorted(required_targets - slugs)
    if missing:
        raise ValueError(f"Missing important visual target classes: {missing}")
    for row in rows:
        if row["dataset_availability_status"] not in ALLOWED_AVAILABILITY_STATUS:
            raise ValueError(
                f"Unsafe availability status for {row['class_slug']}: "
                f"{row['dataset_availability_status']}"
            )


def validate_no_committed_images() -> bool:
    """Validate that no downloaded/local image files are present in the repository.

    The course project keeps image-dataset work as feasibility planning only.
    A fresh clone or clean submission archive may not contain data/images at all,
    because Git does not preserve empty directories and downloaded images are
    intentionally excluded from version control. In that case, the repository is
    clean and the validation should pass.
    """

    if not IMAGES_DIR.exists():
        return False

    image_files = [path for path in IMAGES_DIR.rglob("*") if path.suffix.lower() in IMAGE_SUFFIXES]
    if image_files:
        rel = [str(path.relative_to(ROOT)) for path in image_files[:10]]
        raise ValueError(
            "Downloaded image files should not be committed during feasibility planning. "
            f"Found examples: {rel}"
        )

    return True


def main() -> None:
    feasibility_rows = read_csv(FEASIBILITY)
    target_rows = read_csv(TARGET_CLASSES)
    validate_feasibility(feasibility_rows)
    validate_targets(target_rows)
    images_dir_present = validate_no_committed_images()
    print("Image dataset feasibility validation PASS")
    print(f"Dataset candidates: {len(feasibility_rows)}")
    print(f"Target visual classes: {len(target_rows)}")
    if images_dir_present:
        print("No downloaded image files detected in data/images")
    else:
        print("data/images is absent, which is valid for a clean repository clone")


if __name__ == "__main__":
    main()
