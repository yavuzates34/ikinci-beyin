# Ortam: kurulanlar ve kalıcı yapılandırma

Bu makinede neyin nereye kurulduğu ve hangi ayarların kalıcı olduğu.

> Merkez: [[BEYIN]] · İlgili: [[arac-izle]] · [[arac-arsiv]] · [[yasanan-hatalar]]

---

| Bileşen | Sürüm / konum | Not |
|---|---|---|
| ffmpeg / ffprobe | 9.0.1, winget (Gyan.FFmpeg) | PATH'e eklendi ama yeni kabuk gerektirir |
| yt-dlp | 2026.08.19 | Eski sürüm 403 veriyordu, güncellendi |
| faster-whisper | 1.2.1 | |
| Whisper `large-v3` | 2.9 GB → `D:\AI\whisper` | C: dar olduğu için D'ye |
| cuBLAS / cuDNN | 2.0 GB → `D:\AI\pylibs` | `pip install --target` ile D'ye zorlandı |
| rclip | 3.3.0 | Görsel arama, ayrı araç |

**Donanım:** RTX 3060 Ti (8 GB), 16 çekirdek. C: ~12 GB boş (**dar**), D: ~167 GB.
**Kural:** büyük dosyalar ve modeller D'ye kurulur.

### Kalıcı yapılandırma değişiklikleri

**1. UserPromptSubmit hook** → `~/.claude/settings.json`

Her kullanıcı mesajında güncel tarih/saati bağlama enjekte eder. Kurulduğu anda,
zaten 5 gündür açık olan bu oturumda çalışmaya başladı — ayar izleyicisi
değişikliği canlı yakalıyor, yeniden başlatma gerekmiyor.

**2. PowerShell profili** → `Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`

`claude` komutunu `--remote-control` ile sarmalayan bir fonksiyon. Böylece her yeni
oturum telefondaki Dispatch listesinde görünür; `/remote-control` yazmaya gerek yok.
Remote Control'süz başlatmak için doğrudan `claude.exe` çağrılır.

---
