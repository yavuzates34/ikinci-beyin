# Beyin — giriş ve harita

Bu klasör bir ikinci beyin denemesidir: oturumlar yenilenir, taşıdığı bilgi
kalır. Her oturumun başında **önce bu dosya** okunur; buradan hangi notun
gerektiği görülür.

**Son güncelleme:** 16 Eylül 2026, 03:10

---

## Klasör düzeni

| Klasör       | Ne var                                                                                                         |
| ------------ | -------------------------------------------------------------------------------------------------------------- |
| `notlar/`    | **Kalıcı katman.** Konuya göre bölünmüş, birbirine bağlı notlar. Oturumla eskimez                              |
| `oturumlar/` | **Arşiv katmanı.** Oturum başına bir kayıt. Her oturumda okunmaz, sorulunca okunur                             |
| `araclar/`   | Python araçları ve Whisper sözlüğü                                                                             |
| `dinleme/`   | Sesli dinlemek için yazılmış düz anlatı dosyaları                                                              |
| `derleme/`   | Gece derleyicisinin çıktısı: `gunluk/` `haftalik/` `aylik/` ve `omurga-anlik/` (PreCompact kurtarma dosyaları) |

Kurallar `CLAUDE.md` içinde; kapanış ritüelinin uygulanabilir hâli orada.

Klasör bir **git deposu** ve private GitHub deposuna bağlı
(`yavuzates34/ikinci-beyin`): her gece otomatik commit + push.

## Kalıcı notlar

| Not | Ne işe yarar |
|---|---|
| [[ikinci-beyin-mimarisi]] | Sistemin neden böyle kurulduğu, katmanlar, hafıza tasarımı |
| [[kapanis-ritueli]] | Oturum nasıl kapanır, neden öyle kapanır |
| [[arac-arsiv]] | Arşivde arama: omurga, ara, anlam, oku |
| [[gece-derleyicisi]] | Her gece çalışan dedektör ve git: ne ölçer, ne ölçmez |
| [[arac-izle]] | Video/sesi modele okutma: izle.py |
| [[olculmus-bulgular]] | Tahmin değil ölçüm. Yeniden ölçmeye gerek yok |
| [[yasanan-hatalar]] | Bir kez düşülmüş tuzaklar |
| [[tasarim-dersleri]] | Geri besleme, ölçümün kalite şartları, komut mu doküman mı |
| [[capraz-arac-baglam]] | Kapalı sohbet uygulamalarına erişim sorunu (çözülmemiş) |
| [[kullanici-baglami]] | Hedefler, zaman kısıtı, öncelikler, çalışma tarzı |
| [[acik-uclar]] | Karar bekleyenler, yapılmamış testler, yol haritası |

## Oturum arşivi

| Oturum | Konu |
|---|---|
| [[2026-08-30-birinci-oturum]] | izle.py kuruldu, arşiv keşfedildi, ikinci beyin tasarlandı |
| [[2026-09-07-ikinci-oturum]] | Kapanış ritüeli ve arşiv arama katmanı kuruldu |
| [[BAGLAM-DEVRI]] | 30 Ağustos itibarıyla teknik devir belgesi (başka bir modele verilmek üzere) |

## Sesli dinleme dosyaları

Düz anlatı, tablo ve şema yok. **Bunlara bağ yazılmaz** — köşeli parantezler
seslendirmede gürültü yapar. Bu bilinçli bir karardır, sonraki oturumlar
"eksik" sanıp düzeltmeye kalkmasın.

`dinleme/` içinde: ikinci beyin dört unsuru · yakalama mimarisi · ChatGPT
yakalama · sunucu ve mem0 · sekiz ay değerlendirmesi · neden AI operatörlüğü

## Bağlama kuralı

Notlar birbirine `[[dosya-adi]]` biçiminde bağlanır (uzantı yazılmaz, klasör
yazılmaz — Obsidian dosya adıyla bulur). Yeni bir not açıldığında **iki yönlü**
bağ kurulur: notun içinden ilgili notlara, ayrıca bu haritaya bir satır.

Haritada görünmeyen dosya, sonraki oturumlar için kayıptır.

## Bir sonraki oturuma not

- **Kapanış ritüeli kurulu.** "Oturumu kapatalım" dendiğinde `CLAUDE.md`'deki
  sırayı izle: önce `python araclar/omurga.py`, sonra yaz, sonra mekanik bakım.
- **Arşiv aranabilir.** Bir şeyin daha önce konuşulup konuşulmadığından emin
  değilsen tahmin etme: `python araclar/ara.py "terim"`. 123 oturum, 10 saniye.
- **Tarih hook'u kurulu** ama yine de dikkatli ol: oturum günlerce açık kalabiliyor
  ve konuşma modele kesintisiz görünüyor.
- **Klasör taşınırsa hafıza öksüz kalır.** Oturumlar ve hafıza, klasör yoluna göre
  gruplanıyor. 7 Eylül'de `Desktop\playground` → `Desktop\desktop\playground`
  taşındı; hafıza dosyaları elle taşındı. Eski yoldaki ham jsonl kaydı silinmemeli.
