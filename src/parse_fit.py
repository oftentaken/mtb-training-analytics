"""
Parse Garmin FIT files and build a summary table of all activities.
"""
import fitparse
import pandas as pd
from pathlib import Path
from datetime import datetime


def parse_single_fit(filepath: Path) -> dict | None:
    """Extract session-level summary from one FIT file. Returns None if unreadable."""
    try:
        fitfile = fitparse.FitFile(str(filepath))
        session_data = {}

        for record in fitfile.get_messages("session"):
            for field in record:
                session_data[field.name] = field.value

        if not session_data:
            return None

        return {
            "filename": filepath.name,
            "sport": session_data.get("sport"),
            "sub_sport": session_data.get("sub_sport"),
            "start_time": session_data.get("start_time"),
            "total_distance_m": session_data.get("total_distance"),
            "total_timer_time_s": session_data.get("total_timer_time"),
            "total_ascent_m": session_data.get("total_ascent"),
            "total_descent_m": session_data.get("total_descent"),
            "avg_heart_rate": session_data.get("avg_heart_rate"),
            "max_heart_rate": session_data.get("max_heart_rate"),
            "avg_speed_ms": session_data.get("avg_speed"),
            "max_speed_ms": session_data.get("max_speed"),
            "total_calories": session_data.get("total_calories"),
        }
    except Exception as e:
        print(f"Skipped {filepath.name}: {e}")
        return None


def build_activities_table(fit_folder: Path) -> pd.DataFrame:
    """Loop through all FIT files in a folder and build a summary DataFrame."""
    fit_files = list(fit_folder.glob("*.FIT")) + list(fit_folder.glob("*.fit"))
    print(f"Found {len(fit_files)} FIT files. Parsing...")

    records = []
    for i, fp in enumerate(fit_files, 1):
        result = parse_single_fit(fp)
        if result:
            records.append(result)
        if i % 200 == 0:
            print(f"  processed {i}/{len(fit_files)}")

    df = pd.DataFrame(records)
    print(f"Done. {len(df)} activities parsed successfully.")
    return df


if __name__ == "__main__":
    RAW_DIR = Path("data/raw/fit_files")
    OUT_PATH = Path("data/processed/all_activities_summary.csv")

    df = build_activities_table(RAW_DIR)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved to {OUT_PATH}")

    print("\nSport types found:")
    print(df["sport"].value_counts())