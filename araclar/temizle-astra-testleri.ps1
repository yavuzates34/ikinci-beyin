param([switch]$Uygula)

# Kullanici 20.09 06:12'de manifestodaki 178 test klasorunu onayladi.
# Varsayilan sadece denetler. Otomatik arac silmeyi engelledigi icin elle
# calistirilmak uzere hazirlandi; raporlar, loglar ve diger klasorler kapsam disi.
$ErrorActionPreference = 'Stop'
$cleanupRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../derleme/astra-kontrol')).Path
$manifestPath = Join-Path $cleanupRoot 'temizlik-manifestosu.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($manifest.allowed_root -ne $cleanupRoot -or $manifest.directories.Count -ne 178) {
    throw 'Manifesto koku veya hedef sayisi beklenenle uyusmuyor.'
}
$verified = @()
foreach ($entry in $manifest.directories) {
    if (-not (Test-Path -LiteralPath $entry.path)) { continue }
    $target = (Resolve-Path -LiteralPath $entry.path).Path
    if ((Split-Path -Parent $target) -ne $cleanupRoot -or (Split-Path -Leaf $target) -notlike 'test-*') {
        throw 'Proje test dizini disinda hedef reddedildi.'
    }
    $items = @((Get-Item -LiteralPath $target)) + @(Get-ChildItem -LiteralPath $target -Recurse -Force)
    if (@($items | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
        throw 'Baglanti veya junction iceren hedef reddedildi.'
    }
    $files = @($items | Where-Object { -not $_.PSIsContainer })
    if ($files.Count -ne $entry.files.Count) { throw 'Dosya sayisi degismis.' }
    foreach ($file in $entry.files) {
        $resolved = (Resolve-Path -LiteralPath (Join-Path $target $file.path)).Path
        if (-not $resolved.StartsWith($target + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
            throw 'Test klasoru disina cikan dosya reddedildi.'
        }
        $info = Get-Item -LiteralPath $resolved
        if ($info.Length -ne $file.bytes -or (Get-FileHash -LiteralPath $resolved -Algorithm SHA256).Hash.ToLowerInvariant() -ne $file.sha256) {
            throw 'Dosya icerigi manifestodan sonra degismis.'
        }
    }
    $verified += $target
}
Write-Output ('Dogrulanan hedef: ' + $verified.Count + '; uygulama: ' + [bool]$Uygula)
if (-not $Uygula) { return }
foreach ($target in $verified) { Remove-Item -LiteralPath $target -Recurse -Force }
[pscustomobject]@{
    DeletedDirectories = $verified.Count
    RemainingTestDirectories = @(Get-ChildItem -LiteralPath $cleanupRoot -Directory -Filter 'test-*').Count
    RemainingFakeBeyin = @(Get-ChildItem -LiteralPath $cleanupRoot -Recurse -File -Filter 'BEYIN.md').Count
} | ConvertTo-Json
