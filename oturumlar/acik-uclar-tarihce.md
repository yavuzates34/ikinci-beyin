# Açık uçlar — tarihçe

`notlar/acik-uclar.md` içinden **kapanmış ya da devredilmiş** maddeler, metinleri
değiştirilmeden buraya taşındı (19.09.2026, kullanıcı kararı: tarihçe `oturumlar/`
altına, silme yok · claude 5c600e7e · 19.09 20:31). Git geçmişi taşımadan önceki
hâli de korur. Bu dosya bir oturum kaydı değildir; `kapanan-oturum:` satırı taşımaz.

> Güncel açık uçlar: [[acik-uclar]] · İlgili: [[sunum-incelemesi-onarim-listesi]]

---

## Sıradaki işler — madde 3 (Nar Ajans'a taşındı)

3. ~~**Yapıyı diğer projelere taşımak**~~ — **Nar Ajans'a taşındı**
   (16–17 Eylül 2026). O klasör artık kendi haritası, kalıcı notları, oturum
   arşivi, akşam derleyicisi ve üç hook'uyla çalışıyor. Yöntem ve elenenler:
   [[2026-09-16-nar-ajans-envanteri]] · [[iki-ajan-calismasi]].
   Diğer projeler için sıra kullanıcının önceliğinde.

## 17–18 Eylül'de açılanlar — madde 1 ve 2 (kapandı)

1. ~~**`SessionEnd` hook'u yok — kapanışsız oturum iz bırakmıyor.** Kapatılmadan
   bırakılan oturumdan kalıcı katmana hiçbir şey geçmiyor. Karar verildi, kurgu
   belli: *işareti ölen bant bıraksın, notu yaşayan bant yazsın.* Kurulmadı.
   Tasarım ve elenen alternatif: [[kapanis-ritueli]].~~
   **Kapandı 19.09 17:3x, SessionEnd'siz.** `araclar/gece_kayit.py` her gece
   kapanışsız ve 6 saattir sessiz oturuma temiz bağlamla taslak yazdırıyor
   (`oturumlar/oto-<id8>.md`). SessionEnd hook'u **elendi**: `kapanan-oturum:`
   satırı geldiğinden beri dedektörün kendisi işaret; çökme de böyle
   yakalanıyor. Taslak kalıcı notlara terfi etmez, onu bir sonraki oturum
   kullanıcıyla yapar. Bu oturumda uçtan uca sınandı: Sonnet 5, 103 saniye,
   7 KB taslak, 18 işaretçinin 18'i gerçek damga
   (claude 5c600e7e · 19.09 17:28). Ayrıntı: [[gece-derleyicisi]].

2. ~~**Omurga model tarafını taşımıyor.**~~ **Kapandı 19.09:** `omurga.py
   <id> --tam` kullanıcı mesajlarına modelin metin cevaplarını ekliyor (araç
   çıktısı ve düşünme hariç). En büyük oturum 258 KB, bu oturum 40 KB.
   Eski metin: Sadece kullanıcı mesajlarını çıkarıyor;
   ölçümler, elenen fikirler, gerekçeler ham kayıtta kalıyor. Madde 1'in ön
   şartı — zenginleştirilmeden temiz örnek eksik malzemeyle yazar.
   **Ek kusur (18.09):** `omurga.py` skill yüklemelerini kullanıcı mesajı
   sanıyor. Bu oturumun omurgasında `claude-api` skill'inin tamamı bir
   "kullanıcı mesajı" olarak göründü ve 128 KB'lık omurganın önemli kısmını
   doldurdu. ~~Filtrelenmeli.~~ **Düzeltildi 19.09 08:3x:** kayıtta bu satırlar
   `isMeta: true` taşıyor. `kayit.py` artık onları atlıyor. Arşivde 67 `isMeta`
   satırı var ve hepsi harness'in yazdığı şeyler: skill metni, komut uyarısı,
   "Continue from where you left off", görsel bilgisi. Kullanıcı mesajı yok.
   `7f10f7a3` omurgası: 137,6 KB / 90 mesaj → 46,0 KB / 89 mesaj. İşaretçi
   denetimi sonrasında yine temiz (42/42) (claude 5c600e7e · 19.09 08:33).
   Filtre ortak katmanda olduğu için `ara.py` ve `anlam.py` de skill metinlerini
   artık aramıyor.

## 17–18 Eylül — madde 3'ün kurulan alt maddesi (mekanik işaretçi denetimi)

   - ~~**Mekanik işaretçi denetimi**~~ **KURULDU 18.09 02:41** — gece
     derleyicisinde. Her işaretçiyi açar, oturum ve damga gerçek mi bakar;
     deseni tutmayanı da "denetlenemedi" diye ayrı raporlar. Negatif testle
     doğrulandı. İlk sonuç: 40 işaretçinin hepsi temiz. Bkz.
     [[gece-derleyicisi]].

## 19 Eylül — madde 1'in ayrıntılı durum metni (19.09 19:37'ye kadar)

   **Yapılan (19.09 16:40–17:10, commit `d0bdf11`):** `CLAUDE.md` → `AGENTS.md`
   (ortak kural, git geçmişiyle taşındı). `CLAUDE.md` artık `@AGENTS.md` içe
   aktarması ve Claude'a özel refleks tablosu. İçe aktarma, kayıt bırakmayan
   temiz bir Claude örneğiyle sınandı: iki kuralı da `AGENTS.md`'den okudu.
   Yönerge metni `.claude/`'dan `araclar/oturum-basi.md`'ye taşındı.
   `oturum_basi.py --bicim duz` hook'u olmayan ajan için. İşaretçi denetimi
   `(codex …)` biçimini de tanıyor. Codex adaptörü kuruldu: üç olay grubu,
   dört komut. **Açık:** kullanıcı güveni verilmedi; `/hooks` akışı resmî
   belgede CLI için var, Desktop'ta uçtan uca doğrulanmadı. Ayrıntı:
   [[iki-ajan-calismasi]] · [[2026-09-19-codex-sunum-ilk-alti-slayt]].
   **Netleştirme (19.09 19:37):** Kurulumun dosya olarak varlığı belirsiz
   değil; `.codex/hooks.json` ve çağırdığı adaptörler mevcut. Belirsiz olan bu
   proje katmanının kullanıcı tarafından güvenilir sayılıp sayılmadığı ve
   Codex Desktop'ta gerçek bir yeni oturumun `SessionStart` zincirini otomatik
   çalıştırıp uyarıları modele teslim edip etmediği. Bu oturumda
   `oturum_basi.py --bicim duz` elle çalıştırıldı; bu, otomatik hook zincirinin
   kanıtı değildir. Yeni oturumla uçtan uca sınanmalı
   (codex 01a0ba74 · 19.09 19:37).

## 19 Eylül — madde 2 ve 3 (kapandı)

2. ~~**Günlük rapor kimseye ulaşmıyor.** Derleyici raporu `derleme/gunluk/`
   altına yazıyor ama `SessionStart` onu açmıyor. "PUSH BASARISIZ" gibi bir
   uyarı kullanıcı sormazsa görünmüyor. 19.09 00:30'da tam olarak bu yaşandı:
   ethernet bağlı değildi, push düştü, 08:27'de hâlâ `ahead 1`
   (claude 5c600e7e · 19.09 08:27).~~ **Kapandı 19.09:** derleyici push
   sonucunu `son-calisma.json`'a yazıyor. `oturum_basi.py` o dosyadan yalnızca
   sorunları çıkarıp oturum başında söylüyor: yarıda kesilme, 36 saatten uzun
   sessizlik, push hatası, kusurlu işaretçi. Her şey yolundaysa sessiz kalıyor.
   Negatif testle doğrulandı.
3. ~~**Dedektör açık oturumu "işlenmiş" sayıyor.** Kimliğin herhangi bir notta
   geçmesi yeterli. Oturum içinde tek bir işaretçi yazılırsa (örneğin
   [[olculmus-bulgular]] §9) oturum kapanmamış olsa bile raporda görünmüyor.
   19.09 raporu "işlenmemiş 0" dedi; `5c600e7e` o sırada kapanmamıştı.~~
   **Kapandı 19.09:** kapanışın tek kaynağı artık arşiv dosyasındaki
   `kapanan-oturum: <id>` satırı. Arşiv dosyaları da başka oturumlara atıf
   yaptığı için "oturumlar/ içinde geçiyor mu" yeterli değildi. İkinci bir açık
   da kapandı: dedektör yalnızca son 24 saate bakıyordu, yani kapanmadan 24
   saat sessiz kalan oturum bir daha hiç raporlanmıyordu. Artık zaman sınırı
   yok. Oturum başındaki uyarı da 6 saatlik pencere yerine aynı ölçütü
   kullanıyor. Mevcut üç arşiv dosyasına işaret geriye dönük eklendi.

## 19 Eylül — madde 6–9 (onarım listesine devredildi: 7, 10, 12 ve sunum)

6. **Sağlayıcıdan bağımsız erken devir yok.** Kapanış ritüeli ortak, fakat
   başlangıç tetikleyicisi değil: bugün kullanıcı bağlam sayacını görüp anlamlı
   bir yerde “oturumu kapatalım” diyor. Codex Desktop sayaç göstermiyor ve
   incelenen oturumun etkin penceresi 258.400 token. `PreCompact` ise bağlam
   dolduğunda gelen son ağ; kontrollü erken devir değil. Tasarlanacak: güvenli
   eşik, ölçüm kaynağı, tur-sonu tetik, Claude/Codex adaptörleri ve kapanış
   işaretinin ancak gerçek geçişte yazılması (codex 01a0ba53 · 19.09 19:00).
   Bkz. [[kapanis-ritueli]].

7. **Sunum incelemesi — 10. slaytın ilk maddesine kadar.** İlk altı slaytta
   sekiz düzeltme adayı çıktı: otomatik
   okuma izlenimi; “ilk mesaj”ın öznesi; Desktop/CLI ayrımı; üç olay/dört komut;
   güven akışının sınanmamış olması; Desktop'ta bağlam sayacının görünmemesi;
   erken-devir boşluğu; yeni uygulamanın dosya ve komut erişimi ön koşulu.
   **Yeni bulgu:** Adaptör ayrımı sağlayıcıya göre değil, somut uygulama veya
   harness'a göre yapılmalı. Hook'lar Anthropic ya da OpenAI modelinin değil,
   Claude Code ve Codex gibi uygulamaların yeteneğidir; aynı sağlayıcının başka
   bir uygulamasında hiç bulunmayabilir. İlk oturumdaki başlangıç komutu bu
   yüzden uygulamayı ve gerçek yeteneklerini tespit etmeli, ortak çekirdeğe
   uygun adaptörü kurup sınamalı; eksik refleksleri de garanti varmış gibi
   göstermeden kaydetmelidir (codex 01a0ba74 · 19.09 19:21).
   7–10. slayt incelemesinde toplam sayı 13'e çıktı. Sunuma dokunulmadı;
   inceleme 10. slaytın kalan maddelerinden sürecek. Kayıtlar:
   [[2026-09-19-codex-sunum-ilk-alti-slayt]] ·
   [[2026-09-19-codex-sunum-yedi-on-ve-onarim-devri]]. Ortak onarım devri:
   [[sunum-incelemesi-onarim-listesi]].

8. **Kalıcı katmanın budama döngüsü yok.** Gece derleyicisi bilinçli olarak
   “ölçer, yazmaz”: haftalık raporda toplam boyutu ve 65 KB eşiğini gösteriyor,
   fakat büyüyen notları bölmüyor, kapanmış maddeleri soğuk katmana indirmiyor
   ve tekrarları birleştirmiyor. Boyut eşiğinin aşılması da şu anda oturum
   başına taşınan derleyici uyarıları arasında değil. Sonuç: başlangıçta
   haritadan seçmeli okuma context maliyetini sınırlıyor, ama kalıcı katmanda
   tarihsel tortu birikiyor. Çözüm otomatik silme olmamalı; derleyici büyük
   dosya, kapanmış madde, haritasız not, güncel durum/tarihçe karışması ve
   yoğun tekrar için **budama adayları** raporlamalı, sonraki canlı oturumda
   kullanıcıyla birlikte bakım yapılmalıdır (codex 01a0ba74 · 19.09 19:32).

9. **Gece taslağının kapsamı daha dar anlatılmalı.** Kullanıcı aynı oturuma
   dönerse taslağı işlemesine gerek yoktur; canlı bağlam ve ham kayıt devam
   eder. `oturum_basi.py`nin mevcut oturum kimliğini kapanmamış *diğer*
   oturumlar listesinden çıkarması bu nedenle büyük ölçüde doğru davranıştır.
   Taslak asıl olarak farklı/yeni bir oturumun kapanışsız kalmış eski oturumu
   kurtarması içindir; paralel oturum görünürlüğüne de yardım eder ama özel bir
   paralelleştirme mekanizması değildir. Aynı oturum daha sonra normal kapanırsa
   eski `oto-<id>.md` dosyasının temizlenip temizlenmediği ayrıca sınanmalı;
   açık kalan dar konu budur. Sunumdaki “Gece taslağını işleyelim” cümlesi,
   yalnızca başka bir oturum bu taslağı bildirdiğinde veya eski oturumun artık
   bittiğine karar verildiğinde geçerlidir (codex 01a0ba74 · 19.09 19:41).

## Nar Ajans'tan devreden (17 Eylül'de kapandı, tarihsel kayıt)

## Nar Ajans'tan devreden

> **17 Eylül'de kapandı — bu başlık artık iş listesi değil, tarihsel kayıt.**
> Nar Ajans kendi klasöründe kendi ajanlarıyla yürüyor; buradan oraya müdahale
> edilmez. Kural: [[proje-egemenligi]]. Aşağıdaki maddeler burada kapatılmaz,
> silinmedi çünkü neyin ne zaman devredildiği de bilgidir.


- **Astra'nın denetimi bekleniyor.** 17 Eylül'de Codex limitleri yenilenince
  kullanıcı denetim yaptıracak. Denetim notu ve kendi işaret ettiğim dört zayıf
  nokta o klasörün `notlar/asistan-yazismasi.md` dosyasında.
- **Gerçek `/compact` orada hiç olmadı.** Hook zinciri sahte girdiyle uçtan uca
  çalıştı; gerçek sıkıştırmada görülmedi. Burada aynı sınama yapılmıştı ve ilk
  denemede enjeksiyon ayağı kırılmıştı — yani bu sınama önemsiz değil.
- **Codex tarafında refleks yok.** Hook'lar Claude'a özel; asimetri oranın
  ortak kural dosyasına yazıldı. Talimat temelli bir disiplinin işe yarar mı
  yoksa sahte güven mi verir sorusu Astra'ya soruldu, cevabı beklemede.
- **Mükerrer oturum elenmiyor.** İki yol anahtarında (C: ve D:) görünen oturum
  iki kez sayılabilir. Aynı zayıflık burada da olabilir; bakılmadı.

## Kapananlar (8–16 Eylül)

## Kapananlar

- ~~Oturum özeti altyapısı~~ **8 Eylül** — kapanış ritüeli kuruldu. Bkz.
  [[kapanis-ritueli]].
- ~~Arşivde arama~~ **8 Eylül** — `ara.py`, `anlam.py`, `oku.py`, `kayit.py`.
  Claude + Codex, 123 oturum. Bkz. [[arac-arsiv]].
- ~~Notların tek dosyada birikmesi~~ **16 Eylül** — iki katmana bölündü
  (`notlar/` + `oturumlar/`). Bkz. [[ikinci-beyin-mimarisi]].
- ~~Kaynak gösterme yok~~ **16 Eylül** — kural `CLAUDE.md` kapanış ritüeline
  eklendi, kalıcı notlarda işaretçi kullanılıyor.
- ~~Gece derleyicisi yok~~ **16 Eylül** — dedektör + haftalık/aylık ölçüm
  kuruldu, görev zamanlayıcıya bağlandı. Bkz. [[gece-derleyicisi]].
- ~~Sürüm geçmişi ve dış yedek yok~~ **16 Eylül** — yerel git deposu açıldı,
  private GitHub deposuna bağlandı (`yavuzates34/ikinci-beyin`), derleyici
  her gece commit + push yapıyor. Bkz. [[gece-derleyicisi]].
- ~~Paralel oturum kör noktası~~ **16 Eylül** — `SessionStart` artık oturum
  kimliğini ve açık paralel oturumları bildiriyor.
- ~~Durum B açıkta~~ **16 Eylül** — `PreCompact` güvenlik ağı kuruldu,
  bloke etmeyen iki ayaklı tasarımla. Bkz. [[kapanis-ritueli]].
- ~~Devir kutusu zinciri gerçek sıkıştırmada denenmedi~~ **16 Eylül 03:32** —
  ikinci `/compact` ile sınandı, zincirin tamamı çalıştı: omurga yazıldı
  (73 mesaj), kutu doldu, mesaj modele ulaştı, kutu silindi. Teslimatı
  `UserPromptSubmit` değil `SessionStart` yaptı. Bkz. [[kapanis-ritueli]].
- ~~`PreCompact` gerçek sıkıştırmada denenmedi~~ **16 Eylül 03:13** — `/compact`
  ile sınandı. Deterministik ayak tuttu (omurga yazıldı), enjeksiyon ayağı
  şema hatasıyla düştü ve devir kutusuyla yeniden kuruldu. Bkz.
  [[yasanan-hatalar]] madde 15.
- ~~Klasör düzeni karmaşık~~ **16 Eylül** — kök dizin 20 öğeden 2 dosya +
  5 klasöre indi.
- ~~mem0 gerek var mı~~ **8 Eylül'de gerekçe netleşti, 16 Eylül'de sıraya kondu** —
  tek yönlü köprü, sırası en sonda.

