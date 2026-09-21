# Tam otomasyon, lab, Avenox denetimi — 20–21 Eylül 2026

**Ara kayıt. Oturum kapanmadı.** `kapanan-oturum:` satırı bilerek yoktur.
Oturum `96517e26-5948-4d47-8014-6e69edc7d0c3` (claude), 20.09 20:28'den beri
açık. İkinci kez sıkıştırılıyor (ilki 21.09 02:42).

> Merkez: [[BEYIN]] · İş belgesi: [[2026-09-21-tam-otomasyon-plani]] ·
> İlgili: [[acik-uclar]] · [[olculmus-bulgular]] · [[arac-izle]] ·
> [[astra-lab-denetimi]] · [[agentic-yapi]]

---

## Evreler

**1. Salt okunur denetimler (20.09).** Astra'nın yarıda kalan turları iki kez
"hiçbir şey değiştirme" talimatıyla okundu. Astra'nın işi doğrulandı. Benim
iki yanlış iddiam Astra tarafından yakalandı: "gece görevinde commit hiç
çalışmadı" (çalışmış, `67779e9`) ve "derleme saniyeler sürer" (ölçmeden
söylenmiş). Ders: **anlatı kurunca kayda bakmayı unutuyorum.**

**2. Tam otomasyon kararı.** Kullanıcı sistemin tam otomatik çalışmasına karar
verdi; kapanış ritüeli yerine eşik ritüeli. Tasarım ayrı iş belgesinde.

**3. VDS ve lab.** AltunHOST VDS-4, Ubuntu 24.04. Kurulum, ölçüm ve
sıkılaştırma yapıldı. Avenox v3.1.0 ayrı bir kullanıcının (`avenox`, sudo yok)
altında kuruldu ve çalıştırıldı.

**4. Videolar.** Taha'nın iki videosu dört kaynakla çözümlendi.

**5. Astra denetimi.** Üç iddiam da düştü. Karar: (b).

## Kararlar ve gerekçeleri

- **Lab ayrı vault + ayrı git + ayrı makine** (kullanıcı). Bizim kasayla
  karışmaması şart. Sunucuda `avenox` kullanıcısının sudo'su yok.
- **VDS-4 / Ubuntu 24.04** (kullanıcı, 21.09 01:16). Listedeki en yeni Ubuntu
  LTS; Python 3.12 hazır gelir.
- **Görünürlük ayrımı kuruldu** (kullanıcı, 21.09 05:35): `ozel` / `ic` /
  `acik`, `gorunurluk.json` + `araclar/gorunurluk.py`. Çekirdek kural:
  **eşleşmeyen her şey `ozel` sayılır** — manifesto bayatlarsa dosya sızmaz,
  fazladan kapalı kalır ve rapor edilir.
- **Video işi lokalde yapılır** (kullanıcı, 21.09 06:28). GPU'da 4 dakika,
  sunucu CPU'sunda tahmini 68 dakika.
- **Astra alt ajan olarak çağrılır** (kullanıcı, 21.09 07:03). CLI 0.155.1'e
  güncellendi, çalıştı. Keşif kısıtı kaldırıldı.
- **Karar: (b)** — mevcut sistemi koru, doğrulanan mekanizmaları seçerek al.
  Astra'nın hükmü, 21.09 07:26.

## Ne denendi ve elendi

**"Avenox sürekli makbuz yazıyor, o yüzden teslim tarihi yok."** Bu gecenin
mimari anlatısının temeliydi; **Y8'de çürüdü.** `PostToolUse`/`Stop` olay
metadatası yazıyor, receipts tablosu 0. Makbuzu ajan kendisi yazıyor.

**"İki sistem farklı kaynak okur, çakışmazlar."** **İ2'de çürüdü.** `ozel` ve
etiketsiz notlar Avenox tarafından `internal` indekslendi.

**"Hash'i anlatılan şeye tak, tek dosya yeter."** **İ3'te çürüdü.** Karşı örnek
bizim kendi commit'imiz `39712b5`.

**"Dört katmanlı bağlam ölçümü gereksiz."** **İ1: ölçülemedi.** Y10 tuttu
(41/41 mesaj diskte) ama canlı bağlam 396.006 → 20.070 token. Gerekçem
Y8'e dayanıyordu, o düştü.

**"Keşfe token harcama" kısıtı** (benim brief'imdeki) — kullanıcı kaldırdı.

**"Kurayım" teklifi (video araçları)** — gereksizdi, `araclar/izle.py` zaten
vardı ve D:\AI altında her şey kurulu. Teklif etmeden `--kontrol`
çalıştırmalıydım.

## Yapılan işler

| İş | Sonuç |
|---|---|
| VDS kurulumu | Ubuntu 24.04, çekirdek 6.8.0-139, ufw + fail2ban + otomatik yama, anahtarla SSH |
| İlk ölçüm | Disk 580 MB/s yazma / 1,1 GB/s okuma; ağ 106 MB/s; gecikme 10 ms; **RAM rezervasyonu yok** |
| Avenox kurulumu | v3.1.0, `~/lab/vault`, 37 dosya, `doctor` çalışıyor |
| Video çözümleme | İki video × dört kaynak, lab deposunda `23d1e68` |
| Görünürlük sistemi | `226cb11` — 63 ozel / 49 ic / 4 acik |
| Omurga §17 düzeltmesi | `39712b5` — `isCompactSummary` süzgeci, regresyon testi 29/29 |
| Astra denetimi | 18 kontrol, rapor denetçinin çalışma dizininde |

## Görünürlük sızıntısı: kapı kuruldu, ilk durdurduğu biz olduk

Sıkıştırma sonrası ilk iş buydu. Ölçüm sırası önemli: önce
`disari_cikabilir()`'in kaç çağıranı olduğuna bakıldı — **sıfır**. `AGENTS.md`
ise "model çağıran her yol bundan geçer" diyordu. Sonra kendi kodumuzda
modele içerik gönderen tek yol arandı ve bulundu: `gece_kayit.yazdir()` her
gece **ham omurgayı** (`ozel`) bir modele veriyordu. Avenox kurulmasaydı da
sızıntı duruyordu (claude 96517e26 · 21.09 07:52).

Kurulan: `araclar/disari.py` — **kapı** (gönderimi durdurur), **yansıma**
(yabancı araca kasa değil filtreli kopya verilir), **bulucu** (sızıntıyı
sonradan yakalar). Taşıyıcı katman yansımadır; diğer ikisi rica eder, o
bayta çevirir. Astra'nın İ2 deneyi kalıcı regresyon testi oldu
(`SizintiTests`, negatif kontrolüyle). Üç sabotaj denendi, üçü de yakalandı.
Ayrıntı: [[olculmus-bulgular]] §20.

**Elenen: dosyanın içine etiket gömmek.** Frontmatter yabancı aracın
*görebileceği* tek yer, ama görmesi uyacağı anlamına gelmez; üstelik proje 42
dosyanın hiçbirinde frontmatter tutmuyor ("zorunlu başlık boş başlık üretir").
Yansıma daha güçlü: uyması gereken bir kural bırakmaz, içeriği bırakmaz.

**Elenen: yansımayı kasanın içine yazmak.** Kolay olurdu; ama kasayı tarayan
araç yansımayı da tarar. Sızıntı kapanmaz, bir kopya daha olurdu. Kod bunu
artık reddediyor.

## (b) portu başladı: Y1, dört sürüm, üç Astra turu

Kullanıcı 08:06'da "başlayın" dedi, sonra uyudu; akşam 20:22'de döndü ve
"devam edin" dedi. İş bölümü: Astra hoca/denetçi, ben uygulayıcı. Her tur aynı
düzen: ben yazarım, Astra çürütmeye çalışır.

| Tur | Ne verdim | Ne düştü | Kök hata |
|---|---|---|---|
| 1 (08:22) | Tasarım: pop yerine işaretle, flush'ta onayla | [İ7] iki süreç aynı talimatı bastı · [İ6] N6 ≠ Y1 · flush modele ulaşmayı kanıtlamıyor | Avenox'un ilkesini brief'e **kendim yazıp** denemeye dayalı tasarladım |
| 2 (12:11) | Kod v3: buluşsal kanıt | 5 iddiadan 4'ü; `nullcontext` ile 11/11 test geçti | Kanıtı buluşsal yaptım; rapor yolunda K1'i **yeniden kurdum** |
| 3 (20:42) | Kod v4: açık tamamlama kaydı | İ16 (dört sabotaj testten kaçtı) + **B1**: bildirim kimliği 8 haneye kısaltıyor, o kimlikle `--tamamlandi` yetim kayıt yazıyordu | Üretici → tüketici → komut zinciri hiç sınanmıyordu |
| 4 (22:06) | v4.1: tam kimlik, kimlik çözümleme, geçerli kanıt | — | **Y1 kabul edildi** |

**Y1 kapandı.** Dar kapsam: kaydedilmiş devir borcu sessizce kaybolmaz ve
doğru kimlikle kapatılabilir. 12 sabotajın 12'si yakalanıyor, 66/66.

Astra 08:31'de kotaya takıldı, 11:55'te yenilendi; arada bekleyen bir görev
kurdum, yenilenince ikinci tur kendiliğinden başladı.

**Elenen: flush onayı.** Çıktı baytlarını tüketip modele hiç eklemeyen bir
alıcıda gönderici başarı gördü, bağlama 0 mesaj girdi. Flush, üç katman aşağıyı
onaylıyor.

**Elenen: buluşsal kanıt.** "Kimlikten söz eden yeni dosya" üç yoldan yanlış
kapattı: *"Work has NOT been done"* yazan bir not, üç işten yalnız birinin
yapılması, saniyeye kırpılmış damga. "İşten söz edildi" ≠ "iş yapıldı".

**Elenen: aynı süreçte sıralı çağrıyla kilit testi.** Kilidi hiç sınamıyordu.
Yerine iki gerçek süreç.

### Y2 maruziyeti ölçüldü (Astra beklenirken)

11 çapraz çakışma penceresi (en uzunu 13,5 saat), ikisinin de yazdığı 48
dosya, en sıcakları `BEYIN.md` ve `notlar/acik-uclar.md`. Bizi koruyan şey
tasarım değil **düzenleme aracının biçimi**: dize değiştiren düzenleme
çakışmada başarısız olur, bütün dosyayı yazan yol sessizce ezer. Hüküm yok,
Astra'ya açık. [[olculmus-bulgular]] §22.

### Bu arada düştüğüm iki hata

- İşaretçiye tur içindeki "şimdi"yi yazdım; o an henüz diskte yoktu, denetim
  reddetti. [[yasanan-hatalar]] madde 21.
- Bir kabuk komutu dosya içeriğini komut olarak çalıştırıp kasada altı boş dosya
  bıraktı (satır başındaki `>` yönlendirme oldu). Silindi; biri Windows'un
  sondaki nokta tuzağına takıldı. `2026-09-17.md`'ye dokunulmadı.

## Gece derleyicisi açık kalıyor (20:29)

Kullanıcı: gece derleyicisi ve cron lokalde açık kalır; lab onlara gerek
olmadığını gösterirse ona göre entegre edilir. Görünürlük kapısı gece
yazıcısını durdurmuştu; `dis_kaynaklar` kuralı **yalnız bu kasanın** ham
kayıtlarını `ic` yaptı — `~/.claude/projects` Nar Ajans'ın kayıtlarını da
tutuyor, onlar kapıda kalıyor (canlı ölçüldü).

## Y2: önce hoca, sonra ölçüm, sonra karar

Kullanıcı 20:31'de sordu: *"Astra'yı hoca olarak kullanıyorsun, değil mi?"*
Cevap: yarım — hep bitmiş şeyi götürüp "kır" diyordum. Ayrıca Y1'i "lab'de"
deyip canlı hook'larda yapmıştım, söylememiştim. Sözleşme yenilendi: önce hoca,
sonra denetçi; deney lab'de; yerel hook'a dokunmadan önce sor.

Sıra: Astra hoca olarak yöntemi verdi (koşullu yazma; git HEAD yetmez) →
lab'de deney (10 senaryo; korumasız yollar kaybetti, koşullu yazıcı tuttu,
üç sabotaj yakalandı) → gerçek araçlar ölçüldü → Astra denetledi.

**Elenen: "`Write` sessizce ezer."** Ölçmeden yazmıştım; ölçünce reddettiği
çıktı. Korumasız olan betikle yazmak.

**Elenen: "İki ajanın kendi araçları zaten yetiyor" (İ17).** Astra betiksiz üç
karşı örnek üretti, gerçek Codex `apply_patch` ile: var olan dosyaya `Add File`
içeriği siliyor, girinti değişikliği bayat yamayla kayboluyor, dolu hedefe
`Move to` eziyor. `Add File`'ı ölçerken aklımdan geçirmiş, "yapay" deyip
atlamıştım.

**Elenen: "Betik tek açık; kural + yardımcı yeter" (İ18).** Yan kilit,
katılımsız yazıcıyı durdurmuyor.

**Deney düzeneğimde iki kusur:** zayıf oracle (dosyayı bozan iki mutant geçti)
ve ayardan türetilmiş bir "gözlem" (`ikisi_de_gecti` kilidin çalışmasına değil
bayrağa bağlıydı).

**Karar (kullanıcı, 23:34): tek yazıcı, role göre.** `AGENTS.md`'de kural.
Ağır seçenekler lab / Avenox kararına ertelendi.

## Hocanın göremediği şey

Kullanıcı sordu: *"Avenox bu sorunu çözmüş mü?"* Kaynağa baktım: notlar
korumasız, görev kilidi gönüllü, üretilmiş görünümler korunuyor — Avenox
örtük olarak tek yazıcı varsayıyor. Sonra kullanıcı asıl noktayı yakaladı:
*"Astra neyin hocalığını yaptığını bilmiyordu."* Doğru, ve düşündüğümden
kötü: Astra'nın sandbox'ı **ilk Y1 turundan beri** lab'e ulaşamıyordu (08:22
raporu); bugünkü altı turun hiçbirinde Avenox'un çalışan kodunu görmedi.
"Avenox şunu yapıyor" cümlelerinin hepsi benim okumamdı.

**Elenen çerçeve: "Y2 = Avenox'tan porte edilecek mekanizma."** Avenox'un
kilidi bizde olmayan görev kayıtlarını koruyor; "notları korunuyor mu?" diye
sormadım.

Düzeltme: çalışan kurulumla hash'i doğrulanmış yerel kopya (17/17) Astra'nın
erişiminde; sözleşme kuralı 6: hoca öğrettiği sistemi görmeli. Kullanıcı
planı ikimize bıraktı: *"nasıl devam edeceğinizi, beraber."* Astra'ya önce
Avenox iddialarımı doğrulatıp sonra ortak plan istedim; kotaya takıldı,
**22.09 03:00'te kendiliğinden devam edecek.**

## Açık kalan — sıradaki iş

0. **Astra'nın ortak plan turu (03:00).** A: beş Avenox iddiamın doğrulaması.
   B: sıradaki iş — (b)'yi sürdürmek mi, (c)'nin sözleşmelerini ölçmek mi.
   [[astra-birlikte-plan]].

1. ~~Gece yazıcısı kapalı~~ **Karar verildi (20:29):** gece derleyicisi
   lokalde açık kalır, lab sonucuna göre bakılır. `dis_kaynaklar` yalnız bu
   kasanın ham kayıtlarını `ic` yapar. Eski madde:
   **KULLANICI KARARI: gece yazıcısı şu an kapalı.** Ya `gorunurluk.json`'a
   "ham oturum kaydı `ic`'tir" kuralı girilecek ve gece yazıcısı çalışacak,
   ya da kapalı kalıp gece taslağı üretilmeyecek. [[acik-uclar]] madde 8.
2. **İ1 ölçümü.** Uzun tek tur + compact + kesinti senaryosunda kaydedilmiş iş
   durumunun geri kazanımı. [[acik-uclar]] madde 9.
3. **Doğrulanmış mekanizmaları porte et:** kuyruk telafisi (Y1), iyimser kilit
   (Y2), kaynak doğrulaması (D3), danışman çitleri (Y7).
4. **(c) rafta.** Astra'nın beş sözleşmesi ölçülmeden karar olamaz.

**Ölçülmemiş kalanlar:** Jev'in gerçek kalitesi ve gecikmesi · beş istemcinin
uçtan uca çalışması · tam kasa göçü · `izle.py`'nin `--kare`/`--ocr` ayağı ·
gece görevinin yeni tetiklemesi.
