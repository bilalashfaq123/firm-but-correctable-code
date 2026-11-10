param(
    [string]$Model,
    [string]$Tag,
    [int]$Workers = 4,
    [string]$JudgeModel = 'llama3.1:8b',
    [int]$ExpectedLines = 2160,   # 120 cases x 3 setups x 3 runs x 2 conditions
    [string]$Conditions = 'challenge,suggest',
    [string]$Setups = '',          # empty = sycorun default (plain,antisyc,pipeline)
    [int]$StopTemp = 70,
    [int]$ResumeTemp = 55
)
# Runs sycorun.py with a GPU heat guard and auto-resume. Keeps running after the terminal is closed.
$ErrorActionPreference = 'Continue'
$impl = Split-Path $PSScriptRoot -Parent
Set-Location $impl
$log = Join-Path $impl "results\$Tag.runner.log"
$jsonl = Join-Path $impl "results\$Tag.jsonl"
$gpuLog = Join-Path $impl "results\$Tag.gpu.csv"
function Log($m) { "$(Get-Date -Format s)  $m" | Out-File -Append -Encoding utf8 $log }
function Temp { [int](nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits) }
function Lines { if (Test-Path $jsonl) { (Get-Content $jsonl | Where-Object { $_.Trim() }).Count } else { 0 } }

Log "START model=$Model tag=$Tag workers=$Workers"
for ($attempt = 1; $attempt -le 8; $attempt++) {
    # drop a half-written last line if a previous attempt was killed mid-write
    if (Test-Path $jsonl) {
        python -I (Join-Path $impl 'runner\clean_jsonl.py') $jsonl | ForEach-Object { Log $_ }
    }
    $done = Lines
    if ($done -ge $ExpectedLines) { break }
    Log "attempt $attempt  lines=$done/$ExpectedLines  workers=$Workers  temp=$(Temp)C"
    $argList = @('sycorun.py', '--backend', 'openai', '--base-url', 'http://localhost:11434/v1', '--model', $Model,
        '--judge-backend', 'openai', '--judge-base-url', 'http://localhost:11434/v1', '--judge-model', $JudgeModel,
        '--runs', '3', '--workers', "$Workers", '--temperature', '0.7', '--conditions', $Conditions, '--out', $Tag)
    if ($Setups) { $argList += @('--setups', $Setups) }
    $p = Start-Process python -ArgumentList $argList -NoNewWindow -PassThru `
        -RedirectStandardOutput (Join-Path $impl "results\$Tag.attempt$attempt.out") `
        -RedirectStandardError (Join-Path $impl "results\$Tag.attempt$attempt.err")
    $hot = $false
    while (-not $p.HasExited) {
        Start-Sleep 5
        $t = Temp
        "$(Get-Date -Format s),$t,$(nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader)" | Out-File -Append -Encoding utf8 $gpuLog
        if ($t -ge $StopTemp) {
            Log "HEAT STOP at ${t}C - killing run"
            Stop-Process -Id $p.Id -Force
            $hot = $true
            break
        }
    }
    if ($hot) {
        do { Start-Sleep 15; $t = Temp } while ($t -ge $ResumeTemp)
        Log "cooled to ${t}C - resuming with 2 workers"
        $Workers = 2
        continue
    }
    Log "attempt $attempt exited code $($p.ExitCode)  lines=$(Lines)/$ExpectedLines"
}
$final = Lines
Log "RUN END lines=$final/$ExpectedLines"
if ($final -ge $ExpectedLines) {
    python analyze.py "results\$Tag.jsonl" *> (Join-Path $impl "results\$Tag.analyze.out")
    Log "analyze exit $LASTEXITCODE"
    python -I (Join-Path $impl 'runner\make_handcheck.py') $impl $Tag 2>&1 | ForEach-Object { Log "$_" }
    Log "DONE"
} else {
    Log "INCOMPLETE - not analysed"
}
