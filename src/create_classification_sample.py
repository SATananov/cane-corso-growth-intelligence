from pathlib import Path
import zipfile
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_ZIP_PATH = PROJECT_ROOT / "data" / "raw" / "Final_Data_PLOS.zip"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "dog_growth_classification_sample.csv"

TARGET_ROWS_PER_CLASS = 5000
CHUNK_SIZE = 100000

VALID_BCS = {"Normal", "Thin", "Heavy"}

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


def create_growth_status(row):
    if row["bcs_source"] == "Normal":
        return "normal_growth"

    if row["bcs_source"] in {"Thin", "Heavy"}:
        return "needs_attention"

    return None


def main():
    if not RAW_ZIP_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset ZIP not found: {RAW_ZIP_PATH}\n"
            "Download it manually and place it in data/raw/ first."
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    normal_parts = []
    attention_parts = []

    with zipfile.ZipFile(RAW_ZIP_PATH, "r") as zip_file:
        csv_files = [name for name in zip_file.namelist() if name.endswith(".csv")]

        if not csv_files:
            raise FileNotFoundError("No CSV file found inside the ZIP archive.")

        csv_name = csv_files[0]
        print(f"Reading CSV from ZIP: {csv_name}")

        with zip_file.open(csv_name) as csv_file:
            for chunk_index, chunk in enumerate(
                pd.read_csv(csv_file, usecols=REQUIRED_COLUMNS, chunksize=CHUNK_SIZE),
                start=1
            ):
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

                chunk["bcs_source"] = chunk["BCS_RECORDED"]

                missing_recorded = (
                    chunk["bcs_source"].isna()
                    | (chunk["bcs_source"] == "None")
                    | (~chunk["bcs_source"].isin(VALID_BCS))
                )

                chunk.loc[missing_recorded, "bcs_source"] = chunk.loc[
                    missing_recorded,
                    "BCS_PREDICTED"
                ]

                chunk = chunk[chunk["bcs_source"].isin(VALID_BCS)].copy()

                if chunk.empty:
                    continue

                chunk["growth_status"] = chunk.apply(create_growth_status, axis=1)
                chunk["growth_status_binary"] = chunk["growth_status"].map({
                    "normal_growth": 0,
                    "needs_attention": 1,
                })

                normal_chunk = chunk[chunk["growth_status"] == "normal_growth"]
                attention_chunk = chunk[chunk["growth_status"] == "needs_attention"]

                normal_current = sum(len(part) for part in normal_parts)
                attention_current = sum(len(part) for part in attention_parts)

                if normal_current < TARGET_ROWS_PER_CLASS and not normal_chunk.empty:
                    normal_needed = TARGET_ROWS_PER_CLASS - normal_current
                    normal_parts.append(normal_chunk.head(normal_needed))

                if attention_current < TARGET_ROWS_PER_CLASS and not attention_chunk.empty:
                    attention_needed = TARGET_ROWS_PER_CLASS - attention_current
                    attention_parts.append(attention_chunk.head(attention_needed))

                normal_current = sum(len(part) for part in normal_parts)
                attention_current = sum(len(part) for part in attention_parts)

                print(
                    f"Chunk {chunk_index}: "
                    f"normal={normal_current}, needs_attention={attention_current}"
                )

                if (
                    normal_current >= TARGET_ROWS_PER_CLASS
                    and attention_current >= TARGET_ROWS_PER_CLASS
                ):
                    break

    if not normal_parts or not attention_parts:
        raise ValueError("Could not collect both classification classes from the dataset.")

    sample = pd.concat(normal_parts + attention_parts, ignore_index=True)

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
    sample["source_type"] = "real_public_classification_sample"

    ordered_columns = [
        "breed_id",
        "pet_id",
        "gender",
        "visit_age_years",
        "visit_age_months",
        "weight_kg",
        "bcs_recorded",
        "bcs_predicted",
        "bcs_source",
        "growth_status",
        "growth_status_binary",
        "preventive_care_visit",
        "healthy_pet_diagnosis",
        "average_adult_breed_weight_kg",
        "source_type",
    ]

    sample = sample[ordered_columns]

    sample.to_csv(OUTPUT_PATH, index=False)

    print("Classification sample created:")
    print(OUTPUT_PATH)
    print("Rows:", len(sample))
    print("Columns:", len(sample.columns))
    print(sample["growth_status"].value_counts())


if __name__ == "__main__":
    main()
