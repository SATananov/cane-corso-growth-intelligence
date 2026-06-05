from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ROOT / "docs" / "stanford_dogs_local_download_real_class_inspection.md",
    ROOT / "data" / "stanford_dogs_download_artifacts.csv",
    ROOT / "data" / "stanford_dogs_real_inspection_rules.csv",
    ROOT / "src" / "download_stanford_dogs_local_dataset.py",
    ROOT / "src" / "inspect_stanford_dogs_real_classes.py",
    ROOT / "reports" / "stanford_dogs_download_readiness.md",
    ROOT / "reports" / "stanford_dogs_real_class_inspection.md",
]
ARTIFACTS_FILE = ROOT / "data" / "stanford_dogs_download_artifacts.csv"
RULES_FILE = ROOT / "data" / "stanford_dogs_real_inspection_rules.csv"
DOC_FILE = ROOT / "docs" / "stanford_dogs_local_download_real_class_inspection.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        raise SystemExit("Missing Step 17 files: " + ", ".join(missing))

    artifacts = read_csv(ARTIFACTS_FILE)
    rules = read_csv(RULES_FILE)
    if len(artifacts) < 4:
        raise SystemExit("Expected at least four Stanford Dogs download artifacts")
    if not any(row.get("artifact_id") == "stanford_dogs_images" for row in artifacts):
        raise SystemExit("Missing images.tar artifact row")
    if not any(row.get("default_download") == "no_large_file" for row in artifacts):
        raise SystemExit("Expected explicit no_large_file boundary for large artifacts")
    if len(rules) < 3:
        raise SystemExit("Expected inspection rules")

    doc = DOC_FILE.read_text(encoding="utf-8").lower()
    required_terms = ["visual similarity", "not breed proof", "not downloaded by default", "local only"]
    for term in required_terms:
        if term not in doc:
            raise SystemExit(f"Step 17 document missing required boundary term: {term}")

    print("Step 17 Stanford Dogs real inspection validation PASS")
    print(f"Download artifacts: {len(artifacts)}")
    print(f"Inspection rules: {len(rules)}")
    print("Boundary: large image archives are not downloaded by default; inspection is visual-similarity only.")


if __name__ == "__main__":
    main()
