# Açık uçlar

Karar bekleyenler, yapılmamış testler, sıralanmış yol haritası.
Kapanan maddeler silinmez, üstü çizilir — neyin ne zaman kapandığı da bilgidir.

> Merkez: [[BEYIN]] · İlgili: [[kullanici-baglami]] · [[ikinci-beyin-mimarisi]] · [[capraz-arac-baglam]]

---

## Sıradaki işler

Altyapı işi 16 Eylül'de kapandı. Kalanlar **ertelenmiş**, sıradaki iş değil:

1. **Gelen kutusu** — ertelendi (kullanıcı kararı, 16 Eylül).
2. **mem0** — ertelendi (kullanıcı kararı, 16 Eylül).
3. ~~**Yapıyı diğer projelere taşımak**~~ — **Nar Ajans'a taşındı**
   (16–17 Eylül 2026). O klasör artık kendi haritası, kalıcı notları, oturum
   arşivi, akşam derleyicisi ve üç hook'uyla çalışıyor. Yöntem ve elenenler:
   [[2026-09-16-nar-ajans-envanteri]] · [[iki-ajan-calismasi]].
   Diğer projeler için sıra kullanıcının önceliğinde.

## 17–18 Eylül'de açılanlar

Sıralı: ilk ikisi Ekim hedefinin ön şartı, üçüncüsü bağımsız.

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

3. **Denetim katmanı yok.** 32 kaynak işaretçisi var, açan kimse yok. Üç
   seviyeli öneri (claude 7f10f7a3 · 17.09 18:29):
   - ~~**Mekanik işaretçi denetimi**~~ **KURULDU 18.09 02:41** — gece
     derleyicisinde. Her işaretçiyi açar, oturum ve damga gerçek mi bakar;
     deseni tutmayanı da "denetlenemedi" diye ayrı raporlar. Negatif testle
     doğrulandı. İlk sonuç: 40 işaretçinin hepsi temiz. Bkz.
     [[gece-derleyicisi]].
   - **Örneklemeli içerik denetimi** — haftada bir, rastgele 3-5 işaretçi;
     temiz bağlamlı ajan iddiayı kayıtla karşılaştırır. Hata oranı yükselirse
     örneklem büyütülür.
   - **Kapanış denetimi** — oturum kapandıktan sonra yazılan notlar omurgaya
     karşı denetlenir. Kullanıcı çekildiğinde onun yerini alan mekanizma.

   **Karar: denetçi rapor eder, düzeltmez.** Düzelten bir denetçi kendi
   düzeltmesini denetletmez; rapor zinciri sonlu, düzeltme zinciri değildir.
   Ayrıca bir iddianın yanlış olduğunu görmek, doğrusunu bilmek demek değildir.

4. **Side chat'ler arşive hiç girmiyor.** Kayıt dosyası oluşmuyor; arama
   bulmuyor, paralel oturum uyarısı görmüyor. Tek taşıma yolu elle aktarma.
   Ölçüm: [[olculmus-bulgular]] §6. Çözüm bilinmiyor — harness tarafında,
   bu vault'un erişemediği bir yer.

5. **Paralelleştirme / mesh — ertelendi** (kullanıcı, 18.09 01:02). Devir
   kutusu mesh'e uygun değil; neden ve ne gerekirdi: [[agentic-yapi]].

## 19 Eylül'de açılanlar

1. **Sağlayıcıdan bağımsızlık.** Beyin tek bir sağlayıcının tek bir
   uygulamasına bağlı kalmamalı. Codex (GPT-5.6, Sol, Astra), ileride çıkacak
   yerel modeller ve Çin modelleri aynı beyni kullanabilmeli (kullanıcı kararı,
   19.09). Bugünkü durum: notlar düz Markdown olduğu için her model okuyabiliyor.
   Arama araçları Codex kayıtlarını da okuyor. **Claude'a bağlı olanlar:**
   `CLAUDE.md` dosya adı (Codex `AGENTS.md` okur, bu klasörde yok), hook'lar ve
   bunların sağladığı otomatik refleksler. Nar Ajans'ta aynı asimetri
   yaşanmıştı: [[iki-ajan-calismasi]].
   **Yapılan (19.09 16:40–17:10, commit `d0bdf11`):** `CLAUDE.md` → `AGENTS.md`
   (ortak kural, git geçmişiyle taşındı). `CLAUDE.md` artık `@AGENTS.md` içe
   aktarması ve Claude'a özel refleks tablosu. İçe aktarma, kayıt bırakmayan
   temiz bir Claude örneğiyle sınandı: iki kuralı da `AGENTS.md`'den okudu.
   Yönerge metni `.claude/`'dan `araclar/oturum-basi.md`'ye taşındı.
   `oturum_basi.py --bicim duz` hook'u olmayan ajan için. İşaretçi denetimi
   `(codex …)` biçimini de tanıyor. **Açık:** Codex adaptörü. Kurulu Codex'te
   hook desteği var (0.150.1, `hooks stable true`); kurulumu Codex'in kendisine
   devredildi (codex 01a0b9eb · 19.09 16:47).
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
4. **İçerik denetimi kararı:** uyuşmazlık bulunursa not düzeltilmez, iddianın
   **altına not düşülür** (kullanıcı, 19.09). Bu, "denetçi rapor eder,
   düzeltmez" kararıyla uyumlu: işaret koyuyor, metni yeniden yazmıyor.

5. **Kalıcı notlar eşiği aştı: 118 KB** (19.09 18:35 ölçümü). `AGENTS.md`
   65 KB'ta "hepsini oku"dan "haritayı oku, gerekeni aç"a geçmeyi söylüyor;
   "Uzun vade" başlığındaki 100 KB bölme eşiği de aşıldı. Karar bekliyor:
   hangi notlar bölünür ya da arşive iner.

## Karar bekleyenler

- Tek ortak hafıza klasörü (`autoMemoryDirectory`) kurulmadı. 30 izole notun
  sorununu çözmez ama yenilerinin dağılmasını durdurur.
- Raspberry Pi alınacak mı? Öneri: almadan önce mevcut makineyi sürekli açık
  bırakıp uzaktan bağlanmayı test et.
- Gelen kutusu (mobilden not düşme) kurulmadı. Uyarı: boşaltılmayan gelen kutusu
  çöplüğe döner; değer yakalamada değil damıtma ritüelinde.

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

## Yapılmamış testler

- `--fork-session` canlı denenmedi
- Ekran kaydı → `izle.py` zinciri gerçek bir ChatGPT kaydıyla test edilmedi

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

## Uzun vade

- Ölçek gerektiğinde sunucuya taşı (şimdiden uğraşma)
- `notlar/` 100 KB'ı geçerse konu notlarını daha da böl; şimdilik gerek yok
