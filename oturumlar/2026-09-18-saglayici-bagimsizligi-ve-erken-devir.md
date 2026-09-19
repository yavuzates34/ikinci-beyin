# Sağlayıcı bağımsızlığı, erken devir ve sunum onarımı — 18.09.2026 04:37 – 20.09.2026 00:40

kapanan-oturum: 5c600e7e, 01a0b9eb-e0f9, 01a0baa5-a350, 01a0bb8e-4631

**25 kullanıcı mesajı, 5.455 KB ham kayıt.** Takvim süresi 44 saat; içinde uzun
uyku araları var. Üç iş kolu: sistem envanteri, sağlayıcıdan bağımsız çekirdek,
sunum ve onarım turu. Kapanış omurga okunarak yazıldı
(`python araclar/omurga.py 5c600e7e`).

> Merkez: [[BEYIN]] · İlgili: [[sunum-incelemesi-onarim-listesi]] ·
> [[kapanis-ritueli]] · [[gece-derleyicisi]] · [[iki-ajan-calismasi]] ·
> [[olculmus-bulgular]] · [[acik-uclar]]

---

## 1. Envanter ve soru-cevap (18.09 04:37 – 19.09 08:25)

Kullanıcı sistemin ne yaptığını ve ne yapmadığını liste hâlinde istedi, sonra
her maddeye tek tek reply verdi. Bu turda düzeltilenler:

- **Arayüz "gidip geldi" olayı:** masaüstü uygulamasının sessiz güncellemesi
  (2.2553.0 → .1), oturum kaydında iz bırakmıyor. [[olculmus-bulgular]] §9.
- **Omurga mesaj sayıları şişkindi:** skill metinleri (`isMeta`) ve
  "[Request interrupted by user]" işaretleri kullanıcı mesajı sayılıyordu.
  Eski arşiv sayıları düzeltilmedi, altlarına denetim notu düşüldü §10.
- Kullanıcının düzeltmesi: "uyuduğunu hook'tan bildim" yanlıştı; hook yalnızca
  saati veriyor.

## 2. Sağlayıcıdan bağımsız çekirdek (19.09 16:29 – 17:30)

Kullanıcının tezi: beyin bir altyapıdır, tek bir sağlayıcının tek bir
uygulamasına bağlı olamaz. Yapılanlar:

- `CLAUDE.md` → **`AGENTS.md`** (ortak kural). `CLAUDE.md` artık içe aktarım +
  Claude'a özel refleks tablosu. Temiz bir Claude örneğiyle sınandı.
- **`kapanan-oturum:`** satırı: kapanışın tek kaynağı. Dedektör ve oturum başı
  uyarısı buna bakıyor.
- **Codex adaptörünü Codex'in kendisi kurdu ve ölçtü** (`01a0b9eb`).
- `kayit.py`: Codex kayıtlarındaki enjeksiyon blokları, `archived_sessions/`
  klasörü, kimlik kaynağı.

## 3. Sunum, sesli inceleme ve onarım turu (19.09 17:35 – 20.09 00:40)

14 slaytlık kullanım rehberi yazıldı ve yayınlandı; Codex'le sesli incelendi
(`01a0ba53`, `01a0ba74`), 13 açık çıktı. Bu oturumda ortak onarım turu yapıldı;
iki açık daha bulundu (14 ve 15). Durum tablosu:
[[sunum-incelemesi-onarim-listesi]].

Kurulanlar: `baglam.py` (erken devir), `bakim.py` (budama adayları),
`gece_kayit.py` genişletmeleri, `rehber/uygulama-adaptorleri.md`,
`rehber/astra-kontrol.md`.

## Kararlar ve nedenleri

- **Erken devir eşiği %50 ve %70** (kullanıcı). Uyarı tur sınırında gelir,
  eşik başına bir kez; omurga diske alınır. Gerekçe: Codex Desktop bağlam
  sayacı göstermiyor, yani "kullanıcı görür ve kapatır" varsayımı her
  uygulamada geçerli değil.
- **Kapanış onayı insana aittir.** Otomasyon riski fark eder ve hazırlığı
  başlatır; oturumun bittiğine dair semantik kararı vermez. İleride yetkili
  orkestratör ajan da onay verebilir (kullanıcı, 19.09).
- **Budama: derleyici aday raporlar, taşımayı insan onaylar.** Otomatik silme
  yok; tarihçe `oturumlar/` altına iner. Kullanıcı dört taşımadan ikisini
  onayladı.
- **Adaptör sağlayıcıya değil uygulamaya göre kurulur.** Hook bir modelin
  değil, harness'ın yeteneğidir.
- **Kısa kimlik kaynağa göre:** Codex'te 13 hane, Claude'da 8. Kapanış
  eşleşmesi önek tabanlı.

## Denenip elenenler

- **`SessionEnd` hook'u ile işaret bırakmak — elendi.** `kapanan-oturum:`
  geldiğinden beri dedektörün kendisi işaret; çökme de böyle yakalanıyor.
  Yerine gece taslağı kuruldu.
- **Compact uyarısına omurga yolu eklemek — gereksiz çıktı.** Kod okununca
  mesajın bunu zaten verdiği görüldü.
- **"Codex Desktop'ta hook'lar çalışıyor" sonucu — geri alındı.** Ekran
  görüntüsü ve modelin ifadesi kanıt sayılmıştı; ham kayıtta satırların tipi
  `custom_tool_call_output` çıktı. [[olculmus-bulgular]] §14.
- **Skill listesini kısaltmak — gereksiz.** Zaten yalnızca ad ve açıklama
  yükleniyor; asıl maliyet kullanılmayan eklentiler.

## Kapanışta yapılan son üç ölçüm (20.09 00:45–00:50)

- **Madde 12 kapandı.** Gece zinciri gerçek koşulda uçtan uca çalıştı: aday
  seçimi, model çağrısı, `oturumlar/oto-01a0bb8e-de58.md`, oturum başı uyarısı
  ve taslaktaki işaretçilerin denetimi (82/82 temiz).
- **Madde 14 kapandı.** Mükerrer oturum elemesi eklendi: aynı kaynak ve aynı
  tam kimlik iki dosyadaysa en büyüğü tutulur. 6 grup elendi, 213 → 207 oturum.
- **Madde 5'in sebebi bulundu.** `codex exec` normalde bağlam vermiyor;
  `--dangerously-bypass-hook-trust` ile bağlam anında geliyor. Adaptör doğru,
  eksik olan **güven kaydı**. Kullanıcı `codex` TUI'sinde `/hooks` ile verecek.
  Güven yokken hook'lar **sessizce** atlanıyor; hiçbir uyarı çıkmıyor.
  [[olculmus-bulgular]] §14.1.

## Açık kalanlar

- **Codex hook güveni** (madde 5): kullanıcı işlemi. Sonrasında Desktop ve
  `exec` ölçülecek.
- **Erken devirin Codex tarafı** (madde 7): mekanizma hazır, taşıyıcı güvene
  bağlı.
- **Kalıcı katman 100 KB üstünde** (madde 10): kullanıcı iki taşımayı
  onaylamadı, karar onun.
- **Astra turu:** üçüncü göz denetimi `rehber/astra-kontrol.md` ile bekliyor.

## Ölçümler

| Ne | Değer |
|---|---|
| Codex arşiv görünürlüğü | 103 → 164 oturum (`archived_sessions/`) |
| İlk-8 kimlik çakışması | 213 oturumda 24 grup, biri dört oturumluk |
| Kalıcı katman | 137,9 → 125,4 KB (bir taşıma), gün sonunda 134 KB |
| İşaretçi denetimi | 80/80 temiz |
| Erken devir | %50 (19.09 20:31) ve %70 (20.09 00:36) canlı |
| Gece taslağı sınaması | 103 saniye, 7 KB, 18/18 işaretçi gerçek |
| Gece zinciri (gerçek koşul) | aday 1, taslak 2 KB, 82/82 işaretçi |
| Mükerrer eleme | 6 grup, 213 → 207 oturum |
| Hook güven teşhisi | güven atlatılınca bağlam anında geldi |
