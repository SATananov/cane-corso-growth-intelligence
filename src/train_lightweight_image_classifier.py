"""Train a lightweight visual-similarity baseline classifier.

Step 21 intentionally avoids deep learning. It uses simple image features and a
scikit-learn classifier to prove the end-to-end image-classification workflow.

The model output is visual similarity among trained classes only. It is not breed
proof, pedigree proof, registry proof, genetic proof, or veterinary advice.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Iterable

import numpy as np

try:
    import matplotlib.image as mpimg
except Exception as exc:  # pragma: no cover - user-facing dependency guard
    raise SystemExit(
        "matplotlib is required for image loading. Activate .venv and run: "
        "python -m pip install -r requirements.txt"
    ) from exc

try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
except Exception as exc:  # pragma: no cover - user-facing dependency guard
    raise SystemExit(
        "scikit-learn is required for this baseline. Activate .venv and run: "
        "python -m pip install -r requirements.txt"
    ) from exc

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUBSET_ROOT = PROJECT_ROOT / "data" / "images" / "local_dataset" / "splits" / "stanford_dogs_first_baseline"
REPORTS_DIR = PROJECT_ROOT / "reports"

METRICS_CSV = REPORTS_DIR / "lightweight_image_classifier_metrics.csv"
CONFUSION_CSV = REPORTS_DIR / "lightweight_image_classifier_confusion_matrix.csv"
EXAMPLES_CSV = REPORTS_DIR / "lightweight_image_classifier_prediction_examples.csv"
REPORT_MD = REPORTS_DIR / "lightweight_image_classifier_training_report.md"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
SPLITS = ("train", "validation", "test")


def iter_image_files(split: str) -> Iterable[tuple[Path, str]]:
    split_root = SUBSET_ROOT / split
    if not split_root.exists():
        return
    for class_dir in sorted(p for p in split_root.iterdir() if p.is_dir()):
        label = class_dir.name
        for image_path in sorted(class_dir.rglob("*")):
            if image_path.is_file() and image_path.suffix.lower() in IMAGE_EXTENSIONS:
                yield image_path, label


def load_image_array(path: Path) -> np.ndarray:
    image = mpimg.imread(path)
    image = np.asarray(image)

    if image.ndim == 2:
        image = np.stack([image, image, image], axis=-1)
    if image.ndim != 3:
        raise ValueError(f"Unsupported image shape for {path}: {image.shape}")
    if image.shape[2] > 3:
        image = image[:, :, :3]

    image = image.astype("float32")
    if image.max() > 1.0:
        image = image / 255.0
    return np.clip(image, 0.0, 1.0)


def extract_features(path: Path, bins: int = 16) -> np.ndarray:
    image = load_image_array(path)
    h, w = image.shape[:2]
    features: list[float] = []

    for channel in range(3):
        hist, _ = np.histogram(image[:, :, channel], bins=bins, range=(0.0, 1.0), density=True)
        features.extend(hist.astype("float32").tolist())

    channel_means = image.reshape(-1, 3).mean(axis=0)
    channel_stds = image.reshape(-1, 3).std(axis=0)
    features.extend(channel_means.astype("float32").tolist())
    features.extend(channel_stds.astype("float32").tolist())
    features.append(float(w / max(h, 1)))

    return np.asarray(features, dtype="float32")


def load_split(split: str) -> tuple[np.ndarray, np.ndarray, list[Path]]:
    rows = list(iter_image_files(split))
    if not rows:
        return np.empty((0, 55), dtype="float32"), np.asarray([], dtype=object), []

    features = []
    labels = []
    paths = []
    for image_path, label in rows:
        try:
            features.append(extract_features(image_path))
            labels.append(label)
            paths.append(image_path)
        except Exception as exc:
            print(f"Skipped unreadable image: {image_path} ({exc})")

    if not features:
        return np.empty((0, 55), dtype="float32"), np.asarray([], dtype=object), []
    return np.vstack(features), np.asarray(labels), paths


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def write_metrics(metrics: list[dict[str, object]]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with METRICS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["split", "samples", "accuracy", "macro_f1", "weighted_f1"])
        writer.writeheader()
        writer.writerows(metrics)


def write_confusion(labels: list[str], y_true: np.ndarray, y_pred: np.ndarray) -> None:
    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    with CONFUSION_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["actual\\predicted", *labels])
        for label, row in zip(labels, matrix):
            writer.writerow([label, *row.tolist()])


def write_prediction_examples(model, labels: list[str], paths: list[Path], y_true: np.ndarray, X: np.ndarray) -> None:
    with EXAMPLES_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["image_path", "actual_label", "predicted_label", *[f"prob_{label}" for label in labels]]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        if len(paths) == 0:
            return
        probabilities = model.predict_proba(X)
        predictions = model.predict(X)
        for image_path, actual, predicted, probs in list(zip(paths, y_true, predictions, probabilities))[:12]:
            row = {
                "image_path": relative_path(image_path),
                "actual_label": actual,
                "predicted_label": predicted,
            }
            for label, prob in zip(model.classes_, probs):
                row[f"prob_{label}"] = f"{prob:.4f}"
            writer.writerow(row)


def write_report(class_counts: dict[str, Counter], metrics: list[dict[str, object]], labels: list[str]) -> None:
    lines = [
        "# Step 21 — Lightweight Baseline Image Classifier Training Report",
        "",
        "This report records a local-only lightweight image-classification prototype.",
        "The output is visual similarity among trained classes only; it is not breed proof, pedigree proof, registry proof, genetic proof, or veterinary advice.",
        "",
        "## Dataset",
        "",
        f"Subset root: `{SUBSET_ROOT}`",
        "",
        "## Labels",
        "",
    ]
    for label in labels:
        lines.append(f"- {label}")

    lines.extend(["", "## Counts by split", ""])
    for split in SPLITS:
        lines.append(f"### {split}")
        for label, count in sorted(class_counts.get(split, Counter()).items()):
            lines.append(f"- {label}: {count}")
        lines.append("")

    lines.extend(["## Metrics", ""])
    for row in metrics:
        lines.append(
            f"- {row['split']}: samples={row['samples']}, accuracy={row['accuracy']:.4f}, "
            f"macro_f1={row['macro_f1']:.4f}, weighted_f1={row['weighted_f1']:.4f}"
        )

    lines.extend([
        "",
        "## Boundary",
        "",
        "The model is a course-project baseline. It uses simple histogram/statistical image features and logistic regression.",
        "No image files and no model weights should be committed to GitHub.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if not SUBSET_ROOT.exists():
        raise SystemExit(
            f"Subset root not found: {SUBSET_ROOT}\n"
            "Run: python src/prepare_stanford_dogs_baseline_subset.py"
        )

    X_train, y_train, train_paths = load_split("train")
    X_val, y_val, val_paths = load_split("validation")
    X_test, y_test, test_paths = load_split("test")

    if len(y_train) == 0:
        raise SystemExit("No training images found. Run Step 19 subset preparation first.")
    if len(set(y_train)) < 2:
        raise SystemExit("At least two training classes are required for classification.")

    labels = sorted(set(y_train.tolist()))
    class_counts = {
        "train": Counter(y_train.tolist()),
        "validation": Counter(y_val.tolist()),
        "test": Counter(y_test.tolist()),
    }

    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=500, class_weight="balanced", solver="lbfgs"),
    )
    model.fit(X_train, y_train)

    metrics: list[dict[str, object]] = []
    evaluation_sets = [
        ("train", X_train, y_train),
        ("validation", X_val, y_val),
        ("test", X_test, y_test),
    ]

    for split, X_split, y_split in evaluation_sets:
        if len(y_split) == 0:
            metrics.append({"split": split, "samples": 0, "accuracy": 0.0, "macro_f1": 0.0, "weighted_f1": 0.0})
            continue
        y_pred = model.predict(X_split)
        metrics.append(
            {
                "split": split,
                "samples": int(len(y_split)),
                "accuracy": float(accuracy_score(y_split, y_pred)),
                "macro_f1": float(f1_score(y_split, y_pred, average="macro", zero_division=0)),
                "weighted_f1": float(f1_score(y_split, y_pred, average="weighted", zero_division=0)),
            }
        )

    write_metrics(metrics)

    if len(y_test) > 0:
        test_pred = model.predict(X_test)
        write_confusion(labels, y_test, test_pred)
        write_prediction_examples(model, labels, test_paths, y_test, X_test)
    else:
        write_confusion(labels, np.asarray([], dtype=object), np.asarray([], dtype=object))
        write_prediction_examples(model, labels, [], np.asarray([], dtype=object), np.empty((0, X_train.shape[1])))

    write_report(class_counts, metrics, labels)

    print("Lightweight baseline image classifier training completed")
    print(f"Classes: {len(labels)} -> {', '.join(labels)}")
    print(f"Train samples: {len(y_train)}")
    print(f"Validation samples: {len(y_val)}")
    print(f"Test samples: {len(y_test)}")
    print(f"Report: {REPORT_MD}")
    print("Boundary: visual similarity only; no breed-proof claim; no model weights saved.")


if __name__ == "__main__":
    main()
