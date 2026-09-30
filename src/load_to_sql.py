"""
Load the cleaned MTB rides dataset into a local SQLite database.
"""
import pandas as pd
import sqlite3
from pathlib import Path

CSV_PATH = Path("data/processed/mtb_rides_clean.csv")
DB_PATH = Path("data/processed/mtb_analytics.db")


def load_to_sqlite():
    df = pd.read_csv(CSV_PATH, parse_dates=["start_time", "date"])

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("rides", conn, if_exists="replace", index=False)

    # Quick sanity check
    count = conn.execute("SELECT COUNT(*) FROM rides").fetchone()[0]
    print(f"Loaded {count} rides into {DB_PATH}, table 'rides'")

    conn.close()


if __name__ == "__main__":
    load_to_sqlite()