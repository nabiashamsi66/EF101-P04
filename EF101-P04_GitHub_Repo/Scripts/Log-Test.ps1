function Get-V($s,$n){ ($s | Where-Object { $_.Path -like "*$n" }).CookedValue }

function Log-Test {
 param([string]$Test='idle',[int]$Minutes=5)
 $dir  = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'EF101-P04\Raw_Logs'
 New-Item -ItemType Directory -Force $dir | Out-Null
 $file = Join-Path $dir ("{0}_{1}.csv" -f $Test,(Get-Date -Format 'yyyyMMdd_HHmmss'))
 $c = '\Processor(_Total)\% Processor Time',
      '\Memory\Available MBytes',
      '\Memory\% Committed Bytes In Use',
      '\Memory\Pages/sec',
      '\Paging File(_Total)\% Usage',
      '\PhysicalDisk(_Total)\Disk Read Bytes/sec',
      '\PhysicalDisk(_Total)\Disk Write Bytes/sec',
      '\PhysicalDisk(_Total)\% Disk Time',
      '\PhysicalDisk(_Total)\Avg. Disk Queue Length'
 $t0 = Get-Date
 Write-Host "Logging $Test for $Minutes min -> $file (Ctrl+C to stop)"
 try {
  Get-Counter -Counter $c -SampleInterval 2 -MaxSamples ($Minutes*30) | ForEach-Object {
   $s = $_.CounterSamples
   [pscustomobject]@{
    test                   = $Test
    timestamp              = $_.Timestamp.ToString('yyyy-MM-dd HH:mm:ss')
    elapsed_s              = [int]($_.Timestamp - $t0).TotalSeconds
    cpu_percent            = [math]::Round((Get-V $s 'processor time'),1)
    ram_available_mb       = [math]::Round((Get-V $s 'available mbytes'),0)
    ram_committed_percent  = [math]::Round((Get-V $s 'committed bytes in use'),1)
    pages_per_sec          = [math]::Round((Get-V $s 'pages/sec'),1)
    pagefile_usage_percent = [math]::Round((Get-V $s '% usage'),1)
    disk_read_mb_s         = [math]::Round((Get-V $s 'disk read bytes/sec')/1MB,2)
    disk_write_mb_s        = [math]::Round((Get-V $s 'disk write bytes/sec')/1MB,2)
    disk_active_percent    = [math]::Round((Get-V $s '% disk time'),1)
    disk_queue_length      = [math]::Round((Get-V $s 'avg. disk queue length'),2)
   } | Export-Csv -Path $file -Append -NoTypeInformation
  }
  Write-Host "Done: $file"
 } catch { Write-Host "ERROR: $_" }
}