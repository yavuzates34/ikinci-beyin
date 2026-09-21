# Açık uçlar

> **05:46 güncellemesi:** Codex %70 uyarısı da bu oturumda gerçek hook
> kaydı ve kurtarma dosyasıyla doğrulandı. Önceki “%70 ölçülmedi” satırları
> bu olaydan önceki durumdur. Canlı PreCompact ve yeni gece tetiklemesi ayrı
> olarak ölçülmedi. Yeniden başlatma sonrası canlı Codex penceresi 828.400;
> katalog üst sınırı 872.000 × %95. Compact ayarı 750.000.
> [[2026-09-20-astra-kontrol]].

Karar bekleyenler, yapılmamış testler, sıralanmış yol haritası. **Yalnızca açık
olanlar burada durur.** Kapanan ya da devredilen madde metniyle birlikte
[[acik-uclar-tarihce]] dosyasına taşınır, silinmez (kullanıcı kararı, 19.09).

> Merkez: [[BEYIN]] · İlgili: [[kullanici-baglami]] · [[ikinci-beyin-mimarisi]] · [[capraz-arac-baglam]] · [[2026-09-19-sunum-onarim-listesi]]

---

## Açık — sistem

**Astra sonrası güncel okuma (20.09):** Tarihsel maddelerdeki iddiaların
düzeltmeleri [[astra-denetim-bulgulari]] içinde. Madde 1'in Codex **%50**
ayağı canlı doğrulandı; **%70**, canlı PreCompact ve uzun tek tur kontrolü
açık. Madde 6'nın görev ayarı kullanıcı onayıyla düzeltildi; yeni gece
tetiklemesi ölçülmedi. “Commit hiç çalışmadı” iddiası yanlış. Madde 5'in
üçüncü göz/kod/kaynak metin denetimi yapıldı; yayımlanan claude.ai sunumu
ölçülmedi. Bakım taşımaları yapılmadı. Yeni 1M Codex ayarı dosyada ve
yapılandırma okuyucusunda doğrulandı; açık Desktop oturumuna uygulanması
henüz doğrulanmadı.
(codex 01a0bc5c-f1c4 · 20.09 05:33)

1. **Erken devir: Claude'da iki eşik canlı; Codex'te eşik olayı bekleniyor.**
   %50 (19.09 20:31) ve %70 (20.09 00:36) uyarıları gerçek hook zinciriyle
   geldi ve ikisinde de kurtarma omurgası yazıldı. Codex'te `SessionStart` ve
   `UserPromptSubmit` taşıyıcıları güven sonrası canlı doğrulandı; formül de
   ham kayıtta elle doğru sonuç veriyor ([[olculmus-bulgular]] §14.2). Açık
   kalan tek kanıt, gerçek bir Codex oturumunun %50 ve %70'i geçip uyarının ve
   kurtarma omurgasının otomatik oluşması. Onarım listesi madde 7.

2. **Denetim katmanı: iki seviye kurulmadı.** Mekanik işaretçi denetimi kurulu
   ve gece taslaklarını da tarıyor. Kurulmayanlar:
   - **Örneklemeli içerik denetimi:** haftada bir, rastgele 3-5 işaretçi.
     Temiz bağlamlı ajan iddiayı kayıtla karşılaştırır.
   - **Kapanış denetimi:** kapanıştan sonra yazılan notlar ham kayda karşı
     denetlenir.

   **Kararlar:** Denetçi rapor eder, düzeltmez. Uyuşmazlık bulunursa iddianın
   altına not düşülür (kullanıcı, 19.09).

3. **Side chat'ler arşive hiç girmiyor.** Kayıt dosyası oluşmuyor. Tek yol elle
   aktarma. Ölçüm: [[olculmus-bulgular]] §6.

4. **Kalıcı katman boyutu.** Bakım döngüsü kuruldu: `araclar/bakim.py`
   adayları ölçüyor, derleyici raporluyor, oturum başı uyarıyor. İlk bakımda
   kullanıcı iki taşımayı onayladı: kapanmış açık uçlar ve iş bitince onarım
   listesi. Kuralların yanındaki tarihçenin taşınmasını onaylamadı
   (claude 5c600e7e · 19.09 20:31). 100 KB eşiği bundan sonra da aşılı
   kalabilir; karar kullanıcının, ileride yetkili orkestratör ajanın.

5. **Sunum onarımı sürüyor.** 13 açık ve sonradan bulunan 14, 15, 16. açıklar:
   [[2026-09-19-sunum-onarim-listesi]].

6. **Gece görevi tetikleniyor ama yarıda ölüyor.** Görev saatinde çalışıyor
   (`LastRunTime 00:30:01`, atlanan çalışma yok) ama `0xC000013A`
   (STATUS_CONTROL_C_EXIT) ile sonlanıyor: `LogonType = Interactive` olduğu
   için görünür bir konsol penceresi açılıyor, o pencere kapanınca süreç
   gidiyor. Günlük derleme yazılıyor, **git commit + push hiç çalışmıyor.**
   Son dört gecenin ikisi böyle. Ölçüm: [[olculmus-bulgular]] §16. Düzeltme
   (görevi S4U / gizli pencere olarak kurmak) **sistem ayarıdır, kullanıcıya
   ait**; uygulanmadı. Onarım listesi madde 16.

7. **Tam otomasyon kararı (20.09).** Kullanıcı sistemin tam otomatik
   çalışmasına karar verdi; kapanış ritüeli yerine **eşik ritüeli** gelecek,
   çünkü sistem uygulamanın arayüzünde oturum açıp kapatamıyor. Tasarım,
   7 açık (3 küme), kabul edilen politikalar ve ölçülecekler
   [[2026-09-21-tam-otomasyon-plani]] içinde. En kritik teknik engel: bağlam
   ölçümü turun **içinde** yok (`UserPromptSubmit`'e bağlı), bu yüzden uzun
   tek tur eşiği kaçırıyor. İlk üç iş: telafi kuyruğu, örneklemeli içerik
   denetimi, sağlık/eskime alarmı.
   (claude 96517e26 · 21.09 01:11)

8. **Görünürlük sızıntısı — mekanizma kuruldu, BİR KARAR bekliyor.**
   Astra ölçtü: açıkça `ozel` ve etiketsiz iki notu Avenox `internal`
   indeksledi, içeriği bağlama verdi ve gölge modunda sağlayıcı taşıyıcısına
   ulaştırdı. `gorunurluk.json` yalnız **bizim** kodumuz sorduğunda çalışıyor;
   kasayı tarayan yabancı bir araç için hiçbir şey ifade etmiyor. Tasarım
   sözleşmeleri [[2026-09-21-tam-otomasyon-plani]] içinde.
   (claude 96517e26 · 21.09 07:29)

   **Yapıldı (21.09 07:57):** `araclar/disari.py` — kapı, yansıma, bulucu.
   Yabancı araca artık kasa değil yansıma verilir. Astra'nın İ2 deneyi kalıcı
   regresyon testi oldu (`SizintiTests`, negatif kontrolüyle birlikte).
   Ölçüm ve tasarım gerekçesi: [[olculmus-bulgular]] §20.

   **Açık kalan — kullanıcı kararı.** Kapı kurulunca ilk durdurduğu şey
   Avenox değil, **kendi gece yazıcımız** oldu: `gece_kayit.py` 19.09'dan beri
   her gece ham omurgayı (`ozel`) bir modele veriyordu. Etiketle davranış
   birbirinden habersiz konmuş, çelişki bugüne kadar sessizdi. İki seçenek:
   **(1)** `gorunurluk.json`'a "ham oturum kaydı `ic`'tir" kuralı girilir,
   gece yazıcısı çalışır; **(2)** kapalı bırakılır, gece taslağı üretilmez.
   Seçim kullanıcının: `ozel` etiketi "makineden çıkmaz" diyor, gece yazıcısı
   ise tam olarak onu çıkarıyordu. (claude 96517e26 · 21.09 07:57)

   **Kapanmayan kısım.** Üç katman da, bir aracın kasayı kendi başına
   taramasını **engellemez**. Onu ancak dosya izinleri engeller. Lab'de
   `avenox` kullanıcısının sudo'su yok; aynı ayrım yerelde kurulmadı, çünkü
   kendi araçlarımızı da kilitlerdi.

9. **İ1 ölçümü bekliyor.** "Dört katmanlı bağlam ölçümü gereksiz" hükmü
   verilemedi. Gereken deney: **uzun tek tur + compact + kesinti** senaryosunda
   kaydedilmiş karar/görev durumunun geri kazanımı ve maliyeti.
   (claude 96517e26 · 21.09 07:29)

## Ertelenenler

- **Gelen kutusu** (mobilden not düşme) ve **mem0** (kullanıcı, 16.09).
  Uyarı: boşaltılmayan gelen kutusu çöplüğe döner; değer damıtma ritüelinde.
- **Paralelleştirme / mesh** (kullanıcı, 18.09): "birkaç seviye sonra". O
  gün geldiğinde yeni oturuma geçiş, `kapanan-oturum:` ve bakım onayı yetkili
  orkestratör ajana da verilebilir (kullanıcı, 19.09). Bugünkü devir kutusu
  mesh'e uygun değil: [[agentic-yapi]].

## Karar bekleyenler

- **Kalıcı katman bölme paketi:** [[kalici-katman-bakim-plani]]. Üç büyük
  notun eski ölçüm/deneme tarihçesini kaynaklarıyla arşive almak önerildi;
  yaklaşık 96–97 KB sıcak katman hedefi tahmin. Henüz onaylanmadı/uygulanmadı.
  (codex 01a0bc5c-f1c4 · 20.09 17:24)

- Tek ortak hafıza klasörü (`autoMemoryDirectory`) kurulmadı.
- Raspberry Pi alınacak mı? Öneri: önce mevcut makineyi sürekli açık bırakıp
  uzaktan bağlanmayı test et.

## Yapılmamış testler

- **Gece taslağının ilk gerçek gecesi:** 20.09 00:30 çalıştı ama **yarıda
  kesildi** (yukarıda madde 6). Zincir aynı gece 00:45'te *elle* tetiklenerek
  uçtan uca çalıştı; zamanlanmış yolun kendisi hâlâ ölçülmedi. Sıradaki fırsat
  21.09 00:30.
- **Codex Desktop'ta yepyeni oturum:** hook güveninden sonra `SessionStart` ve
  erken devir uyarısı ham kayıtta görülmeli.
- `--fork-session` canlı denenmedi.
- Ekran kaydı → `izle.py` zinciri gerçek bir ChatGPT kaydıyla denenmedi.
  **Kısmen kapandı (21.09):** zincir iki gerçek YouTube videosunda uçtan uca
  çalıştı — indirme, `--altyazi` ikinci tanık, `large-v3` GPU transkripti,
  birleşik döküm. 955 sn'lik video 4 dakikada bitti. Ölçüm ve kaynak seçme
  kuralı [[arac-izle]] içinde. **Denenmeyen kalan:** `--kare` + `--ocr` ayağı,
  yani ekrandaki yazıyı okuma — ChatGPT kaydı senaryosunun asıl kısmı.
  (claude 96517e26 · 21.09 06:42)

## Uzun vade

- Ölçek gerektiğinde sunucuya taşı (şimdiden uğraşma).
