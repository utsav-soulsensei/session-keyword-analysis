# Session Demand Analytics

Analysis of what drives **demand → add-to-cart → conversion** across wellness/course
sessions, plus an interactive dashboard.

## What it does

Joins two source sheets on the session instance id:

- **Funnel** (`leader_name`, `course_name`, `course_instance`, page views, PV→RC, PV→RS)
- **Course info** (`id`, `shortName`, `startDate`, `type`, `price`)

…then engineers features (day of week, IST time-of-day, price tier, name length &
theme keywords, leader) and measures how each factor moves demand (page views),
add-to-cart rate, and conversion rate — using **volume-weighted rates** so small
sessions don't distort the picture.

> Timestamps in the source are **UTC**; the pipeline converts them to **IST (+5:30)**
> before any day/time analysis.

## The dashboard

`Session Demand Dashboard.html` — a self-contained, single-file dashboard (no build
step, works from `file://`). Features:

- Three views (tabs): **All sessions**, **Excluding 4 outlier leaders**, and
  **Online only, excl. 4 leaders**.
- Funnel, price, session type, day of week, time of day, name length/keywords,
  leaders, and monthly trend — each with dynamically recomputed insights.
- Keyword table drills down to each theme's **top 5 sessions**.
- Keyword & leader tables are **sortable and searchable**.
- Light/dark aware, colorblind-validated palette.

## Pipeline

```
build_dataset.py   # join sheets, clean, engineer features  -> merged_analysis.csv
analyze.py         # driver analysis printed to console
export_json.py     # aggregate the 3 views                  -> dashboard_data.json
make_dashboard.py  # inline data + render                   -> Session Demand Dashboard.html
```

Run in order:

```bash
python3 build_dataset.py && python3 export_json.py && python3 make_dashboard.py
```

## Note on data

The raw CSVs and derived data files are intentionally **not committed** (see
`.gitignore`). To reproduce, place the two source CSVs in this folder and run the
pipeline. The published dashboard HTML contains aggregated figures inline.
