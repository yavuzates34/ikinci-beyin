# Tam otomasyon planı — 21 Eylül 2026

Oturum kaydı değil: **iş belgesi.** Kullanıcının "sistem tam otomatik olsun"
kararından çıkan tasarım ve açık listesi. Astra'ya devredilecek işin kaynağı
budur. Kapanış işareti taşımaz; iş bitince durumu buradan güncellenir.

> Merkez: [[BEYIN]] · İlgili: [[acik-uclar]] · [[agentic-yapi]] ·
> [[kapanis-ritueli]] · [[gece-derleyicisi]] · [[iki-ajan-calismasi]] ·
> [[astra-denetim-bulgulari]] · [[2026-09-19-sunum-onarim-listesi]]

Kaynak: 20–21.09 gecesi Claude ile planlama konuşması
(claude 96517e26 · 20.09 20:28 – 21.09 01:11).

---

## Neden

Kullanıcının gerekçesi (20.09 20:28): *"İşler gittikçe birikiyor,
karmaşıklaşıyor ve ben bunu insan olarak takip edemiyorum."* Hedef: ne
düzeltilecekse, ne raporlanacaksa, ne derlenecekse sistem kendi yapsın; saat
kaçırılsa bile ilk fırsatta telafi etsin; arka planda, kullanıcıyı rahatsız
etmeden.

Kullanıcının benzetmesi, tasarım ilkesi olarak kabul edildi: *"Musluğu açıp
sebzeyi yıkayan birisi şehir şebekesinin nasıl çalıştığını biliyor mu?"* Yani
sisteme dair soru kullanıcıya sorulmaz. **Ama** şebekenin basınç sensörü ve
nöbetçi ekibi de vardır — kimse kullanıcıya sormaz, birileri *uyarılır*. İkinci
yarı atlanırsa "rahatsız etmeyen sistem", sessizce çürüyen sistem olur.

## Tasarımın çekirdeği: kapanış yerine eşik

**Sorun.** Kapanış ritüeli kullanıcının "oturumu kapatalım" demesine bağlı.
Sistem uygulamanın arayüzünde oturum açıp kapatamaz — bu harness yeteneği,
model yeteneği değil. Yani ritüelin bugünkü tetikleyicisi tam otomasyonla
çelişiyor (kullanıcı, 20.09 20:35).

**Elenen fikir: "compaction'ı iyileştirip kapanışı gereksiz kılmak."**
Compaction hafıza değil, modelin kendi bağlamını sıkıştırmasıdır — kayıplıdır
ve kaybettiğini söylemez. `AGENTS.md` kapanışı bilerek **okumaya** dayandırır
(`omurga.py`, ham kayıt), hatırlamaya değil. Compaction'ı hafıza yoluna
çevirmek, sistemin kaçmak için kurulduğu şeye geri dönmektir. Ayrıca
[[kapanis-ritueli]] 16.09'da bunu bir kez karara bağlamış: PreCompact **ana yol
değil, güvenlik ağı**, çünkü rastgele bir anda, cümle ortasında tetiklenir.

**Kabul edilen fikir (kullanıcı, 20.09 20:45).** Ritüeli compaction'ın
tetiklemesine bırakma; **eşiğe** bağla ve compaction'dan *önce* çalıştır.
Model %90'da değil, hâlâ iyi durumdayken seçim yapar. İtirazın konusu böylece
ortadan kalkar.

**Kapanış yerine işlenme damgası.** Bugün `kapanan-oturum: <id>` ikili bir
cevap verir: kapandı / kapanmadı. Hiç bitmeyen oturumda bu satır hiç yazılamaz
ve oturum sonsuza kadar "işlenmemiş" görünür. Yerine damga konur: *"bu oturumun
şu saate kadarki içeriği terfi edildi."* Sistem bir sonraki turda damgadan
ileri okur, kalıcı olanı alır, damgayı ilerletir. Oturumun bitmesine gerek
kalmaz.

**Damga kuralı (Astra'ya not).** Damga, kimliğin tek ve tekil olduğunu
varsaymamalı. İki olgu ölçüldü: (a) klasör taşınınca oturum fork'lanıp kimlik
değişti, `6052d412` → `3c1530e9` ([[olculmus-bulgular]] §4); (b) aynı tam
kimlik birden çok dosyaya yayılabiliyor — Astra'nın bulduğu 81 gizli mesaj
bundandı. Fork olursa zincirlenebilmeli, çok dosyalıysa hepsi birlikte
okunmalı.

## Compaction tarafı

**Uyarı kalır, iş de eklenir.** İkisi alternatif değil, farklı işler:

- **Terfi işi otomatik** — kullanıcı onay vermese de kalıcı olan diske geçer.
- **Compact kararı** kullanıcıda ya da orkestratörde kalır; sistem arayüzden
  zaten tetikleyemez.

Orkestratör gerekçesi kullanıcıdan (20.09 20:45): bağlamı dolmuş bir ana ajan
altındaki alt ajanları yönetemez. Yani %50 uyarısı yalnız kullanıcıya değil,
**orkestratöre de** ulaşabilmeli.

**Sıkıştırmayı gerçekten tetikleyen şey hook değil, ayar.** Ölçüldü
(claude 96517e26 · 21.09 00:56): `.codex/config.toml` içinde
`model_auto_compact_token_limit = 750000`, etkin pencere 828.400 → harness
kendiliğinden ancak **%90,5**'ta sıkıştırıyor. Bizim %50/%70 eşiklerimiz
sıkıştırmıyor, yalnız omurgayı diske alıp uyarıyor. Kimse butona basmazsa
bağlam %90'a kadar dolar.

Bu **arayüze müdahale değil, yapılandırma**: uygulamaya kendi eşiğinin nerede
olduğu söylenir, sıkıştırmayı yine uygulama yapar. Kapının açık olduğu ölçüldü
(Astra, `config/read` ile doğruladı).

**Öneri: eşik %70'e çekilsin** (`750000` → `~580000`). Gerekçe: %50 ritüeli
çalışır ve uyarır; iş devam eder; %70'te ikinci ritüel çalışır ve harness tam o
noktada sıkıştırır — aradaki boşluk ≈ sıfır. %50'ye çekmek sıkıştırma sıklığını
ikiye katlar ve her sıkıştırma kayıplı bir yeniden yazmadır; karşılığında
kazanılan 20 puanlık marj o bedeli hak etmiyor. **Başlangıç değeri olarak
alınsın**, bir hafta ölçülsün, veriye göre 60 ya da 50'ye indirilsin.

**PreCompact kalkmaz, rolü değişir: artık toplayıcı.** Üç sebeple: (a)
compaction eşiğin altında da tetiklenebilir — `/compact` elle her an
yazılabilir; (b) son ritüel ile sıkıştırma arasında yeni malzeme birikir, onu
PreCompact toplar; (c) [[kapanis-ritueli]]'nin kendi dersi: *"İki ayaklı, çünkü
tek ayak güvenilmez"* — ve o karar 16.09'da kendini ödedi. Maliyeti de sıfır
(saf Python). Ne zaman kaldırılabilir: %50 ritüelinin her uygulamada güvenilir
çalıştığı **ve** eşik altı sıkıştırmanın hiç olmadığı ölçülürse.

**En kritik teknik engel: ölçüm turun içinde yok.** Astra'nın N6 bulgusu —
bağlam kontrolü yalnız `UserPromptSubmit`'te. Kullanıcı mesaj yazmazsa olay
**hiç gerçekleşmez**. Tek bir turda 40 dakika araç çağrısı yapılabilir ve bağlam
%45'ten %95'e çıkabilir; o turda tek ölçüm yapılmaz. Yani "bağlamı %50'de tut"
hedefi doğru ama **mevcut mekanizma onu uygulayamaz**: ölçen şey yalnız turlar
arasında okuyor, dolduran şeyse turun kendisi.

Çözüm dört katmanlı:

1. **`PostToolUse`** — her araç çağrısından sonra ölçüm. Ucuz kapı: önce ham
   kaydın **dosya boyutuna** bak (tek sistem çağrısı); belli bir adım
   büyümediyse hiçbir şey yapma.
2. **Konuşabilir mi — ÖLÇÜLMELİ.** [[agentic-yapi]]'nin ölçülmüş kuralı: bir
   hook modele ancak hemen ardından bir model turu başlayacaksa konuşabilir.
   `PostToolUse` turun içinde olduğu için konuşabilmeli — **ama bu kuraldan
   çıkarım, ölçüm değil.** Her uygulamada ayrı ölçülsün. Konuşamazsa
   deterministik ayak yine çalışır: omurga diske yazılır, veri kurtulur.
3. **`Stop`** — tur sonunda tetiklenir. O turdaki taşmayı önlemez ama her turda
   en az bir ölçüm garantisi verir.
4. **Dış gözcü** — hook'u olmayan uygulamalar için. Veriyi kurtarır, modele
   **konuşamaz**. Sağlayıcıdan bağımsızlığın gerçek tavanı burasıdır ve sunumda
   böyle yazmalı.

**Sağlayıcı asimetrisi:** Codex'in ölçülmüş olay listesinde `PostToolUse`
**yok** (`SessionStart`, `UserPromptSubmit`, `PreCompact`, `Stop`,
`SessionEnd`). Yani Claude'da Katman 1 kurulsa bile Codex'te `Stop`'la
yetinmek gerekebilir. `AGENTS.md`'ye ve sunuma açıkça yazılsın, gizlenmesin.

## Avenox ölçümü: eşiğin anlamı değişti (21.09 05:48)

Lab'da Avenox v3.1.0 kuruldu ve hook bağlantıları ölçüldü. İki bulgu bu
planın çekirdeğini değiştiriyor.

**Ölçüm 1 — altı olay, sıfır eşik.** Hem Claude hem Codex tarafında altı
olaya birden bağlanmışlar: `SessionStart`, `UserPromptSubmit`, `PostToolUse`,
`Stop`, `PreCompact`, `SessionEnd`. `PreCompact` listede var ama orada özel
bir kurtarma mantığı yok — sadece kuyruğu boşaltmak için bir fırsat daha.
Ve bağlam doluluğu ölçümü **hiç yok**; eşik kavramı kodda geçmiyor
(`CONTEXT_LIMIT = 4000` alıntı penceresiyle ilgili, bağlam penceresiyle değil).

**Ölçüm 2 — neden ihtiyaçları yok.** Sürekli yazıyorlar: `PostToolUse` ve
`Stop` ile her turda makbuz düşüyor. Biriktirmedikleri için kaybedecek
birikmiş bir şeyleri yok.

**Çıkarım.** Bizim kapanış ritüelimiz var çünkü anlamı oturum boyunca
biriktirip sonunda yazıyoruz. Biriktirmek bir **teslim tarihi** yaratır;
compaction'ın tehdit ettiği şey o teslim tarihidir. Onlarda teslim tarihi
olmadığı için compaction bir olay, karar değil. Yani "oturum mu değiştirmeli,
compaction mı yapmalı" sorusu onların mimarisinde **sorulmuyor**. Bizde
sorulmasının sebebi bir tasarım tercihinin yan etkisi.
(claude 96517e26 · 21.09 05:48)

### Birleştirme: üç katman

Kod tabanları birleştirilmez — iki sistem tek kasada iki doğruluk kaynağı
demektir. Alınacak olan mekanizma.

1. **Sürekli makbuz (onlardan).** Emniyet ağı. Olay bazında, kaynağıyla
   birlikte ham olgu yazılır. Model gerektirmez. Tek işi hiçbir olgunun
   kaybolmaması.
2. **Dönemsel sentez (bizden).** Makbuz yığını şunu asla vermez: hangi karar
   alındı ve **neden**, ne denendi ve **elendi**. Elenen fikir hiçbir makbuzda
   iz bırakmaz, çünkü olmayan şeydir. Onu ancak bağlamın tamamına bakan
   yazabilir.
3. **Bayatlama işareti (onlardan, uyarlanarak).** Onların hash'i "alıntıladığım
   kaynak dosya değişti mi" sorusunu çözer. Bizim işaretçimiz ham oturum
   kaydına bakar ve **ham kayıt değişmez**, yalnız eklenir — yani o problem
   bizde yok. Bizim bayatlama problemimiz başka: *"19.09'da ölçtüğüm şey bugün
   hâlâ doğru mu?"* Çözüm, hash'i konuşmaya değil **anlatılan şeye** takmak:
   `derle.py` davranışına dair bulgu `derle.py`'nin hash'ini taşısın, dosya
   değişince bulgu kendini "ölçüm eskimiş olabilir" diye işaretlesin. Bugün
   böyle bir şey yok; bayatlamış ölçümü yalnız insan fark ediyor.

Alınmayacaklar: sqlite, kendi CLI'ları, kasa düzeni, `receipts/` klasörü.
Bizde kalacaklar: bağlam doluluğu ölçümü, gece derleyicisi, arşiv arama.

### Eşik artık kurtarma değil, sentez zamanı

Yukarıdaki "Tasarımın çekirdeği" bölümü eşiği **acil kayıt** olarak yazıyor:
*bağlam %50'ye gelince her şeyi yaz, yoksa kaybolur.* Makbuz katmanı gelirse
bu gerekçe düşer — kaybolacak ham malzeme kalmaz. Eşiğin yeni anlamı:
*"karar ve gerekçeleri damıtmak için bağlam hâlâ yeterince temiz."*
Kaçırılması felaket değil, gecikme. Önceki metin kayıt olarak duruyor.

### Elenen fikir: dört katmanlı tur içi bağlam ölçümü

**Karar: planlanan iş olmaktan çıkarıldı** (kullanıcı, 21.09 06:06).
Yukarıdaki "Çözüm dört katmanlı" listesi — `PostToolUse` kapısı, uygulama
başına "konuşabilir mi" ölçümü, `Stop` yedeği, dış gözcü — kayıt olarak
duruyor ama yapılacak iş değil.

**Gerekçe: dayandığı varsayım ölçümle çürüdü.** Korku şuydu: *"compaction
gelirse oturumda biriken şey kaybolur."* 21.09 02:42'de elle `/compact`
yapıldı ve sonrasında omurga okundu: 39, 40, 41 numaralı kullanıcı mesajları
zaman damgalarıyla yerinde duruyordu. Compaction **diskteki ham kaydı
silmiyor**, modelin çalışma belleğini sıkıştırıyor ve dosyaya özeti *ekliyor*.
§17'de ölçülen kusur da buydu: özet eklendi, orijinaller silinmedi. Ritüel
zaten diskten okumak üzere kurulu (`AGENTS.md`: *"kapanış hatırlamaya değil
okumaya dayanmalı"*). Yani korunan kayıp büyük ölçüde gerçekleşmiyor.

**Yerine kalan, ucuz olan.** Zaten elde olan noktalarda (`UserPromptSubmit`,
`Stop`) bir sayı ölçülür. Amacı kaybı önlemek değil, *"sentez için iyi bir an
mı"* sorusuna cevap vermek. Maliyeti sıfır, kod zaten yazılı.

**Elenmeyen, gerçek kalan üç şey.** (a) §17 kusuru gerçek ama çaresi bağlamı
düşük tutmak değil, `omurga.py`'nin sıkıştırma özetini tanıyıp ayırması.
(b) Sentez kalitesinin yüksek bağlamda düşmesi makul ama **ölçülmedi**.
(c) Alt ajan yöneten orkestratörün alan ihtiyacı gerçek — ama o bellek değil,
**canlı koordinasyon durumu** problemidir; ayrı iş.

**Asıl teşhis.** Bağlam koruma çabası, makbuz katmanının yokluğunu telafi
ediyordu. Biriktirip sonda yazdığımız için teslim tarihimiz var; teslim tarihi
olduğu için ona zırh icat ettik. Sürekli yazılırsa teslim tarihi kalkar ve
zırh gereksizleşir. Otomasyon tarafında da aynı: saatlerce kendi kendine
çalışan bir sistemde doğru savunma "bağlamı düşük tut" değil, **iş durumunu
adım adım diske yazmak.**

**Yeni sıra:** (1) `omurga.py` §17 düzeltmesi, (2) sürekli makbuz katmanı,
(3) telafi kuyruğu, (4) bayatlama işareti.

**Dürüstlük notu.** Dört katmanlı çözüm 21.09 gecesi bu oturumda tasarlandı ve
aynı oturumda, birkaç saat sonra elendi. Aradaki fark Avenox ölçümüdür.
Tasarım yanlış değildi; dayandığı varsayım yanlıştı.
(claude 96517e26 · 21.09 06:06)

### Düzeltme: onlarda da sentez katmanı var

Yukarıda "makbuz yığını karar ve gerekçe vermez, o bizim katmanımız" denmişti.
Ölçüm bunu kısmen çürütüyor: `Last-Session.md`'nin kendi talimatı
*"Anlamlı çalışma sonunda **sonuç, gerekçe, açık kalan adım** ve kaynak
bağlantılarını buraya yaz"* diyor; `Threads.md` açık konuları tutuyor;
`SessionStart` enjeksiyonu ajana *"bitmemiş iş için Last-Session/Threads'e
bak"* diye başlıyor. Yani sentez onlarda da var, yalnız teslim tarihine bağlı
değil.

Gerçekten bize özgü kalan tek şey: **"ne denendi ve elendi".** Onların
talimatında geçmiyor, bizim ritüelimizde zorunlu üç sorudan biri. En pahalı
bilgi, çünkü elenen şey hiçbir yerde iz bırakmaz.
(claude 96517e26 · 21.09 06:06)

## Astra denetimi: üç iddia da düştü, karar (b) (21.09 07:26)

Astra 18 kontrolü tamamladı: 14 doğrulama, 3 çürütme, 1 ölçülemeyen.
Rapor ve yeniden üretim kodu denetçinin çalışma dizininde; özetler burada.
**Kararı: bugün (b)** — mevcut sistemi koru, doğrulanan mekanizmaları
seçerek al. (c) koşullu aday.

### Elenen: "Avenox sürekli makbuz yazıyor, teslim tarihi yok" (Y8)

Bu gecenin mimari anlatısının temeliydi. Ölçüm çürüttü: `PostToolUse` → `Stop`
çalıştırıldığında **olay metadatası ve kaynak indeksi oluşuyor, receipts
tablosu 0, receipt dosyası 0.** Makbuz ayrı bir `receipt` komutuyla, **ajanın
verdiği** summary/refs ile yazılıyor. Üstelik `PostToolUse` matcher'ı yalnız
`Edit|Write|apply_patch`; kabuktan yazma tetiklemiyor.

Sonuç: onlarda da "ajan yazarsa yazılır" bağımlılığı var. "Biriktirmiyorlar,
o yüzden compaction tehdit değil" çıkarımı geçersiz.

### Elenen: "iki sistem farklı kaynak okur, çakışmazlar" (İ2)

Karşı örnek ölçüldü: biri açıkça `ozel`, biri etiketsiz (varsayılanla `ozel`)
iki sentetik not. **Avenox ikisini de `internal` indeksledi ve içeriği bağlama
verdi**; Jev gölge modu açıkken canary'ler sağlayıcı taşıyıcısına ulaştı.
Avenox Markdown tarıyor, bizim notlarımız da Markdown; `gorunurluk.json`'dan
haberi yok. Ayrıca iki sistem **aynı anlamsal alanları** üretiyor: kullanıcı
kuralı, gerekçe, son oturum, açık iş.

### Elenen: "hash'i anlatılan şeye tak, tek dosya yeter" (İ3)

Karşı örnek bizim kendi commit'imiz: `39712b5`'te `derle.py` hash'i birebir
aynı (`37718c59…`), değişen `kayit.py`. Aynı işaretçi önce geçerli, sonra
"o damgada mesaj yok" verdi. Hedef dosyanın hash'i yararlı bir işaret ama
**tek başına yetersiz**; bağımlılık + ayar/sürüm kapsamıyla tutulmalı. Salt
yorum değişikliği de ters yönde yanlış alarm verir.

### Ölçülemedi: "dört katmanlı ölçüm gereksiz" (İ1)

Y10 desteklendi — 02:42 anlık görüntüsündeki **41 mesajın 41'i** ham kayıtta
duruyor. Ama sınır metadatası: canlı bağlam **396.006 → 20.070** token.
*Diskten kurtarılabilirlik, işin ortasında doğru kısıtlarla devam edebilmek
demek değil.* Dayanağım olan "makbuzlar zaten düşüyor" da Y8'de çürüdü.
Astra tersini de kanıtlamıyor: karar, **uzun tek tur + compact + kesinti**
senaryosunda kaydedilmiş iş durumunun geri kazanımı ölçülmeden verilmemeli.

### Düzeltmeler

- **Sürüm ayrımı (Y7).** `~/kasa/avenoxbeyin` = HEAD/`aef7c14`, kurulu kasa =
  v3.1.0/`e112d8a`. Okuduğum `docs/v3/JEV.md` kurulu sürümü anlatmıyor.
- **Gizli veri süzgeci güvenlik sınırı değil (Y4).** Varsayılan kapalı;
  açıkken bile `metadata`/`title` alanındaki anahtar diske yazıldı.
- **Makbuzsuz tur sinyali kalıcı değil (D4).** Sonraki `UserPromptSubmit`'te
  eski kayıt kayboluyor (1 → 0).
- **`notlar/` 146.398 bayt (143,0 KiB)**, "130 KB" bayatmış.
- **Y11 güçlendi.** VDS bellek rezervasyonu yokluğu, GuestLib API'si doğrudan
  çağrılarak teyit edildi; "araç okuyamadı" kaçamağı elendi.

### (c) için Astra'nın şartları

Beş sözleşme ölçülmeden (c) karar olamaz: bilinmeyen görünürlük private kalır ·
her paylaşılan dosyanın tek yazarı olur · makbuz/son-oturum/açık-iş kayıtları
birbirini çoğaltmaz · compact/kesinti sonrası iş durumu gerçekten geri gelir ·
geri alma mevcut notları ve izinleri korur.
(claude 96517e26 · 21.09 07:29)

## Kabul edilen politikalar

**1. Kural `AGENTS.md`'de, uygulanışı adaptörde.** Sözleşme ortak dosyada
durur ("%70 civarında sıkıştırılır, öncesinde ritüel çalışır"); her uygulama
izin verdiği kadarıyla uygular. Ayarı açan uygulamada tam otomatik, açmayanda
yarı otomatik. `rehber/uygulama-adaptorleri.md` tablosunda yeni uygulamanın
hücresi **"ölçülmedi"** diye başlar.

**2. Her şey taşımadır, hiçbir şey silinmez.** İlk taslak "geri alınabiliyorsa
yap, alınamıyorsa sor" idi; kullanıcı haklı olarak kırdı: *"o raporu ben
uygulamayacaksam, sistem de uygulamayacaksa kim uygulayacak?"* Uygulayıcısı
olmayan rapor çöptür — projenin kendi uyarısı da bu (*"boşaltılmayan gelen
kutusu çöplüğe döner"*).

Doğru çözüm raporu gereksiz kılmak: **budama zaten silme değil, taşımadır**
(`AGENTS.md`: kapanan madde tarihçeye taşınır, silinmez). Taşıma git'te izini
bırakır, geri alınabilir, dolayısıyla **otomatik olabilir** — onay da rapor da
gerekmez. Git dışı dosyalar (`derleme/omurga-anlik/`) için kural: silme yerine
**soğuk klasöre taşı**. Geriye insan işi olarak yalnız "disk gerçekten dolarsa"
kalır; o da rutin rapor değil, nadir bir alarmdır ve cevaplanmazsa bir şey
bozulmaz.

**3. Token harcaması takvime değil, yeni içeriğe bağlanır.** Bugün böyle ve
korunmalı: `derle.py` saf Python (sıfır token); model çağıran tek parça
`gece_kayit.py` ve kapısı dar (bu projenin kapanmamış oturumu + 6 saat
sessizlik). Ölçüldü: on gün kullanılmazsa aday olmaz, `gece_kayit.py --kuru`
→ `aday yok` (claude 96517e26 · 21.09 00:05). Otomasyonda asıl risk ters
yönde: hatalı bir döngü aynı içeriği tekrar tekrar terfi ederse kota yanar.
Korumalar: (a) harcama yalnız damganın ilerisinde yeni içerik varsa tetiklenir;
(b) günlük sert tavan.

## Açıklar — 7 madde, 3 küme

### A. Otomasyonun çalışması için şart

**1. Telafi kuyruğu.** Yapılamayan iş diske yazılır ve her fırsatta yeniden
denenir: ağ geldiğinde, oturum açıldığında, herhangi bir hook tetiklendiğinde.
Push bunun içinde — `derle.py` commit atıyor ama push'u *"kullanıcı hazır
olduğunda"*ya bırakıyor; 19.09'da push düştü ve borç elle kapandı. Kullanıcının
"saat kaçırılsa bile ilk internet erişiminde yapsın" isteği tam olarak budur.
**Bu olmadan sistem otomatik değil, sadece zamanlanmış olur.**

**2. Damga, kimlik değişimine ve çok dosyalılığa dayanıklı olmalı.** Ayrı iş
kalemi değil; damga tasarlanırken uyulacak kural (yukarıda).

### B. Paralelleşme için şart — ikinci oturum açılmadan önce

**3. Sahiplikle bölme (eski 3 ve 4 birleşti).** Kullanıcının önerisi — commit'e
orkestratör karar versin — doğru yönde ama dar: çakışma yalnız `git commit`'te
değil, **dosya düzeyinde** olur. İki ajan aynı notu açıp yazarsa biri diğerini
ezer, commit'i kim atarsa atsın.

Doğru kural kilit değil **mülkiyet**: alt ajan yalnız **kendi** dosyalarına
yazar (kendi oturum kaydı, kendi çıktısı); paylaşılan katmana (`notlar/`,
`BEYIN.md`) ve commit'e yalnız **orkestratör** dokunur. Paylaşılan dosyanın tek
yazarı olduğu için çakışma yapısal olarak imkânsızlaşır. Yan fayda: alt ajan
ölse bile kendi kaydı diskte kalır.

Bedeli: orkestratör **tek arıza noktası** olur. İki sonucu var — (a) bağlamı
dolarsa her şey durur, yani orkestratörün eşik disiplini alt ajanlardan **daha
sıkı** olmalı; (b) yazma ortasında ölürse yarım iş kalır, çaresi 1. madde.

**4. Uyarı kanalı orkestratöre ulaşmıyor.** Bugünkü devir kutusunun üç kusuru
ölçülmüş ([[agentic-yapi]]): **tek alıcılı** (kim okursa alır ve boşaltır),
**tek mesajlık** (kuyruk yok), **pasif** (mesaj bırakmak karşı tarafı
tetiklemez). Mesh için yeniden tasarım gerekiyor.

### C. Güvenlik ve denetim

**5. Örneklemeli içerik denetimi.** [[acik-uclar]] madde 2, hiç kurulmadı.
Bugün "işaretçi var mı" mekanik olarak denetleniyor; **"işaretçinin gösterdiği
şey gerçekten orada mı" denetlenmiyor.** Terfiyi makine yapmaya başlayınca
uydurmayı yakalayan tek mekanizma bu olur.

Buraya eski "terfi yetkisi" maddesi de karıştı. Kullanıcının itirazı haklıydı:
içerik kararını bugün de model veriyor, kullanıcı yalnız tetikliyor. Değişen
karar veren değil, **kararın koşulları**: bugün oturumda bir kez, ham kaydın
tamamına bakarak, kullanıcının "bu konu bitti" dediği sınırda; otomatikte
defalarca, iş sürerken, damgadan sonraki dilime bakarak, kimse bakmadan. Yani
sorun yetki değil, **hatanın sessizce birikmesi.**

**Ek ölçüt (avenox v2'den alınan fikir):** hafızanın çalıştığı, **yeni bir
oturum kayıtlı bir bilgiyi geri okuyana kadar** iddia edilmez. Bizde yok; bugün
terfi başarısı "dosyaya yazıldı mı" diye ölçülüyor, "sonraki oturum görebildi
mi" diye değil. Ucuz, çünkü model yargısı gerektirmiyor.

**6. Sağlık dosyası + eskime alarmı.** Bugün tek geri bildirim kanalı oturum
başı uyarısı — kullanıcı oturum açmazsa bozulmayı öğrenemez. Gece görevi iki
gece sessizce öldü ve ancak bakılınca çıktı. Kural: **her otomatik işin son
başarılı çalışma zamanı tutulur, eskirse alarm üretir.**

**7. Token tavanı.** Politika 3'ün uygulanması: harcama yeni içeriğe bağlı,
üstüne günlük sert tavan.

## Sıra

1. **Telafi kuyruğu (1)** — otomasyonun tanımı bu; en somut, en az tartışmalı.
2. **Örneklemeli denetim (5)** — otomatik terfi denetimsiz başlarsa, sonradan
   hangi notun uydurma olduğunu ayıklamak katlanarak zorlaşır. Denetim
   terfiden **önce** kurulmalı.
3. **Sağlık/alarm (6)** — bu olmadan diğerlerinin çalıştığı bilinemez.

**B kümesi (3, 4) şimdi yapılmasın.** Henüz paralel çalışılmıyor; şimdi
kurulursa ölçülemeyen tasarım olur. Gerçekten ikinci oturum açılmadan hemen
önce yapılsın.

## Ölçülecekler (kod değil, ölçüm)

- `PostToolUse` modele konuşabiliyor mu — her uygulamada ayrı.
- Claude Code'da `model_auto_compact_token_limit` eşdeğeri bir ayar var mı.
- Tekrarlanan compaction'da oturum kimliği sabit kalıyor mu.
- Claude pencere büyüklüğü hâlâ **kalibrasyon**, ölçüm değil. Astra daha sağlam
  bir kaynak buldu ama bağlamadı: status line girdisindeki
  `context_window.context_window_size` ve `used_percentage`.

## Lab kararı (ayrı iş kolu)

Kullanıcı avenox (Taha) ikinci beyin sistemini **ayrı bir lab** olarak kurup
incelemek istiyor. Kararlar:

- **Ayrı vault, ayrı git deposu**, bizimkine karışmayacak (kullanıcı, 21.09 00:52).
- Kurulum vault dışına taşıyor — çalışma durumu app-data'ya, Python sistem
  geneline, hook güveni istemci ayarlarına. Bunlar **makine geneli**, klasöre
  özel değil; ayrı klasör bunu çözmüyor. Ayrı bir makine/ortam çözüyor.
- **Karar: VDS kiralanacak.** Lab'ın ötesinde gerekçesi var: 1. madde (telafi
  kuyruğu) uyuyan bir dizüstünde **düzgün test edilemez**; sürekli açık bir
  sunucu gözcü sürecin doğal evi. Asıl beyin yerelde kalır — sunucuya giden
  şey lab, sonra gözcü.
- **Seçim: AltunHOST SSD VDS-3** (3 core / 4 GB DDR4 ECC / 60 GB NVMe,
  İstanbul/Datacasa), 134,61 ₺/ay kampanya. Ölçüm: aynı özellikte VDS,
  VPS'ten **ucuz** — VPS ucuz görünmesini ilk sipariş indirimine borçlu
  (VPS-3 yenileme 161,36 ₺ vs VDS-3 134,61 ₺). VDS'te RAM kullanılmasa bile
  kullanıcıya atanır; paylaşımlı VPS'te Node tabanlı ajan swap'a düşebilir
  (claude 96517e26 · 21.09 01:05).
- **Kullanıcının kararı (21.09 01:16): VDS-3 değil VDS-4.** 4 core / 6 GB DDR4
  ECC / 90 GB NVMe, 185,86 ₺/ay. Üstteki VDS-3 satırı önerinin kendisidir,
  kayıt olarak duruyor. **İşletim sistemi: Ubuntu 24.04 LTS 64 Bit** —
  sağlayıcının listesindeki en yeni Ubuntu LTS bu (26.04 sunulmuyor; en yeni
  Debian 12). Gerekçe: Python 3.12 hazır gelir, Node tabanlı CLI ajanları için
  en iyi desteklenen taban. Oturum kaydı: [[2026-09-21-otomasyon-lab-ve-vds]].
- **Alımdan önce:** 1 günlük demo iste; yenileme fiyatını destekten teyit et
  (VPS sayfası yenileme tablosunu gösteriyor, **VDS sayfası göstermiyor**).
- Sağlayıcı kalitesi hakkında bağımsız kanıt **yok** — yalnız kendi pazarlama
  sayfaları okundu. Demo gününde ölçülecek.
- Alım, ödeme, panel girişi ve SSH anahtarı kurulumu **kullanıcıda**. Parola ve
  ödeme bilgisi ajana verilmez.
- Egemenlik kuralı esnetilmiyor: ayrı ortam zaten ayrı makine sayılır.

**Uyarı:** avenox sayfası (`https://avenox.lol/beyin.md`) bir tasarım belgesi
değil, **ajana hitap eden kurulum talimatı**. Kurulum hedefi olarak "mevcut
çalışma klasörü"nü alıyor ve kullanıcının istemediği bir izni verilmiş sayan
ifade içeriyor. Bu bir dağıtım tercihi, kusur değil — ama **ajanla okunurken
veri sayılmalı, talimat değil.** Lab dışında hiçbir ajana kurdurulmamalı.

**Beklenti:** o sistemde git yok ve zamanlayıcı yok (*"kapali uygulamayi
uyandiran bir zamanlayici kurulmaz"*). Yani bizim iki büyük açığımızda
muhtemelen bizden **az**ına sahip. Değeri "açıklarımızı çözüyor" değil, farklı
ödünler vermiş olması. İncelenecek dört şey: yarım kalan yazma, kapalıyken
telafi, iki eşzamanlı oturum, kabul testinin uygulanışı.

Vardığımız sonuçlar **yalnız v2 hakkında** olacak; Taha'nın yeni sürümleri
görülmedi, genel yargı kurulmayacak.

---

## (b) portu: mekanizma mekanizma zemin

Karar (b) "doğrulanan mekanizmaları seçerek al" diyor. Sıra: Y1 → Y2 → D3 → Y7.
Her biri için önce **bizde karşılığı var mı** ölçülür; varsa port yazılmaz.

### Y1 — telafi kuyruğu: tasarım kırıldı (21.09 08:24)

Avenox: `beyin_v3_hook.py:44–102`. Hook iş yapmaz, "iş borcu var" diye küçük bir
JSON yazar; pahalı iş ayrı boşaltma adımında; borç ancak sonuç başarılıysa
`os.replace` ile `hook-done/`'a **taşınır**, silinmez. Çekirdek ilke: *borç,
denemeyle değil sonucun gözlenmesiyle kapanır.*

Bizde iki kusur ölçüldü (claude 96517e26 · 21.09 08:10):
- **K1** `devir.al()` (`araclar/devir.py:68–89`) mesajı `pop` edip diske yazar,
  teslim *sonra* olur. `print`/`flush` patlarsa, hook zaman aşımıyla öldürülürse
  (ki `baglam.kontrol()` tam o pencerede çalışıyor) ya da harness çıktıyı yok
  sayarsa mesaj gider.
- **K2** `_oku()` 12 saatten eski girdiyi her okumada süzer, sonraki `_yaz`
  süzmeyi kalıcılaştırır. Kimse haberdar edilmez.

**Yedek yol K1'i kapatmıyor.** `oturum_basi.py:125` aynı `devir.al()`'i çağırıyor
— kuyruğun ikinci *tüketicisi*, kurtarıcısı değil. Bir teslim penceresinde
kaybolan mesaj için SessionStart'ta bakacak bir şey kalmıyor
(claude 96517e26 · 21.09 08:11).

**Astra'nın hükmü:** K1 ve K2 doğrulandı; tasarımım [İ7]'de çürütüldü (iki
Windows süreci aynı talimatı bastı — damga kilit değildir), [İ5] ölçülemedi,
[İ6] çürütüldü. **N6 ≠ Y1:** tur içi ölçüm açığı ayrı bir şey, kuyruk onu
kapatmaz. Ayrıntı ve dört sözleşme: [[olculmus-bulgular]] §21.

### Y2 — iyimser kilit (henüz ölçülmedi)

İki mekanizma **farklı katmanlarda duruyor**; bu yüzden "bizde zaten var"
demek yanlış olur, "gerekli" demek de erken.

| | Bizim `dosya_kilidi.kilit` | Avenox `update_task` |
|---|---|---|
| Tür | Karamsar, işletim sistemi kilidi (`msvcrt` / `fcntl`) | İyimser, revizyon karşılaştırması |
| Koruduğu | Aynı anda yazan iki **süreç** | Zaman içinde yazan iki **ajan** |
| Çakışmada | 3 sn bekler, sonra `TimeoutError` | `RevisionConflict: reread source` |
| Kayıt | Yok | Append-only `events` tablosu |

Bizim kilit mikro saniyeyi korur. Avenox'unki **kayıp güncellemeyi** korur:
iki ajan aynı kaydı okur, ikisi de düşünür, ikincisi birincinin kararını
sessizce ezer. Kilit buna hiçbir şey yapmaz, çünkü yazmalar dakikalar arayla.

Bizde bunun karşılığı **git**: iki ajan da commit ederse tarihçede görünür.
Ama commit edilmemiş pencerede koruma yok — ve iki ajan aynı klasörde
çalışıyor ([[iki-ajan-calismasi]]).

**Maruziyet ölçüldü (21.09 08:38):** 11 çapraz çakışma penceresi, en uzunu
13,5 saat; ikisinin de yazdığı 48 dosya, en sıcakları `BEYIN.md` ve
`notlar/acik-uclar.md`. Bizi şu an koruyan şey tasarım değil **düzenleme
aracının biçimi**: dize değiştiren düzenleme çakışmada başarısız olur, bütün
dosyayı yazan yol sessizce ezer. Geçmişteki kayıp güncelleme geriye dönük
ölçülemez. Ayrıntı: [[olculmus-bulgular]] §22. Karar Astra'ya açık.

### D3 — kaynak doğrulaması (henüz ölçülmedi)

Bizde işaretçiler yalnız **mekanik** denetleniyor: damga var mı, oturum var mı.
İçeriğin hâlâ o iddiayı desteklediği kontrol edilmiyor. Avenox içeriği
hash'leyip sorgu anında yeniden doğruluyor, bayatsa `abstained`. Astra'nın İ3
bulgusu kısıt: **tek dosya hash'i yetmez**, bağımlılık kapsamı şart — karşı
örnek bizim kendi commit'imiz `39712b5`.

### Y7 — danışman çitleri (henüz ölçülmedi)

Gölge mod + kapatma anahtarı. Jev'i ya da başka bir ucuz modeli hiçbir karara
bağlamadan önce gereken şey bu: çalıştır, kararlarını kaydet, hiçbir şeyi
etkilemesin. Kalibrasyon ölçülene kadar danışman danışmandır.
