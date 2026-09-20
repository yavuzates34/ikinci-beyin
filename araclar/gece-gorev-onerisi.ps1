param([switch]$Uygula)

# Varsayilan yalniz oneri; -Uygula sadece kullanicinin acik onayindan sonra.
$ErrorActionPreference = 'Stop'
$gorevRoot = Split-Path -Parent $PSScriptRoot
$gorevTask = Get-ScheduledTask -TaskName 'playground-derleyici'
$gorevRunner = Join-Path $PSScriptRoot 'derle-gece.ps1'
$gorevShell = Join-Path $env:SystemRoot 'System32/WindowsPowerShell/v1.0/powershell.exe'
$gorevArguments = '-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "' + $gorevRunner + '"'
[pscustomobject]@{
    TaskName = $gorevTask.TaskName
    EskiEylem = $gorevTask.Actions.Execute
    YeniEylem = $gorevShell
    YeniArgumanlar = $gorevArguments
    YeniCalismaDizini = $gorevRoot
    EskiSureSiniri = $gorevTask.Settings.ExecutionTimeLimit
    YeniSureSiniri = 'PT1H'
    LogonType = [string]$gorevTask.Principal.LogonType
    Uygulama = [bool]$Uygula
} | ConvertTo-Json
if (-not $Uygula) { return }

$gorevBackup = Join-Path $gorevRoot ('derleme/astra-kontrol/gorev-oncesi-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.xml')
Export-ScheduledTask -TaskName $gorevTask.TaskName | Out-File -LiteralPath $gorevBackup -Encoding utf8
$gorevAction = New-ScheduledTaskAction -Execute $gorevShell -Argument $gorevArguments -WorkingDirectory $gorevRoot
$gorevSettings = $gorevTask.Settings
$gorevSettings.ExecutionTimeLimit = 'PT1H'
Set-ScheduledTask -TaskName $gorevTask.TaskName -Action $gorevAction -Settings $gorevSettings | Out-Null
# Tetik, kullanici, giris tipi ve diger ayarlar korunur. Gorev tetiklenmez.
