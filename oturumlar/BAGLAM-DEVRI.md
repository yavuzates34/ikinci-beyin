# Bağlam Devri — Video Anlama Altyapısı + Oturum Belleği Tasarımı

> Bu dosya, 30 Ağustos 2026 tarihli bir Claude Code oturumunun devridir.
> Başka bir modele soğuktan bağlam vermek için yazıldı. İçindeki sayılar
> tahmin değil, o oturumda **ölçülmüş** değerlerdir — yeniden ölçmeye gerek yok.

---

## 1. Ortam

| | |
|---|---|
| Makine | Windows 11 Pro, 16 çekirdek, **NVIDIA RTX 3060 Ti (8 GB)** |
| Diskler | `C:` ~12 GB boş (**dar**), `D:` ~167 GB boş |
| Kural | Büyük dosyalar/modeller **D:'ye** kurulur, C: kullanılmaz |
| Çalışma klasörü | `C:\Users\Anj\Desktop\playground` (deneme alanı) |

Kurulu araçlar ve yerleri:

- `ffmpeg` / `ffprobe` 9.0.1 — winget (Gyan.FFmpeg), PATH'e eklendi ama **yeni kabuk gerektirir**
- `yt-dlp` 2026.08.19 (eski sürüm 403 hatası veriyordu, güncellendi)
- `faster-whisper` 1.2.1 + `ctranslate2` 4.8.1
- Whisper `large-v3` modeli → `D:\AI\whisper` (2.9 GB)
- cuBLAS/cuDNN → `D:\AI\pylibs` (2.0 GB, `pip install --target` ile D'ye zorlandı)
- `rclip` 3.3.0 (CLIP tabanlı yerel görsel arama, ayrı araç)

---

## 2. Kurulan araç: `izle.py`

Amaç: bir modelin video "izleyebilmesi". Model videoyu okuyamaz; video
**kareye ve metne** çevrilir, model o formatları zaten okuyabilir.

```bash
# 1. AŞAMA — tarama: sadece ses çekilir, zaman damgalı transkript üretilir
python izle.py <kaynak> --basla 0:00 --bitir 16:39

# 2. AŞAMA — yakın bakış: dar aralığın videosu alınır, kare çıkarılır
python izle.py <kaynak> --basla 4:00 --bitir 6:00 --kare

# ORTAM SINAMASI — neyin eksik olduğunu söyler
python izle.py --kontrol
```

`<kaynak>` yerel dosya yolu **veya** YouTube linki olabilir.

Yan dosya: `sozluk.txt` — Whisper'a `initial_prompt` olarak verilir, Türkçe
anlatım içindeki İngilizce terimleri tanıması için.

### Neden iki aşama

Kare sayısı sabittir (varsayılan 24), video uzunluğuyla artmaz. Yani:

| Aralık | Kare | Kare arası |
|---|---|---|
| 1 dk | 24 | 2.5 sn |
| 5 dk | 24 | 12 sn |
| 40 dk | 24 | 100 sn |

Uzun aralıkta kareler işe yaramayacak kadar seyrekleşir. Doğru kullanım:
**önce transkript** (ucuz, tamamını kapsar) → ilgili zamanı bul → **sonra o dar
aralığın kareleri**. Görseller metnin kat kat üstünde bağlam yer kaplar.

---

## 3. Ölçülmüş bulgular

### 3.1 YouTube indirme stratejisi

| Yöntem | Boyut | Süre |
|---|---|---|
| Ses, tamamı (16:39 video) | 15 MB | **2 sn** |
| Ses, kırpılmış (100 sn) | 1.7 MB | 55 sn |
| Video, tamamı (16:39) | 54 MB | ~5 sn |
| Video, kırpılmış (100 sn) | **3.7 MB** | 55 sn |

Kırpma süresi **kaynak uzunluğundan bağımsız** (sadece dilim uzunluğuna bağlı);
tam indirme kaynakla doğru orantılı büyür. Başabaş noktası ≈ **1 saatlik video**.

**Uygulanan kural:** ses her zaman tam indirilir; video 60 dakikadan uzunsa
kırpılarak indirilir. Eşik `IZLE_KIRPMA_ESIGI` ile ayarlanır.

### 3.2 Whisper model karşılaştırması (aynı ses, aynı sözlük)

`small` → `large-v3` geçişinde düzelenler:

| `small` | `large-v3` |
|---|---|
| "cpt 5.5" | "GPT 5.5" |
| "kenar altyapımda" | "kendi altyapımda" |
| "bağır hava hara" | "bağıra bağıra" |
| "kontrol edilse müsaiti" | "kontrol edebilsin o sayede" |

104 saniyelik ses, GPU'da **52 saniye** (model yüklemesi dahil).

### 3.3 Sözlüğün (initial_prompt) yan etkisi — ÖNEMLİ

Sözlük tek yönlü kazanç değil. **Listelenen terimlere doğru eğiyor, bu da
olmayan yerde onları duymasına yol açıyor:**

- `small`, "modele **kod** yazdırıyorsun"u "modeli **Code** yazdırıyorsun" yazdı
- `large-v3`, "skor"u "**score**" yazdı

Sonuç: sözlük **dar ve spesifik** tutulmalı. "loop", "goal", "graph" gibi genel
İngilizce kelimeler Türkçe konuşmaya yanlış sızar.

### 3.4 Claude Code oturum arşivi

Konum: `~/.claude/projects/<proje-yolu-hash>/<oturum-id>.jsonl`
Durum: 37 oturum, 83 MB. En büyük tek oturum **28.8 MB** (4279 satır).

Her satır bir olay: `user` / `assistant` mesajları, `timestamp`, `cwd`,
`custom-title`, `attachment` kayıtları.

**Görseller arşivin içinde gömülü** (base64): 63 görsel, 11.5 MB. Orijinal
dosyaya bağımlı değil — silinmiş bir ekran görüntüsü bile geri çıkarılabilir.
Bu doğrulandı: 13 gün önceki başka bir projenin oturumundan görsel çıkarılıp
okundu.

**Belgeler (PDF/zip/vb.) gömülü DEĞİL** — sadece dosya yolu saklanır:

| Kayıt tipi | Yol sayısı | Hâlâ var |
|---|---|---|
| `edited_text_file` (proje içi) | 17 | 17 |
| `pdf_reference` | 1 | 1 |
| `file` | 38 | 18 |
| `compact_file_reference` | 11 | 4 |
| **Toplam** | **67** | **40 (%59)** |

Kayıpların 14'ü `Temp/scratchpad` (zaten geçici), 13'ü taşınmış/silinmiş dosya.
`pdf_reference` dosya kaybolsa bile sayfa sayısını ve boyutunu hatırlıyor.

**Çıkarım:** önemli kaynak belgeler proje içinde bir `kaynaklar/` klasörüne
kopyalanmalı. Bu tek hamle %59'u %100'e çıkarır.

---

## 4. Yaşanan hatalar (tekrar keşfedilmesin)

1. **`ffmpeg -vsync` kaldırıldı.** ffmpeg 9.0'da seçenek yok, `-fps_mode` oldu.
2. **Sahne algılama ekran kaydında çalışmaz.** Ekran yavaş değiştiği için 0.04
   eşikte bile tek kare çıktı. Ekran kayıtlarında **eşit aralıklı örnekleme**
   kullanılmalı.
3. **`yt-dlp --force-keyframes-at-cuts` → 403 Forbidden.** Kullanılmamalı.
   Kırpma bu bayrak olmadan sorunsuz çalışıyor.
4. **CUDA için `cublas64_12.dll` gerekiyor.** `nvidia-cublas-cu12` +
   `nvidia-cudnn-cu12` paketleri kurulmalı; DLL klasörleri
   `os.add_dll_directory()` ile kaydedilmeli.
5. **jsonl'i Python'da açarken Windows yolu kullanılmalı** (`C:\...`), MSYS
   yolu (`/c/...`) çözülemiyor. Türkçe karakterler için `encoding="utf-8"` şart.

---

## 5. Tasarım sonuçları

Bu bölüm, izlenen bir eğitim videosundan (Avenox/Taha, "Kendini düzeltme ve
doğru altyapı") çıkarılan derslerin, oturum içinde yaşananlarla sınanmış hâlidir.

### 5.1 Geri besleme döngüsünün üç parçası

| Parça | Kim sağlar |
|---|---|
| **Aksiyon** — model bir değişiklik yapar | Model |
| **Ölçüm** — sonuç iyi mi kötü mü | **Kullanıcı / proje** |
| **Dönüş** — sonuç modele ulaşır | Harness *veya* kullanıcı (kopyala-yapıştır) |

Ortadaki parça asla modelden gelmez. Harness sadece üçüncüyü otomatikleştirir.
Shell'i olmayan bir modelde insan taşıyıcı olur; döngü yavaşlar ama **kurulur**.

### 5.2 Ölçümün dört kalite şartı (dördü de bu oturumda ihlal edildi)

1. **Doğru şeyi ölçmeli.** Bir GPU testi "BAŞARILI" dedi ama yalnızca modelin
   *yüklenmesini* deniyordu, çıkarımı hiç çalıştırmadı. Yanlış ölçen gösterge,
   "bilmiyorum"u "iyiyim"e çevirdiği için hiç gösterge olmamasından kötüdür.
2. **Yıkımdan önce gelmeli.** Bir yama script'i dosyayı diske yazdı, *sonra*
   sözdizimini doğruladı. Hasarı önlemedi, rapor etti.
3. **Kırmızı ışık da yalan söyleyebilir.** "ffmpeg kurulu değil" hatası aracın
   değil, testin hatasıydı (`--ffmpeg-location` unutulmuştu).
4. **Sessiz başarı yasak.** `KARE SAYISI: 0` çıktısı iki hatayı yakalattı. Her
   komut ne yaptığını **sayıyla** söylemeli: "tamam" değil, "12 kare, 104 sn".

### 5.3 Komut mu, doküman mı

- **Yeniden hesaplanabilen** (testler geçiyor mu, ne çalışıyor) → **komut**.
  Doküman olarak yazılırsa bir hafta içinde yalan söyler.
- **Yeniden hesaplanamayan** (neden bu yol seçildi, ne denenip elendi) →
  **doküman**. Hiçbir komut geçmişteki muhakemeyi yeniden üretemez.

Kural: *ölçülebileni ölç, ölçülemeyeni yaz.*

Bunun somut karşılığı, projede "durum iyi mi?" sorusunu tek seferde cevaplayan
bir komut bulunmasıdır (ör. `./dogrula`) — çıkış kodu 0/1 + ne geçti ne kaldı
raporu. Görsel bir uygulamada bu komut mutlaka **ekran görüntüsü karşılaştırma**
katmanı içermelidir; yoksa model kendi çıktısına kör kalır.

### 5.4 Oturumlar arası bellek — dört katman

```
1. HAM       jsonl — her şey + gömülü görseller, hiç silinmez
2. YOLLAR    PDF/zip için işaretçi — %59 sağlam, kaynaklar/ ile %100
3. ÖZET      oturum başına ~1 sayfa
4. KOLEKTİF  tek dosya, ~2-3 sayfa, her oturumun başında okunur
```

Özete ne yazılır (sırasıyla değerli):

- **Kararlar + gerekçeleri** — yeniden türetilemez
- **Denenip elenenler** — en değerlisi; bilinmezse aynı duvara tekrar toslanır
- **Kurulan şeyler** — neyin var olduğu
- **Açık uçlar**

İkinci madde, geri besleme ile bağlamın birleştiği yerdir: ölçümün bulduğu
başarısızlıklar, sonraki oturumun en değerli bağlamıdır. Ölçüm bilgi üretir,
bağlam onu taşır. Biri olmadan diğeri anlamsızdır.

### 5.5 Eski oturuma soru sorma ekonomisi

CLI imkânları (Claude Code 2.1.250):

```bash
claude --resume <id>                              # etkileşimli devam
claude -p "soru" --resume <id> --fork-session     # sor, cevabı stdout'a bas
```

`--fork-session` yeni oturum kimliği açar, orijinal arşive dokunmaz.

**Kritik sınır:** `--resume` o oturumun tüm geçmişini yükleyerek başlar. %60-70
dolulukta bırakılmış bir oturum, o noktadan devam eder. Yani compact atmamak
arşivi korur ama devam edilebilirliği pahalılaştırır.

**Fork sabit taban özelliğini ancak atıldığı sürece korur.** Aynı fork'a ertesi
gün tekrar sorulursa o da birikir ve problem geri gelir. Kural: *her soru için
taze fork, cevap alınınca sil, cevabı özete yaz.*

Ama asıl nokta: **çoğu soru için fork'a hiç gerek yok.**

| Katman | Nasıl | Maliyet | Soruların ~oranı |
|---|---|---|---|
| Özet | yazılı özeti oku | bedava | %90 |
| Arşivi oku | jsonl'de grep + ilgili satırları oku | çok ucuz | %9 |
| Fork + sor | `--resume --fork-session` | soru başına %60-70 pencere | %1 |

Bir oturuma **devam etmek** tüm bağlamı yüklemektir; bir oturumu **okumak**
sadece ilgili satırları okumaktır. jsonl bir konuşma değil, bir **belgedir**.
Fork yalnızca cevap hiçbir yere yazılmamış, o anki muhakemede kalmışsa gerekir.

### 5.6 Arşivi yedeklemenin gerçek gerekçesi

Oturumlar proje **klasör yoluna göre** gruplanıyor. Çalışma dizini değiştiğinde
arşivde yeni bir proje klasörü oluştuğu gözlemlendi. Bir proje klasörü yeniden
adlandırılır veya taşınırsa eski oturumlar silinmez ama öksüz kalır ve
`--resume` ile bulunmaları zorlaşır. Yedekleme bunun için gerekir — bağlam
birikimi için değil.

---

## 6. Açık uçlar

- Oturum özeti/arama altyapısı (`ozetle`, `ara`, `oku`) **henüz kurulmadı**.
  Karar bekleyen soru: özet otomatik mi (unutulmaz ama sessizce kötü özet
  üretebilir) yoksa elle mi (isabetli ama unutulur) oluşsun.
- `izle.py` yalnızca bu makinede çalışacak şekilde bırakıldı (taşınabilirlik
  istenmedi). ffmpeg yolu winget klasörüne göre yedeklenmiş durumda.
- Büyük proje senaryosu (Blender benzeri bir studio uygulaması) için `dogrula`
  komutu tasarlandı ama yazılmadı.

---

## EK — 7 Eylül 2026

Bu dosya 30 Ağustos itibarıyla yazıldı. Oturum 4 Eylül'e kadar sürdü ve
sonrasında çok daha fazlası konuşuldu. **Güncel ve tam kayıt: `BEYIN.md` ve `notlar/`.**

30 Ağustos'tan sonra eklenenlerin özeti:

- YouTube kırpmalı indirme ölçüldü ve karara bağlandı (başabaş ~1 saat)
- Codex oturum arşivi bulundu (`~/.codex/sessions/`, 80+ oturum)
- `UserPromptSubmit` hook kuruldu (her mesajda tarih/saat enjeksiyonu)
- PowerShell profiline `--remote-control` sarmalayıcısı eklendi
- İkinci beyin mimarisi çıkarıldı (klasör / git / Obsidian / mem0 ayrımı)
- Çapraz-araç bağlam sorunu incelendi; kapalı uygulamalarda canlı erişim yok
- Sesli dinleme için altı ayrı açıklama dosyası yazıldı
- Yeni hatalar: boru hattı çıkış kodunu maskeler, heredoc ters bölü yiyor,
  `claude config list` diye bir alt komut yok, klasör taşınınca hafıza öksüz kalır

**Uyarı:** proje klasörü 7 Eylül'de `Desktop\playground` →
`Desktop\desktop\playground` taşındı. Bu dosyadaki yollar eski olabilir.

Bu dosyanın güncel ve kapsamlı hâli için: [[BEYIN]]
