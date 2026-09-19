# Beyin — giriş ve harita

Bu klasör bir ikinci beyin denemesidir: oturumlar yenilenir, taşıdığı bilgi
kalır. Her oturumun başında **önce bu dosya** okunur; buradan hangi notun
gerektiği görülür.

**Son güncelleme:** 19 Eylül 2026, 17:19

---

## Klasör düzeni

| Klasör       | Ne var                                                                                                         |
| ------------ | -------------------------------------------------------------------------------------------------------------- |
| `notlar/`    | **Kalıcı katman.** Konuya göre bölünmüş, birbirine bağlı notlar. Oturumla eskimez                              |
| `oturumlar/` | **Arşiv katmanı.** Oturum başına bir kayıt. Her oturumda okunmaz, sorulunca okunur                             |
| `araclar/`   | Python araçları ve Whisper sözlüğü                                                                             |
| `dinleme/`   | Sesli dinlemek için yazılmış düz anlatı dosyaları                                                              |
| `derleme/`   | Gece derleyicisinin çıktısı: `gunluk/` `haftalik/` `aylik/` ve `omurga-anlik/` (PreCompact kurtarma dosyaları) |

Kurallar `AGENTS.md` içinde. Burada çalışan her ajan (Claude, Codex, sonrakiler)
için ortak; kapanış ritüelinin uygulanabilir hâli orada. `CLAUDE.md` onu içe
aktarır ve yalnızca Claude'a özel olanı ekler.

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
| [[iki-ajan-calismasi]] | Claude ve Codex aynı klasörde: yöntem, denetim, asimetri |
| [[yasanan-hatalar]] | Bir kez düşülmüş tuzaklar |
| [[tasarim-dersleri]] | Geri besleme, ölçümün kalite şartları, komut mu doküman mı |
| [[capraz-arac-baglam]] | Kapalı sohbet uygulamalarına erişim sorunu (çözülmemiş) |
| [[kullanici-baglami]] | Hedefler, zaman kısıtı, öncelikler, çalışma tarzı |
| [[proje-egemenligi]] | Her klasör ayrı devlet: okunur, müdahale edilmez |
| [[agentic-yapi]] | Model, harness, bağlam: ne ajan, ne değil — şemalı |
| [[acik-uclar]] | Karar bekleyenler, yapılmamış testler, yol haritası |

## Oturum arşivi

Aralık, ham kaydın **ilk ve son damgasından** ölçüldü — dosya adındaki tarih
oturumun açılışıdır, kapanışı değil.

| Oturum | Açılış – Kapanış | Konu |
|---|---|---|
| [[2026-08-30-birinci-oturum]] | 30.08 12:34 – 04.09 22:13 | izle.py kuruldu, arşiv keşfedildi, ikinci beyin tasarlandı |
| [[2026-09-07-ikinci-oturum]] | 07.09 13:02 – 17.09 01:55 | **On gün, 110 mesaj, iki iş kolu.** İlk yarı: kapanış ritüeli, arşiv arama, gece derleyicisi, git, PreCompact ağı. İkinci yarı: yapının Nar Ajans'a taşınması |
| [[2026-09-16-nar-ajans-envanteri]] | 16.09 04:00 – 04:45 | Ayrı oturum değil — yukarıdaki oturumun **alt kolu**. Nar Ajans çalışma alanı sayımı: 6 depo, Codex checkpoint'leri, 4.21 GB yedek |
| [[2026-09-17-agentic-yapi-ve-denetim]] | 17.09 01:59 – 18.09 04:40 | **90 mesaj, 26,7 saat.** izle.py dört katmana çıktı (OCR + birleştirme), agentic yapı notu ve dört şema, denetim katmanı kararı, SessionEnd boşluğu, gece derleyicisine üç ekleme |
| [[BAGLAM-DEVRI]] | — | 30 Ağustos itibarıyla teknik devir belgesi (başka bir modele verilmek üzere) |

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

- **Kapanış ritüeli kurulu.** "Oturumu kapatalım" dendiğinde `AGENTS.md`'deki
  sırayı izle: önce `python araclar/omurga.py`, sonra yaz, sonra mekanik bakım.
- **Arşiv aranabilir.** Bir şeyin daha önce konuşulup konuşulmadığından emin
  değilsen tahmin etme: `python araclar/ara.py "terim"`. 123 oturum, 10 saniye.
- **Tarih hook'u kurulu** ama yine de dikkatli ol: oturum günlerce açık kalabiliyor
  ve konuşma modele kesintisiz görünüyor.
- **Klasör taşınırsa hafıza öksüz kalır.** Oturumlar ve hafıza, klasör yoluna göre
  gruplanıyor. `Desktop\playground` → `Desktop\desktop\playground` taşındı;
  hafıza dosyaları elle taşındı. Eski yoldaki ham jsonl kaydı silinmemeli.
  **Tarih düzeltmesi (17.09 ölçümü):** burada "7 Eylül" yazıyordu; yeni yol
  anahtarındaki ilk damga **04.09 22:13**. Taşımada oturum fork'landı, kimlik
  `6052d412` → `3c1530e9` oldu. Ayrıntı: [[olculmus-bulgular]] §4.
