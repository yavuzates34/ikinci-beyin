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

## 11. Codex Desktop kapanan oturumu başka klasöre taşıyor

Desktop, kapatılan oturumu `~/.codex/sessions/` klasöründen
`~/.codex/archived_sessions/` klasörüne taşıyor. `kayit.py` yalnızca
birincisine bakıyordu, bu yüzden **61 oturum** arşiv araçlarına görünmüyordu.
Onarım listesinin kaynağı `01a0ba53` de bunlardan biriydi. İkinci klasör de
taranınca Codex oturumu sayısı 103'ten 164'e çıktı
(claude 5c600e7e · 19.09 20:10).

## 12. Bağlam doluluğu ham kayıttan ölçülebiliyor

- **Codex:** `token_count` olayında `last_token_usage.input_tokens` alanı
  `model_context_window` alanına bölünür (pencere 258.400). `01a0ba74`
  oturumu uyarı almadan %83'e çıktı ve 20:07'de sıkıştırıldı: sayaç
  gösterilmeyen arayüzde erken devrin neden gerektiğinin kanıtı
  (claude 5c600e7e · 19.09 20:28).
- **Claude:** son asistan satırında `usage` alanının `input + cache_read +
  cache_creation` toplamı alınır. Pencere boyutu kayıtta geçmiyor. Kullanıcının
  arayüzde gördüğü yüzdeyle kalibre edildi: 472.650 token yaklaşık %45-50
  gösteriyordu, yani pencere yaklaşık 1 milyon token
  (claude 5c600e7e · 19.09 20:26).

## 13. Codex oturum kimliklerinin ilk 8 hanesi çakışıyor

Codex zaman tabanlı UUID (v7) kullanıyor: aynı dakikada açılan iki oturum aynı
ilk 8 haneyi paylaşıyor. 20 Eylül'de iki denetim oturumu arka arkaya açılınca
ikisi de `01a0bb8e` göründü. Arşivin tamamında ölçüldü: **213 oturumda 24 ayrı
ilk-8 çakışması**, biri dört oturumluk (claude 5c600e7e · 20.09 00:29).

Bu, sistemin her yerini etkiliyordu: kapanış işareti, işaretçi denetimi, gece
taslağı dosya adı ve dedektör hep 8 haneye dayanıyordu. Yanlış oturum kapanmış
sayılabilirdi.

**Düzeltme:** Codex için kısa kimlik 13 hane (`01a0bb8e-de58`), Claude için 8
kalıyor. Kapanış eşleşmesi artık **önek** karşılaştırması, yani eski 8 haneli
işaretler de çalışmaya devam ediyor. İşaretçi deseni iki uzunluğu da tanıyor.

Ayrı bir olgu: 13 hanede de altı çakışma var. Bunlar farklı oturumlar değil,
**aynı oturumun iki kopyası** — Claude tarafında iki proje yolunda (`C:` ve
`D:`), Codex tarafında iki rollout dosyasında. Bu, eskiden beri bilinen
"mükerrer oturum" açığının bu klasörde de doğrulanması; elenmesi yapılmadı.

## 14. Codex Desktop'ta hook'lar otomatik tetiklenmiyor

> **Astra denetim notu (önceki §13'e):** En büyük dosyanın bütün kopyaları
> içerdiği varsayımı yanlış çıktı; üç Codex grubunda 81 farklı mesaj
> okuyucuya görünmüyordu. Parçalar artık birleştiriliyor. Kimlik zincirindeki
> kalan ilk-8 kullanımları da düzeltildi. [[astra-denetim-bulgulari]].
> (codex 01a0bc5c-f1c4 · 20.09 04:22)

20 Eylül'de iki ayrı yoldan ölçüldü (claude 5c600e7e · 20.09 00:38):

- **Kullanıcı testi:** Desktop oturumunda yeni bir turda "hook'lardan sana ne
  geldi" diye soruldu. Cevap: *hiçbir satır gelmedi.* Ham kayıt bunu
  doğruluyor: o turda saat satırı yok.
- **Kayıt tipi:** Daha önce "hook çalıştı" sandığımız harita ve saat satırları
  `custom_tool_call_output` tipinde. Yani onları hook enjekte etmedi; Codex
  modeli `/hooks` mesajına cevaben betikleri **kendisi çalıştırdı**.

Yanıltıcı olan şey: Codex'in cevabı "bu projede etkin ve güvenilir üç hook
grubu var" diyordu. Bu, `.codex/hooks.json` dosyasını okumuş olmasının
sonucudur; enjeksiyonun kanıtı değildir. **Model bir şeyin çalıştığını söylemek
için o şeyin yapılandırmasını okumuş olabilir.**

Claude'un ilk yorumu bu yüzden yanlıştı ve düzeltildi: `/hooks` ekranının
görüntüsü ve modelin ifadesi kanıt sayılmıştı. Kanıt yalnızca ham kayıttaki
enjeksiyon tipidir.

### 14.1 Sebep bulundu: hook'lar güven kaydı bekliyor

Aynı gece ölçüldü (claude 5c600e7e · 20.09 00:48). `codex exec` ile normal
çalıştırmada oturum başı bağlamı **gelmedi**. Aynı komut
`--dangerously-bypass-hook-trust` ile çalıştırıldığında bağlam **anında geldi**:
"BU PROJENIN BEYNI: BEYIN.md…", ve `hook: Stop` satırları da göründü.

Yani adaptör doğru, betikler doğru: eksik olan **proje hook'larına verilmiş
güven kaydı**. Codex bu güveni kendi TUI'sinde `/hooks` ekranından alıyor;
`codex exec` ve Codex Desktop o ekranı açmadığı için hook'lar sessizce
atlanıyor. "Sessizce" önemli: hiçbir uyarı yok, yalnızca bağlam gelmiyor.

Kullanıcının yapması gereken tek şey: terminalde bu klasörde `codex` (TUI)
açıp `/hooks` ile güven vermek. Sonra Desktop'ta ve `exec`'te de çalışması
beklenir — bu **ölçülmedi**.

### 14.2 Güven verildi: Desktop ve normal `codex exec` çalışıyor

Kullanıcı TUI'de proje hook'larına güven verdi. Hemen sonraki yeni Codex
Desktop oturumunda `SessionStart` çıktısı "BU PROJENIN BEYNI: BEYIN.md…",
ilk kullanıcı mesajında da `UserPromptSubmit` saat çıktısı otomatik geldi.
Ham kayıtta ikisi de `role=developer` ve `content_item_kinds =
["hooks.additional_context"]`; önceki yanlış pozitiflerdeki
`custom_tool_call_output` değiller (codex 01a0bbc6-b6f6 · 20.09 01:28).

Ayrıca güven-atlatma bayrağı olmadan yeni bir `codex exec --json` oturumu
açıldı. Aynı iki çıktı yine ham kayıtta `hooks.additional_context` olarak
görüldü; model başlangıç metninin ilk satırını doğru aktardı
(codex 01a0bbcc-8818 · 20.09 01:32).

Sonuç: `.codex/hooks.json`, Windows adaptörleri ve kalıcı güven kaydı hem
Desktop hem CLI için çalışıyor. `SessionStart` ile `UserPromptSubmit` canlı
doğrulandı. `PreCompact` ve Codex'te %50/%70 eşiğinin gerçek uyarısı henüz
canlı ölçülmedi; yapılandırmanın varlığı onların gerçekleştiğinin kanıtı değil.

## 15. Astra alt ajan olarak çağrılamıyor: CLI sürümü yetmiyor

20 Eylül 00:49'da denendi ve ölçüldü (claude 5c600e7e · 20.09 00:49).
`codex exec -m gpt-6-astra` çağrısı API'den şu hatayı aldı: *"The 'gpt-6-astra'
model requires a newer version of Codex."* Kurulu CLI 0.150.1; Codex Desktop
ise 0.155-alpha. Ayrıca CLI "model metadata bulunamadı" uyarısı veriyor.

Sonuç: **Astra yalnızca Codex Desktop'tan çalıştırılabiliyor.** Claude, Astra'yı
alt ajan olarak çağırıp üçüncü göz denetimini kendi başına yaptıramaz; o tur
kullanıcının Desktop oturumunda yapılmak zorunda. `gpt-5.6-sol` CLI'da
çalışıyor, iki denetim turunu o yaptı.

Bu, 16 Eylül'de Nar Ajans'ta ölçülen "model adı değişti, kurulu CLI yeni modeli
çalıştıramadı" bulgusunun hâlâ geçerli olduğunu gösteriyor: **model adı
varsayılmaz, sürüm uyumu ölçülür.**


> **Güncelleme (21.09 06:53): bu bulgu artık geçerli değil.** CLI `0.150.1`'den
> `0.155.1`'e güncellendi ve `codex exec -m gpt-6-astra` **çalıştı**
> (oturum `01a0c21a`, 20.624 token, istenen tek kelimeyi döndürdü). Yani Astra
> artık alt ajan olarak çağrılabiliyor; üçüncü göz denetimi için kullanıcının
> Desktop oturumu **zorunlu değil**. Bulgunun kendisi silinmedi: 20.09'daki
> ölçüm o günün doğrusuydu ve dersi hâlâ geçerli — *model adı varsayılmaz,
> sürüm uyumu ölçülür.* Bu güncelleme de o dersin ikinci yarısı: **ölçüm
> bayatlar, yeniden ölçülür.**
>
> **Yeni bulgu — denetçinin varsayılanı yanlış yönde.** Aynı çağrının başlığı
> `approval: never`, `sandbox: danger-full-access` gösterdi. Yani alt ajan
> olarak çağrılan Astra, onay sormadan tam disk erişimiyle çalışıyor.
> Denetçinin yazma yetkisi olmamalı; çağrı yapılırken sandbox salt okunur
> kısıtlanmalı. Henüz uygulanmadı.
>
> **Yan gözlem (ölçülmedi, takip edilecek):** aynı çağrıda `UserPromptSubmit`
> hook'u günlükte **iki kez** göründü (`hook: UserPromptSubmit` ×2, ardından
> `Completed` ×2). Tek tetiklemenin çift kaydı mı, gerçek çift çalıştırma mı
> ayrılmadı.
> (claude 96517e26 · 21.09 06:53)

## 16. Gece derleyicisi tetikleniyor ama konsolu kapanınca ölüyor

20 Eylül 01:50'de ölçüldü (claude 96517e26 · 20.09 01:50). Bu gecenin
dosyalarının commit'siz kalması "cron çalışmadı" sanılmıştı; Görev
Zamanlayıcı'nın kendi kaydı tersini söylüyor:

```
LastRunTime        : 20.09.2026 00:30:01
LastTaskResult     : 3221225786        # 0xC000013A = STATUS_CONTROL_C_EXIT
NumberOfMissedRuns : 0
NextRunTime        : 21.09.2026 00:30:00
```

**Görev saatinde tetiklendi, atlanan çalışma yok.** Dönüş kodu
`0xC000013A`, sürecin Ctrl+C ya da konsol penceresinin kapanmasıyla
sonlandırıldığını söyler — zaman aşımı ya da Python hatası değil.
Görevin çalışma limiti PT15M ve çalışma 00:30:01'de başladı; derleme
saniyeler sürer, yani limite de takılmadı.

**Sebep, görevin nasıl kurulduğunda:** `Principal.LogonType = Interactive`,
`RunLevel = Limited`. Görev kullanıcının açık oturumunda, `derle-gece.cmd`
üzerinden **görünür bir konsol penceresi açarak** çalışıyor. O pencere
kapanırsa süreç ölür. Derleme sırası da bunu doğruluyor: `son-calisma.json`
(başlangıç) ve `derleme/gunluk/2026-09-20.md` yazıldı, ardından gelen log
satırı ve **git commit + push adımı hiç çalışmadı**.

`derleme/derleyici.log` aynı imzayı daha önce de taşıyor: 18.09 çalışmasının
yerinde bir `^C` var ve o gecenin log kaydı hiç yok. Yani son dört gecenin
ikisi bu şekilde yarıda kalmış:

| Gece | Sonuç |
|---|---|
| 17.09 00:30 | temiz, commit + push tamam |
| 18.09 00:30 | log'a yazılmamış, `^C` |
| 19.09 00:30 | commit atıldı, push başarısız (borç sonradan kapandı) |
| 20.09 00:30 | başladı, `0xC000013A` ile kesildi |

**Neden önemli:** [[BEYIN]] "her gece otomatik commit + push" diyor; ölçüm son
üç gecenin birinde tuttuğunu gösteriyor. Ayrıca gece taslağı zincirinin
(onarım listesi madde 12) "gerçek koşulda çalıştı" kanıtı **elle tetiklenmiş**
bir çalışmaya dayanıyor (20.09 00:45); zamanlanmış yolun kendisi henüz uçtan
uca tamamlanmadı.

**Kullanıcının gözlemi ve düzeltmesi:** kullanıcı o saatlerde Codex'in kullanım
limiti dolduğu için 00:16'ya kadar beklemiş, 00:16–00:30 arası ve sonrasında
aktif çalışmıştı; "o yüzden cron çalışmamış olabilir" diye tahmin etti
(kullanıcı, 20.09 01:52). Ölçüm tahmini düzeltiyor: **aktif oturum cron'u
engellemedi, açılan pencereyi öldürdü.** Mekanizma ters yönde.

**Önerilen düzeltme (uygulanmadı, sistem ayarı kullanıcıya ait):** görevi
"kullanıcı oturum açmasa da çalıştır" (S4U) olarak kurmak ya da pencereyi
gizlemek. Konsol penceresi olmadığı sürece kapatılamaz. Değişiklik yapılırsa
ertesi gece `derleme/derleyici.log` ve `LastTaskResult` ile doğrulanmalı.

> İlgili: [[gece-derleyicisi]] · [[acik-uclar]] · [[2026-09-19-sunum-onarim-listesi]]

> **Astra denetim notu (§16):** “git commit + push adımı hiç çalışmadı”
> cümlesinin commit kısmı çürütüldü: `67779e9` 20.09 00:30:05'te atılmış.
> Push sonucu ölçülmedi. Konsolu kullanıcının kapattığı da kanıtlanamaz.
> Üç model çağrısı toplam 45 dakika sürebildiğinden “derleme saniyeler sürer”
> genel süre garantisi değildir. Görev kullanıcı onayıyla düzeltildi; gece
> tetiklemesi bekleniyor. [[astra-denetim-bulgulari]] · [[2026-09-20-astra-kontrol]].
> (codex 01a0bc5c-f1c4 · 20.09 04:26)

## 17. Sıkıştırma özeti omurgaya "kullanıcı mesajı" olarak giriyor

Kapanış ritüelinin dayanağı `omurga.py`: ham kayıttan **yalnız kullanıcının
gerçek mesajlarını** çıkarır, çünkü ritüel hatırlamaya değil okumaya
dayanmalıdır. Ölçüm, bu garantinin sıkıştırmadan sonra bozulduğunu gösteriyor.

21.09 02:42'de elle `/compact` çalıştırıldı. PreCompact anlık görüntüsü
(sıkıştırmadan hemen önce, aynı oturum):

```
41 mesaj, 19.5 KB
```

Sıkıştırmadan sonra aynı oturumun omurgası:

```
43 kullanici mesaji, 44.2 KB omurga
```

Aradaki fark tek bir girdiden geliyor: 42 numaralı "mesaj", uygulamanın
oturuma enjekte ettiği **kendi sıkıştırma özeti** (`This session is being
continued from a previous conversation…`). Omurga bunu kullanıcı konuşması
sayıyor: ~24 KB, yani omurganın yarıdan fazlası.

**Neden önemli.** Bu, `AGENTS.md`'nin özellikle engellemek istediği hal:
modelin kendi kayıplı özeti, kullanıcının sözü gibi görünüyor. Sıkıştırma
sonrası kapanış yazan bir ajan "ham kaydı okudum" derken aslında bir özeti
okumuş olur ve bunu ayırt edemez. Ayrıca özet, önceki turda düzeltilmiş
yanlış iddiaları da taşıyabilir — bu oturumda taşıdı.

**Düzeltme — UYGULANDI (21.09 07:15).** Kayıtta ayırt edici alan aranmalı
demiştim; alan varmış: sıkıştırma özeti satırı `isCompactSummary: true` (ve
`isVisibleInTranscriptOnly: true`) taşıyor. Metin desenine hiç bakılmadı.
Süzgeç `kayit.py::_claude_mesajlari` içine kondu — ortak katman olduğu için
`omurga.py`, `ara.py`, `anlam.py` ve `oku.py` birlikte düzeldi. Aynı oturumun
omurgası **43 mesaj / 44,2 KB** iken, düzeltmeden sonra 23 mesaj daha
eklenmesine rağmen **66 mesaj / 29,1 KB**. Sıkıştırmanın kendisi kaybolmuyor:
PreCompact zaten `derleme/omurga-anlik/` altına anlık görüntü yazıp devir
kutusuna not bırakıyor.

Regresyon testi: `test_compact_summary_is_not_counted_as_user_message`.
Testin gerçekten koruduğu ölçüldü — süzgeç geçici olarak kapatılıp test
çalıştırıldı, **düştü**; süzgeç geri konunca 29/29 geçti. (Boş test yazmamak
için: geçmeyen bir testin geçtiğini görmek, hiç test yazmamaktan kötüdür.)
Tam otomasyon planında eşik ritüeli sıkıştırmadan **önce** çalışacağı için
bu kusur oradaki ana yolu bozmaz, ama yedek yolu (sıkıştırma sonrası yazma)
bozar.
(claude 96517e26 · 21.09 02:48)

> İlgili: [[kapanis-ritueli]] · [[2026-09-21-tam-otomasyon-plani]] ·
> [[2026-09-21-otomasyon-lab-ve-vds]] · [[acik-uclar]]

## 18. Lab VDS'i: ilanla ölçüm arasındaki fark

AltunHOST SSD VDS-4, `89.144.20.133`, Ubuntu 24.04 LTS. Kurulum ve ölçüm
21.09 03:01–03:23 arası, SSH üzerinden.

| Ne | Ölçülen | İlanla ilişkisi |
|---|---|---|
| CPU | Xeon E5-2699 v4 @ 2,2 GHz, 4 vCPU | Çekirdek sayısı doğru; yonga **2016 Broadwell** |
| RAM | 6.067.600 kB | 6 GB iddiasıyla uyumlu |
| Disk | 90 GB, dönmeyen. Yazma 580 MB/s, okuma 1,1 GB/s (`oflag=direct`) | NVMe sınıfı **doğrulandı** |
| Ağ | 106 MB/s (~850 Mbit/s, cachefly) | Hızlı |
| Gecikme | 10 ms (kullanıcının PC'sinden, 10 paket, %0 kayıp) | İstanbul iddiasıyla tutarlı |
| Swap | 1,9 GB kurulu geldi | — |

**"Ayrılmış RAM" iddiası doğrulanamadı.** VDS'i VPS'e tercih etme
gerekçelerimden biri şuydu: *"VDS'te RAM kullanılmasa bile kullanıcıya
atanır"* (claude 96517e26 · 21.09 01:05). Makinedeki ölçüm bunu
desteklemiyor:

```
vmware-toolbox-cmd stat memres    → 0 MB          (rezervasyon tanımlı degil)
vmware-toolbox-cmd stat memlimit  → 4294967295 MB (sinir yok)
lsmod | grep balloon              → vmw_balloon yuklu, su an 0 MB geri alinmis
```

Yani hipervizör tarafında bize ayrılmış bellek rezervasyonu **yok** ve balon
sürücüsü yüklü. Şu an kimse RAM geri almıyor, ama almasını engelleyen bir şey
de yok. Tek kaçamak yorum: aracın `memres`'i okuyamayıp 0 basması — ancak
`memlimit` gerçek değer döndürdüğü için zayıf ihtimal. **Karar iptal
edilmedi** (lab yükü hafif, 5,4 GB boşta), ama gerekçelerden biri düştü.

**Teslim edilen güvenlik durumu.** Sunucu `PermitRootLogin yes` ve parolayla
SSH **açık** halde geldi; çekirdek `6.8.0-31` (GA, yamasız) idi. Sağlayıcı
varsayılanı güvenli değil, kurulumdan sonra sıkılaştırma şart.

**`apt upgrade` çekirdeği yükseltmez.** Düz `upgrade` yeni paket kurmayı
gerektiren yükseltmeyi atlar; `6.8.0-31` → `6.8.0-139` ancak `full-upgrade`
ile geldi. Ara raporumda "çekirdek yamalandı" dedim, yanlıştı; `uname -r`
ölçümü düzeltti. Ders: yükseltme komutunun çıktısı değil, **sürümün kendisi**
ölçülür.
(claude 96517e26 · 21.09 03:23)

> İlgili: [[2026-09-21-tam-otomasyon-plani]] · [[2026-09-21-otomasyon-lab-ve-vds]] · [[acik-uclar]]

## 19. Jev ve görünürlük ayrımı: Avenox'tan alınan tasarım

**Jev nedir (ölçülmedi, satıcı ve basın iddiası).** TypeSafe AI'ın 15.09.2026'da
çıkardığı "System One" modeli. Paragraf üretmez; dağınık program durumunu alıp
**tipli, olasılıklı karar** döndürür. İddialar: sınır modellere göre 40–200 kat
hız, milyon girdi token'ı 0,042 $, çıktı ücretsiz, "matematiksel olarak
halüsinasyon ve tip hatası üretemez". Son iddia dikkatli okunmalı: çıktı şemaya
zorlandığı için **geçersiz tipte** bir şey üretemez; bu yanılmaz olmak değildir.
Kurucu CEO Diogo Almeida, InstructGPT ortak yazarı.

**Neden bizi ilgilendiriyor.** Planımızdaki üç iş — örneklemeli içerik
denetimi, sağlık/eskime alarmı, eşik ritüelinde "bu kalıcı mı" ayıklaması —
tipli karar işidir. Kullanıcının itirazı buydu: *"10 gün boyunca hiç ikinci
beyni kullanmadım, boşu boşuna Claude kotamdan mı yiyecek?"* Ucuz bir karar
modeli bu hesabı değiştirir.

**Avenox'un çit tasarımı (okundu, `docs/v3/JEV.md`, 258 satır).** Asıl
alınacak şey modelin kendisi değil, etrafındaki çit: varsayılan **kapalı**;
üç mod `off/shadow/on` (gölge = çalışır, sonucu etkilemez, yani kalibrasyon);
özellik bazlı anahtar; `BEYIN_JEV_DISABLE=1` kill-switch; ve çağrı kaydı
**içeriksiz** — sorgu metni, aday metni, yanıt ve anahtar yazılmıyor, yalnız
sayaç. `--key` seçeneği bilerek yok. Bir denetçiye güvenmeden önce gölge
modunda çalıştırıp haklılığını ölçmek, bizim "denetçi rapor eder, düzeltmez"
kuralımızın bir üst basamağı.

**Kurulan ayrım (kullanıcı kararı, 21.09 05:35).** Avenox notları
private/internal/public olarak ayırıyor ve `private` olanı sağlayıcıya hiç
göndermiyor. Aynı ayrım bizde de kuruldu: `gorunurluk.json` +
`araclar/gorunurluk.py`. Düzeyler `ozel` / `ic` / `acik`.

Tasarımın tek önemli kararı: **etiket dosyaların içine gömülmedi.** Proje
bilerek şablondan kaçınıyor ve 42 dosyanın hiçbirinde frontmatter yok. Etiket
ayrı manifestoda durur, bedeli bayatlamadır, ve bedeli kabul edilebilir kılan
kural şudur: **eşleşmeyen her şey `ozel` sayılır.** Manifesto bayatlayınca yeni
dosya sessizce sızmaz, gereksiz yere kapalı kalır ve rapor edilir. Hata yönü
güvenli tarafta. Bu yüzden `notlar/*` gibi toplu desen kullanılmadı — toplu
desen yeni dosyayı da kapsar ve varsayılanı bozar.

İlk tarama: **63 ozel · 48 ic · 4 acik**, 4 etiketsiz. Doğrulandı:
`notlar/kullanici-baglami.md` → `ozel` (modele gitmez),
`notlar/olculmus-bulgular.md` → `ic` (lab IP'si burada geçtiği için
yayımlanamaz), `AGENTS.md` → `acik`, olmayan bir dosya → `ozel`.

**Yan bulgu.** Tarama, kökte **`2026-09-17.md`** adlı boş ama git'te takipli
bir dosya buldu. `AGENTS.md` kök dizinde günlük dosyası açmayı yasaklıyor.
Silinmedi; karar kullanıcının.
(claude 96517e26 · 21.09 05:35)

## 20. Görünürlük kapısının sıfır çağıranı vardı — ve sızıntı bizdeydi

**Ölçüm (21.09 07:52).** `disari_cikabilir()` fonksiyonunun kasada kaç çağıranı
olduğu sayıldı:

```
grep -rn "gorunurluk" --include=*.py .   ->  yalnız gorunurluk.py'nin kendisi
```

**Sıfır.** Oysa `AGENTS.md` şunu yazıyordu: *"Model çağıran her yol
`gorunurluk.disari_cikabilir()` üzerinden geçer."* Kural yazılıydı, kurulu
değildi. Bu, §17'deki dersin aynısı: anlatı kurulunca kayda bakmak unutuluyor.

**Asıl bulgu: sızıntı Avenox'ta değil, bizdeydi.** Kendi kodumuzda modele
içerik gönderen tek yol arandı. `anlam.py` yerel ONNX ile gömüyor (fastembed,
ağ yok). Geriye tek yol kaldı: `gece_kayit.yazdir()` →
`subprocess.run(["claude", "-p", ...], input=istem(o, omurga))`. İstemin
içindekiler:

| Parça | Düzey | Durum |
|---|---|---|
| `AGENTS.md` | `acik` | sorun yok |
| `BEYIN.md` | `ic` | sorun yok (`hedef=model`) |
| **tam omurga** (ham kullanıcı + model mesajları, 600 KB'a kadar) | **`ozel`** | **çıkmamalıydı** |

Omurganın kaynağı ham oturum kaydı; o dosya proje kökünün dışında durur, yani
`duzey()` ona `ozel` der. `derleme/**` altındaki anlık görüntüleri de manifesto
açıkça `ozel` sayıyor ("omurga anlık görüntüleri ham kullanıcı mesajı taşır").
Yani sistem, kendi yazdığı kuralı her gece çiğniyordu — 19.09'dan 21.09'a.
Avenox kurulmasaydı da sızıntı duruyordu.

**Kuralla davranış birbirinden habersiz konmuştu.** Etiketler 21.09 05:35'te
kullanıcı kararıyla girildi; gece yazıcısı 19.09'da yazıldı. İkisini kimse
karşılaştırmadı, çünkü karşılaştıracak kod yoktu. *Sözleşmenin ihlali,
sözleşmeyi soran bir kod olmadan görünmez.*

### Kurulan: üç katman, güçten zayıfa

`araclar/disari.py`.

1. **Kapı** (`dene`, `kapi`). Gönderimdeki **bütün** yolları birden denetler —
   tek tek değil, çünkü istem bölünemez: bir dosya bile çıkamıyorsa istemin
   tamamı çıkamaz. `gece_kayit.yazdir()` artık ilk iş bunu soruyor.
2. **Yansıma** (`yansit`). Yabancı araca kasanın yolu değil, yalnız
   çıkabilenlerden oluşan bir kopya verilir. **Tek taşıyıcı katman bu:**
   diğer ikisi rica eder, bu bayta çevirir — yasak içerik orada yoktur.
   Ölçüldü: `hedef=model` → 54 dosya alındı / 64 bırakıldı; `hedef=yayin` →
   4 / 114. Kasanın **içine** yazmayı reddeder (yazsa sızıntı kapanmaz, bir
   kopya daha olurdu) ve yazdıktan sonra çıktıyı yeniden tarayıp her dosyanın
   kapıdan geçtiğini doğrular; geçmeyen varsa çıktıyı siler.
3. **Bulucu** (`denetle`). Herhangi bir ağaçta `ozel` içeriğin izini arar:
   birebir kopya (sha256), **imza satırı** ve yol. İmza = kasanın tamamında
   **yalnız bir kez** geçen, 60 karakterden uzun satır; tek kez geçme şartı
   şablon/başlık gürültüsünü tanım gereği eler. 52 `ozel` dosyadan 180 imza
   çıktı. Parçalayarak indeksleyen aracı da yakalar, çünkü parça satırı
   bütün taşır.

### Astra'nın İ2 deneyi kalıcı test oldu

Astra 21.09 07:26'da bir kez ölçmüş ve bitmişti. Şimdi her test koşusunda
tekrar koşuyor (`SizintiTests`, 39/39). En kritik testi **negatif kontrol**:
`test_bulucu_yabanci_indekste_yakalar`. Bulucunun "TEMİZ" demesi, ancak bulucu
gerçekten bulabiliyorsa bir şey ifade eder — o test olmadan diğerlerinin hepsi
boş yere geçerdi.

Testlerin koruduğu doğrulandı: üç sabotaj denendi, üçü de yakalandı.
Yansıma süzgeci kapatıldı → 2 test düştü; imza çıkarımı boşaltıldı → negatif
kontrol düştü; kapı `gece_kayit`'ten çıkarıldı → kapı testi düştü. Her seferinde
dosya birebir geri yüklendi (`diff` ile doğrulandı).

### Ne kapanmadı

Üç katman da, bir aracın kasayı **kendi başına taramasını** engellemez. Onu
ancak dosya izinleri engeller. Lab'de `avenox` kullanıcısının sudo'su yok; aynı
ayrım yerelde kurulmadı, çünkü kendi araçlarımızı da kilitlerdi. Bulucu da
özetlenmiş, çevrilmiş ya da yeniden yazılmış içeriği yakalamaz — bu bir **kanıt**
aracıdır, garanti değil.

**Açık karar kullanıcıda:** gece yazıcısı şu an kapalı. Ya ham oturum kaydı
`ic` ilan edilecek, ya da gece taslağı üretilmeyecek. [[acik-uclar]] madde 8.
(claude 96517e26 · 21.09 07:57)

## 21. Y1 portu: tasarımım kırıldı, iki kusur doğrulandı

Karar (b)'nin ilk portu. Ben iki kusur ölçtüm, bir tasarım önerdim, Astra
tasarımı kırdı. Sıra doğruydu: **kod yazılmadan önce kırıldı.**

### Doğrulanan iki kusur

**K1 — borç, teslim edilmeden önce siliniyor.** `devir.al()`
(`araclar/devir.py:68–89`) mesajı `pop` edip diske yazar; teslim *sonra* olur.
Arada korumasız pencere var. Yedek yol bunu kapatmıyor: `oturum_basi.py:125`
aynı `al()`'i çağırıyor, yani kuyruğun ikinci **tüketicisi**, kurtarıcısı değil
(claude 96517e26 · 21.09 08:11; Astra [İ4] DOGRULANDI).

**K2 — bayat mesaj sessizce yok ediliyor.** İki aşamalı: `_oku()` 12 saatten
eskiyi süzüp **görünmez** yapar, kalıcı kayıp **sonraki yazmada** olur. 13
saatlik sentetik borçla ölçüldü: `_oku()` → `[]`, diskte girdi duruyor; sonraki
`birak()` çağrısında girdi gitti, `stderr` boş (Astra [K2] DOGRULANDI).

### Kırılan tasarım — ve neden kırıldı

Önerim şuydu: `al()` pop etmesin, işaretlesin; `print`+`flush` başarılıysa
`onayla()` çağrılsın; onaylanmayan yeniden teslim edilsin.

**[İ7] ÇÜRÜTÜLDÜ.** İki gerçek Windows süreci bariyerle sıralandı ve **aynı
talimat iki ayrı stdout akışına çıktı** (`delivered_output_lines=2`), üstelik
son durum dosyası geçerli JSON ve `done=1` iken. Sıra: A kilitler → damgalar →
bırakır → basar; B kilitler → hâlâ onaysız aynı girdiyi damgalar → bırakır →
basar; A onaylar; B onaylayacak bir şey bulamaz. **Damga kilit değildir.**
`os.replace` atomik olsa bile `oku → sahiplen → dışarı yaz → onayla` bütünü
atomik olmaz.

**[İ5] ÖLÇÜLEMEDİ.** "Yeniden teslim zararsızdır" diyordum. PreCompact mesajı
bilgi değil **emir**: kaydı yaz, notlara terfi et, haritayı güncelle. Ekleyerek
çalışan temsili bir tüketicide tek olgu için iki terfi satırı oluştu. Astra bunu
gerçek modele mal etmeyi reddetti — doğru davranış; ama "zararsız" da
kanıtlanmadı.

**Print/flush onayı yanlış katmanı onaylıyor.** Çıktı baytlarını tüketip modele
hiç eklemeyen bir alıcı kuruldu: gönderici `exit=0, done=1` gördü,
`simulated_model_context_messages=0`. Yani K1'in "harness çıktıyı yok sayar"
ayağı flush onayıyla **kapanmıyor**.

**Kök hata bende.** Brief'imin içinde Avenox'un ilkesini kendim yazmıştım:
*"borç, denemeyle değil, sonucun gözlenmesiyle kapanır."* Sonra denemeye dayalı
bir mekanizma tasarladım. Gözlemlediğim şey (flush) ile umursadığım şey (iş
yapıldı mı) arasında üç katman var.

### Adlandırma düzeltmesi: N6 ≠ Y1

Plan `:102`'de **N6** bizim tur içi ölçüm açığımız (20.09 Astra denetimi).
`rehber/astra-lab-denetimi.md:102`'deki **Y1** Avenox'un kuyruk telafisi.
İkisini birbirine karıştırmıştım. **[İ6] ÇÜRÜTÜLDÜ:** kuyruk, hiç
tetiklenmeyen işi kendiliğinden başlatamaz. Kullanıcı mesaj yazmadan süren araç
döngüsünde `al/onayla` hiç çalışmaz; boş kuyruğa yeni eşik borcu üretemez.
Sonraki bir hook önceden **kaydedilmiş** borcu telafi eder; yapılmamış ölçümü
yapılmış hâle getiremez. Ayrıca planın `:341–346` telafi kuyruğu ağ/push
borçlarını da kapsıyor; yalnız devir mesajı portu o işi bitirmez.

### Tasarımın ayrıca kapatmadığı üç yer

- **Eşik uyarısı ayrı borç.** `baglam.py:190–199` seviye durumunu uyarının
  çıktı sonucundan **önce** kaydediyor. İlk uyarı teslim edilmezse devir
  mesajını yeniden denemek bunu telafi etmez; seviye zaten yanmış sayılıyor.
- **Sınırlı done listesi yeni sessiz kayıp yaratır.** Raporlanmamış başarısız
  borç, daha yeni kayıtlar tarafından kapasite dışına atılabilir. Raporlanmayı
  bekleyen borç ile temizlenebilir teslim geçmişi aynı saklama politikasına
  bağlanamaz.
- **Bütün tüketiciler birlikte taşınmalı.** `devir.main` ve
  `oturum_basi.main` aynı protokole geçmezse yedek yolun kayıp penceresi kalır.

(claude 96517e26 · 21.09 08:24)

## 22. Y2 maruziyeti ölçüldü: çakışma gerçek, koruma kazara

Y2 (iyimser kilit) portunun gerekli olup olmadığına karar vermek için önce
**maruziyet** ölçüldü. Soru: iki ajan gerçekten aynı anda aynı dosyaya
yazıyor mu, yoksa risk teorik mi?

### Çakışma: 11 pencere, en uzunu 13,5 saat

Arşivdeki 20 oturumun her biri için `[ilk mesaj, son mesaj]` penceresi
çıkarıldı ve kesişimler sayıldı (`y2_cakisma.py`, çalışma dizininde):

```
20 oturum penceresi | claude 7, codex 13
CAPRAZ cakisma (claude <-> codex): 11
  13:25:30 | 20.09 04:10 | claude 96517e26 <-> codex 01a0bc5c-f1c4
   0:50:51 | 19.09 19:16 | claude 5c600e7e <-> codex 01a0ba74-3f5f
   0:35:37 | 19.09 18:40 | claude 5c600e7e <-> codex 01a0ba53-479d
   ...
AYNI kaynak cakismasi: 5 (en uzunu 5 gun 9:38)
```

### Ortak yazma yüzeyi: 48 dosya

82 commit, `Co-Authored-By: Claude` taşıyanla taşımayan diye ayrıldı (62 / 20)
ve dokundukları dosyalar karşılaştırıldı. **İkisinin de yazdığı 48 dosya var**,
üstelik en sıcak olanlar:

| dosya | claude | codex |
|---|---|---|
| `BEYIN.md` | 28 | 8 |
| `notlar/acik-uclar.md` | 23 | 6 |
| `notlar/olculmus-bulgular.md` | 14 | 4 |
| `notlar/kapanis-ritueli.md` | 8 | 3 |
| `araclar/derle.py` | 6 | 4 |

Yani maruziyet teorik değil: uzun çakışma pencereleri ve yüksek trafikli
ortak dosyalar birlikte duruyor.

### Kazara koruma — ve nerede bitiyor

Beklemediğim şey: bizi şu an koruyan şey tasarlanmış değil, **düzenleme
aracının biçimi.** Dize değiştiren bir düzenleme (`Edit`), hedef metin
değişmişse **başarısız olur** — yani iyimser kilidin yaptığı işi kazara yapar.
Ama bütün dosyayı yazan bir yol (`Write`, ya da `read_text()` → `write_text()`
deseni) hiçbir şey sormaz ve sessizce ezer. Bu oturumda ben o deseni defalarca
kullandım.

**Koruma araca bağlı, sözleşmeye değil.** Ajan hangi yolu seçerse o kadar
korunuyoruz.

### Ne ölçülemedi

Geçmişte gerçekten bir kayıp güncelleme olup olmadığı **geriye dönük
ölçülemez**: kaybolan yazma hiçbir yerde iz bırakmaz, git yalnız commit'lenmiş
hâlleri görür. Bu yüzden "olmadı" da denemez, "oldu" da. Y2 kararı arkeolojiyle
değil, ileriye dönük bir deneyle verilmeli: iki ajanın aynı dosyayı
çakışan pencerede güncellediği kontrollü bir koşu.

**Şimdilik hüküm yok.** Maruziyet ölçüldü ve büyük; koruma kısmi ve kazara.
Port gerekli mi sorusu Astra'ya açık. (claude 96517e26 · 21.09 08:31)

> İlgili: [[2026-09-21-tam-otomasyon-plani]] · [[acik-uclar]] · [[ikinci-beyin-mimarisi]] · [[2026-09-21-otomasyon-lab-ve-vds]]
