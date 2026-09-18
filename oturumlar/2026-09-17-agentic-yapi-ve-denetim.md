# Üçüncü oturum — 17.09.2026 01:59 – 18.09.2026 04:40

**90 kullanıcı mesajı, 4.247 KB ham kayıt.** Takvim süresi 26,7 saat; içinde
14,6 saatten fazla ara var (en uzunu 05:52 → 13:28, 7,6 saat).

Omurga okunarak yazıldı (`python araclar/omurga.py 7f10f7a3`).

Konu iki koldan ilerledi: **`izle.py` video hattının yeniden kurulması** ve
**agentic yapının ne olduğu** — ikincisi denetim katmanı tartışmasına, oradan da
gece derleyicisine üç somut eklemeye çıktı.

---

## 1. Hedef güncellendi: Nisan değil, Ekim sonu

Kullanıcı teslim tarihini öne çekti (01.59–02.21):

- **Ekim 2026 sonu.** Nar Ajans'ın *tüm dijital süreçleri* kendi kendine yürüyen
  bir AI sistemine bağlı olacak. Kasım'ın ilk haftası tolerans, ilerisi yok.
- **App security, kullanıcının kendi tanımıyla:** web sitesi ya da mobil
  uygulamayı production'a alırken açıkları kapatmak. Prompt injection ve benzeri
  AI-özelinde güvenlik **öncelik değil** — modelin önceki önerisi düzeltildi.
- **Nar Ajans bir ara adım**, nihai hedef değil: dijital işler otomatikleşecek,
  sonra kullanıcı kendi işlerine ve AI operatörlüğüne odaklanacak.
- **AI operatörlüğü tanımı netleşti:** "dijital iş gücü — manpower". Hearts of
  Iron 4 analojisi. Dijital işlerin tamamını alt ajan sistemlerine yönlendirmek
  **ve sistemin kontrollü, kararlı kalmasını sağlamak.** Son şart tanımın
  parçası.

**Model gücü konusunda net tavır:** "modelin etrafındaki kabuğu bilirsen modelin
önemi kalmaz" — shell, harness, bağlam yönetimi, loop, graph, paralelleştirme.
Modelin "makineye özgü ustalık eskir" karşı tezi **reddedildi**.

Ayrıntı: [[kullanici-baglami]].

## 2. Proje egemenliği kuralı kondu

*"Her proje, her klasör, her vault ayrı bir devlet gibidir."* Okunur, analiz
edilir, ama kullanıcı özellikle söylemedikçe **müdahale edilmez.** Nar Ajans'a
16–17 Eylül'de yapılan müdahale bir defalık "start verme"ydi ve bitti.

Yeni not açıldı: [[proje-egemenligi]]. Açık uçlardaki "Nar Ajans'tan devreden"
başlığı iş listesi olmaktan çıkarılıp tarihsel kayda dönüştürüldü.

## 3. Tarih hatası ve üç kökü — en pahalı ders

Model "8 Temmuz" dedi, kullanıcı itiraz etti, model **yanlış soruyu ölçtü.**
Üç kök ayrı ayrı çıkarıldı ([[yasanan-hatalar]] madde 19):

1. **Etiketsiz sayı taşındı** — bir cümlede konuşma tarihi, yükleme tarihi ve
   video süresi yan yanaydı, ikisi etiketsizdi.
2. **Belirsiz soru netleştirilmeden ölçüldü** — ölçüm doğruydu ama yanlış şeyi
   ölçtü, ve ölçüm yapmış olmak sahte güven verdi. *Doğrulama ritüeli yanlış
   hedefe uygulandığında hatayı düzeltmez, sertleştirir.*
3. **Araç tuzağı ölçüldü** — `ara.py` başlığındaki tarih `st_mtime`, yani
   kaydın son yazılma tarihi. Avenox oturumu başlıkta 07.09 görünüyor, konuşma
   30 Ağustos'ta.

**Kullanıcının kendi cevabı, sorulunca:** tarih önemli çünkü **modelin zaman
algısı yok.** *"Uzay boşluğunda seyahat eden bir foton gibisin; senin için her
şey aynı anda var gibi."* Bağlamda sıra var, süre yok.

Bu oturumda aynı kökten **beş hata** çıktı: tarih, "altı oturum" (dosya sayıp
oturum demek), "beş buçuk saat" (ölçülebilir şeyi tahmin etmek), "bu gece"
(saat 19:32'de), ve haftalık rapor ikilemi (üçüncü seçeneği atlamak).
**Beşini de kullanıcı yakaladı, sistem değil.**

## 4. Arşiv tarih kuralı düzeltildi

Kullanıcı haritada dün geceki oturumu bulamadı. Kayıt vardı ama üç kusur
üst üste binmişti: harita satırı oturumun ilk gününü anlatıyordu, dosya
başlıklarındaki tarihler yanlıştı (hatırlanarak yazılmışlardı), ve kapanış
yanlış dosyaya yazılmıştı — **oturumun baskın konusu, oturumun tamamı
sanılmıştı.**

Düzeltildi ve kural yazıldı ([[kapanis-ritueli]]): aralık ham kayıttan ölçülür,
hem başlık hem harita **saatiyle** taşır, kapanış oturumun kendi dosyasına
yazılır, harita satırı son iş kolunu değil tamamını özetler.

## 5. 4–7 Eylül boşluğunun arkeolojisi

Boşluk boş değilmiş: o aralıkta Nar Ajans'ta üç, Desktop'ta bir oturum var.
Ve asıl bulgu — **konuşma kopmadı, kimlik değişti:** klasör taşınmasıyla oturum
fork'landı, `6052d412` → `3c1530e9`. `BEYIN.md`'deki "7 Eylül'de taşındı"
iddiası düzeltildi; yeni yol anahtarındaki ilk damga 04.09 22:13.

Mükerrer oturum şüphesi de doğrulandı: `adbd10b1` iki yol anahtarında birden.
Ölçümler: [[olculmus-bulgular]] §4.

## 6. `izle.py` yeniden kuruldu — dört katmanlı hat

**Ölçülen kusur:** kare **sayısı** sabitti (24), sıklık değil. Tam videoda
41,6 saniyede bir kare — kullanıcının "belki 10 saniyede bir" tahmini iyimsermiş.

**Elenen fikir: `mpdecimate`.** Model önerdi, ölçüm çürüttü: 120 kareden
10'unu eledi, en agresif ayarda 34'ünü. Sebep — video animasyonlu metin slaytı,
ekran kaydı değil; "neredeyse özdeş kare" hiç yok. Tamamen elenmedi, ekran
kayıtlarında denenebilir.

**Seçilen:** yoğunluk parametresi (`--kare-sn`) + algısal hash elemesi
(120 → 29 kare). Üstüne **OCR** (Tesseract, Türkçe, D:/AI/tessdata) ve dördüncü
katman olarak **birleştirme**: Whisper + YouTube altyazısı + kare yazıları tek
zaman çizelgesinde, ayrışan kelimeler işaretli.

**Kurulurken çıkan kusur:** ilk birleştirme 38 kelimeyi ayrışma sandı, gerçek
sayı 5'ti — hizalama kayması. Karşılaştırma dar pencerede gösterilip **geniş
pencerede** yapılır oldu.

**İlk testte yakalanan gerçek ayrışmalar:** `bytecoder`/`bipecoder` (ikisi de
yanlış), `Hermes`/`her birisi` (karar verilemedi), `yorun`/`görün` (Whisper
yanıldı), `ayda`/`ayta` (altyazı yanıldı). İki tanığın **aynı yerde farklı
şekilde** yanılması en güçlü şüphe işareti.

**Kullanıcı talimatı, refleks olarak kaydedildi:** video verildiğinde **önce
sorulacak** — şema/diyagram var mı? Çünkü OCR şemada boş dönmez, kutu
etiketlerini okur ve model "içeriği gördüm" sanır. *"Gördüğünü zannedersin."*

**Yerel VLM kurulmadı**, gerekçesiyle: OCR işi çözdü, bağlam tasarrufu zaten
sağlandı. Ölçüt kondu — OCR boş/anlamsız dönerse ya da eşik her videoda elle
ayar isterse kurulur.

Ayrıntı: [[arac-izle]], ölçümler [[olculmus-bulgular]] §5.

## 7. Agentic yapı — yeni not ve dört şema

Kullanıcının sorusu: *"Codex'i nasıl çağırdın? Cevabı beklerken nasıl bir
moddaydın?"* Cevap [[agentic-yapi]] notunu doğurdu:

- **Üç katman, tek "ben" yok:** model (kesintili), harness (sürekli), bağlam.
- **Bekleme harness'ta.** Model o aralıkta hiç çalışmaz; `codex exec` kırk
  dakika sürse de `ls` kırk milisaniyede dönse de modele aynı görünür.
- **Codex bir Bash komutuydu**, özel protokol yok. İlişki tek yönlü.
- **Tanım:** agentic yapı, modelde olmayan dört şeyi ekleyen kabuktur — döngü,
  araçlar, durum, durma koşulu. *Ajan olan şey model değil, döngüyü çeviren
  programdır.*
- **Bağlam penceresi:** Opus 5 / Sonnet 5 / Fable 1M, Haiku 4.5 200K
  (`claude-api` referansından, tahmin değil).
- **En önemli incelik:** model her turda her şeyi okur ama **eşit okumaz.**
  Bağlamda olması, dikkat ettiği anlamına gelmez.

**Dört şema üretildi** ve okuma güzergahına göre yeniden adlandırıldı
(`Pictures/Screenshots`): 1 agentic döngü · 2 bağlamın içi · 3 kapanış yolları ·
4 birleşik. `notlar/agentic-dongu.svg` vault içinde, nota gömülü.

## 8. Denetim katmanı — tartışma ve karar

Kullanıcı: *"Sistemin deterministik çalışmasını istiyorum, hata yapmamalı.
Daha sık `/compact` mi atmalıyım?"*

**Cevap: hayır.** Determinizm yanlış katmanda aranıyordu. Model katmanı
olasılıksal; disk, hook'lar, araçlar deterministik. Kritik hiçbir yol modelin
**hatırlamasından** geçmemeli — ve kullanıcı bunu zaten kurmuş.

**Modelin `/compact` hakkındaki iddiası yanlış çıktı** ve kullanıcı düzeltti:
bu projede `PreCompact` omurgayı diske döküyor, ham kayıt da silinmiyor. Yani
compact geri dönülemez kayıp değil. Kalan risk: *veri duruyor ama erişim
tetiklenmiyor.*

**Diskten bağlama dönüşün üç yolu** ayrıştırıldı: enjeksiyon (zorunlu), arama
(gönüllü), denetim (yok).

**Kullanıcının en keskin itirazı:** *"Açıp bakma kararını yine model veriyor.
Ortada hiçbir sebep yokken kayıtlar neye göre açılacak?"*

**Çözüm:** arama olaya bağlıdır, **denetim takvime bağlanabilir.** Denetimin
sebebe ihtiyacı yok — cron açar, sırayla ve hepsini. Kullanıcı bunu da
düzeltti: *"Cron karar vermez, cron bir zamanlayıcı."* Doğru — ve cron'un
güvenilir olmasının sebebi tam olarak karar vermemesi.

**Denetçi neden model olabilir** (kullanıcı: "modelin üstünde üst akıl yok"):
denetçinin daha zeki olması gerekmiyor, **farklı bağlamda** olması yeterli;
doğrulama üretmekten kolaydır; ve hakem model değil **ham kayıt** — akıllı
değil ama değişmez.

**Karar: denetçi rapor eder, düzeltmez.** Düzelten bir denetçi kendi
düzeltmesini denetletmez; rapor zinciri sonlu, düzeltme zinciri değil.

## 9. `SessionEnd` boşluğu — ölçüldü ve karara bağlandı

Üç hook var, **kapanış hook'u yok.** Oturum kapatılmadan bırakılırsa kalıcı
katmana hiçbir şey geçmiyor.

**Elenen kurgu:** `SessionEnd`'de headless örnek doğurup notu ona yazdırmak.
Teknik olarak mümkün, yan faydası da var (temiz bağlam), ama iki kusuru var:
`SessionEnd` çökmede/güç kesintisinde hiç tetiklenmez, ve omurga yetmez.

**Seçilen kurgu:** *işareti ölen bant bıraksın, notu yaşayan bant yazsın.*
`SessionEnd` ucuz ve modelsiz olsun; pahalı iş gece derleyicisine bağlansın.
Ayrıntı: [[kapanis-ritueli]].

## 10. Side chat kör noktası — ve `izle.py`'nin ikinci işlevi

Kullanıcı bir side chat'te uzun bir konuşma yaptı, sonra **kaydırmalı ekran
kaydı** olarak getirdi. `izle.py` hattı 17 kare okudu, konuşma eksiksiz
kurtarıldı. Yani hat aynı zamanda bir **kurtarma aracı.**

Ve side chat'in kendi iddiası ana oturumdan doğrulandı: **`1bfbca18` kaydı
diskte yok.** Side chat'ler hiç kaydedilmiyor — ana oturumlar canlı yazılırken.
Arama bulmuyor, paralel oturum uyarısı görmüyor. [[olculmus-bulgular]] §6.

Side chat'teki örnek ayrıca **kendi sistem promptunu okumamıştı** — "read-only
tools" bağlamındaydı, fark etmedi; oturum kimliği değişti, MCP koptu, hiçbirini
görmedi. *Bağlamda olması dikkat ettiği anlamına gelmez* tezinin canlı kanıtı.

## 11. Gece derleyicisine üç ekleme — kuruldu ve doğrulandı

Kullanıcı sordu: *"Haftalık rapor kaçarsa ne olur?"* Ölçüm üç şey buldu:

- Görev kaçması **zaten telafi ediliyor** (`StartWhenAvailable = True`).
- Haftalık rapor **kaçmamıştı, sırası gelmemişti** — modelin kurduğu ikilem
  üçüncü seçeneği atlıyordu.
- **Beklenmeyen:** 18.09 00:30 çalıştırması çıkış kodu `0xC000013A` ile
  bitmişti; dosya yazılmış, commit atılmış, görev "Ready" görünüyordu.

**Kurulanlar** ([[gece-derleyicisi]]):

1. **Telafi** — "bugün hangi gün" yerine "bu hafta üretilmiş mi".
2. **İşaretçi denetimi** — her gece tüm işaretçiler açılır. İlk sürüm sessizce
   8 tanesini atlıyordu; desen esnetildi ve **üçüncü kategori** eklendi:
   *denetlenemeyen*. Negatif testle doğrulandı.
3. **Sağlık** — `son-calisma.json`; derleyici kendi kesintisini bildiriyor.

**İlk tam denetim: 40 işaretçinin hepsi doğrulandı.**

---

## Açık kalanlar

Tamamı [[acik-uclar]] içinde, sıralı. Özetle: `SessionEnd` kurulmadı, omurga
model tarafını taşımıyor, içerik denetimi ve kapanış denetimi yok, side chat
kör noktası çözümsüz (harness tarafında), `notlar/` 136 KB ile 65 KB eşiğini
iki katına çıkardı, paralelleştirme ertelendi.

**Ve bu oturumun kendi dersi:** beş model hatasının beşini de kullanıcı
yakaladı. Ekim hedefi "sistem kullanıcı başında durmadan çalışsın" olduğuna
göre, o denetçi çekildiğinde yerine konacak şey bu oturumun asıl konusuydu.

## Bu oturumda fark edilen küçük kusur

`omurga.py` **skill yüklemelerini kullanıcı mesajı sanıyor.** Bu oturumun
omurgasında `claude-api` skill'inin tamamı 46 numaralı "kullanıcı mesajı"
olarak görünüyor ve omurgayı gereksiz şişiriyor. Filtrelenmeli.
