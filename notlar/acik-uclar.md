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
