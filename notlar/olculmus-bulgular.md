# Ölçülmüş bulgular

Tahmin değil, ölçüm. Yeniden ölçmeye gerek yok — kaynağı belirtilmiştir.

> Merkez: [[BEYIN]] · İlgili: [[arac-izle]] · [[arac-arsiv]] · [[ortam-kurulum]]

---

Bunlar tahmin değil, bu oturumda ölçüldü. Yeniden ölçmeye gerek yok.

### 3.1 YouTube indirme stratejisi

| Yöntem | Boyut | Süre |
|---|---|---|
| Ses, tamamı (16:39 video) | 15 MB | **2 sn** |
| Ses, kırpılmış (100 sn) | 1.7 MB | 55 sn |
| Video, tamamı (16:39) | 54 MB | ~5 sn |
| Video, kırpılmış (100 sn) | **3.7 MB** | 55 sn |

Kırpma süresi **kaynak uzunluğundan bağımsız**, sadece dilim uzunluğuna bağlı.
Tam indirme kaynakla doğru orantılı büyür. **Başabaş ≈ 1 saatlik video.**

Uygulanan kural: ses her zaman tam indirilir; video 60 dakikadan uzunsa kırpılır.
Eşik `IZLE_KIRPMA_ESIGI` ile ayarlanır.

### 3.2 Whisper model karşılaştırması (aynı ses, aynı sözlük)

`small` → `large-v3` geçişinde düzelenler: "cpt 5.5"→"GPT 5.5", "kenar
altyapımda"→"kendi altyapımda", "bağır hava hara"→"bağıra bağıra", "kontrol edilse
müsaiti"→"kontrol edebilsin o sayede".

104 saniyelik ses, GPU'da **52 saniye** (model yüklemesi dahil).

### 3.3 Sözlüğün yan etkisi — ÖNEMLİ

Sözlük tek yönlü kazanç değil. **Listelenen terimlere doğru eğiyor, bu da olmayan
yerde onları duymasına yol açıyor:**

- `small`, "modele **kod** yazdırıyorsun"u "modeli **Code** yazdırıyorsun" yazdı
- `large-v3`, "skor"u "**score**" yazdı
- Her iki model de "Claude"u ısrarla **"cloud"** duyuyor (Türkçe telaffuzda
  "klod" ≈ "cloud"). Sözlükteki "Claude" kaydı yetmiyor.

**Sonuç:** sözlük dar ve spesifik tutulmalı. "loop", "goal", "graph" gibi genel
kelimeler Türkçe konuşmaya yanlış sızıyor.

### 3.4 Claude Code oturum arşivi

Konum: `~/.claude/projects/<proje-yolu>/<oturum-id>.jsonl`
Durum (30 Ağustos ölçümü): **37 oturum, 83 MB**. En büyük tek oturum **28.8 MB**.

**Görseller arşivin İÇİNDE gömülü** (base64): 63 görsel, 11.5 MB. Orijinal dosyaya
bağımlı değil. Doğrulandı: 13 gün önceki başka bir projenin oturumundan görsel
çıkarılıp okundu.

**Belgeler (PDF/zip) gömülü DEĞİL** — sadece dosya yolu saklanır:

| Kayıt tipi | Yol | Hâlâ var |
|---|---|---|
| `edited_text_file` (proje içi) | 17 | 17 |
| `pdf_reference` | 1 | 1 |
| `file` | 38 | 18 |
| `compact_file_reference` | 11 | 4 |
| **Toplam** | **67** | **40 (%59)** |

Kayıpların 14'ü `Temp/scratchpad` (zaten geçici), 13'ü taşınmış/silinmiş dosya.
**Çıkarım:** önemli kaynak belgeler proje içinde bir `kaynaklar/` klasörüne
kopyalanmalı — bu tek hamle %59'u %100'e çıkarır.

### 3.5 Codex oturum arşivi

`~/.codex/sessions/` altında yıl/ay/gün klasörlerinde, Mayıs 2026'ya kadar geriye
giden **80+ oturum**, ayrıca 47 arşivlenmiş oturum.

**Toplam:** Claude + Codex = **117+ oturum** konuşma kaydı, zaman damgalı, diskte.

### 3.6 Hafıza dosyaları (30 Ağustos ölçümü)

9 projede 37 hafıza dosyası. **7'sinde `[[wikilink]]` var, 30'u tamamen izole.**
Bağ olan 7'yi kullanıcı yazmadı — hafıza formatını takip eden modeller yazdı.

---

## 4. Arşiv arkeolojisi — 4–7 Eylül boşluğu

Kullanıcı arşiv tablosuna bakıp *"4 Eylül ile 7 Eylül arasındaki üç günlük
boşluğun sebebi ne"* diye sordu. Tüm yol anahtarlarındaki ham kayıtlar
tarandı (claude 7f10f7a3 · 17.09 04:53).

### 4.1 Boşluk playground'a ait, kullanıcıya değil

playground tarafında gerçek sessizlik: **04.09 22:08 → 07.09 10:24**, yaklaşık
iki buçuk gün. Ama o aralıkta başka klasörlerde çalışılmış:

| Oturum | Klasör | Aralık |
|---|---|---|
| `1b86bb52` | Nar Ajans - Codex | 05.09 04:02 – 07.09 12:08 |
| `54366b9c` | Nar Ajans - Codex | 05.09 04:21 – 04:33 |
| `adbd10b1` | Nar Ajans - Codex | 06.09 15:27 – 15:32 |
| `3febe5ab` | Desktop | 06.09 03:52 – 07.09 10:21 |

İkisi çok kısa (12 ve 5 dakika) — kullanıcının hatırlamaması beklenir.

### 4.2 Boşluğun asıl sebebi: oturum fork'landı, klasör taşındı

`6052d412` (eski yol: `Desktop\playground`) 04.09 22:08'de son mesajı aldı.
Aynı konuşma **`3c1530e9` kimliğiyle yeni yol anahtarında**
(`Desktop\desktop\playground`) devam etti; kaydın ilk damgası **04.09 22:13**.
Kullanıcı 07.09 10:24'te oraya yazdığında sistem şunu bildirmişti:
*"This conversation was forked from another session and now runs in a different
working tree."*

Yani 4–7 Eylül boşluğu iki şeyin üst üste binmesi: klasör taşıması ve ona bağlı
fork. Konuşma kopmadı, **kimlik değişti.**

**Düzeltme:** [[BEYIN]] "7 Eylül'de taşındı" diyordu; yeni yol anahtarındaki ilk
damga **04.09 22:13**. Taşıma 4 Eylül gecesi oldu, kullanıcı 7 Eylül sabahı
devam etti.

**İkinci düzeltme:** [[acik-uclar]] "`--fork-session` canlı denenmedi" diyor.
Fork fiilen **olmuş** — bayrakla mı yoksa klasör taşımasının yan etkisi olarak
mı belirsiz, ama bağlam yeni kimliğe taşınmış ve çalışmış.

### 4.3 Mükerrer oturum burada da doğrulandı

`adbd10b1` iki yol anahtarında birden duruyor: `C--Users-Anj-Desktop-Nar-Ajans---Codex`
ve `D--AI-Nar-Ajans---Codex`. Aynı kimlik, aynı aralık, aynı satır sayısı.
Bu boşlukta **7 kayıt dosyası** ama **6 benzersiz oturum** var.
[[acik-uclar]]'da Nar Ajans'tan devreden bir şüphe olarak duruyordu; playground
tarafında da gerçek olduğu ölçüldü.

## 5. Kare çıkarma ölçümü — mpdecimate elendi, algısal hash seçildi

Kullanıcı *"videonun kaç saniyesinde bir kare alıyorsun"* diye sordu; ölçüldü
(claude 7f10f7a3 · 17.09 05:12). Test: Avenox `eE7WZ0_LPCU`, 10:24–12:24 arası,
iki dakika, 720p.

### 5.1 Mevcut yöntemin gerçek sıklığı

`izle.py` kare **sayısını** sabit tutuyor (varsayılan 24), sıklığı değil:
`adım = aralık / max_kare`, alt sınır 1 sn. Sonuç: tam videoda **41,6 saniyede
bir kare**. Kullanıcının sezgisi ("belki 10 saniyede bir") iyimsermiş.
En iyi hâlde saniyede 1 kare — insanın gördüğünün yirmi beşte biri.

### 5.2 Karşılaştırma

| Yöntem | Kare | Kare arası |
|---|---|---|
| Mevcut (24 sabit) | 24 | 5,0 sn |
| 1 fps ham | 120 | 1,0 sn |
| 1 fps + `mpdecimate` (varsayılan) | 110 | 1,1 sn |
| `mpdecimate` agresif (`hi=64*48:lo=64*24:frac=0.6`) | 86 | 1,4 sn |
| 1 fps + **dhash** (eşik 24) | **29** | 4,1 sn |
| 1 fps + dhash (eşik 32) | 20 | 6,0 sn |

### 5.3 Elenen fikir: mpdecimate

**`mpdecimate` bu videoda işe yaramadı** — 120 kareden 10'unu eledi, en agresif
ayarda 34'ünü. Sebep: video **animasyonlu metin slaytı**, ekran kaydı değil.
Sürekli hareket olduğu için "neredeyse özdeş kare" hiç yok; `mpdecimate` tam da
onu arıyor. Bu, [[arac-izle]]'deki "sahne algılama ekran kayıtlarında çalışmaz"
bulgusunun kardeşi: **piksel tabanlı filtrelerin hepsi video tipine bağlı.**

Tamamen elenmedi — ekran kayıtlarında (gerçekten donuk kareler olan yerde)
denenmeye değer. Ama varsayılan hattan çıkarıldı.

### 5.4 Seçilen: algısal hash (dhash)

120 → 29 kare, yani dört kat daha iyi eleme. Ama sınırı bilinerek kullanılmalı:
dhash **görsel** benzerliği ölçer, **bilgisel** benzerliği değil. Konuşan kafada
kafa oynayınca "farklı" der (bilgi aynıdır); slaytta tek kelime değişince "aynı"
der (bilgi farklıdır).

### 5.5 Asıl bulgu: bilgi görüntüde değil, görüntüdeki yazıda

Karelere bakıldığında içerik animasyonlu **metin** çıktı ("PROMPT MI? CONTEXT
Mİ? — AYNI ŞEY, ARADA FARK YOK"). Bu, doğru eleme ölçütünü değiştiriyor: soru
"görüntü değişti mi" değil, **"ekrandaki yazı değişti mi".** Cevabı OCR verir,
piksel farkı değil. OCR ayrıca bağlam maliyetini kırk kat düşürür: 100 kare
görsel olarak ~130k token, metin olarak ~3k token.

### 5.6 Donanım sınırı

RTX 3060 Ti, **8 GB VRAM** (6,7 GB boşta). Whisper aynı GPU'yu kullanıyor —
yerel bir görsel-dil modeli eklenirse **sıralı** çalışmalı, eşzamanlı değil.
Disk: C **%94 dolu, 14 GB kaldı**; model indirilecekse D'ye (122 GB boş).

## 6. Side chat kaydı diskte yok — kör nokta ölçüldü

17 Eylül'de bir side chat'te uzun bir konuşma yapıldı. O taraftaki örnek kendi
kaydını arayamadı (yazma aracı yoktu); ana oturumdan ölçüldü
(claude 7f10f7a3 · 17.09 22:01):

- Side chat'in oturum kimliği `1bfbca18`. **Bu kimliğe ait `.jsonl` hiçbir
  yerde yok** — proje klasöründe de, `.claude` altında da.
- Side chat'in hipotezi "belki kayıt oturum kapanınca yazılıyor" idi. **Düştü:**
  bu ana oturumun kaydı açıkken yazılıyor (ölçüm anında dosya damgası dakikalar
  öncesiydi). Yani ana oturumlar **canlı** yazılıyor, side chat'ler **hiç**.

**Sonuç: side chat'te ne konuşulursa konuşulsun arşivde iz bırakmıyor.**
`ara.py` bulamaz, `anlam.py` bulamaz, paralel oturum uyarısı göstermez.
Tek taşıma yolu kullanıcının elle aktarmasıdır.

17 Eylül'de bu bir kez yapıldı: kullanıcı side chat'in kaydırmalı ekran
görüntüsünü video olarak alıp `izle.py` hattına soktu; OCR ile 17 kare okundu ve
konuşma eksiksiz kurtarıldı. Yani **`izle.py` aynı zamanda bir kurtarma aracı.**

## 7. Oturum süresi ölçümü — takvim, boşluk, aktif

Model "beş buçuk saattir açık" dedi, kullanıcı sordu, ölçüldü ve **üçü de
farklı çıktı** (claude 7f10f7a3 · 17.09 20:03):

| Ölçü | Değer |
|---|---|
| Takvim süresi (ilk–son damga) | **18,1 saat** |
| 10 dakikadan uzun aralar toplamı | **14,6 saat** |
| Aktif konuşma | **3,5 saat** |
| En uzun tek ara | 7,6 saat (05:52 → 13:28) |

**"Oturum ne kadar sürdü" sorusunun tek cevabı yok.** Hangi ölçünün
kastedildiği yazılmazsa sayı yanıltır — [[yasanan-hatalar]] madde 19 ve 20 ile
aynı kök: etiketsiz sayı.

## 8. Kaynak işaretçisi denetimi — ilk örnekleme

Kalıcı notlarda **32 kaynak işaretçisi** var. İkisi rastgele seçilip ham kayda
karşı denetlendi, **ikisi de doğru çıktı**; denetim başına maliyet ~10 saniye
(claude 7f10f7a3 · 17.09 18:29).

- `(claude 3557db3e · 08.09 17:34)` → o damgada gerçekten mesaj var.
- `iki-ajan-calismasi`'ndaki "kökteki ortak dosya alt klasörlerde otomatik
  yüklenmiyor" iddiası, `16.09 08:38` → kayıtta ölçüm var, iddia uyuşuyor.

Yani bugünkü hata oranı düşük görünüyor. **Ama denetçi şu an sistem değil,
kullanıcıdır** — 17 Eylül'deki dört model hatasının dördünü de kullanıcı
yakaladı. Ekim hedefi "kullanıcı başında durmadan çalışsın" olduğuna göre o
denetçi çekildiğinde yerine bir şey konmalıdır. Bkz. [[acik-uclar]].

## 9. Arayüz "gidip geldi" — sessiz güncelleme, oturum kaydında iz yok

18 Eylül 13:49'da kullanıcı okurken masaüstü uygulaması kapanıp açıldı. Sebep
**otomatik güncelleme**: uygulama bir süre boşta kalınca kendini sessizce
güncelliyor (2.2553.0 → 2.2553.1). Açık oturumu durduruyor, yeniden başlatıyor
ve pencereyi aynı yere geri koyuyor. Toplam kesinti yaklaşık 6 saniye
(claude 5c600e7e · 18.09 13:50).

- **Oturum kaydında (`.jsonl`) hiç iz bırakmıyor.** 13:37 ile 13:50 arasında
  tek satır yok. `SessionStart:resume` bile tetiklenmedi, oturum kaldığı yerden
  sürdü.
- **Görüldüğü yer:** `%LOCALAPPDATA%\Claude\logs\main.log`. Aranacak satırlar:
  `stealth-update`, `beforeQuitForUpdate`, `Version changed since last launch`.
- Kayıp yok. Konuşma, izinler ve bağlam yerinde.

Genel ders: oturum kaydı modelin gördüğünü tutar, **uygulamanın başına
geleni tutmaz.** Arayüzle ilgili bir soruda bakılacak yer `main.log`.

## 10. Omurga mesaj sayıları şişkindi — harness işaretleri

19 Eylül'de omurga filtrelenirken ölçüldü (claude 5c600e7e · 19.09 17:24).
Omurga iki tür harness metnini **kullanıcı mesajı** olarak sayıyordu:

- `isMeta: true` satırlar: skill metni, komut uyarısı, "Continue from where
  you left off". Arşivde 67 tane.
- `[Request interrupted by user]`: reply biçimli mesajlarda her parçanın
  arkasına ekleniyor.

| Oturum | Arşivde yazan | Gerçek | Kesme işareti |
|---|---|---|---|
| `7f10f7a3` | 90 | **68** | 21 (+1 skill) |
| `3557db3e` | 110 | **75** | 33 |
| `5c600e7e` | — | 23 | 16 |

İkisi de `kayit.py`'de filtrelendi. Filtre ortak katmanda olduğu için omurga,
arama ve gece taslağı birlikte düzeldi. Eski arşiv kayıtlarındaki sayılar
**düzeltilmedi**; altlarına denetim notu düşüldü. Kural: denetçi rapor eder,
metni yeniden yazmaz ([[acik-uclar]]).

Codex tarafındaki karşılığı: `AGENTS.md` içeriği, eklenti listesi ve ortam
bilgisi, kullanıcı mesajının ayrı blokları olarak yazılıyor. Blok bazında
atılıyor (codex 01a0b9eb · 19.09 16:47).
