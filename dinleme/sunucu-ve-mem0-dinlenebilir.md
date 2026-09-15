# Sunucu Nerede Çalışmalı ve Mem Sıfıra Gerçekten İhtiyaç Var mı

Sesli dinlemek için yazıldı. Tarih: 4 Eylül 2026, akşam.

---

## Birinci soru: Harness sunucuda mı çalışmalı

Sorun şuydu: Raspberry Pi gibi sürekli açık bir cihaz alsam, Codex ve Claude Code
gibi araçların orada mı çalışması gerekiyor, yoksa kendi bilgisayarımda çalışıp
sadece dosya mı aktarsam yeter mi.

Cevap: ikisi de olur, ama farklı şeyler kazandırır. Üç yapılandırma var, tek tek
anlatayım.

Birinci yapılandırma. Araçlar senin bilgisayarında çalışır, beyin Raspberry Pi'de
durur, aralarında düzenli aktarım olur. Bilgisayarında çalışırken beynin bir
kopyası yanındadır, işin bitince gönderirsin. Bu durumda Pi sadece bir depo ve
buluşma noktası olur. Kendi başına hiçbir şey yapmaz.

Avantajı, bilgisayarının tam gücünü kullanman. Dezavantajı, beyin ancak sen
gönderdiğinde güncellenir. Ve sen bilgisayarını kapattığında Pi'de kimse
çalışmıyor demektir.

İkinci yapılandırma. Araçlar yine bilgisayarında çalışır ama beynin durduğu
klasörü ağ üzerinden doğrudan açarsın. Yani Pi'deki klasör senin bilgisayarında
bir sürücü gibi görünür.

Avantajı, aktarım adımı yok, her şey anlık güncel. Dezavantajı iki tane. Birincisi
ağ üzerinden çok sayıda küçük dosya okumak yavaştır ve bu araçlar tam olarak bunu
yapar. İkincisi evden çıktığında bağlantı kopar.

Üçüncü yapılandırma. Araçlar Raspberry Pi'nin kendisinde çalışır. Sen telefondan
ya da bilgisayarından uzaktan bağlanırsın.

Avantajı, bilgisayarın kapalıyken bile sistem çalışır. Telefondan iş
başlatabilirsin. Dezavantajı, Pi'nin gücü sınırlıdır.

---

## Burada önemli bir yanlış anlaşılma var

Şunu netleştirmek istiyorum, çünkü karar verirken en çok bunu yanlış hesaplarsın.

Raspberry Pi zayıf bir cihaz, bu doğru. Ama bu araçların ihtiyaç duyduğu güç
sandığın yerde değil.

Claude Code ya da Codex çalıştığında asıl ağır iş modelin kendisinde olur. Ve
model senin cihazında çalışmaz, bulutta çalışır. Cihazın yaptığı şey, isteği
göndermek, cevabı almak, dosya okuyup yazmak ve komut çalıştırmak. Bunlar hafif
işlerdir.

Yani bir Raspberry Pi, bu araçları çalıştırmak için fazlasıyla yeterlidir. Zayıf
olması bir engel değil.

Ama sınırları da var ve bunlar gerçek.

Kod derlemek, paket kurmak, test çalıştırmak gibi işler Pi'de yavaştır. Büyük bir
projeyi orada geliştirmek eziyet olur.

Ve kesinlikle yapamayacağı bir şey var: ekran görüntüsü işleme, video çözümleme,
konuşmayı metne çevirme gibi işler. Senin bilgisayarında bir ekran kartı var ve
biz o kartla dakikalar süren işleri saniyelere indiriyoruz. Pi'de böyle bir şey
yok. O tarafın bilgisayarında kalması şart.

---

## Önerdiğim bölüşüm

Bu yüzden ikili bir yapı öneriyorum. Ne tamamen Pi'de, ne tamamen bilgisayarında.

Raspberry Pi'de şunlar dursun. Beynin kendisi, yani bütün notların. Sürekli açık
kalması gereken hafif işler. Mesela akşam derleyicisi, yani gün içinde biriken ham
notları düzgün notlara dönüştüren işlem. Mesela telefondan gelen kayıtları
yakalayıp gelen kutusuna yazan işlem. Bunlar saniyeler süren, güç istemeyen işler.

Bilgisayarında ise şunlar kalsın. Gerçek proje geliştirme, kod yazma ve derleme.
Video ve görsel işleme. Ekran kartı gerektiren her şey.

İkisi arasındaki bağ da düzenli aktarımla kurulur. Bilgisayarında çalışırken
beynin bir kopyası yanında olur, iş bitince gönderirsin. Pi de kendi işini yapıp
sonucu oraya yazar.

Bu, Avenox'un yaptığının aynısı. Onun sunucuda çalışan bir agentı var ve
laptopunda da çalışıyor, ikisi aynı beyni paylaşıyor.

Bir de şunu ekleyeyim. Raspberry Pi almadan önce şunu dene: bilgisayarını bir
süre kapatmadan bırak ve uzaktan bağlanmayı test et. Belki ihtiyacın olan şey yeni
bir cihaz değil, mevcut makineni uyku moduna girmeyecek şekilde ayarlamaktır. Para
harcamadan önce ölçmeye değer.

---

## İkinci soru: Mem sıfıra gerçekten ihtiyaç var mı

Bu soruyu doğru soruyorsun ve cevabım muhtemelen beklediğinden farklı olacak.

Şu an itibarıyla hayır. İhtiyacın yok. Sebebini anlatayım.

Mem sıfırın sana sunduğu iki şey var. Birincisi otomatik çıkarım. Yani konuşurken
neyin hatırlanmaya değer olduğuna kendisi karar verir, sen uğraşmazsın. İkincisi
anlamsal arama. Yani bağ kurmadığın notları anlamlarına göre bulur.

Şimdi senin durumuna bakalım. Sen beyni sıfırdan kuruyorsun. Notlar yazılırken
birbirine bağlanacak. Akşam derleyicisi gelen ham notları alıp mevcut notlarla
ilişkilendirecek. Yani ikinci faydayı zaten kendi sisteminle üretiyorsun.

Birinci faydaya gelince, otomatik çıkarım kulağa iyi geliyor ama iki yüzü var.
Neyi hatırlayacağına o karar verir. Sen ne kaydettiğini görmezsin. Yanlış bir şey
çıkarırsa ya da önemli bir şeyi atlarsa, bunu ancak eksikliğini yaşadığında fark
edersin. Bu, üzerine çok konuştuğumuz sessiz başarısızlık türünden bir şey.

Ve daha önemli bir sakınca var. İki hafıza sistemi birbiriyle çelişebilir.
Notlarında bir şey yazar, mem sıfırda başka bir şey durur. Hangisi doğru? Bu
soruyla uğraşmak, tek bir sistemin eksikliğiyle uğraşmaktan daha kötüdür.

Yani şu aşamada mem sıfır eklemek, çözmek üzere olduğun bir problemi ikinci kez,
farklı bir yerde çözmek olur.

---

## Peki ne zaman gerekir

Bir tane gerçek tetikleyici var ve onu net söyleyeyim.

Kapalı bulut uygulamaları senin dosyalarını okuyamaz. Raspberry Pi'ndeki bir
klasöre ChatGPT erişemez. Ama bir hafıza servisine erişebilir, çünkü o servis
internet üzerinden çağrılabilir bir arayüz sunar.

Yani mem sıfırın senin için tek gerçek üstünlüğü şu: kapalı uygulamaların
ulaşabileceği tek hafıza katmanı olması.

Ama dikkat, bu üstünlük sandığın kadar büyük değil. Çünkü mem sıfır konuşmanın
tamamını değil, sadece oraya açıkça yazılanları tutar. Senin asıl derdin olan
karara bağlanmamış konuşmalar yine gelmez.

Dolayısıyla şu kuralı koyabilirsin. Mem sıfırı, birden fazla kapalı uygulamanın
aynı gerçekleri görmesi gerektiğinde düşün. Ondan önce değil.

---

## Onun yerine ne yapmalısın

Mem sıfırın verdiği anlamsal aramayı kendi makinende, bedava, dışarıya hiçbir veri
çıkmadan kurabilirsin.

Mantığı şu. Notlarının her birini bir modele okutup anlamlarını sayısal bir
temsile çevirirsin. Sonra bir soru sorduğunda o soru da aynı şekilde çevrilir ve
anlamca en yakın notlar bulunur. Bağ olmasına gerek yok, dosya adını bilmene gerek
yok.

Bu tam olarak görseller için kullandığımız aracın yaptığı şeyin metin versiyonu.
Aynı mantık, aynı model ailesi. Senin makinende çalışıyor, hiçbir ücreti yok,
veri dışarı çıkmıyor.

Yani mem sıfırın iki faydasından birini kendi sistemin zaten üretecek, diğerini
de yerel olarak kurabilirsin. Geriye sadece kapalı uygulama meselesi kalıyor ki
o da şu an senin en acil sorunun değil.

---

## Toparlarsak

Harness sorusuna cevap: bilgisayarında da çalışabilir, Pi'de de. Doğrusu ikisi
birden. Beyin ve hafif sürekli işler Pi'de, ağır işler ve ekran kartı gerektiren
her şey bilgisayarında. Aralarında düzenli aktarım.

Pi'nin zayıf olması engel değil, çünkü asıl güç modelin çalıştığı yerde ve orası
bulut. Ama video işleme ve derleme gibi işler kesinlikle bilgisayarında kalmalı.

Cihaz almadan önce mevcut makineni sürekli açık bırakmayı dene, belki yeterlidir.

Mem sıfır sorusuna cevap: şu an gerek yok. Sağladığı iki faydadan birini kendi
kuracağın sistem zaten üretecek, diğerini yerel olarak bedava kurabilirsin. Tek
gerçek gerekçesi kapalı uygulamaların erişebileceği ortak bir hafıza olması ve o
da şimdilik önceliğin değil.

İki hafıza sistemi kurmak, birinin eksiğiyle yaşamaktan daha zahmetlidir.
Önce birini düzgün kur, eksiğini yaşa, sonra karar ver.
