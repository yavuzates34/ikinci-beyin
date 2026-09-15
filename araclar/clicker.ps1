# Dunyanin en basit clicker'i:
# Belirlenen saatte bir kez sol tiklar, sonra kapanir.

$hedef = Get-Date -Year 2026 -Month 9 -Day 6 -Hour 5 -Minute 47 -Second 0 -Millisecond 0

Add-Type @'
using System;
using System.Runtime.InteropServices;
public class Fare {
    [DllImport("user32.dll")]
    static extern void mouse_event(uint dwFlags, int dx, int dy, uint cButtons, IntPtr dwExtraInfo);
    public static void SolTik() {
        mouse_event(0x0002, 0, 0, 0, IntPtr.Zero); // LEFTDOWN
        mouse_event(0x0004, 0, 0, 0, IntPtr.Zero); // LEFTUP
    }
}
'@

if ((Get-Date) -ge $hedef) {
    Write-Host "Hedef saat gecmis: $hedef"
    exit 1
}

Write-Host "Bekleniyor -> $hedef  (imleci tiklanmasini istedigin yere birak)"

while ($true) {
    $kalan = ($hedef - (Get-Date)).TotalSeconds
    if ($kalan -le 0) { break }
    if ($kalan -gt 2) { Start-Sleep -Seconds ([Math]::Min(30, $kalan - 1)) }
    else { Start-Sleep -Milliseconds 20 }
}

[Fare]::SolTik()
Write-Host "Tiklandi: $(Get-Date -Format 'HH:mm:ss.fff')"
