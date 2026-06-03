from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = ROOT / "data" / "images" / "local_dataset"
RAW_ROOT = LOCAL_ROOT / "raw" / "stanford_dogs"
DOWNLOAD_ROOT = LOCAL_ROOT / "downloads" / "stanford_dogs"
CANDIDATES_FILE = ROOT / "data" / "stanford_dogs_baseline_class_candidates.csv"
REPORT_MD = ROOT / "reports" / "stanford_dogs_baseline_class_selection.md"
REPORT_CSV = ROOT / "reports" / "stanford_dogs_baseline_class_selection.csv"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def normalize_label(value: str) -> str:
    value = value.strip()
    # Stanford folder names often look like: n02108089-boxer
    if "-" in value and re.match(r"^n\d+", value):
        value = value.split("-", 1)[1]
    value = value.lower().replace("_", " ").replace("-", " ")
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def count_images(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS)


def candidate_dirs() -> list[Path]:
    roots = [RAW_ROOT, DOWNLOAD_ROOT]
    dirs: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for child in root.rglob("*"):
            if child.is_dir():
                # A class folder usually contains images directly or nearby.
                if count_images(child) > 0:
                    dirs.append(child)
    # Prefer shorter paths first and remove duplicates.
    unique = []
    seen = set()
    for path in sorted(dirs, key=lambda p: (len(p.parts), str(p))):
        key = str(path.resolve())
        if key not in seen:
            unique.append(path)
            seen.add(key)
    return unique


def read_candidates() -> list[dict[str, str]]:
    if not CANDIDATES_FILE.exists():
        raise FileNotFoundError(f"Missing candidate file: {CANDIDATES_FILE}")
    with CANDIDATES_FILE.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def aliases_for(row: dict[str, str]) -> set[str]:
    raw = row.get("expected_stanford_label_aliases", "")
    aliases = {normalize_label(part) for part in raw.split("|") if part.strip()}
    aliases.add(normalize_label(row.get("preferred_display_name", "")))
    return {item for item in aliases if item}


def main() -> None:
    candidates = read_candidates()
    local_dirs = candidate_dirs()
    normalized_dirs = [(path, normalize_label(path.name), count_images(path)) for path in local_dirs]

    rows: list[dict[str, str]] = []
    for candidate in candidates:
        aliases = aliases_for(candidate)
        matches = [(path, norm, image_count) for path, norm, image_count in normalized_dirs if norm in aliases]
        available = bool(matches)
        image_count = sum(item[2] for item in matches)
        local_paths = "; ".join(str(item[0].relative_to(ROOT)) for item in matches[:5])

        include = "no"
        if available and candidate.get("include_if_available", "").startswith("yes"):
            include = "yes"
        elif available and candidate.get("include_if_available", "") == "optional":
            include = "optional"
        elif not available:
            include = "pending_or_no"

        rows.append({
            "candidate_id": candidate.get("candidate_id", ""),
            "preferred_display_name": candidate.get("preferred_display_name", ""),
            "available_locally": str(available),
            "image_count": str(image_count),
            "local_class_paths": local_paths,
            "include_in_first_baseline": include,
            "baseline_role": candidate.get("baseline_role", ""),
            "decision_notes": "confirmed from local folders" if available else "not confirmed locally yet; do not train this class before data is available",
        })

    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_CSV.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    confirmed = [row for row in rows if row["available_locally"] == "True"]
    included = [row for row in rows if row["include_in_first_baseline"] == "yes"]

    lines = [
        "# Stanford Dogs Baseline Class Selection",
        "",
        f"Raw root: `{RAW_ROOT}`",
        f"Downloads root: `{DOWNLOAD_ROOT}`",
        f"Local image-containing folders detected: {len(local_dirs)}",
        f"Candidate rows evaluated: {len(rows)}",
        f"Confirmed candidate classes: {len(confirmed)}",
        f"Selected first-baseline classes: {len(included)}",
        "",
        "## Candidate decisions",
        "",
        "| Candidate | Available locally | Image count | Include | Notes |",
        "|---|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['preferred_display_name']} | {row['available_locally']} | {row['image_count']} | {row['include_in_first_baseline']} | {row['decision_notes']} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "Before Stanford Dogs is downloaded/extracted locally, zero confirmed classes is acceptable.",
        "The purpose of Step 16 is to make class selection evidence-based, not to train a model.",
        "",
        "A future baseline image classifier should use only classes confirmed as available locally.",
        "If Cane Corso, Dogo Argentino or Presa Canario are not confirmed, the project must not claim that the model can recognize them.",
        "",
        "## Responsible boundary",
        "",
        "This report supports visual-similarity research only. It is not breed proof, pedigree proof, registry proof, certificate proof or veterinary diagnosis.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Stanford Dogs baseline class selection completed")
    print(f"Candidate rows evaluated: {len(rows)}")
    print(f"Local image-containing folders detected: {len(local_dirs)}")
    print(f"Confirmed candidate classes: {len(confirmed)}")
    print(f"Selected first-baseline classes: {len(included)}")
    print(f"CSV report: {REPORT_CSV}")
    print(f"Markdown report: {REPORT_MD}")
    print("Note: zero confirmed classes is acceptable before Stanford Dogs is downloaded locally.")


if __name__ == "__main__":
    main()
