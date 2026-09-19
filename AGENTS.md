# playground

Burası deneme alanı: her şey serbest, bozulursa sorun değil.
Kalıcı/üretim kodu beklentisi yok — hızlı denemeler, öğrenme amaçlı projeler.

Aynı zamanda bir ikinci beyin denemesi: oturumlar yenilenir, taşıdığı bilgi kalır.
Giriş ve harita `BEYIN.md` içinde — **her oturumda önce o okunur.**

## Bu dosya kimin için

**Burada çalışan her ajan için ortak kural dosyası.** Claude, Codex (GPT-5.6
Sol, Astra) ya da ileride gelecek başka bir model fark etmez. Beyin tek bir
sağlayıcıya bağlı değildir (kullanıcı kararı, 19.09.2026). Ajana özel olan şey
ayrı dosyada durur: `CLAUDE.md` Claude'a, `AGENTS.override.md` (varsa) Codex'e.
Aynı kuralın iki kopyası tutulmaz, bir gün birbirinden ayrılırlar.

**Oturum başı bağlamı.** Hook'u olan ajana otomatik gelir. Gelmediyse ilk iş:

```
python araclar/oturum_basi.py --bicim duz
```

Bu komut haritanın özetini, kapanmamış oturumları ve gece derleyicisinin
uyarılarını basar. Hook'lu ajanlar da aynı betiği çağırır; metin tek yerde
üretilir.

## Zaman

Cevap vermeden önce güncel tarih ve saati kontrol et (PowerShell: `Get-Date`).
Oturum başında verilen tarih bayatlar — bir oturum günlerce açık kalabiliyor ve
konuşma bana kesintisiz görünür. "Bugün", "dün", "sabah" gibi ifadeleri kendi
akışıma göre değil, kullanıcının takvimine göre kullan.

## Klasör düzeni

| Klasör | Ne var | Ne zaman okunur |
|---|---|---|
| `BEYIN.md` | Giriş ve harita | Her oturumda, ilk |
| `notlar/` | Kalıcı katman, konuya göre | Her oturumda, gerekeni |
| `oturumlar/` | Arşiv, oturum başına kayıt | Sorulunca |
| `araclar/` | Python araçları | — |
| `dinleme/` | Sesli dinleme dosyaları | — |
| `derleme/` | Akşam derleyicisi çıktısı | — |

**Boyut eşiği:** `notlar/` toplamı **65 KB**'ı geçerse "hepsini oku"dan
"haritayı oku, gerekeni aç"a geç. Haftalık derleme bu eşiği ölçüp raporluyor.

## Arşivde arama

Bir şeyin daha önce konuşulup konuşulmadığından emin değilsen **tahmin etme, ara.**
Claude ve Codex arşivinin tamamı, ~10 saniye:

```
python araclar/ara.py "terim"                    # sözcüksel
python araclar/anlam.py "tarif" --kapsam proje   # kelimeyi hatırlamıyorsan
python araclar/oku.py <oturum-id> --saat 14:00-14:30
```

## Oturum kapanışı

"Oturumu kapatalım" / "yeni oturuma geçelim" dediğimde şu sırayı izle.

**1. Önce oku, sonra yaz.** Kapanış anı, bu iş için en kötü halinde olduğun andır:
bağlam dolu, oturumun başı en uzakta. Özet yazmadan önce omurgayı oku:

```
python araclar/omurga.py <oturum-id>
```

Kimliği mutlaka ver. Argümansız çağrı "en son yazılan kaydı" seçer; iki oturum
açıkken yanlış oturumu okur.

Bu, bu oturumun kaydından sadece kullanıcının gerçek mesajlarını, zaman
damgalarıyla ve kronolojik sırada çıkarır. Kayıt zaten diskte duruyor; kapanış
**hatırlamaya değil okumaya** dayanmalı.

**2. İki çıktı yaz.**

- **Arşiv:** `oturumlar/YYYY-AA-GG-kisa-ad.md` — bu oturumun kendi kaydı.
  Ne konuşuldu, ne yapıldı, hangi sırayla. Başlığın hemen altına **kapanış
  işareti** yazılır:

  ```
  kapanan-oturum: 5c600e7e
  ```

  Bir oturumun kapandığını söyleyen **tek** kaynak budur. Gece derleyicisi ve
  oturum başı uyarısı buna bakar. Kimliğin başka bir notta geçmesi kapandı
  demek değildir. Compact sonrası yazılan ara kayıtta bu satır yazılmaz,
  çünkü oturum bitmemiştir. Bu oturumun başka bir ajana devrettiği alt görev
  oturumları (örneğin `codex exec`) aynı satıra eklenir, çünkü onların
  kapanışı çağıran oturumun kaydıdır: `kapanan-oturum: 5c600e7e, 01a0b9eb`.

  **Gece taslakları.** Kapanışsız kalan ve 6 saattir sessiz olan oturuma gece
  derleyicisi temiz bağlamla bir taslak yazdırır: `oturumlar/oto-<id8>.md`.
  Taslak kapanış **değildir**: kalıcı notlara terfi etmez, `kapanan-oturum:`
  yazmaz, haritaya girmez. Oturum başında "GECE TASLAĞI VAR" uyarısı görülürse
  kullanıcıya söylenir ve birlikte şu yapılır: taslak omurgaya karşı okunur,
  terfi önerileri ilgili notlara işlenir, dosya gerçek arşiv adına
  (`YYYY-AA-GG-kisa-ad.md`) çevrilir, `oto-kayit:` satırı silinir,
  `kapanan-oturum:` yazılır. Taslaktaki işaretçileri gece denetimi de açar.
- **Terfi:** kalıcı olan `notlar/` içindeki ilgili konu notuna taşınır. Yeni bir
  konu çıktıysa yeni not açılır ve `BEYIN.md` haritasına satır eklenir.

Ne yazacağın, ne kadar yazacağın senin o anki kararın — proje dallanmışsa kapanış
da ona göre şekillenir. Sabit şablon yok; zorunlu başlık boş başlık üretir.
Sadece şu üçü, konu ne olursa olsun, cevapsız kalmasın:

- hangi kararlar alındı ve **neden** — karar yeniden hesaplanamaz, kod okunur karar okunmaz
- ne denendi ve **elendi** — en pahalı bilgi, çünkü elenen şey hiçbir yerde iz bırakmaz
- ne **açık kaldı** — bir sonraki oturumun tutacağı yer

**3. Kaynak göster.** Kalıcı notlardaki **ölçüm, karar ve elenen fikirler**
işaretçi taşır: `(claude 3557db3e · 08.09 17:34)` ya da `(codex <8 hane> · ...)`. İşaretçi doğrudan komuta
çevrilir, yani iddia denetlenebilir olur. Genel anlatım işaretçi taşımaz.

*Hatırlayan bir sistemin en tehlikeli hali, uydurduğunu hatırlıyor sanmasıdır.*

**4. Mekanik bakım.** Yargı istemez, tam da bu yüzden atlanır:

- `BEYIN.md` içindeki "Son güncelleme" satırını **tarih ve saatle** güncelle
  (`Get-Date` ile bak; saatsiz tarih hangi oturumun yazdığını belirsiz bırakır)
- yeni dosya açıldıysa `BEYIN.md` haritasına satır ekle
- bağları kur (`[[dosya-adi]]` — uzantı ve klasör yazılmaz), iki yönlü olsun
- kapanan açık uçları [[acik-uclar]] listesinden düş

**İstisna:** `dinleme/` içindeki dosyalara bağ **yazılmaz** — köşeli parantezler
seslendirmede gürültü yapar. Bunlar haritada listelenir ama içleri bağsız kalır.
