# Kapanış ritüeli

Bir oturum bağlam kaybı olmadan nasıl kapanır, yenisi mirası nasıl devralır.
Kuralın uygulanabilir hâli [[AGENTS]] içindedir; burada **neden öyle olduğu** yazar.

> Merkez: [[BEYIN]] · İlgili: [[arac-arsiv]] · [[ikinci-beyin-mimarisi]] · [[tasarim-dersleri]]
> Kaynak: [[2026-09-07-ikinci-oturum]] (claude 3557db3e · 08.09)

---

## Sorun: köprünün bir ayağı yoktu

Oturum **başlangıcı** mühürlüydü (`SessionStart` hook'u okumaya zorluyor), ama
**kapanış** tamamen gönüllüydü. Ne yazılacağına, hatta yazılıp yazılmayacağına
o anki model karar veriyordu. `SessionEnd` diye bir hook yoktu — kullanıcı
olduğunu sanıyordu, yoktu.

## Neden hook ile çözülmedi

**Hook modele emir veremez, kabuk komutu çalıştırır.** `SessionStart` işe yarıyor
çünkü oturumun başında bağlama metin enjekte ediyor; model sonra gelip okuyor.
Kapanışta model çoktan gitmiştir.

Belgeyle doğrulandı: `SessionEnd` hook'u **`additionalContext` enjekte edemiyor**
ve toplam 1.5 saniyelik bütçesi var. Yani kapanışta modele söz geçirilemez.

## İki durum ayrımı

- **Durum A — kullanıcı "kapatalım" diyor.** Model hâlâ oradadır, bağlam yüklüdür,
  kapanış talimatı oturumun başında verilmişse hâlâ bağlamdadır. Ekstra mimari
  gerekmez. **Fiilen kullanılan yol budur.**
- **Durum B — kullanıcı demiyor** (pencere kapanır, bağlam dolar).

Karar: **Durum B kapsam dışı**, çünkü kullanıcı pencereyi kendisi izleyip konu
bittiğinde devrediyor — yani devir anlamlı bir sınırda oluyor.

16 Eylül'de bu karar güncellendi: Durum B `PreCompact` hook'uyla **güvenlik ağı**
olarak kapatılacak, ana yol olarak değil. Gerekçe: `PreCompact` rastgele bir yerde
tetiklenir, cümlenin ortasında; ana mekanizma olsa kötü olurdu, ağ olarak değerli.

## Asıl tasarım kararı: determinizm çıktıya değil, girdiye

İlk öneri sabit bir kapanış şablonuydu. **Elendi**, iki gerekçeyle:

1. Proje başta yazılan kurallardan bambaşka yönlere dallanabilir; o anki duruma
   uygun kapanış biçimine model karar vermeli.
2. **Kontrol listesi düşünmenin yerine geçer.** Zorunlu başlık boş başlık üretir.

Yerine konan: **ne yazılacağı serbest, ne okunacağı zorunlu.** Kapanışta model
önce `araclar/omurga.py` ile oturumun omurgasını okur, sonra yargısını kullanır.

Gerekçe ölçülebilir bir zaafa dayanıyor: kapanış anı, model bu iş için en kötü
halindeyken gelir — bağlam dolu, oturumun başı en uzakta. Kural yargıyı
kısıtlamak için değil, **öngörülebilir bir körleşmeyi dengelemek** için var.

## İkinci sabit: yargı değil, bakım

Tarih başlığını güncellemek, haritaya satır eklemek, bağ kurmak — düşünmek
gerektirmez, tam da bu yüzden atlanır. Kanıt: notların başında "Son güncelleme
7 Eylül 10:24" yazarken dosyanın gerçek değişiklik saati 13:01'di. İçerik
yazılmış, başlık unutulmuştu.

## Değişmeyen üç soru

Konu ne olursa olsun cevapsız kalmaması gerekenler — biçim serbest:

- hangi kararlar alındı ve **neden** (karar yeniden hesaplanamaz)
- ne denendi ve **elendi** (en pahalı bilgi; elenen hiçbir yerde iz bırakmaz)
- ne **açık kaldı**

## Kaynak gösterme kuralı (16 Eylül)

Avenox'un belgesinden alınan tek fikir: *"Hatırlayan bir sistemin en tehlikeli
hali, uydurduğunu hatırlıyor sanmasıdır."*

Kalıcı notlardaki **ölçümler, kararlar ve elenen fikirler** kaynak işaretçisi
taşır: `(claude 3557db3e · 08.09 17:34)`. İşaretçi doğrudan komuta çevrilir —
`python araclar/oku.py 3557db3e --saat 17:34` — yani iddia denetlenebilir olur.
Genel anlatım işaretçi taşımaz, yoksa her cümle parantezle dolar.

## PreCompact: güvenlik ağı (16 Eylül'de kuruldu)

`araclar/precompact.py`, `.claude/settings.json` içinde `PreCompact` olayına
**matcher'sız** bağlı: hem `auto` (sistem kendi sıkıştırırsa) hem `manual`
(`/compact` yazılırsa) tetikliyor. Manual'i de kapsaması bilinçli — ağ ancak
bilerek tetiklenebiliyorsa sınanabilir.

**İki ayaklı, çünkü tek ayak güvenilmez.** Bu karar 16 Eylül gecesi kendini
ödedi — ikinci ayak gerçek testte kırıldı, birincisi tuttu.

1. **Deterministik ayak:** oturumun omurgası `derleme/omurga-anlik/` altına
   yazılır. Model hiçbir şey yapmasa, enjeksiyon hiç çalışmasa bile ham malzeme
   kurtulur. Bu dosya sıkıştırmadan etkilenmez — diskte durur.
2. **Dolaylı enjeksiyon ayağı:** "şimdi yaz" uyarısı **devir kutusuna** bırakılır,
   konuşabilen bir hook onu modele taşır. Aşağıya bak.

## Devir kutusu: PreCompact modele konuşamıyor

Ölçüldü, varsayılmadı: `PreCompact` olayında `additionalContext` **geçerli
değil**. Claude Code çıktıyı şema hatasıyla reddediyor ([[yasanan-hatalar]]
madde 15). O olayda hook yalnızca kullanıcıya görünen `systemMessage`
basabiliyor; modele tek kelime söyleyemiyor.

Bu yüzden mesaj el değiştiriyor. `araclar/devir.py` bir posta kutusudur:

- `precompact.py` mesajı kutuya **bırakır** (`derleme/omurga-anlik/devir-bekliyor.json`)
  ve kullanıcıya tek satır durum basar.
- Kutuyu **konuşabilen** iki hook boşaltır, hangisi önce tetiklenirse:
  `SessionStart` ya da `UserPromptSubmit`. Ölçüldü: sıkıştırma bitince Claude
  Code `SessionStart`'ı zaten tetikliyor, yani teslimat kullanıcının bir şey
  yazmasını beklemiyor — pratikte kutuyu `SessionStart` boşaltıyor.
  `UserPromptSubmit` bu yol kaçtığında (hook henüz yüklü değilse, oturum başka
  türlü devam ederse) devreye giren ikinci yol olarak duruyor.
- Teslim eden kutuyu siler, yani mesaj bir kez okunur.
- **12 saatten eski mesaj teslim edilmez.** Günler sonra gelen "şimdi yaz" emri
  yanlış oturuma yanlış işi yaptırır; bayat emir sessizce düşer.

Genel kural, bu projeye özgü değil: *bir hook'un söyleyemediğini, söyleyebilen
bir hook'a diske bırakarak söyletebilirsin.*

**Neden bloke etmiyor.** Hook, çıkış kodu 2 ile sıkıştırmayı engelleyebiliyor ve
bu ilk bakışta daha iyi görünüyor (model tam bağlamla yazardı). Seçilmedi:
sıkıştırma engellenir ve pencere zaten doluysa oturum sert bir sınıra çarpabilir.
**Ağın kendisi hasara yol açmamalı.** Onun yerine omurga dosyası kurtarma
malzemesi olarak bırakılıyor — sıkıştırma sonrasında bile oturum kaydı ondan
yazılabilir.

**Gerçek sıkıştırmada ölçüldü** (16 Eylül 03:13, `/compact`, tetik `manual`):
omurga dosyası yazıldı — 69 kullanıcı mesajı, 44.974 bayt, 07.09 13:02'den
16.09 03:08'e kadar zaman damgalarıyla eksiksiz. Enjeksiyon aynı anda şema
hatasıyla düştü (claude 3557db3e · 16.09 03:13). Yani ağ, tasarlandığı gibi tek ayak üstünde iş gördü.

**Zincirin tamamı gerçek sıkıştırmada ölçüldü** (16 Eylül 03:32, `/compact`,
tetik `manual`): `precompact.py` şema hatası vermeden çalıştı, omurga yazıldı
(73 kullanıcı mesajı, 47.947 bayt), kutu doldu ve mesaj sıkıştırmadan sonraki
ilk turda modele ulaştı — `SessionStart` bloğunun içinde, `DEVIR KUTUSUNDAN:`
başlığıyla. `devir-bekliyor.json` teslimden sonra diskte yoktu; tek okumalık
tüketim de doğrulandı (claude 3557db3e · 16.09 03:35).

**Beklenmeyen sonuç: asıl yol sandığım `UserPromptSubmit` değil, yedek saydığım
`SessionStart` teslim etti.** Varsayım şuydu: "sıkıştırmadan sonra kullanıcı bir
şey yazar, `UserPromptSubmit` aynı oturumda teslim eder." Gerçekte sıkıştırmanın
kendisi `SessionStart`'ı tetikliyor, dolayısıyla teslimat daha erken oluyor.
Tasarımın iki yollu olması tam da bu yüzden işe yaradı: hangi yolun kazanacağını
bilmeden ikisini birden kurmak, doğru yolu tahmin etmeye çalışmaktan ucuzdu
(claude 3557db3e · 16.09 03:35).

---

## Arşiv kaydında tarih kuralı

17 Eylül'de kullanıcı haritaya bakıp *"birkaç saat önce kapattığımız oturumun
kaydı neden yok"* diye sordu. Kayıt vardı — ama bakılacak yerde değildi. Üç ayrı
kusur üst üste binmişti (claude 7f10f7a3 · 17.09 04:47):

1. **Harita satırı oturumun ilk gününü anlatıyordu.** On günlük, 110 mesajlık,
   iki iş kollu bir oturum "Kapanış ritüeli ve arşiv arama katmanı kuruldu"
   diye özetlenmişti; bu 8 Eylül'ün işiydi. Kullanıcı son günü arıyordu.
2. **Dosya başlıklarındaki tarihler yanlıştı.** Birinci oturum "30 Ağustos –
   7 Eylül" yazıyordu, ham kayıt **04.09 22:13** diyor. İkincisi "7–16 Eylül"
   yazıyordu, ham kayıt **17.09 01:55** diyor. İkisi de hatırlanarak yazılmıştı.
3. **Kapanış yanlış dosyaya yazılmıştı.** Oturumun son 97 mesajı Nar Ajans iş
   kolunda geçtiği için kapanış, o alt kolun dosyasına eklenmişti. Yani
   **oturumun baskın konusu, oturumun tamamı sanıldı.**

Üçüncüsü modelin yapısal bir zaafına dayanıyor ve tekrar edeceği için burada
duruyor: bağlamda **sıra** var ama **ağırlık** yok. Sondaki yoğunluk bütünün
rengi gibi görünür. Kapanış anı zaten modelin bu iş için en kötü hâlidir
(bkz. yukarısı); oturum uzunsa baskın konu yanılgısı buna eklenir.

**Kural — arşiv kaydı yazarken:**

- Aralık **ham kayıttan ölçülür, hatırlanmaz.** İlk ve son damga:
  `araclar/omurga.py <id>` kullanıcı mesajlarını verir; kaydın gerçek son anı
  için `.jsonl`'ın son satırındaki damgaya bakılır (model çıktıları ve araç
  çağrıları omurgada görünmez, kaydın sonunu onlar belirler).
- Hem dosya başlığı hem harita satırı **açılış ve kapanışı saatiyle** taşır:
  `30.08.2026 12:34 – 04.09.2026 22:13`. Dosya adındaki tarih yalnızca açılıştır
  ve tek başına yanıltır; kullanıcı oturumları *kapandıkları* zamanla hatırlıyor.
- **Kapanış, oturumun kendi dosyasına yazılır.** Oturum içinde açılan alt kol
  dosyaları ayrı oturum değildir; o dosyalar hangi oturuma ait olduklarını
  kendi içlerinde söyler ve asıl dosyaya bağ verir.
- Harita satırı oturumun **tamamını** özetler. İki iş kolu varsa ikisi de
  yazılır; son iş kolu bütünün adı olarak kullanılmaz.

İlgili: [[yasanan-hatalar]] madde 19 (aynı kökten çıkan tarih hatası),
[[kullanici-baglami]] (modelin zaman algısı üzerine).

---

## SessionEnd boşluğu ve compact'in yeri

17–18 Eylül'de ölçüldü ve bir açık bulundu (claude 7f10f7a3 · 18.09 01:02).

### Bugün üç hook var, kapanış hook'u yok

`.claude/settings.json`: `SessionStart`, `PreCompact`, `UserPromptSubmit`.
**`SessionEnd` yok.** Yani "oturumu kapatalım" dendiğinde çalışan şey bir hook
değil, bu dosyadaki ritüeli modelin uygulaması — **gönüllü.**

Sonucu: **oturum kapatılmadan bırakılırsa hiçbir şey yazılmaz.** Ne arşiv, ne
terfi, ne harita. Ham kayıt diskte durur ama kalıcı katmana hiçbir şey geçmez.
Kullanıcının oturumları günlerce açık kaldığı için bu gerçek bir açıktır.

### Dört çıkış yolu ve ne bıraktıkları

| Oturum nasıl biter | Kalıcı katmana ne geçer |
|---|---|
| "oturumu kapatalım" | Tam not: karar, elenen fikir, açık uç |
| `/compact` | Omurga diske düşer; not **sıkışmış bağlamdan** yazılır |
| Kapatılmadan bırakılır | **Hiçbir şey** — ham kayıt var, okuyan yok |
| Side chat'te konuşulur | **Kayıt bile oluşmaz** — bkz. [[acik-uclar]] |

### `/compact` bir kapanış aracı değildir

Compact bandın **ortasında** olur, kapanış **sonunda**. Compact sonrası model
kendi ürettiği özete bakar — kuralı yoktur, denetlenmez, neyi attığını söylemez.
Kapanış notu ise kural gereği üç şeyi taşır. Yani biri modelin o anki yargısı,
diğeri yapılandırılmış bir devir.

**Doğru sıra: önce kapanış yazılır, sonra compact ya da yeni oturum.**
`PreCompact` bir **güvenlik ağı**; ağ düşen için vardır, plan düşmemektir.

Ham kayıt her iki durumda da silinmiyor — ama durması yetmiyor, birinin dönüp
bakmaya karar vermesi gerekiyor.

### Karar: işareti ölen bant bıraksın, notu yaşayan bant yazsın

`SessionEnd` hook'u modele **konuşamaz** — o an son model turu kapanmıştır,
muhatap yoktur (mekanizma: [[agentic-yapi]]). Dolayısıyla "kapanışta modele not
yazdır" kurgusu doğrudan kurulamaz.

Denenen ve **elenen** kurgu: `SessionEnd`'de headless bir örnek doğurup notu
ona yazdırmak. Teknik olarak mümkün (Claude Code'un tek seferlik çağrı modu var)
ve bir yan faydası da var — o örnek **temiz bağlamla** doğar, yani "kapanış anı
modelin en kötü hâlidir" problemi ortadan kalkar. İki kusuru yüzünden elendi:

1. **`SessionEnd` her zaman tetiklenmez.** Çökme, güç kesintisi, uygulamanın
   kapatılması — hook hiç çalışmaz ve çalışmadığını kimse fark etmez.
2. **Omurga yetmez.** Sadece kullanıcı mesajlarını taşır; ölçümler, elenen
   fikirler, gerekçeler model tarafındadır ve ham kayıttadır.

**Seçilen kurgu:**

- **`SessionEnd`:** ucuz ve modelsiz olsun — omurgayı döksün, *"bu oturum
  kapanışsız bitti"* işareti bıraksın. Çökmeye dayanıklı, çünkü yapacağı küçük.
- **Gece derleyicisi:** işareti görsün, temiz bağlamlı bir örnek doğurup notu
  yazdırsın, sonucu rapora yazsın. Cron ile tetiklenir, yani oturumun nasıl
  bittiğinden bağımsızdır ve **kaçmaz**; birden çok kapanışsız oturumu aynı
  çalıştırmada sırayla işler; yapıldığı raporda **görünür** olur.

Bu ikisi kurulmadan önce **omurganın zenginleştirilmesi** gerekir — yoksa temiz
örnek eksik malzemeyle yazar. İkisi tek işin iki parçasıdır.

---

## Kapanış işareti (19 Eylül)

Arşiv dosyasının başlığının altına `kapanan-oturum: <8 hane>` yazılır. Bir
oturumun kapandığını söyleyen **tek** kaynak budur: gece derleyicisinin
dedektörü ve oturum başındaki "kapanmamış oturumlar" uyarısı buna bakar.
Compact sonrasında yazılan ara kayıtta bu satır yazılmaz, çünkü oturum
bitmemiştir. `precompact.py`'nin devir mesajı bunu açıkça söylüyor.

Kural artık `CLAUDE.md`'de değil `AGENTS.md`'de. Kapanış ritüeli bu klasörde
çalışan her ajan için ortak. Bkz. [[gece-derleyicisi]] · [[acik-uclar]].

---

## Erken devir boşluğu (19 Eylül Codex incelemesi)

Kapanış ritüeli sağlayıcıdan bağımsızlaştırıldı, fakat **onu doğru zamanda
başlatan tetikleyici** hâlâ kullanıcıya bağlı. Claude tarafında kullanıcı
bağlam yüzdesini arayüzden görüp yüzde 60–70 civarında “oturumu kapatalım”
diyebiliyor. Codex Desktop'ta eşdeğer sayaç görünmüyor; incelenen oturumun
etkin penceresi de 258.400 token ölçüldü (codex 01a0ba53 · 19.09 19:09).

Bu nedenle `PreCompact` ağı ile kontrollü devir arasında boşluk var:

- `PreCompact` bağlam zaten dolarken ve konunun rastgele bir yerinde gelir.
- Kullanıcı sayaç görmüyorsa anlamlı bir sınırda erken kapanışı zamanlayamaz.
- Daha küçük pencere, görünürlük eksikliğini daha önemli hâle getirir.

**Yeni tasarım gereksinimi:** Claude veya Codex fark etmeksizin, bağlam güvenli
bir eşiğe geldiğinde sistem turun sonunda kontrollü devir başlatmalı; kararları,
elenenleri ve açık uçları özgün bağlam hâlâ eldeyken yazmalı. Eşik aşılması tek
başına `kapanan-oturum:` yazmamalı; kapanış işareti ancak yeni oturuma gerçek
geçişte konmalı. `PreCompact` ana yol değil, son savunma hattı olarak kalmalı
(codex 01a0ba53 · 19.09 19:00). İnceleme kaydı:
[[2026-09-19-codex-sunum-ilk-alti-slayt]].

**Kuruldu (19.09 20:30):** `araclar/baglam.py`. Tur başı hook'u, kullanıcı yeni
mesaj yazınca bağlam doluluğunu ham kayıttan ölçer. Kullanıcının seçtiği iki
eşikte birer kez uyarır: %50 ve %70. Uyarıyla birlikte tam omurgayı diske
alır. Aynı seviyede tekrar uyarmaz. Compact sonrasında doluluk düşerse seviye
sıfırlanır. Kapanışı kullanıcı başlatır. `kapanan-oturum:` onayı kullanıcıya,
ileride yetkili bir orkestratör ajana aittir. Bu oturumda gerçek hook ile
sınandı: %50 aşıldı, uyarı modele ulaştı, omurga yazıldı
(claude 5c600e7e · 19.09 20:31). Ölçüm kaynakları: [[olculmus-bulgular]] §12.



> **Astra denetim notu:** Kimlik karışması, taslağın yanlış kapanış sayılması, kurtarma hatasının yeniden denenmesi ve devir kuyruğu bağımsız denetimde düzeltildi. Codex %50/%70 bu oturumda canlı doğrulandı; uzun tek tur içi kontrol ve canlı PreCompact ayrı sınırlar.
> Kanıtlar: [[astra-denetim-bulgulari]] · [[2026-09-20-astra-kontrol]].
> (codex 01a0bc5c-f1c4 · 20.09 05:46)
