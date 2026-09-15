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
