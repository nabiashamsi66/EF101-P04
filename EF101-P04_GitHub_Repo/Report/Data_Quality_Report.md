# Data Quality Report (EF101-P04)

Raw files in Raw_Logs/ are unchanged copies of the logger output. All cleaning is in Cleaned_Data/.

| file | test | rows | expected | blank cells | last elapsed (s) | min gap (s) | max gap (s) | timestamps increasing | cpu out of 0-100 | disk active > 100 | negative values |
|---|---|---|---|---|---|---|---|---|---|---|---|
| idle_20261015_135254.csv | idle | 150 | 150 | 0 | 304 | 2 | 3 | yes | 0 | 0 | 0 |
| cpu_20261018_113237.csv | cpu load | 330 | 330 | 0 | 717 | 2 | 4 | yes | 0 | 10 | 0 |
| cooldown_20261018_114614.csv | cooldown | 150 | 150 | 0 | 304 | 2 | 3 | yes | 0 | 0 | 0 |
| ram_20261015_142951.csv | RAM | 150 | 150 | 0 | 304 | 2 | 3 | yes | 0 | 0 | 0 |
| storage_20261015_145445.csv | storage | 150 | 150 | 0 | 305 | 2 | 3 | yes | 0 | 5 | 0 |
| mixed_20261015_144438.csv | mixed | 150 | 150 | 0 | 303 | 2 | 3 | yes | 0 | 1 | 0 |
| hwinfo_session1_15oct.csv | HWiNFO session 1 | 2146 data rows | - | 0 | - | - | - | yes | 0 | - | - |
| hwinfo_session2_18oct_cpu_rerun.csv | HWiNFO session 2 | 646 data rows | - | 0 | - | - | - | yes | 0 | - | - |

## Notes
- The CPU log has 330 rows and no empty cells. Sampling interval was 2 to 4 seconds, which is within the 1 to 5 second requirement.
- The CPU load started about one minute after logging started. The first minute is therefore a pre-load baseline.
- `disk_active_percent` is above 100 in some rows. This is a known behaviour of the Windows counter. Values were kept as recorded.
- Storage read values are low on average because Windows served much of the file from its memory cache.
- Both HWiNFO files contained repeated header and blank lines. These were removed in the cleaned files.
- The raw HWiNFO file for session 2 was renamed from `hwinfo_cpu_rerun_csv.CSV` to `hwinfo_session2_18oct_cpu_rerun.csv`. Its content is unchanged.

## GPU test (21 October 2026)
- gpu_20261021_210253.csv: 150 rows, no empty cells, sampling 2 to 3 seconds, time order correct.
- hwinfo_session3_21oct_gpu_test.csv: all GPU rows present, 146 samples inside the test window.
- Note: the GPU test is a light video workload. It is not a 3D stress test.
