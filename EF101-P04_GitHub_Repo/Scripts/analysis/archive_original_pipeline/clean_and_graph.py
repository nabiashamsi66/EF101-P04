import os, io, re, csv, shutil
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

NEW = '/home/claude/new/EF101-P04'
OUT_ROOT = '/home/claude/out2'
OUT = f'{OUT_ROOT}/EF101-P04'
if os.path.exists(OUT_ROOT): shutil.rmtree(OUT_ROOT)
for d in ['Raw_Logs', 'Practice_Runs', 'Cleaned_Data', 'Graphs', 'Screenshots/Extra', 'Report', 'Scripts']:
    os.makedirs(f'{OUT}/{d}', exist_ok=True)
def P(*a): return os.path.join(OUT, *a)
def read_text(path):
    b = open(path, 'rb').read()
    for enc in ('utf-8-sig', 'utf-16'):
        try: return b.decode(enc)
        except UnicodeDecodeError: pass
    raise ValueError(path)
def find_src(name):
    for p in [f'{NEW}/Raw_Logs/{name}', f'{NEW}/Raw_Logs/Practice_Runs/{name}']:
        if os.path.exists(p): return p
    return None

# ---------- 1. Raw files ----------
keep = {'idle_20261015_135254.csv': 'idle', 'cpu_20261018_113237.csv': 'cpu',
        'cooldown_20261018_114614.csv': 'cooldown', 'ram_20261015_142951.csv': 'ram',
        'storage_20261015_145445.csv': 'storage', 'mixed_20261015_144438.csv': 'mixed'}
for f in keep: shutil.copyfile(find_src(f), P('Raw_Logs', f))
shutil.copyfile(f'{NEW}/Raw_Logs/hwinfo_session.csv', P('Raw_Logs', 'hwinfo_session1_15oct.csv'))
shutil.copyfile(f'{NEW}/Raw_Logs/hwinfo_cpu_rerun_csv.CSV', P('Raw_Logs', 'hwinfo_session2_18oct_cpu_rerun.csv'))
move = {
 'idle_20261013_011151.csv': '13 Oct purana idle (30 rows, practice)',
 'idle_20261013_091859.csv': '13 Oct purana idle (150 rows, practice, HWiNFO data nahi)',
 'idle_20261015_133823.csv': 'Dusra idle (150 rows). HWiNFO data nahi (HWiNFO 13:50 ke baad shuru hua). Baseline 135254 hai',
 'pilot_20261013_085550.csv': '13 Oct pilot, format kharab (header nahi)',
 'pilot_20261013_095044.csv': '13 Oct pilot (30 rows, practice)',
 'pilot_20261015_133239.csv': 'Pilot (script test)',
 'pilot_20261015_134904.csv': 'Pilot (script test)',
 'cpu_20261015_135900.csv': 'INVALID CPU run: PowerShell log 13:59-14:10 chala, load 14:11 par shuru hua. Rerun se replace hua',
}
for f, why in move.items(): shutil.copyfile(find_src(f), P('Practice_Runs', f))
# cooldown from the first (late CPU) session: it was accidentally renamed to a file called "Practice_Runs"
shutil.copyfile(f'{NEW}/Practice_Runs', P('Practice_Runs', 'cooldown_20261015_142401.csv'))
move['cooldown_20261015_142401.csv'] = 'Cooldown jo late CPU load ke 4 min baad shuru hua. Naye cooldown (18 Oct) se replace hua'
with open(P('Practice_Runs', 'README_practice_files.txt'), 'w', encoding='utf-8') as fh:
    fh.write('Ye files analysis ke main data mein shamil nahi hain. Delete nahi ki gayi.\n\n')
    for k, v in move.items(): fh.write(f'{k}: {v}\n')
shutil.copyfile(f'{NEW}/Scripts/Log-Test.ps1', P('Scripts', 'Log-Test.ps1'))
with open(P('Report', 'specs_utf8.txt'), 'w', encoding='utf-8') as fh:
    fh.write(read_text(f'{NEW}/Report/specs.txt').replace('\r\n', '\n').strip() + '\n')

# ---------- 2. PowerShell logs ----------
NUM = ['cpu_percent','ram_available_mb','ram_committed_percent','pages_per_sec','pagefile_usage_percent',
       'disk_read_mb_s','disk_write_mb_s','disk_active_percent','disk_queue_length']
def read_log(path):
    df = pd.read_csv(io.StringIO(read_text(path)))
    df['timestamp'] = pd.to_datetime(df['timestamp']); return df
def add_phase(df, test):
    e = df['elapsed_s']
    if test == 'idle': ph = np.full(len(df), 'baseline')
    elif test == 'cooldown': ph = np.full(len(df), 'cooldown')
    elif test == 'cpu': ph = np.where(e < 60, 'pre-load', np.where(e <= 640, 'load', 'post-load'))
    elif test == 'ram': ph = np.where(e <= 270, 'load', 'recovery')
    elif test == 'storage': ph = np.where(e < 60, 'pre-load', np.where(e <= 300, 'load', 'post'))
    elif test == 'mixed': ph = np.full(len(df), 'load')
    df.insert(1, 'phase', ph); return df
clean = {}
for f, test in keep.items():
    df = read_log(P('Raw_Logs', f))
    for c in NUM: df[c] = pd.to_numeric(df[c], errors='coerce')
    df = add_phase(df, test)
    df.to_csv(P('Cleaned_Data', f'{test}_clean.csv'), index=False, encoding='utf-8')
    clean[test] = df

# ---------- 3. HWiNFO two sessions ----------
def col(hdr, exact=None, contains=None):
    if exact and exact in hdr: return hdr.index(exact)
    if contains:
        m = [i for i, h in enumerate(hdr) if contains.lower() in h.lower()]
        if m: return m[0]
    return None
def parse_hw(path, session):
    rows = list(csv.reader(io.StringIO(read_text(path)))); hdr = rows[0]
    data = [r for r in rows[1:] if r and re.match(r'^\d{2}\.\d{2}\.\d{4}$', r[0].strip())]
    C = dict(usage=col(hdr,'Total CPU Usage [%]'), clk=col(hdr,'Core Clocks (avg) [MHz]'),
             pkgC=col(hdr,'CPU Package [°C]'), pkgW=col(hdr,'CPU Package Power [W]'),
             pl1=col(hdr,'PL1 Power Limit (Static) [W]'), gpuU=col(hdr,'GPU GT Usage [%]'),
             gpuC=col(hdr,'GPU Core Temperature [°C]'), gpuMem=col(hdr,'GPU D3D Memory Dynamic [MB]'),
             physUsed=col(hdr,'Physical Memory Used [MB]'), drvT=col(hdr,'Drive Temperature [°C]'),
             drvW=None)
    wr = [i for i, h in enumerate(hdr) if 'write rate' in h.lower()]
    wr = sorted(wr, key=lambda i: 'MB/s' not in hdr[i])
    C['drvW'] = wr[0] if wr else None
    flags = [i for i, h in enumerate(hdr) if any(k in h for k in ['Power Limit Exceeded', 'Critical Temperature', 'Thermal Throttl'])]
    def fv(r, k):
        i = C[k]
        if i is None: return np.nan
        try: return float(r[i])
        except Exception: return np.nan
    recs = []
    for r in data:
        h, mi, se = map(int, re.match(r'(\d+):(\d+):(\d+)', r[1].strip()).groups())
        d, m_, y = r[0].strip().split('.')
        rec = {'session': session, 'timestamp': pd.Timestamp(year=int(y), month=int(m_), day=int(d), hour=h, minute=mi, second=se)}
        for k in ['usage','clk','pkgC','pkgW','pl1','gpuU','gpuC','gpuMem','physUsed','drvT','drvW']:
            rec[k] = fv(r, k)
        rec['flags_yes'] = sum(1 for i in flags if r[i].strip().lower() == 'yes')
        recs.append(rec)
    df = pd.DataFrame(recs).sort_values('timestamp').reset_index(drop=True)
    return df, len(data), len(rows) - 1 - len(data)
h1, n1, s1 = parse_hw(P('Raw_Logs', 'hwinfo_session1_15oct.csv'), 'S1 (15 Oct)')
h2, n2, s2 = parse_hw(P('Raw_Logs', 'hwinfo_session2_18oct_cpu_rerun.csv'), 'S2 (18 Oct)')
HW = pd.concat([h1, h2]).reset_index(drop=True)
HW.to_csv(P('Cleaned_Data', 'hwinfo_clean_both_sessions.csv'), index=False, encoding='utf-8')
def load_window(h):
    # longest unbroken block of CPU usage >= 90 % (the stress block, not random spikes)
    hi = (h.usage >= 90).astype(int).values
    best = (0, 0, 0); start = None
    for i, v in enumerate(list(hi) + [0]):
        if v and start is None: start = i
        if not v and start is not None:
            if i - start > best[0]: best = (i - start, start, i - 1)
            start = None
    _, s, e = best
    return h.timestamp.iloc[s], h.timestamp.iloc[e]
L1 = load_window(h1); L2 = load_window(h2)
print('Session1 load window:', L1); print('Session2 load window:', L2)
print('hwinfo rows: S1', n1, 'non-data lines dropped', s1, '| S2', n2, 'non-data lines dropped', s2)

# ---------- 4. summaries ----------
def st(d):
    return dict(rows=len(d), cpu_avg_pct=d.cpu_percent.mean(), cpu_max_pct=d.cpu_percent.max(),
                ram_avail_min_mb=d.ram_available_mb.min(), ram_avail_avg_mb=d.ram_available_mb.mean(),
                committed_max_pct=d.ram_committed_percent.max(), pages_avg=d.pages_per_sec.mean(),
                pages_max=d.pages_per_sec.max(), pagefile_max_pct=d.pagefile_usage_percent.max(),
                disk_write_avg_mb_s=d.disk_write_mb_s.mean(), disk_write_max_mb_s=d.disk_write_mb_s.max(),
                disk_read_avg_mb_s=d.disk_read_mb_s.mean(), disk_active_avg_pct=d.disk_active_percent.mean(),
                disk_active_max_pct=d.disk_active_percent.max(), disk_queue_max=d.disk_queue_length.max())
use = {'idle': 'baseline', 'cpu': 'load', 'ram': 'load', 'storage': 'load', 'mixed': 'load', 'cooldown': 'cooldown'}
rows = []
for t in ['idle', 'cpu', 'ram', 'storage', 'mixed', 'cooldown']:
    d = clean[t][clean[t].phase == use[t]]
    r = {'test': t, 'window': use[t]}; r.update(st(d)); rows.append(r)
summary = pd.DataFrame(rows).round(2)
summary.to_csv(P('Cleaned_Data', 'summary_by_test_clean.csv'), index=False, encoding='utf-8')

def hw_run_summary(h, L, name):
    s, e = L
    cl = h[(h.timestamp >= s) & (h.timestamp <= e)]
    first = cl[cl.timestamp < s + pd.Timedelta(minutes=3)]
    last = cl[cl.timestamp > e - pd.Timedelta(minutes=3)]
    after = h[(h.timestamp > e) & (h.timestamp <= e + pd.Timedelta(minutes=5))]
    pre = h[(h.timestamp < s) & (h.timestamp >= s - pd.Timedelta(minutes=3))]
    return dict(run=name, load_start=str(s.time()), load_end=str(e.time()), load_rows=len(cl),
                cpu_usage_avg_pct=round(cl.usage.mean(), 1), cpu_usage_min_pct=cl.usage.min(),
                clock_avg_mhz=round(cl.clk.mean(), 0), clock_first3min_mhz=round(first.clk.mean(), 0),
                clock_last3min_mhz=round(last.clk.mean(), 0), clock_min_1min_mean_mhz=round(cl.set_index('timestamp').clk.resample('1min').mean().min(), 0),
                pkg_temp_pre_load_c=round(pre.pkgC.mean(), 1), pkg_temp_max_c=cl.pkgC.max(),
                pkg_temp_5min_after_c=round(after.pkgC.iloc[-1], 1) if len(after) else np.nan,
                pkg_power_avg_w=round(cl.pkgW.mean(), 2), pl1_limit_w=cl.pl1.iloc[0],
                flags_yes_in_load=int(cl.flags_yes.sum()), flags_yes_session=int(h.flags_yes.sum()),
                gpu_usage_max_pct=h.gpuU.max(), gpu_temp_max_c=h.gpuC.max())
hwsum = pd.DataFrame([hw_run_summary(h1, L1, 'Run 1 (15 Oct, 13:52 session)'),
                      hw_run_summary(h2, L2, 'Run 2 (18 Oct, rerun)')])
hwsum.to_csv(P('Cleaned_Data', 'hwinfo_cpu_load_summary.csv'), index=False, encoding='utf-8')

# ---------- 5. QC ----------
exp = {'idle': 150, 'cpu': 330, 'cooldown': 150, 'ram': 150, 'storage': 150, 'mixed': 150}
qc = []
for f, test in keep.items():
    d = read_log(P('Raw_Logs', f))
    dt = d.timestamp.diff().dt.total_seconds().dropna()
    qc.append(dict(file=f, test=test, rows=len(d), expected_rows=exp[test], blank_cells=int(d.isna().sum().sum()),
                   elapsed_last_s=int(d.elapsed_s.max()), gap_s_min=dt.min(), gap_s_max=dt.max(),
                   timestamps_increasing=bool(d.timestamp.is_monotonic_increasing),
                   cpu_out_of_0_100=int(((d.cpu_percent < 0) | (d.cpu_percent > 100)).sum()),
                   disk_active_over_100=int((d.disk_active_percent > 100).sum()),
                   negative_values=int((d[NUM] < 0).sum().sum())))
for f, lab in [('hwinfo_session1_15oct.csv', 'S1'), ('hwinfo_session2_18oct_cpu_rerun.csv', 'S2')]:
    h = HW[HW.session.str.startswith(lab)]
    qc.append(dict(file=f, test='hwinfo', rows=len(h), expected_rows='', blank_cells=int(h[['usage','clk','pkgC','pkgW']].isna().sum().sum()),
                   elapsed_last_s='', gap_s_min='', gap_s_max='', timestamps_increasing=bool(h.timestamp.is_monotonic_increasing),
                   cpu_out_of_0_100=int(((h.usage < 0) | (h.usage > 100)).sum()), disk_active_over_100='', negative_values=''))
qcdf = pd.DataFrame(qc); qcdf.to_csv(P('Cleaned_Data', 'qc_report.csv'), index=False, encoding='utf-8')

# ---------- 6. Graphs ----------
G = P('Graphs')
def save(fig, name): fig.tight_layout(); fig.savefig(f'{G}/{name}', dpi=120); plt.close(fig)

# 01 CPU utilization (PowerShell) all tests
fig, ax = plt.subplots(figsize=(10, 5))
for t, c in [('idle','gray'),('cpu','tab:orange'),('ram','tab:blue'),('storage','tab:green'),('mixed','tab:red'),('cooldown','tab:purple')]:
    d = clean[t]; ax.plot(d.elapsed_s/60, d.cpu_percent, color=c, lw=1.1, label=t)
ax.axvspan(60/60, 640/60, color='orange', alpha=.08)
ax.set_xlabel('Time since test start (minutes)'); ax.set_ylabel('CPU utilization (%)')
ax.set_title('CPU utilization (PowerShell counter): idle vs each stress test (shaded = CPU load)')
ax.legend(loc='center right', fontsize=8); ax.grid(alpha=.3)
save(fig, '01_cpu_utilization_all_tests.png')

# 02 HWiNFO CPU load, two runs, aligned at load start
fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)
specs = [('usage','CPU usage (%)'),('clk','Core clock avg (MHz)'),('pkgC','CPU package temp (°C)'),('pkgW','CPU package power (W)')]
for (h, L, lab, c) in [(h1, L1, 'Run 1 (15 Oct)', 'tab:blue'), (h2, L2, 'Run 2 (18 Oct, rerun)', 'tab:red')]:
    x = (h.timestamp - L[0]).dt.total_seconds()/60
    m = (x >= -2) & (x <= 13)
    for ax, (k, _) in zip(axs, specs): ax.plot(x[m], h.loc[m, k], color=c, lw=1, label=lab)
for ax, (k, lab) in zip(axs, specs):
    ax.set_ylabel(lab); ax.grid(alpha=.3)
    ax.axvspan(0, (L1[1]-L1[0]).total_seconds()/60, color='orange', alpha=.07)
axs[3].axhline(18, color='k', ls='--', lw=1); axs[3].text(0.2, 18.4, 'PL1 limit 18 W', fontsize=8)
axs[0].legend(loc='lower right', fontsize=8)
axs[-1].set_xlabel('Minutes since CPU load started')
fig.suptitle('HWiNFO: CPU load, two independent runs (shaded = load on Run 1)')
save(fig, '02_hwinfo_cpu_load_two_runs.png')

# 03 Cooldown / recovery after load
fig, axs = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
for (h, L, lab, c) in [(h1, L1, 'Run 1 (15 Oct)', 'tab:blue'), (h2, L2, 'Run 2 (18 Oct)', 'tab:red')]:
    x = (h.timestamp - L[1]).dt.total_seconds()/60
    m = (x >= -1) & (x <= 12)
    axs[0].plot(x[m], h.loc[m,'pkgC'], color=c, label=lab); axs[1].plot(x[m], h.loc[m,'clk'], color=c, label=lab)
axs[0].set_ylabel('CPU package temp (°C)'); axs[1].set_ylabel('Core clock avg (MHz)')
axs[1].set_xlabel('Minutes after CPU load ended (0 = load end)')
for a in axs: a.grid(alpha=.3); a.axvline(0, color='k', lw=.8, ls=':')
axs[0].legend(); fig.suptitle('Cooldown after CPU load: temperature and clock recovery')
save(fig, '03_cooldown_recovery_hwinfo.png')

# 04-05 RAM
d = clean['ram']; x = d.elapsed_s/60
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, d.ram_available_mb, color='tab:blue', label='Available RAM (MB)'); ax.set_ylabel('Available RAM (MB)')
ax.set_xlabel('Time since test start (minutes)')
ax2 = ax.twinx(); ax2.plot(x, d.ram_committed_percent, color='tab:orange', label='Committed memory in use (%)')
ax2.set_ylabel('Committed memory in use (%)'); ax.axvspan(0, 270/60, color='orange', alpha=.12)
ax.set_title('RAM test: available RAM falls, committed memory rises (shaded = RAM load)')
h_1, l_1 = ax.get_legend_handles_labels(); h_2, l_2 = ax2.get_legend_handles_labels()
ax.legend(h_1+h_2, l_1+l_2, loc='lower left'); ax.grid(alpha=.3)
save(fig, '04_ram_available_and_committed.png')
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, d.pagefile_usage_percent, color='tab:purple', label='Pagefile usage (%)'); ax.set_ylabel('Pagefile usage (%)')
ax.set_xlabel('Time since test start (minutes)')
ax2 = ax.twinx(); ax2.plot(x, d.pages_per_sec, color='tab:gray', lw=.8, label='Pages/sec'); ax2.set_ylabel('Pages/sec')
ax.axvspan(0, 270/60, color='orange', alpha=.12); ax.set_title('RAM test: virtual memory (pagefile) and paging activity')
h_1, l_1 = ax.get_legend_handles_labels(); h_2, l_2 = ax2.get_legend_handles_labels()
ax.legend(h_1+h_2, l_1+l_2, loc='upper left'); ax.grid(alpha=.3)
save(fig, '05_ram_pagefile_and_paging.png')

# 06 storage
d = clean['storage']; x = d.elapsed_s/60
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, d.disk_write_mb_s, color='tab:red', label='Write (MB/s)'); ax.plot(x, d.disk_read_mb_s, color='tab:blue', label='Read (MB/s)')
ax.set_ylabel('Disk throughput (MB/s)'); ax.set_xlabel('Time since test start (minutes)')
ax2 = ax.twinx(); ax2.plot(x, d.disk_active_percent, color='tab:green', alpha=.7, label='Disk active (%)'); ax2.set_ylabel('Disk active (%)')
ax.axvspan(1, 5, color='orange', alpha=.12)
ax.set_title('Storage test: throughput and disk activity (shaded = load). Read near 0 = Windows cache')
h_1, l_1 = ax.get_legend_handles_labels(); h_2, l_2 = ax2.get_legend_handles_labels()
ax.legend(h_1+h_2, l_1+l_2, loc='center right'); ax.grid(alpha=.3)
save(fig, '06_storage_throughput_and_activity.png')

# 07 mixed
d = clean['mixed']; x = d.elapsed_s/60
fig, axs = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
axs[0].plot(x, d.cpu_percent, color='tab:blue'); axs[0].set_ylabel('CPU (%)')
axs[1].plot(x, d.ram_available_mb, color='tab:orange'); axs[1].set_ylabel('Available RAM (MB)')
axs[2].plot(x, d.disk_write_mb_s, color='tab:red'); axs[2].set_ylabel('Disk write (MB/s)'); axs[2].set_xlabel('Time since test start (minutes)')
for a in axs: a.grid(alpha=.3)
fig.suptitle('Mixed workload (browser + video + zip): CPU, RAM and disk together')
save(fig, '07_mixed_cpu_ram_disk.png')

# 08 comparison
t_list = ['idle','cpu','ram','storage','mixed']
sv = summary.set_index('test').loc[t_list]
fig, axs = plt.subplots(2, 2, figsize=(10, 7))
panels = [('cpu_avg_pct','Average CPU (%)'),('ram_avail_min_mb','Lowest available RAM (MB)'),
          ('disk_write_avg_mb_s','Average disk write (MB/s)'),('disk_active_avg_pct','Average disk active (%)')]
cols = ['gray','tab:orange','tab:blue','tab:green','tab:red']
for a, (c, lab) in zip(axs.flat, panels):
    a.bar(t_list, sv[c], color=cols); a.set_title(lab); a.grid(axis='y', alpha=.3)
    for i, v in enumerate(sv[c]): a.text(i, v, f'{v:.1f}', ha='center', va='bottom', fontsize=8)
fig.suptitle('Idle vs each stress test (each averaged over its own load window)')
save(fig, '08_comparison_idle_vs_tests.png')

# 09 GPU (session 1 full)
g = h1
fig, axs = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
axs[0].plot(g.timestamp, g.gpuU, color='tab:green', lw=.8); axs[0].set_ylabel('GPU GT usage (%)')
axs[1].plot(g.timestamp, g.gpuC, color='tab:red', lw=.8); axs[1].set_ylabel('GPU temp (°C)')
axs[2].plot(g.timestamp, g.gpuMem, color='tab:purple', lw=.8); axs[2].set_ylabel('GPU memory (MB)')
axs[2].set_xlabel('Time, 15 Oct 2026 (HH:MM)')
for a in axs: a.grid(alpha=.3)
fig.suptitle('Integrated GPU (Intel UHD 620) during the session: usage, temperature, memory')
save(fig, '09_gpu_usage_temp_memory.png')

# ---------- 7. Screenshots ----------
S = f'{NEW}/Screenshots'
ren = {'specs.png': '01_specs.png', 'pilot_excel.png': '02_pilot_excel.png',
       'cpu_hwinfo_rerun.png': '03_hwinfo_cpu_load_rerun_CPU_rows.png',
       'cooldown_hwinfo.png': '04_hwinfo_cooldown_rerun.png',
       'ram_taskmanager.png': '05_ram_taskmanager.png', 'mixed_taskmanager.png': '06_mixed_taskmanager.png',
       'storage_taskmanager.png': '07_storage_taskmanager.png'}
extra = {'cpu_hwinfo.png': 'hwinfo_session1_during_load_GPU_drive_view.png',
         'hwinfo_sensors_png.png': 'hwinfo_sensors_13oct_practice.png',
         'pilot_excel_png.png': 'pilot_excel_duplicate1.png', 'pilot_excel_png2.png': 'pilot_excel_duplicate2.png'}
for a, b in ren.items(): shutil.copyfile(f'{S}/{a}', P('Screenshots', b))
for a, b in extra.items(): shutil.copyfile(f'{S}/{a}', P('Screenshots', 'Extra', b))

# ---------- 8. Save QC md ----------
def md_table(df):
    cols = list(df.columns)
    out = '| ' + ' | '.join(cols) + ' |\n|' + '---|' * len(cols) + '\n'
    for _, r in df.iterrows():
        out += '| ' + ' | '.join('' if (isinstance(v, float) and np.isnan(v)) else str(v) for v in r.values) + ' |\n'
    return out
with open(P('Report', 'Data_Quality_Report.md'), 'w', encoding='utf-8') as fh:
    fh.write('# Data Quality Report (EF101-P04)\n\n')
    fh.write('Raw files Raw_Logs mein bilkul waisi hain jaisi logger ne banayi. Cleaning sirf Cleaned_Data mein hai.\n\n')
    fh.write(md_table(qcdf.astype(str)) + '\n')
    fh.write('## Notes\n\n')
    fh.write('- CPU load ka PowerShell run (18 Oct) 330 rows, koi khali cell nahi. Sampling interval 2 se 4 second ke beech hai (1 se 5 second ki requirement mein hai).\n')
    fh.write('- Load PowerShell log start hone ke lagbhag 1 minute baad shuru hua. Pehla minute pre-load baseline ki tarah use hua hai.\n')
    fh.write('- disk_active_percent kuch jagah 100 se zyada hai (Windows counter ka aisa karna mumkin hai). Data nahi badla gaya.\n')
    fh.write('- Storage read values near 0 hain kyun ke file Windows cache se padhi gayi. Limitation hai.\n')
    fh.write('- HWiNFO files mein dobara header lines thi, cleaned files mein hata di gayi hain.\n')

shutil.make_archive(f'{OUT_ROOT}/EF101-P04_Organized_v2', 'zip', OUT_ROOT, 'EF101-P04')

# ---------- 9. print key numbers ----------
pd.set_option('display.width', 250)
print('\nSUMMARY (PowerShell):'); print(summary[['test','window','rows','cpu_avg_pct','cpu_max_pct','ram_avail_min_mb','committed_max_pct','pagefile_max_pct','pages_avg','disk_write_avg_mb_s','disk_active_avg_pct','disk_queue_max']].to_string(index=False))
print('\nHWiNFO CPU runs:'); print(hwsum.T.to_string())
print('\nQC:'); print(qcdf[['file','rows','expected_rows','blank_cells','gap_s_min','gap_s_max','cpu_out_of_0_100','disk_active_over_100']].to_string(index=False))
print('\nGPU session1: usage max', h1.gpuU.max(), 'temp max', h1.gpuC.max(), 'mem min/max', h1.gpuMem.min(), h1.gpuMem.max(), 'usage mean', round(h1.gpuU.mean(),1))
print('Graphs:', sorted(os.listdir(G)))
