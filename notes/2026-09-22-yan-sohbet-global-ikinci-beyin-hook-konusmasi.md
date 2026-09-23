# Yan sohbet dökümü — Global İkinci Beyin hook/plugin tasarımı

Tarih: 2026-09-22  
Kapsam: Yan sohbet sınırından sonra kullanıcı ile asistan arasında görünen mesajlar. Sistem/geliştirici talimatları, araç çağrıları ve ham araç çıktıları bu döküme dahil edilmemiştir.

---

## 1. Kullanıcı

### Seçilen metin

> Ardından İkinci Beyin hook’unu CLI’dan güvenilir hâle getirip, başka projelerde de çalışması için global plugin/hook biçimine taşımalıyız. Bu, senin beklediğin “kod projede; kararların özeti hem projede hem İkinci Beyin’de” davranışını gerçekten kurar.

### İstek

Burada kastettiğin şeyi tam anlayamadım. Bana konuyu bilmeyen bir yabancıymışım gibi basit bir şekilde anlatmaya çalışsana.

## 2. Asistan — Ara güncelleme

Bunu basit bir “iki ayrı defter ve otomatik kurye” benzetmesiyle anlatacağım. Güncel Codex davranışını yanlış aktarmamak için `openai-docs` becerisini kullanıyorum; hiçbir ayarı veya dosyayı değiştirmeyeceğim.

## 3. Asistan — Yanıt

En basit hâliyle iki ayrı oda düşün:

- **Kodlama odası:** `D:\KODLAMA\codex-dynamic-usage-bar`
- **İkinci Beyin odası:** `D:\AI\ikinci-beyin-v3.2`

Şu anda bu iki oda birbirinden ayrı. Kodlama odasında proje dosyaları var; İkinci Beyin odasında ise senin genel hafızan var.

### `AGENTS.md` ne yapar?

`AGENTS.md`, bir odanın duvarına asılmış çalışma talimatıdır:

> “Bu projeye girince önce `PRODUCT.md` ve `DEVELOPMENT.md` dosyalarını oku. Önemli kararları kaydet. Testleri çalıştır.”

Codex o projede yeni bir görev açıldığında bu talimatı otomatik okur. Ancak bu talimat yalnızca bulunduğu proje için geçerlidir. [OpenAI Docs – AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

### Hook ne yapar?

Hook ise kapıdaki otomatik sensör gibidir:

- Yeni görev açıldı → çalışır.
- Yeni mesaj gönderildi → çalışır.
- Context sıkıştırıldı → çalışır.
- Oturum kapandı → çalışır.

Modelin “bunu yapmayı hatırlaması” gerekmez; olay gerçekleşince hook otomatik tetiklenir.

Fakat şu anda İkinci Beyin hook’u yalnızca **İkinci Beyin klasörünün kapısında** bulunuyor. Sen `D:\KODLAMA` projesine geçtiğinde oradaki kapıda bu sensör yok. Codex proje hook’larını proje klasöründen, global hook’ları ise kullanıcı düzeyindeki Codex klasöründen yükler. [OpenAI Docs – Hooks](https://learn.chatgpt.com/docs/hooks)

### “Global plugin/hook” ne demek?

Sensörü tek bir odanın kapısından çıkarıp binanın ana girişine koymak demek.

Böylece hangi projeye girersen gir:

1. Codex aktif projenin hangisi olduğunu görür.
2. İkinci Beyin’den o projeyle ilgili özeti getirir.
3. Model “Bu projenin amacı neydi, hangi kararlar alınmıştı?” bilgisini alır.
4. İş bittiğinde önemli sonuçların İkinci Beyin’e kaydedilmesi kontrol edilir.

Örneğin kullanım barı projesini açtığında:

```text
Kod dosyaları
D:\KODLAMA\codex-dynamic-usage-bar
        │
        ├── PRODUCT.md
        ├── DEVELOPMENT.md
        └── kaynak kodları

Proje özeti ve geçmiş kararlar
D:\AI\ikinci-beyin-v3.2
        │
        └── kullanım barının amacı, kararları ve kaldığımız yer
```

Kod İkinci Beyin’e taşınmaz. İkinci Beyin’e yalnızca şöyle bir özet gider:

> “Aktif hesap değişince eski kota sıfırlanacak. Bu yaklaşım, yanlış hesabın değerini göstermemek için seçildi. Sonraki adım canlı hesap geçişini test etmek.”

### Neden hem `AGENTS.md` hem global plugin?

Çünkü görevleri farklı:

- **`AGENTS.md`:** Modele o projede nasıl çalışacağını söyler.
- **Proje Markdown dosyaları:** Projenin teknik bilgisini saklar.
- **Global hook/plugin:** Hangi projede olursan ol İkinci Beyin bağlantısını otomatik çalıştırır.
- **İkinci Beyin:** Projeler arasında taşınabilecek üst düzey hafızayı saklar.

Plugin, hook ve gerekli hafıza talimatlarını tek paket hâlinde taşımak için daha düzenli bir yöntemdir. “Global” olması da Codex’te açtığın bütün yerel projelerde kullanılabilmesi demektir.

Kısacası: **Her proje kendi ayrıntılı defterini tutar; İkinci Beyin bütün projelerin kısa özetlerini tutar; global plugin de ikisi arasında çalışan otomatik kurye olur.** Şu anda kurye yalnız İkinci Beyin odasında çalışıyor; amaç onu bütün projelerde çalışır hâle getirmek.

---

## 4. Kullanıcı

### Yanıt içinden seçilen metin

> Böylece hangi projeye girersen gir: Codex aktif projenin hangisi olduğunu görür. İkinci Beyin’den o projeyle ilgili özeti getirir.

### Kullanıcı açıklaması

Şimdi biz bu bar kodlama klasörünü projesini yine bu ikinci beyin içerisinde oluşturduk. Ben ikinci beyin içerisinde modele dedim ki bu d: diskinde kodlama dizininin altına bu son kullanım kota ve kontekst barını gösteren bir bar kodlamak için proje dosyası klasör oluştur dedim. O da oluşturdu. Dolayısıyla nerede ne oluşturduğunun bilgisini biliyordu ve o projeden haberdar olabilecek bir şekilde o proje içerisine gerekli Markdown dosyalarını ekleyerek talimatlar ekleyerek oluşturdu. Sen şimdi şunu mu söylüyorsun? Sen artık bu ikinci beyin içerisinde şurada şu klasörü oluşturup şu projeyi oluştur demene gerek yok. Bilgisayarında nerede hangi klasörü oluşturursan oluştur, senin ikinci beyinin o projeye artık vakıf olacak. O projeden haberdar olacak mı diyorsun?

## 5. Asistan — Ara güncelleme

Evet, tam olarak sorduğun ayrımı netleştireceğim: “klasörün varlığından otomatik haberdar olmak” ile “o proje hakkında İkinci Beyin’de kayıt bulunduğunda onu otomatik getirmek” aynı şey değil. Güncel Codex proje erişim sınırını `openai-docs` ile doğrulayıp basitçe anlatacağım; herhangi bir değişiklik yapmayacağım.

## 6. Asistan — Yanıt

Evet, kastettiğim hedef buna yakın; ama önemli bir sınır var: **İkinci Beyin bilgisayardaki bütün klasörleri kendiliğinden tarayıp öğrenmeyecek.**

Şöyle düşün:

### Şu anda olan

Kullanım barı projesini bu İkinci Beyin oturumunda oluşturdun:

> “`D:\KODLAMA` altında böyle bir proje oluştur.”

Bu konuşma projeyi bildiği için:

- Klasörü oluşturdu.
- Amacını biliyordu.
- `PRODUCT.md` ve `DEVELOPMENT.md` dosyalarına bilgileri yazdı.
- İkinci Beyin’e de projenin özetini kaydetti.

Yani bağlantıyı sen İkinci Beyin içerisinden başlattığın için iki taraf birbirinden haberdar oldu.

### Global sistem kurulursa ne değişir?

Artık projeyi mutlaka İkinci Beyin sohbetinden başlatman gerekmez.

Örneğin sen kendi başına:

```text
D:\Denemeler\yeni-muhasebe-uygulamasi
```

klasörünü oluşturabilirsin. Ancak İkinci Beyin o anda bunu sihirli biçimde öğrenmez.

Sonra bu klasörü Codex’te proje olarak açtığında global sistem şunu görür:

> “Şu anda `D:\Denemeler\yeni-muhasebe-uygulamasi` projesindeyiz.”

Eğer İkinci Beyin’de bu proje için kayıt yoksa:

1. Projenin klasörünü ve adını belirler.
2. Mevcut `README`, `AGENTS.md` ve proje belgelerinden amacını öğrenir.
3. Gerekirse sana “Bu projenin amacı nedir?” diye sorar.
4. İkinci Beyin’de bu proje için ilk kaydı oluşturur.
5. Bundan sonraki oturumlarda ilgili özeti otomatik getirir.

Codex yalnızca açtığın veya projeye eklediğin klasörlere erişir; bilgisayarındaki bütün klasörleri kendiliğinden keşfetmez. [OpenAI Docs – Projects and chats](https://learn.chatgpt.com/docs/projects?surface=app)

Kısaca:

- **Klasörü oluşturup hiç Codex’te açmazsan:** İkinci Beyin haberdar olmaz.
- **Klasörü Codex’te proje olarak açarsan:** Global sistem projeyi tanıyıp İkinci Beyin’e kaydedebilir.
- **Projeyi doğrudan İkinci Beyin içinden oluşturursan:** Şimdiki kullanım barı örneğinde olduğu gibi baştan bağlantılı oluşur.
- **Daha sonra tekrar açarsan:** Önceki amaç, kararlar ve kaldığın yer geri getirilebilir.

Bir de çok önemli düzeltme: Bu anlattığım şey **şu anda tamamen kurulmuş durumda değil**. Önceki cümlem hedeflediğimiz mimariyi anlatıyordu. Şu an kullanım barı projesinden haberdar olmamızın sebebi onu bu oturumda birlikte oluşturmuş olmamız. Global plugin/hook kurulursa, aynı bağlantıyı başka projeler için de elle İkinci Beyin’den başlatmadan kurabiliriz.

En kısa ifadeyle:

> İkinci Beyin bütün bilgisayarı izlemez. Fakat global bağlantı kurulduktan sonra Codex’te açtığın her projeyle tanışabilir, onu kaydedebilir ve daha sonraki oturumlarda hatırlayabilir.

---

## 7. Kullanıcı

### Yanıt içinden seçilen metin

> Klasörü Codex’te proje olarak açarsan: Global sistem projeyi tanıyıp İkinci Beyin’e kaydedebilir.

### Kullanıcı açıklaması

Kaydedebilir misin? Nasıl yani? Bunu bir ihtimal olarak mı söylüyorsun, yoksa yanlış bir ifade mi kullandın? Çünkü eğer bu bir global hook olacaksa, hook olacaksa deterministik olmasını beklerim. Yani ben herhangi bir klasör açıp oluşturup Codex arayüzünde de o klasörü bir proje olarak seçip orada işlememi yapmaya başladığım zaman global hook sistemi gerekli Markdown dosyalarını oluşturup ikinci beyinde de gerekli kayıtları açıp iki vault'un hem ikinci beynin hem de o yeni kodlama klasörünün birbirinden haberdar olmasını sağlamasını beklerim.

## 8. Asistan — Ara güncelleme

“Kaydedebilir” ifadem belirsizdi; burada iki farklı şeyi ayırmam gerekiyordu: projenin mekanik olarak kaydedilmesi ve projenin anlamının doğru biçimde özetlenmesi. `openai-docs` ile hook’un hangi olayı deterministik yakalayabildiğini doğrulayıp beklentinin hangi kısmını kesin garantiye çevirebileceğimizi anlatacağım; hiçbir değişiklik yapmayacağım.

## 9. Asistan — Yanıt

Evet, senin beklentin doğru. “Kaydedebilir” derken yanlış derecede ihtimalli konuştum. Kuracağımız sistemin davranışı şöyle olmalı:

> Güvenilmiş global hook etkinse, Codex’te açılan her yerel projeyi deterministik olarak kaydeder. Başarısız olursa sessizce geçmez; hata bildirir.

### Proje ilk defa açıldığında

Codex `SessionStart` olayını tetikler. Hook’a projenin çalışma dizini `cwd` olarak verilir. [OpenAI Docs – Hooks](https://learn.chatgpt.com/docs/hooks)

Global hook sırasıyla şunları yapar:

1. Açılan klasörün daha önce kaydedilip kaydedilmediğine bakar.
2. Kayıtlı değilse projeye sabit bir kimlik verir.
3. Proje klasöründe güvenli hafıza dosyalarını oluşturur; mevcut dosyaları ezmez.
4. İkinci Beyin’de aynı kimlikle karşılık gelen proje kaydını oluşturur.
5. İki tarafa birbirlerinin bağlantısını yazar.
6. Mevcut README veya proje belgelerinden çıkarılabilen başlangıç bilgisini kaydeder.
7. İkinci Beyin’den gelen ilgili özeti mevcut Codex oturumuna ekler.

Örneğin:

```text
D:\KODLAMA\yeni-proje
│
├── AGENTS.md
├── PROJECT_MEMORY.md
└── .codex\second-brain-project.json
```

Kimlik dosyası şöyle bir bağlantı taşıyabilir:

```text
project_id: proje-7f31...
brain_record: projects/proje-7f31.md
```

İkinci Beyin tarafındaki kayıt da ters bağlantıyı taşır:

```text
project_id: proje-7f31...
project_path: D:\KODLAMA\yeni-proje
project_memory: D:\KODLAMA\yeni-proje\PROJECT_MEMORY.md
```

Böylece klasör ile İkinci Beyin birbirlerini gerçekten tanır.

### Her oturumun sonunda

Sistem şunları denetler:

- Yeni bir karar alındı mı?
- Projenin durumu değişti mi?
- Açık kalan bir sonraki adım var mı?
- Proje hafızası ve İkinci Beyin özeti güncellendi mi?

Eksikse hook bunu tespit edip kayıtsız şekilde kapanmasına izin vermeyecek veya açık bir hata/eksik-receipt kaydı oluşturacak biçimde tasarlanabilir.

### Deterministik olan ve olmayan kısım

Deterministik olarak garanti edebileceğimiz şeyler:

- Hook’un her proje açılışında çalışması.
- Projeyi algılaması.
- Kimlik ve Markdown dosyalarını oluşturması.
- İkinci Beyin kaydını oluşturması.
- İki tarafı birbirine bağlaması.
- Mevcut proje özetini oturuma yüklemesi.
- Oturum sonunda kayıt bulunup bulunmadığını kontrol etmesi.
- Hataları sessizce yutmaması.

Modelin yorumuna ihtiyaç duyan şey ise şudur:

> “Bu konuşmada alınan asıl önemli karar neydi?”

Çünkü bir kararın anlamını yalnız mekanik bir script belirleyemez. Ancak bunu da başıboş bırakmayız: modele yapılandırılmış bir sonuç kaydı hazırlatır, hook’a da bu kaydın oluşturulup oluşturulmadığını ve gerekli alanları taşıyıp taşımadığını doğrulatırız.

Yani:

```text
Model: Kararın anlamını yazar.
Hook: Yazının gerçekten oluşturulduğunu, doğru projeye bağlı olduğunu
      ve zorunlu alanlarının bulunduğunu denetler.
```

Özetle senin tarifin hedef davranış açısından doğru:

> Codex’te herhangi bir klasörü proje olarak açtığında global sistem o projeyi otomatik kaydedecek, gerekli proje hafızasını oluşturacak, İkinci Beyin’de karşılık açacak ve iki tarafı birbirine bağlayacak.

Bu şu anda kurulmuş mevcut davranış değil; oluşturmayı konuştuğumuz global sistemin kesin gereksinimi olmalı. Burada “yapabilir” değil, **“çalışır durumdaysa yapar; yapamazsa açıkça hata verir”** demek daha doğru.

---

## 10. Kullanıcı

### Yanıt içinden seçilen metin

> Codex’te herhangi bir klasörü proje olarak açtığında global sistem o projeyi otomatik kaydedecek, gerekli proje hafızasını oluşturacak, İkinci Beyin’de karşılık açacak ve iki tarafı birbirine bağlayacak.

### Kullanıcı açıklaması

Tamam şu an bu haliyle on numara gözüküyor, yapalım. Fakat şu an side chatteyiz, yan sohbetteyiz. Yapabiliyor muyuz buradan? Yoksa ana oturuma mı bir prompt yazmamız gerekiyor?

## 11. Asistan — Ara güncelleme

Bunu burada uygulamaya başlamayacağım; global hook/plugin kurulumu geniş kapsamlı ve kalıcı bir sistem değişikliği olduğu için ana oturumda yürütmek doğru. `openai-docs` ile yalnızca görev/yan sohbet sınırını doğrulayıp sana ana oturuma göndereceğin hazır promptu vereceğim.

## 12. Asistan — Yanıt

Bu iş için **ana oturuma dönmemiz gerekiyor**.

Yan sohbet teknik olarak bazı dosyalara erişebilse de amacı açıklama ve hafif incelemedir. Global hook/plugin kurulumu ise:

- Codex’in kullanıcı düzeyi yapılandırmasını değiştirir.
- Bütün projeleri etkiler.
- İkinci Beyin kaynaklarını günceller.
- Güven onayı ve kontrollü test gerektirir.

Bu nedenle burada başlatmak ana oturumdaki çalışma durumuyla çakışabilir.

Ana oturuma şu promptu gönderebilirsin:

> Konuştuğumuz deterministik global İkinci Beyin bağlantısını şimdi uygulayalım. Codex’te açtığım herhangi bir yerel projede global `SessionStart` hook’u çalışma dizinini algılasın. Yeni projeyse mevcut dosyaları ezmeden sabit bir `project_id`, proje tarafında güvenli hafıza/bağlantı dosyaları ve İkinci Beyin’de karşılık gelen proje kaydı oluştursun; iki taraf birbirine kaynak bağlantılarıyla bağlansın. Mevcut projeyse İkinci Beyin’den ilgili özeti oturuma yüklesin. Compaction sonrasında bağlamı tekrar yüklesin. Anlamlı çalışma sonunda yapılandırılmış receipt ve proje hafızası bulunmasını doğrulasın; başarısızlıkları sessizce geçmesin. Bunu kullanıcı düzeyi kişisel plugin/global hook olarak tasarla. Mevcut İkinci Beyin V3 dosyalarını, hook’larını ve skill’lerini önce incele; işlevleri kopyalayan ikinci bir sistem kurma. Mevcut dosyaları ezme. Hook güvenini bypass etme; tanımları inceleyip normal güven akışını kullan. Sonunda yeni, zararsız bir deneme projesiyle başlangıç, proje kaydı, oturum sonu receipt ve compaction sonrası geri yükleme davranışlarını doğrula.

Bu prompt, ana oturumun hem mevcut araştırmayı kullanmasını hem de doğrudan uygulama ve test aşamasına geçmesini sağlar.

---

## 13. Kullanıcı

Sen direkt bu yan sohbette konuştuğumuz her şeyi, kendi cevaplarını, benim promptlarımı içeren bir Markdown dosyası oluştursana.

## 14. Asistan — İşlem sonucu

Yan sohbet dökümü oluşturuldu ve İkinci Beyin içinde kaynak olarak kaydedildi.
