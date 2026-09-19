# Gece derleyicisi ve git

Her gece 00:30'da çalışan `araclar/derle.py`. Ne yaptığı ve neden böyle
tasarlandığı.

> Merkez: [[BEYIN]] · İlgili: [[kapanis-ritueli]] · [[ikinci-beyin-mimarisi]] · [[tasarim-dersleri]] · [[acik-uclar]]
> Kaynak: [[2026-09-07-ikinci-oturum]] (claude 3557db3e · 16.09)

---

## Tek ilke: ölçer, yazmaz

Avenox'un "akşam derleyicisi" fikri otomatik **özetleyici** olarak geliyordu.
Öyle kurulmadı. Gerekçe kendi tasarım derslerimizde yazılı: *ölçülebileni ölç,
ölçülemeyeni yaz.* Her gece otomatik özet üreten bir süreç, kalıcı katmanı vasat
metinle kirletir ve "sessizce kötü özet" riskini yaratır.

Bu yüzden derleyici **anlatı üretmez, sayı üretir.** Anlatıyı model kapanışta
yazar; derleyici sadece **eksiği ve orantısızlığı gösterir.**

## Üç çıktı

| Rapor | Ne zaman | Ne ölçer |
|---|---|---|
| `derleme/gunluk/` | her gece | Kapanış kaydı yazılmadan biten oturumların **dedektörü** |
| `derleme/haftalik/` | pazartesi | Faaliyet dökümü: oturum sayısı, projeler, commitler, kalıcı katmanın boyutu |
| `derleme/aylik/` | ayın 1'i | **Açık uçların yaşı** + damıtma kalitesi göstergesi |

`--hepsi` üçünü birden zorlar (sınama için), `--kuru` hiçbir şey yazmadan ekrana
basar.

## Dedektör nasıl çalışır

**19 Eylül'den beri:** bir oturum ancak arşiv dosyasında
`kapanan-oturum: <id>` satırı varsa kapanmış sayılır. Zaman sınırı yok; bu
projenin her kapanmamış oturumu her gece rapora düşer, okuma komutuyla birlikte.
Son 6 saatte yazılmış olanlar "muhtemelen hâlâ açık" diye etiketlenir.
Proje kapsamı Codex oturumlarını da içerir (çalışma dizini bu klasör olanlar).

**Elenen eski ölçüt:** "kimlik `notlar/` ya da `oturumlar/` içinde geçiyor mu".
İki yerden sızdırıyordu. Birincisi, oturum içinde yazılan tek bir kaynak
işaretçisi açık oturumu "işlenmiş" gösteriyordu. İkincisi, arşiv dosyaları başka
oturumlara atıf yapıyor. Ayrıca yalnızca son 24 saate bakıldığı için
kapanmadan sessiz kalan oturum ertesi gece görünmez oluyordu
(claude 5c600e7e · 19.09 08:27).

## Gece taslağı: ilkenin tek istisnası (19 Eylül)

"Ölçer, yazmaz" ilkesinin bilinçli bir istisnası var: `araclar/gece_kayit.py`.
Kapanışsız kalıp 6 saattir sessiz olan oturumun tam omurgasını (kullanıcı ve
model metni) temiz bağlamlı, araçsız bir modele verip **arşiv taslağı**
yazdırıyor: `oturumlar/oto-<id8>.md`.

İstisna dar tutuldu, çünkü ilkenin gerekçesi hâlâ geçerli ("sessizce kötü
özet"):

- **Kalıcı katmana dokunmaz.** Terfi önerileri taslağın içinde kalır. Onları
  bir sonraki oturum kullanıcıyla birlikte işler.
- **Taslağın işaretçileri her gece denetlenir.** Uydurma damgayı mekanik
  denetim yakalar.
- **Oturum başı onu gösterir.** "GECE TASLAĞI VAR" uyarısı olmadan taslak
  unutulurdu.
- **Tavan:** gecede en fazla 3 oturum, omurga 600 KB'ı geçerse ortası kırpılır,
  oturum başına 15 dakika.
- **Model:** varsayılan `claude -p` ve Sonnet 5. Proje hook'ları, MCP ve
  araçlar kapalı. Hook'lar kapalı çünkü SessionStart devir kutusunu tüketir ve
  gerçek bir compact mesajı kaybolurdu. `GECE_KAYIT_KOMUT` ortam değişkeniyle
  başka bir sağlayıcıya verilebilir.
- Codex alt ajan oturumları (`originator: codex_exec`) işlenmez.

**Sınama** (claude 5c600e7e · 19.09 17:28): bu oturumun kendisi üzerinde
103 saniyede 7 KB taslak çıktı. Tarih aralığını ölçerek yazdı, iş kollarını
ayırdı, kararları gerekçeleriyle, elenenleri ve açık kalanları ayrı verdi.
18 işaretçinin hepsi gerçek bir damgaya denk geldi. Bir kusuru vardı: çıktıyı
kod çitine sarmıştı, ayıklayıcı eklendi.

**Elenen: `SessionEnd` hook'u ile işaret bırakmak.** `kapanan-oturum:` satırı
geldiğinden beri dedektörün kendisi işaret. Oturumun bitiş anını yakalamaya
gerek yok; çökme ve elektrik kesintisi de böyle yakalanıyor. Codex'in
SessionEnd'i boşta kalınca da tetikleniyor, yani "konu bitti" demek değil
(codex 01a0b9eb · 19.09 16:47).

**Rapor artık bir alıcıya ulaşıyor.** Push sonucu `son-calisma.json`'a
yazılıyor. Oturum başı betiği o dosyadaki sorunları (kesinti, 36 saatten uzun
sessizlik, push hatası, kusurlu işaretçi) ilk mesajla modele veriyor. Önceden
rapor diske düşüyor ve orada kalıyordu. Bkz. [[acik-uclar]].

**Kapsam sadece bu proje.** Diğer projelerde bu yapı henüz yok; onları
"işlenmemiş" diye listelemek her gece onlarca satır gürültü üretirdi ve rapor
çöplüğe dönerdi. Diğer projeler raporda tek satır sayı olarak geçiyor. Yapı
başka bir projeye taşındığında orada kendi derleyicisi çalışır.

## Damıtma kalitesi göstergesi

Sistem bir özetin *iyi* olup olmadığını yargılayamaz. Ama **orantısızlığı
ölçebilir**: 300 KB'lık bir konuşmadan 2 KB'lık kayıt çıkmışsa bu şüphelidir.

Aylık rapor, oturum kaydının konuşma metnine oranını hesaplayıp %2'nin altında
kalanları "ince, gözden geçir" diye işaretliyor. Kalite yargısı değil, sessiz
bozulmayı yakalayan ucuz bir vekil ölçüt.

## Açık uçların yaşı

Aylık rapor `notlar/acik-uclar.md` üzerinde `git blame` çalıştırıp üstü çizili
olmayan maddelerin kaç gündür durduğunu listeliyor; 60 günü geçenleri
işaretliyor. Yaş, git deposunun başladığı **16 Eylül 2026**'dan ölçülür — daha
eski maddeler için gerçek yaş bundan büyüktür.

## Git

Klasör 16 Eylül'de yerel git deposu oldu (`ana` dalı) ve aynı gün **private
GitHub deposuna** bağlandı: `yavuzates34/ikinci-beyin`. Derleyici her gece
`git add -A` + commit + `push` yapıyor.

Ne veriyor: **geçmiş, geri alma ve dış yedek.** Yanlışlıkla silinen bir not geri
getirilebilir; disk giderse depo GitHub'da durur. Ücretsiz private depo, ek
masraf yok (kullanıcı iCloud için abonelik masrafı istemiyordu; GitHub bunu
masrafsız çözdü).

**Push başarısız olursa derleme bozulmuyor:** internet yoksa ya da kimlik
düşmüşse yerel commit yine atılır ve rapora `PUSH BASARISIZ - dis yedek guncel
degil` satırı düşer. Sessiz başarı yasak.

**Gönderilmeden önce tarandı:** izlenen dosyalarda API anahtarı, parola, token,
e-posta, kimlik/IBAN benzeri örüntü aranıp temiz çıktı. Depo private ama
[[ikinci-beyin-mimarisi]] içindeki "hiç girmeyen katman" kuralı geçerli:
kimlik numarası, mali detay ve kimlik bilgileri bu klasöre hiç yazılmaz.

## Zamanlama

Windows Görev Zamanlayıcı görevi: `playground-derleyici`, her gün 00:30,
`araclar/derle-gece.cmd` çağırıyor. Elle tetiklenip uçtan uca doğrulandı:
çıkış kodu 0, rapor yazıldı, commit atıldı. Log: `derleme/derleyici.log`
(git'e girmiyor).

---

## 18 Eylül 2026: üç ekleme — telafi, denetim, sağlık

Kullanıcı "haftalık rapor kaçarsa ne olur" diye sordu; ölçüm üç ayrı şey buldu
(claude 7f10f7a3 · 18.09 02:41).

### Ölçülen durum

- **Görev kaçması zaten telafi ediliyor:** `playground-derleyici` görevinde
  `StartWhenAvailable = True` — makine kapalıyken kaçan görev, açılınca çalışır.
  `WakeToRun = False`, yani uyuyan makineyi uyandırmaz (fan sesi nedeniyle
  bilinçli doğru ayar).
- **Haftalık rapor kaçmamıştı, sırası gelmemişti.** Tetik `weekday() == 0`
  (Pazartesi); elimizdeki tek haftalık 16 Eylül Çarşamba tarihliydi çünkü
  kurulumda elle üretilmişti. Model "ya üretildi kimse bakmadı ya ölçüm
  çalışmıyor" diye ikilem kurmuştu — **üçüncü seçeneği atlamıştı.**
- **Ve beklenmeyen:** 18.09 00:30 çalıştırması çıkış kodu `0xC000013A`
  (kontrol kesmesi) ile bitmişti. Günlük dosya yazılmış, commit atılmıştı,
  görev "Ready" görünüyordu — ama log'da 18 Eylül bölümü hiç yoktu.
  **Denetim mekanizmasının kendisi sessizce bozulabiliyor.**

### 1. Telafi: "bugün hangi gün" değil, "eksik olan var mı"

`haftalik_gerekli()` ve `aylik_gerekli()` eklendi. Eski koşul güne bakıyordu ve
bir açık bırakıyordu: makine Pazartesi gecesi kapalıysa görev Salı telafi olarak
çalışır ama içeride "bugün Pazartesi değil" diye haftalığı **atlar, sessizce.**
Yeni koşul çıktıya bakar — bu hafta üretilmiş mi, bu ay üretilmiş mi.

Bu, [[kapanis-ritueli]]'ndeki `SessionEnd` kurgusunun aynı deseni: **ölen bant
işaret bırakır, yaşayan bant eksiği toplar.** Kullanıcı aynı deseni bağımsız
olarak ikinci kez buldu.

### 2. Denetim: kaynak işaretçileri her gece açılır

`isaretci_denetle()` eklendi. `notlar/` içindeki her `(claude <id> · <damga>)`
işaretçisini açar, o oturum kaydı var mı ve o damgada mesaj var mı diye bakar.
**İçeriği denetlemez** — sadece "bu adres mevcut mu" der. Model gerektirmez,
yargı gerektirmez, deterministiktir.

Çözdüğü sorun: işaretçi bir **imkândır, denetim değildir.** Denetlenmeyen bir
işaretçi denetlenebilirlik görüntüsü verir; uydurulmuş bir kaynak tam da bu
yüzden hatanın en tehlikeli türüdür.

**İlk sürüm sessizce 8 işaretçi atlıyordu.** Katı desen 40'ın 32'sini yakalıyor,
gerisini görmezden geliyordu — çünkü işaretçi formatı tek tip değil: saat
aralığı (`17:54–18:10`), saatsiz tarih (`08.09`), tek işaretçide iki damga,
satır sonuna bölünmüş olanlar. Desen esnetildi ve **üçüncü bir kategori**
eklendi: *denetlenemeyen*. Eşleşmeyen bir işaretçi artık sessizce atlanmıyor,
raporlanıyor.

**Negatif testle doğrulandı** — "hepsi doğru" çıktısı tek başına mekanizmanın
çalıştığını kanıtlamaz. Geçici bir dosyaya üç kusurlu işaretçi konuldu; üçü de
ayrı ayrı yakalandı: uydurma damga, var olmayan oturum kimliği, okunamayan
damga. Gerçek olan geçti.

**İlk tam denetim sonucu: 40 işaretçinin hepsi doğrulandı.**

### 3. Sağlık: derleyici kendi kesintisini bildirir

`derleme/son-calisma.json` eklendi. Çalışma başında `tamamlandi: false` yazılır,
sonunda `true`. Bir sonraki çalışma bu dosyayı okur; `false` bulursa önceki
çalıştırmanın **tamamlanmadan kesildiğini** bildirir.

Gerekçe: bir denetim mekanizması sessizce bozulabiliyorsa, denetlediği şeyler
hakkında söyledikleri de güvenilmez olur. Log'a değil ayrı bir duruma yazılıyor,
çünkü log'u görev zamanlayıcı yönetiyor ve üzerine yazıyor.

Dosya ayrıca son denetim sonucunu taşır: işlenmemiş oturum sayısı, işaretçi
toplamı, kusurlular, denetlenemeyenler.
