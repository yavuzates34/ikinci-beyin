# Uygulama adaptörleri — yetenek tablosu ve ilk oturum protokolü

> **05:46 güncellemesi:** Codex %70 uyarısı da bu oturumda gerçek hook
> kaydı ve kurtarma dosyasıyla doğrulandı. Önceki “%70 ölçülmedi” satırları
> bu olaydan önceki durumdur. Canlı PreCompact ve yeni gece tetiklemesi ayrı
> olarak ölçülmedi. Yeniden başlatma sonrası canlı Codex penceresi 828.400;
> katalog üst sınırı 872.000 × %95. Compact ayarı 750.000.
> [[2026-09-20-astra-kontrol]].

Beyin tek bir çekirdektir: `AGENTS.md`, `notlar/`, `oturumlar/` ve
`araclar/*.py`. Hook'lar ise bir **modelin** değil, somut bir **uygulamanın**
(harness) yeteneğidir. Aynı sağlayıcının iki uygulaması farklı davranabilir;
Codex CLI ile Codex Desktop'ın sürümleri ve arayüzleri bile ayrı. Bu yüzden
adaptör uygulama başına kurulur. Çekirdek hiçbir zaman çoğaltılmaz
(onarım listesi madde 9 · codex 01a0ba74 · 19.09 19:21).

Durum etiketleri:
- **ölçüldü:** bu makinede, ham kayıtla doğrulandı.
- **belge:** üreticinin belgesinde yazıyor, burada ölçülmedi.
- **ölçülmedi:** bilinmiyor. Çalışıyor varsayılmaz.

## Yetenek tablosu

**20.09 Astra denetim eki:** Desktop'ta harita/saat ve **%50 uyarısı** bu
oturumda ham `hooks.additional_context` kaydıyla doğrulandı. %70 ve
PreCompact hâlâ ölçülmedi. Kontrol yeni kullanıcı mesajında; uzun tek tur
içinde yok. Claude'un 1M penceresi ölçülmüş pencere değil, kalibrasyon.
Proje Codex ayarı 1.050.000 pencere/900.000 compact olarak yüklendi; açık
oturumun canlı penceresi hâlâ 258.400. [[astra-denetim-bulgulari]].
Resmî hook çıktısı alanları: [Codex hooks](https://learn.chatgpt.com/docs/hooks).

| Yetenek | Claude Code (masaüstü, Code sekmesi) | Codex CLI 0.150 | Codex Desktop 0.155-alpha |
|---|---|---|---|
| Ortak kural dosyası | `CLAUDE.md` → `@AGENTS.md` — **ölçüldü** (temiz örnek, 19.09 16:46) | `AGENTS.md` otomatik — **ölçüldü** (01a0b9eb kaydında enjeksiyon bloğu) | `AGENTS.md` otomatik — **ölçüldü** (01a0ba74 kaydında enjeksiyon bloğu) |
| Oturum başı bağlamı | `SessionStart` → `oturum_basi.py` — **ölçüldü** (startup ve resume) | `SessionStart` → aynı betik — **ölçüldü** (normal `exec`, 01a0bbcc-8818) | aynı — **ölçüldü** (01a0bbc6-b6f6); ham kayıt türü `hooks.additional_context` |
| Tur başı bağlamı (saat, devir kutusu, erken devir) | `UserPromptSubmit` → `devir.py` — **ölçüldü** | saat + `devir.py` — **ölçüldü** (normal `exec`, 01a0bbcc-8818) | saat + `devir.py` taşıyıcısı — **ölçüldü** (01a0bbc6-b6f6); %50/%70 gerçek uyarısı henüz ölçülmedi |
| Compact öncesi | `PreCompact` → `precompact.py`, modele konuşamaz — **ölçüldü** (16.09) | `PreCompact` → `--bicim codex`, modele konuşamaz — **belge** + adaptör testi | **ölçülmedi** |
| Tur sonu (`Stop`) | var, kullanılmıyor | var, kullanılmıyor — **belge** | **ölçülmedi** |
| Oturum sonu (`SessionEnd`) | var, modele konuşamaz; kullanılmıyor (gerekçe: gece taslağı) | var, "konu bitti" demek değil — **belge** | **ölçülmedi** |
| Bağlam doluluğu kaynağı | `message.usage` (input + cache) ÷ pencere; pencere kayıtta yok, kalibre 1M — **ölçüldü** | `token_count`: `last_token_usage.total_tokens ÷ model_context_window` — **ölçüldü** | aynı alanlar — **ölçüldü** (01a0ba74: %83'e çıktı, 20:07'de sıkıştı) |
| Arayüzde sayaç | var (kullanıcı görüyor) | ölçülmedi | **yok** (kullanıcı gözlemi) |
| Hook güven akışı | proje ayarı, ek adım yok | `/hooks` (TUI) ile güven verilir; güven yoksa sessizce atlanır, güven sonrası normal `exec` çalışır — **ölçüldü** (20.09 00:48–01:32) | Desktop içindeki `/hooks` ekran açmıyor; CLI TUI'de verilen kalıcı güven Desktop'ta da geçerli — **ölçüldü** (01a0bbc6-b6f6) |
| Ham kayıt yeri | `~/.claude/projects/<proje>/<id>.jsonl` | `~/.codex/sessions/<y>/<a>/<g>/` | aynı, kapatılınca `~/.codex/archived_sessions/` |
| Arşiv okuyucusu (`kayit.py`) | var | var | var (arşivlenmiş klasör 19.09'da eklendi) |

Side chat (Claude) ve bulut sohbet uygulamaları tabloda yok: kayıt dosyası
oluşmuyor, adaptör kurulamıyor (bkz. `notlar/olculmus-bulgular.md` bölüm 6).

## Yeni bir uygulamayı tanıtma protokolü

Bir uygulama bu klasörde ilk kez açıldığında, o oturumdaki ajan kullanıcıyla
birlikte şu adımları izler. Her adımın sonucu yukarıdaki tabloya yeni bir sütun
olarak, durum etiketiyle yazılır.

1. **Ön koşul:** uygulama yerel klasörü okuyabiliyor ve komut
   çalıştırabiliyor mu? Çalıştıramıyorsa beyin yalnızca okunur. Tabloya
   "salt okunur" yazılır, gerisi atlanır.
2. **Kural dosyası:** `AGENTS.md` kendiliğinden yükleniyor mu? Sınama sorusu
   ilk ipucudur, kanıt değildir: model cevabı eski bağlamdan veya elle
   okumadan alabilir. Temiz oturumun ham kaydında otomatik enjeksiyonun
   türünü ve dosya içeriğini doğrula; araç çıktısını ayır. Yüklenmiyorsa kalıcı proje
   talimatı yeri varsa oraya tek satır yazılır: "Önce AGENTS.md'yi oku." O da
   yoksa **kullanıcı** her oturumun ilk mesajında bunu söyler.
3. **Başlangıç bağlamı:** `python araclar/oturum_basi.py --bicim duz` elle
   çalışıyor mu?
4. **Hook desteği:** uygulamanın belgesi ve sürümü okunur. Destek varsa yalnızca
   ince bir adaptör kurulur: aynı betikleri çağırır, çıktıyı uygulamanın
   biçimine çevirir. Çekirdeğe uygulamaya özel kod girmez; gerekiyorsa bir
   `--bicim` dalı eklenir.
5. **Güven ve etkinleştirme:** hook güveni gibi arayüz işlemlerini **kullanıcı**
   yapar. Ajan yapılmış varsaymaz.
6. **Ham kayıt ve ölçüm:** konuşma diske nereye yazılıyor? `kayit.py`'ye okuyucu,
   `baglam.py`'ye doluluk kaynağı eklenir. Kaynak yoksa tabloya "ölçülemiyor"
   yazılır ve erken devir o uygulamada kullanıcının sayacına kalır.
7. **Uçtan uca sınama:** **yepyeni** bir oturumda başlangıç bağlamının modele
   ulaştığı ham kayıttan doğrulanır. Elle çalıştırılan komut otomatik zincirin
   kanıtı değildir.
8. **Eksikleri açık bırak:** kurulamayan refleks tabloda "yok" ya da "ölçülmedi"
   olarak kalır. İki uygulamanın hafıza garantisi aynı sanılmaz.
