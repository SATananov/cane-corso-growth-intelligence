from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_FILE = ROOT / "data" / "stanford_dogs_baseline_class_candidates.csv"
TEMPLATE_FILE = ROOT / "data" / "stanford_dogs_baseline_class_selection_template.csv"
POLICY_FILE = ROOT / "docs" / "baseline_visual_class_selection_policy.md"
GUIDE_FILE = ROOT / "docs" / "local_stanford_dogs_inspection_baseline_class_selection.md"
REPORT_FILE = ROOT / "reports" / "stanford_dogs_baseline_class_selection.md"

REQUIRED_CANDIDATE_COLUMNS = {
    "candidate_id",
    "preferred_display_name",
    "expected_stanford_label_aliases",
    "expected_status_before_download",
    "baseline_role",
    "include_if_available",
    "relationship_to_cane_corso_target",
}

REQUIRED_PHRASES = [
    "Do not assume a breed class exists",
    "visual similarity",
    "not breed proof",
    "future consent-based USG image dataset",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def main() -> None:
    candidates = read_csv(CANDIDATES_FILE)
    template = read_csv(TEMPLATE_FILE)

    if len(candidates) < 5:
        raise AssertionError("Expected at least five Stanford baseline candidate rows.")

    missing_cols = sorted(REQUIRED_CANDIDATE_COLUMNS - set(candidates[0].keys()))
    if missing_cols:
        raise AssertionError(f"Candidate CSV missing columns: {missing_cols}")

    names = {row["preferred_display_name"].lower() for row in candidates}
    for required in ["boxer", "bullmastiff", "great dane", "cane corso"]:
        if required not in names:
            raise AssertionError(f"Missing required candidate or target boundary row: {required}")

    if not template:
        raise AssertionError("Selection template must not be empty.")

    guide_text = GUIDE_FILE.read_text(encoding="utf-8")
    policy_text = POLICY_FILE.read_text(encoding="utf-8")
    combined = guide_text + "\n" + policy_text
    missing = [phrase for phrase in REQUIRED_PHRASES if phrase.lower() not in combined.lower()]
    if missing:
        raise AssertionError(f"Missing required responsible boundary phrases: {missing}")

    if not REPORT_FILE.exists():
        raise AssertionError("Expected generated baseline class selection report. Run src/select_stanford_dogs_baseline_classes.py first.")

    print("Stanford baseline class selection validation PASS")
    print(f"Candidate rows: {len(candidates)}")
    print(f"Template rows: {len(template)}")
    print("Boundary: visual similarity only; class availability must be verified locally.")


if __name__ == "__main__":
    main()
