from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE='/home/claude/final/EF101-P04'
G=f'{BASE}/Graphs'
OUT=f'{BASE}/Report/EF101-P04_Project_Report.docx'
NAVY=RGBColor(0x1F,0x3A,0x5F); TEAL=RGBColor(0x2E,0x7D,0x8C); GREY=RGBColor(0x55,0x55,0x55)

doc=Document()
st=doc.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(10.5)
st.element.rPr.rFonts.set(qn('w:eastAsia'),'Calibri')
st.paragraph_format.space_after=Pt(6); st.paragraph_format.line_spacing=1.12
for name,size,color in [('Heading 1',14,NAVY),('Heading 2',11.5,TEAL)]:
    s=doc.styles[name]; s.font.name='Calibri'; s.font.size=Pt(size); s.font.bold=True; s.font.color.rgb=color
    s.paragraph_format.space_before=Pt(12 if name=='Heading 1' else 8); s.paragraph_format.space_after=Pt(4)
sec=doc.sections[0]; sec.left_margin=sec.right_margin=Cm(2.2); sec.top_margin=Cm(2.0); sec.bottom_margin=Cm(2.0)

def field(par,instr):
    r=par.add_run(); a=OxmlElement('w:fldChar'); a.set(qn('w:fldCharType'),'begin')
    it=OxmlElement('w:instrText'); it.set(qn('xml:space'),'preserve'); it.text=instr
    b=OxmlElement('w:fldChar'); b.set(qn('w:fldCharType'),'end'); r._r.append(a); r._r.append(it); r._r.append(b)
h=sec.header.paragraphs[0]; h.text='EF101-P04  |  Computer Hardware Stress Testing and Resource Analysis'; h.runs[0].font.size=Pt(8.5); h.runs[0].font.color.rgb=GREY
f=sec.footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.CENTER; rr=f.add_run('Page '); rr.font.size=Pt(8.5); field(f,'PAGE')

def shade(cell,hexc):
    tcPr=cell._tc.get_or_add_tcPr(); s=OxmlElement('w:shd'); s.set(qn('w:val'),'clear'); s.set(qn('w:color'),'auto'); s.set(qn('w:fill'),hexc); tcPr.append(s)
def H1(t): doc.add_heading(t,level=1)
def H2(t): doc.add_heading(t,level=2)
def P(t,bold=False,italic=False,size=None,color=None,align=None):
    p=doc.add_paragraph(); r=p.add_run(t); r.bold=bold; r.italic=italic
    if size: r.font.size=Pt(size)
    if color: r.font.color.rgb=color
    if align is not None: p.alignment=align
    return p
def BUL(items):
    for i in items:
        p=doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after=Pt(3)
        if isinstance(i,tuple): r=p.add_run(i[0]); r.bold=True; p.add_run(i[1])
        else: p.add_run(i)
def TABLE(rows,widths,caption=None,font=9):
    if caption:
        c=doc.add_paragraph(); r=c.add_run(caption); r.bold=True; r.font.size=Pt(9.5); r.font.color.rgb=NAVY
        c.paragraph_format.space_after=Pt(2); c.paragraph_format.keep_with_next=True
    t=doc.add_table(rows=len(rows),cols=len(rows[0])); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False
    for j,w in enumerate(widths): t.columns[j].width=Cm(w)
    for i,row in enumerate(rows):
        for j,val in enumerate(row):
            cell=t.cell(i,j); cell.width=Cm(widths[j]); cell.text=''
            p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(0)
            run=p.add_run(str(val)); run.font.size=Pt(font)
            if i==0: run.bold=True; run.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); shade(cell,'1F3A5F')
            elif i%2==0: shade(cell,'EAF0F7')
    doc.add_paragraph().paragraph_format.space_after=Pt(2)
def FIG(path,caption,w=15.5):
    doc.add_picture(path,width=Cm(w)); doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
    c=doc.add_paragraph(); r=c.add_run(caption); r.italic=True; r.font.size=Pt(8.5); r.font.color.rgb=GREY
    c.alignment=WD_ALIGN_PARAGRAPH.CENTER; c.paragraph_format.space_after=Pt(8)
def BOX(title,text):
    t=doc.add_table(rows=1,cols=1); t.alignment=WD_TABLE_ALIGNMENT.CENTER; c=t.cell(0,0); c.width=Cm(16.5); shade(c,'EAF0F7')
    p=c.paragraphs[0]; r=p.add_run(title+'  '); r.bold=True; r.font.color.rgb=NAVY; r.font.size=Pt(10)
    r2=p.add_run(text); r2.font.size=Pt(10)
    doc.add_paragraph().paragraph_format.space_after=Pt(2)

# ---------- COVER ----------
for _ in range(4): doc.add_paragraph()
P('EF-101 Fall 2026  |  System Understanding Project',size=11,color=GREY,align=WD_ALIGN_PARAGRAPH.CENTER)
P('EF101-P04',bold=True,size=14,color=TEAL,align=WD_ALIGN_PARAGRAPH.CENTER)
P('How a Laptop Behaves Under Load',bold=True,size=24,color=NAVY,align=WD_ALIGN_PARAGRAPH.CENTER)
P('Measuring the CPU, memory, storage and graphics of one laptop, and finding what slows it down',italic=True,size=12,color=GREY,align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()
TABLE([['Item','Details'],
       ['Group members','Student A: ______________________\nStudent B: ______________________\nStudent C: ______________________'],
       ['Test laptop','HP EliteBook 850 G5, Intel Core i5-8250U, 8 GB RAM, 256 GB SSD, Windows 10 Pro'],
       ['Measurement dates','15, 18 and 21 October 2026'],
       ['Submission','Monday, 9 November 2026 (Week 13)']],[4.2,12.3],font=10)
doc.add_page_break()

# ---------- SUMMARY ----------
H1('1. The project in one page')
P('We wanted to know one simple thing: when a laptop is given different kinds of work, which part gets full first, and does that part slow the whole computer down? To find out, we gave the laptop five kinds of work, one at a time, and recorded its numbers every two seconds. We then compared every test with a resting laptop, which we call the baseline.')
P('What we found, in plain words:',bold=True)
BUL([('The processor (CPU) can be fully used without slowing down. ','During the CPU test the processor was busy 97.6 % of the time. Its speed stayed about the same and its temperature stopped rising at about 66 °C. It did not slow itself down to protect itself.'),
     ('Memory (RAM) is a common limit. ','In the RAM test the free memory dropped from about 3.4 GB to 1.1 GB. The computer then started to use a part of the SSD as extra memory, which is much slower.'),
     ('The SSD is a limit when we write a lot of data. ','The storage test wrote about 257 MB/s, and the disk was busy almost half of the time.'),
     ('A computer can feel slow while the processor is not full. ','In the mixed test (browser, video and file zipping) the processor was only 17 % busy, but memory was almost full and the computer was waiting for the disk. This explains most “slow computer” situations.'),
     ('The graphics chip (GPU) is light. ','When a video played full screen, the GPU was used about 20 % on average and reached only 55 °C. This laptop has a built-in GPU, so it shares memory and power with the processor.')])
BOX('Main message:','Look at several numbers together. A busy processor alone does not explain a slow computer. Memory, the virtual memory file, the disk and the speed of the processor tell the real story.')

# ---------- CONCEPTS ----------
H1('2. Key ideas explained simply')
P('Each idea below is explained with an everyday example. These are the words the teacher is likely to ask about.')
TABLE([['Idea','Simple meaning','Everyday example'],
       ['CPU (processor)','The part that does the calculations of every program.','The chef in a kitchen.'],
       ['Core and thread','A core is one worker. A thread is one task a worker can hold. Our CPU has 4 cores, so it can handle 8 tasks at once (8 threads).','Four chefs, and each chef can juggle two orders.'],
       ['Utilization','How busy a part is, as a percentage.','How many minutes the chef was busy in one hour.'],
       ['Clock speed','How many steps per second the CPU takes. Measured in GHz.','How fast the chef moves their hands.'],
       ['Temperature','How hot the chip is, in °C.','How hot the kitchen gets.'],
       ['Throttling','The chip slows itself down to avoid damage from heat or too much power.','The chef slows down when the kitchen is too hot.'],
       ['Power limit (PL1)','The long-term amount of power the CPU may use. Our laptop: 18 W.','The gas supply limit of the kitchen.'],
       ['RAM','Fast short-term memory where running programs keep their data.','The chef\'s working table.'],
       ['Pagefile (virtual memory)','A file on the SSD that Windows uses as extra memory when RAM is full.','Putting ingredients in the fridge when the table is full. It works, but it is slower.'],
       ['Paging','Moving data between RAM and the pagefile.','Walking to the fridge again and again.'],
       ['Disk throughput','How much data the disk moves per second (MB/s).','How many plates the waiter carries per minute.'],
       ['Disk queue','How many disk requests are waiting in line.','A line of customers at the counter.'],
       ['Bottleneck','The one part that limits the whole task.','The narrowest door in a crowd.'],
       ['Integrated GPU','A graphics chip built into the CPU package. It shares memory and power with the CPU.','A chef who also works at the same table.'],
       ['Baseline (idle)','How the laptop behaves when it is doing nothing. Every other test is compared with it.','The kitchen on a quiet morning.'],
       ['Sampling','Taking a reading at a regular time. We read every 2 seconds.','Checking a clock every 2 seconds.']],[3.6,7.2,5.7],font=8.5)

# ---------- HOW WE MEASURED ----------
H1('3. How we measured')
P('The system has four simple parts. Figure 1 shows them.')
FIG(f'{G}/00_system_architecture.png','Figure 1. The measurement system. A workload runs, Windows counts what happens, our script saves the counts to a file, and HWiNFO reads the hardware sensors.',w=15.5)
BUL([('Workloads: ','small programs that give the laptop a specific job: a CPU job, a memory job, a storage job, a mixed job (browser with video plus zipping files), and a GPU job (full-screen video).'),
     ('Log-Test script (PowerShell): ','every two seconds it reads nine Windows numbers and writes one row to a CSV file. CSV is a plain text table that Excel can open.'),
     ('HWiNFO: ','reads the hidden sensors: clock speed, temperature, power and throttling flags.'),
     ('Cleaning and graphs: ','we checked every file (row count, empty cells, time order), and made the graphs from the clean copies. Raw files were never changed.')])
P('What happens, step by step, when a test runs:',bold=True)
for i,t in enumerate(['We start the logging script in one PowerShell window.','We start the workload in a second window.','Windows keeps counting: how busy the CPU is, how much memory is free, how much the disk works.','Every two seconds the script reads these numbers and saves one row.','HWiNFO saves the sensor values in its own file at the same time.','After the test we check the files and draw graphs.'],1):
    p=doc.add_paragraph(style='List Number'); p.paragraph_format.space_after=Pt(2); p.add_run(t)
P('Does it need the Internet? No. The whole project runs on the laptop. The browser in the mixed test loads a web page and a video, but that is part of the workload, not something the project depends on.')
P('Where is the data? In the folder Documents\\EF101-P04. Raw_Logs keeps the original files, which are never edited. Cleaned_Data keeps the checked copies and summaries.')
P('What if the data is deleted? A deleted raw file cannot be recovered, so that test would need to be run again. The cleaned copies and the report would also be lost unless they were copied elsewhere.')

H2('3.1 The laptop and the tools')
TABLE([['Item','Value'],
       ['Laptop','HP EliteBook 850 G5 (battery present)'],
       ['Processor','Intel Core i5-8250U: 4 cores, 8 threads'],
       ['Memory','8 GB installed (7.8 GB usable), pagefile 2 GB'],
       ['Graphics','Intel UHD Graphics 620 (built into the processor)'],
       ['Storage','256 GB SSD (Samsung)'],
       ['Operating system','Windows 10 Pro'],
       ['Tools','PowerShell (Get-Counter), our Log-Test script, HWiNFO64, Task Manager, Excel']],[4.5,12.0],caption='Table 1. The laptop and the tools')

# ---------- TESTS ----------
H1('4. The tests')
TABLE([['Test','What we did, in simple words','Why we did it'],
       ['Idle (baseline)','Did nothing for 5 minutes.','To know the normal state.'],
       ['CPU load','Ran a loop on all 8 processor threads for about 9 minutes.','To make the processor fully busy.'],
       ['Cooldown','Did nothing for 5 minutes after the CPU load.','To see how fast the chip cooled down.'],
       ['RAM load','Filled memory in steps until only about 1.5 GB was free (about 4.5 minutes).','To see what happens when memory is full.'],
       ['Storage load','Wrote and read a 1 GB file again and again (about 4 minutes).','To test how fast the SSD works.'],
       ['Mixed','Browser with 5 tabs and a video, plus zipping 600 MB of files (about 4 minutes).','To copy a real day of work.'],
       ['GPU (video)','Full-screen video for 5 minutes.','To see how the built-in graphics chip works.']],[3.2,8.2,5.1],caption='Table 2. The tests')
P('Each test ran for 5 minutes, except the CPU test (11 minutes, so we could see the start and the end of the load). Every test started logging before the work began. The CPU test was run twice: the first try recorded nothing, because logging stopped before the load began. The second try is the one we use.')

# ---------- RESULTS ----------
H1('5. Results')
P('The table shows the average of each test. The “lowest free memory” is the smallest amount of memory left during the test.')
TABLE([['Test','CPU average','Lowest free memory','Disk writing (average)','Disk busy (average)','GPU use (average)'],
       ['Idle','6.1 %','3.06 GB','0.3 MB/s','1.1 %','1.2 %'],
       ['CPU load','97.6 %','3.25 GB','0.4 MB/s','13.6 %','1.8 %'],
       ['RAM load','11 %','1.10 GB','0.7 MB/s','1.2 %','4.5 %'],
       ['Storage','18 %','1.83 GB','256.7 MB/s','46.3 %','3.6 %'],
       ['Mixed','17.5 %','1.53 GB','10.4 MB/s','3.9 %','1.7 %'],
       ['GPU (video)','39.3 %','2.47 GB','2.1 MB/s','2.7 %','20.5 %']],[3.1,2.4,3.0,3.3,3.0,2.7],caption='Table 3. Summary of results (each test averaged over its own load time)')
FIG(f'{G}/08_comparison_idle_vs_all_tests.png','Figure 2. Idle compared with every test. Each bar is one test. The GPU test is included, so every test can be compared with idle.',w=16.0)
FIG(f'{G}/02_hwinfo_cpu_load_two_runs.png','Figure 3. CPU load, two separate runs on two days. Both runs show the same pattern: full use, steady speed, and no slow-down.',w=14.5)

# ---------- ANALYSIS ----------
H1('6. What the results mean')
H2('6.1 Which part is the limit in each test?')
TABLE([['Test','The limit','Why, in simple words'],
       ['CPU load','The processor','The processor was full, and its speed stayed steady. Nothing else was waiting.'],
       ['RAM load','Memory','Memory was almost full, so Windows used the SSD as extra memory. The SSD is slow, so programs waited.'],
       ['Storage','The disk','The disk was busy almost half of the time and wrote 257 MB/s. The processor was mostly free.'],
       ['Mixed','Memory, and then the disk','The processor was only 17 % busy, yet memory was nearly full and the computer kept waiting for the disk. This is why the computer feels slow.'],
       ['GPU (video)','Nothing','The GPU was lightly used and stayed cool. No limit was reached.']],[2.8,3.6,10.1],caption='Table 4. The limit in each test')
H2('6.2 Busy is not the same as fast')
P('“Busy” (utilization) tells you how much of a part is working. “Fast” (performance) tells you how quickly the work is finished. In the CPU test the processor was 98 % busy and still fast, because its speed did not drop. In the mixed test the processor was only 17 % busy, yet the computer was slow, because the work was waiting for memory and the disk. So a low busy number does not mean the computer is fast.')
H2('6.3 What happens when memory is full')
P('When free memory becomes small, Windows moves some data from RAM to the pagefile on the SSD. The SSD is much slower than RAM, so each program that needs that data has to wait. In the RAM test, the waiting happened in short bursts. Most of the time nothing was moved, but at some moments many pages were moved at once.')
P('An important point: the pagefile is not only used when memory is full. During the CPU test the pagefile grew a little, even though there was plenty of free memory. Windows also moves rarely used data there to keep RAM free. So a bigger pagefile does not always mean there is a memory problem.')
H2('6.4 Does the processor slow down when it gets hot? (Bonus A)')
P('This is the main question of the thermal bonus. We ran the CPU load twice, on two different days, and watched the speed, the temperature and the power.')
TABLE([['What we watched','Run 1','Run 2','What it means'],
       ['Speed at the start and end of the load','2005 → 2063 MHz','2022 → 1975 MHz','Speed stayed about the same (+3 % and -2 %). No steady drop.'],
       ['Highest temperature','66 °C','67 °C','The temperature rose and then levelled off. It stayed far from the danger level.'],
       ['Power used','8.6 W','8.4 W','Far below the limit of 18 W.'],
       ['Throttling warnings','None','None','The laptop never reported that it slowed itself down.']],[4.8,2.8,2.8,6.1],caption='Table 5. CPU load, two runs')
P('What we conclude: in these two runs the processor did not slow down because of heat or power. After the load, the temperature went back to about 36 to 43 °C within five minutes (Figure 4). We only tested two loads of about 9 minutes on one laptop, so we cannot say this is true for every laptop or for a much longer load.',bold=False)
FIG(f'{G}/03_cooldown_recovery_hwinfo.png','Figure 4. Cooldown after the CPU load. The temperature falls back close to its starting value within about five minutes.',w=14.5)
H2('6.5 The graphics chip (GPU)')
P('The GPU was used in one light test: a full-screen video. Its use rose from about 1 % (idle) to about 20 % on average. The clock speed stayed near 300 MHz, with short jumps to about 450 MHz. The highest temperature was 55 °C, and HWiNFO reported no throttling. This laptop has a built-in GPU, so it shares its power and memory with the processor. We did not run a heavy 3D test, so the GPU result describes only this light video load.')
FIG(f'{G}/10_gpu_test_timeline.png','Figure 5. GPU during the 5-minute video test: usage, clock speed, temperature and memory.',w=14.5)
H2('6.6 Two different kinds of work: CPU and storage')
P('The CPU test and the storage test push on different parts. The CPU test kept the processor at 98 % and hardly used the disk (0.4 MB/s). The storage test used the disk heavily (257 MB/s) while the processor stayed at 18 %. So the same laptop can be limited by a different part, depending on the work.')
H2('6.7 Why a slow computer can have a low CPU number')
P('The mixed test is the best example. The processor looked almost idle, but free memory fell to about 1.5 GB and the computer kept moving data to the SSD. Each time a program needed that data, it waited. The CPU was not the problem: the waiting was.')

# ---------- BONUS ----------
H1('7. Bonus tasks')
BUL([('Bonus A, thermal throttling: ','we tested it on the laptop with two CPU loads and found no throttling. The method and the numbers are in section 6.4.'),
     ('Bonus B, logging script: ','Log-Test.ps1 records nine Windows numbers every two seconds into a CSV file with a timestamp. It was used in every test. Its main idea: it asks Windows for the numbers, adds the time and units, and writes each row at once, so no data is lost if the test is stopped early.')])

# ---------- CHECKS ----------
H1('8. How we know the data is correct')
BUL(['Every file was checked: the right number of rows (150 for 5-minute tests, 330 for the CPU test), no empty cells, and times that always go forward.',
     'The CPU load was run twice, and both runs gave the same result.',
     'The first CPU attempt recorded no load, because logging had stopped before the load started. We did not use it, and we explain this in the report.',
     'Screenshots were taken during each test, so we can check the tool readings with our own eyes.'])

# ---------- LIMITS ----------
H1('9. Limits of this project')
BUL(['Each RAM, storage, mixed and GPU test was run once. Only the CPU test was repeated.',
     'The idle baseline had only about 20 seconds of rest before logging. A longer rest would be better.',
     'The CPU load lasted about 9 minutes, not 10, because the timer started a little before the load jobs.',
     'The storage read speed is low because Windows keeps recent files in memory. The write speed is the reliable number.',
     'The GPU test was a light video test, not a heavy 3D stress test.',
     'We did not measure how long a fixed task takes, so “fast” is judged from speed and disk numbers only.',
     'The results are for one laptop only.'])

# ---------- SAFETY ----------
H1('10. Safety')
P('We did not overclock the laptop, change its voltage, or turn off its heat protection. Each test had a stop rule: stop if the temperature reached 95 °C or the laptop froze. No test reached that point. The test laptop belongs to the group. No university computer was stress-tested.')

# ---------- CONTRIBUTIONS ----------
H1('11. Who did what')
P('The group must complete this table honestly. Every member should be able to explain the whole project, not only their own part.',italic=True)
TABLE([['Member','Main work','Explain in the viva'],
       ['Student A','Specifications, tools, HWiNFO, Bonus A','The laptop, the tools, the processor speed and temperature'],
       ['Student B','Workloads, the logging script, running the tests','How the workloads and the script work'],
       ['Student C','Cleaning, graphs, analysis, the report','The graphs, the limits, what each graph shows']],[3.0,6.8,6.7],caption='Table 6. Contribution table (to be completed by the group)')

# ---------- AI ----------
H1('12. Tools and AI disclosure')
BUL([('Tools used: ','Windows Task Manager, PowerShell (Get-Counter, Start-Job, Compress-Archive, Export-Csv), HWiNFO64 (www.hwinfo.com), Excel, and Python (pandas, matplotlib) for the graphs.'),
     ('AI assistance: ','an AI assistant (Claude, by Anthropic) helped write the scripts and the first draft of this report. The group ran the scripts on the laptop and checked every number against the raw files. The scripts are in the Scripts folder so they can be read and explained.')])

# ---------- CONCLUSION ----------
H1('13. Conclusion')
P('A laptop does not have one single limit. The processor was the limit in the CPU test, memory was the limit in the RAM and mixed tests, and the disk was the limit in the storage test. The built-in GPU was used only lightly, and the processor did not slow down from heat in our tests. The most useful lesson is this: when a computer feels slow, check memory and the disk before you blame the processor.')

H1('14. References')
for r_ in ['Microsoft. Get-Counter. Microsoft Learn. https://learn.microsoft.com/powershell/module/microsoft.powershell.diagnostics/get-counter',
           'Microsoft. Start-Job. Microsoft Learn. https://learn.microsoft.com/powershell/module/microsoft.powershell.core/start-job',
           'Microsoft. Compress-Archive. Microsoft Learn. https://learn.microsoft.com/powershell/module/microsoft.powershell.archive/compress-archive',
           'Microsoft. Export-Csv. Microsoft Learn. https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/export-csv',
           'HWiNFO. HWiNFO64 hardware monitoring software. https://www.hwinfo.com',
           'Intel. Intel Core i5-8250U specifications. Intel ARK. https://ark.intel.com (search i5-8250U)']:
    p=doc.add_paragraph(style='List Number'); p.paragraph_format.space_after=Pt(2); p.add_run(r_).font.size=Pt(9)
P('Check each link before submission and write the date you read it.',italic=True,size=9,color=GREY)

# ---------- APPENDIX ----------
doc.add_page_break()
H1('Appendix A: Files in the project folder')
TABLE([['Folder','What is inside'],
       ['Raw_Logs','The original measurement files: 6 PowerShell logs (idle, CPU, cooldown, RAM, storage, mixed), 1 GPU log, and 3 HWiNFO sensor logs.'],
       ['Cleaned_Data','Checked copies, summary tables, the comparison table, and the data-quality report.'],
       ['Practice_Runs','Earlier practice runs and the invalid first CPU run. Kept for honesty, not used in the results.'],
       ['Graphs','The graphs in this report and the extra graphs (00 to 11).'],
       ['Screenshots','Screenshots of specifications, HWiNFO, Task Manager and Excel checks.'],
       ['Scripts','Log-Test.ps1 (logging script) and analysis/ (cleaning and graph scripts).'],
       ['Report','This report (DOCX and PDF), the concept guide, the demo guide, the requirements check, and the data-quality report.']],[3.4,13.1],caption='Table A1. Folder contents')
H1('Appendix B: Additional graphs')
FIG(f'{G}/01_cpu_utilization_all_tests.png','Figure B1. CPU use over time for idle and every test.',w=15.0)
FIG(f'{G}/04_ram_available_and_committed.png','Figure B2. RAM test: free memory and committed memory.',w=15.0)
FIG(f'{G}/05_ram_pagefile_and_paging.png','Figure B3. RAM test: pagefile and paging.',w=15.0)
FIG(f'{G}/06_storage_throughput_and_activity.png','Figure B4. Storage test: how fast data moves and how busy the disk is.',w=15.0)
FIG(f'{G}/07_mixed_cpu_ram_disk.png','Figure B5. Mixed test: processor, memory and disk together.',w=15.0)
FIG(f'{G}/11_gpu_test_cpu_ram_disk.png','Figure B6. GPU test: processor, memory and disk during the same five minutes.',w=15.0)

doc.save(OUT); print('saved',OUT)
