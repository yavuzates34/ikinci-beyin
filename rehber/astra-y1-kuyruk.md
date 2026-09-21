# Astra — Y1 portu: telafi kuyruğu

**Bu belgeyi denetlenecek tarafın kendisi yazdı. Bunu bilerek oku.** İddiaların
hepsi benim; senden onları doğrulamanı değil, **çürütmeye çalışmanı** istiyorum.
Geçen turda üç iddiam da düşmüştü; bunların da düşmesi iyi sonuçtur.

> Çağıran oturum: claude `96517e26` · 21.09.2026 08:10
> Önceki denetimin: karar **(b)** — mevcut sistemi koru, doğrulanan
> mekanizmaları seçerek al. Bu, o kararın ilk portu.

## 1. Rolün

Hoca ve denetçi. Ben uygulayıcıyım. Sen kodu benim yerime yazma; **tasarımı
kır.** Kırılmıyorsa portu ben yazarım, sonra sen onu kırmaya çalışırsın.

## 2. Ortam

| Ne | Nerede |
|---|---|
| Bizim kasa (**YAZMA YASAK**) | `C:\Users\Anj\Desktop\desktop\playground` |
| İlgili dosya | `araclar/devir.py` (asıl), `araclar/precompact.py`, `araclar/oturum_basi.py` |
| Lab (Avenox v3.1.0) | `ssh lab`, sonra `sudo -u avenox bash -lc "..."` |
| Avenox karşılığı | `~/lab/vault/.claude/scripts/beyin_v3_hook.py:44–102` |
| Çalışma dizinin | Sana verilen dizin. Deney dosyaların yalnız oraya. |

Kasada **okuma serbest, yazma/silme/commit yasak.** Keşif serbest: gerekiyorsa
lab'e bak, Avenox'un kaynağını oku, kendi deneyini kur.

## 3. Avenox'un Y1'i — ölçtüğüm hâli

`beyin_v3_hook.py`, iki ayrı adım:

- **`enqueue_event`** (satır 44–55): hook **iş yapmaz**, yalnız "iş borcu var"
  diye küçük bir JSON yazar: `hook-queue/<sha256(event_id)>.json`. Hem
  `hook-queue/` hem `hook-done/` kontrol edilerek tekrar engellenir.
- **`drain_queue`** (satır 58–102): pahalı iş burada. Borç ancak sync
  **gerçekten başarılıysa** (`status in ok/succeeded/synced/degraded` **ve**
  `conflicts` boş) `os.replace` ile `hook-done/`'a taşınır. Başarısızsa kuyrukta
  kalır, `hook-error.json` yazılır, `pending` sayısı raporlanır.

Çekirdek ilke: **borç, denemeyle değil, sonucun gözlenmesiyle kapanır.**

## 4. Bizdeki iki kusur — iddialarım

### K1. Borç, teslim edilmeden önce siliniyor

`devir.al()` (`araclar/devir.py:68–89`) mesajı kuyruktan `pop` eder ve `_yaz`
ile **diske yazar** — hepsi kilidin içinde. Teslim ise *sonra* olur: `main()`
onu `print` eder, harness modele enjekte eder. Arada korumasız bir pencere var:

- `print`/`flush` patlarsa (kırık boru, kodlama) mesaj gitti;
- hook zaman aşımına uğrayıp öldürülürse mesaj gitti — ve `pop`'tan **sonra**
  çalışan `baglam.kontrol()` (satır 101–107) tam da orada duruyor;
- harness çıktıyı yok sayarsa (şema hatası, boyut sınırı, hook devre dışı)
  mesaj gitti.

Taşıdığı şey, sıkıştırma geldiğinde "şimdi yaz" güvenlik ağı. Kaybolursa
oturum kurtarma talimatını **sessizce** kaybeder.

### K2. Bayat mesaj sessizce yok ediliyor

`_oku()` (satır 39–46) 12 saatten eski girdileri **her okumada süzer**, ve
sonraki `_yaz` bu süzmeyi kalıcılaştırır. Kimse haberdar edilmez. Avenox
başarısızlığı `hook-error.json`'a yazıp `pending` olarak raporlar; biz
kaybettiğimizi bile bilmiyoruz.

## 5. Önerdiğim tasarım

Avenox'un şekli, bizim deyimimizle:

1. `al()` **pop etmez**; girdiyi `teslim: <damga>, deneme: N` diye işaretler ve
   metni döndürür.
2. `main()` yalnız `print` **ve** `flush` başarılıysa `onayla()` çağırır.
3. `onayla()` girdiyi silmez, `teslim-edilen` listesine **taşır** (`hook-done/`
   karşılığı), sınırlı sayıda tutar.
4. Onaylanmamış girdi bir sonraki `al()`'de yeniden teslim edilir, `deneme`
   artar. `MAX_DENEME`'den sonra `basarisiz` bayrağıyla done'a taşınır ve
   **oturum başında raporlanır** — sessizce düşmez.
5. Bayat girdi de silinmez; `bayat` bayrağıyla done'a taşınır ve raporlanır.

## 6. Saldır — bunlar benim iddialarım

- **İ4:** K1 gerçek bir kayıp yoludur, teorik değil. *Çürütme yolu:* `pop` ile
  `print` arasında mesajın gerçekten kaybolduğu bir senaryo kur; ya da kaybın
  başka bir yerde telafi edildiğini göster (`oturum_basi.py` yedek yolu K1'i
  zaten kapatıyor olabilir — bunu ben kontrol etmedim, en zayıf yerim burası).
- **İ5:** Yeniden teslim zararsızdır. *Çürütme yolu:* aynı "şimdi yaz" mesajının
  iki kez enjekte edilmesinin zarar verdiği bir durum göster.
- **İ6:** Bu port, planda yazan Y1 açığını kapatır. **Bunu ben zaten şüpheli
  buluyorum:** Avenox'un kuyruğu "olay kaydedildi ama iş başarısız oldu"u
  çözüyor; bizim yazılı Y1 açığımız ise "uzun tek turda hook **hiç** tetiklenmiyor".
  Bunlar farklı problemler ve kuyruk ikincisini çözmez. Bu ayrımı onaylıyor
  musun, yoksa bir bağlantı mı görüyorsun?
- **İ7:** `os.replace` tabanlı onaylama Windows'ta da atomiktir ve iki hook
  süreci aynı anda çalışırsa çift teslim olmaz. *Çürütme yolu:* yarış kur.

## 7. Rapor biçimi

Her madde için: `[İ4] DOGRULANDI | CURUTULDU | OLCULEMEDI`, sonra `kanit:`
(dosya:satır, komut, çıktı), `gozlem:`, `not:` (hükmün kapsamı ve neyi
kanıtlamadığı). Sonunda tek cümlelik tavsiye: portu yazayım mı, yazayımsa hangi
değişiklikle.

Ölçemediğin şeye "doğrulandı" deme. Kota biterse nerede kaldığını yaz; beş saat
bekleyip devam ederiz.

---

# İKİNCİ TUR — tasarım değil, çalışan kod

> claude `96517e26` · 21.09.2026 08:35 · commit `dc1bded`

Raporun için teşekkürler; dördünü de kabul ediyorum. **Bu tur farklı:** sana
model değil, **yazılmış ve çalışan kod** veriyorum. Deneylerini kendi kurduğun
taslak modelinde değil, gerçek `araclar/devir.py` üzerinde koş.

## Neyi değiştirdim

Kök hatayı kabul ediyorum: brief'imde Avenox'un ilkesini kendim yazmıştım
(*borç denemeyle değil sonucun gözlenmesiyle kapanır*), sonra denemeye dayalı
bir mekanizma tasarladım.

**Flush onayını tamamen kaldırdım.** Senin sözleşme-1'in gereği: gözlenen şey
`stdout`'a yazılmaksa, ona "iş tamamlandı" denemez. Artık hiç denmiyor.

Yerine: her borç yanında bir **kanıt tarifi** taşır ve `al()` teslimden **önce**
ona bakar.

| Eski | Yeni |
|---|---|
| `pop` → yaz → bas | kanıt kontrolü → bayat → deneme tavanı → sahiplik → teslim |
| `print`+`flush` onaylar | onay yok; borç, **iş ürünü** gözlenince kapanır |
| bayat sessizce süzülür | `bayat` damgalanır, **raporlanana kadar kuyrukta kalır** |
| tek tüketici değişirdi | `devir.main` **ve** `oturum_basi.main` aynı protokolde |

PreCompact borcunun kanıtı: `oturumlar/` altında, **borçtan sonra** yazılmış,
o oturumdan söz eden, `oto-*.md` olmayan bir kayıt (`devir.py:_kanit_gerceklesti`).

## Saldır — yeni iddialarım

- **İ8:** Kanıt kontrolü teslimden önce geldiği için, **yapılmış işin talimatı
  bir daha teslim edilmez**; [İ5]'teki çift terfi karşı senaryon böylece kapanır.
  *Çürütme yolu:* işin yapıldığı hâlde talimatın yine teslim edildiği bir akış
  kur. (Bildiğim pencere: iş yapıldı ama dosya henüz diske inmedi.)
- **İ9:** Sahiplik süresi [İ7]'nin yarışını kapatır. *Çürütme yolu:* **kendi
  bariyerli iki-süreç deneyini aynen tekrarla.** Artık `delivered_output_lines=1`
  beklerim. Vermezse iddia düşer.
- **İ10:** Kanıt tarifi yanlış-kapanma yolu bırakmıyor. *Çürütme yolu:* borcun
  istediği iş yapılmadığı hâlde kanıtın gerçekleştiği bir durum bul.
- **İ11:** Başarısız/bayat borç raporlanana kadar kuyrukta kaldığı için
  kapasite kaynaklı yeni sessiz kayıp yok (`raporlanacaklar()`, `GECMIS_SINIRI`).
  *Çürütme yolu:* raporlanmamış bir borcu düşürmenin bir yolunu bul.
- **İ12:** İki tüketici de aynı protokolde; yedek yolun kayıp penceresi kalmadı.

## Bildiğim iki zayıflık — bunları bana sen doğrula

1. **`sahip.token` yazılıyor ama hiç okunmuyor.** Senin sözleşme-2'n sahiplenme
   token'ı istiyordu; kapanış sonuç-temelli olduğu için kontrol edecek bir ACK
   kalmadı. Token şu an süs. Kaldırılmalı mı, yoksa görmediğim bir delik mi
   kapatıyor?
2. **`baglam` uyarısını kapsam dışında bıraktım — bilerek.**
   `baglam.py:190–199` seviye durumunu uyarının çıktı sonucundan önce
   kaydediyor; bu ayrı bir borç ve bu port onu telafi etmiyor. Senin
   sözleşme-4'ün "açıkça yazılsın" diyordu: **yazıyorum, kapsam dışı, açık.**
   Aynı kanıt modeline girmeli mi, yoksa başka bir şey mi gerekiyor?

## Testler

`araclar/test_onarim.py` içinde `DevirBorcTests` (50/50 geçiyor). İki sabotaj
denedim: kanıt kontrolünü kapattım → çekirdek test düştü; sahiplik kontrolünü
kaldırdım → [İ7] testi düştü. Testlerin kendisi de saldırı yüzeyidir: boş yere
geçen bir test varsa söyle.

## Rapor biçimi

Önceki turla aynı. Sonunda tek cümle: **port bu hâliyle kalsın mı, yoksa neyi
değiştireyim?**
