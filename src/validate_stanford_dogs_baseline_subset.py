from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "reports" / "stanford_dogs_baseline_subset_manifest.csv"
SUMMARY = ROOT / "reports" / "stanford_dogs_baseline_subset_summary.md"
EXPECTED_COLUMNS = {
    "row_id",
    "source_dataset",
    "label",
    "display_name",
    "split",
    "source_relative_path",
    "split_relative_path",
    "original_class_folder",
    "filename",
    "copied",
}


def fail(message: str) -> None:
    raise SystemExit(f"Stanford Dogs baseline subset validation FAIL: {message}")


def main() -> None:
    if not MANIFEST.exists():
        fail(f"missing manifest: {MANIFEST}")
    if not SUMMARY.exists():
        fail(f"missing summary: {SUMMARY}")

    with MANIFEST.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])
        missing = EXPECTED_COLUMNS - columns
        if missing:
            fail(f"manifest missing columns: {sorted(missing)}")
        rows = list(reader)

    if not rows:
        print("Stanford Dogs baseline subset validation PASS")
        print("Manifest rows: 0")
        print("Note: zero rows are acceptable in a clean repository before local image extraction/subset preparation.")
        return

    labels = Counter(row["label"] for row in rows)
    splits = Counter(row["split"] for row in rows)
    invalid_splits = sorted(set(splits) - {"train", "validation", "test"})
    if invalid_splits:
        fail(f"invalid split names: {invalid_splits}")

    missing_files = []
    for row in rows:
        split_path = ROOT / row["split_relative_path"]
        if not split_path.exists():
            missing_files.append(row["split_relative_path"])
            if len(missing_files) >= 5:
                break
    if missing_files:
        fail(f"manifest points to missing local copied image files: {missing_files}")

    if len(labels) < 2:
        fail("at least two labels are required for a useful baseline subset")

    for required_split in ["train", "validation", "test"]:
        if splits.get(required_split, 0) == 0:
            fail(f"split has zero rows: {required_split}")

    print("Stanford Dogs baseline subset validation PASS")
    print(f"Manifest rows: {len(rows)}")
    print(f"Labels: {len(labels)}")
    for label, count in sorted(labels.items()):
        print(f"- {label}: {count}")
    print("Rows by split:")
    for split in ["train", "validation", "test"]:
        print(f"- {split}: {splits.get(split, 0)}")
    print("Boundary: this validates local subset structure only; it does not train an image model.")


if __name__ == "__main__":
    main()
