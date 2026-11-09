# Presentation, Demonstration and Viva Guide (EF101-P04)

This guide explains how to present the project, what to show live, and what each member must be able to explain. The handbook (sections 2.4, 2.5 and 3) says that evaluation includes a live demonstration, live modifications and an individual viva. Every member must understand the whole system, not only their own part.

## 1. What the instructor will check (from the handbook)
- The working project runs and can be demonstrated (here: the logging tool and the measurement setup).
- The group can explain the architecture, the data flow and where data is stored.
- The group can answer: what happens when the user presses a button, which parts run on the device, what happens without Internet, what happens if the storage is deleted, why these tools were chosen, and one limitation.
- The instructor may ask the group to add a record, change a configuration value, enter incorrect input, trace one operation, identify a component, and make one small modification.
- Each member answers questions individually (viva, 15 % of the marks).

## 2. Setup before the session (checklist)
- [ ] Laptop charged and on the charger. Sleep set to Never. Browser closed.
- [ ] Folder open: `Documents\EF101-P04` (Raw_Logs, Cleaned_Data, Graphs, Report, Scripts).
- [ ] Report (PDF) and graph 00 (architecture) open on a second screen or printed.
- [ ] PowerShell Window 1 open, with `Log-Test.ps1` loaded (run the two load lines first and check with `Get-Command Log-Test`).
- [ ] Excel open with one CSV from Raw_Logs (for showing the data).
- [ ] Tested beforehand: the one-minute pilot and the two "incorrect input" and "small modification" tests in section 4 (record what really happens).

## 3. Demonstration flow (about 10 minutes)

| Step | What to show | What to say (short) | Who speaks |
|---|---|---|---|
| 1 | Architecture diagram (Graph 00) | Components: PowerShell + Get-Counter, workloads, HWiNFO, CSV, cleaning script, graphs. | Nabia |
| 2 | Folder structure | Where raw data lives (Raw_Logs, never edited), where cleaned data lives (Cleaned_Data). | Abdul |
| 3 | Specs file (`Report\specs_utf8.txt`) | Test machine: i5-8250U, 4 cores, 8 threads, 8 GB, SSD, Windows 10, integrated GPU. | Areeza |
| 4 | Live run: `Log-Test -Test pilot -Minutes 1` | The script prints the file name, then after one minute `Done:`. A new CSV appears in Raw_Logs. Open it in Excel. | Abdul |
| 5 | Trace one row | One row = one call of Get-Counter, with timestamp, elapsed seconds, and 9 counter values with units. | Abdul |
| 6 | Graph 08 (idle vs tests) | Idle is the baseline. CPU, RAM, storage and mixed compared with idle. | Nabia |
| 7 | Graph 02 (CPU load, two runs) | Clock stays near 2 GHz, temperature levels off at 66 to 67 °C, power stays below 18 W. No throttling. | Areeza |
| 8 | Graph 04 or 05 (RAM) | Available RAM falls to 1.1 GB, committed rises to 86 %, pagefile and paging rise. RAM pressure. | Areeza |
| 9 | Graph 06 (storage) | Writes about 257 MB/s, disk active 46 %: disk is the limit. | Nabia |
| 10 | Graph 07 (mixed) | CPU only 17 %, but RAM and paging are stressed: the system feels slow with a low CPU. | Nabia |
| 11 | Graph 08 (idle vs all tests, GPU included) | Integrated GPU: light use during video (about 20 % average), low clock, 55 °C at most. A heavy 3D stress test was not run. | Areeza |
| 12 | Conclusion | Utilization alone does not explain slowness. Read memory, paging, disk queue and clock together. | Nabia |

## 4. Live modification tests (prepare and test before the session)
The instructor may ask for these. Test each one on the laptop before the session, and write down the exact result, so you are not surprised.

1. **Add a new record and show where it appears:** run a new one-minute pilot with a new name, `Log-Test -Test demo -Minutes 1`. The new file `demo_<date>_<time>.csv` appears in Raw_Logs and can be opened in Excel.
2. **Change a configuration value:** in `Log-Test.ps1`, the sampling interval is `-SampleInterval 2`. Change it to `-SampleInterval 5` in a copy of the script, run a one-minute test, and show that the timestamps now differ by 5 seconds. Put the file back afterwards. Also `-Minutes` controls the test length.
3. **Enter incorrect input:** run `Log-Test -Test demo -Minutes 0` (or a misspelled counter name in a copy of the script). Show the exact message and explain: the `try/catch` block prints `ERROR:` instead of crashing, and a bad counter name stops the reading. Run it once before the session and remember the exact message.
4. **Trace one operation:** pick the RAM counter `\Memory\Available MBytes`. Show it in the `$c` list, show it in the output CSV column `ram_available_mb`, and show the RAM graph (Graph 04).
5. **Identify the component:** `\Processor(_Total)\% Processor Time` = CPU. `\Memory\...` = RAM. `\PhysicalDisk(_Total)\...` = SSD. HWiNFO = temperature, clock, power.
6. **Small modification:** add one column to the output, or change a label. Example: rename `cpu_percent` to `cpu_utilization_percent` in the script. Test it first and save a backup copy of the script before the session.

## 5. What each member must be able to explain

**Areeza Rehan (specifications, HWiNFO, logging script, thermal):**
- Specs and what each one means (cores vs threads, RAM, SSD, integrated GPU).
- Why HWiNFO is needed (temperature, clock, power, throttling flags). Bonus A result: no throttling; the reasons (clock stable, temperature levelled off, power far below PL1 18 W, no flags). Graph 02 and Graph 03 (cooldown).
- How Log-Test.ps1 works (Bonus B): counters, Get-Counter every 2 s, timestamps and units, Export-Csv -Append, try/catch. The CSV is written row by row, so data is kept if the test is stopped.
- The invalid first CPU run: it recorded no load because logging stopped before the load started. Fixed by starting logging first and the load in Window 2.
- RAM pressure (Graph 04, 05) and the GPU test (Graph 09 to 11).

**Abdul Muqeet (idle, mixed, data checks, live demo):**
- The idle baseline and why it is short (about 20 s of rest), and the mixed workload (browser with 5 tabs + video + zipping).
- The data checks: row count (150 or 330), no empty cells, timestamps in order. Why raw files are never edited, and what Practice_Runs is.
- The live demo: folder structure, the one-minute run, tracing one CSV row, the live modification (section 4).

**Nabia Shamsi (storage, cleaning, graphs, analysis, report):**
- The storage test (1 GB file write and 600 MB zip), why the read speed is low (Windows cache), and the cleaning and quality-check scripts (`Scripts/analysis/analyze_logs.py` re-checks the numbers).
- Bottleneck per workload (Table 4 in the report).
- Utilization versus performance: CPU at 97.6 % with a steady clock (good performance); mixed CPU at 17 % but slow (memory and disk).
- Pagefile: used when RAM is full. Pagefile use does not always mean RAM shortage (CPU test pagefile rose while RAM stayed above 3.2 GB). Limitations.

Every member should be able to answer a question about any graph, not only their own.

## 6. Likely questions (short answers)

**Q: Why is the CPU at 97 % but the clock is not higher?**
The processor shares its power and heat budget across cores. Under a load on all 8 logical processors, the clock settles at a sustained all-core value. We did not measure the maximum turbo frequency, so we do not claim how far it is from the maximum.

**Q: How do you know it is not thermal throttling?**
Three things together: the clock did not fall over the load, the temperature levelled off at 66 to 67 °C, and power stayed far below the 18 W PL1 limit. HWiNFO throttling flags stayed "No".

**Q: Why did you need two CPU runs?**
The first PowerShell run recorded no load, because logging stopped before the load started. The second run was valid. A second HWiNFO run on the same day showed the same pattern, which supports the result.

**Q: What does the idle baseline tell you?**
It is the normal state of the computer. Every test is compared with it. Idle CPU was 6 %, free RAM about 3.2 GB.

**Q: Why is the storage read speed so low?**
Windows keeps recently used files in a memory cache. Many reads came from the cache and did not reach the SSD. The write speed (257 MB/s) is the reliable value.

**Q: Why does the mixed test feel slow with a low CPU?**
Free RAM fell to 1.5 GB and committed memory reached 82 %. Windows moved pages to the pagefile, and programs waited for the SSD. The CPU was idle while waiting.

**Q: Is the pagefile a sign of memory shortage?**
Not always. In the CPU test the pagefile rose from 14.8 % to 17.7 % while free RAM stayed above 3.2 GB. Windows also moves inactive pages.

**Q: What is the limitation of the GPU results?**
The GPU is integrated, and the test was a light workload (full-screen video), not a 3D stress test. The results describe this light load only.

**Q: What would happen without Internet?**
The measurements, logs and graphs do not need Internet. Only the video in the mixed and GPU tests would stop.

**Q: What would happen if the Raw_Logs folder were deleted?**
The raw data would be lost, and the tests would have to be repeated. The script creates the folder again if it is missing, but it cannot restore deleted files. The cleaned copies and the report would not be affected.

**Q: Why PowerShell and not Python?**
PowerShell is built into Windows and reads the performance counters directly, with no installation. Python was used only for the analysis after the measurements.

**Q: Why CSV?**
It is simple, readable in Excel, and easy to check (row count, empty cells, time order).

**Q: Which AI tools were used?**
An AI assistant (Claude, Anthropic) helped draft the scripts and the report. The group tested the scripts on the laptop and checked all numbers against the raw CSV files. The disclosure is in Section 12 of the report.

## 7. Limitations to state yourself (do not wait to be asked)
- Each RAM, storage and mixed test was run once. Only the CPU load was repeated.
- The idle baseline had only about 20 seconds of rest before logging.
- The CPU load lasted about 9 minutes, not 10.
- No dedicated GPU stress test was run.
- Task completion time was not measured.
- One laptop only.

## 8. Time plan on the day
- 1 minute: introduction and architecture (Nabia).
- 8 minutes: demonstration (steps 1 to 12 in section 3). Each member speaks at least once.
- 3 minutes: live modification (section 4), done by Abdul with Areeza guiding.
- Remaining time: questions. Each member answers at least one question individually.
