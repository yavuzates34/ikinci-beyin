# Kullanıcı bağlamı

Hedefler, zaman kısıtı, öncelik sırası ve çalışma tarzı tercihleri.

> Merkez: [[BEYIN]] · İlgili: [[acik-uclar]]

---

> Mali detaylar bilinçli olarak bu dosyaya yazılmadı. Kaynak: 4 Eylül'de yüklenen
> iki ChatGPT devir belgesi (`.claude/uploads/` altında).

**Hedef:** AI operatörlüğü. Klasik istihdam değil — kendi projelerini
üretebilmek, bir işverene bağımlı olmadan ekonomik değer üretebilmek.

**Teslim tarihi — 17 Eylül'de öne çekildi.** Eski hedef "2027 ilkbaharı"
ve aşağıdaki Nisan ölçütüydü; artık geçersiz. Yeni hedef: **Ekim 2026 sonu**,
Nar Ajans'ın *tüm* dijital süreçleri kendi kendine yürüyen bir AI sistemine
bağlı olacak. Kasım'ın ilk haftası tolerans bölgesi, daha ilerisi kabul
edilmiyor. Kullanıcının ifadesi: "bunu yapacak zamanım, rutin planım da var."
Eldeki süre 17 Eylül itibarıyla ~6 hafta. (claude 7f10f7a3 · 17.09 02:09)

**Neden AI operatörlüğü:** Sekiz iş fikri var (Nar Ajans, hayalet mutfak,
müteahhitlik, vize danışmanlığı, İngilizce uygulaması, YouTube, abonelikli web
platformu, trading botu). Hepsinin ortak paydası: müşteri kazanma, ürün geliştirme,
operasyon otomasyonu. **Bir insan sekiz iş yürütemez; tekrarlayan kısımları
sistemlere devreden bir insan yürütebilir.** AI operatörlüğü meslek değil, kaldıraç.

**Birinci öncelik: Nar Ajans** — catering, fuar personeli ve etkinlik personeli
şirketi (dijital ajans **değil**). Kullanıcı orada müşteri kazanma motorunu kuruyor:
cold mail, Instantly, HubSpot, lead toplama, ileride Meta Ads.

**Zaman yapısı:** Saha işi haftanın 7 günü, 16:30–03:00. Uyku ~04:00–11:00. Geriye
11:00–16:30 kalıyor — çalışma penceresi bu, sıfır boşluk. Saha işi ~1 Ocak 2027'ye
kadar sürecek. Yani **Ocak sonrası ilk dört ayın üç katı zaman olacak**; derin
öğrenme ikinci yarıya bırakılmalı.

**İkinci teknik hedef: App Security — kullanıcının kendi tanımıyla.**
Kastettiği şey: bir web sitesini ya da mobil uygulamayı production'a alırken
arkasında kalabilecek güvenlik açıklarını kapatmak. Yani açık taşıyan bir
uygulamayı, siteyi, aracı internete koymamak. Eğitim ihtiyacı burası.
Prompt injection ve benzeri AI-özelinde güvenlik konuları **şu an öncelik
değil**; gerekli olduğu gösterilirse öğrenilir, kendiliğinden öne sürülmez.
Bu, daha önce bu notta yazan önerinin (güvenliği AI operatörlüğünün alt
boyutu olarak öğren) kullanıcı tarafından düzeltilmiş hâlidir.
(claude 7f10f7a3 · 17.09 02:09)

**Kendi belgesinde yazan 1 numaralı risk:** aynı anda fazla işe başlamak.
Önerilen: teslim tarihine kadar ikinci bir iş fikrine hiç başlanmasın. Tarih
öne çekildiğine göre bu kural gevşemedi, sertleşti.

~~**Nisan ölçütü**~~ → **Ekim sonu ölçütü:** Sertifika veya izlenen video
değil — *Nar Ajans'ın dijital süreçleri, kullanıcı başında durmadan çalışıyor
mu.* Ölçüt aynı kaldı, tarih öne çekildi.

### Ekim hedefinin bilinen zemini

17 Eylül'de netleşenler (claude 7f10f7a3 · 17.09 02:21):

- **İnternete açık yüz var.** `ajansnar.net` Vercel'de **canlıda**, ama bilinçli
  olarak kimseye gösterilmiyor: ne kartvizitte, ne cold mail attığımız firmalara.
  Site yokmuş gibi davranılıyor. Sebep tek: **logo.** Eski N+A harfli logo
  kullanılamıyor, meyve-nar logosu ise sitedeki tasarıma uymuyor. N+A logosu
  tasarıma çok daha uygun ama Derya onu kabul etmedi. Yeni logo aranıyor.
- Kullanıcı siteyi Vercel'den geri çekmeyi mantıklı buluyor ama **şimdilik
  dokunmak istemiyor**; canlıda kalsın diyor.
- Site ve geliştirme dosyaları `Desktop\Nar Ajans - Codex` altında
  (`nar-ajans/`, `design-source/`, `Nar Ajans - Logolar/`). O klasöre **okuma
  izni verildi**; yazma yok, orası kendi ajanlarının alanı.
- **Saha işi askıya alınabilir.** 1-2 haftalık askı opsiyonu var, henüz net değil.
  Kullanıcı ihtimal olarak söyledi, karar değil.

### Asıl plan: Nar Ajans bir ara adım

Nar Ajans otomasyonu nihai hedef değil, **önündeki engel.** Sıra şu: gerekli
dijital işlemleri otomatize et, sonra kendi işlerine yönel ve AI operatörlüğü
sürecine tam odaklan. Kimlik hedefi: **2027'nin ilk çeyreği bitmeden "ben bir
AI operatörüyüm" diyebilmek** — kullanıcının kendi ifadesiyle "hatta AGI
operatörüyüm", çünkü o tarihteki modelleri AGI seviyesinde bekliyor.
(claude 7f10f7a3 · 17.09 02:21)

### AI operatörlüğü — kullanıcının kendi tanımı

"AI operatörüyüm diyebilmek" ölçülemez bir kimlik hedefi demiştim; kullanıcı
düzeltti. Kastettiği şey ölçülebilir ve şu (claude 7f10f7a3 · 17.09 02:39):

**Dijital bir iş gücü — "manpower".** Hearts of Iron 4'teki manpower gibi
düşünülecek: dijital taraftaki yüksek kas gücü. Dijital işlerin tamamını
AI operatörlüğüyle halledebilmek, her şeyi alt ajan sistemlerine yönlendirip
onlara yaptırabilmek, ve **sistemin kontrollü ve kararlı kalmasını sağlamak.**
Son şart tanımın parçası, süsü değil.

**Model gücü konusunda:** rakipte de aynı model olacak, bu doğru — fakat asıl
mesele onu nasıl kullanacağını bilmek. Kullanıcının analojisi: bir F1 pilotuna
bir de MotoGP pilotuna aynı güçlü motosikleti ver; MotoGP pilotu daha iyi
kullanır. Yani gelecek için kendini eğitmek. Kimseyi bu yoldan kısıtlamak ne
mümkün ne etik.

**Modelin önemi konusunda — net tavır.** "Makineye özgü ustalık model
değişince eskir" dedim; kullanıcı reddetti ve daha güçlü bir tez koydu:
*modelin etrafındaki kabuğu bilirsen modelin önemi kalmaz.* Kabuk derken
saydıkları: shell/harness, bağlam yönetimi, loop, graph, paralelleştirme
"ve daha sayamadığım birçok sistem". Model düşük bir Sonnet de olabilir,
yüksek bir Fable/Astra da — eldeki işe göre planlama yapılır. Eğitimin
konusu model değil, **modelin etrafındaki dünya.**
(claude 7f10f7a3 · 17.09 02:54)

**Komutanlık:** "Bu süreçte iyi bir komutan olacağımı düşünüyorum."

**Bakım yaklaşımı:** Çıktı kalitesi sürekli takip edilecek. Sistemin yapısı
kuş bakışı, kullanıcının anlayabildiği ölçüde kendisi tarafından incelenecek;
anlaşılmayan yerde **orkestratör ajanlardan öğrenilerek** anlaşılacak. Yani
kullanıcı her katmanı tek tek okumayı değil, katmanı anlatacak bir muhatap
bulundurmayı planlıyor.

**Rakip görüşü:** Sektör fark etmeksizin rakipleri rakip olarak değil,
bilgilerinden faydalanılabilecek **ortaklar** olarak görüyor.

### Instagram — düzeltme

"Siteniz yoksa tamamen görünmezsiniz" iddiam eksikti, kullanıcı düzeltti:
**her mailde Instagram bağlantısı veriliyor** ve tüm geçmiş işler orada.
Yani dışarıdan doğrulanabilir bir varlık zaten var; site o varlığın tek yolu
değil. Logo meselesi için kullanıcı iPhone'unda her gece 00:00'da çalan bir
anımsatıcı kurdu; en geç bir-iki hafta içinde kendi çözecek. Logo üretme
teklifim masada ama öncelik verilmedi — ısrar edilmeyecek.
(claude 7f10f7a3 · 17.09 02:39)

### Neden tarih bu kadar önemli — kullanıcının cevabı

17 Eylül'de doğrudan soruldu. Esas sebep tek ve yapısal: **modelin zaman algısı
yok.** Kullanıcının analojisi: *"Sen uzay boşluğunda seyahat eden bir foton
gibisin. Senin için her şey aynı anda var gibi."* (claude 7f10f7a3 · 17.09 04:29)

Teknik karşılığı tam oturuyor: bağlamda **sıra** var ama **süre** yok. İki mesaj
arasında altı gün geçmesiyle altı saniye geçmesi, damga olmadığında model için
ayırt edilemez — ikisi de art arda iki blok. Bu yüzden modelin "dün", "az önce",
"hâlâ" gibi kelimeleri yapısal olarak güvenilmez: süre gerektiren kelimeler,
süre duygusu olmayan bir yerde kullanılıyor.

Mekanizmanın tamamı: [[agentic-yapi]].

Sonuç: **zaman bilgisi her seferinde dışarıdan verilmeli, içeriden üretilemez.**
Fotonun kendi çerçevesinde zaman geçmez, ama gözlemci için geçer — saati tutan
hep dışarısıdır. Kullanıcının kurduğu `UserPromptSubmit` tarih hook'u ve
notlardaki kaynak işaretçileri tam olarak bu dışarıdaki saattir.

Kullanıcı diğer çıkarımları da (zamanın en kıt kaynağı olması, tarihin
denetim mekanizması olması) doğru buldu, ama asıl sebep bu.

### Nar Ajans'ta iş bölümü

**Saha operasyonu Derya'da.** Personel ve catering akışının takibini kullanıcı
değil Derya yapıyor. Kullanıcının alanı **dijital taraf**: müşteri kazanma,
otomasyon, site. Logo kararı da Derya'dan geçiyor.
Kapsam açısından önemli: Ekim sonunda otomatikleşecek olan şey dijital taraf,
saha operasyonu değil. (claude 7f10f7a3 · 17.09 04:29)

**Saha işi durumu:** 17 Eylül'de işe çıkmadı, "muhtemelen bir iki gün daha
çıkmayacağım" dedi. Askı opsiyonu fiilen kısmen başlamış durumda.

### Çalışma tarzı tercihleri

- Superpowers skill'lerini kullanma (ayrı hafıza notu var)
- Mikro plan, saat saat program, uzun kontrol listesi istemiyor — büyük resim ve
  stratejik çerçeve tercih ediliyor
- Nötr ve saygılı Türkçe; "kanka/bro/kral" gibi hitaplar kullanılmamalı
- İş fikirlerini sadece destekleme, **eleştirel değerlendir**
- Sesli dinlenecek çıktılarda tablo/şema/dosya yolu kullanma
- Verbose arayüzü kullandığı dönemlerde thinking'in **Türkçe** yazılmasını
  istiyor (19.09)
- Uzun cevaplara madde madde "reply" veriyor. Tek cevapta toplanmasını
  istiyor. Uyku düzeni bozuk olduğu için reply'lar arasında saatler olabilir.

### Bu beynin amacı — kullanıcının tanımı (19.09)

Playground **kontrollü deneme ortamı**. Burada başarılı olan yapı sonra diğer
projelere ve vault'lara taşınacak. Hedef bir "Jarvis": hiçbir şeyi unutmayan,
kendi kendine yeten bir beyin. Jarvis'ten tek farkı, konuşmanın sesli değil
yazılı olması.

**Sağlayıcıdan bağımsız olmalı.** Beyin bir altyapıdır, tek bir sağlayıcının
uygulaması değil. Codex tarafı (GPT-5.6, Sol, Astra) zaman zaman burada
çalışacak. İleride yerel modeller ve Çin modelleri de gelecek. Açık uç:
[[acik-uclar]]. Paralel çalışma da hedefte, ama "birkaç seviye sonra".

---
