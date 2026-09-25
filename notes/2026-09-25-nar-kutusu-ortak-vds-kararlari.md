---
{
  "visibility": "internal",
  "project": "Instantly Alternatif Nar Kutusu",
  "kind": "fact"
}
---
# Nar Kutusu — 25 Eylül 2026 ortak VDS kararları ve Goal devri

## 03:24 — Goal uygulaması başladı, canlı gönderim kapalı

Yavuz güncel ortak VDS Goal planını “Başlayalım” diyerek başlattı. Root yalnız
orkestrasyon yapıyor; üç Luna max ajanı yerelde auth/roller, giriş arayüzü ve
Gmail adapter/worker üzerinde çalışıyor. Yerel Git deposu ve
[kanıt odaklı yürütme kaydı](../../../KODLAMA/Instantly%20Alternatif%20(Nar%20Kutusu)/docs/GOAL_EXECUTION_2026-09-25.md)
açıldı. VDS kurulumu, Google bağlantısı ve gerçek e-posta gönderimi henüz yok.

Opus'un mevcut Kasım ara dosyaları uygulamanın CSV sözleşmesine doğrudan uymuyor:
benzersiz e-posta CSV'sinde 836 satır/7 fuar, denetlenmiş firma CSV'sinde
780 satır/6 fuar var; Türkçe başlık ve satır bazlı fuar taşıyorlar. Bu ara
dosyalar Opus'un son teslimi sayılmaz. Kaynak: [yerel Opus ara paketi](../../Nar%20Ajans%20-%20Codex/Instantly/Kat%C4%B1l%C4%B1mc%C4%B1-listeleri/outputs/kasim2026/),
[mevcut içe alma kodu](../../../KODLAMA/Instantly%20Alternatif%20(Nar%20Kutusu)/backend/app/main.py).

Google'ın 3 Eylül 2026 güncellenen [Workspace API kullanıcı verisi politikası](https://developers.google.com/workspace/workspace-api-user-data-developer-policy)
Gmail scopes kullanan uygulamalar için istenmeyen ticari posta dağıtımını
uygun kullanım saymıyor; izinli toplu ticari postayı ayrı örneklendiriyor.
Opus alıcılarının ticari ileti izni Yavuz'a soruldu, yanıt bekleniyor. Bu yanıt
ve uygun taşıma kararı olmadan canlı cold Gmail gönderimi açılmayacak; yerel
uygulama geliştirmesi devam ediyor.

## Kullanıcının doğrudan kararları

- Nar Kutusu, Nar Ajans'ın Instantly yerine bütün cold mail süreçlerinde kullanacağı kendi uygulaması olacak. Yavuz, ek Vercel Pro, Neon veya benzeri sürekli ücretli abonelik istemiyor; mevcut AltunHost VDS'de Nar Kutusu'na yer ayırıp aynı sunucuyu ileride İkinci Beyin için de kullanmak istiyor. Bu 25 Eylül 02:44 kararı, 24 Eylül'deki VDS'yi boşta yedek tutma tercihini ve aynı günün Vercel önerisini bu proje açısından geçersiz kılar. Mevcut VDS ve Google Workspace ödemeleri devam ediyor; yeni abonelik açılmadı.
- Yavuz kurucu yönetici olacak: kullanıcı oluşturma, parola ve rol yönetimi dâhil daha geniş yetki. Derya yönetici olacak: kampanya/Unibox operasyonu ve olumlu müşteri yanıtlarını aynı sender hesabından Nar Kutusu içinde gerçek manuel yanıtlayacak. Derya 2022 MacBook kullanıyor.
- 20 sender tek Google Workspace yöneticisi altında. Yavuz Admin girişini kendisi yapmayı teklif etti; uygulama aşamasında önce salt okunur sender/domain envanteri çıkarılacak. Şifre sohbete veya kaynak dosyasına alınmayacak.
- Yavuz'a göre 20 sender Instantly'de sıcak; sender başına yaklaşık 10 warm-up + 30 cold/gün. Warm-up ek cold kapasite sayılmaz. Instantly warm-up hizmetinin Nar Kutusu'na taşındığı varsayılmaz.
- Reoon ilk aşamada zorunlu değil. Araştırma lead'leri kayıpsız tutulacak; doğrulanmamışlar SAFE diye yanlış etiketlenmeyecek. Önceki temas, opt-out, mükerrer ve bilinen bounce/invalid engelleri korunacak; bounce sorunu çıkarsa Reoon yeniden değerlendirilecek.
- Eski Instantly konuşmaları Derya'nın Nar Kutusu kutusuna taşınmayacak; yalnız Nar Kutusu dönemindeki yeni müşteri konuşmaları görünecek. Önceki temas/engel geçmişi ise yeniden iletişimi önlemek için alınacak.
- Gerçek cold gönderim için hem Opus'un fuar/katılımcı verisinin hem Nar Kutusu'nun hazır olması gerekiyor. Belirli kampanya/liste ayrıca incelenip onaylanacak. Yavuz bu kayıt tamamlandıktan sonra güncel Goal promptunu max eforda kendisi çalıştıracağını söyledi; bu notun yazılması Goal'ün başladığı anlamına gelmez.

## Planlanan teknik düzen ve sınır

- Kullanıcının daha önce paylaştığı AltunHost panel görüntüsü Ubuntu 24.04, 6.144 MB RAM ve 90 GB disk gösteriyor. Bu kapasite ekran görüntüsü bilgisidir; güncel CPU, boş RAM/disk, disk türü ve İkinci Beyin'in gelecek iş yükü henüz ölçülmedi.
- İlk aday: Nar Kutusu için ayrı Linux kullanıcısı ve web/worker servisleri; mevcut SQLite veri dosyası; Caddy ile HTTPS; İkinci Beyin için ileride ayrı kullanıcı, servis ve veri. Başlangıçta yazılım için ek abonelik hedeflenmiyor. SQLite yazma kapasitesi ve VDS kaynağı gerçek yükte ölçülecek; büyüme gerekirse aynı VDS'de PostgreSQL değerlendirilebilir.
- Aynı VDS içindeki ikinci kopya felaket yedeği değildir. Var olan yerel bilgisayar/depolama gibi VDS dışı şifreli yedek hedefi seçilip geri yükleme denenmeli. DNS/HTTPS ve Gmail bağlantısı canlı aşamada ayrıca kurulacak; Workspace MX kayıtları taşınmayacak.
- Mevcut uygulama yerelde fake modda. Giriş/roller, gerçek Gmail bağlantısı, işçi ve üretim güvenliği henüz bitmedi. VDS'ye bu plan turunda bağlanılmadı; önceki erişmeme talimatı sürüyor. Gerçek/test e-postası gönderilmedi.
- 25 Eylül 02:50'de Yavuz sunucu erişiminin olup olmadığını sordu; gerekirse IP, kullanıcı adı ve terminalde şifre girişi sağlayabileceğini belirtti. Bağlantı henüz denenmedi; şifre sohbet, not veya loga alınmadı. Goal başladığında ve erişim adımı gerektiğinde kimlik bilgisi gizli terminal istemi veya SSH anahtarı üzerinden kullanılacak.
- 25 Eylül 02:51'de Yavuz hemen erişim kontrolü istedi; önceki erişmeme talimatı bu kapsamda kaldırıldı. SSH parola istemine ulaşıldı, ancak Codex SSH oturumu kullanıcıya görünmediği için parola ayrı normal PowerShell istemine yanlışlıkla yazıldı. Parolanın kendisi buraya kaydedilmedi ve kullanılmayacak. Bekleyen SSH oturumu kapatıldı; yanlışlıkla girilen satır yerel PSReadLine kayıtlı geçmişinden kaldırıldı. Yavuz'a root parolasını AltunHost panelinden değiştirmesi söylendi. Ayrı Ed25519 anahtarı `C:\Users\Anj\.ssh\nar_kutusu_vds` konumunda hazırlandı; public key'in sunucuya eklenmesi bekleniyor. Sunucuda başarılı oturum veya değişiklik yok. Sonraki bağlantı yeni parolayı sohbet/tool komutuna almadan anahtarla denenir.
- 25 Eylül 02:59'da Yavuz public key ekleme komutunun sessizce tamamlandığını bildirdi. Ayrı Ed25519 anahtarıyla **salt okunur SSH oturumu başarıyla kuruldu**; `BatchMode=yes` ile parola kullanılmadı. Ölçüm: Ubuntu 24.04 LTS, 4 vCPU, 5.925 MB toplam/5.280 MB kullanılabilir RAM, kök disk 89 GB toplam/80 GB boş (%7 dolu). `ss -ltn` yalnız SSH :22'yi dış dinleyici olarak gösterdi; uygulama servisi görünmüyor. Bu yalnız 25 Eylül 02:59 anlık ölçümü, İkinci Beyin'in gelecek yükü hâlâ bilinmiyor. Public key'i kullanıcı `authorized_keys` içine ekledi; benim SSH ölçümüm dosya yazmadı veya servis ayarı yapmadı. Güncel [ortak VDS Goal planı](../../../KODLAMA/Instantly%20Alternatif%20(Nar%20Kutusu)/docs/ORTAK_VDS_GOAL_PLANI_2026-09-25.md) erişim doğrulamasına göre güncellendi.

## Kaynaklar ve sonraki adım

- Kullanıcının 25 Eylül 2026 doğrudan mesajları ve 23 Eylül AltunHost panel görseli.
- [Güncel ortak VDS ve Goal planı](../../../KODLAMA/Instantly%20Alternatif%20(Nar%20Kutusu)/docs/ORTAK_VDS_GOAL_PLANI_2026-09-25.md); [Nar Kutusu proje hafızası](../../../KODLAMA/Instantly%20Alternatif%20(Nar%20Kutusu)/PROJECT_MEMORY.md); [yerel API sözleşmesi](../../../KODLAMA/Instantly%20Alternatif%20(Nar%20Kutusu)/docs/API_CONTRACT.md).
- Sonraki adım: İlk ajan dalgasının yerel kabulünü ve lead içe alma uyarlamasını tamamla; sonra kontrollü VDS/HTTPS/yedek kurulumu. Sunucu dışı yedek hedefi ve alıcı izin durumu yanıtları bekleniyor. Opus verisi ve uygulama hazır olmadan gerçek cold gönderim yapılmaz.
