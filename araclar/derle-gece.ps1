param([switch]$Kuru)

# Gorev eylemi icin pencere acmadan calistirilacak giris noktasi.
# -Kuru: model, commit, push ve rapor dosyasi yazimi yok; sadece test logu.
$ErrorActionPreference = 'Stop'
$derlemeRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $derlemeRoot
$derlemePython = (Get-Command python.exe -ErrorAction Stop).Source
$derlemeLog = if ($Kuru) {
    Join-Path $derlemeRoot 'derleme/astra-kontrol/gorev-kuru.log'
} else {
    Join-Path $derlemeRoot 'derleme/derleyici.log'
}
$derlemeArgs = @('-u', (Join-Path $PSScriptRoot 'derle.py'))
if ($Kuru) { $derlemeArgs += '--kuru' }
# Yonlendirilmis stdout tamponlanmasin: kesinti oncesi satirlar logda kalsin.
$ErrorActionPreference = 'Continue'
& $derlemePython @derlemeArgs 2>&1 | Out-File -LiteralPath $derlemeLog -Append -Encoding utf8
$derlemeExit = $LASTEXITCODE
exit $derlemeExit
