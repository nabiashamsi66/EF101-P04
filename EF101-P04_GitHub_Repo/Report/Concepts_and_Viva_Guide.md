# Concepts and Viva Guide (EF101-P04)

Use this file to answer questions. Each answer is short, uses everyday words, and ends with the number from our own data. Learn the idea, not the sentence.

## Part 1: Hardware words

**What is a CPU?**
The part that does all the calculations. Our CPU is an Intel Core i5-8250U. Think of it as the chef in a kitchen.

**What is the difference between a core and a thread?**
A core is one real worker. A thread is one task a worker can hold. Our CPU has 4 cores and 8 threads, so Windows sees 8 "logical processors". Think of 4 chefs, each juggling two orders.

**What is clock speed?**
How many steps the CPU takes per second, in GHz. In our CPU test the clock stayed at about 2.0 GHz.

**What is temperature, and why does it matter?**
How hot the chip is. Heat is the enemy of chips. In our CPU test the highest temperature was 66 to 67 °C.

**What is throttling?**
The chip slows itself down to avoid damage from heat or too much power. In our two CPU runs there was no throttling. The clock did not fall, and HWiNFO reported no throttling.

**What is the power limit (PL1)?**
The long-term power the CPU is allowed to use. On our laptop it is 18 W. In the CPU test the CPU used about 8 to 9 W, so the limit was not reached.

**What is RAM?**
The fast short-term memory of the computer. Running programs keep their data there. Think of a chef's working table. Our laptop has 8 GB installed (7.8 GB usable).

**What is the pagefile?**
A file on the SSD that Windows uses as extra memory when RAM is full. It is much slower than RAM. Think of putting ingredients in the fridge when the table is full.

**What is paging?**
Moving data between RAM and the pagefile. In our RAM test, paging came in bursts (peak 4175 pages per second).

**What is the SSD, and what is disk throughput?**
The SSD is the storage. Throughput is how much data it moves per second (MB/s). In the storage test it wrote about 257 MB/s.

**What is a disk queue?**
How many disk requests are waiting in line. In our storage test the longest queue was about 1.8, so the disk was busy but not overloaded.

**What is an integrated GPU?**
A graphics chip built into the processor package. It shares memory and power with the CPU. Our GPU is an Intel UHD 620.

## Part 2: Measurement words

**What is utilization?**
How busy a part is, as a percentage. CPU utilization of 97.6 % means the CPU was almost fully busy.

**What is performance?**
How quickly the work is finished. Utilization and performance are different. A part can be 100 % busy and still fast, if its speed stays steady.

**What is a bottleneck?**
The one part that limits the whole task. It is the narrowest door in a crowd. The bottleneck is different for each test: CPU in the CPU test, memory in the RAM and mixed tests, disk in the storage test.

**What is a baseline?**
The normal state of the laptop when it does nothing (idle). Every other test is compared with it. Our idle baseline: CPU about 6 %, free memory about 3.2 GB on average (lowest 3.06 GB).

**What is sampling?**
Taking a reading at a regular time. Our script reads every 2 seconds, which is inside the 1 to 5 second range the project asks for.

**What is a counter?**
A number that Windows keeps up to date, such as "% Processor Time" (how busy the CPU is) or "Available MBytes" (free memory). Our script reads nine counters.

**Why CSV?**
CSV is a plain table of text, with values separated by commas. Excel opens it easily, and anyone can check it. We never edit the raw CSV files.

## Part 3: Our project

**What does Log-Test.ps1 do?**
It asks Windows for nine counters every 2 seconds, adds a timestamp and units, and writes one row to a CSV file. Each row is saved at once, so data is not lost if the test is stopped.

**Why do we run two PowerShell windows?**
Window 1 runs the logging. Window 2 runs the workload. Logging starts first, so the start of the load is recorded.

**Why was the first CPU test invalid?**
Logging stopped before the load started. The CPU test was therefore repeated on 18 October, and that run is used. We say this openly in the report.

**Why did we use HWiNFO too?**
Windows counters do not show temperature, clock speed or throttling. HWiNFO reads the hardware sensors.

**Why is the CPU load about 9 minutes and not 10?**
The timer started a little before the load jobs started, so the load ended a little earlier. We report the real length.

**What does the storage test really measure?**
How fast the SSD writes data. Reads were low because Windows keeps recent files in memory. The write number is the reliable one.

**What is the GPU test?**
A 5-minute full-screen video. It uses the GPU lightly. We did not run a heavy 3D test, and we say this in the report.

## Part 4: Questions about results

**Q: The CPU was at 97 %. Why was the speed not higher?**
The CPU shares its power and heat budget across all cores. With all 8 threads busy, the speed settles at a steady value. The speed did not fall during the load, which is what matters for throttling.

**Q: How do you know there was no throttling?**
Three things together: the speed did not drop during the load, the temperature stopped rising at 66 to 67 °C, and the power stayed far below the 18 W limit. HWiNFO also reported no throttling.

**Q: Why is the computer slow in the mixed test if the CPU is only 17 % busy?**
Free memory fell to about 1.5 GB and committed memory reached 82 %. Windows moved data to the pagefile, and programs waited for the SSD. The CPU was idle while waiting, so the CPU number looks low, but the computer still feels slow.

**Q: Is a big pagefile always a sign of memory trouble?**
No. During the CPU test the pagefile grew a little, while free memory stayed above 3.2 GB. Windows also moves rarely used data there.

**Q: What happened after the CPU load?**
The temperature fell from about 65 °C back to about 36 to 43 °C within five minutes. The speed returned to the idle level.

**Q: What did the GPU do?**
Its use rose from about 1 % to about 20 % during the video. The clock stayed near 300 MHz, and the highest temperature was 55 °C. No throttling was reported.

**Q: Which test had the biggest limit?**
The storage test. The disk wrote about 257 MB/s and was busy 46 % of the time.

**Q: Which test was limited by the CPU?**
The CPU test. It was 97.6 % busy and its speed stayed steady.

**Q: How do you know the data is correct?**
Every file was checked for the right number of rows, empty cells, and time order. The CPU test was repeated, and both runs gave the same result. Screenshots show the tools during each test.

**Q: What would you do with more time?**
Repeat every test three times, time a fixed task to measure how long it takes, rest the laptop longer before the idle test, and do a heavy GPU test.

## Part 5: Difficult follow-up questions

**Q: Your utilization is high. Does that mean the computer is slow?**
Not always. High utilization means the part is busy. It does not mean the work is slow. In the CPU test the CPU was busy and the speed was steady.

**Q: Why not just use Task Manager?**
Task Manager shows the numbers only on screen and only for the moment. Our script saves a number every 2 seconds into a file, so we can compare tests, draw graphs, and check the data later.

**Q: What would happen if the Internet were disconnected?**
Nothing in the project would change. The project uses only local Windows tools. Only the video in the mixed and GPU tests would stop.

**Q: What would happen if the Raw_Logs folder were deleted?**
The raw data would be lost and the tests would have to be run again. The script creates the folder again if it is missing, but it cannot bring back deleted files.

**Q: Which parts of your work did AI help with?**
An AI assistant helped write the scripts and the first draft of the report. The group ran the scripts on the laptop, checked the numbers against the raw files, and can explain every script line. This is written in the report's AI disclosure.

**Q: Can you explain one line of your script?**
For example: `Get-Counter -Counter $c -SampleInterval 2 -MaxSamples ($Minutes*30)`. It asks Windows for all nine counters every 2 seconds. With 5 minutes, that is 5 × 30 = 150 readings.

**Q: Why are the numbers in the graphs different from the numbers in Task Manager?**
Task Manager shows a number at one moment. Our graphs show the average or the highest value over a full test, taken every 2 seconds. A single moment can look different from an average.
