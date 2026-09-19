# Açık uçlar

Karar bekleyenler, yapılmamış testler, sıralanmış yol haritası. **Yalnızca açık
olanlar burada durur.** Kapanan ya da devredilen madde metniyle birlikte
[[acik-uclar-tarihce]] dosyasına taşınır, silinmez (kullanıcı kararı, 19.09).

> Merkez: [[BEYIN]] · İlgili: [[kullanici-baglami]] · [[ikinci-beyin-mimarisi]] · [[capraz-arac-baglam]] · [[2026-09-19-sunum-onarim-listesi]]

---

## Açık — sistem

1. **Sağlayıcıdan bağımsızlık: Codex hook'ları güven kaydı bekliyor.**
   **Sebep bulundu 20.09 00:48:** `codex exec` normalde bağlam vermiyor, ama
   `--dangerously-bypass-hook-trust` ile bağlam anında geliyor. Yani adaptör
   çalışıyor; eksik olan güven kaydı. Kullanıcı terminalde `codex` TUI açıp
   `/hooks` ile güven verecek; sonrasında Desktop ve exec ölçülecek
   ([[olculmus-bulgular]] §14.1). Önceki ölçüm (20.09 00:38, sonuç olumsuz): `/hooks` güven ekranı açmıyor;
   yeni turda hiçbir hook satırı gelmiyor; kayıttaki harita ve saat satırları
   `custom_tool_call_output`, yani betikleri modelin kendisi çalıştırmış.
   Claude bunu bir ara yanlışlıkla "çalışıyor" saydı ve düzeltti
   ([[olculmus-bulgular]] §14). Codex CLI tarafı yalıtılmış testte çalışıyor.
   Eski metin: Çekirdek
   ortak: `AGENTS.md`, `kayit.py` Claude ve Codex okuyucuları, işaretçi
   denetimi. Codex adaptörü `.codex/hooks.json` içinde kurulu. Ama kullanıcı
   hook güveni vermedi. İki Codex Desktop oturumunda `AGENTS.md` enjeksiyonu
   var, hook metni yok (claude 5c600e7e · 19.09 20:21). Desktop'taki güven
   akışı resmî belgede yok; yalnızca CLI'ınki var. Uygulama bazlı durum:
   `rehber/uygulama-adaptorleri.md`. Onarım listesi madde 3, 5, 9.

2. **Erken devir: Claude'da iki eşik de canlı, Codex'te taşıyıcı yok.**
   %50 (19.09 20:31) ve %70 (20.09 00:36) uyarıları gerçek hook zinciriyle
   geldi, ikisinde de kurtarma omurgası yazıldı. Codex tarafında mekanizma
   hazır ve elle doğru sonuç veriyor, ama hook tetiklenmediği için canlı
   uyarı yok. Eski metin:
   `araclar/baglam.py` %50 ve %70'te tur sınırında birer kez uyarıyor ve
   omurgayı diske alıyor. Bu oturumda gerçek hook ile çalıştı: %50 aşıldı,
   uyarı modele ulaştı, kurtarma omurgası yazıldı
   (claude 5c600e7e · 19.09 20:31). Codex tarafı aynı betiği `devir.py`
   üzerinden çağırıyor, ama hook güveni olmadan çalışmaz. Onarım listesi
   madde 6, 7.

3. **Denetim katmanı: iki seviye kurulmadı.** Mekanik işaretçi denetimi kurulu
   ve gece taslaklarını da tarıyor. Kurulmayanlar:
   - **Örneklemeli içerik denetimi:** haftada bir, rastgele 3-5 işaretçi.
     Temiz bağlamlı ajan iddiayı kayıtla karşılaştırır.
   - **Kapanış denetimi:** kapanıştan sonra yazılan notlar ham kayda karşı
     denetlenir.

   **Kararlar:** Denetçi rapor eder, düzeltmez. Uyuşmazlık bulunursa iddianın
   altına not düşülür (kullanıcı, 19.09).

4. **Side chat'ler arşive hiç girmiyor.** Kayıt dosyası oluşmuyor. Tek yol elle
   aktarma. Ölçüm: [[olculmus-bulgular]] §6.

5. **Kalıcı katman boyutu.** Bakım döngüsü kuruldu: `araclar/bakim.py`
   adayları ölçüyor, derleyici raporluyor, oturum başı uyarıyor. İlk bakımda
   kullanıcı iki taşımayı onayladı: kapanmış açık uçlar ve iş bitince onarım
   listesi. Kuralların yanındaki tarihçenin taşınmasını onaylamadı
   (claude 5c600e7e · 19.09 20:31). 100 KB eşiği bundan sonra da aşılı
   kalabilir; karar kullanıcının, ileride yetkili orkestratör ajanın.

6. **Sunum onarımı sürüyor.** 13 açık ve sonradan bulunan 14. açık:
   [[2026-09-19-sunum-onarim-listesi]].

## Ertelenenler

- **Gelen kutusu** (mobilden not düşme) ve **mem0** (kullanıcı, 16.09).
  Uyarı: boşaltılmayan gelen kutusu çöplüğe döner; değer damıtma ritüelinde.
- **Paralelleştirme / mesh** (kullanıcı, 18.09): "birkaç seviye sonra". O
  gün geldiğinde yeni oturuma geçiş, `kapanan-oturum:` ve bakım onayı yetkili
  orkestratör ajana da verilebilir (kullanıcı, 19.09). Bugünkü devir kutusu
  mesh'e uygun değil: [[agentic-yapi]].

## Karar bekleyenler

- Tek ortak hafıza klasörü (`autoMemoryDirectory`) kurulmadı.
- Raspberry Pi alınacak mı? Öneri: önce mevcut makineyi sürekli açık bırakıp
  uzaktan bağlanmayı test et.

## Yapılmamış testler

- **Gece taslağının ilk gerçek gecesi:** 20.09 00:30. Sonuç
  `derleme/gunluk/` ve `derleme/son-calisma.json` içinde görülecek.
- **Codex Desktop'ta yepyeni oturum:** hook güveninden sonra `SessionStart` ve
  erken devir uyarısı ham kayıtta görülmeli.
- `--fork-session` canlı denenmedi.
- Ekran kaydı → `izle.py` zinciri gerçek bir ChatGPT kaydıyla denenmedi.

## Uzun vade

- Ölçek gerektiğinde sunucuya taşı (şimdiden uğraşma).
