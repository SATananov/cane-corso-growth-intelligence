"""Create the local folder structure for future Computer Vision image datasets.

This script does not download images and does not train a model.
It only prepares ignored local folders for future public/consent-based image data.
"""

from __future__ import annotations

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET_CLASSES_PATH = PROJECT_ROOT / "data" / "molossoid_visual_target_classes.csv"
LOCAL_ROOT = PROJECT_ROOT / "data" / "images" / "local_dataset"
SPLITS = ("train", "validation", "test")
IMAGE_SUBFOLDERS = ("downloads", "raw", "processed", "splits", "manifests")


def read_target_classes() -> list[str]:
    if not TARGET_CLASSES_PATH.exists():
        raise FileNotFoundError(f"Missing target class file: {TARGET_CLASSES_PATH}")

    with TARGET_CLASSES_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if "class_slug" not in (reader.fieldnames or []):
            raise ValueError("Target class CSV must include a 'class_slug' column.")
        classes = [row["class_slug"].strip() for row in reader if row.get("class_slug", "").strip()]

    if not classes:
        raise ValueError("No target classes found in data/molossoid_visual_target_classes.csv")

    return classes


def ensure_file(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    classes = read_target_classes()

    LOCAL_ROOT.mkdir(parents=True, exist_ok=True)

    ensure_file(
        LOCAL_ROOT / ".gitignore",
        "*\n!.gitignore\n!README.md\n",
    )
    ensure_file(
        LOCAL_ROOT / "README.md",
        "# Local Image Dataset Folder\n\nThis folder is ignored by Git and is used only for local image experiments.\n",
    )

    for folder in IMAGE_SUBFOLDERS:
        (LOCAL_ROOT / folder).mkdir(parents=True, exist_ok=True)

    for class_slug in classes:
        (LOCAL_ROOT / "raw" / class_slug).mkdir(parents=True, exist_ok=True)
        (LOCAL_ROOT / "processed" / class_slug).mkdir(parents=True, exist_ok=True)

    for split in SPLITS:
        for class_slug in classes:
            (LOCAL_ROOT / "splits" / split / class_slug).mkdir(parents=True, exist_ok=True)

    manifest_path = LOCAL_ROOT / "manifests" / "local_image_manifest.csv"
    ensure_file(
        manifest_path,
        "image_id,dataset_source,source_reference,local_relative_path,breed_label,split,license_or_terms_checked,permission_status,view_type,age_stage,notes\n",
    )

    print("Created local image dataset structure")
    print(f"Root: {LOCAL_ROOT}")
    print(f"Classes: {len(classes)}")
    for class_slug in classes:
        print(f"- {class_slug}")
    print("\nNo images were downloaded or committed. This is a local folder preparation step only.")


if __name__ == "__main__":
    main()
