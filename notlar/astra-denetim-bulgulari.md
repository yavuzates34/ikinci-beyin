# Astra denetimi — güncel sınırlar ve düzeltmeler

> Merkez: [[BEYIN]] · Kanıtlar ve test çıktıları: [[2026-09-20-astra-kontrol]] ·
> İlgili: [[olculmus-bulgular]] · [[gece-derleyicisi]] · [[kapanis-ritueli]] ·
> [[arac-arsiv]] · [[acik-uclar]] · [[2026-09-19-sunum-onarim-listesi]]

## Arşiv ve kapanış

**En büyük ham dosya tam kayıt olmayabilir.** Üç Codex oturumunun elenen
parçalarında 69 + 4 + 8 = **81 farklı mesaj** bulundu. `kayit.py` artık aynı
mantıksal oturumu tek sayar, bütün parçaların farklı mesajlarını zaman
sırasıyla okur. Birleşik mesaj sayıları 179 / 21 / 30. Ham dosyalar
taşınmadı/silinmedi. Semantik aramanın önceden oluşturulmuş gömme indeksi
ayrı bir önbellektir; yeniden kurulması bu turda yapılmadı.
(codex 01a0bc5c-f1c4 · 20.09 04:22)

Başlangıç bağlamı kardeş oturumun kapanış kimliğini verebiliyor, bağlam
ölçümü yanlış oturuma bakabiliyordu. Artık **tam kimlik korunur, belirsiz
önek seçilmez**. PreCompact transcript yokken verilen kimliği arar;
“en son yazılan” oturumu tahmin etmez. Kurtarma dosyaları tam kimlik ve
mikrosaniye taşır; semantik aramanın okuma komutu da tam kimlik kullanır.
(codex 01a0bc5c-f1c4 · 20.09 04:15)

**Taslak kapanış yetkisi taşımaz.** Modelin kapanış satırı yazdığı taslak
çıktısı reddedilir. Kapanış okuyucusu taslakları ve kod çitindeki örnekleri
kabul etmez. Eski kısa kapanış işareti yalnız benzersizse çözülür. Bozuk
kaynak kimliği sessizce atlanmaz, “denetlenemeyen” diye raporlanır.
(codex 01a0bc5c-f1c4 · 20.09 04:15)

## Kurtarma ve gerçek otomasyon

Codex Desktop harita/saat enjeksiyonu ve **%50 uyarısı canlı doğrulandı**:
20.09 04:26:03, 162.272 / 258.400 token, `hooks.additional_context`, mevcut
kurtarma dosyası. **%70 de 05:46'da canlı doğrulandı:** 219.146 / 258.400 token, aynı hook
türü ve kurtarma dosyası. Canlı PreCompact ölçülmedi. Kontrol
yalnız yeni kullanıcı mesajında; uzun tek araç döngüsünün içinde yoktur.
(codex 01a0bc5c-f1c4 · 20.09 05:46)

Bağlam durumuna süreç kilidi eklendi; iki eşzamanlı Python yazıcısının
güncellemesi korundu. Kurtarma yazılamazsa hata bildirilir ve tekrar denenir;
pencere bilinmiyorsa “ölçülmedi” uyarılır. Devir kutusu oturum kimlikli,
kilitli kuyruktur; bir oturum diğerinin mesajını ezmez/kendi mesajı sanmaz.
Bu düzeltmeler sentetik testten geçti; iki canlı uygulamanın eşzamanlı
PreCompact olayı ölçülmedi.
(codex 01a0bc5c-f1c4 · 20.09 04:26)

Claude'un 1M penceresi hâlâ **kalibrasyon**. Daha sağlam belgelenmiş kaynak
status line JSON'undaki `context_window.context_window_size`; yerelde bu
kanal bağlanmadı. [Üretici belgesi](https://code.claude.com/docs/en/statusline).
(codex 01a0bc5c-f1c4 · 20.09 04:26)

## Gece ve yedek

20.09 kesintisi doğrulandı (`0xC000013A`), fakat “commit hiç çalışmadı”
iddiası yanlış: **`67779e9`, 00:30:05** derleme commit'i mevcut. O çalışmanın
push sonucu ve kesintiyi kimin/neyle başlattığı ölçülmedi.
(codex 01a0bc5c-f1c4 · 20.09 04:22)

Kullanıcı onayıyla görev eylemi gizli PowerShell'e alındı, log tamponlaması
kapatıldı, süre 15 dakikadan 1 saate çıktı: üç model çağrısının her biri
900 saniye sürebilir. 00:30 tetik ve Interactive giriş türü korundu; eski
XML projede yedeklendi. Kuru çalışma ve kayıtlı ayarlar doğrulandı;
**yeni ayarın zamanlanmış gece sonucu ölçülmedi**.
(codex 01a0bc5c-f1c4 · 20.09 04:26)

Git dönüş kodları denetlenir; yerel tracking ref uzak başarı kanıtı sayılmaz.
Taslak/commit/bakım hataları başlangıçta görünür. Aylık ince-kayıt oranı
ilgili oturumun arşivinden hesaplanır. `--kuru --oturum` gerçekten
yazmaz/model çağırmaz. 30 günden eski omurgalar otomatik silinmez.
(codex 01a0bc5c-f1c4 · 20.09 04:26)

## Bu projenin yeni Codex bağlam ayarı

Kullanıcı isteğiyle pencere 1.050.000 istendi. Yeniden başlatmadan sonra
**canlı etkin pencere 828.400** oldu (önce 258.400). Yerel Codex kataloğu
`max_context_window=872000`, etkin pay %95 gösteriyor; 1M isteği bu sınıra
kırpılıyor. API model sınırı ile Codex kataloğunun sınırı aynı değil.
Katalog elle değiştirilmedi. Compact eşiği etkin pencerenin altında
**750.000** yapıldı; global ayarlar değişmedi. Büyük penceredeki gerçek
%50/%70 olayları ve 750K compact henüz ölçülmedi.
[API model sınırı](https://developers.openai.com/api/docs/models/gpt-6-astra) ·
[Ayarlar](https://learn.chatgpt.com/docs/config-file/config-reference).
(codex 01a0bc5c-f1c4 · 20.09 05:47)
