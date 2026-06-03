"""Validate the local image dataset preparation structure.

This script validates structure and metadata templates only. It does not prove
image quality, class correctness, licensing, or train a Computer Vision model.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = PROJECT_ROOT / "data" / "images" / "local_dataset"
TARGET_CLASSES_PATH = PROJECT_ROOT / "data" / "molossoid_visual_target_classes.csv"
INVENTORY_TEMPLATE = PROJECT_ROOT / "data" / "image_dataset_local_inventory_template.csv"
SPLITS = ("train", "validation", "test")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}

REQUIRED_INVENTORY_COLUMNS = {
    "dataset_name",
    "source_url_or_reference",
    "local_storage_path",
    "class_list_checked",
    "terms_checked",
    "allowed_for_education",
    "download_date",
    "notes",
}


def read_target_classes() -> list[str]:
    if not TARGET_CLASSES_PATH.exists():
        raise FileNotFoundError(f"Missing target class file: {TARGET_CLASSES_PATH}")
    with TARGET_CLASSES_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if "class_slug" not in (reader.fieldnames or []):
            raise ValueError("Target class CSV must include a 'class_slug' column.")
        classes = [row["class_slug"].strip() for row in reader if row.get("class_slug", "").strip()]
    if not classes:
        raise ValueError("No target classes found.")
    return classes


def validate_inventory_template() -> None:
    if not INVENTORY_TEMPLATE.exists():
        raise FileNotFoundError(f"Missing inventory template: {INVENTORY_TEMPLATE}")
    with INVENTORY_TEMPLATE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_INVENTORY_COLUMNS - columns
        if missing:
            raise ValueError(f"Inventory template missing columns: {sorted(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("Inventory template should include example rows.")


def count_images(root: Path) -> Counter:
    counts: Counter[str] = Counter()
    if not root.exists():
        return counts
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            try:
                class_slug = path.parent.name
            except Exception:
                class_slug = "unknown"
            counts[class_slug] += 1
    return counts


def main() -> None:
    classes = read_target_classes()
    validate_inventory_template()

    if not LOCAL_ROOT.exists():
        raise FileNotFoundError(
            "Local image dataset folder does not exist. Run: python src/prepare_image_dataset_structure.py"
        )

    required_paths = [
        LOCAL_ROOT / ".gitignore",
        LOCAL_ROOT / "README.md",
        LOCAL_ROOT / "downloads",
        LOCAL_ROOT / "raw",
        LOCAL_ROOT / "processed",
        LOCAL_ROOT / "splits",
        LOCAL_ROOT / "manifests",
        LOCAL_ROOT / "manifests" / "local_image_manifest.csv",
    ]

    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(f"Missing local image dataset path: {path}")

    for class_slug in classes:
        for subdir in ("raw", "processed"):
            path = LOCAL_ROOT / subdir / class_slug
            if not path.exists():
                raise FileNotFoundError(f"Missing class folder: {path}")

    for split in SPLITS:
        for class_slug in classes:
            path = LOCAL_ROOT / "splits" / split / class_slug
            if not path.exists():
                raise FileNotFoundError(f"Missing split/class folder: {path}")

    raw_counts = count_images(LOCAL_ROOT / "raw")
    processed_counts = count_images(LOCAL_ROOT / "processed")
    split_counts = count_images(LOCAL_ROOT / "splits")

    print("Local image dataset structure validation PASS")
    print(f"Root: {LOCAL_ROOT}")
    print(f"Target classes: {len(classes)}")
    print(f"Raw image files counted: {sum(raw_counts.values())}")
    print(f"Processed image files counted: {sum(processed_counts.values())}")
    print(f"Split image files counted: {sum(split_counts.values())}")
    print("\nNote: zero image files is acceptable at Step 13. This validates local structure only.")
    print("It does not check licensing, image quality, label correctness, or train a model.")


if __name__ == "__main__":
    main()
