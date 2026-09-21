# Beyin — giriş ve harita

> **05:46 güncellemesi:** Codex %70 uyarısı da bu oturumda gerçek hook
> kaydı ve kurtarma dosyasıyla doğrulandı. Önceki “%70 ölçülmedi” satırları
> bu olaydan önceki durumdur. Canlı PreCompact ve yeni gece tetiklemesi ayrı
> olarak ölçülmedi. Yeniden başlatma sonrası canlı Codex penceresi 828.400;
> katalog üst sınırı 872.000 × %95. Compact ayarı 750.000.
> [[2026-09-20-astra-kontrol]].

Bu klasör bir ikinci beyin denemesidir: oturumlar yenilenir, taşıdığı bilgi
kalır. Her oturumun başında **önce bu dosya** okunur; buradan hangi notun
gerektiği görülür.

**Son güncelleme:** 21.09.2026 07:40

---

## Klasör düzeni

| Klasör       | Ne var                                                                                                         |
| ------------ | -------------------------------------------------------------------------------------------------------------- |
| `notlar/`    | **Kalıcı katman.** Konuya göre bölünmüş, birbirine bağlı notlar. Oturumla eskimez                              |
| `oturumlar/` | **Arşiv katmanı.** Oturum başına bir kayıt. Her oturumda okunmaz, sorulunca okunur                             |
| `araclar/`   | Python araçları ve Whisper sözlüğü                                                                             |
| `gorunurluk.json` | **Neyin nereye gideceği.** `ozel` / `ic` / `acik`. Eşleşmeyen her şey `ozel` sayılır. Sorgusu: `python araclar/gorunurluk.py` |
| `dinleme/`   | Sesli dinlemek için yazılmış düz anlatı dosyaları                                                              |
| `derleme/`   | Gece derleyicisinin çıktısı: `gunluk/` `haftalik/` `aylik/` ve `omurga-anlik/` (PreCompact kurtarma dosyaları) |
| `rehber/`    | Kullanıcıya ve dış ajanlara rehberler: sunumun kaynağı (`rehber/sunum/`) Codex'in sesli inceleme haritası ([[codex-sunum-rehberi]]) uygulama bazlı yetenek tablosu (`rehber/uygulama-adaptorleri.md`) Astra kontrol dosyası (`rehber/astra-kontrol.md`) [[astra-lab-denetimi]] ve [[kalici-katman-bakim-plani]] |

Kurallar `AGENTS.md` içinde. Burada çalışan her ajan (Claude, Codex, sonrakiler)
için ortak; kapanış ritüelinin uygulanabilir hâli orada. `CLAUDE.md` onu içe
aktarır ve yalnızca Claude'a özel olanı ekler.

Klasör bir **git deposu** ve private GitHub deposuna bağlı
(`yavuzates34/ikinci-beyin`). Gece görevi 00:30 için kurulu. **20.09 Astra
denetiminde kullanıcı onayıyla** gizli PowerShell, anında log ve 1 saat süre
sınırına geçirildi. Kuru çalışma geçti; yeni ayarın kendi gece tetiklemesi
henüz ölçülmedi. Önceki “commit'e hiç gelmedi” iddiası yanlıştı: 20.09
00:30:05'te `67779e9` commit'i var, sonra çalışma kesilmiş. O çalışmanın
push sonucu ölçülmedi. Güncel kanıt: [[astra-denetim-bulgulari]].

## Kalıcı notlar

| Not | Ne işe yarar |
|---|---|
| [[ikinci-beyin-mimarisi]] | Sistemin neden böyle kurulduğu, katmanlar, hafıza tasarımı |
| [[kapanis-ritueli]] | Oturum nasıl kapanır, neden öyle kapanır |
| [[arac-arsiv]] | Arşivde arama: omurga, ara, anlam, oku |
| [[gece-derleyicisi]] | Her gece çalışan dedektör ve git: ne ölçer, ne ölçmez |
| [[arac-izle]] | Video/sesi modele okutma: izle.py |
| [[ortam-kurulum]] | Makinede neyin nereye kurulduğu: ffmpeg, yt-dlp, Python paketleri, kalıcı ayarlar |
| [[olculmus-bulgular]] | Ölçüm tarihçesi; güncel denetim notlarını birlikte oku |
| [[astra-denetim-bulgulari]] | Üçüncü göz: 81 gizli mesaj, yanlış kapanış/kimlik, gece görevi, canlı %50 ve 1M ayarının sınırları |
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
| [[2026-09-07-ikinci-oturum]] | 07.09 13:02 – 17.09 01:55 | **On gün, 110 mesaj (gerçek 75, bkz. [[olculmus-bulgular]] §10), iki iş kolu.** İlk yarı: kapanış ritüeli, arşiv arama, gece derleyicisi, git, PreCompact ağı. İkinci yarı: yapının Nar Ajans'a taşınması |
| [[2026-09-16-nar-ajans-envanteri]] | 16.09 04:00 – 04:45 | Ayrı oturum değil — yukarıdaki oturumun **alt kolu**. Nar Ajans çalışma alanı sayımı: 6 depo, Codex checkpoint'leri, 4.21 GB yedek |
| [[2026-09-17-agentic-yapi-ve-denetim]] | 17.09 01:59 – 18.09 04:40 | **90 mesaj (gerçek 68), 26,7 saat.** izle.py dört katmana çıktı (OCR + birleştirme), agentic yapı notu ve dört şema, denetim katmanı kararı, SessionEnd boşluğu, gece derleyicisine üç ekleme |
| [[2026-09-19-codex-sunum-ilk-alti-slayt]] | 19.09 18:40 – 19:10 | Codex ile sunumun ilk altı slaytı incelendi; sekiz anlatım/teknik bulgu ve sağlayıcıdan bağımsız erken-devir açığı kaydedildi |
| [[2026-09-19-codex-sunum-yedi-on-ve-onarim-devri]] | 19.09 19:16 – 20:04 | 7–10. slaytlar incelendi; bulgular 13'e çıktı, erken devir P0 hibrit tasarıma bağlandı ve Claude + Codex ortak onarım devri yazıldı |
| [[2026-09-18-saglayici-bagimsizligi-ve-erken-devir]] | 18.09 04:37 – 20.09 00:40 | **25 mesaj, 44 saat.** Sağlayıcıdan bağımsız çekirdek (AGENTS.md, kapanış işareti, Codex adaptörü), erken devir (%50/%70), bakım döngüsü, 14 slaytlık kullanım rehberi ve 15 açıklık ortak onarım turu |
| [[2026-09-19-sunum-onarim-listesi]] | — | Oturum kaydı değil: 15 açıklık onarım turunun iş belgesi ve durum tablosu (19–20.09). Astra turu bunun üzerinden yürür |
| [[2026-09-21-tam-otomasyon-plani]] | — | Oturum kaydı değil: **tam otomasyon iş belgesi.** Kapanış yerine eşik ritüeli, compaction tasarımı, 7 açık (3 küme), kabul edilen politikalar, ölçülecekler ve lab/VDS kararı. **Sıradaki işin kaynağı** |
| [[2026-09-21-otomasyon-lab-ve-vds]] | 20.09 20:28 – **sürüyor** | **Ara kayıt, oturum kapanmadı.** Tam otomasyon kararı, VDS-4 kurulumu ve ölçümü, Avenox v3.1.0 lab'ı, iki videonun dört kaynaklı çözümlemesi, görünürlük ayrımı, omurga §17 düzeltmesi, Astra denetimi ve **dört elenen fikir** |
| [[2026-09-20-astra-kontrol]] | 20.09 04:10 – 20.09 05:55 | Bağımsız 16 madde denetimi, yeni açıklar, kod/not/sunum kaynağı düzeltmeleri, onaylı gece görevi ve proje 1M ayarı |
| [[2026-09-20-toparlama-ve-sunum]] | 20.09 06:06 – 20.09 17:37 | Önceki denetimin commitleri, test kirliliğinin giderilmesi, bakım planı ve sağlayıcıdan bağımsız sunumun yeniden yazımı |
| [[2026-09-20-codex-hook-guven-oncesi-denetimi]] | 20.09 00:25 – 00:35 | Desktop'ta güven öncesi hook denetimi; model beyanı ile gerçek `hooks.additional_context` kaydının ayrımı |
| [[2026-09-20-codex-hook-guveni-ve-testlerin-kapanisi]] | 20.09 00:45 – 01:39 | Güven öncesi/sonrası beş Codex test kaydı; Desktop ve normal CLI zinciri doğrulandı, tüm açık Codex oturumları kapatıldı |
| [[acik-uclar-tarihce]] | — | Oturum kaydı değil: açık uçlardan kapanan ve devredilen maddeler, metniyle (19.09 bakımında taşındı) |
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

- **SIRADAKİ İŞ: görünürlük sızıntısı (21.09 07:40).** Astra ölçtü: açıkça
  `ozel` ve etiketsiz iki notu Avenox `internal` indeksledi ve içeriği bağlama
  verdi. `gorunurluk.json` yalnız **bizim** kodumuz sorduğunda çalışıyor;
  kasayı tarayan yabancı bir araç için hiçbir şey ifade etmiyor. Bu, Avenox
  kurulmasa da açık. [[acik-uclar]] madde 8. Sonraki: İ1 ölçümü (madde 9),
  sonra doğrulanmış mekanizmaların portu.

- **Astra denetimi bitti, karar (b).** Üç iddiam da düştü; "Avenox sürekli
  makbuz yazıyor" yanlış çıktı, iki sistemin çakışmayacağı çürüdü, tek dosya
  hash'i yetersiz. Gerekçeler ve elenenler:
  [[2026-09-21-tam-otomasyon-plani]]. Denetim belgesi: [[astra-lab-denetimi]].
  Oturum kaydı: [[2026-09-21-otomasyon-lab-ve-vds]].

- **Tam otomasyon tasarımı** [[2026-09-21-tam-otomasyon-plani]] içinde duruyor;
  eşik ritüeli, işlenme damgası, compaction ayarı. Elenen fikirler de orada,
  gerekçeleriyle.


- **Toparlama ve sunum:** [[2026-09-20-toparlama-ve-sunum]]. Önceki
  denetim dört commit'te kaydedildi; testler artık kasa dışında kendi geçici
  verisini temizliyor. Eski 178 test klasörü de kalktı: bağımsız son sayımda sahte BEYIN 0,
  test sonrası yeni kalıntı 0; yedi kanıt logu korunuyor.
- **Kalıcı katman:** [[kalici-katman-bakim-plani]] yaklaşık 100 KB altına
  iniş önerisi; henüz uygulanmadı, kullanıcı onayı gerekir.
- **Sunumun yeni kaynağı:** `rehber/sunum/index.html`. 14 slayt önce amaç ve
  sağlayıcıdan bağımsızlığı, sonra işleyişi anlatıyor. Yeni sıra ve kaynaklar
  [[codex-sunum-rehberi]] içinde. Yerel görsel kontrol yapıldı. Kullanıcının
  claude.ai hesabındaki yayına dokunulmadı.
- **Astra denetimi:** [[2026-09-20-astra-kontrol]] ve
  [[astra-denetim-bulgulari]]. Codex %50/%70 canlı doğrulandı; canlı
  PreCompact ve yeni gece ayarının zamanlı sonucu ölçülmedi. Etkin Codex
  penceresi yeniden başlatma sonrası 828.400; büyük pencerenin eşik/
  compact geçişi ayrı testtir. Eski 1–16 durum tablosu tarihçe olarak durur.

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
