# İkinci beyin mimarisi

Sistemin neden böyle kurulduğu. Neyin hangi katmanda durduğu, neyin bilinçli
olarak dışarıda bırakıldığı.

> Merkez: [[BEYIN]] · İlgili: [[kapanis-ritueli]] · [[tasarim-dersleri]] · [[capraz-arac-baglam]] · [[acik-uclar]]
> Kaynak: [[2026-09-07-ikinci-oturum]] (claude 3557db3e · 07–16.09)

---

## İki katmanlı not yapısı (16 Eylül kararı)

Notlar 16 Eylül'e kadar tek bir 39 KB'lık dosyaydı (`OTURUM-NOTLARI.md`). İkiye
bölündü:

- **`notlar/` — kalıcı katman.** Konuya göre. Her oturumda okunur. Ölçümler,
  hatalar, tasarım dersleri, kullanıcı bağlamı, açık uçlar.
- **`oturumlar/` — arşiv katmanı.** Oturuma göre. Kronolojik kayıt. Her oturumda
  okunmaz, sorulunca okunur.

**Bölme ekseni neden konu, neden sadece oturum değil:** kullanıcının ilk önerisi
"her oturum kendi dosyasını yazsın, yeni oturum sadece sonuncusunu okusun" idi.
Bölme fikri doğru, ikinci yarısı yanlış — çünkü **bilgi oturumla eskimiyor.**
30 Ağustos'ta ölçülen Whisper karşılaştırması ya da `ffmpeg -vsync` tuzağı bugün
de geçerli; sadece son oturum okunursa hepsi görünmez olur ve yeniden keşfedilir.
Eskiyen şey konuşma; ölçüm ve karar eskimiyor.

Kapanış bu yüzden **iki çıktı** üretir: oturumun kendi kaydı (arşiv) ve kalıcı
olanın ilgili konu notuna terfi ettirilmesi (damıtma). İkincisi kalıcı katmanı
hem küçük hem güncel tutan şeydir.

Yan kazanç: Obsidian graph'ı ancak çok sayıda bağlı notla anlamlı olur. Tek dosya
model için iyiydi, graph için kötüydü.

## Katmanlar: "bana dair her şey olmalı" reddedildi

Kullanıcının tezi: ikinci beyin içinde kendisine dair her şey olmalı (özel
bilgiler hariç). **İtiraz edildi ve kabul gördü.** İnsan hafızasını değerli kılan
şey biriktirmesi değil **unutabilmesi**; her şeyi eşit ağırlıkta tutan sistem
hiçbir şeye ağırlık vermemiş olur. Somut maliyet: otomatik yüklenen her satır,
her oturumun düşünme alanından çalınır.

Doğru soru "ne girsin" değil, **"hangi katmanda dursun"**:

| Katman | Ne | Kural |
|---|---|---|
| **Sıcak** | Kim olduğun, ne yaptığın, nasıl çalıştığın | Her oturumda yüklenir → küçük ve durağan kalmalı |
| **Soğuk** | Oturum kayıtları, eski kararlar, ölçümler | Diskte durur, sorulunca aranır |
| **Hiç girmeyen** | Kimlik no, mali detay, kimlik bilgileri | Girmez |

Üçüncüsü sadece mahremiyet değil **güvenlik** meselesi: bağlamda ne varsa dışarı
sızma riski olan odur ve model internetten veri okuyan bir ajandır. Kullanıcının
ikinci teknik hedefi olan App Security bu sistem üzerinde somut olarak
çalışılabilir (prompt injection, bağlam sızdırma, araç izinleri).

## Elenen: diğer projelerin loglarını okutmak

Log ile damıtılmış bilgi ayrı şeyler; ham kaydın çoğu araç çıktısı ve çıkmaz
sokak. Üstelik log "o an ne düşünüldüğünü" söyler, "şu an ne doğru olduğunu"
değil. Projeler arasında paylaşılması gereken şey proje bilgisi değil, **kişi
bilgisi** ve **taşınabilir teknik**. Mekanizması log okumak değil, ortak hafıza
klasörü — hâlâ açık uç.

## mem0: yeri ve sırası

**Disk taratmak için değil.** mem0 bir indeksleyici değil; klasör taramaz,
konuşma sırasında içine yazılanı tutar. Doğru sıralama: **önce grep** (aramaların
çoğu sözcükseldir ve bedavadır), yetmezse **yerel gömme indeksi** (kuruldu, bkz.
[[arac-arsiv]]), **mem0 en sonda**.

**Gerçek yeri:** kapalı bulut uygulamaları (ChatGPT web, Gemini, Grok) için ortak
hafıza katmanı — bir köprü, beyin değil. Ve köprü **tek yönlü**: bulut
uygulamasının yereldeki beyni *okumasını* sağlar, orada konuşulanların
*yakalanmasını* sağlamaz. Çapraz-araç boşluğunu kapatmaz; onu yakalama kapatır.

Sıra: buluta aynalanacak şey önce iyi olmalı. Zayıf bir beyni aynalamak az şey
kazandırır.

## Obsidian'ın yeri

Bağlar `[[...]]` biçiminde **düz metin olarak dosyaların içinde** durur — bağ
veride, programda değil. Model Obsidian'a ihtiyaç duymaz, dosyaları diskten okur.
Obsidian bir görüntüleyici ve graph aracıdır; silinse notlar durur.

## Avenox'un ikinci beyin sistemi — değerlendirme (16 Eylül)

Kaynak: `github.com/avenoxai/sifirdan` · ekstra-ikinci-beyin/notlar.md

**Kurulmadı.** Gerekçe: bileşenlerinin çoğu burada zaten kurulu ya da bilinçli
olarak elenmiş; kurulum yöntemi ("şu prompt'u yapıştır, ajan kursun") öngörülemez
ve bu klasöre doğrultulursa kendi `CLAUDE.md` kurallarımızla, hook'umuzla ve tek
merkezli not yapımızla çakışır. İki hafıza sisteminin çelişmesi tek hafızadan
kötüdür. Denenecekse **ayrı ve boş bir vault'a** kurulmalı.

**Alınan üç fikir:**

1. **Kaynak gösterme** — en değerlisi. Bkz. [[kapanis-ritueli]].
2. **`PreCompact` hook'u** — Durum B'yi güvenlik ağı olarak kapatıyor.
3. **Git** — yedek ve geçmiş. Öğrenme gerektirdiği için ertelendi.

**Alınmayanlar:** Obsidian (zaten var, isteğe bağlı), mem0 (sırası gelmedi),
akşam derleyicisi otomatik özetleyici olarak (yerine **dedektör** kuruldu —
özet yazmaz, eksik gösterir).

**Doğrulanamayan iddia:** "130 gündür elle müdahalesiz çalışıyor." Kendi tasarım
derslerimize göre bu tek başına bir şey söylemez: bir sistem çalışıyor görünürken
sessizce kötü özetler üretiyor olabilir.

## Paralel oturumlar: kalıcı katmanın kör noktası (16 Eylül)

Kullanıcının sorduğu ve gerçek bir boşluğa denk gelen soru: *"Şimdi yeni bir
oturum açsam, bu oturumda konuştuklarımızı bilir mi?"*

**Kendiliğinden bilmez.** Yeni oturum `BEYIN.md` ve `notlar/` okur — yani
**damıtılmış** olanı. Henüz kapanmamış bir oturumda konuşulanlar damıtılmamıştır,
dolayısıyla kalıcı katmanda yoktur. Bu, iki katmanlı yapının doğal sonucu ve
kaçınılmaz: damıtma kapanışta olur.

**Ama ham kayıt canlıdır.** jsonl sürekli yazılıyor; açık bir oturumun kaydı,
o oturum devam ederken bile başka bir oturumdan okunabilir. Yani bilgi
erişilemez değil, sadece **otomatik gelmiyor**.

Çözüm: `SessionStart` hook'u PowerShell'den `araclar/oturum_basi.py`'ye taşındı
ve iki şey daha enjekte ediyor:

1. **Oturumun kendi kimliği.** Araçların argümansız çağrısı "en son yazılan
   kaydı" seçer; aynı projede iki oturum açıkken yanlış oturumu seçebilir.
   Kimlik bilinince `omurga.py <id>` kesinleşir.
2. **Paralel oturum uyarısı.** Son 6 saatte yazılmış başka oturum kaydı varsa
   listeleniyor, "bunlar henüz kapanmamış olabilir, notlarda görünmezler, ham
   kayıtları şöyle okunur" diye. Kritik cümle: *kullanıcı "az önce şunu
   konuşmuştuk" derse ve notlarda yoksa tahmin etme, paralel oturumun kaydını
   oku.*

Böylece yan iş için açılan bir oturum, gerektiğinde ana oturumun bağlamına
**ulaşabilir** hale geliyor — otomatik yüklenmiyor (ki yüklenmemeli, bağlam
pahalı), ama nasıl ulaşacağını biliyor.
