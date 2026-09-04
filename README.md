# MTB Training Analytics

Analysis of personal MTB training data from Garmin Connect (heart rate, 
elevation, training load) using Python, SQL, and Power BI.

## Project status
🚧 In progress — data requested, analysis underway.

## Goal
Answer the question: is my MTB fitness improving season over season, and 
on which trails/conditions do I perform strongest?

## Stack
- **Python** (pandas, fitparse) — data cleaning and processing
- **SQL** (SQLite) — storage and querying
- **Power BI** — visualization and dashboard

## Data source
Personal activity data exported from Garmin Connect (FIT files + activity 
summaries). Raw location data is anonymized before publishing — GPS traces 
near home are trimmed to protect privacy.

## Structure
```
├── data/
│   ├── raw/          # raw exports (gitignored, not published)
│   └── processed/    # cleaned, anonymized data
├── notebooks/        # Jupyter notebooks with analysis
├── sql/              # SQL queries
├── powerbi/          # dashboard file and screenshots
└── src/              # Python scripts (cleaning, helper functions)
```
