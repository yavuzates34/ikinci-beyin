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

1. **`SessionEnd` hook'u yok — kapanışsız oturum iz bırakmıyor.** Kapatılmadan
   bırakılan oturumdan kalıcı katmana hiçbir şey geçmiyor. Karar verildi, kurgu
   belli: *işareti ölen bant bıraksın, notu yaşayan bant yazsın.* Kurulmadı.
   Tasarım ve elenen alternatif: [[kapanis-ritueli]].

2. **Omurga model tarafını taşımıyor.** Sadece kullanıcı mesajlarını çıkarıyor;
   ölçümler, elenen fikirler, gerekçeler ham kayıtta kalıyor. Madde 1'in ön
   şartı — zenginleştirilmeden temiz örnek eksik malzemeyle yazar.
   **Ek kusur (18.09):** `omurga.py` skill yüklemelerini kullanıcı mesajı
   sanıyor. Bu oturumun omurgasında `claude-api` skill'inin tamamı bir
   "kullanıcı mesajı" olarak göründü ve 128 KB'lık omurganın önemli kısmını
   doldurdu. Filtrelenmeli.

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
