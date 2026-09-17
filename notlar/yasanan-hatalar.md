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

15. **Hook, desteklemediği bir alana yazdı: `PreCompact` modele konuşamıyor.**
    16 Eylül 03:13'te `/compact` ile yapılan **gerçek sıkıştırma testinde**
    ölçüldü. `precompact.py`, `hookSpecificOutput.additionalContext` basıyordu;
    Claude Code çıktıyı *Hook JSON output validation failed* diyerek reddetti ve
    geçerli olay listesini bastı: `PreToolUse`, `UserPromptSubmit`,
    `UserPromptExpansion`, `SessionStart`, `Setup`, `PreModelSwitch`,
    `PostToolUse`, `PostToolBatch`, `Stop`/`SubagentStop`, `PermissionRequest`.
    **`PreCompact` listede yok.** O olayda sadece üst düzey alanlar geçerli:
    `systemMessage`, `decision`, `reason`, `continue`, `stopReason`,
    `suppressOutput`, `terminalSequence`.

    **Ders bir:** belgeye dayanan "muhtemelen destekliyordur" varsayımı, sınanana
    kadar iddiadır. Bu varsayım nota bile "muhtemelen" diye yazılmıştı; yine de
    kod ona güvendi.
    **Ders iki:** iki ayaklı tasarım tam da bunun için vardı ve işe yaradı —
    enjeksiyon düştü, omurga dosyası (44.974 bayt, 69 mesaj) yazıldı ve
    sıkıştırmadan sağ çıktı. Tek ayaklı olsaydı oturum sessizce kaybolurdu.
    **Çözüm:** [[kapanis-ritueli]] içindeki devir kutusu — `araclar/devir.py`.

    **Kapanış (16 Eylül 03:32).** İkinci `/compact` ile zincir uçtan uca
    doğrulandı: şema hatası yok, omurga yazıldı (73 mesaj, 47.947 bayt), mesaj
    modele ulaştı, kutu silindi. Küçük bir sürpriz: teslimatı asıl yol sandığım
    `UserPromptSubmit` değil, yedek saydığım `SessionStart` yaptı — sıkıştırma
    kendisi `SessionStart`'ı tetikliyor. **Üçüncü ders:** düzeltmenin hangi
    ayağının tutacağını da bilmiyordum; bilmediğimi kabul edip ikisini birden
    kurmak doğru tahmini aramaktan ucuzdu.

16. **Python'un `write_text`'i Windows'ta satır sonunu değiştiriyor.** 16 Eylül
    03:37'de beş nota küçük yamalar atıldı; `git diff --stat` beşini de baştan
    sona değişmiş gösterdi — `BEYIN.md`'de tek satır değiştirdiğim hâlde 154
    satır. Sebep: `read_text()` okurken `

` → `
` çeviriyor, `write_text()`
    yazarken `
` → `os.linesep` yani `

` geri koyuyor. Dosya LF ise
    tamamı CRLF'e dönüyor.

    Bu yalnızca estetik bir sorun değil: **gerçek değişiklik gürültünün içinde
    kayboluyor.** Bu projede git'in şimdiye kadarki iki faydası da (Obsidian'ın
    sessiz düzenlemesini ve bayat yapılandırma iddiasını yakalaması) diff'in
    okunabilir olmasına dayanıyordu. Diff okunamazsa denetim de biter.

    **Kural:** bir dosyayı yerinde yamalayan script satır sonuna dokunmamalı.
    `read_bytes()` / `write_bytes()` kullan, ya da `newline=""` ver. Depo
    karışık: notların çoğu LF, `yasanan-hatalar.md` CRLF (Obsidian'ın izi).
    Bu yüzden "hepsini LF yap" da doğru cevap değil — **dosya neyse o kalsın.**

17. **Kaçış karakteri tuzağı üç kılıkta tekrarladı.** Madde 16 satır sonlarını
    anlatıyordu; aynı kök sebep bu oturumda üç kez daha vurdu: satır sonu kaçışı
    heredoc'tan geçerken gerçek satır sonuna dönüşüp üretilen Python dosyasını
    bozdu; Windows yolundaki `\U` "truncated escape" hatası verdi; başka bir
    yoldaki `\N` "malformed character escape" verdi
    (claude 3557db3e · 16.09 10:20 ve 17.09 01:55).

    **Kural:** kod üreten kod yazarken kaçış kullanma. Satır sonu için
    `chr(10)`, Windows yolu için **ham dizge**. Üçü de derleme anında patlıyor,
    yani ucuz yakalanıyor — ama her seferinde bir tur kaybettiriyor. Bu maddeyi
    yazarken bile bir kez daha düşüldü.

18. **Alt dize eşleşmesini ölçüm sanmak.** İki kez yapıldı (claude 3557db3e ·
    16.09 08:28 ve 10:22): yapılandırma dosyasında "nar ajans" geçen satırlar
    sayıldı ve başka bir klasöre ait kayıt da sayıya girdi; `.env` kontrolü
    çıktı içinde alt dize arıyordu ve `.env.example` her çalışmada yanlış alarm
    verdirdi.

    **Kural:** eşleşmeyi **ayırt et**. Satır bazlı karşılaştır, tam eşleşme ara,
    ya da neyi saydığını gözle gör. Arama sonucu bir ölçüm değildir.

19. **Tarih hatası: etiketsiz sayı, yanlış soruya ölçüm, araç tuzağı.** Üç katman
    üst üste geldi (claude 7f10f7a3 · 17.09 03:08–03:11). Kullanıcı "tarih benim
    için çok önemlidir" dediği için madde uzun tutuldu.

    **Ne oldu:** "30 Ağustos'ta Taha'nın videosunu (8 Temmuz 2026, 16:39)
    işlemiştik" yazdım. Bir cümlede üç zaman bilgisi vardı — konuşma tarihi,
    videonun yükleme tarihi, videonun süresi — ve ikisi etiketsizdi. Kullanıcı
    "8 Temmuz mu? Emin misin?" diye sordu; **bizim konuşma tarihimizi**
    soruyordu. Ben videonun yükleme tarihini ölçtüm, "doğruymuş" dedim ve
    yanlış soruyu doğrulamış oldum.

    **Kök 1 — Etiketsiz sayıyı taşıdım.** `ara.py` çıktısında "Avenox, 8 Temmuz
    2026, 16:39" yazıyordu; orası da etiketsizdi. Stringi olduğu gibi kopyaladım.
    *Kural: sayı taşınırken etiketi de taşınır.* Cümlede birden fazla tarih
    varsa her birinin neyin tarihi olduğu yazılır.

    **Kök 2 — Belirsiz soruya netleştirmeden ölçümle cevap verdim.** Soru iki
    anlama geliyordu; ben kendi niyetimi okuyucunun niyeti sandım. Sonra ölçüm
    yaptım ve ölçüm doğru çıktı — ama yanlış şeyi ölçtü. Bu, 30 Ağustos'ta
    Avenox videosundan çıkardığımız dersin aynısı: *yanlış şeyi ölçen tabela,
    hiç tabela olmamasından kötüdür, çünkü "bilmiyorum"u "doğruladım"a çevirir.*
    Burada daha da kötüsü oldu: ölçüm yapmış olmak bana sahte güven verdi ve o
    güveni kullanıcıya da aktardım. **Doğrulama ritüeli yanlış hedefe
    uygulandığında hatayı düzeltmez, sertleştirir.** *Kural: kullanıcı bir
    tarihi/sayıyı sorguladığında, ölçmeden önce hangisini sorduğunu netleştir.*

    **Kök 3 — Araç tuzağı, ölçüldü.** `ara.py` başlığındaki tarih oturumun
    `st_mtime`'ı, yani kaydın **son yazılma** tarihi (`kayit.py:180,196`).
    Avenox oturumu başlıkta `07.09.2026` görünüyor; oysa konuşma **30 Ağustos**
    12:34'te başlamış ve **4 Eylül** 22:08'e kadar sürmüş. Başlığa güvenseydim
    "7 Eylül'de konuşmuştuk" derdim — o da yanlış olurdu.
    *Kural: arşivden tarih alırken **mesaj damgasını** oku, oturum başlığını
    değil. Gerekirse `omurga.py <id>` ile ilk ve son mesaja bak.*

    **Neden bu projede tarih özellikle kırılgan:** oturumlar günlerce açık
    kalıyor. Bu örnekte tek bir oturumun üç farklı "tarihi" var: başlangıç
    (30.08), son mesaj (04.09), dosya mtime (07.09). `CLAUDE.md` bunun yazma
    tarafını uyarıyordu ("oturum başında verilen tarih bayatlar"); **okuma
    tarafı** bu maddeyle kapandı.

20. **Dosya saydım, oturum saydığımı söyledim.** 4–7 Eylül boşluğunu tararken
    "o üç günde altı oturum var" dedim. Kullanıcı itiraz etti: *"Ben kendim o
    kadar oturum açtığımı hatırlamıyorum."* Haklıydı — ben `.jsonl` dosyası
    saymıştım (claude 7f10f7a3 · 17.09 04:54).

    Gerçek sayım üç farklı rakam veriyor ve hangisini kastettiğim yazılmamıştı:
    **7 kayıt dosyası**, **6 benzersiz oturum kimliği** (`adbd10b1` iki yol
    anahtarında mükerrer), ve **4 yeni açılmış konuşma** (biri `6052d412`'nin
    fork'u, yani kullanıcının açtığı yeni bir oturum değil).

    **Kural:** sayı verirken **neyin** sayısı olduğu yazılır. Bu, madde 19'daki
    tarih hatasının aynı kökü: etiketsiz sayı. Orada "hangi tarih" eksikti,
    burada "hangi birim". Dosya ≠ oturum ≠ konuşma; arada fork ve mükerrer
    kayıt var. Ölçüm: [[olculmus-bulgular]] §4.
