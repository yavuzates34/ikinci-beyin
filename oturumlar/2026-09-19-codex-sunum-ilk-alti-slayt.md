# Codex sunum incelemesi — ilk altı slayt

kapanan-oturum: 01a0ba53

**Aralık:** 19.09.2026 18:40–19:10  
**Konu:** “İkinci Beyin — Kullanım Rehberi” sunumunun Codex ile sesli
incelemesi; ilk altı slayt.

> Merkez: [[BEYIN]] · İlgili: [[codex-sunum-rehberi]] ·
> [[iki-ajan-calismasi]] · [[kapanis-ritueli]] · [[acik-uclar]]

---

## Ne yapıldı

Oturum başında `rehber/codex-sunum-rehberi.md`, başlangıç bağlamı ve `BEYIN.md`
okundu. Kullanıcı sunumun ilk altı sayfasını sesli olarak açtı; Codex soruları
sunum kaynağına, proje dosyalarına, yerel Codex yapılandırmasına ve resmî
OpenAI belgelerine bakarak cevapladı. İnceleme sırasında hiçbir dosya
değiştirilmedi; aşağıdaki kayıt yalnızca kullanıcı devir istediğinde yazıldı.

## İlk altı slaytta bulunanlar

1. **“Her oturumda BEYIN.md okunur” otomatiklik izlenimi veriyor.** Kural bütün
   ajanlar için ortak; otomasyon araca göre değişiyor. Claude ve Codex'in ince
   adaptörleri var. Bilinmeyen bir araç, yalnızca klasör açıldığı için bu iki
   dosyayı okuyacağını bilemez.
2. **Üçüncü slayttaki “destekliyorsa AGENTS.md, yoksa ilk mesaj” ifadesi
   belirsiz.** “İlk mesaj”, kullanıcının yeni uygulamaya her oturumda elle
   göndereceği başlangıç talimatı. Başlık bunu açıkça söylemeli.
3. **Beşinci slayt Codex Desktop ile Codex CLI'ı ayırmıyor.** Resmî belgede
   `/hooks` ile güven incelemesi CLI için anlatılıyor; Desktop'ta aynı kullanıcı
   akışı bu oturumda doğrulanmadı.
4. **“Üç hook” teknik olarak kaba bir özet.** `.codex/hooks.json` içinde üç
   olay grubu (`SessionStart`, `UserPromptSubmit`, `PreCompact`) ve bunların
   altında toplam dört komut var; `UserPromptSubmit` saat ile devir kutusunu
   ayrı ayrı çalıştırıyor.
5. **Hook güven akışı henüz uçtan uca ölçülmedi.** Sunum yazıldığında kullanıcı
   güveni verilmemişti; bu oturumda da kullanıcı, bağlam görünürlüğünü çözmeden
   hook'ları onaylamama kararı aldı.
6. **Codex Desktop'ta görünür bağlam yüzdesi yok.** Bu oturumun yerel kaydı
   etkin pencereyi `258.400` token olarak gösterdi. Kapanış öncesindeki son
   ölçüm `141.137` etkin giriş tokenı, yaklaşık `%54,6` idi. CLI resmî
   belgesinde “context left” göstergesi var; Desktop için eşdeğeri bulunmadı
   (codex 01a0ba53 · 19.09 19:09).
7. **Asıl mimari açık: otomatik compact'tan güvenli biçimde önce çalışan,
   sağlayıcıdan bağımsız bir devir tetikleyicisi yok.** Bugünkü manuel yol,
   kullanıcının bağlam yüzdesini görüp “oturumu kapatalım” demesine dayanıyor.
   Codex Desktop'ta sayaç yok ve pencere kullanıcının Claude oturumuna göre
   daha küçük. `PreCompact` ise erken devir değil, son güvenlik ağı
   (codex 01a0ba53 · 19.09 19:00).
8. **Altıncı slayttaki “Her oturumun ilk mesajı” başlığı özneyi saklıyor.**
   “Her oturumda senin göndereceğin ilk mesaj” denmeli. Ayrıca yeni uygulamanın
   yerel klasöre erişebilmesi ve komut çalıştırabilmesi ön koşul.

## Karar ve gerekçe

Kullanıcı, ikinci beyin sisteminin Claude ve Codex için aynı temel davranışa
evrilmesi gerektiğini belirledi: bağlam güvenli bir eşiğe ulaştığında sistem,
sağlayıcının otomatik compact'ını beklemeden devir sürecini kendisi başlatmalı.
`PreCompact` son savunma hattı olarak kalmalı; ana yol olmamalı. Eşik konu
ortasında aşılırsa oturumu doğrudan kapalı mühürlemek yerine turun sonunda
kontrollü devir yapılmalı ve kapanış işareti gerçek geçişte yazılmalı
(codex 01a0ba53 · 19.09 19:00).

## Denenen, elenen ve yapılmayan

- **Yalnızca manual compact = devir** düşüncesi elendi. Compact kayıplı bir
  sıkıştırmadır; karar, elenen fikir ve açık uç garantisi vermez.
- **PreCompact'ı ana kapanış yolu saymak** elendi. Rastgele bir konu noktasında
  ve bağlam zaten doluyken gelir.
- Hook'lara güven verilmedi, sunum dosyaları düzeltilmedi ve yeni erken-devir
  mekanizması kurulmadı. Kullanıcı bu oturumun amacının inceleme olduğunu,
  uygulamanın sonraya kalacağını açıkça söyledi.

## Açık kalanlar — yeni oturumun tutacağı yer

1. Sunum incelemesine **7. slayttan** devam et.
2. İlk altı slayttaki sekiz bulguyu sunum revizyonunda işle.
3. Sağlayıcıdan bağımsız erken-devir mekanizmasını tasarla: ölçüm kaynağı,
   güvenli eşik, tur-sonu tetik, kapanış işaretinin zamanı ve Claude/Codex
   adaptörleri.
4. Codex Desktop'ta `/hooks` güven arayüzünü ve gerçek `PreCompact` zincirini
   kullanıcı hazır olduğunda uçtan uca ölç.
