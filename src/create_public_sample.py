from pathlib import Path
import zipfile
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_ZIP_PATH = PROJECT_ROOT / "data" / "raw" / "Final_Data_PLOS.zip"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "dog_growth_public_sample.csv"

TARGET_ROWS = 10000
CHUNK_SIZE = 100000

REQUIRED_COLUMNS = [
    "BREED_ID",
    "PET_ID",
    "GENDER",
    "VISIT_AGE",
    "WEIGHT",
    "BCS_RECORDED",
    "BCS_PREDICTED",
    "PREVENTIVE_CARE_VISIT",
    "HEALTHY_PET_DIAGNOSIS",
    "AV_BREED_WEIGHT",
]


def main():
    if not RAW_ZIP_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset ZIP not found: {RAW_ZIP_PATH}\n"
            "Download it manually and place it in data/raw/ first."
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    sampled_chunks = []

    with zipfile.ZipFile(RAW_ZIP_PATH, "r") as zip_file:
        csv_files = [name for name in zip_file.namelist() if name.endswith(".csv")]

        if not csv_files:
            raise FileNotFoundError("No CSV file found inside the ZIP archive.")

        csv_name = csv_files[0]
        print(f"Reading CSV from ZIP: {csv_name}")

        with zip_file.open(csv_name) as csv_file:
            for chunk in pd.read_csv(csv_file, usecols=REQUIRED_COLUMNS, chunksize=CHUNK_SIZE):
                chunk = chunk.copy()

                chunk["VISIT_AGE"] = pd.to_numeric(chunk["VISIT_AGE"], errors="coerce")
                chunk["WEIGHT"] = pd.to_numeric(chunk["WEIGHT"], errors="coerce")
                chunk["AV_BREED_WEIGHT"] = pd.to_numeric(chunk["AV_BREED_WEIGHT"], errors="coerce")

                chunk = chunk.dropna(subset=["VISIT_AGE", "WEIGHT"])

                chunk = chunk[
                    (chunk["VISIT_AGE"] >= 0)
                    & (chunk["VISIT_AGE"] <= 3)
                    & (chunk["WEIGHT"] > 0)
                    & (chunk["WEIGHT"] <= 150)
                ]

                if chunk.empty:
                    continue

                sampled_chunks.append(chunk)

                current_rows = sum(len(part) for part in sampled_chunks)
                print(f"Collected rows: {current_rows}")

                if current_rows >= TARGET_ROWS:
                    break

    if not sampled_chunks:
        raise ValueError("No usable rows were collected from the dataset.")

    sample = pd.concat(sampled_chunks, ignore_index=True).head(TARGET_ROWS)

    sample = sample.rename(
        columns={
            "BREED_ID": "breed_id",
            "PET_ID": "pet_id",
            "GENDER": "gender",
            "VISIT_AGE": "visit_age_years",
            "WEIGHT": "weight_kg",
            "BCS_RECORDED": "bcs_recorded",
            "BCS_PREDICTED": "bcs_predicted",
            "PREVENTIVE_CARE_VISIT": "preventive_care_visit",
            "HEALTHY_PET_DIAGNOSIS": "healthy_pet_diagnosis",
            "AV_BREED_WEIGHT": "average_adult_breed_weight_kg",
        }
    )

    sample["visit_age_months"] = (sample["visit_age_years"] * 12).round(2)
    sample["source_type"] = "real_public_processed_sample"

    ordered_columns = [
        "breed_id",
        "pet_id",
        "gender",
        "visit_age_years",
        "visit_age_months",
        "weight_kg",
        "bcs_recorded",
        "bcs_predicted",
        "preventive_care_visit",
        "healthy_pet_diagnosis",
        "average_adult_breed_weight_kg",
        "source_type",
    ]

    sample = sample[ordered_columns]

    sample.to_csv(OUTPUT_PATH, index=False)

    print("Processed sample created:")
    print(OUTPUT_PATH)
    print("Rows:", len(sample))
    print("Columns:", len(sample.columns))


if __name__ == "__main__":
    main()
