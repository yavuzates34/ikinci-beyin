# Toparlama ve sağlayıcıdan bağımsız ikinci beyin sunumu — 20 Eylül 2026

**Ara kayıt; çalışma sürüyor.** Aynı Codex oturumu: `01a0bc5c-f1c4`.
Bu, [[2026-09-20-astra-kontrol]] sonrasında kullanıcının verdiği ikinci iş
evresidir; önceki denetim kaydı kendi zaman aralığını korur.

> Merkez: [[BEYIN]] · Önceki ölçümler: [[astra-denetim-bulgulari]] ·
> İlgili: [[acik-uclar]] · [[ikinci-beyin-mimarisi]] · [[tasarim-dersleri]]

## İstek ve sıra

Kullanıcı aktif hedefte önce commit'lenmemiş onarımları anlamlı parçalarda
kaydetmeyi, sonra test kalıntılarını/test temizliğini ve kalıcı notların
bölme planını ele almayı istedi. Ardından 14 slaydın kaynağı yeniden
yazılacak: önce hangi sorunu çözdüğü ve neden böyle kurulduğu, sonra çalışma
biçimi. Tez: model/uygulama değişse de taşınan bilgi kalır. Yayındaki hesap
kopyasına müdahale yok. Silme/taşıma/budama/sistem ayarı için ayrıca onay.

## 06:06 — başlangıç ölçümü

- AGENTS ve BEYIN yeniden okundu; önceki denetim ve kalıcı bulgular açıldı.
- HEAD `065ef50`; önceki denetim değişiklikleri henüz commit'lenmemiş.
  32 takipli dosya değişmiş; ayrıca yeni kod, rapor ve ölçüm çıktıları var.
- Gerçek kalıntı **178 test klasörü ve 178 sahte BEYIN.md**: 745 dosya,
  352.943 bayt. `test-*` adıyla 185 girişin 7'si test sonuç dosyası,
  klasör değil. Silme önerisi yalnız 178 klasörü kapsayacak; 7 kanıt logu kalır.
- Önceki testleri depo dışında kendi geçici dizinine yönlendirerek yeniden
  çalıştırdım: **26/26 geçti**, geçici dizin temizlendi, kasadaki sahte BEYIN
  sayısı 178 olarak kaldı. Kuru derleme ve satır sonunu dikkate alan diff
  kontrolü de çalıştırıldı. Kuru çalışmanın uyarıları gece sonucu değildir.
- Satır sonu değişimleri diff'i gereksiz büyütüyordu. İçerik satırları aynı
  tutularak takipli dosyalarda mevcut depo biçimi korundu; sistem git ayarı
  değiştirilmedi.

## Commit'ler, temizlik, not planı ve sunum

### Geri dönüş noktaları

- `747e999`: arşiv kimliği, kurtarma, gece denetimi ve 26 regresyon testi.
- `938de04`: önceden onaylı gece görevi girişi ve geniş bağlam ayarı.
- `d0d12ac`: Astra raporu/kanıtları, kalıcı terfi, önceki sunum metin yamaları.
- `e20b165`: mevcut Obsidian zoom ve bağlam durumu; kullanıcı/uygulama
  değişikliği olduğu görünür kalsın diye ayrı commit.

### Test kirliliği ve silme engeli

Testler `TemporaryDirectory` + `addCleanup` kullanıyor; kasa dışındaki
yalnız kendi geçici klasörünü temizliyor. SetUp hatası ve assertion hatası
özel olarak sınandı. **28/28 başarılı**, kasa ve geçici alanda yeni kalıntı
0. Bu düzeltme, eski 178 klasörün silindiği anlamına gelmez.

Kullanıcı 20.09 06:12'de **178 test klasörünü sil** diye açık onay verdi.
178 yol/745 dosya için SHA-256 manifestosu çıkarıldı. Doğrulama ve silme
içeren PowerShell çağrısını otomatik onay denetimi `blocked by policy`
ile reddetti; ayrıntılı gerekçe yok. Silme gerçekleşmedi. Engeli dolaşacak
alternatif silme çağrısı yapılmadı. `araclar/temizle-astra-testleri.ps1`
hazırlandı; varsayılan salt doğrulama 178 hedefi doğruladı. `-Uygula`
seçeneği kullanıcının elle çalıştırabileceği aynı kapsamlı işlemdir.

### 17:24 — kalıcı katman planı

`rehber/kalici-katman-bakim-plani.md`: 128,5 KB → yaklaşık 96 KB hedefi.
Üç büyük notta güncel yöntem kalır, eski ölçüm/elenen tasarım/durum
tarihçesi kaynakları ve karşı kanıtlarıyla arşivde korunur. Hedef tahmin;
uygulama yapılmadı. Yeni dosyalara bölüp hepsini sıcak katmanda bırakmanın
toplam boyutu azaltmadığı açıklandı. Onay bekleyen ayrı bakım paketi.

### Sunum yaklaşımı

Kullanıcı yalnız mevcut HTML/deck kaynağını istediğinden çıktı aynı 14
HTML dosyası ve `deck.json` olarak kalacak. Presentations becerisinin
yazı/yerleşim/kanıt ve görsel denetim ilkeleri uygulandı; ayrı PPTX üretimi
kullanıcının istediği kaynak biçimini değiştireceği için kullanılmadı.
Yayınlanan claude.ai kopyasına erişim/yazma yapılmayacak.
