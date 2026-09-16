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

Bir oturum "işlenmiş" sayılır: kimliğinin ilk 8 karakteri `notlar/` ya da
`oturumlar/` içindeki herhangi bir dosyada geçiyorsa. Geçmiyorsa kapanış kaydı
yazılmamış demektir ve rapora, okuma komutuyla birlikte düşer.

Bu, kaynak gösterme kuralının beklenmedik bir yan faydası: işaretçiler aynı
zamanda "bu oturum işlendi mi" sorusunun cevabı oluyor.

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
