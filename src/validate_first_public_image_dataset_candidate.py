from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_FILE = ROOT / "data" / "first_public_image_dataset_candidate.csv"
CHECKLIST_FILE = ROOT / "data" / "stanford_dogs_local_download_checklist.csv"
GUIDE_FILE = ROOT / "docs" / "first_public_image_dataset_candidate_download_guide.md"
REPORT_FILE = ROOT / "reports" / "first_public_image_dataset_candidate_validation.md"

REQUIRED_CANDIDATE_COLUMNS = {
    "dataset_name",
    "primary_use_in_project",
    "why_selected_first",
    "expected_download_location",
    "expected_raw_location",
    "git_policy",
    "training_status",
    "cane_corso_status",
    "responsible_use_boundary",
}

REQUIRED_GUIDE_PHRASES = [
    "visual similarity classifier",
    "not as",
    "breed proof",
    "not training an image model",
    "should not be committed",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def main() -> None:
    candidate_rows = read_csv(CANDIDATE_FILE)
    checklist_rows = read_csv(CHECKLIST_FILE)

    if len(candidate_rows) != 1:
        raise AssertionError("Expected exactly one first public image dataset candidate.")

    columns = set(candidate_rows[0].keys())
    missing = sorted(REQUIRED_CANDIDATE_COLUMNS - columns)
    if missing:
        raise AssertionError(f"Candidate CSV missing columns: {missing}")

    candidate = candidate_rows[0]
    if "stanford" not in candidate["dataset_name"].lower():
        raise AssertionError("The first candidate should be Stanford Dogs / ImageNet Dogs.")

    if candidate["training_status"] != "not_trained_in_stage_15":
        raise AssertionError("The first candidate stage must not claim that an image model has already been trained.")

    if "not_assumed" not in candidate["cane_corso_status"]:
        raise AssertionError("Cane Corso availability must be documented as not assumed before label inspection.")

    if len(checklist_rows) < 5:
        raise AssertionError("Download checklist should contain multiple local preparation steps.")

    guide_text = GUIDE_FILE.read_text(encoding="utf-8")
    missing_phrases = [phrase for phrase in REQUIRED_GUIDE_PHRASES if phrase.lower() not in guide_text.lower()]
    if missing_phrases:
        raise AssertionError(f"Guide missing required responsible-use phrases: {missing_phrases}")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        "# First Public Image Dataset Candidate Validation\n\n"
        "Validation PASS.\n\n"
        f"Candidate: {candidate['dataset_name']}\n\n"
        f"Expected download location: `{candidate['expected_download_location']}`\n\n"
        f"Expected raw location: `{candidate['expected_raw_location']}`\n\n"
        "Training status: no image model is trained at this candidate-selection stage.\n\n"
        "Responsible boundary: visual similarity only; not breed proof, pedigree proof, registry proof or veterinary diagnosis.\n",
        encoding="utf-8",
    )

    print("First public image dataset candidate validation PASS")
    print(f"Candidate: {candidate['dataset_name']}")
    print(f"Checklist rows: {len(checklist_rows)}")
    print(f"Report: {REPORT_FILE}")
    print("Note: this validates download-guide artifacts only. It does not download images or train a model.")


if __name__ == "__main__":
    main()
