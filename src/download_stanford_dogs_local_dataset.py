from __future__ import annotations

import argparse
import csv
import shutil
import sys
import tarfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = ROOT / "data" / "images" / "local_dataset"
DOWNLOAD_ROOT = LOCAL_ROOT / "downloads" / "stanford_dogs"
RAW_ROOT = LOCAL_ROOT / "raw" / "stanford_dogs"
ARTIFACTS_FILE = ROOT / "data" / "stanford_dogs_download_artifacts.csv"
REPORT_FILE = ROOT / "reports" / "stanford_dogs_download_readiness.md"

LARGE_ARTIFACT_IDS = {"stanford_dogs_images", "stanford_dogs_annotations"}
SMALL_DEFAULT_MODES = {"yes_small_file"}
STANFORD_HOST_HTTPS = "https://vision.stanford.edu/"
STANFORD_HOST_HTTP = "http://vision.stanford.edu/"


def read_artifacts() -> list[dict[str, str]]:
    if not ARTIFACTS_FILE.exists():
        raise FileNotFoundError(f"Missing artifacts file: {ARTIFACTS_FILE}")
    with ARTIFACTS_FILE.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def build_url_candidates(url: str) -> list[str]:
    """Return safe download candidates without disabling TLS verification.

    The Stanford Dogs page is historically documented with http:// URLs. On some
    Windows/Python installations, https://vision.stanford.edu may fail with a
    certificate hostname mismatch before the server redirects or serves content.
    We do not bypass SSL verification. Instead, for this official Stanford host
    only, we try the documented http:// endpoint as a fallback.
    """
    candidates = [url]
    if url.startswith(STANFORD_HOST_HTTPS):
        http_url = STANFORD_HOST_HTTP + url[len(STANFORD_HOST_HTTPS) :]
        if http_url not in candidates:
            candidates.append(http_url)
    return candidates


def stream_download(url: str, target: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; CaneCorsoGrowthIntelligence/1.0; educational dataset preparation)",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        with target.open("wb") as output_file:
            shutil.copyfileobj(response, output_file)


def download_file(url: str, target: Path, force: bool = False) -> tuple[str, str, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not force:
        return "already_exists", url, "existing_file_reused"

    errors: list[str] = []
    for candidate_url in build_url_candidates(url):
        print(f"Downloading: {candidate_url}")
        print(f"Target:      {target}")
        try:
            stream_download(candidate_url, target)
            return "downloaded", candidate_url, "ok"
        except Exception as exc:  # pragma: no cover - network depends on local machine
            if target.exists():
                try:
                    target.unlink()
                except OSError:
                    pass
            errors.append(f"{candidate_url} -> {type(exc).__name__}: {exc}")
            print(f"Download attempt failed: {errors[-1]}")

    raise RuntimeError("Download failed for all candidate URLs:\n" + "\n".join(errors))


def extract_tar(archive_path: Path, destination: Path, force: bool = False) -> str:
    if not archive_path.exists():
        return "missing_archive"
    destination.mkdir(parents=True, exist_ok=True)
    marker = destination / f".{archive_path.stem}_extracted"
    if marker.exists() and not force:
        return "already_extracted"
    print(f"Extracting: {archive_path}")
    print(f"To:         {destination}")
    with tarfile.open(archive_path) as tar:
        # Python 3.12 supports filter='data'. Keep compatibility with older local versions.
        try:
            tar.extractall(destination, filter="data")
        except TypeError:  # pragma: no cover
            tar.extractall(destination)
    marker.write_text("extracted\n", encoding="utf-8")
    return "extracted"


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare or explicitly download Stanford Dogs local dataset artifacts.")
    parser.add_argument("--download-small", action="store_true", help="Download small official metadata files such as README and split lists.")
    parser.add_argument("--download-images", action="store_true", help="Download the large Stanford Dogs images.tar archive. This may take time and disk space.")
    parser.add_argument("--download-annotations", action="store_true", help="Download the annotation.tar archive.")
    parser.add_argument("--extract-images", action="store_true", help="Extract images.tar into the local raw Stanford Dogs folder.")
    parser.add_argument("--extract-annotations", action="store_true", help="Extract annotation.tar under local downloads for later bounding-box work.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing downloaded/extracted files when possible.")
    args = parser.parse_args()

    DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    artifacts = read_artifacts()

    actions: list[dict[str, str]] = []
    for artifact in artifacts:
        artifact_id = artifact["artifact_id"]
        local_path = ROOT / artifact["local_file"]
        should_download = False
        reason = "not_requested"

        if args.download_small and artifact.get("default_download") in SMALL_DEFAULT_MODES:
            should_download = True
            reason = "download_small_requested"
        if artifact_id == "stanford_dogs_images" and args.download_images:
            should_download = True
            reason = "download_images_requested"
        if artifact_id == "stanford_dogs_annotations" and args.download_annotations:
            should_download = True
            reason = "download_annotations_requested"

        status = "planned_only"
        final_url = artifact["official_url"]
        download_note = "not_attempted"
        if should_download:
            status, final_url, download_note = download_file(artifact["official_url"], local_path, force=args.force)

        actions.append({
            "artifact_id": artifact_id,
            "local_path": str(local_path.relative_to(ROOT)),
            "status": status,
            "reason": reason,
            "exists_after": str(local_path.exists()),
            "final_url": final_url,
            "download_note": download_note,
        })

    images_archive = DOWNLOAD_ROOT / "images.tar"
    annotations_archive = DOWNLOAD_ROOT / "annotation.tar"
    image_extract_status = "not_requested"
    annotation_extract_status = "not_requested"
    if args.extract_images:
        image_extract_status = extract_tar(images_archive, RAW_ROOT, force=args.force)
    if args.extract_annotations:
        annotation_extract_status = extract_tar(annotations_archive, DOWNLOAD_ROOT / "annotations_extracted", force=args.force)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Stanford Dogs Local Download Readiness",
        "",
        f"Download root: `{DOWNLOAD_ROOT}`",
        f"Raw root: `{RAW_ROOT}`",
        "",
        "## Actions",
        "",
        "| Artifact | Status | Exists after | Reason | Final URL | Local path |",
        "|---|---|---:|---|---|---|",
    ]
    for item in actions:
        lines.append(
            f"| {item['artifact_id']} | {item['status']} | {item['exists_after']} | {item['reason']} | `{item['final_url']}` | `{item['local_path']}` |"
        )
    lines.extend([
        "",
        "## Extraction",
        "",
        f"- Images extraction status: `{image_extract_status}`",
        f"- Annotations extraction status: `{annotation_extract_status}`",
        "",
        "## Download safety note",
        "",
        "This script does not disable SSL verification. If the Stanford HTTPS endpoint fails on a local Python/Windows environment because of a certificate hostname mismatch, the script uses the official historically documented `http://vision.stanford.edu/...` Stanford Dogs endpoint instead.",
        "",
        "## Responsible boundary",
        "",
        "This script prepares local public dataset artifacts only. It does not commit images, train a model, prove breed identity, prove pedigree, or create a registry/certificate decision.",
    ])
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Stanford Dogs local download readiness completed")
    print(f"Download root: {DOWNLOAD_ROOT}")
    print(f"Raw root:      {RAW_ROOT}")
    print(f"Report:        {REPORT_FILE}")
    if not any(a["status"] in {"downloaded", "already_exists"} for a in actions):
        print("Dry-run/planning mode: no downloads were performed. Use --download-small or --download-images explicitly.")
    print("Large image archive is never downloaded unless --download-images is provided.")


if __name__ == "__main__":
    main()
