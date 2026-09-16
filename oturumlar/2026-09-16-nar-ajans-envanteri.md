# Nar Ajans çalışma alanı — envanter ve ilk kararlar

**16 Eylül 2026, 04:00–04:45.** Oturum `3557db3e` içinde açılan ikinci iş kolu.
Amaç: `C:\Users\Anj\Desktop\Nar Ajans - Codex` klasörünü düzenlemek ve oraya
playground'dakine benzer, ama kendi koşullarına uygun bir hafıza kurmak.

Bu dosya **ölçüm kaydıdır.** Nar Ajans'ın kendi beyni kurulduğunda buradaki
kalıcı bulgular oraya terfi eder; bu dosya arşivde kalır.

## Neden ayrı bir iş kolu

Kullanıcı üç şeyi baştan kararlaştırdı (16.09 04:00–04:07):

1. **Federe hafıza.** Merkezde iş hafızası, her alt projede kendi küçük notu.
   Tek merkezi hafıza elendi: `fuar-takvimi-api`'nin hafızası ile Nar Ajans'ın
   iş hafızası aynı şey değil.
2. **İş bölümü.** Claude kendi tarafını kurar (hook'lar, `CLAUDE.md`), Codex'in
   tarafını **onun yerine kurmaz** — Codex'e devir notu bırakılır, kullanıcı
   Codex'i açıp kendi düzenlemesini ona yaptırır.
3. **Yedeksiz adım yok.** Envanter ve yedek çıkmadan tek dosya oynatılmaz.

## Ölçülen durum

**Kök dizin git deposu değil.** 4.9 GB, ~17.000 dosya, 17 öğe. İçinde 6 git
deposu var:

| Depo | Durum |
|---|---|
| `fuar-takvimi-api` | Gerçek depo, GitHub uzaklı, temiz, `main` |
| `nar-ajans` | Gerçek depo, GitHub uzaklı, **`agent/add-site-images` dalında**, 4 takipsiz |
| `Staffing-imgs` | Gerçek depo, GitHub uzaklı, 6 takipsiz |
| `Instantly` | Commit yok, dal yok. 105 nesne, 2.6 MB |
| `Instantly/Katılımcı-listeleri` | Commit yok, dal yok. **2.558 nesne, 171 MB.** İç içe depo |
| `NAR - Sözleşme Oluşturma` | Boş depo, **klasörün kendisi de tamamen boş** |

**Bu üç "boş" depoyu kullanıcı açmamış — Codex açmış.** Kanıt: hepsinde
`refs/codex/turn-diffs/checkpoints/<sha>/...` ref'leri var, `refs/heads` boş.
Codex her turun anlık görüntüsünü oraya yazıyor. Codex'in kendi incelemesi
`Instantly/.git` içinde **16 aday kök ağaç** buldu (blob=66, tree=39);
`TODAY-CHECKLIST.md` → `TODAY-CHECKLIST-GUNCEL.md` geçişi ve CSV'lerin gelip
gitmesi o görüntülerde izlenebiliyor (codex 01a0a7d7 · 16.09 04:35).

**Düzeltme kaydı:** ilk okumada bu depolara "terk edilmiş `git init`, boş kabuk,
silinse kaybı yok" demiştim ve kullanıcının onayını o yanlış bilgiyle aldım.
Yedek doğrulaması sırasında ortaya çıktı, uygulanmadan önce düzeltildi
(claude 3557db3e · 16.09 04:27). **Ders:** commit yokluğu deponun boş olduğunu
göstermez; `refs/` altına bakmadan "boş" denmez.

**Hacim metinde değil ikili dosyalarda.** Instantly 1.6 GB (neredeyse tamamı
`Katılımcı-listeleri`), nar-ajans 1.4 GB, Kataloglar 1.1 GB, codex-backups
620 MB. Buna karşılık **bilgi katmanı toplam ~400 KB markdown.**

**Canlılık (son değişiklik tarihine göre):** Instantly, Kataloglar,
codex-backups 15 Eylül; Staffing-imgs 10 Eylül; Kartvizit 8 Eylül. Ağustos'ta
donmuşlar: nar-ajans (19.08), fuar-takvimi-api (20.08), google-workspace-tools
(27.08), Logolar (27.08), design-source (06.08).

**Disk:** C: sürücüsünde **11.5 GB boş** (222 GB'ın %5'i). Ayrı bir konu ama
yedekleme kararlarını sınırlıyor.

## En kritik risk

`Instantly/` operasyonun kalbi — kampanya kuralları, fiyat listesi, müşteri
metin kuralları, 37 maddelik hata kaydı, araştırma protokolü — ve **hiçbir
sürüm geçmişi yok.** Bir dosya bozulursa geri dönüş yok. Playground'da git'in
iki kez kurtardığı şeyin karşılığı burada mevcut değil.

İyi haber: `Instantly/.gitignore` doğru; `.env` (Reoon ve fuar API anahtarları)
git'in görüş alanı dışında. `git check-ignore` ile doğrulandı.

## Yapılan tek fiziksel iş: yedek

`C:\Users\Anj\Yedekler\NarAjans-20260916-0422` — robocopy ile birebir kopya.
**20.307 dosya, 4.21 GB, 0 hata, 7 dakika.** `node_modules` ve `__pycache__`
hariç (611 MB, yeniden üretilebilir). Kritik dosyaların MD5'leri tek tek
karşılaştırıldı, Türkçe karakterli derin yollar dahil hepsi aynı.

Zip yerine klasör kopyası seçildi: Türkçe karakterli adlar arşiv formatlarında
sorun çıkarabiliyor, tek dosya geri almak kopyada zahmetsiz
(claude 3557db3e · 16.09 04:22).

## Açık kalanlar

- **Instantly nasıl sürümlenecek?** Codex'in `.git`'ini paylaşmak
  (`refs/heads/main` bizim, `refs/codex/*` onun) en az müdahale görünüyor ama
  Codex'in checkpoint mekanizmasını bozup bozmayacağı bilinmiyor. Kullanıcı bu
  kararı Claude'un tek başına değil, **bir Codex ajanıyla ortaklaşa** almasını
  istedi.
- **Kök depo kurulsun mu?** Kurulursa Codex checkpoint'lerini oraya yazabilir;
  `.gitignore` olmadan bu her turda 4.2 GB'lık anlık görüntü demek. Sıra bu
  yüzden **önce `.gitignore`, sonra `git init`.**
- **`Katılımcı-listeleri/.git` 171 MB** — temizlenmeli mi, temizlik geri alma
  yeteneğini ne kadar geriye götürür?
- **Kökte `AGENTS.md` yok.** Claude kökte 6.8 KB talimatla çalışıyor, Codex
  talimatsız. Ortak kuralların ikisinin de okuduğu bir yerde olması gerekiyor.
- **Bayatlama tuzakları:** `Instantly/DURUM.md` mezar taşı olarak duruyor ama
  duruyor; `TODAY-CHECKLIST-GUNCEL.md` adında "güncel" geçen dosya.
- **`NAR - Sözleşme Oluşturma` tamamen boş** — silinsin mi, kullanıcıya sorulacak.

## Yöntem notu

Codex'e danışma `-s read-only` ile zorlandı. Codex'in kendi yapılandırması
`sandbox_mode = "danger-full-access"` ve `approval_policy = "never"`; fikir
almak için çağrılan bir ajanın yazma yetkisi olmamalı
(claude 3557db3e · 16.09 04:31).

İlk danışma turu elektrik kesintisiyle yarıda kaldı; oturum kimliğiyle
(`codex exec resume 01a0a7d7-...`) kaldığı yerden açıldı. Codex'in ürettiği
48 KB'lık ara çıktı diskte durduğu için araştırma yeniden yapılmadı.

Bağlantılar: [[kapanis-ritueli]], [[yasanan-hatalar]], [[acik-uclar]]
