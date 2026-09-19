# Uygulama adaptörleri — yetenek tablosu ve ilk oturum protokolü

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

| Yetenek | Claude Code (masaüstü, Code sekmesi) | Codex CLI 0.150 | Codex Desktop 0.155-alpha |
|---|---|---|---|
| Ortak kural dosyası | `CLAUDE.md` → `@AGENTS.md` — **ölçüldü** (temiz örnek, 19.09 16:46) | `AGENTS.md` otomatik — **ölçüldü** (01a0b9eb kaydında enjeksiyon bloğu) | `AGENTS.md` otomatik — **ölçüldü** (01a0ba74 kaydında enjeksiyon bloğu) |
| Oturum başı bağlamı | `SessionStart` → `oturum_basi.py` — **ölçüldü** (startup ve resume) | `SessionStart` → aynı betik — **ölçüldü** (Codex'in yalıtılmış testi, 01a0b9eb) | Adaptör kurulu, **güven verilmedi** — **ölçülmedi** (01a0ba74'te hook metni yok) |
| Tur başı bağlamı (saat, devir kutusu, erken devir) | `UserPromptSubmit` → `devir.py` — **ölçüldü** | aynı — **ölçüldü** (saat ve devir testi) | **ölçülmedi** (güven bekliyor) |
| Compact öncesi | `PreCompact` → `precompact.py`, modele konuşamaz — **ölçüldü** (16.09) | `PreCompact` → `--bicim codex`, modele konuşamaz — **belge** + adaptör testi | **ölçülmedi** |
| Tur sonu (`Stop`) | var, kullanılmıyor | var, kullanılmıyor — **belge** | **ölçülmedi** |
| Oturum sonu (`SessionEnd`) | var, modele konuşamaz; kullanılmıyor (gerekçe: gece taslağı) | var, "konu bitti" demek değil — **belge** | **ölçülmedi** |
| Bağlam doluluğu kaynağı | `message.usage` (input + cache) ÷ pencere; pencere kayıtta yok, kalibre 1M — **ölçüldü** | `token_count`: `last_token_usage.input_tokens ÷ model_context_window` — **ölçüldü** | aynı alanlar — **ölçüldü** (01a0ba74: %83'e çıktı, 20:07'de sıkıştı) |
| Arayüzde sayaç | var (kullanıcı görüyor) | ölçülmedi | **yok** (kullanıcı gözlemi) |
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
2. **Kural dosyası:** `AGENTS.md` kendiliğinden yükleniyor mu? Sınama sorusu:
   "Kapanış işaretinin tam adı ne?" Cevap `kapanan-oturum:` olmalı; uygulama
   dosyayı okumadan bunu bilemez. Yüklenmiyorsa uygulamanın kalıcı proje
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
