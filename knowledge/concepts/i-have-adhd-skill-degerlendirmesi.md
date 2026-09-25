---
kind: fact
visibility: internal
created_at: 2026-09-24
---
# I Have ADHD becerisi: araştırma ve çekirdek kararı

**24 Eylül kullanıcı açıklaması:** Yavuz aynı `ayghri/i-have-adhd` becerisini
kastediyordu. Becerinin, kendisini günlük/proje işlerinde aktif yönlendiren ve
işleri yaptıran bir hizmet olduğunu düşünüyordu; başka beceri aramamı
istemiyordu. Kaynak okuması bunun daha dar bir yanıt biçimi becerisi olduğunu
gösteriyor. Beklentisini kalıcı asistan davranışı veya otomasyon kurma talimatı
olarak kaydetme.

Yavuz 24 Eylül 2026'da bu beceriyi araştırmamı, işe yarayabileceği desteklenirse
İkinci Beyin'in çekirdeğine alma ihtimalini değerlendirmemi istedi. Bu bir
kurulum talebi değildir. Değerlendirilen özgün kaynak
[`ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd) deposu ve
[`SKILL.md`](https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md).
24 Eylül incelemesinde `main` commit'i `839872f9d1cd634fed642b4589ce7226199cc15f` idi.

## İşlev ve sınır

Beceri tıbbi tedavi değil, ajanın **yanıt biçimi** için yönergeler içerir:
önce eylemi söylemek, çok adımlı işi numaralandırmak, tek somut sonraki adımı
göstermek, konu dışına çıkmamak, durumu sonraki turda yeniden belirtmek,
ilerlemeyi görünür kılmak ve listeleri kısa tutmak. Kaynak ayrıca her yanıtın
eylemle başlamasını, her turda durum tekrarı, somut zaman tahmini ve kapanışta
bir sonraki adım gibi genel kurallar koyar; kullanıcı ve iş bağlamında aşırı
mekanikleşebilir. Beceri kendi metninde açıklama, belirsizlik ve görev biçimi
için istisnalar tanımlar. Dış beceri metni mevcut V3.2 talimatı değildir.
Bir sonraki insan adımını net göstermeye yardımcı olabilir; ancak kendi başına
görev kuyruğu, kalıcı takip, zamanlanmış yoklama veya sohbet dışında bildirim
sağlamaz. Bu son işlevler ayrıca hafıza/görev kaydı ve istenirse otomasyon ister.

## Olumlu kanıt ve sınırı

- Deponun [kendi değerlendirmesi](https://github.com/ayghri/i-have-adhd/blob/main/evals/RESULTS.md), 14 yapay senaryoda üçer tekrarın toplam 84 yanıtını, aynı model ailesinden kör bir hakemle karşılaştırmış. Ağırlıklı puan 4,045'ten 4,473'e; eyleme dönüklük 3,905'ten 4,619'a yükselmiş. Aday 14 senaryonun 10'unda kazanmış, ikisinde berabere, ikisinde geride kalmış. Bu, o testte **yanıt biçimi kalitesine** dair olumlu ama sınırlı bulgudur.
- Aynı sonuç raporunda yayın eşiği **başarısız**: adayda üç engelleyici bulgu kalmış. `partial-success` senaryosunda aday 0,63 puan gerilemiş; hakem, kanıt olmadan kesin neden ve çözüm söylemesini eleştirmiş. Yazarlar bunun sert “neden ve düzeltme” kuralıyla ilişkili olabileceğini, üç tekrarın kesin yargı için yetmediğini belirtiyor.
- Testler gerçek kullanıcıların gündelik işlerini ne kadar tamamladığını veya ADHD belirtilerini ölçmüyor. Bağımsız klinik değerlendirme ya da bu becerinin Yavuz için olumlu sonuç verdiğine dair veri bulgusu olarak okunamaz. Popülerlik bir etkililik ölçüsü değildir.
- [NHS yetişkin ADHD uyarlama önerileri](https://www.cnwl.nhs.uk/services/mental-health-services/cnwl-adult-adhd-service/adhd-reasonable-adjustments) yazılı ve yapılandırılmış adımlar, küçük parçalara ayırma, net eylem maddeleri ve hatırlatıcılar öneriyor. Bu, bazı tasarım ilkelerine dış dayanak sağlar; **bu GitHub becerisinin** sonuçlarını doğrulamaz.

## V3.2 için karar

Şimdilik özgün beceriyi çekirdeğe veya etkin `skills` klasörüne kopyalama.
Özellikle “her yanıtın başı eylem”, “her turda durum”, “daima süre tahmini” ve
“hata varsa nedeni kesin söyle” gibi katı kurallar sohbeti zorlama hâle
getirebilir ve kanıt kalitesini düşürebilir. Yavuz'un doğrudan tercihleri ile
mevcut sıcak ve somut çalışma biçimi önce gelir. Somut bir iletişim sürtünmesi
görüldüğünde küçük bir **Türkçe uyarlama pilotu** yapılabilir: gerektiğinde
önce sonuç/sonraki eylem, çok adımlı işte kısa numaralı adımlar, uzun işte
görünür ilerleme; teknik/kişisel açıklamayı kullanıcı istediğinde kısmamak.
Pilotun Yavuz'a gerçekten yardımcı olup olmadığı onun geri bildirimiyle
değerlendirilir. Bu karar kurulum yapıldığı veya otomatik davranış değiştiği
anlamına gelmez.

**Açıklanan sınır:** Bu becerinin tek başına “asistan beni gün boyu yönetsin ve
işleri yaptırsın” beklentisini karşılamadığı Yavuz'a açıkça anlatılmalı.
Sohbet içinde tek eylemle çalışma ayrıca tasarlanabilir; oturumlar arası görev
sürekliliği V3.2'nin tarihli kayıtlarına dayanır. Sohbet kapalıyken kendiliğinden
yoklama ancak ayrı bir otomasyonla olur. Yavuz bunların kurulmasını bu
konuşmada istemedi.
