# Codex için sunum rehberi — cevap anahtarı değil, harita

Merhaba Codex. Bu dosyayı Claude (oturum 5c600e7e, 19.09.2026) yazdı.
Kullanıcı Yavuz, "İkinci Beyin — Kullanım Rehberi" adlı 14 slaytlık sunumu
seninle **sesli sohbet modunda** inceleyecek. Sorular soracak, itiraz edecek,
değerlendirmeni isteyecek.

Bu dosya cevapları vermiyor. Her slaytın **hangi dosyaya, hangi koda, hangi
ölçüme dayandığını** söylüyor. Soru gelince buradan yeri bul, oraya git,
cevabı oradan öğren.

---

## Önce bunlar

1. **Oturum başında oku:** `AGENTS.md` (ortak kurallar, sana otomatik yüklenmiş
   olmalı) ve `BEYIN.md` (harita). Hook'ların güven onayı henüz verilmediyse
   başlangıç bağlamı sana gelmemiştir. O durumda şunu çalıştır:
   `python araclar/oturum_basi.py --bicim duz`
2. **Sunumu göremezsin.** Sunum kullanıcının claude.ai hesabında ve gizli.
   Metni burada: `rehber/sunum/slides/<id>.html` (slayt başına bir dosya),
   sıra ve bölümler `rehber/sunum/deck.json` içinde. Her slaytın sonundaki
   `<aside>` konuşma notudur. Kullanıcı "5. slayt" derse aşağıdaki listeden
   dosyayı bul.
3. **Hafızadan ya da tahminle cevap verme.** Haritadaki dosyayı aç, oku, öyle
   söyle. Açamıyorsan (sesli modda araç kullanamıyorsan) bunu açıkça söyle:
   "Slayt şunu diyor, ama doğrulamak için şu nota bakmam gerekiyor."
4. **Doğruluk sırası:** kod (`araclar/*.py`) > `AGENTS.md` > `notlar/` > sunum.
   Sunum bir özet; kodla ya da `AGENTS.md` ile çelişirse **kod ve AGENTS.md
   doğrudur**. Çelişkiyi kullanıcıya söyle. Bu, değerlendirmenin en değerli
   bulgusu olur.
5. **Ölçülmüş bir iddiayı açmak için** notlardaki kaynak işaretçisini kullan.
   `(claude 7f10f7a3 · 18.09 02:41)` işaretçisinin komutu şu:
   `python araclar/oku.py 7f10f7a3 --saat 02:41`
   Bir konunun daha önce konuşulup konuşulmadığını bilmiyorsan ara:
   `python araclar/ara.py "terim"`
6. **Canlı durum soruları için** (örneğin "şu an kapanmamış oturum var mı",
   "bu gece ne olacak") yazmayan komutları çalıştır:
   - `python araclar/derle.py --kuru`
   - `python araclar/gece_kayit.py --kuru`
   - `derleme/son-calisma.json` dosyasını oku
   - `git log --oneline -5`
7. **Bu bir inceleme, düzenleme değil.** Hiçbir dosyaya yazma, hiçbir şeyi
   düzeltme. Bulduğun hata, çelişki ve önerileri aklında tut. Sohbetin sonunda
   kullanıcıya kısa bir liste olarak söyle; o, listeyi Claude'a taşır.
8. **Sesli cevap biçimi:** kısa, düz Türkçe. Dosya yolu, komut, tablo sesli
   okunmaz. "Kapanış ritüeli notunda yazıyor" de, `notlar/kapanis-ritueli.md`
   deme. Kullanıcı ayrıntı isterse yolu ekranda göstermek için ayrıca söyle.

---

## Slayt slayt harita

### 1 · Kapak — `kapak`
**Der ki:** Bu rehber, Claude, Codex ya da başka bir ajanla bu klasörün nasıl
kullanılacağını anlatıyor. Temeli 19 Eylül'de kurulan AGENTS.md düzeni.
**Bak:** `AGENTS.md` → "Bu dosya kimin için" bölümü · beynin amacı ve "Jarvis"
tanımı için `notlar/kullanici-baglami.md` → "Bu beynin amacı" bölümü.

### 2 · Beyin altı parçadan oluşur — `parcalar`
**Der ki:** BEYIN.md, notlar/, oturumlar/, araclar/, AGENTS.md ve gece
derleyicisi.
**Bak:** klasör düzeni için `BEYIN.md` ve `AGENTS.md` → "Klasör düzeni" ·
katmanların neden böyle ayrıldığı (kalıcı ve arşiv, sıcak ve soğuk) için
`notlar/ikinci-beyin-mimarisi.md` · derleyici için
`notlar/gece-derleyicisi.md`.

### 3 · Çekirdek ortak, adaptör uygulamaya göre — `ilke`
**Der ki:** Kural dosyası ortak; onu kendiliğinden okumak, hook ve bağlam
ölçümü uygulamanın yeteneği. Tablo sağlayıcıya değil uygulamaya göre: Claude
Code, Codex CLI, Codex Desktop, diğerleri. Her hücre ölçüldü, belge ya da
ölçülmedi etiketi taşır.
**Bak:**
- Tam tablo ve yeni uygulama tanıtma protokolü: `rehber/uygulama-adaptorleri.md`.
- Kural: `AGENTS.md` → "Ortak kural otomatik uygulama değildir".
- Güncel durum: `notlar/acik-uclar.md` → "Açık — sistem" madde 1. Önceki
  metin: `oturumlar/acik-uclar-tarihce.md`.
- "Arşive girer mi" sütunu: `araclar/kayit.py` → `oturumlar()` (Claude,
  Codex `sessions/` ve `archived_sessions/`).

### 4 · Claude: zaten hazır — `claude`
**Der ki:** Klasörü aç, başka ayar yok. Çalıştığını ilk cevaptaki oturum
kimliğinden anlarsın.
**Bak:**
- Hook'lar: `.claude/settings.json`.
- Oturum başında enjekte edilen metin: `araclar/oturum_basi.py` ve
  `araclar/oturum-basi.md`.
- Saat bilgisi: global ayar, `~/.claude/settings.json` → UserPromptSubmit.
- İçe aktarma: `CLAUDE.md` ilk satırı `@AGENTS.md`. Sınandığı an:
  `oturumlar/acik-uclar-tarihce.md` → "19 Eylül — madde 1'in ayrıntılı durum metni".
- Klasör taşınma riski (konuşma notunda geçiyor): `BEYIN.md` → "Bir sonraki
  oturuma not" ve `notlar/olculmus-bulgular.md` bölüm 4.

### 5 · Codex: CLI ve Desktop ayrı ölçülür — `codex`
**Der ki:** AGENTS.md iki uygulamada da yükleniyor (ölçüldü). Hook'lar üç olay,
dört komut. Güveni kullanıcı verir: CLI'da `/hooks` (belge), Desktop'ta akış
belgede yok (ölçülmedi). Desktop'ta bağlam sayacı yok; erken devir uyarısı
güven verilince ham kayıttan gelir.
**Bak:**
- AGENTS.md enjeksiyonunun ve hook metninin yokluğunun ölçümü:
  `notlar/acik-uclar.md` → "Açık — sistem" madde 1.
- Sayaç yokluğu ve %83 bulgusu: `notlar/olculmus-bulgular.md` bölüm 12.
- Senin kendi adaptörün: `.codex/hooks.json`, `araclar/codex-run-python.ps1`,
  `araclar/codex-time.ps1`, `araclar/precompact.py` (`--bicim codex`).
- Senin ölçüm raporun: `notlar/iki-ajan-calismasi.md` → "Asimetriyi gizleme".
  Tamamı kendi oturum kaydında: `python araclar/omurga.py 01a0b9eb --tam`.
- Hook olaylarının belgesi: OpenAI'ın Codex hooks ve advanced configuration
  sayfaları. Bunları sen bulmuştun.

### 6 · Başka bir uygulama: önce yeteneğini tanı — `diger`
**Der ki:** Ön koşul: yerel klasörü okuyup komut çalıştırabilmek. Kalıcı
talimat yeri varsa bir kez tek satır; yoksa **kullanıcı** her oturumun başında
ilk mesajı gönderir. Sınırı: refleks yok, konuşma arşive girmez.
**Bak:**
- Tanıtma protokolü: `rehber/uygulama-adaptorleri.md` → "Yeni bir uygulamayı
  tanıtma protokolü".
- `AGENTS.md` → "Oturum başı bağlamı" · `araclar/oturum_basi.py` → `--bicim duz`.
- "Arşive girmez" gerekçesi: `araclar/kayit.py` → `_claude_mesajlari` ve
  `_codex_mesajlari`. Başka biçim okuyucusu yok.
- **Doğrulanmadı:** Antigravity'nin AGENTS.md'yi kendiliğinden okuyup okumadığı.
  Kullanıcı sorarsa bunu söyle, istenirse web'den araştır.

### 7 · Bir oturumun yaşamı — `yasam`
**Der ki:** Aç, dinle, çalış, kapat, gece. Kapatmayı unutursan gece taslağı
yazılır.
**Bak:**
- Adımlar: `AGENTS.md` → "Oturum kapanışı".
- Kapanışın neden böyle tasarlandığı: `notlar/kapanis-ritueli.md`.
- Gece taslağı: `araclar/gece_kayit.py` (6 saatlik eşik `SESSIZLIK` sabiti) ve
  `notlar/gece-derleyicisi.md` → "Gece taslağı". Aynı oturuma dönüş,
  devralma ve terk: `AGENTS.md` → "Gece taslakları" ve sonraki paragraf.
- Bağlam uyarısı: `araclar/baglam.py` · `AGENTS.md` → "Erken devir".

### 8 · Duyabileceğin uyarılar — `uyarilar`
**Der ki:** Yedi uyarı: bağlam %50/%70, push, kesinti, kapanmamış oturum,
gece taslağı, bakım eşiği, kusurlu işaretçi. Sessizlik yalnızca bu tanımlı
uyarıların olmadığını söyler.
**Bak:**
- Gece derleyicisi uyarıları: `araclar/oturum_basi.py` → `derleyici_uyarilari()`
  (36 saat eşiği) · kaynağı `derleme/son-calisma.json`, yazanı `araclar/derle.py`.
- Bakım uyarısı: `araclar/bakim.py` → `olc()` ve `uyarilar()`.
- Bağlam uyarısı: `araclar/baglam.py` → `kontrol()`, çağıran `araclar/devir.py`.
- Gerekçeler: `oturumlar/acik-uclar-tarihce.md` (push olayı) ·
  `notlar/sunum-incelemesi-onarim-listesi.md` madde 7, 10, 11.

### 9 · Altı cümle yeter — `cumleler`
**Bak (cümle cümle):**
- "Oturumu kapatalım" → `AGENTS.md` → "Oturum kapanışı".
- "Daha önce konuşmuş muyduk" → `AGENTS.md` → "Arşivde arama" ·
  `notlar/arac-arsiv.md`.
- "Kalıcı nota yaz" → `araclar/oturum-basi.md` → "NE ZAMAN" ve "YAZMA".
- "Kaynağını göster" → `AGENTS.md` → "3. Kaynak göster" · `araclar/oku.py` ·
  denetim: `araclar/derle.py` → `isaretci_denetle()`.
- "Eski oturumun taslağını işleyelim" → `AGENTS.md` → "Gece taslakları" ve
  kapsam paragrafı. Aynı oturuma dönüşte geçerli değildir.
- "Sol'a devret" → `notlar/iki-ajan-calismasi.md` → "Pratik: nasıl çağrılır" ·
  alt ajanın kapanışı: `AGENTS.md`, "kapanan-oturum" paragrafının sonu.

### 10 · Kapanış: önce oku, sonra yaz — `kapanis`
**Der ki:** Ham JSONL günlüğü (uygulamanın) → omurga → Markdown arşiv
(`oturumlar/`). Kapanış satırı yalnızca gerçek geçişte, kullanıcı onayıyla.
Compact son ağdır; erken devir %50/%70'te uyarır.
**Bak:**
- Omurganın neyi taşıdığı (kullanıcı mesajı; `--tam` ile model metni):
  `araclar/omurga.py` başındaki açıklama · filtreler `araclar/kayit.py`.
- Adımlar: `AGENTS.md` → "Oturum kapanışı" 1–4.
- Neden: `notlar/kapanis-ritueli.md` → "Asıl tasarım kararı", "Kapanış işareti",
  "SessionEnd boşluğu ve compact'in yeri".
- Compact ağı: `araclar/precompact.py` ve `araclar/devir.py`. Gerçek
  sıkıştırmada ölçüldüğü an: `notlar/kapanis-ritueli.md` → "PreCompact".

### 11 · Gece 00:30 — `gece`
**Der ki:** Telafi, dedektör, gece taslağı, işaretçi denetimi, raporlar, yedek.
**Bak:**
- Akış: `araclar/derle.py` → `main()`.
- Zamanlama: `araclar/derle-gece.cmd` ve Windows Görev Zamanlayıcı'daki
  `playground-derleyici` görevi.
- Telafi ayarı ve "uyandırmaz" bilgisi: `notlar/gece-derleyicisi.md` → "18 Eylül".
- Taslak tavanı ve modeli: `araclar/gece_kayit.py` sabitleri (`GECE_SINIRI`,
  `VARSAYILAN_KOMUT`).
- Son çalışmanın sonucu: `derleme/son-calisma.json` · `derleme/gunluk/`.

### 12 · Bilmen gereken beş sınır — `sinirlar`
**Bak:**
- Side chat: `notlar/olculmus-bulgular.md` bölüm 6.
- Bulut sohbetleri: `notlar/capraz-arac-baglam.md` · `notlar/arac-izle.md`.
- İki ajanın garantisi: `CLAUDE.md` → refleks tablosunun altındaki Codex paragrafı · `notlar/iki-ajan-calismasi.md`.
- Hiç girmeyen katman: `notlar/ikinci-beyin-mimarisi.md` → "Katmanlar" ·
  `notlar/gece-derleyicisi.md` → "Git".
- Paralel çalışma: `notlar/agentic-yapi.md` · `notlar/acik-uclar.md` → "Ertelenenler".

### 13 · Başvuru kartı — `komutlar`
**Bak:** Her aracın dosyasının başındaki açıklama ve "Kullanım" bölümü
(`araclar/<ad>.py`) · arama araçları için `notlar/arac-arsiv.md`.

### 14 · Kapanış cümlesi — `son`
**Bak:** `notlar/kapanis-ritueli.md` → "Kaynak gösterme kuralı". Cümlenin
kökeni Avenox değerlendirmesi: `notlar/ikinci-beyin-mimarisi.md`.

---

## Sunumun bilinen zayıf noktaları — özellikle buralara bak

Bunları Claude kendisi işaretliyor. Saklanan zayıflık incelemeyi tiyatroya
çevirir.

19.09 onarımından sonra (onarım listesi, 13 + 1 madde) hâlâ geçerli olanlar:

- **Gece taslağı gerçek bir gecede hiç çalışmadı.** İlk gerçek çalışma
  20.09.2026 00:30; sonucu `derleme/gunluk/` ve `derleme/son-calisma.json`.
- **Codex Desktop'ta hook güveni ve yeni oturum testi yapılmadı.** Slayt 3 ve
  5 bunu "ölçülmedi" diye gösteriyor; test yapılınca etiket güncellenmeli.
- **Erken devir yalnızca Claude'da canlı sınandı** (bu oturumda %50 uyarısı
  geldi). Codex tarafı güvene bağlı.
- **Claude penceresi kalibre edildi, kayıttan okunmuyor:** model değişirse
  `araclar/baglam.py` → `PENCERE` tablosu güncellenmeli.
- **Kalıcı notlar hâlâ 100 KB üstünde:** kullanıcı yalnızca iki taşımayı
  onayladı. Bakım uyarısı sürüyor.

Onarımda düzeltilenler: "Derleyiciyi çalıştır"ın gerçekten yazdığı (slayt 8
konuşma notu), "Pazartesi haftalık" (slayt 11 artık gün vermiyor), bakım
eşiğinin görünmemesi (slayt 8 uyarısı).

## Bu sunum nasıl yazıldı

Claude oturumu `5c600e7e`, 19.09.2026 17:35'te istendi, aynı akşam yazıldı. Sunumun neden bu yapıda
olduğunu merak edersen:
`python araclar/omurga.py 5c600e7e --tam` ya da
`python araclar/oku.py 5c600e7e --saat 17:35-18:40`
