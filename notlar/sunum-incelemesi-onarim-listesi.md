# Sunum incelemesi — onarım listesi

Claude ve Codex'in birlikte kapatacağı, “İkinci Beyin — Kullanım Rehberi”
incelemesinde bulunan **13 açık**. Bu dosya yalnızca sunum metnini düzeltme
listesi değildir: sunumun açığa çıkardığı gerçek sistem kusurlarını da kapsar.

> Merkez: [[BEYIN]] · İlgili: [[acik-uclar]] · [[kapanis-ritueli]] ·
> [[gece-derleyicisi]] · [[iki-ajan-calismasi]] ·
> [[2026-09-19-codex-sunum-ilk-alti-slayt]] ·
> [[2026-09-19-codex-sunum-yedi-on-ve-onarim-devri]] ·
> [[codex-sunum-rehberi]]
>
> Kaynaklar: İlk sekiz bulgu önceki Codex incelemesinde ölçüldü
> (codex 01a0ba53 · 19.09 18:40–19:10). Dokuzuncu–on üçüncü maddeler devam
> oturumunda kullanıcıyla sesli incelemede bulundu
> (codex 01a0ba74 · 19.09 19:18–19:55).

## Çalışma kuralı

Sunum özet, kaynak değildir. Düzeltme sırası:

1. Önce gerçek davranışı kod, `AGENTS.md`, hook yapılandırmaları ve ham oturum
   kayıtlarıyla doğrula.
2. Sistem kusuru varsa önce sistemi düzelt ve uçtan uca sına.
3. Kalıcı notları güncelle.
4. En son `rehber/sunum/slides/` altındaki sunum kaynağını ve
   `rehber/codex-sunum-rehberi.md` dosyasını güncelle.

Claude ve Codex aynı iddiayı birbirinden bağımsız kontrol etsin; biri değişiklik
yaparsa diğeri kaynak ve test açısından denetlesin. Kullanıcıdan işlem gereken
noktalar aşağıda ayrıca işaretlidir. Belirsiz davranışı çalışıyor varsaymayın.

**Anthropic oturumunda başlangıç cümlesi:** “`BEYIN.md` ile
`notlar/sunum-incelemesi-onarim-listesi.md` dosyasını oku. Bir Codex ajanı
çalıştır; on üç açığı kaynaklardan bağımsız denetleyip birlikte kapatın. Önce
gerçek sistemi, sonra kalıcı notları, en son sunumu düzeltin. Kullanıcı kararı
veya arayüz işlemi gereken yerde bana sorun; doğrulanmamış işi tamamlandı
saymayın.”

## On üç bulgu

### 1. “Her oturumda BEYIN.md okunur” otomatiklik izlenimi veriyor

Ortak kural her ajan içindir; otomatik okuma her uygulamada garanti değildir.
Claude ve Codex için adaptör olabilir, bilinmeyen bir uygulama yalnızca klasörü
açtığı için dosyayı okumaz.

**Bak:** `AGENTS.md`, `araclar/oturum_basi.py`, sunumun `parcalar` ve `ilke`
slaytları.

**Bitiş ölçütü:** Sunum ortak kural ile otomatik uygulama refleksini açıkça
ayırmalı.

### 2. “Yoksa ilk mesaj” ifadesinin öznesi belirsiz

Üçüncü slayttaki ifade, mesajı kimin göndereceğini saklıyor. Hook veya proje
talimatı desteği olmayan uygulamada bu, **kullanıcının bir kez ya da her
oturumda göndereceği başlangıç mesajıdır**; hangi sıklığın gerektiği uygulamanın
kalıcı proje talimatı desteğine bağlıdır.

**Bak:** `rehber/sunum/slides/ilke.html`, `AGENTS.md` → “Oturum başı bağlamı”.

**Bitiş ölçütü:** Özne ve tekrar sıklığı açık yazılmalı.

### 3. Codex Desktop ile Codex CLI ayrılmıyor

Sunum, komut satırı için belgelenen veya görülen akışları Desktop'ta da aynıymış
gibi anlatıyor. Aynı ürün ailesinde olmak, arayüz ve güven akışının birebir aynı
olduğu anlamına gelmez.

**Bak:** `rehber/sunum/slides/codex.html`, `.codex/hooks.json`, resmî Codex
hooks belgesi.

**Bitiş ölçütü:** Belgelenen davranış, yerelde ölçülen davranış ve henüz
ölçülmemiş Desktop davranışı ayrı etiketlenmeli.

### 4. “Üç hook” teknik olarak kaba bir özet

Codex yapılandırmasında üç olay grubu vardır: `SessionStart`,
`UserPromptSubmit`, `PreCompact`. Fakat `UserPromptSubmit` altında saat ve devir
kutusu ayrı çalıştığı için toplam dört komut vardır.

**Bak:** `.codex/hooks.json`.

**Bitiş ölçütü:** Sunum “üç olay, dört komut” demeli ya da teknik sayıyı hiç
iddia etmemeli.

### 5. Codex hook kurulumu var, otomatik zincir doğrulanmış değil

`.codex/hooks.json` ve çağırdığı Windows adaptörleri diskte mevcut. Belirsiz
olan kurulumun varlığı değil; bu proje katmanına kullanıcı güveni verilip
verilmediği ve gerçek bir Codex Desktop başlangıcında `SessionStart` çıktısının
modele teslim edilip edilmediğidir. Bu oturumda `oturum_basi.py --bicim duz`
elle çalıştırıldı; bu otomatik zincirin kanıtı değildir
(codex 01a0ba74 · 19.09 19:37).

**Bak:** `.codex/hooks.json`, `araclar/codex-run-python.ps1`,
`araclar/oturum_basi.py`, [[iki-ajan-calismasi]].

**Kullanıcı gerekir:** Codex'in hook güven arayüzünde proje hook'larını inceleyip
onaylamak ve ardından yepyeni bir Codex oturumu açmak.

**Bitiş ölçütü:** Yeni oturumda `SessionStart` otomatik çalışmalı; kimlik,
harita yönergesi ve gerçek bir kontrollü test uyarısı modele ulaşmalı. Sonuç
ham oturum kaydıyla doğrulanmalı.

### 6. Codex Desktop'ta görünür context yüzdesi yok

Desktop arayüzünde kullanıcıya bağlam doluluğu gösterilmedi. Ham Codex kaydı
etkin pencereyi `258.400` token olarak tutuyor ve son kullanım kaydından yüzde
hesaplanabiliyor; fakat kullanıcı bunu arayüzde göremiyor. Devam oturumunda
ölçülen son tamamlanmış değer yaklaşık `%64` idi
(codex 01a0ba74 · 19.09 19:45).

**Bak:** [[agentic-yapi]], [[kapanis-ritueli]], ilgili Codex JSONL kaydındaki
`token_count` olayları.

**Bitiş ölçütü:** Görünür sayaç yokluğu sunumda sınır olarak yazılmalı; sistem
kararını yalnızca kullanıcının sayaç görmesine bağlamamalı.

### 7. P0 — Sağlayıcıdan bağımsız erken devir tetikleyicisi yok

Bugünkü ana yol, kullanıcının anlamlı bir yerde “Oturumu kapatalım” demesidir.
`PreCompact` bağlam dolduğunda gelen son güvenlik ağıdır; kontrollü erken devir
değildir. Güvenli eşik, ölçüm kaynağı, turun sonunda tetikleme ve gerçek geçiş
olmadan `kapanan-oturum:` yazmama birlikte tasarlanmalıdır
(codex 01a0ba53 · 19.09 19:00).

Bu bir “elle mi, tamamen otomatik mi?” ikili seçimi değildir. **Önerilen hibrit
yol:**

1. Uygulama adaptörü, arayüz gösterse de göstermese de erişebildiği en güvenilir
   kaynaktan context doluluğunu otomatik ölçer. Codex'te bunun bir adayı JSONL
   içindeki `token_count`; başka uygulamada başka kaynak gerekebilir.
2. Güvenli eşik aşılınca oturumu cümlenin ortasında kapatmaz. Turun sonunda
   otomatik bir kurtarma kontrol noktası çıkarır ve kontrollü devir önerir.
3. Kullanıcı “devret” dediğinde canlı model omurgayı okuyup arşiv ve terfiyi
   yazar; ancak gerçekten yeni oturuma geçilirken `kapanan-oturum:` eklenir.
4. Kullanıcı devam ederse uyarı boğucu biçimde her tur tekrarlanmaz; risk artınca
   yeniden görünür olur.
5. Ölçüm kaynağı yoksa adaptör bunu açıkça söyler ve daha zayıf bir vekil ölçüt
   kullanır; görünür sayaç varmış gibi davranmaz.
6. `PreCompact`, ölçüm veya kullanıcı akışı kaçarsa omurgayı kurtaran son
   savunma hattı olarak kalır; ana kapanış yolu olmaz.

Gerekçe: yalnızca manuel yol, context yüzdesini göstermeyen uygulamalarda
kullanıcıya görünmez bir sorumluluk yükler. Tam otomatik `PreCompact` kapanışı
ise çok geç ve anlamsız bir konu sınırında gelebilir. Otomasyon **riski fark
etmeli ve hazırlığı başlatmalı**; oturumun gerçekten bittiğine dair semantik
kararı tek başına vermemelidir (codex 01a0ba74 · 19.09 19:58).

**Bak:** [[kapanis-ritueli]] → “Erken devir boşluğu”, `araclar/precompact.py`,
`araclar/devir.py`.

**Kullanıcı kararı gerekir:** Güvenli eşik, ilk uyarıdan sonra ne kadar
ertelenebileceği ve gerçek yeni oturuma geçişin yalnızca kullanıcı onayıyla mı
yoksa uygulamanın desteklediği otomatik bir geçişle mi yapılacağı.

**Bitiş ölçütü:** Claude ve Codex'te aynı anlamı taşıyan, test edilmiş ana yol;
görünür sayaç olmayan Codex Desktop'ta eşik uyarısı gerçek token kaydından
ölçülür; uyarı anlamlı tur sınırında gelir; kullanıcı devam edebilir; gerçek
geçiş olmadan kapanış işareti yazılmaz; `PreCompact` yalnızca son savunma olarak
kalır.

### 8. “Her oturumun ilk mesajı” başlığı özneyi ve ön koşulları saklıyor

Altıncı slayt, mesajı kullanıcının göndereceğini söylemiyor. Ayrıca uygulamanın
yerel klasörü okuyabilmesi ve komut çalıştırabilmesi ön koşulunu gizliyor.

**Bak:** `rehber/sunum/slides/diger.html`, `araclar/oturum-basi.md`.

**Bitiş ölçütü:** Başlık kullanıcı eylemini ve uygulama ön koşullarını açıkça
söylemeli.

### 9. Adaptör sağlayıcıya değil somut uygulamaya göre kurulmalı

Hook'lar “Anthropic” veya “OpenAI” modelinin genel yeteneği değildir; Claude
Code ve Codex gibi uygulama/harness yeteneğidir. Aynı sağlayıcının başka bir
uygulamasında aynı hook sistemi hiç bulunmayabilir. Ortak beyin çoğaltılmamalı;
ilk temas komutu uygulamayı ve gerçek yeteneklerini tanıyıp yalnızca ince
adaptörü kurmalı, sınamalı ve eksik refleksleri açıkça kaydetmelidir
(codex 01a0ba74 · 19.09 19:21).

**Bak:** `.claude/settings.json`, `.codex/hooks.json`, `CLAUDE.md`, `AGENTS.md`.

**Bitiş ölçütü:** Tek ortak çekirdek + uygulama bazlı yetenek/adaptör tablosu +
ilk oturum kurulum ve doğrulama protokolü.

### 10. Kalıcı katmanın budama döngüsü yok

Gece derleyicisi bilinçli olarak “ölçer, yazmaz”. Kalıcı notların boyutunu
ölçüyor ama büyük dosyaları bölmüyor, kapanmış tarihi soğuk katmana indirmiyor,
tekrarları birleştirmiyor ve haritasız notları bakım adayı olarak sunmuyor.
Kalıcı Markdown notları 19 Eylül akşamı yaklaşık `123 KB` idi; `65 KB` seçmeli
okuma ve `100 KB` bölme eşikleri aşılmıştı. `acik-uclar.md` kapanmış tarih
taşıyor; `kapanis-ritueli.md` güncel yöntem ile elenmiş tasarımı karıştırıyor;
`ortam-kurulum.md` BEYIN haritasında görünmüyor
(codex 01a0ba74 · 19.09 19:26–19:32).

**Bak:** `araclar/derle.py`, `araclar/oturum_basi.py`, [[gece-derleyicisi]],
[[acik-uclar]], [[kapanis-ritueli]], `BEYIN.md`.

**Kullanıcı kararı gerekir:** Otomatik silme yapılmamalı. Hangi tarihsel
malzemenin arşive taşınacağı ve sıcak notların ne kadar kısa tutulacağı kullanıcı
ile kararlaştırılmalı.

**Bitiş ölçütü:** Derleyici budama **adaylarını** raporlar ve bu uyarıyı oturum
başına taşır; canlı oturumda kullanıcıyla bakım yapılır. Git ve oturum arşivi
tarihçeyi korur.

### 11. Sekizinci slaytta bilgi tabanı sağlığı uyarısı eksik

Mevcut beş uyarı operasyoneldir: push, yarıda kalan gece çalışması, kapanmamış
oturum, gece taslağı ve kusurlu işaretçi. Kalıcı katmanın büyümesi ve budama
ihtiyacı yoktur. “Her şey yolundaysa ajan hiçbir şey söylemez” cümlesi bu yüzden
fazla güçlüdür; sessizlik yalnızca **tanımlı uyarıların** bulunmadığını söyler.

**Bak:** `rehber/sunum/slides/uyarilar.html`, `derleme/son-calisma.json`,
`araclar/oturum_basi.py` → `derleyici_uyarilari()`.

**Bitiş ölçütü:** Sistem önce bakım sağlığı verisini üretip başlangıca taşımalı;
ardından slayta “Kalıcı katman bakım eşiğini aştı” uyarısı eklenmeli. Sunum,
henüz çalışmayan uyarıyı çalışıyor gibi göstermemeli.

### 12. “Gece taslağını işleyelim” yalnızca belirli durumda geçerli

Kullanıcı aynı oturuma dönerse taslağı işlemesine gerek yoktur; canlı bağlam ve
ham kayıt devam eder. Taslak, asıl olarak farklı/yeni bir oturumun kapanışsız
kalmış eski oturumu kurtarması içindir. Paralel oturum bundan yararlanabilir ama
bu özel bir paralelleştirme mekanizması değildir. “Taslağı işle” demek taslağı
körü körüne terfi etmek değil; güncel omurgaya karşı doğrulayıp yalnızca kalıcı
olanı taşımaktır (codex 01a0ba74 · 19.09 19:39–19:41).

**Bak:** `rehber/sunum/slides/cumleler.html`, `araclar/gece_kayit.py`,
`araclar/oturum_basi.py`, `AGENTS.md` → “Gece taslakları”.

**Açık test:** Aynı oturum daha sonra normal kapanırsa eski `oto-<id>.md`
dosyasının temizlenip temizlenmediğini ölç.

**Bitiş ölçütü:** Slayt kapsamı dar ve doğru anlatır; aynı-oturum devamı,
başka-oturum devri ve terk edilmiş oturum kurtarması ayrı sınanır.

### 13. “Omurgayı kayıttan okur” ifadesi ham JSONL'ı saklıyor

Onuncu slayttaki “kayıt”, `oturumlar/` altındaki Markdown arşiv değildir;
Claude veya Codex'in konuşma sırasında tuttuğu ham JSONL günlüğüdür. Birinci
adımda omurga bu kayıttan çıkarılır; ikinci adımda insan-okur Markdown arşiv
yazılır. Normal kapanış omurgası kullanıcı mesajlarını taşır; `--tam` gece
yazıcısı gibi temiz bir ajana modelin metin cevaplarını da verir. Araç çıktıları
ve düşünme blokları iki biçimde de dışarıda kalır
(codex 01a0ba74 · 19.09 19:42).

**Bak:** `rehber/sunum/slides/kapanis.html`, `araclar/omurga.py`,
`araclar/kayit.py`.

**Bitiş ölçütü:** Slayt “sağlayıcının ham JSONL oturum günlüğünden” demeli ve
ham kayıt ile yazılan Markdown arşivi görsel olarak ayırmalı.

## Önerilen uygulama sırası

1. **Önce testler:** Codex hook güveni ve gerçek `SessionStart`; gece taslağının
   aynı/farklı oturum davranışı; normal kapanıştan sonra eski taslak kalıntısı.
2. **Sonra tasarım kararları:** erken devir eşiği ve davranışı; budama
   politikasının sınırı; ilk oturum adaptör protokolü.
3. **Sonra sistem:** ortak çekirdeği koruyarak Claude/Codex adaptörleri,
   bakım-adayı raporu ve başlangıç uyarıları.
4. **Sonra kalıcı not bakımı:** güncel durum ile tarihçeyi ayır, haritasız notu
   bağla, kapanmış maddeleri sıcak açık-uç listesinden çıkar. Silmeden/taşımadan
   önce kullanıcıya sor.
5. **En son sunum:** 13 bulgunun metin karşılıklarını slaytlara ve konuşma
   notlarına işle; kaynakla çelişki kalmadığını yeniden denetle.

## Kullanıcıdan beklenebilecek işlemler

- Codex Desktop'ta proje hook güvenini incelemek ve onaylamak.
- Gerçek yeni Claude ve Codex oturumları açarak ilk cevapları gözlemek.
- Erken devir için tercih edilen davranışı seçmek.
- Kalıcı not budamasında hangi tarihçenin taşınabileceğine karar vermek.
- Sunumun son metnini, özellikle kullanıcıya söylenecek kısa cümleleri onaylamak.

Bu işlemler gerektiğinde kullanıcıdan tek tek istenmeli; kullanıcı arayüzünde
yapılmamış bir işlem yapılmış varsayılmamalıdır.

## Tamamlanma ölçütü

- On üç maddenin her biri `kapandı`, `kısmen kapandı` veya gerekçeli `elendi`
  durumuna gelir.
- Sistem davranışı kaynak ve gerçek oturum testiyle doğrulanır.
- Claude ve Codex yeni oturumda aynı ortak bilgiyi alır; uygulama farkları
  açıkça görünür kalır.
- Kalıcı katmanın büyümesi yalnızca ölçülmez, insan denetimli bakım döngüsüne
  bağlanır.
- Sunum artık sistemi olduğundan daha otomatik, daha güvenli veya daha tamamlanmış
  göstermez.
