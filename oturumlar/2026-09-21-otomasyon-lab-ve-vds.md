# Tam otomasyon, lab kararı ve VDS — 20–21 Eylül 2026

**Ara kayıt. Oturum kapanmadı.** Bağlam 21.09 02:42'de *elle* sıkıştırıldı
(`/compact`, PreCompact tetiklendi). `kapanan-oturum:` satırı bilerek yoktur:
oturum bitmedi, sadece sıkıştı. Konuşma aynı oturumda sürüyor.

Oturum kimliği: `96517e26-5948-4d47-8014-6e69edc7d0c3` (claude).
Sıkıştırma öncesi omurga diske alındı:
`derleme/omurga-anlik/2026-09-21-024230-463898-96517e26-…md`
(41 kullanıcı mesajı, 19,5 KB). Sıkıştırmadan etkilenmedi; bu kaydın
kaynağı odur.

> Merkez: [[BEYIN]] · İş belgesi: [[2026-09-21-tam-otomasyon-plani]] ·
> İlgili: [[acik-uclar]] · [[olculmus-bulgular]] · [[agentic-yapi]] ·
> [[astra-denetim-bulgulari]] · [[2026-09-19-sunum-onarim-listesi]]

---

## Oturumun seyri

Üç evre: (1) Astra'nın yarıda kalan turlarını **salt okunur** denetlemek,
(2) tam otomasyon tasarımını konuşmak, (3) lab ve sunucu kararı.

### 1. Salt okunur denetimler

Kullanıcı iki kez, Astra kullanım limitine takıldığı için, "sadece okuma yap,
hiçbir şey değiştirme" diyerek durum raporu istedi. Okunanlar: gece görevi
ölçümü, test kirliliği kaynağı (`araclar/test_onarim.py`), Obsidian grafik
patlaması, sunum kaynağı, commit geçmişi.

Sonuç: Astra'nın işi doğrulandı — 10 commit, temiz ağaç, 83/83 işaretçi,
1 `BEYIN.md`, 0 test klasörü, 7 kanıt logu korunmuş, sunum sağlayıcı
bağımsızlığı teziyle yeniden yazılmış ve "ölçülmedi" sınırları dürüstçe
etiketlenmiş.

**Benim iki yanlış iddiam ve düzeltmeleri** (ders olarak kalsın):

- *"Gece görevinde git commit + push adımı hiç çalışmadı."* **Yanlış.**
  `git show --format=fuller --stat 67779e9` → `AuthorDate: Sun Sep 20
  00:30:05 2026`. Commit çalıştı; çalışmayan sadece log satırı ve tamamlanma
  işaretiydi. Kurduğum nedensellik de yanlıştı: commit'lenmemiş 11 dosya
  00:45–01:39 arasında değişmişti, yani commit'ten *sonra*.
- *"Derleme saniyeler sürer, süre sınırına takılmaz."* **Ölçmeden söyledim.**
  Astra çürüttü: 3 aday × model çağrısı başına 900 s bütçe, 15 dakikalık
  pencereye karşı.

İkisini de Astra yakaladı. Proje kuralı gereği (*denetçi rapor eder,
düzeltmez*) iddianın altına not düştü, metni yeniden yazmadı.
(claude 96517e26 · 21.09 02:48)

### 2. Tam otomasyon kararı

Kullanıcının gerekçesi ve tasarımın tamamı ayrı iş belgesinde:
[[2026-09-21-tam-otomasyon-plani]]. Burada yalnız kararın kendisi durur.

Kullanıcı 20.09 20:28'de sistemin **tam otomatik** olmasına karar verdi.
Kapanış ritüelinin tetikleyicisi (kullanıcının "kapatalım" demesi) bu hedefle
çelişiyor; yerine **eşik ritüeli** gelecek. Karar gerekçesi: sistem
uygulamanın arayüzünde oturum açıp kapatamaz — bu harness yeteneğidir, model
yeteneği değil.

### 3. Lab ve sunucu

- **Lab kararı (kullanıcı, 21.09).** Avenox'un (Taha) v2 ikinci beyin sistemi,
  bizim kasadan **tamamen ayrı bir vault ve ayrı bir git deposunda**
  incelenecek. Karışma yasak. Laboratuvarda oynayan Claude olacak.
  Egemenlik kuralı lab'lar için esnetilebilir (kullanıcı kararı).
- **Sunucu kararı.** Lab lokal sanal makine yerine kiralık sunucuda kurulacak.
  AltunHOST araştırıldı: aynı özelliklerde **VDS, VPS'ten ucuza yenileniyor**
  (VPS-3 yenileme 161,36 ₺ / VDS-3 134,61 ₺) ve üstüne ayrılmış RAM, DDR4 ECC,
  adı verilen veri merkezi geliyor. Kullanıcı **VDS-4**'ü alıyor:
  4 çekirdek / 6 GB DDR4 ECC / 90 GB NVMe, 185,86 ₺/ay.
  (claude 96517e26 · 21.09 01:05, 01:16)
- **İşletim sistemi: Ubuntu 24.04 LTS 64 Bit.** Sağlayıcının listesindeki en
  yeni Ubuntu LTS bu; 26.04 sunulmuyor, en yeni Debian ise 12. Server sürümü,
  masaüstü değil. Gerekçe: Python 3.12 hazır gelir (Avenox kurulumunun
  ihtiyacı), Node tabanlı CLI ajanları için en iyi desteklenen taban.
- **Sınır:** IP ve SSH kullanıcı adı bana verilecek, giriş **anahtarla**
  kurulacak. Parola, panel girişi, ödeme bilgisi bana gelmeyecek.

## Kaynak işaretçisi ve devir

Bu oturumun asıl çıktısı [[2026-09-21-tam-otomasyon-plani]] ve
[[acik-uclar]] madde 7'dir; ikisi de `04c43e9` ile commit'lendi ve push
edildi. Plan belgesi Astra'ya devredilecek işin kaynağıdır.

## Açık kalan

- VDS kurulumu bekleniyor; kurulumdan sonraki ilk iş **ölçüm** (gecikme, disk,
  RAM gerçekten ayrılmış mı, çalışma süresi), sonra lab kurulumu.
- `notlar/` 130,4 KB — 100 KB bölme eşiğinin üstünde. Budama planı
  [[kalici-katman-bakim-plani]] içinde, **onay bekliyor**. Silme yok; tarihçe
  `oturumlar/` altına taşınır.
- Sıkıştırma sonrası `oturum_basi.py` kaynak ayrımı yapmıyor: `source` bilgisi
  okunmadığı için sıkıştırma sonrası da jenerik harita bloğu geliyor,
  "kaldığın yer" değil. Bu turda BEYIN'deki "sıradaki iş" notu bu boşluğu
  kapattı; kalıcı çözüm plan belgesinde.
