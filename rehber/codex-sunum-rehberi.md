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

### 3 · Çekirdek ortak, adaptör ince — `ilke`
**Der ki:** Tablo, üç ajan türünü karşılaştırıyor: kuralları nereden okuyor,
refleksleri var mı, arşive giriyor mu.
**Bak:**
- Karar ve gerekçe: `notlar/acik-uclar.md` → "19 Eylül'de açılanlar" madde 1.
- Claude'un refleksleri: `CLAUDE.md` · Codex'in refleksleri: `.codex/hooks.json`.
- "Arşive girer mi" sütunu: `araclar/kayit.py` → `oturumlar()`. Yalnızca
  Claude ve Codex kayıt biçimlerinin okuyucusu var.
- İki ajanın tarihçesi: `notlar/iki-ajan-calismasi.md`.

### 4 · Claude: zaten hazır — `claude`
**Der ki:** Klasörü aç, başka ayar yok. Çalıştığını ilk cevaptaki oturum
kimliğinden anlarsın.
**Bak:**
- Hook'lar: `.claude/settings.json`.
- Oturum başında enjekte edilen metin: `araclar/oturum_basi.py` ve
  `araclar/oturum-basi.md`.
- Saat bilgisi: global ayar, `~/.claude/settings.json` → UserPromptSubmit.
- İçe aktarma: `CLAUDE.md` ilk satırı `@AGENTS.md`. Sınandığı an:
  `notlar/acik-uclar.md` madde 1.
- Klasör taşınma riski (konuşma notunda geçiyor): `BEYIN.md` → "Bir sonraki
  oturuma not" ve `notlar/olculmus-bulgular.md` bölüm 4.

### 5 · Codex: bir kerelik onay — `codex`
**Der ki:** Codex'i bu klasörde aç, bir kez `/hooks` ile üç hook'a güven ver.
**Bak:**
- Senin kendi adaptörün: `.codex/hooks.json`, `araclar/codex-run-python.ps1`,
  `araclar/codex-time.ps1`, `araclar/precompact.py` (`--bicim codex`).
- Senin ölçüm raporun: `notlar/iki-ajan-calismasi.md` → "Asimetriyi gizleme".
  Tamamı kendi oturum kaydında: `python araclar/omurga.py 01a0b9eb --tam`.
- Hook olaylarının belgesi: OpenAI'ın Codex hooks ve advanced configuration
  sayfaları. Bunları sen bulmuştun.

### 6 · Başka bir ajan: ilk mesajla bağla — `diger`
**Der ki:** Hook'u olmayan araçlar için tek satırlık kural ya da her oturumun
ilk mesajında bir komut. Sınırı: refleks yok, konuşma arşive girmez.
**Bak:**
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
  `notlar/gece-derleyicisi.md` → "Gece taslağı".

### 8 · Oturum başında duyabileceklerin — `uyarilar`
**Der ki:** Beş uyarı (push, kesinti, kapanmamış oturum, gece taslağı, kusurlu
işaretçi); her birinin anlamı ve kullanıcının ne diyeceği.
**Bak:**
- Uyarıları üreten kod: `araclar/oturum_basi.py` → `derleyici_uyarilari()`
  (36 saat eşiği burada).
- Uyarıların kaynağı: `derleme/son-calisma.json`. Onu yazan:
  `araclar/derle.py` → `main()`.
- Gerekçe: 19 Eylül gecesi push'un sessizce düşmesi.
  `notlar/acik-uclar.md` → "19 Eylül'de açılanlar" madde 2.

### 9 · Altı cümle yeter — `cumleler`
**Bak (cümle cümle):**
- "Oturumu kapatalım" → `AGENTS.md` → "Oturum kapanışı".
- "Daha önce konuşmuş muyduk" → `AGENTS.md` → "Arşivde arama" ·
  `notlar/arac-arsiv.md`.
- "Kalıcı nota yaz" → `araclar/oturum-basi.md` → "NE ZAMAN" ve "YAZMA".
- "Kaynağını göster" → `AGENTS.md` → "3. Kaynak göster" · `araclar/oku.py` ·
  denetim: `araclar/derle.py` → `isaretci_denetle()`.
- "Gece taslağını işleyelim" → `AGENTS.md` → "Gece taslakları" paragrafı.
- "Sol'a devret" → `notlar/iki-ajan-calismasi.md` → "Pratik: nasıl çağrılır" ·
  alt ajanın kapanışı: `AGENTS.md`, "kapanan-oturum" paragrafının sonu.

### 10 · Kapanış: önce oku, sonra yaz — `kapanis`
**Der ki:** Kapanışın beş adımı ve "compact bir kapanış değildir".
**Bak:**
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
- Paralel çalışma: `notlar/agentic-yapi.md` · `notlar/acik-uclar.md` madde 5.

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

- **Gece taslağı gerçek bir gecede hiç çalışmadı.** Yalnızca elle sınandı.
  İlk gerçek çalışma 20.09.2026 00:30. Sonucunu `derleme/gunluk/` ve
  `derleme/son-calisma.json` söyler.
- **Codex tarafı yarı ölçülü.** Compact uçtan uca ve modelin bağlamı
  gerçekten gördüğü ölçülmedi. Senin raporunda yazıyor.
- **`/hooks` onayı** bu rehber yazılırken henüz verilmemişti. Slayt 5 bunu
  varsayıyor.
- **Slayt 8'deki "Derleyiciyi elle çalıştır"** gerçek bir çalıştırmadır: rapor
  yazar, commit atar, push eder. Denemek için `--kuru` gerekir. Slayt bunu
  söylemiyor.
- **Slayt 11'deki "Pazartesi haftalık":** gerçekte "bu hafta üretilmediyse ilk
  gecede" çalışıyor (`araclar/derle.py` → `haftalik_gerekli()`). Slayt
  basitleştirmiş.
- **Kalıcı notlar 118 KB.** `AGENTS.md` 65 KB'lık eşikte "hepsini oku"dan
  "haritayı oku, gerekeni aç"a geçmeyi söylüyor. Sunum bu eşikten hiç
  bahsetmiyor.

## Bu sunum nasıl yazıldı

Claude oturumu `5c600e7e`, 19.09.2026 17:35'te istendi, aynı akşam yazıldı. Sunumun neden bu yapıda
olduğunu merak edersen:
`python araclar/omurga.py 5c600e7e --tam` ya da
`python araclar/oku.py 5c600e7e --saat 17:35-18:40`
