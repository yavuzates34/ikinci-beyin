# Yaşanan hatalar

Bir kez düşülmüş tuzaklar. Tekrar keşfedilmesin diye yazıldı.

> Merkez: [[BEYIN]] · İlgili: [[arac-izle]] · [[arac-arsiv]] · [[tasarim-dersleri]]

---

1. **`ffmpeg -vsync` kaldırıldı.** ffmpeg 9.0'da seçenek yok, `-fps_mode` oldu.
2. **Sahne algılama ekran kaydında çalışmaz.** (bkz. 1. bölüm)
3. **`yt-dlp --force-keyframes-at-cuts` → 403 Forbidden.** Kullanılmamalı. Kırpma
   bu bayrak olmadan sorunsuz çalışıyor.
4. **CUDA için `cublas64_12.dll` gerekiyor.** `nvidia-cublas-cu12` +
   `nvidia-cudnn-cu12` kurulmalı, DLL klasörleri `os.add_dll_directory()` ile
   kaydedilmeli.
5. **jsonl'i Python'da açarken Windows yolu kullanılmalı** (`C:\...`), MSYS yolu
   (`/c/...`) çözülemiyor. `encoding="utf-8"` şart.
6. **Bash heredoc ters bölüleri yiyor.** `<<'PY'` ile yazılan Python script'lerinde
   regex kaçışları bozuluyor (`\u` → hata). Script'i Write aracıyla dosyaya yazıp
   çalıştırmak gerekiyor. Bu tuzağa iki kez düşüldü.
7. **Boru hattı çıkış kodunu maskeler.** `komut | grep | tail` yapısında çıkış kodu
   son komuta (`tail`) aittir. Bir arka plan işi "exit 0" raporladı ama hiçbir şey
   üretmemişti. Çözüm: `set -o pipefail` ya da çıktıyı dosyaya yazıp sonucu ayrıca
   sınamak.
8. **`claude config list` diye bir alt komut yok.** Çalıştırıldığında gerçek bir
   Claude oturumu başlatıp sohbet cevabı üretti, boşuna token harcadı. Ayarlara
   bakmak için `~/.claude/settings.json` doğrudan okunmalı.
9. **Klasör taşınınca hafıza öksüz kalır.** 7 Eylül'de klasör
   `Desktop\playground` → `Desktop\desktop\playground` taşındı; hafıza dosyaları
   eski proje yolunda kaldı ve yüklenmedi. Elle taşındı. Oturumlar ve hafıza,
   **klasör yoluna göre** gruplanıyor.

---

10. **PowerShell komutuna uzun metin gömmek kırılgan.** `SessionStart` hook'unun
    mesajı JSON içindeki PowerShell komutuna gömülüydü; metin uzayınca tırnak
    kaçışları çözülemez hale geldi (`Unexpected token` hatası). Çözüm: metin
    ayrı bir dosyaya (`.claude/oturum-basi.md`) alındı, hook `Get-Content -Raw`
    ile okuyup yer tutucuları dolduruyor. Kural: **durağan metin kabuk komutunun
    içine gömülmez.** Aynı ders daha önce heredoc'ta öğrenilmişti (madde 6).

11. **Hook çıktısındaki ASCII dışı karakter konsol kodlamasında bozuluyor.**
    Mesaj dosyasındaki tek bir `·` karakteri, PowerShell'in çıktısını geçersiz
    UTF-8 yapıp JSON çözümlemesini kırdı. Hook metinleri **saf ASCII** tutulmalı;
    Türkçe karakterler de dahil. (Python araçlarında çözüm farklı: orada
    `sys.stdout.reconfigure(encoding="utf-8")` kullanılıyor, bkz. madde 12.)

12. **Windows konsolu Türkçeyi bozuyor.** Python araçları çıktıyı cp1254 ile
    basıyor; çıktı boruya ya da dosyaya yönlendirilse bile bozuluyor. Çözüm:
    `sys.stdout.reconfigure(encoding="utf-8")`. Bu projede Türkçe basan her
    script'e gerekli — `araclar/kayit.py` içindeki `utf8_zorla()` bunu yapıyor.

13. **Obsidian vault'u açıkken dosyaları sessizce değiştirebiliyor.** 16 Eylül'de
    `BEYIN.md` içinde backtick içindeki `CLAUDE.md` ifadesi `[[[[CLAUDE]]]].md`
    hâlinde bulundu — iç içe dört köşeli parantez. Tablolar da yeniden
    hizalanmıştı. Mekanizma kesin değil (otomatik bağ güncelleme ya da düzenleyici
    davranışı), ama sonuç ölçüldü. **Ders:** vault açıkken yazılan dosyalar
    değişebilir; kritik metni yazdıktan sonra doğrula. Bunu yakalayan şey git
    oldu — `git status` dosyayı "değişmiş" gösterdi. Sürüm kontrolü olmasa fark
    edilmezdi.

14. **Not, kendi anlattığı sistemden geri kalabiliyor.** `kapanis-ritueli.md`
    `PreCompact` hook'unu "`matcher: auto` ile bağlı" diye anlatıyordu; matcher
    aynı oturumda kaldırılmıştı. Yani not, iki saat içinde yalan söyler hâle
    geldi. **Ders:** bir notta yapılandırma iddiası varsa, yapılandırma
    değiştiğinde not da değişmeli — ya da iddia nottan çıkarılıp komutla
    ölçülmeli. ([[tasarim-dersleri]] içindeki "komut mu doküman mı" kuralının
    tam olarak uyardığı durum.)
