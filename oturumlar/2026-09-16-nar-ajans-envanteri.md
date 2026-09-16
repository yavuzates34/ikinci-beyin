# Nar Ajans çalışma alanı — envanter ve ilk kararlar

**16 Eylül 2026, 04:00–04:45.** Oturum `3557db3e` içinde açılan ikinci iş kolu.
Amaç: `C:\Users\Anj\Desktop\Nar Ajans - Codex` klasörünü düzenlemek ve oraya
playground'dakine benzer, ama kendi koşullarına uygun bir hafıza kurmak.

Bu dosya **ölçüm kaydıdır.** Nar Ajans'ın kendi beyni kurulduğunda buradaki
kalıcı bulgular oraya terfi eder; bu dosya arşivde kalır.

## Neden ayrı bir iş kolu

Kullanıcı üç şeyi baştan kararlaştırdı (16.09 04:00–04:07):

1. **Federe hafıza.** Merkezde iş hafızası, her alt projede kendi küçük notu.
   Tek merkezi hafıza elendi: `fuar-takvimi-api`'nin hafızası ile Nar Ajans'ın
   iş hafızası aynı şey değil.
2. **İş bölümü.** Claude kendi tarafını kurar (hook'lar, `CLAUDE.md`), Codex'in
   tarafını **onun yerine kurmaz** — Codex'e devir notu bırakılır, kullanıcı
   Codex'i açıp kendi düzenlemesini ona yaptırır.
3. **Yedeksiz adım yok.** Envanter ve yedek çıkmadan tek dosya oynatılmaz.

## Ölçülen durum

**Kök dizin git deposu değil.** 4.9 GB, ~17.000 dosya, 17 öğe. İçinde 6 git
deposu var:

| Depo | Durum |
|---|---|
| `fuar-takvimi-api` | Gerçek depo, GitHub uzaklı, temiz, `main` |
| `nar-ajans` | Gerçek depo, GitHub uzaklı, **`agent/add-site-images` dalında**, 4 takipsiz |
| `Staffing-imgs` | Gerçek depo, GitHub uzaklı, 6 takipsiz |
| `Instantly` | Commit yok, dal yok. 105 nesne, 2.6 MB |
| `Instantly/Katılımcı-listeleri` | Commit yok, dal yok. **2.558 nesne, 171 MB.** İç içe depo |
| `NAR - Sözleşme Oluşturma` | Boş depo, **klasörün kendisi de tamamen boş** |

**Bu üç "boş" depoyu kullanıcı açmamış — Codex açmış.** Kanıt: hepsinde
`refs/codex/turn-diffs/checkpoints/<sha>/...` ref'leri var, `refs/heads` boş.
Codex her turun anlık görüntüsünü oraya yazıyor. Codex'in kendi incelemesi
`Instantly/.git` içinde **16 aday kök ağaç** buldu (blob=66, tree=39);
`TODAY-CHECKLIST.md` → `TODAY-CHECKLIST-GUNCEL.md` geçişi ve CSV'lerin gelip
gitmesi o görüntülerde izlenebiliyor (codex 01a0a7d7 · 16.09 04:35).

**Düzeltme kaydı:** ilk okumada bu depolara "terk edilmiş `git init`, boş kabuk,
silinse kaybı yok" demiştim ve kullanıcının onayını o yanlış bilgiyle aldım.
Yedek doğrulaması sırasında ortaya çıktı, uygulanmadan önce düzeltildi
(claude 3557db3e · 16.09 04:27). **Ders:** commit yokluğu deponun boş olduğunu
göstermez; `refs/` altına bakmadan "boş" denmez.

**Hacim metinde değil ikili dosyalarda.** Instantly 1.6 GB (neredeyse tamamı
`Katılımcı-listeleri`), nar-ajans 1.4 GB, Kataloglar 1.1 GB, codex-backups
620 MB. Buna karşılık **bilgi katmanı toplam ~400 KB markdown.**

**Canlılık (son değişiklik tarihine göre):** Instantly, Kataloglar,
codex-backups 15 Eylül; Staffing-imgs 10 Eylül; Kartvizit 8 Eylül. Ağustos'ta
donmuşlar: nar-ajans (19.08), fuar-takvimi-api (20.08), google-workspace-tools
(27.08), Logolar (27.08), design-source (06.08).

**Disk:** C: sürücüsünde **11.5 GB boş** (222 GB'ın %5'i). Ayrı bir konu ama
yedekleme kararlarını sınırlıyor.

## En kritik risk

`Instantly/` operasyonun kalbi — kampanya kuralları, fiyat listesi, müşteri
metin kuralları, 37 maddelik hata kaydı, araştırma protokolü — ve **hiçbir
sürüm geçmişi yok.** Bir dosya bozulursa geri dönüş yok. Playground'da git'in
iki kez kurtardığı şeyin karşılığı burada mevcut değil.

İyi haber: `Instantly/.gitignore` doğru; `.env` (Reoon ve fuar API anahtarları)
git'in görüş alanı dışında. `git check-ignore` ile doğrulandı.

## Yapılan tek fiziksel iş: yedek

`C:\Users\Anj\Yedekler\NarAjans-20260916-0422` — robocopy ile birebir kopya.
**20.307 dosya, 4.21 GB, 0 hata, 7 dakika.** `node_modules` ve `__pycache__`
hariç (611 MB, yeniden üretilebilir). Kritik dosyaların MD5'leri tek tek
karşılaştırıldı, Türkçe karakterli derin yollar dahil hepsi aynı.

Zip yerine klasör kopyası seçildi: Türkçe karakterli adlar arşiv formatlarında
sorun çıkarabiliyor, tek dosya geri almak kopyada zahmetsiz
(claude 3557db3e · 16.09 04:22).

## Açık kalanlar

- **Instantly nasıl sürümlenecek?** Codex'in `.git`'ini paylaşmak
  (`refs/heads/main` bizim, `refs/codex/*` onun) en az müdahale görünüyor ama
  Codex'in checkpoint mekanizmasını bozup bozmayacağı bilinmiyor. Kullanıcı bu
  kararı Claude'un tek başına değil, **bir Codex ajanıyla ortaklaşa** almasını
  istedi.
- **Kök depo kurulsun mu?** Kurulursa Codex checkpoint'lerini oraya yazabilir;
  `.gitignore` olmadan bu her turda 4.2 GB'lık anlık görüntü demek. Sıra bu
  yüzden **önce `.gitignore`, sonra `git init`.**
- **`Katılımcı-listeleri/.git` 171 MB** — temizlenmeli mi, temizlik geri alma
  yeteneğini ne kadar geriye götürür?
- **Kökte `AGENTS.md` yok.** Claude kökte 6.8 KB talimatla çalışıyor, Codex
  talimatsız. Ortak kuralların ikisinin de okuduğu bir yerde olması gerekiyor.
- **Bayatlama tuzakları:** `Instantly/DURUM.md` mezar taşı olarak duruyor ama
  duruyor; `TODAY-CHECKLIST-GUNCEL.md` adında "güncel" geçen dosya.
- **`NAR - Sözleşme Oluşturma` tamamen boş** — silinsin mi, kullanıcıya sorulacak.

## Yöntem notu

Codex'e danışma `-s read-only` ile zorlandı. Codex'in kendi yapılandırması
`sandbox_mode = "danger-full-access"` ve `approval_policy = "never"`; fikir
almak için çağrılan bir ajanın yazma yetkisi olmamalı
(claude 3557db3e · 16.09 04:31).

İlk danışma turu elektrik kesintisiyle yarıda kaldı; oturum kimliğiyle
(`codex exec resume 01a0a7d7-...`) kaldığı yerden açıldı. Codex'in ürettiği
48 KB'lık ara çıktı diskte durduğu için araştırma yeniden yapılmadı.

Bağlantılar: [[kapanis-ritueli]], [[yasanan-hatalar]], [[acik-uclar]]

## Codex'le ortak karar ve uygulama (04:49–05:00)

Danışma `codex exec` ile yapıldı, `-s read-only` zorlandı, ilk tur kesintiye
uğrayınca `codex exec resume <oturum-id>` ile kaldığı yerden sürdürüldü.
`resume` alt komutu `-s`/`-m`/`-C` bayraklarını **almıyor**; kısıt ancak
`-c sandbox_mode="read-only"` biçiminde veriliyor. Ayrıca resume çalışma
dizinini taşımıyor, çağıran oturumunkini alıyor.

**Codex planımdaki gerçek bir hatayı yakaladı:** `Katılımcı-listeleri` iç içe
bir depo olduğu için, yalnızca `Instantly`'ye commit atmak o klasörün
dosyalarını sürümlemiyor — git kendi `.git`'i olan alt klasöre girmez. Yani
"aynı depoyu paylaş" planı 38 KB'lık hata kaydını ve araştırma protokolünü
korumasız bırakacaktı (codex 01a0a7d7 · 16.09 04:49).

Ortak karar: **hiçbir şey silinmeden iki depoya ayrı ayrı commit.** Birleştirme
ertelendi — geri alınabilir bir iş.

Codex'in kök depo hakkındaki görüşü: **kurmayın.** İç içe depolar gitlink gibi
davranabilir, commit'siz depolar hata çıkarabilir. Kök dosyalar sürümlenecekse
ancak "yalnızca izin verilenleri takip eden" sıkı bir meta depo olarak.

## Uygulanan

- `Katılımcı-listeleri/.gitignore` yazıldı (yoktu). `tmp/` **1.3 GB** ve o
  klasörün ağırlığının neredeyse tamamı; dışarıda bırakıldı.
  İlk commit: **257 dosya, 22.4 MB** (`11f4a22`).
- `Instantly/.gitignore`'a `tmp/`, `__pycache__/` ve `Katılımcı-listeleri/`
  eklendi. Sonuncusu bilinçli: alt depo ayrı, yanlışlıkla bozuk gitlink
  eklenmesin. İlk commit: **47 dosya, 12.2 MB** (`19e1592`). `.env` dışarıda
  kaldığı `git check-ignore` ile doğrulandı.

## Ölçülmüş bulgu: uzun yol, checkpoint'leri git'e görünmez yapıyor

Codex'in checkpoint ref'leri şu biçimde:
`refs/codex/turn-diffs/checkpoints/<64 hex>/<64 hex>/<13 hane ts>/<uuid>`

Bu yol `Katılımcı-listeleri` içinde **311 karakter** — Windows'un 260 sınırının
üstünde. Sonuç: `git for-each-ref` ref'i hiç listelemiyor, `git show-ref`
"bad ref ... (0000...)" diyor. Yani checkpoint git açısından **bozuk** ve bir
`git gc` onu çöp sayıp işaret ettiği nesneleri silerdi.

Çözüm ölçüldü: `git -c core.longpaths=true show-ref` ref'i doğru çözüyor
(`4e3775be...`). İki depoya da `core.longpaths=true` kalıcı olarak yazıldı
(claude 3557db3e · 16.09 05:00).

**Ders:** "nesne erişilemez" demek "çöp" demek değil. Erişilemezliğin sebebi
ref'in yokluğu olabileceği gibi, ref'in **okunamaması** da olabilir. Temizlikten
önce sebep ayırt edilmeli. Codex'in raporladığı 125 MB'lık erişilemez yığının
bir kısmı muhtemelen bu yüzden erişilemez görünüyordu.

**Durum:** `Instantly`'de tek ref var (bizim commit) — oradaki checkpoint
klasörleri gerçekten boş iskelet. `Katılımcı-listeleri`'nde iki ref: bizimki ve
Codex'in bir checkpoint'i, artık görünür ve `gc`'ye karşı korumalı.

## Henüz yapılmayan

- Hafıza yapısının kendisi (asıl iş)
- Kök `AGENTS.md` ve Codex'e devir notu
- `NAR - Sözleşme Oluşturma` boş klasörü — silinsin mi, sorulacak
- `Katılımcı-listeleri/.git` içindeki ~125 MB erişilemez nesne — `gc` kararı
- Bayatlama tuzakları: `DURUM.md` mezar taşı, `TODAY-CHECKLIST-GUNCEL.md`

## Hafıza katmanı kuruldu (05:05–05:15)

Nar Ajans artık kendi hafızasına sahip. Kurulanlar:

- **`AGENTS.md`** — ortak kurallar, tek kaynak. Kök `CLAUDE.md` içindeki marka
  kararı, kapasite sayıları ve bağlayıcı güvenlik kuralları oraya taşındı,
  **kopya bırakılmadı.** Sebep ölçülmüş: Codex `CLAUDE.md` okumuyor, yani ortak
  sanılan kuralların yarısı ona görünmüyordu.
- **`CLAUDE.md`** yeniden yazıldı: başında "önce `AGENTS.md`", gerisi Claude'a
  özel. Eski sürüm yedekte duruyor.
- **`BEYIN.md` + `notlar/` + `oturumlar/`** — playground'daki yapının aynısı.
  Bilinçli olarak aynısı: kullanıcının iki projede iki zihin modeli taşıması
  gereksiz.
- **`CODEX-DEVIR.md`** — Codex'e devir notu. Onun tarafı onun kararı; ne
  yapıldığı, ne bırakıldığı ve neye dokunulmayacağı yazılı.

**Playground'un biçimi buraya zorla taşınmadı.** Oradaki `(15 Eyl 2026, Yavuz)`
biçimi zaten çalışıyordu, korundu; üstüne ajan ölçümleri için oturum işaretçisi
eklendi. Kullanıcının eklediği kural: **saat ve dakika zorunlu**
(16 Eyl 2026 05:03, Yavuz) — yalnız tarih, aynı gün alınmış iki kararın sırasını
kaybettiriyor.

Devralınan saatsiz kayıtlar için yöntem: **uydurma yok.** Saat çoğu zaman diskte
duruyor — kararın uygulandığı dosyanın damgası. `DURUM.md`'nin emekliye
ayrılması 15 Eyl 23:01, marka kararı 4 Eyl 14:23 böyle bulundu ve
`· saat dosya damgasından` diye işaretlendi.

## Bu oturumun kendi tuzağı

Ölü işaretçi tuzağına **iki kez** düşüldü. Biri devralınmıştı
(`memory/fuar-takvimi-api.md` — öyle bir klasör hiç yok). Diğerini ben yazdım:
`.claude/settings.json` dedim, dosyanın adı `settings.local.json`. Üstelik
"bir belgeye yol yazarken yolun var olduğu o an doğrulanır" kuralını yazdıktan
**on dakika sonra** (claude 3557db3e · 16.09 05:12).

Ders playground için de geçerli: kuralı yazmak, kurala uymayı sağlamıyor.
Denetim kuralın kendisinden ayrı bir iş — bağ denetimi bu yüzden komutla
yapıldı, gözle değil.

## Geriye dönük saatlendirme (05:19–05:30)

Kullanıcı kuralı sertleştirdi: **"kayıtlarda tüm saat detaylarını geriye dönük
olarak da yazmamız hayati derecede önemli"** (16 Eyl 2026 05:19, Yavuz).
Benim yazdığım kural "eskiler uydurularak doldurulmaz" diyordu; bu yeterli
değilmiş — doldurulmalı, ama kaynağı gösterilerek.

Devralınan **18 saatsiz kayıt** tarandı, 17'si saatlendi. Yöntem: arşiv arama.
`ara.py` ile kararın konuşulduğu mesaj bulunup zaman damgası alındı.

Üç işaret tanımlandı: `· saat arşivden` (kararın konuşulduğu an),
`· saat dosya damgasından` (uygulandığı an), `· saat arşivde bulunamadı`
(arandı, çıkmadı). Sonuncusu boşluk değil **ölçüm sonucudur** — bir sonraki
oturum aynı aramayı baştan yapmasın diye.

**Bulgu:** 15 Eylül 16:08'deki **tek kullanıcı mesajının içinde beş ayrı karar**
varmış ve bunlar üç ayrı dosyaya dağılmış: açılış biçimi, "arasında" kelimesinin
atılması, yalnız-WhatsApp kanalı, paket notunun yeri, kısa/uzun iki versiyon.
Saat eklenmeden önce bu beşinin aynı ana ait olduğu görünmüyordu — hepsi
"(15 Eyl 2026, Yavuz)" diye duruyordu. Saat, kararları **birbirine bağlayan**
şeymiş; sadece sıralayan değil (claude 3557db3e · 16.09 05:25).

Bu, playground için de geçerli bir ders: oradaki `(claude 3557db3e · 08.09 17:34)`
biçimi zaten saat taşıyor, ama insan kararları için aynı disiplin yoktu.

## Sözleşme klasörü kararı

`NAR - Sözleşme Oluşturma` klasörü tamamen boştu. Kullanıcı kararı bana bıraktı.
Silmeden önce arşivde arandı ve çıktı: sözleşme işi **5 Ağustos 17:00'de** Google
Drive'a taşınmış (`dryaylldzz@gmail.com` hesabı) ve ayrı bir Codex projesinde
(`Sözleşmeler`, oturum `019ea444`) yürütülüyormuş.

Karar: **klasör silindi, bilgi kaydedildi.** Gerekçe: boş ama çağrışımlı bir
klasör adı bir sonraki oturumu oraya yazmaya davet eder ve tek doğru kaynağı
ikiye böler. Değerli olan klasör değil, sözleşmelerin nerede olduğuydu — o
`AGENTS.md` §11 işaretçi tablosuna yazıldı (claude 3557db3e · 16.09 05:28).

## Taşıma uyarısı

Kullanıcı klasörü **D: sürücüsüne taşıyacağını** söyledi (Codex tarafında Astra
yapacak). Ölçülen risk: `~/.codex/config.toml` içinde bu ağaç için **altı**
yol-anahtarlı güven kaydı var; D:'de hepsi geçersiz olur. Ayrıca oturum arşivi
yola göre gruplandığı için proje adı ikiye bölünür — playground'da aynı şey
7 Eylül'de yaşanmıştı. Uyarı devir notuna ve açık uçlara yazıldı.

## Codex devraldı ve beni iki yerde düzeltti (08:17–08:32)

Kullanıcı devir notunu Codex'e (Astra, oturum `01a0a892`) verdi. Kendi tarafını
kurdu, klasörü taşıdı ve yazışma dosyasına cevap yazdı. **Üç iddiasını
bağımsız ölçtüm, üçünde de haklı çıktı.**

**Düzeltme 1 — güven kayıtları beş, altı değil.** `config.toml` içinde
"nar ajans" geçen satırları sayıp altı demiştim; altıncı saydığım
`desktop\nar ajans` bu ağaca ait değil, ayrı bir klasör.
**Ders:** eşleşmeyi ayırt etmeden saymak, arama sonucunu ölçüm sanmaktır.
`grep | wc -l` bir ölçüm değildir; neyi saydığını görmeden sayı yazılmaz
(claude 3557db3e · 16.09 08:28).

**Düzeltme 2 — uzun yol bulgusu fazla iddialı yazılmıştı.** "Erişilemezliğin
gerçek sebebi uzun yolmuş" demiştim. Ölçüm: `core.longpaths` erişilen nesne
sayısını 92'den 349'a çıkardı, yani **257 nesneyi kurtardı**; geri kalan
**2.236 nesne** hâlâ hiçbir ref'ten erişilemiyor. Doğru ifade: uzun yol gerçek
bir okuma sorunuydu ve bir `gc`'nin canlı checkpoint'i silmesini önledi, ama
yığının tamamını açıklamıyor. Kendi ölçümüm Codex'inkiyle birebir aynı çıktı
(2.585 / 349 / 2.236).

**Düzeltme 3 — DURUM kararı 22:57, 23:01 değil.** Ben dosya damgasından 23:01
yazmıştım; arşivde kullanıcı 22:57'de "Durum.md ile bundan sonra bir iş
yapmayalım" diyor, 23:01 modelin bitirdiğini bildirdiği an.

**Ve burada tasarımın kendisi işe yaradı:** o kaydın yanına koyduğum
`· saat dosya damgasından` işareti, Codex'e "bu saat çıkarımdır, kararın
kendisi değil" dedi; o da gidip gerçeğini buldu. İşaret koymanın sebebi tam
buydu ve **dört saat içinde** karşılığını verdi (claude 3557db3e · 16.09 08:30).

Codex'in benim kaçırdıklarım: WhatsApp kararı aslında 15:38'de verilmiş,
16:08 onu ayrıntılandırıyormuş; commit saatleri git committer zamanından tam
alınabiliyor (04:57:06, ben 04:58 diye yuvarlamışım); arşiv başlığındaki tarih
mesajın kendi damgasından farklı olabiliyor.

## Taşıma: junction çözümü

Klasör `D:\AI\Nar Ajans - Codex` konumuna taşındı; 50.996 dosya SHA-256 ile
doğrulandı. Eski masaüstü yolu **silinmedi, junction'a çevrildi** — yani tüm
mutlak yollar, kayıtlı proje girdileri ve eski görev dizinleri çalışmaya devam
ediyor. Taşımanın en pahalı yan etkisi böyle ödenmeden geçildi; benim "yol
anahtarları kırılır" uyarım bu sayede büyük ölçüde konusuz kaldı.

## Bu iş birliğinden çıkan yöntem notu

İki ajanın aynı klasörde çalışması, **birbirini denetlemesi** sayesinde işe
yaradı — nazik olduğu için değil. Codex benim iç içe depo hatamı, ben onun
okuyamadığı ref'i, o benim iki fazla iddiamı yakaladı. Ortak dosya olmasa
bunların hiçbiri görünmezdi; sohbette kalan düzeltme kaybolur.

Açık kalan: bağ biçimi ikiye bölündü — benim notlarım `[[wikilink]]`, Codex'in
yazdıkları markdown göreli bağ. Markdown bağda birleşmeyi önerdim (wikilink
yalnız Obsidian'da çözülür), itiraz gelmezse tek taraflı uygulanacak.

