# EF101-P04: Contribution Statement and Tools

## What the project is about
EF101-P04 measures how one laptop behaves under idle, CPU, memory, storage, mixed and GPU workloads and finds which part limits speed in each case.
Test machine: HP EliteBook 850 G5 (Core i5-8250U, 4 cores / 8 threads, 7.8 GB usable RAM, 256 GB Samsung SSD, Intel UHD 620, Windows 10 Pro).
A PowerShell script logs nine Windows counters every 2 seconds, HWiNFO adds clock, temperature and power, and Python re-checks the data and draws the graphs.
Three students share the work; every member can explain the whole system.

## Who did what

All three members planned and ran **every test together** on the same laptop (13 Oct practice, 15 Oct idle/RAM/storage/mixed, 18 Oct valid CPU run and cooldown, 21 Oct GPU). After the tests the work was shared as below.

| | **Nabia Shamsi** (EE-001) | **Areeza Rehan** (EE-010) | **Abdul Muqeet** (EE-038) |
|---|---|---|---|
| Main work | Data cleaning and quality check; summary tables; graphs 00 to 11; bottleneck analysis; the report; requirements check | Specifications; HWiNFO logging; wrote and maintains `Log-Test.ps1` (Bonus B); thermal-throttling analysis (Bonus A); GPU test results | Checked every raw CSV (rows, empty cells, time order); kept `Practice_Runs`; idle baseline and mixed workload set-up; runs the live demo |
| Gave the project | Cleaned CSVs; QC report; Graphs 00 to 11; report (DOCX + PDF) | Specs file; HWiNFO session files; `Scripts/Log-Test.ps1`; screenshots 01, 03, 04, 08 | Data-check notes; `Practice_Runs/`; screenshots 02, 06 |
| In the presentation | Introduction; architecture; results, bottlenecks and graphs (04, 06, 07, 08); verdict | Laptop and specs; HWiNFO; CPU test and throttling (Graphs 02, 03); GPU result | How tests were run; the script; live demo; data checks |
| Explains | Bottleneck per workload; utilization vs performance; why a laptop is slow at low CPU; pagefile; storage and cache; limitations | Cores vs threads; why HWiNFO; counters and try/catch; no throttling (four signs); GPU test; the invalid first CPU run and its fix | Two windows and logging first; the workloads; idle baseline and its short rest; data checks; why raw files are never edited |

**Order of work:** (1) specs recorded, `Log-Test.ps1` written, HWiNFO started before each test that needs sensors; (2) all three run the tests (logger first, then the workload; the first CPU run failed because this order was reversed); (3) raw CSVs go into `Raw_Logs/` and are never edited, and Abdul checks them; (4) Nabia cleans the data and draws the graphs; (5) Nabia writes the report; all three review before submission.

## Tools and equipment

| Item | Category | How we used it |
|---|---|---|
| HP EliteBook 850 G5 | Hardware | The single machine under test |
| Windows 10 Pro | Operating system | Runs the tests and keeps the performance counters |
| PowerShell 5.1 (Get-Counter, Start-Job, Compress-Archive, Export-Csv) | Built-in tool | Reads 9 counters every 2 s; creates the CPU, RAM and storage loads; writes CSV rows |
| `Log-Test.ps1` | Our script (Bonus B) | Runs one logged test and saves one row every 2 seconds to `Raw_Logs/` |
| HWiNFO64 | Free tool | Clock speed, temperature, power and throttling flags (Bonus A) |
| Task Manager | Built-in tool | Visual check and screenshots (RAM, storage, mixed tests) |
| Browser (5 tabs) and full-screen video | Workload | Mixed workload and light GPU workload (the only use of the internet) |
| Excel | Software | Opens CSV files for quick checks |
| Python (pandas, matplotlib) | Software | Quality check, summary tables, graphs, report build |
| Microsoft Learn, HWiNFO, Intel ARK | References | Counter definitions, tool documentation, processor limits |
| Claude (Anthropic) | AI assistant | Helped draft the scripts and the first draft of the report; the group ran every test and checked every number against the raw files |

No database, cloud service or internet connection is needed to run the project.
