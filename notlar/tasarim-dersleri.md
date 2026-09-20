# Tasarım dersleri

> **20.09 ek ders — denetim verisi de ürünü bozabilir:** Git'in yok saydığı
> test klasörlerini Obsidian yine tarar. Önceki Astra testleri 178 sahte
> BEYIN.md bıraktı. Test fixture'ı artık kasa dışındaki geçici alanda,
> başarı/kurulum hatası/assertion hatasında `addCleanup` ile temizleniyor.
> 28 test geçti, yeni kalıntı 0. Kullanıcı 178 eski klasörü silmeyi onayladı;
> sonraki bağımsız sayımda hedefler ve sahte BEYIN 0, kanıt logları mevcut.
> [[2026-09-20-toparlama-ve-sunum]].
> (codex 01a0bc5c-f1c4 · 20.09 17:35)

Eğitim videolarından çıkarılıp bu projede yaşananlarla sınanmış ilkeler.

> Merkez: [[BEYIN]] · İlgili: [[ikinci-beyin-mimarisi]] · [[kapanis-ritueli]] · [[yasanan-hatalar]]

---

Bu bölüm, izlenen eğitim videolarından (Avenox) çıkarılan derslerin oturumda
yaşananlarla sınanmış hâlidir.

### 5.1 Geri besleme döngüsünün üç parçası

| Parça | Kim sağlar |
|---|---|
| **Aksiyon** — model değişiklik yapar | Model |
| **Ölçüm** — sonuç iyi mi kötü mü | **Kullanıcı / proje** |
| **Dönüş** — sonuç modele ulaşır | Harness *veya* kullanıcı (kopyala-yapıştır) |

Ortadaki parça asla modelden gelmez. Harness sadece üçüncüyü otomatikleştirir.

### 5.2 Ölçümün dört kalite şartı (dördü de bu oturumda ihlal edildi)

1. **Doğru şeyi ölçmeli.** Bir GPU testi "BAŞARILI" dedi ama yalnızca modelin
   *yüklenmesini* deniyordu, çıkarımı hiç çalıştırmadı. Yanlış ölçen gösterge,
   "bilmiyorum"u "iyiyim"e çevirdiği için hiç gösterge olmamasından kötüdür.
2. **Yıkımdan önce gelmeli.** Bir yama script'i dosyayı diske yazdı, *sonra*
   sözdizimini doğruladı. Hasarı önlemedi, rapor etti.
3. **Kırmızı ışık da yalan söyleyebilir.** "ffmpeg kurulu değil" hatası aracın
   değil, testin hatasıydı (`--ffmpeg-location` unutulmuştu).
4. **Sessiz başarı yasak.** `KARE SAYISI: 0` çıktısı iki hatayı yakalattı. Her
   komut ne yaptığını **sayıyla** söylemeli.

### 5.3 Komut mu, doküman mı

- **Yeniden hesaplanabilen** (testler geçiyor mu, ne çalışıyor) → **komut**.
  Doküman olarak yazılırsa bir hafta içinde yalan söyler.
- **Yeniden hesaplanamayan** (neden bu yol seçildi, ne denenip elendi) → **doküman**.

Kural: *ölçülebileni ölç, ölçülemeyeni yaz.*

### 5.4 İkinci beynin dört unsuru

**Sadece biri notları gerçekten tutar:**

| Silinen | Kaybedilen | Notlar durur mu |
|---|---|---|
| Obsidian | Rahat okuma, graph görünümü | ✅ |
| GitHub | Uzak yedek, çok makine | ✅ |
| Git | Geçmiş, geri alma | ✅ |
| mem0 | Anlamsal hatırlama | ✅ |
| **Klasör** | **Her şey** | ❌ |

- **Git** = bilgisayara kurulan program, klasörün geçmişini tutar. İnternet/hesap
  gerekmez. **GitHub** = o geçmişin kopyasını saklayan site.
  `git commit` yerelde kalır, `git push` internete gider.
- **Obsidian** notlar arası bağı sağlar (`[[bağ]]`, backlinks, graph). Ama o bağlar
  **düz metin olarak dosyanın içinde** durur — bağ veride, programda değil.
  Modelin Obsidian'a doğrudan ihtiyacı yok; dosyaları diskten okur.
- **mem0** anlamsal bağ kurar (sen kurmadan). Ama **klasörleri taramaz** —
  konuşmalar sırasında içine yazılanı tutar.

### 5.5 Oturumlar arası bellek — dört katman

```
1. HAM       jsonl — her şey + gömülü görseller, hiç silinmez
2. YOLLAR    PDF/zip için işaretçi — %59 sağlam, kaynaklar/ ile %100
3. ÖZET      oturum başına ~1 sayfa
4. KOLEKTİF  tek dosya, her oturumun başında okunur
```

Özete yazılacaklar, değer sırasıyla: **kararlar + gerekçeleri**, **denenip
elenenler** (en değerlisi), kurulan şeyler, açık uçlar.

### 5.6 Eski oturuma soru sorma ekonomisi

```bash
claude --resume <id>                            # etkileşimli devam
claude -p "soru" --resume <id> --fork-session   # sor, cevabı stdout'a bas
```

`--fork-session` yeni oturum kimliği açar, orijinale dokunmaz. **Ama fork sabit
taban özelliğini ancak atıldığı sürece korur** — aynı fork'a tekrar sorulursa o da
birikir.

| Katman | Maliyet | Soruların ~oranı |
|---|---|---|
| Özet oku | bedava | %90 |
| jsonl'de grep + oku | çok ucuz | %9 |
| Fork + sor | soru başına %60-70 pencere | %1 |

**Bir oturuma devam etmek** tüm bağlamı yüklemektir; **bir oturumu okumak** sadece
ilgili satırları okumaktır. jsonl bir konuşma değil, bir **belgedir**.

> Not: `--fork-session` mekanizması komut düzeyinde doğrulandı (CLI yardımından),
> **canlı test edilmedi.**

---

### 5.7 Kuralı yazmak, kurala uymayı sağlamıyor

16 Eylül oturumunda aynı **sınıf** hata üç kez tekrarlandı ve her seferinde
kuralı yazan kişi tarafından yapıldı:

| Hata | Ne zaman |
|---|---|
| Ölü işaretçi (`memory/...`) | devralındı |
| Ölü işaretçi (`.claude/settings.json`) | kural yazıldıktan **10 dakika** sonra |
| Alt dize eşleşmesi (güven kaydı sayımı) | 08:28 |
| Alt dize eşleşmesi (`.env` kontrolü) | 10:22, **iki saat** sonra |

**Ders:** bir hatayı adlandırmak ona karşı bağışıklık kazandırmıyor. Kural
yazmak ucuz; **kuralı denetleyen bir komut yazmak** pahalı ama tek işleyen yol.
Akşam derleyicisinin varlık sebebi tam olarak budur — ve kurulduğu gün, onu
kuran kişinin yeni yazdığı dosyadaki kırık bağı yakaladı
(claude 3557db3e · 16.09 10:42).

**Yan ders:** yanlış alarm veren bir denetleyici, denetlemeyenden **beterdir**.
`.env` kontrolü her çalışmada yanlış alarm veriyordu; böyle bir kontrol insanı
üçüncü seferde bakmayı bırakmaya iter. Denetleyici de bir iddiadır ve
denetlenmesi gerekir.

### 5.8 "Erişilemez" ile "çöp" aynı şey değil

Bir ölçüm "şu kadar nesne hiçbir ref'ten erişilemiyor" diyorsa, sebebi iki ayrı
şey olabilir: ref **yok**, ya da ref **okunamıyor**. İkisi aynı komutta aynı
görünür, sonuçları zıttır — birincisinde temizlik güvenli, ikincisinde canlı
veriyi siler.

Ölçülen örnek: Windows'un 260 karakter yol sınırı, Codex'in checkpoint
ref'lerini git'e "bozuk" gösteriyordu. `core.longpaths=true` 257 nesneyi
kurtardı; kalan 2.236 gerçekten erişilemezdi. Sebep ayırt edilmeden `gc`
çalıştırılsaydı canlı bir checkpoint silinecekti (claude 3557db3e · 16.09 08:30).

**Genel hâli:** bir sayıyı yorumlamadan önce o sayının **nasıl üretildiğini**
sor. `grep | wc -l` bir ölçüm değildir; neyi saydığını görmeden sayı yazılmaz.
