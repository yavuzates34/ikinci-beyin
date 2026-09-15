# Kapanış ritüeli

Bir oturum bağlam kaybı olmadan nasıl kapanır, yenisi mirası nasıl devralır.
Kuralın uygulanabilir hâli [[CLAUDE]] içindedir; burada **neden öyle olduğu** yazar.

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
`matcher: auto` ile bağlı. Bağlam sıkıştırılmadan hemen önce çalışır.

**İki ayaklı, çünkü tek ayak güvenilmez.** Belge `PreCompact` için
`additionalContext` desteğini "muhtemelen" diye geçiyor:

1. **Deterministik ayak:** oturumun omurgası `derleme/omurga-anlik/` altına
   yazılır. Model hiçbir şey yapmasa, enjeksiyon hiç çalışmasa bile ham malzeme
   kurtulur. Bu dosya sıkıştırmadan etkilenmez — diskte durur.
2. **Best-effort ayak:** bağlama "şimdi yaz" uyarısı enjekte edilir; uyarı
   omurga dosyasının yolunu da taşır.

**Neden bloke etmiyor.** Hook, çıkış kodu 2 ile sıkıştırmayı engelleyebiliyor ve
bu ilk bakışta daha iyi görünüyor (model tam bağlamla yazardı). Seçilmedi:
sıkıştırma engellenir ve pencere zaten doluysa oturum sert bir sınıra çarpabilir.
**Ağın kendisi hasara yol açmamalı.** Onun yerine omurga dosyası kurtarma
malzemesi olarak bırakılıyor — sıkıştırma sonrasında bile oturum kaydı ondan
yazılabilir.

**Sınanan:** geçerli girdiyle doğru oturumu bulup omurgayı yazdığı ve geçerli
JSON ürettiği doğrulandı; bozuk girdide yedek yola düşüp yine çıktı ürettiği de.
**Sınanmayan:** gerçek bir sıkıştırma olayında enjeksiyonun modele ulaşıp
ulaşmadığı. İlk gerçek tetiklenmede görülecek.
