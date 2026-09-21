# Araç: izle.py — video ve sesi modele okutma

Model video okuyamaz; video iki okunabilir biçime çevrilir: kare ve transkript.

> Merkez: [[BEYIN]] · İlgili: [[arac-arsiv]] · [[olculmus-bulgular]] · [[yasanan-hatalar]]

---

**Amaç:** Model video okuyamaz. Video, modelin zaten okuyabildiği iki formata
çevrilir: kare (görsel) ve transkript (metin).

```bash
# 1. AŞAMA - tarama: sadece ses, zaman damgalı transkript
python izle.py <kaynak> --basla 0:00 --bitir 16:39

# 2. AŞAMA - yakın bakış: dar aralığın videosu, kareler
python izle.py <kaynak> --basla 4:00 --bitir 6:00 --kare

# ORTAM SINAMASI
python izle.py --kontrol
```

`<kaynak>` yerel dosya yolu **veya** YouTube linki olabilir.

### Neden iki aşama

Kare sayısı **sabittir** (varsayılan 24), video uzunluğuyla artmaz:

| Aralık | Kare | Kare arası |
|---|---|---|
| 1 dk | 24 | 2.5 sn |
| 5 dk | 24 | 12 sn |
| 40 dk | 24 | 100 sn |

Uzun aralıkta kareler işe yaramaz hale gelir. Doğru kullanım: önce transkript
(ucuz, tamamını kapsar) → ilgili zamanı bul → o dar aralığın kareleri. Görseller
metnin kat kat üstünde bağlam yer kaplar.

### Ayar tuzakları (önemli)

- **Ekran kaydı / kaydırmalı sohbet kaydı için varsayılan 24 kare YANLIŞ.** Her
  karede farklı metin vardır; atlanan kare = kaybolan içerik. 2 dakikalık kayıt
  için `--max-kare 50-70` ve `--sessiz` kullan.
- **Sahne algılama (`--sahne`) ekran kayıtlarında çalışmaz.** Ekran yavaş
  değiştiği için 0.04 eşikte bile tek kare çıkar. Varsayılan eşit aralıklı
  örnekleme bu yüzden seçildi.

---

## Dört katmanlı hat — 17 Eylül 2026 kurulumu

Eski hat iki katmanlıydı (ses + kare). Kullanıcı *"videonun kaç saniyesinde bir
kare alıyorsun"* diye sorunca ölçüldü, kusur çıktı ve hat yeniden kuruldu
(claude 7f10f7a3 · 17.09 05:30). Ölçümler: [[olculmus-bulgular]] §5.

| Katman | Ne yapar | Durum |
|---|---|---|
| 1. Ses | Whisper large-v3, GPU, Türkçe sözlükle | vardı, dokunulmadı |
| 1b. İkinci tanık | YouTube'un hazır altyazısı (`--altyazi`) | **yeni** |
| 2. Kare | Yoğunluk (`--kare-sn`) + dhash elemesi (`--benzer`) | **yeni** |
| 3. Yazı | Tesseract OCR, Türkçe (`--ocr`) | **yeni** |
| 4. Birleştirme | Üç kaynak tek zaman çizelgesinde, ayrışma işaretli | **yeni** |

### Neden sıklık, neden sayı değil

Eski davranış kare **sayısını** sabit tutuyordu (24), yani aralık uzadıkça
kareler seyreliyordu — tam videoda 41,6 saniyede bir kare. `--kare-sn 2`
sıklığı sabitler, kare sayısı aralıkla büyür. Kullanıcının kafasındaki birim
zaten buydu; araç yanlış birimle konuşuyordu.

### Eleme iki aşamalı

Önce `dhash` (ucuz, görsel benzerlik), sonra OCR metni (pahalı ama doğru ölçüt).
Sıra önemli: hash 120 kareyi 29'a indirir, OCR sadece o 29'u okur. Son söz
OCR'ındır çünkü sorulan soru *"görüntü değişti mi"* değil, **"bilgi değişti mi".**

### İkinci tanık: altyazı

`--altyazi` önce kanalın yüklediği altyazıyı, yoksa YouTube'un otomatik
üretimini çeker. **İkisi de tahmindir, hakem değildir** — Avenox'un "manuel"
görünen altyazısı bile elle yazılmamış, kendi AI transkripsiyon aracının
çıktısı (kullanıcı 17.09 05:24'te düzeltti). Değeri yine de var: o araç ham
kaydı duydu, Whisper YouTube'un sıkıştırmasını duyuyor. **Uyuştukları yer
güçlü, ayrıştıkları yer şüpheli.**

### İlk gerçek test

`WIw1lMIRL3I` 22:10–23:15, `--kare-sn 2 --ocr --altyazi`:
32 ham kare → 3 benzersiz slayt. Whisper 4 paragraf verdi; OCR ise
transkriptte **hiç geçmeyen** bir ödev listesi çıkardı. Bu videoda ses ve
görüntü farklı şey söylüyor: biri anlatıyor, diğeri veriyor.

### Bilinen kusurlar

- **OCR gürültü üretiyor:** süs şekiller ve logolardan "İcik dik, dale kür"
  gibi parçalar geliyor. Üç karakterden kısa parçalar ayıklanıyor ama yetmiyor.
- **dhash eşiği video tipine bağlı.** 24 animasyonlu slaytta doğru; eşiği 8'e
  düşürmek bu testte sonucu değiştirmedi, yani eşik her videoda ayarlanmalı
  değil ama körü körüne de güvenilmemeli.
- **Yerel görsel-dil modeli kurulmadı.** Yeri belli: video tipini tanıyıp
  eşiği seçmek. Önce OCR hattının çıktısı güvenilir olsun; denetlenemeyen
  özet, kazanılan bağlamı doğrulukla öder.

### Kurulum

Tesseract `winget install UB-Mannheim.TesseractOCR`, Türkçe dil paketi
`tessdata_best`'ten **D:/AI/tessdata**'ya (C diski %94 dolu). `IZLE_TESSDATA`
ortam değişkeniyle taşınabilir. `--kontrol` artık Pillow ve Tesseract dillerini
de raporluyor.

### Katman 4: birleştirme ve ayrışma haritası

Üç kaynak (Whisper, altyazı, OCR) zaman kovalarında (`--kova`, varsayılan 20 sn)
tek `birlesik.md` dosyasında toplanır. Amaç **doğruyu seçmek değil**, iki
tanığın ayrıştığı yeri işaretlemek: ayrışan kelime ya birinin hatasıdır ya
ötekinin duyduğu ek bilgidir; ikisi de bakmaya değer.

**Kurulurken çıkan kusur ve çözümü (claude 7f10f7a3 · 17.09 05:45):**
İlk sürüm 38 kelimeyi ayrışma diye işaretledi; gerçek sayı **5**'ti. Aradaki
fark hizalama kaymasıydı — Whisper bir segmentin **başını** damgalayıp uzun
paragraf veriyor, altyazı her cümleyi ayrı damgalıyor. Aynı cümle iki kaynakta
farklı kovaya düşünce sistem "biri söylemiş öteki söylememiş" sandı.

**Kural:** kelime karşılaştırması dar pencerede gösterilir ama **geniş
pencerede** (±1 kova) yapılır. Aksi hâlde araç kendi hizalama hatasını
içerik hatası gibi raporlar — yanlış şeyi ölçen tabelanın bir başka kılığı.

**İlk testte yakalanan gerçek ayrışmalar** (`WIw1lMIRL3I` 22:10–23:15):

| Whisper | Altyazı | Durum |
|---|---|---|
| `bytecoder` | `bipecoder` | **ikisi de yanlış** — muhtemelen "vibe coder" |
| `Hermes` | `her birisi` | karar verilemedi, işaretli kaldı |
| `yorun` | `görün` | Whisper yanıldı ("eğitim bütçesi gibi görün") |
| `ayda` | `ayta` | altyazı yanıldı ("ayda 100 bin dolar") |

İki tanığın **aynı yerde farklı şekilde** yanılması en güçlü şüphe işaretidir:
tek transkriptte bu dördü sessizce doğru sanılırdı.

## Video verilince SOR: şema var mı?

**Refleks kuralı, kullanıcı talimatı (claude 7f10f7a3 · 17.09 05:46).**
Bir video verildiğinde, işe başlamadan önce sorulacak: *videoda mimari şema,
akış diyagramı, grafik var mı?* Varsa yerel görsel-dil modeli kurulur; yoksa
OCR hattı yeterlidir.

### Neden soru şart — sessiz başarısızlık

"Şemalı videoda OCR boş döner" demiştim; kullanıcı düzeltti: **boş dönmez.**
Şemadan kutu etiketlerini okur, birkaç kelime çıkarır, ve model o kelimelere
bakıp *içeriği gördüm* sanır.

Oysa şemada bilgi kutuların içinde değil, **kutular arasındaki ilişkidedir**:
okun yönü, hangi kutunun hangisini beslediği, hiyerarşi, gruplama. OCR bunların
hiçbirini görmez — ve görmediğini **söylemez.**

Modelin bunu kendi başına fark etmesi yapısal olarak imkânsız: elinde karenin
kendisi değil, yalnızca OCR çıktısı vardır. Eksiği anlaması için zaten görmüş
olması gerekir. Kullanıcının ifadesiyle: *"gördüğünü zannedersin."*

Bu, [[tasarim-dersleri]]'ndeki sessiz başarı vakalarının video hattındaki
karşılığıdır ve aynı kökten gelir: **çıkış kodu 0 döndürmek, işin yapıldığı
anlamına gelmez.**

### Kural

- Video isteği geldiğinde **önce sor**, sonra hat kur.
- Cevap "şema var" ise VLM kurulur; OCR tek başına kullanılmaz.
- Cevap "yok, düz metin/slayt" ise mevcut dört katmanlı hat yeterlidir.
- Emin değilsen bir kareyi **gözünle gör** ve öyle karar ver — ucuzdur,
  yanlış karar pahalıdır.

## Kaç kaynak, hangisi neyde iyi (ölçüldü 21.09.2026)

Avenox'un iki videosu dört ayrı kaynakla çözümlendi ve özel isimler tek tek
karşılaştırıldı. Sonuç sezgiye aykırı: **en büyük model en iyi kaynak değil.**

| Terim | YouTube elle | YouTube oto | yerel `small` | yerel `large-v3` |
|---|---|---|---|---|
| Claude | ✔ | cloud | Cloud | **Cloud** |
| Mem0 | ✔ | Memziro | Memzüro | **Memziro** |
| Karpathy | ✔ | Karpati | Carpathian | yok |
| GitHub | ✔ | Gitapta | kitapla | ✔ |
| harness | ✔ | harnsta | harnista | ✔ |
| hook | ✔ | ✔ | hukuk | ✔ |
| Vault | ✔ | W'da | Valtı | ✔ |
| Obsidian | ✔ | Obsidyen | ✔ | ✔ |
| agent | ✔ | — | **Ejint** | ✔ |
| **Skor** | **9/9** | 2/9 | 1/9 | **6/9** |

**Neden.** Ses tanıma, duyduğu sese en yakın *bilinen* kelimeye düşer. Yeni
bir özel isim eğitim verisinde yoksa model onu uyduramaz: JEV videosunda
`large-v3` "JEV"i baştan sona **"Java" / "Jav"**, "LLM"i **"el elem"** yazdı —
"JEV" 15.09.2026'da çıkmış bir kelime. YouTube'daki elle yüklenen altyazı ise
terimi *bilerek* üretildiği için doğru yazıyor. Kanalın altyazısını yapay
zekânın üretmiş olması onu zayıflatmıyor; üretim bağlamlı yapılmış.

**Kural.** Video çözümlemesinde tek kaynağa güvenme, `--altyazi` ile en az iki
tanık al ve şöyle oku:

- **Özel isim, komut, sürüm numarası** → YouTube'un elle altyazısı hakem.
- **Cümlenin tamamı, atlanan bölüm, akışın yapısı** → whisper hakem.
  Ölçüldü: elle altyazıda eksik olan 01:21–01:24 aralığını `large-v3` doldurdu.
- **`small` modeli teknik içerikte kullanılmaz.** "agent"ı baştan sona
  "Ejint", "hook"u "hukuk" yazdı.

**Nerede çalıştırılır.** Lokal GPU (RTX 3060 Ti, 8 GB). 955 sn'lik video,
indirme dahil **4 dakika**. Aynı iş sunucunun CPU'sunda (Xeon E5-2699 v4,
4 çekirdek) `medium` ile gerçek zamanın 4,3 katı yavaş ilerliyordu, tahmini
68 dakika. Video işi sunucuya gönderilmez.

**Bilinen kusur.** `birlesik.md` iki akışı zaman penceresine göre eşliyor;
damgalar kaydıkça pencereler kayıyor ve "ayrışma" işaretlerinin bir kısmı
gerçek anlaşmazlık değil **hizalama kayması** oluyor. İlk videoda 48 ayrışma
işaretlendi, hepsi gerçek değil. `--kova` ile pencere genişletilebilir;
düzeltme yapılmadı.
(claude 96517e26 · 21.09 06:42)

> İlgili: [[olculmus-bulgular]] · [[acik-uclar]] · [[2026-09-21-otomasyon-lab-ve-vds]]
