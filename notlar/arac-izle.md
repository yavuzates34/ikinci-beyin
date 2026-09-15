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
