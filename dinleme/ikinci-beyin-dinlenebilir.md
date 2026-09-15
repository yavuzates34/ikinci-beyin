# İkinci Beyin: Mimari, Sınırlar ve Yol Haritası

Bu metin sesli dinlemek için yazıldı. Tablo, şema ve teknik kısaltma kullanılmadı.
Tarih: 4 Eylül 2026.

---

## Giriş: Neyi konuşuyoruz

Bir ikinci beyin kurmak istiyorsun. Yani tüm notlarının, kararlarının ve
birikiminin tek bir yerde durduğu, hangi yapay zeka aracını kullanırsan kullan
oradan beslenen bir sistem. Ve buna evden de dışarıdan da erişebilmek istiyorsun.

Bu metin dört şeyi anlatıyor. Birincisi, böyle bir sistemin parçaları neler ve
hangisi gerçekten önemli. İkincisi, notların birbirine nasıl bağlanıyor, daha
doğrusu neden şu anda bağlanmıyor. Üçüncüsü, mobilden erişim meselesi. Ve
dördüncüsü, en can alıcı olan: farklı yapay zeka uygulamalarındaki konuşmaların
neden birbirini görmüyor ve bu konuda gerçekten ne yapılabilir.

---

## Birinci bölüm: Sistemin parçaları

Ortada dört unsur var ve bunların birbirine karışması çok normal. Tek tek ayıralım.

Birincisi klasörün kendisi. Diskindeki sıradan bir klasör. İçinde markdown
dosyaları, görseller, ne koyarsan. Özel bir formatı yok, not defteriyle bile
açılır. Ve şunu baştan söyleyeyim: notlarını gerçekten tutan tek şey budur.
Diğer üçü ya ona bakan bir pencere, ya onu taşıyan bir araç, ya da yanına
konulmuş ayrı bir kutu.

İkincisi git ve github ikilisi. Bu ikisini birbirine karıştırman çok yaygın bir
durum, ayrımı şöyle: git, bilgisayarına kurulan bir programdır. Klasörünün
geçmişini kaydeder. İnternet gerektirmez, hesap gerektirmez. Github ise bir
internet sitesidir, Microsoft'a aittir, o geçmişin bir kopyasını saklar.

Benzetme yapayım: git, Word'ün değişiklikleri izle özelliği gibidir, dosyanın
her hâlini hatırlar. Github ise o dosyayı yüklediğin buluttur.

İki temel komut var, ikisi ayrı iş yapar. Commit dediğin şey, şu anki hâlin
fotoğrafını çek demektir ve bilgisayarında kalır. Push dediğin şey ise, biriken
fotoğrafları internete yolla demektir. Avenox'un videoda otuz beş bin değişiklik
birikmiş, henüz yollamadık demesi tam olarak bu ayrımdan geliyor. Fotoğraflar
yerelde birikiyor, internete arada bir gönderiliyor.

Git'i github olmadan kullanabilirsin, gayet mantıklıdır. Tersi anlamsızdır.

Üçüncüsü Obsidian. Burada bir düzeltme yapmam gerekiyor, çünkü baştan yanlış
anlamıştın: Obsidian sadece bir görüntüleyici değil. Notlar arasında bağ kurmak
onun ana özelliği. Bir notta iki köşeli parantez açıp başka bir notun adını
yazdığında, o tıklanabilir bir bağa dönüşür. Ayrıca hangi notların o nota bağ
verdiğini gösteren bir panel sunar, ve bütün notlarının bağlantı haritasını çizer.

Ama işin püf noktası şurada: o bağlar düz metin olarak dosyanın içinde durur.
İki köşeli parantez yazdığında dosyaya harfi harfine o karakterler yazılıyor.
Obsidian sadece onu tıklanabilir gösteriyor. Yani bağ verinin içinde, programın
içinde değil. Obsidian'ı yarın silsen bağların yerinde kalır.

Buradan çıkan sonuç şu: yapay zekanın Obsidian'a doğrudan hiçbir ihtiyacı yok.
Model dosyaları diskten okur. Obsidian tamamen senin için var, rahat okuyasın,
gezinesin diye. Ama dolaylı faydası gerçek: senin kurduğun bağları model de görür.

Dördüncüsü mem sıfır. Bu diğer üçünden farklı bir şey, çünkü klasöre bağlı değil,
yanında ayrı duruyor. Konuşmalar sırasında ortaya çıkan küçük gerçekleri kendi
veritabanında tutar ve onları anlamca aratmanı sağlar.

Aradaki fark şu: Obsidian bağını sen kurarsın, elle, tam isimle. Mem sıfır bağını
ise kimse kurmaz, anlam üzerinden bulunur.

Kontrol testi olarak şöyle düşün. Obsidian'ı silersen rahat okumayı kaybedersin,
notlar durur. Github'ı silersen uzak yedeği kaybedersin, notlar durur. Git'i
silersen geçmişi kaybedersin, notlar durur. Mem sıfırı silersen anlamsal
hatırlamayı kaybedersin, notlar durur. Ama klasörü silersen her şeyi kaybedersin.
Hiyerarşi bu.

---

## İkinci bölüm: Notların şu anda birbirine bağlı değil

Sordun: Obsidian bu bağı sağlamıyorsa ne sağlıyor.

Dürüst cevap: hiçbir şey. Yapısal bir bağ yok.

Elde olanlar sadece şunlar. Klasör yapısı, yani aynı klasördeki dosyaların aynı
konuya ait sayılması. Dosya adları, yani adından konusunun anlaşılması. İçeriğin
kendisi, yani iki notun da aynı konudan bahsetmesi. Ve son olarak, okuyan model.

Bu sonuncusu önemli. Modelin iki dosya arasındaki ilişkiyi anlaması, o dosyaları
okuyup kafasında birleştirmesiyle olur. Ama bu bağ hiçbir yere yazılmaz. O oturum
bittiğinde buhar olur. Ertesi gün başka bir oturum aynı işi sıfırdan yapar, hatta
yapmayabilir de.

Ve asıl kısıt şu: model, var olduğunu bilmediği dosyayı okuyamaz.

Bunun somut bir örneği bu oturumda yaşandı. Senin makinende, başka bir projenin
hafıza klasöründe, saatle ilgili bir not duruyor. İçeriği şu: saat bilgisini asla
tahmin etme, önce sistem saatini sorgula. Gerekçesi de yazılmış: Yavuz yanlış saat
bilgisini fark etti ve uyardı.

Yani sen bu uyarıyı daha önce, başka bir projede yapmışsın, yazıya da geçmiş.
Buna rağmen ben bugün aynı hatayı yaptım ve sen aynı uyarıyı ikinci kez yapmak
zorunda kaldın. Çünkü o dosya başka bir klasörde ve benim ondan haberim yoktu.

Notlarını saydım. Otuz yedi hafıza dosyan var. Bunların yedisinde bağ var,
otuzunda hiç yok. Yani sezgin doğruydu, çoğu izole. Bağ olan o yedi tanesini de
sen yazmamışsın, hafıza formatını takip eden modeller yazmış.

---

## Üçüncü bölüm: Mobil erişim

Sorduğun şey şuydu: yereldeki klasörüme mobilden nasıl erişirim.

Bu sorunun içinde ters bir varsayım var. Doğrusu şu: yerel, merkez olmaktan
çıkmalı.

Beynin bilgisayarında yaşadığı sürece her erişim yolu, bilgisayarın açık olması
şartına bağlanır. Dışarıdayken bu, makineyi uzaktan uyandırma oyununa döner. Ve
ileride çok sayıda agent çalıştırmak istediğinde tamamen çöker, çünkü o agentlar
senin masaüstünün uykudan uyanmasını bekleyemez.

Profesyonel kurulumda sıra tersine döner: beyin her zaman açık bir yerde yaşar,
yerel bilgisayarın onun kopyası olur. Avenox'un sunucusunda çalışan Hermes adlı
agentı tam olarak bu. Onun beyni sunucuda, laptopu sadece bir istemci.

Üç mimari var. Birincisi, beyin bilgisayarında. Bugün senin durumun bu. Telefondan
uzaktan kontrolle bağlanabiliyorsun, ki bunu bu sabah kurduk ve çalışıyor. Ama iki
sınırı var: bilgisayarın açık olmalı, ve bu yalnızca Claude ile çalışıyor.

İkincisi, beyin git deposunda. Github her zaman açık, her araç okuyabiliyor,
bedava. Okuma tarafı mükemmel çözülüyor. Yazma tarafı zahmetli ama imkansız değil.

Üçüncüsü, beyin her zaman açık bir sunucuda ya da ev sunucusunda. Kalıcı cevap bu.
Senin daha önce kendi ağzınla söylediğin şeydi zaten, sunucu kiralamak ya da bir
ağ depolama cihazı almak.

Mobilden yazma sorununun üç somut çözümü var. Birincisi, telefondan github'ın
kendi arayüzüne girip dosyayı düzenleyip kaydetmek. Hantal ama bedava ve bugün
çalışıyor. İkincisi, ki en zarif olanı, github üzerinde bir konu kaydı açmak.
Telefondan tek dokunuşluk iş. Kurduğun bir otomasyon o kayıtları alıp beyninde
gelen kutusu klasörüne not olarak yazar, sonra işlenir. Bunun güzelliği, hangi
araçta konuştuğunun fark etmemesi. Üçüncüsü sunucu, yani kalıcı çözüm.

---

## Dördüncü bölüm: En can alıcı mesele

Asıl sorun şu: farklı yapay zeka uygulamalarındaki konuşmalar birbirini görmüyor.

Diyelim Claude ile konuştun, önemli bir karar aldın, not olarak kaydettin. Sorun
yok. Ama birkaç saat sonra ChatGPT'de bir şeyler konuştun, karara bağlamadın,
sadece konuştun. Sonra tekrar Claude'a döndüğünde, Claude o konuşmadan haberdar
değil. Sana, bak sen bu konuyu geçen gün şöyle konuşmuştun diyemiyor.

Bunun neden böyle olduğunu ölçtüm, durum şu.

Claude Code konuşmalarını senin diskine yazıyor. Otuz yedi oturum, seksen üç
megabayt. Codex de aynı şeyi yapıyor, kendi klasöründe seksenden fazla oturum
kaydı var, mayıs ayına kadar geriye gidiyor. Yani bu iki araç, komut satırı
araçları oldukları için, her konuşmayı diske bırakıyor.

Ama ChatGPT uygulaması, Gemini ve Grok böyle değil. Onların konuşmaları kendi
sunucularında duruyor. Ve burada sert bir gerçek var: kapalı bir sohbet
uygulamasındaki konuşmaya canlı erişim yok. Bu bir ayar meselesi değil, mimari
bir gerçek. Bu şirketlerin geçmiş konuşmalarımı oku diye bir arayüzü yok.
Sundukları arayüz yeni cevap üretmek için, geçmişini okumak için değil.

Yani sorduğun senaryo, ChatGPT'de konuştuğumu Claude görsün, bugünkü teknolojiyle
doğrudan mümkün değil. Bunu böyle bilmek önemli, çünkü çözüm arayışını doğru yere
yöneltiyor.

Üç gerçek strateji var.

Birincisi, dönemsel dışa aktarma. ChatGPT'nin veri dışa aktarma özelliği var, tüm
konuşmalarını dosya olarak alabilirsin. Ayda bir indirip beynine koyarsın, bir
modele özetletirsin. Gerçek bir yöntem ama gecikmeli ve elle yapılıyor. Anlık
olarak, bunu birkaç saat önce konuşmuştuk bilgisini vermez.

İkincisi, konuşmanın yerini değiştirmek. Önemli konuşmaları kapalı uygulamalarda
yapmamak. Komut satırı araçlarında konuşursan kayıt zaten diske düşüyor.

Üçüncüsü, modeli kendi altyapına almak. ChatGPT uygulamasını kullanmak yerine
aynı modeli kendi sisteminden çağırmak. Model aynı model, ama konuşma senin
sistemine yazılıyor.

Şimdi burada Avenox'un bir cümlesi başka anlam kazanıyor. Videoda şöyle diyor:
asla sohbet arayüzünü kullanmam, her şeyi kendi vaultumun içerisinde yönetirim.

Ben bunu ilk duyduğumda bir üslup tercihi sandım. Değilmiş. Zorunluluk. Sohbet
arayüzünde konuştuğu her şey beynine erişilemez hale geliyor, o yüzden oraya hiç
girmiyor. Senin sorduğun problemi çözmüyor, oluşmasına izin vermiyor.

---

## Beşinci bölüm: Profesyonel mimarinin özeti

Yapay zeka operatörü olmak istiyorsan mimari şuraya oturuyor.

Bugünkü durumda beş ayrı kapalı bahçen var. ChatGPT kendi kutusunda, Gemini kendi
kutusunda, Grok kendi kutusunda, Claude kendi kutusunda. Beş ayrı hafıza ve
hiçbiri diğerini görmüyor.

Hedef mimaride ise ortada senin beynin var ve konuşmaların sahibi o. Modeller ise
takılıp çıkarılabilir motorlar. Yarın daha iyi bir model çıkarsa motoru
değiştirirsin, birikimin yerinde kalır.

Yani beş bahçeyi nasıl senkronlarım sorusunun cevabı, beş bahçen olmasın.

Bu arada senin kurulumunda bunun tohumu zaten var. Yüklü olan bir araç, birden
fazla modele aynı anda danışıp cevapları toplayabiliyor. Onu komut satırından
çalıştırdığında ne oluyor: diğer modellere soru gidiyor, cevapları bu oturumun
kaydına düşüyor, yani diske yazılıyor ve beynine erişilebilir oluyor. Üçüncü
stratejinin küçük ölçekli hâli bu.

Mem sıfırın buradaki yeri de kısmi bir köprü. Hem Claude'a hem ChatGPT'ye aynı
hafıza bağlanırsa, ikisinin yazdığı gerçekler ortak havuza düşer. Ama dikkat,
konuşmanın tamamını değil sadece açıkça kaydedilenleri taşır. Senin tarif ettiğin
karara bağlanmamış ama önemli konuşmalar bu yolla gelmez.

---

## Sonuç ve yol haritası

Özetle, ChatGPT'deki bir konuşmayı Claude'a gösteremezsin. Ama önemli konuşmaları
oraya hiç götürmeyerek problemi ortadan kaldırabilirsin. Bu senin için ciddi bir
alışkanlık değişikliği demek. Telefonda uygulama açmak kolay, komut satırına
gitmek zor. Profesyonelleşmenin gerçek maliyeti burada duruyor.

Yol haritası şöyle olabilir.

Birinci adım, beyni oluşturup git'e almak. Yeni bir klasör, içine mevcut notların,
sonra özel bir depoya göndermek. Bu tek adım seni bilgisayar açık olmalı hapsinden
çıkarıyor, en azından okuma tarafında.

İkinci adım, gelen kutusunu kurmak. Telefondan açılan kayıtların otomatik olarak
nota dönüşmesi. Mobilden yazma sorunu böylece bedava çözülüyor.

Üçüncü adım, mevcut komut satırı kayıtlarını birleştirmek. Claude ve Codex
tarafında toplam yüz on yediden fazla oturum kaydın var. Bunları tek yerde
aranabilir hâle getirmek, birikiminin büyük kısmını kullanılabilir kılıyor.

Dördüncü adım, ölçek gerektiğinde sunucuya taşımak. Ama bu ancak gerçekten çok
sayıda agent çalıştırmaya başladığında gerekiyor, şimdiden uğraşmaya değmez.

Son bir not. Bu sistemin asıl değeri, modelin daha zeki olması değil. Bu oturumda
defalarca gördük: hatalar zekâ eksikliğinden değil, geri besleme ve bağlam
eksikliğinden çıkıyor. Saat konusundaki hatayı ben yaptım, çünkü bilgi bana
ulaşmıyordu. Bilgiyi getiren bir mekanizma kurulduğu anda hata durdu. Öğrenme
modelde değil, altyapıda birikiyor.
