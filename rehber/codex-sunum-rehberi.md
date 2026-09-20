# Sunum inceleme haritası — sağlayıcıdan bağımsız ikinci beyin

20 Eylül 2026’da kaynak yeniden yazıldı. Yerel sürüm 14 slayt; ana tez:
**model ve uygulama değişse de karar, gerekçe ve kaynak sonraki işe kalır.**
Yayımlanmış claude.ai kopyası ayrı; bu kaynak değişikliği onu otomatik güncellemez.

> Merkez: [[BEYIN]] · İlgili: [[2026-09-20-toparlama-ve-sunum]] ·
> [[ikinci-beyin-mimarisi]] · [[astra-denetim-bulgulari]]

## Okuma ve inceleme

Önce AGENTS.md ve BEYIN.md. Bir iddiada güncel çalışan kod, kural ve ham
kanıdı birlikte kontrol et. Kodun mevcut davranışı kuralı ihlal edebilir;
“kodda öyle” tek başına doğru tasarım veya başarı kanıtı değildir.

`rehber/sunum/index.html` yerel önizleme. Her HTML dosyasının `aside`
bölümü konuşma notlarını ve kaynak adreslerini taşır. Slayt kimlikleri
eski yayına bağlantı koparmamak için korunuyor; dosya adı eski konuyu
çağrıştırabilir, güncel başlık aşağıdaki haritadır.

## Yeni sıra

| # | Kaynak kimliği | Konu |
|---|---|---|
| 1 | `kapak` | Sağlayıcıdan bağımsız ikinci beyin |
| 2 | `parcalar` | Yeniden anlatma sorunu |
| 3 | `ilke` | Bir sonraki oturuma kalan bilgi |
| 4 | `claude` | Tek ortak hafıza |
| 5 | `codex` | Bilgi neden dosyalarda? |
| 6 | `diger` | İki bilgi katmanı, bir giriş haritası |
| 7 | `yasam` | Bir oturumun çalışma akışı |
| 8 | `uyarilar` | Bir iddiayı kanıtına bağlamak |
| 9 | `cumleler` | Yeni bir uygulamayı bağlamak |
| 10 | `kapanis` | Kapanışta bilgi aktarımı |
| 11 | `gece` | Otomasyonun görevleri ve sınırları |
| 12 | `sinirlar` | Bugünkü kanıt durumu |
| 13 | `komutlar` | Bilgi biriktikçe bakım gerekir |
| 14 | `son` | Sonraki oturumun başlangıç noktası |

## Kaynağa gitmek

- 1–5: AGENTS.md, `ikinci-beyin-mimarisi`, `kullanici-baglami`,
  `iki-ajan-calismasi`; taşınan şey ortak dosyalardaki bilgidir, canlı bağlam değil.
- 6–7: BEYIN.md, AGENTS.md, `kayit.py`, `oturum_basi.py`; seçmeli okuma,
  çalışma sırasında yazma, arşiv ve kalıcı terfi ayrımı.
- 8: `astra-denetim-bulgulari` ve `2026-09-20-astra-kontrol` 04:22;
  81 farklı mesaj, ham dosya karşılaştırması. Adres denetimi içerik denetimi değildir.
- 9: `rehber/uygulama-adaptorleri.md`; yeni uygulama sekiz adımla sınanır.
  Antigravity burada ölçülmedi; sağlayıcı/model/uygulama kavramlarını ayır.
- 10: AGENTS.md kapanış ritüeli; `omurga.py` normal/`--tam`; kesin kimlik.
- 11–12: `baglam.py`, `precompact.py`, `devir.py`, `gece_kayit.py`, `derle.py`;
  gerçek hook metadata türü, kurtarma dosyaları ve kayıtlı zamanlanmış görev.
- 13: [[kalici-katman-bakim-plani]], `bakim.py`, `test_onarim.py`; test
  geçici alanı not kasasının dışında. Not budaması plan, gerçekleşmiş işlem değil.
- 14: başarı ölçütü; yeni ajan gerekli bilgiyi ve kanıtı bulup kullanabiliyor mu?

## İfadelerin sınırları

- %50 ve %70 Codex olayları 258.400 pencerede canlı ölçüldü. Şimdiki etkin
  pencere 828.400; daha büyük pencerenin eşik ve compact geçişleri ölçülmedi.
- Codex canlı PreCompact zinciri ölçülmedi. Kod/adaptör ve sentetik test var.
- Gece görevi yeni ayarıyla kuru testten geçti; planlı gece sonucu ölçülmedi.
  Oturum ve güç koşulları vardır; her gece başarı garantisi yoktur.
- Claude pencere boyutu kalibrasyondur. Yeni uygulamalar aynı yetenekte varsayılmaz.
- Bu rehber yalnız yerel kaynağı anlatır. Hesaptaki yayının güncelliği bu turda ölçülmedi.

## Tekrar üretim ve görsel kontrol

`node araclar/sunum-kaynak.cjs` içerik ve konuşma notlarından mevcut 14 HTML,
deck.json ve yerel önizlemeyi üretir. `sunum-kontrol.cjs` Playwright ile
1920×1080 ekran görüntüsü ve taşma raporu üretir; çıktılar işletim sisteminin
geçici alanında kalır. Yayınlama yapmaz.
