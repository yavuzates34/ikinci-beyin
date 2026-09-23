---
{
  "kind": "fact",
  "project": "Instantly Alternatif Nar Kutusu",
  "visibility": "internal"
}
---
# Instantly ödeme gecikmesi ve Nar Kutusu geçişi

Tarih: 2026-09-23. Proje: Instantly Alternatif (Nar Kutusu).

## Kullanıcının doğrudan beyanı

- Yavuz normalde Instantly ödemelerini ayın 10'unda yapıyor; Eylül 2026 ödemesini 23 Eylül itibarıyla yapmadığını ve yaklaşık 13 gündür ödeme yapmadığını söyledi. Fatura vadesi ve hesap durumu bağımsız olarak doğrulanmadı.
- Nar Kutusu hedefi: sender hesaplarını kendi uygulamasından yönetmek, lead'lere oradan e-posta göndermek, lead yanıtlarını Nar Kutusu gelen kutusunda görmek. Bu bir hedef beyanıdır; özelliklerin uygulanmış olduğu anlamına gelmez.

## 23 Eylül 2026 resmî kaynak araştırması

- Instantly Hizmet Koşulları §5.1(c): yenileme ödemesi alınmazsa aboneliği askıya alabilir veya sonlandırabilir ve ödemeyi yeniden tahsil etmeyi deneyebilir. §5.6: ücretler 30 günden fazla gecikmişse yazılı bildirimle erişimi derhal askıya alma hakkı saklıdır. 30 günlük madde, erişimin ilk 30 gün garanti edildiğini söylemez. Kaynak: https://instantly.ai/terms
- Yardım merkezi, başarısız yenileme ödemesini sistemin tekrar denediğini; fatura durumunun Billing and Usage → Payment and Invoices → Manage bölümünden kontrol edilebildiğini söylüyor. Kaynak: https://help.instantly.ai/en/articles/13559163-understanding-your-billing-charges
- Plan sona ererse dashboard erişimi kaybolabilir; email hesapları, warmup ve kampanyalar durur. Süre bitiminden sonra dışa aktarım için yeniden abonelik gerekebilir. Kaynak: https://help.instantly.ai/en/articles/7918821-access-your-expired-instantly-account

## Çıkarım ve belirsizlik

- Kullanıcının belirttiği 10 Eylül ödeme gününden 30 gün sonrası yaklaşık 10 Ekim'dir; bu, 10 Ekim'e kadar erişim garantisi veya hesap özelinde kapanış tarihi değildir. Güvenle planlanabilecek ek süre belirlenemedi.
- Instantly API'sinin ödeme/abonelik sonrasında çalışacağı doğrulanmadı; Nar Kutusu geçiş planı API erişiminin sürekli kalacağını varsaymamalı.
- Hesap özelindeki fatura/abonelik ekranı otomatik incelemede doğrulanamadı; bilgisayar erişim aracı tarayıcı URL'sini güvenle saptayamadığı için durdu. Bu turda ödeme, ayar veya hesap değişikliği yapılmadı.

## Açık adım

- Instantly'deki doğru workspace için fatura ve abonelik durumunu salt okunur doğrula; kritik lead, sender ve yanıt verilerini erişim varken dışa aktarılabilirlik açısından incele. Nar Kutusu'nun gerçek gönderim/gelen kutusu mimarisini mevcut Instantly bağımlılıklarına göre ayrıca planla.

