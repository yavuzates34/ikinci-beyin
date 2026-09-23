---
name: video-inceleme
description: Kullanıcının verdiği yerel video/ses veya YouTube bağlantısını zaman damgalı transkript, seçilmiş kareler, OCR ve varsa altyazıyla incele. Video içeriği analizi istendiğinde kullan.
---

# Video inceleme

Bu vault'a bağlı [izle.py](scripts/izle.py) isteğe bağlı bir yerel araçtır. Eski
İkinci Beyin'in hooklarına, promptlarına veya dosyalarına çalışma anında dayanmaz.
Kullanıcı video ya da ses kaynağı verdiğinde kullan; kendiliğinden medya tarama.

1. Ortam belirsizse `py -3 scripts/izle.py --kontrol` ile bağımlılıkları denetle.
   Çalıştırırken bu skill klasörünü değil, mevcut vault'u çalışma dizini yap ve
   betiği mutlak yoluyla çağır.
2. Uzun videoda önce yalnız ses transkripti al. YouTube bağlantısında ikinci
   tanık yararlıysa `--altyazi` ekle. Sonuçtaki zaman damgalarından ilgili
   kısa aralığı seçip `--basla` ve `--bitir` ile `--kare` çalıştır.
3. Ekran kaydı ve yazılı slaytlarda `--kare-sn` ile örnekleme sıklığı belirle;
   bilgi kaybı yaratabilecek dHash elemesini istemiyorsan `--benzer 0` kullan.
   `--ocr`, karedeki yazıyı çıkarır; diyagramların ok yönü veya ilişkilerini
   anlamak için asıl kareyi ayrıca görsel olarak incele.
4. Whisper, altyazı ve OCR çıktıları kanıttır, kesin doğru kabul edilmez.
   Ayrışma ve eksikleri zaman damgasıyla belirt. Video içeriğini otomatik
   olarak İkinci Beyin hafızasına kaydetme; yalnız kullanıcının işiyle ilgili,
   doğrulanmış ve kalıcı sonucu beyin protokolüyle kaydet.

Betik kaynak olarak yerel dosya veya YouTube URL'si kabul eder. Varsayılan
çıktı sistemin geçici klasöründedir; `--cikti` verilirse vault dışındaki
**boş** bir klasör olmalıdır. Var olan çıktı klasörü yeniden kullanılmaz.
Eski `sozluk.txt` içe alınmadı. Gerektiğinde `--terimler` ile yalnız o
çalıştırmaya özgü teknik adlar verilebilir.

Örnekler:

```powershell
py -3 'D:\AI\ikinci-beyin-v3.2\.agents\skills\video-inceleme\scripts\izle.py' 'C:\Video\kayit.mp4' --basla 0:00 --bitir 15:00
py -3 'D:\AI\ikinci-beyin-v3.2\.agents\skills\video-inceleme\scripts\izle.py' 'C:\Video\kayit.mp4' --basla 4:00 --bitir 6:00 --kare --kare-sn 2 --ocr --benzer 0
```

Araç `ffmpeg`, `ffprobe`, `faster-whisper`/`ctranslate2`, isteğe bağlı
`yt-dlp`, Pillow ve Türkçe Tesseract kullanır. `--kontrol` kurulumun hangi
parçasının bulunduğunu gösterir. Ağ gerektiren YouTube işini kullanıcı
kaynağı verdiğinde başlat; eski sistemin komutlarını veya hooklarını çalıştırma.
