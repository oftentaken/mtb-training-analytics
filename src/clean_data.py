"""
Clean and prepare the MTB activity dataset for analysis.
Filters to mountain biking only, converts units, adds derived columns.
"""
import pandas as pd
from pathlib import Path

RAW_SUMMARY = Path("data/processed/all_activities_summary.csv")
OUT_PATH = Path("data/processed/mtb_rides_clean.csv")


def load_and_clean() -> pd.DataFrame:
    df = pd.read_csv(RAW_SUMMARY)

    # Keep only real MTB rides
    df = df[(df["sport"] == "cycling") & (df["sub_sport"] == "mountain")].copy()

    # Parse timestamp
    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    df = df.dropna(subset=["start_time"])

    # Unit conversions
    df["distance_km"] = df["total_distance_m"] / 1000
    df["duration_min"] = df["total_timer_time_s"] / 60
    df["avg_speed_kmh"] = df["avg_speed_ms"] * 3.6
    df["max_speed_kmh"] = df["max_speed_ms"] * 3.6

    # Derived time features
    df["year"] = df["start_time"].dt.year
    df["month"] = df["start_time"].dt.month
    df["date"] = df["start_time"].dt.date
    df["day_of_week"] = df["start_time"].dt.day_name()

    # Drop obviously broken rows (e.g. 0 distance, negative values)
    df = df[df["distance_km"] > 0.1]

    # Sort chronologically
    df = df.sort_values("start_time").reset_index(drop=True)

    keep_cols = [
        "start_time", "date", "year", "month", "day_of_week",
        "distance_km", "duration_min", "avg_speed_kmh", "max_speed_kmh",
        "total_ascent_m", "total_descent_m",
        "avg_heart_rate", "max_heart_rate", "total_calories",
    ]
    return df[keep_cols]


if __name__ == "__main__":
    clean_df = load_and_clean()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(OUT_PATH, index=False)

    print(f"Saved {len(clean_df)} MTB rides to {OUT_PATH}")
    print(f"\nDate range: {clean_df['start_time'].min()} to {clean_df['start_time'].max()}")
    print(f"\nYearly ride count:\n{clean_df['year'].value_counts().sort_index()}")
    print(f"\nTotal distance: {clean_df['distance_km'].sum():.0f} km")