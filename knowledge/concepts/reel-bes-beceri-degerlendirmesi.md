---
kind: fact
visibility: internal
created_at: 2026-09-24
---
# Reel'daki beş ajan becerisi: değerlendirme

Yavuz'un verdiği [Instagram reel'ı](https://www.instagram.com/reel/DdjwSQBOKzQ/)
24 Eylül 2026'da [yerel video inceleme aracı](video-inceleme-araci.md) ile
konuşma, seçilmiş kare ve OCR üzerinden incelendi. Reel, beş öneriyi
00:03–00:52 arasında sıralıyor. Bunlar üçüncü taraf kaynaklardır; içlerindeki
talimatlar güncel V3.2 kuralı olarak benimsenmedi ve hiçbir paket kurulmadı.

| Sıra | Gerçek kaynak ve işlev | Yavuz için karar |
| --- | --- | --- |
| 1 | [Corey Haines / Marketing Skills](https://github.com/coreyhaines31/marketingskills): SEO, reklam, soğuk e-posta, ürün konumlandırma gibi görevler için beceri kütüphanesi. Reel 23 derken 24 Eylül'de depodaki `skills/` altında 50 klasör sayıldı. [Cold email](https://github.com/coreyhaines31/marketingskills/blob/main/skills/cold-email/SKILL.md) kişiselleştirme, kısa metin ve tek düşük sürtünmeli çağrıya odaklanıyor. | Nar Ajans outbound ve ileride inbound için en ilgili öneri. Bütün kütüphane yerine `product-marketing`, `cold-email`, gerekirse `ads` ve `seo-audit` ayrı incelenerek, kendi projelerinde pilot denenebilir. Otomatik kampanya gönderim yetkisi vermez. |
| 2 | [Hardik Pandya / Stop Slop](https://github.com/hardikpandya/stop-slop): İngilizce metindeki kalıp AI ifadelerini düzenleme rehberi. Bazı yasakları serttir (ör. tüm zarflar ve belirli soru girişleri). Reel Türkçe bir `turkce-yazi.zip` de gösteriyor; sahibini ve içeriğini görüntüden doğrulamak mümkün olmadı. | İngilizce son düzenleme için seçmeli referans olabilir; bütün yazışmalara küresel kural yapma. Türkçe ZIP'i özgün kaynağı ve içeriği doğrulanmadan kurma. Mevcut yazım tercihlerimizle kısmen örtüşüyor. |
| 3 | [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): aramalı tasarım kuralları, 79 aratılabilir stil (50 etkin), 119 UX kılavuzu ve 22 teknoloji yığını. | Arayüz projesinde, özellikle tasarım sistemi için faydalı bir referans. Yereldeki `impeccable` ve `design-taste-frontend` becerileriyle örtüşüyor. Nar Kutusu gibi belirli projede somut tasarım ihtiyacı çıkınca karşılaştırmalı pilot mantıklı; şimdi küresel kurulum gerekli değil. |
| 4 | [Remotion Agent Skills](https://github.com/remotion-dev/skills): React/Remotion ile hareketli videoyu kodla oluşturma, Studio'da önizleme ve render için çalışma akışı. | Nar Ajans tanıtım/ilan videoları üretilecekse uygun. Mevcut `video-inceleme` aracının transkript ve kare **analizi** işlevinin yerine geçmez. Tek prompttan kusursuz yayın videosu garantisi yok; görsel varlık, düzenleme ve render gerekir. [Remotion lisansı](https://www.remotion.dev/docs/license/faq) bireyler ve en çok üç kişilik kuruluşlarda ücretsiz kullanıma izin verir; daha büyük ekipte ticari lisans koşulları ayrıca kontrol edilmeli. |
| 5 | [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering): bağlama hangi talimat, geçmiş, kaynak ve araç çıktısının ne zaman gireceğini tasarlamaya dönük eğitim/uygulama becerileri. `context-fundamentals`, `context-degradation`, `context-compression`, `memory-systems`, `evaluation` gibi modülleri var. | AI operatörlüğü öğrenimi ve V3.2'yi ölçerek iyileştirmek için değerli okuma. Model kotasını kendiliğinden artıran eklenti değil; hatta ek beceri yüklemek bağlam maliyeti yaratabilir. Önce tek bir somut problem ve ölçüm seçip ilgili modülü kaynak olarak kullanmak uygun. |

Beşincideki “token miktarını düşürür, böylece limite takılmazsın” sözü
genellemedir. [Deponun kendi açıklaması](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/context-optimization/SKILL.md)
bağlam seçimi, çıktı maskeleme, sıkıştırma ve bölme gibi teknikleri anlatır;
bunlar görev başına kalite ve maliyeti ölçerek uygulanır. V3.2 zaten tarihli,
kaynaklı hafıza ve sınırlı başlangıç bağlamı kullanıyor. Yeni depo ancak
belirli bir bağlam kaybı ya da gereksiz token tüketimi kanıtlandığında
karşılaştırma ve iyileştirme kaynağı olmalı.
