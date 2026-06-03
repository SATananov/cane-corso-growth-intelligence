from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_CSV = PROJECT_ROOT / "data" / "public_image_dataset_class_candidates.csv"
RULES_CSV = PROJECT_ROOT / "data" / "public_image_dataset_target_audit_rules.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "public_image_dataset_class_availability_audit.md"

REQUIRED_CANDIDATE_COLUMNS = {
    "dataset_name",
    "source_type",
    "public_class_name",
    "normalized_class_name",
    "target_class",
    "match_level",
    "baseline_role",
    "confirmation_status",
    "usable_for_step15_baseline",
    "limitation_notes",
}

REQUIRED_RULE_COLUMNS = {"target_class", "priority", "baseline_policy", "reason"}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_columns(rows: list[dict[str, str]], required: set[str], path: Path) -> None:
    if not rows:
        raise ValueError(f"CSV has no data rows: {path}")
    available = set(rows[0].keys())
    missing = sorted(required - available)
    if missing:
        raise ValueError(f"CSV {path} is missing required columns: {missing}")


def normalize_label(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def inspect_local_class_dir(class_dir: Path | None) -> list[str]:
    if class_dir is None:
        return []
    if not class_dir.exists():
        raise FileNotFoundError(f"Class directory does not exist: {class_dir}")
    return sorted(normalize_label(p.name) for p in class_dir.iterdir() if p.is_dir())


def build_report(candidates: list[dict[str, str]], rules: list[dict[str, str]], local_classes: list[str]) -> str:
    dataset_counts = Counter(row["dataset_name"] for row in candidates)
    target_counts = Counter(row["target_class"] for row in candidates)
    usable_counts = Counter(row["usable_for_step15_baseline"] for row in candidates)

    lines: list[str] = []
    lines.append("# Public Image Dataset Class Availability Audit")
    lines.append("")
    lines.append("This report validates the class-availability planning data for the future visual similarity module.")
    lines.append("")
    lines.append("## Candidate rows by dataset")
    lines.append("")
    for dataset_name, count in sorted(dataset_counts.items()):
        lines.append(f"- {dataset_name}: {count}")
    lines.append("")
    lines.append("## Candidate rows by target class")
    lines.append("")
    for target_class, count in sorted(target_counts.items()):
        lines.append(f"- {target_class}: {count}")
    lines.append("")
    lines.append("## Step 15 usability flags")
    lines.append("")
    for flag, count in sorted(usable_counts.items()):
        lines.append(f"- {flag}: {count}")
    lines.append("")
    lines.append("## Target audit rules")
    lines.append("")
    for row in rules:
        lines.append(f"- {row['target_class']}: {row['baseline_policy']} — {row['reason']}")
    lines.append("")

    if local_classes:
        candidate_labels = {normalize_label(row["normalized_class_name"]) for row in candidates}
        matched = sorted(set(local_classes) & candidate_labels)
        unmatched = sorted(set(local_classes) - candidate_labels)
        lines.append("## Optional local class directory inspection")
        lines.append("")
        lines.append(f"Local class folders inspected: {len(local_classes)}")
        lines.append(f"Matched candidate labels: {len(matched)}")
        for label in matched:
            lines.append(f"- matched: {label}")
        if unmatched:
            lines.append("")
            lines.append("Unmatched local labels that may need manual review:")
            for label in unmatched[:50]:
                lines.append(f"- review: {label}")
        lines.append("")
    else:
        lines.append("## Optional local class directory inspection")
        lines.append("")
        lines.append("No local class directory was provided. This is expected before downloading a public image dataset.")
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("This audit supports planning only. It does not download images, train a model, prove dataset quality, or prove breed identity from a photo.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate public image dataset class availability planning files.")
    parser.add_argument(
        "--class-dir",
        type=Path,
        default=None,
        help="Optional local directory containing one subfolder per image class after a public dataset is downloaded.",
    )
    args = parser.parse_args()

    candidates = read_csv(CANDIDATES_CSV)
    rules = read_csv(RULES_CSV)
    validate_columns(candidates, REQUIRED_CANDIDATE_COLUMNS, CANDIDATES_CSV)
    validate_columns(rules, REQUIRED_RULE_COLUMNS, RULES_CSV)

    local_classes = inspect_local_class_dir(args.class_dir)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(candidates, rules, local_classes), encoding="utf-8")

    print("Public image dataset class availability audit PASS")
    print(f"Candidate rows: {len(candidates)}")
    print(f"Target rules:   {len(rules)}")
    print(f"Report:         {REPORT_PATH}")
    if local_classes:
        print(f"Local classes inspected: {len(local_classes)}")
    else:
        print("Local classes inspected: 0 (optional)")
    print("Note: This validates class-availability planning only. It does not train an image model.")


if __name__ == "__main__":
    main()
