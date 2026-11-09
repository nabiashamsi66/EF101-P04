"""
analyze_logs.py - re-check the project numbers from the raw logs.

What it does (in simple words):
  1. Reads the PowerShell logs in Raw_Logs/ (one CSV per test).
  2. Checks quality: row count, blank cells, time order, sampling gaps.
  3. Calculates the summary of each test (CPU, free RAM, paging, disk).
  4. Saves the table to Cleaned_Data/summary_recomputed.csv and prints it.

Run from anywhere:   python Scripts/analysis/analyze_logs.py
Needs:               pip install pandas
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]          # repository root
RAW = ROOT / "Raw_Logs"
OUT = ROOT / "Cleaned_Data" / "summary_recomputed.csv"

# test name -> (raw file, which rows count as "the load")
TESTS = {
    "idle":     ("idle_20261015_135254.csv",     lambda d: d),
    "cpu":      ("cpu_20261018_113237.csv",      lambda d: d[(d.elapsed_s >= 60) & (d.elapsed_s <= 640)]),
    "cooldown": ("cooldown_20261018_114614.csv", lambda d: d),
    "ram":      ("ram_20261015_142951.csv",      lambda d: d[d.elapsed_s <= 270]),
    "storage":  ("storage_20261015_145445.csv",  lambda d: d[(d.elapsed_s >= 60) & (d.elapsed_s <= 300)]),
    "mixed":    ("mixed_20261015_144438.csv",    lambda d: d),
}

def quality(df):
    t = pd.to_datetime(df["timestamp"])
    gaps = t.diff().dt.total_seconds().dropna()
    return {"rows": len(df), "blank_cells": int(df.isna().sum().sum()),
            "gap_min_s": gaps.min(), "gap_max_s": gaps.max(), "time_increasing": bool(t.is_monotonic_increasing)}

rows, qc = [], []
for test, (fname, window) in TESTS.items():
    df = pd.read_csv(RAW / fname)
    qc.append({"test": test, "file": fname, **quality(df)})
    w = window(df)
    rows.append({
        "test": test, "load_rows": len(w),
        "cpu_avg_pct": round(w.cpu_percent.mean(), 2),
        "ram_free_min_mb": int(w.ram_available_mb.min()),
        "committed_max_pct": w.ram_committed_percent.max(),
        "pages_per_sec_max": w.pages_per_sec.max(),
        "disk_write_avg_mb_s": round(w.disk_write_mb_s.mean(), 2),
        "disk_active_avg_pct": round(w.disk_active_percent.mean(), 2),
        "disk_queue_max": w.disk_queue_length.max(),
    })

summary = pd.DataFrame(rows)
summary.to_csv(OUT, index=False)
pd.set_option("display.width", 200)
print("\nQUALITY CHECK"); print(pd.DataFrame(qc).to_string(index=False))
print("\nSUMMARY (saved to", OUT.relative_to(ROOT), ")"); print(summary.to_string(index=False))
