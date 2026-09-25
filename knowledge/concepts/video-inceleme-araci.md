---
kind: fact
visibility: internal
created_at: 2026-09-24
---
# Yerel video inceleme aracı

## Neden burada

Yavuz, 24 Eylül 2026'da eski deneysel İkinci Beyin'indeki video ayrıştırma ve
analiz aracını yeni V3.2 sistemine bağlamayı açıkça istedi. Eski sistemin
talimatları, promptları ve hookları bu isteğin kapsamında değildir. Eski kaynak
klasörü `C:\Users\Anj\Desktop\desktop\playground` salt okunur incelendi.

## Doğrulanan araç

Kaynak uygulama `C:\Users\Anj\Desktop\desktop\playground\araclar\izle.py`
(özellikle satır 79–187, 192–343, 365–427 ve 470–586; SHA-256
`6B1EACDBDC2E7DFABDDF2922D7BA7BFF1E5C7FF5CC54A73B0C5888A7C990CB12`).
Yerel dosya veya YouTube videosundan zaman damgalı Whisper transkripti,
isteğe bağlı altyazı, kare ve Tesseract OCR metni çıkarıp bunları bir zaman
dökümünde birleştiriyor. Kendi başına çalışan bir CLI; eski hook veya proje
modüllerini import etmiyor. Eski tarihli kullanım ve sınırlar
`C:\Users\Anj\Desktop\desktop\playground\notlar\arac-izle.md` içinde kayıtlıdır.
Bu kullanım kayıtları bugünkü çalışma durumunun kanıtı değildir.

## V3.2 bağlantısı

Araç kodu incelenerek yalnız V3.2 içindeki
[video-inceleme becerisine](../../.agents/skills/video-inceleme/SKILL.md) uyarlandı;
eski `sozluk.txt` promptu, eski hooklar ve eski talimatlar taşınmadı. Yeni
[betik](../../.agents/skills/video-inceleme/scripts/izle.py) yalnız kullanıcı
video verdiğinde çağrılır. Varsayılan çıktı sistemin geçici klasöründedir;
vault dışındaki boş bir `--cikti` klasörü de seçilebilir. Eski çıktı klasörünü
yeniden kullanmak engellenerek kaynak doğrulamayan önbellek riski giderildi.
YouTube indirmesi tek videoyla sınırlandı; geçersiz parametre ve bazı alt süreç
hataları açık hata verir. Kullanıcıya özel teknik terimler ancak o çalıştırmada
`--terimler` ile verilir.

24 Eylül yerel kontrolü: yeni betiğin sözdizimi ve CLI yardımı açıldı;
ffmpeg/ffprobe, yt-dlp, CTranslate2 ile CUDA, `large-v3` model klasörü,
Pillow ve Türkçe Tesseract görüldü. Yapay 3 saniyelik yerel videodan üç kare
çıktı, OCR `TEST 123` okudu. Aynı çıktı klasörünü tekrar kullanma ve sıfır
kare parametresi reddedildi. Whisper `large-v3` GPU yolu yapay sinüs sesini
işledi; konuşma olmadığı için transkript 0 satırdı. Gerçek Türkçe konuşmanın
kalitesi ve YouTube altyazısı bu entegrasyon turunda sınanmadı.

## İçerik sınırları

OCR şemadaki okları ve ilişkileri tek başına açıklamaz; görsel yapı gerekiyorsa
kare ayrıca incelenir. Whisper, YouTube altyazısı ve OCR ayrı ve hatalı
olabilecek tanıklardır. Eski `notlar/arac-izle.md:140–170` bu sınırla ilgili
tarihli kullanıcı düzeltmesi aktarıyor; ham kullanıcı konuşması burada yoktur.
Eski kişisel tercih özetleri, tarihli doğrulama eksikliği nedeniyle Core'a
aktarılmadı. Eski AI operatörlüğünün “kariyer değil” anlatımı, Yavuz'un
23 Eylül'deki doğrudan mesleki hedef beyanıyla çeliştiğinden içe alınmadı.
Eski genel “proje egemenliği” notu Yavuz'un 24 Eylül'deki açık cevabı üzerine
güncel kural sayılmadı; Nar Ajans için ayrı salt okuma talimatı geçerlidir.

## 24 Eylül 2026 — Esat reels görselindeki iki kaynak

Yavuz'un paylaştığı ekran görüntüsünde `yt-dlp.md` ve `ffmpeg.md` adlı iki
“developer resource” kartı görünüyor; dosyaların içeriği ve reel bağlantısı
görselde yok. Bu nedenle bu iki Markdown kaynağının özgün önerileri henüz
karşılaştırılamadı. Ancak yerel [video becerisi](../../.agents/skills/video-inceleme/SKILL.md)
ve [betik](../../.agents/skills/video-inceleme/scripts/izle.py) her iki aracı
zaten kullanıyor: `yt-dlp` YouTube videosu/altyazısı için; `ffmpeg`/`ffprobe`
kesit, ses dönüşümü, kare çıkarımı ve süre ölçümü için. Aynı gün
`izle.py --kontrol` çıktısı üçünün de sistemde bulunduğunu doğruladı.
Görsel tek başına ek kod veya yeni skill kurmayı gerektirmiyor. Özgün dosya
veya reel bağlantısı gelirse farklı yöntem/özellik olup olmadığı yeniden
değerlendirilebilir. Kaynak: Yavuz'un 24 Eylül'de paylaştığı reels ekran
görüntüsü ve yukarıdaki yerel beceri/betik.

## 24 Eylül 2026 — Gerçek Instagram videosuyla kullanım

Yavuz'un verdiği [60,7 saniyelik reel](https://www.instagram.com/reel/DdjwSQBOKzQ/)
`yt-dlp` ile geçici yerel MP4'e alındı; mevcut `izle.py` bu yerel dosyada
Whisper large-v3/CUDA ile 23 zaman damgalı transkript satırı, birer saniyelik
60 kare ve Türkçe/İngilizce OCR üretti. Beş becerinin adları ses ve karelerde
eşleşti; “Claude” gibi terimler transkriptte yer yer yanlış yazıldı ve
repo özellikleri özgün GitHub kaynaklarından ayrıca denetlendi. Bu, gerçek
Türkçe konuşma ve Instagram'dan yerel dosyaya aktarma yolunun çalıştığını
gösterir; otomatik Instagram URL desteği eklendiği anlamına gelmez. Sonuç:
[beş beceri değerlendirmesi](reel-bes-beceri-degerlendirmesi.md).
