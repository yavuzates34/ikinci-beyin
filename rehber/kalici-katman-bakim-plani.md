# Kalıcı katmanı bölme planı — 20 Eylül 2026

**Öneri; henüz uygulanmadı.** Dosya taşıma, metin budama ve silme için
kullanıcının ayrıca onayı gerekir. Mevcut izin test klasörleriyle sınırlı.

> Merkez: [[BEYIN]] · İlgili: [[acik-uclar]] · [[ikinci-beyin-mimarisi]] ·
> [[2026-09-20-toparlama-ve-sunum]]

## Ölçüm ve amaç

Başlangıç ölçümü 16 kalıcı not **128,5 KB**; 17:31 yeniden ölçümü **129,1 KB**.
100 KB bölme eşiği yaklaşık 29 KB aşılmış. Dosyaları
yalnız ikiye bölüp ikisini de `notlar/` içinde tutmak toplamı azaltmaz.
Amaç, güncel karar ve yöntemi kısa konu notunda; eski deneme, ölçüm dökümü
ve değişen durumların tarihçesini `oturumlar/` içinde tutmak.

Ölçüm: `derleme/astra-kontrol/not-boyutlari.json`. Aşağıdaki hedefler
**tahmin**, uygulanmış sonuç değil. Yeni iddia doğrulanmadan metin
“güncel” diye birleştirilmeyecek.

## Önerilen ilk paket

| Kaynak | Şimdi | Sıcak hedef | Korunacak güncel çekirdek | Soğuk tarihçe |
|---|---:|---:|---|---|
| `olculmus-bulgular.md` | 22,45 KB | ~7 KB | Son doğrulanmış davranış, sınır, tek kaynak adresi | §4 arşiv arkeolojisi, §5 ayrıntılı kare deneyi; §7–10 geçmiş ölçüm dökümleri; §14 güven öncesi/sonrası, §15 eski CLI, §16 yanlışlanmış gece açıklaması **denetim notuyla birlikte** |
| `kapanis-ritueli.md` | 16,60 KB | ~6 KB | Neden önce okunur; üç soru; arşiv/terfi; kesin kimlik; kapanış yetkisi ve güncel eşik sınırı | Eski Durum B kararı, SessionEnd tasarım denemeleri, 16.09 PreCompact test kronolojisi, 17.09 tarih hatasının olay dökümü |
| `gece-derleyicisi.md` | 11,50 KB | ~5 KB | Güncel akış, görev koşulları, taslak yetkisi, hata görünürlüğü, yazma/silme sınırı | 18.09 üç ekleme ve eski testlerin ayrıntısı; değişmiş dedektör ve git iddiaları |

Bu üç notta yaklaşık **32,5 KB** yer değişir; kalıcı toplam yaklaşık
**96–97 KB** olur. Girişler ve bağlantılarla birlikte 100 KB altına sığması
beklenir; hedef garanti değil, uygulama sonunda yeniden ölçülür.

Hedef arşivler: `oturumlar/olcum-tarihcesi.md`,
`oturumlar/kapanis-tarihcesi.md`, `oturumlar/gece-derleyicisi-tarihcesi.md`.
Bunlar yeni konuşma kapanışı değildir; `kapanan-oturum:` taşımazlar.
Yanlış eski iddia, onu çürüten nottan koparılmaz. Kaynak işaretçileri ve
gerekçeler olduğu gibi korunur; kısa konu notundan tarihçeye, tarihçeden
konu notuna ve BEYIN haritasından ikisine bağ verilir.

## İkinci paket, yalnız gerekirse

İlk paket ölçümde 100 KB altına inmezse `agentic-yapi.md` içindeki
“Codex nasıl çağrıldı” ile eski pencere sayıları (~2 KB) tarihçeye adaydır.
`yasanan-hatalar.md` ve `kullanici-baglami.md` ilk pakette değişmez: güncel
dersleri veya kullanıcı tercihlerini boyut uğruna kısaltmak doğru değil.
`astra-denetim-bulgulari.md` de yeni doğruluk sınırlarını taşıdığı için kalır.

## Uygulama kabulü

Onaydan sonra önce mevcut commit sabitlenir. Taşınacak her bölüm için
kaynak/hedef/işaretçi listesi tutulur. Kaynak içerik, gerekçe ve karşı kanıt
arşivde korunur. Bağlar, kaynak işaretçileri ve kalan sıcak boyut tekrar
ölçülür; kuru derleme geçer. Paket ayrı commit olur. Kullanıcı bu paketi
onaylayana kadar yalnız bu plan yazılmıştır, hiçbir not taşınmamıştır.
