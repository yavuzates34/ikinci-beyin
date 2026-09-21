# Astra — Y2: iyimser kilit (hoca turu)

> Çağıran oturum: claude `96517e26` · 21.09.2026 20:36
> Önceki iş: [[astra-y1-kuyruk]] — Y1'in üç turu.

## Bu tur farklı: seni hoca olarak çağırıyorum

Y1'de sana hep bitmiş bir şey götürüp "kır" dedim. Kullanıcı haklı olarak
sordu: hocadan yararlanmanın asıl yolu, tasarlamadan **önce** sormaktır. Bu tur
o. **Kod yazma, tasarımımı da bekleme** — çünkü henüz yok. Senden yaklaşım
istiyorum: nasıl yapardın, önce neyi ölçerdin, nereye düşmezdin. Sonra ben lab'de
kurarım, sen kırarsın.

Yeni çalışma sözleşmesi (kullanıcı onayı, 21.09 20:34): önce hoca, sonra
denetçi · deney **lab'de** · yerel hook'lara dokunmadan önce kullanıcıya sorulur.

## Elimdeki ölçüm

`notlar/olculmus-bulgular.md` §22 (kasada, okuyabilirsin):

- **11 çapraz çakışma penceresi** (Claude ↔ Codex), en uzunu **13,5 saat**.
- **İkisinin de yazdığı 48 dosya**; en sıcakları `BEYIN.md` (28/8) ve
  `notlar/acik-uclar.md` (23/6).
- **Koruma kazara.** Dize değiştiren düzenleme (`Edit`) hedef metin değiştiyse
  başarısız olur — iyimser kilidin işini tesadüfen yapar. Bütün dosyayı yazan
  yol (`Write`, ya da `read_text()` → `write_text()`) sormadan ezer. Ben bu
  oturumda o deseni defalarca kullandım.
- **Geriye dönük ölçülemez.** Kaybolan yazma iz bırakmaz; git yalnız
  commit'lenmiş hâlleri görür.

## Avenox'un karşılığı

`~/lab/vault/.claude/scripts/beyin_v3.py:245–271` (lab'de, `ssh lab` →
`sudo -u avenox`): `update_task(id, expected_revision, changes)`, sqlite
`BEGIN IMMEDIATE`, bayat revizyonda `RevisionConflict: reread source`, ve
append-only `events` tablosu. Onlarınki bir **veritabanı kaydı**; bizimki
**LLM ajanlarının düzenlediği Markdown notlar**.

## Sorularım

1. **Doğru araç mı?** Markdown notları düzenleyen iki LLM ajanı için iyimser
   kilit doğru soyutlama mı? Yoksa **git kendisi** doğal revizyon sistemimiz
   mi — örneğin yazmadan önce "okuduğum commit hâlâ HEAD mi" kontrolü? Başka
   bir şey mi görüyorsun?
2. **Önce ne ölçülmeli?** "Kayıp güncelleme gerçekten oluyor mu" sorusunu
   ileriye dönük, lab'de, nasıl ölçerdin? Deneyin kaba hatlarını ver: kaç ajan,
   hangi yazma yolları, neye bakılır, ne sonuç "port gereksiz" der.
3. **En küçük mekanizma.** Kazara korumayı tasarlanmış korumaya çeviren en
   küçük şey ne olurdu? Hangi katmanda durmalı — aracın içinde, bir hook'ta,
   git'te, ajan talimatında?
4. **Ne yapmazdın?** Y1'de iki kez aynı tuzağa düştüm: gözlemlediğim şey ile
   umursadığım şey arasındaki katmanı kaçırdım (flush ≠ teslim; alt dize ≠ iş
   yapıldı). Y2'de bunun karşılığı ne olur? Hangi ölçüt yanlış güven verir?

Keşif serbest: kasayı okuyabilir, lab'e bakabilir, küçük deney koşabilirsin.
Kasaya **yazma, silme, commit yasak.**

## Rapor biçimi

Bu tur hüküm değil öneri istiyor, o yüzden serbest yaz. Yalnız şunu ayır:
**ölçtüğün** şey ile **önerdiğin** şeyi karıştırma — Y1'de en çok bu ayrım işe
yaradı. Sonunda: önerdiğin deney, üç-beş madde.

---

> Aşağıdaki metin Astra'nın raporudur, değiştirilmeden alındı. Göreli bağlantıları (log, json) onun çalışma dizinindedir ve kasaya taşınmadı; o dizin geçicidir. Karar ve ölçümlerin kalıcı özeti: [[olculmus-bulgular]] §25.

## Astra'nın cevabı (21.09 22:10)

21.09.2026, 22:10 (Europe/Istanbul). **Önerim: dosyanın okunan sürümüne bağlı koşullu yazma; karşılaştırma ile dosyayı değiştirme, bütün yazıcıların geçtiği tek kısa kritik bölümde yapılmalı.** Git geçmiş ve birleştirme için yararlı; paylaşılan çalışma dizininde yalnız HEAD kontrolü bu sözleşmeyi sağlamaz. İlk iş algoritma seçmekten önce gerçek yazma yollarını çıkarmaktır.

**Bu turda ne incelendi, ne ölçülmedi?** Y2 brief'i, `notlar/olculmus-bulgular.md:787` ile başlayan §22, `araclar/dosya_kilidi.py` ve ilgili yerel yazıcılar okundu. §22'nin 11 çapraz pencere / 48 ortak dosya sayılarını yeniden hesaplamadım. Oturum pencerelerinin kesişmesi aynı anda yazma demek değildir; commit'leri `Co-Authored-By` varlığıyla ayırmak da kusursuz ajan kimliklendirmesi değildir. Bunlar deney önceliği veren maruziyet göstergeleridir, kayıp güncelleme sayacı değildir.

Y2 için kod yazılmadı ve yarış deneyi çalıştırılmadı. `ssh lab` takma adı bu yürütme hesabında çözülemedi; kullanıcı yapılandırması açıkça verilince `C:/Users/Anj/.ssh/config` için izin hatası geldi ([ilk deneme](y2-lab-kaynak-okuma.log), [yapılandırmalı deneme](y2-lab-kaynak-okuma-acik-config.log)). Dolayısıyla Avenox'un lab kaynağını bu tur bağımsız doğrulamadım; aşağıdaki Avenox bağlantısı brief'in tarifine dayanıyor. Kasa ve yerel hook'lar değiştirilmedi. Aşağıdaki deney sonuçları **beklenen kabul koşullarıdır**, elde edilmiş ölçümler değildir.

**1. Doğru araç mı?**

Evet, “bu değişiklik, okuduğum sürüm hâlâ geçerliyse uygulansın” doğru sözleşme. LLM uzun süre düşünebilir; dosyayı bu sürenin tamamında kilitlemek yerine yalnız son uygulama anında kısa kilit alınır. Bu yüzden iyimser sürüm denetimi ile kısa süreli karşılıklı dışlama birbirinin alternatifi değildir: biri bayat taslağı reddeder, diğeri kontrol–yazma yarışını kapatır.

İlk sürüm için hedef dosyanın **okunan aynı baytlarından** üretilmiş içerik hash'i yeterli bir başlangıçtır. Token kanonik dosya yoluna ve dosyanın var/yok durumuna bağlı olmalı. Ajanın gördüğü içerik bir okumadan, hash başka okumadan gelmemeli. mtime, boyut veya dosya adına güvenmem. İçerik A→B→A olursa hash aynı çıkar; yalnız mevcut içeriğe bağlı düzenleme için bu kabul edilebilir. Aradaki her olayı ayırt etmek gerekiyorsa tek yazıcının yönettiği artan sürüm gerekir. Ayrı, bağımsız güncellenen bir `.rev` dosyası yeni tutarsızlık penceresi açar.

**HEAD önerisinin karşı örneği:** A ve B aynı commit'teyken aynı notu okur; A commit yapmadan yazar; B eski taslağıyla dosyayı ezer. HEAD bütün akışta aynı kalabilir. Ters yönde, ilgisiz bir dosyanın commit'i HEAD'i değiştirip gereksiz ret yaratabilir. Git çalışma ağacının commit edilmemiş değişiklikleri de içerdiği resmî belgede açıkça ayrılır; bu karşı örnek o ayrımdan yaptığım çıkarımdır. [Git kullanıcı kılavuzu](https://git-scm.com/docs/user-manual)

Git'i güvenilir alternatif yapan şey **ajan başına ayrı worktree/branch ve ortak sonuca tek, sıralı entegrasyon yolu** olur. Böylece ajanlar aynı dosya kopyasını doğrudan ezmez; entegrasyon güncel tabana karşı yapılır. Ortak kasa üzerinde iki branch adı kullanmak aynı izolasyonu sağlamaz. Worktree ayrı çalışma alanı sağlar; anlamsal çelişkileri kendiliğinden çözmez. [Git worktree belgesi](https://git-scm.com/docs/git-worktree)

Brief'teki Avenox yaklaşımından taşınacak ilke, `expected_revision` kontrolü ile değişikliğin aynı işlem içinde olmasıdır. SQLite `BEGIN IMMEDIATE` yazma işlemini baştan alır ve aynı anda başka yazıcı varsa bekleme/başarısızlık gündeme gelir; eski istemci revizyonunu ayrıca karşılaştırmak gerekir. Markdown'a yalnız revizyon alanını taşımak bu işlemi taşımaz. [SQLite işlem belgesi](https://www.sqlite.org/lang_transaction.html)

**2. Önce ne ölçülmeli?**

Önce iki kontrollü istemciyle zamanlamayı kurar, sonra iki gerçek ajanla — bir Claude, bir Codex — kendi araç yollarının bu korumaya gerçekten uyduğunu ölçerdim. Bu turda ajan çalıştırmadım. Lab'de sentetik `BEYIN.md`, konu notu ve açık işler dosyası yeterli; gerçek özel notları taşımaya gerek yok.

İlk yük iki **birbirinden bağımsız ve korunması gereken** değişiklik olsun: A bir karar, B başka bir karar eklesin. İki istemci aynı başlangıç sürümünü okuyup “okudum” bariyerine ulaşsın; ardından A yazsın, sonra B eski sürümden yazmayı denesin. Ters sırayı da çalıştır. `sleep` ile eşzamanlılık varsayma; okunmuş sürümü ve yazma sırasını hazır işaretleriyle kanıtla.

| Yol / durum | Deneyin ayıracağı şey |
|---|---|
| Tüm dosyayı değiştiren `Write` | İki başarı bildirimi varken ilk bağımsız etkinin kaybolması |
| Kabukta okuma→değiştirme→yazma; geçici dosya→replace | Yerleşik düzenleme aracını kullanmadan aynı kaybın mümkün olması |
| `Edit` / patch, aynı hedef metin | Bayat önkoşul gerçekten reddediliyor mu; reddedilince dosya değişmiyor mu? |
| `Edit` / patch, farklı bölgeler | İki etki korunuyor mu; aracın metin eşleşmesi yalnız yerel bölgeyi mi denetliyor? |
| Koşullu yazma, aynı temel sürüm | İlk denemede bir uygulama + bir açık çatışma; yeniden okuma ve yeniden hazırlamadan sonra iki etkinin korunması |
| Kontrolden hemen sonra duraklatma | İki istemcinin aynı hash'i geçip sonradan birbirini ezebildiği kontrol–yazma aralığı |

`Edit` başarısını ayrı bir anlamsal örnekle de sına: B başka bölümdeki bir karar değiştiği için artık yanlış hâle gelen bir cümleyi, hedef dize hâlâ aynı diye değiştirebilsin. Böylece “metin eşleşti” ile “kararım güncel dayanaklara dayanıyor” ayrılır. Araçların bu davranışlarını adı üzerinden varsayma; gerçek sürüm ve gerçek çağrı yolunu kaydet.

Her işlem için deney kimliği, aktör, yazma yolu, okunan sürüm/içerik, amaçlanan bağımsız etki, önerilen çıktı, gerçek yanıt ve disk üzerindeki önce/sonra durumları tutulsun. İstemcinin “yazdım” beyanı dışında, deney yöneticisi duraklama noktalarında dosyayı okuyup beklenen içeriği karşılaştırsın. A'nın etkisinin bulunmaması, sonraki bir görevle bilerek kaldırılmadığı sürece kayıp sayılır. Reddedilen öneri kayıp değildir; **uygulanmış diye bildirilen etkinin sessizce silinmesi** temel başarısızlıktır. “Sadece son JSON geçerli” türü bir ölçüt burada yeterli değildir.

Güvenlik ölçütü: bayat bütün-dosya önerilerinde sessiz kayıp 0; çatışmada dosya değişikliği 0; kabul edilen bağımsız etkilerin korunması. Kullanılabilirlik ölçütleri ayrı olsun: çatışma oranı, yeniden okuma/deneme sayısı, bekleme süresi ve farklı bölgelerdeki zararsız değişikliklerin kaç kez engellendiği. Bir sonraki aşamada iki ajanla örneğin 20 görev çifti, doğal araç seçimini ve sürtünmeyi gösterebilir; bu sayı bir güvenlik kanıtı değildir.

**“Port gereksiz” sonucu ne olur?** Mevcut bütün izinli yazma yollarının zaten aynı koşullu uygulama sözleşmesini sağladığı ve alternatif yolların aşamadığı gösterilirse ikinci bir katmana gerek yoktur. Ya da ortak dosyalara yalnız tek yazıcı erişebiliyorsa, ayrı bir iki-yazıcı portu yerine bu mimari korunur. Yalnız “bu koşularda kayıp görmedik” veya “ajanlar genelde Edit seçti” yeterli değildir. Kontrollü korumasız karşı örnek bile üretilemiyorsa önce deneyin doğru aralığı zorlayıp zorlamadığı sorgulanmalı.

**3. En küçük mekanizma ve doğru katman**

İlk lab sürümünü tek dosyaya koşullu uygulama yapan ortak yazma kapısı olarak kurardım. Okuma, içeriği ve ona bağlı sabit temel token'ını verir. Ajan yeni metni kendi alanında hazırlar. Kapı, bu temel token ile öneriyi alır; kısa kilidi tutarken güncel içeriği yeniden okur, sürümü karşılaştırır ve uygunsa aynı dosya sistemindeki hazır dosyayı hedefe geçirir. Uymuyorsa açık çatışma döner ve hedefe dokunmaz. Ajan güncel metni okuyup taslağı yeniden kurar; yalnız token'ı yenileyip eski taslağı tekrar göndermek yasaklanması gereken kurtarma davranışıdır.

İlk lab için ortak tek kilit, dosya başına çok sayıda kilitten daha kolay denetlenir. Kilit LLM düşünürken tutulmaz; kilit nesnesi hedef dosyanın replace ile değişen nesnesinden ayrı ve sabit kalır. Yerel `dosya_kilidi.py:9` verilen yolu kilitliyor; `devir.py` bunu yan `.lock` dosyasında kullanıyor. Bu, aynı kurala uyan süreçleri sıralar. Başka bir aracın Markdown'ı doğrudan yazmasını kendiliğinden engellemez.

**Kapının zorunlu olması algoritmanın parçasıdır.** Lab'de ajanların ortak son dosyalara doğrudan yazma hakkını kaldırıp yalnız kendi öneri alanlarına yazmalarını; son dosyayı ayrı yetkili yazıcının değiştirmesini öneririm. `Write`, `Edit`, shell, rename/replace, gece yazıcısı ve varsa Obsidian/senkronizasyon süreçlerinin kapsama girip girmediğini açıkça listele. Denetimli araç kullanmayan yazıcı varsa garanti yalnız katılan yazıcılar için geçerlidir. Önce mevcut harness'in bunu zorlayıp zorlayamadığını ölç; zorlayamıyorsa yalıtılmış worktree + tek entegrasyon yolu daha dürüst alternatiftir.

Araç içi koşullu uygulama veya bu ortak yazıcı doğru yerdir. Ön-hook'un hash'e bakıp sonra serbest bırakması arada başka yazıya izin verir; son-hook hasarı ancak sonradan görebilir. Bir hook tüm yazma süresini kapsayıp geçişi zorlayabiliyorsa yardımcı olabilir, fakat sadece önce/sonra bildirim veren hook için bu garanti varsayılmaz. Ajan talimatı protokolü açıklar; dosya erişiminin yerine geçmez. Git commit hook'u da commit öncesinde kaybolmuş çalışma-ağacı içeriğini geri getiremez.

İlk garanti **tek dosya ve belirtilen yazıcılar** olsun. Not + harita + açık işler dosyasını birlikte değiştiren işlerde tek tek hash kontrolü bütün işi işlem yapmaz. Başka dosyadan okunan kararlar da değişikliği etkiliyorsa o okuma kümesi doğrulanmalı. Birden çok dosyayı kilit altında sırayla yazmak bile süreç ölümünde yarım iş bırakabilir. Bunu Y1 olay kimliğiyle yeniden yürütülebilen adımlar olarak ele alabilir veya ayrıca çoklu-dosya işlem mekanizması tasarlayabilirsin; ilk sürüme olmayan atomiklik atfetme. Yeni dosyada “hâlâ yok” önkoşulu gerekir; silme/yeniden adlandırma yolları da korunmalı veya ilk kapsamda açıkça reddedilmelidir.

**4. Yapmayacağım şeyler ve yanlış güven ölçütleri**

| Yanlış çıkarım | Eksik kalan bağ |
|---|---|
| HEAD aynı → dosya aynı | Commit edilmemiş değişiklik |
| Hash kontrolü geçti → yazma güvenli | Kontrol ile uygulama arasındaki yarış |
| Atomik replace → güncelleme kaybolmaz | Bayat fakat bütün bir dosya da atomik biçimde eskisinin üstüne geçebilir |
| Kilit dosyası var → bütün yazıcılar kilitli | Diğer yollar o kilide katılmayabilir |
| Edit başarılı → bütün dayanaklar güncel | Hedef metnin dışındaki anlamsal bağımlılıklar |
| İki exit 0 / iki log satırı → iki etki korundu | Gerçek son içerik ve işlem geçmişi |
| Git merge çatışmasız → kararlar tutarlı | Ayrı satırlardaki anlamsal çelişki |
| Çatışma var ama otomatik zorla yeniden dene → sorun çözüldü | Eski önerinin yeni sürüm numarasıyla kabulü |

`os.replace` mevcut dosyayı değiştirebilir; API beklenen eski içerik koşulu almaz. Bu nedenle replace, sürüm kontrolünün veya işlemin tamamının yerine konamaz. [Python os.replace belgesi](https://docs.python.org/3/library/os.html#os.replace) Benzer biçimde `git worktree lock`, çalışma dosyalarının düzenlenmesini kilitleyen mekanizma değildir; worktree'nin yönetim bilgilerinin temizlenmesini, taşınmasını/silinmesini korur. [Git açıklaması](https://git-scm.com/docs/git-worktree)

İşlem uygulandıktan sonra yanıt kaybolabilir. Bu durumda “başarısız” deyip aynı etkiyi körlemesine tekrarlamam; işlem kimliğiyle durumu uzlaştırır, belirlenemiyorsa **belirsiz** olarak bırakırım. Ayrı dosyadaki başarı logu ile Markdown değişikliği birlikte atomik değilse logu gerçeğin kendisi saymam. Süreç ölümü ile elektrik kesintisi dayanıklılığını da aynı deney sonucu diye sunmam.

İlk adımda bütün Markdown'ı veritabanına taşımam, CRDT veya otomatik anlamsal birleştirici kurmam, LLM düşünme süresince uzun kilit tutmam. Önce bayat yazının görünür çatışmaya dönüşmesini ve kaçış yollarını ölçerim. §22'deki “geçmiş hiç ölçülemez” sözünü de daraltırım: yalnız commit geçmişi kaybı göstermeyebilir; korunmuş eski içerikler ve araç izleri varsa tekil geçmiş olaylar yeniden kurulabilir. Kayıt yokluğu, kayıp yokluğunu kanıtlamaz.

**Önerdiğim deney, uygulayıcıya beş adım:**

1. Lab'de sentetik üç dosya, iki kontrollü istemci ve bütün yazma yollarının listesini hazırla; iki istemcinin aynı sürümü okuduğunu bariyerle doğrula. Kanıtı final dosyadan bağımsız işlem niyetleri ve ara durumlarla topla.
2. Mevcut `Write`, shell ve `Edit` yollarını aynı/farklı bölge görevleriyle çalıştır; A→B ve B→A sıralarında kayıp, ret ve korunan etkileri ayrı say. HEAD değişmeyen karşı örneği özellikle dahil et.
3. Ortak koşullu yazıcıyı aynı senaryoya sok: ilk bayat bütün-dosya denemesinde bir uygulama + bir çatışma, yeniden hazırlama sonrasında iki etki bekle. Sürüm denetimini kaldıran ve kontrol–uygulama kilidini kaldıran iki ayrı sabotaj deneyleri düşürmeli.
4. Gerçek Claude ve Codex araçlarıyla geçişi doğrula; doğrudan shell/Write ile kapıyı aşmayı, replace öncesi/sonrası süreç ölümünü ve yanıt kaybını sına. Korumasız yol başarıyla ortak dosyayı değiştirebiliyorsa genel güvenceyi reddet; Linux lab sonucu Windows yerel davranışı ölçülmüş sayılmaz.
5. Sessiz kayıp ve bypass sayısı 0, çatışmada hedef değişikliği 0, kurtarma sonrası beklenen etkiler korunmuşsa sürtünme ölçümleriyle port kararını ver; yerel hook entegrasyonunu brief'teki kullanıcı onayı aşamasına daha sonra taşı.
