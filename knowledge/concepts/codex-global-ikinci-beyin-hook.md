---
id: codex-global-ikinci-beyin-hook
kind: fact
project: ikinci-beyin-v3.2
visibility: internal
created_at: 2026-09-23T01:31:00+03:00
updated_at: 2026-09-23T01:31:00+03:00
revision: 1
---
# Codex global İkinci Beyin hook sistemi

## Amaç

Codex'te açılan yerel projeleri İkinci Beyin V3'e deterministik biçimde bağlamak,
proje oturumlarında kaynak-backed handoff yüklemek ve her kullanıcı promptunda gerçek
yerel saati modele vermek. Kod depoları bağımsız kalır; İkinci Beyin kodun tamamını veya
ham konuşmaları kopyalamaz.

Gereksinim kaynağı: [yan sohbet dökümü](../../notes/2026-09-22-yan-sohbet-global-ikinci-beyin-hook-konusmasi.md).

## Kurulu mimari

- Kişisel Codex eklentisi: `C:\Users\Anj\plugins\ikinci-beyin-global`
- Kurulu sürüm: `0.1.0+codex.202609230132`
- Yaşam döngüsü köprüsü: `.claude/scripts/beyin_v3_bridge.py`
- Proje kayıt katmanı: `.claude/scripts/beyin_v3_projects.py`
- Kullanılan olaylar: `SessionStart`, `UserPromptSubmit`, `PostToolUse`, `Stop`,
  `PreCompact`, `SessionEnd`
- Eski proje-yerel hook devre dışıdır; geri alınabilir yedeği
  `.codex/hooks.project-local-backup.json` konumundadır.

Köprü ikinci bir hafıza motoru kurmaz. Mevcut V3 hook, senkronizasyon, receipt ve doktor
katmanlarını çağırır. Codex'in güven kontrolü atlanmamıştır; değişen tanım CLI `/hooks`
ekranında `Plugin - ikinci-beyin-global@personal` kaynağıyla incelenmiş ve altı olayın
altısı etkinleştirilmiştir.

## Proje kaydı

Bir klasörde ilk gerçek Codex conversation'ı başladığında global `SessionStart` hook'u:

1. Normalize edilmiş tam yoldan sabit 24 karakterlik `project_id` üretir.
2. Mevcut dosyaları ezmeden `AGENTS.md`, `PROJECT_MEMORY.md` ve
   `.codex/second-brain-project.json` oluşturur veya doğrular.
3. İkinci Beyin'de `projects/<project_id>.md` ters kaydını oluşturur.
4. Proje handoff'unu, ilgili kaynak kayıtlarını ve receipt session kimliğini oturuma ekler.
5. Compaction sonrası `SessionStart(source=compact)` ile aynı bağlantıyı yeniden yükler.

Kayıt yalnız aktif `cwd` için yapılır; diskler taranmaz. Windows'ta çalışma anında tüm
yerel/removable/RAM filesystem kökleri keşfedilir. Bu makinede `C:`, `D:`, `E:`, `F:` ve
`X:` kapsamdadır. Sürücü kökleri, Windows/Program Files/ProgramData, geçici klasörler,
Codex eklenti/cache alanları ve başka bir V3 vault'u otomatik kayıt dışıdır. Symlink
zincirleri reddedilir.

## Saat ve gizlilik

`SessionStart` ve her `UserPromptSubmit` olayında Europe/Istanbul yerel tarih-saat değeri
ephemeral context olarak üretilir. Modelden eski mesajlara bakarak günün saatini tahmin
etmemesi istenir. Saat üretimi proje kaydı dışında da çalışır.

Prompt yalnız o çağrı sırasında kaynak araması için bellekte kullanılır. Hook kuyruğuna
event, harness, opaque session, proje etiketi ve `project_id` yazılır; prompt metni
yazılmaz. Benzersiz bir privacy-probe ifadesi runtime state içinde aranmış ve bulunmamıştır.
`no_memory=true` storage/retrieval'i kapatır; saat bağlamı prompt saklamadan devam eder.

## Doğrulama — 2026-09-22/23

- Gerçek proje: `D:\KODLAMA\codex-dynamic-usage-bar`,
  `project_id=7d8c4df65aac83e29116dea9`. Dosyalar ikinci çalışmada byte-identical kaldı.
- Zararsız yeni proje: `D:\KODLAMA\ikinci-beyin-global-smoke`,
  `project_id=4957ab65db0c7c18ace40b20`. İlk gerçek promptta `SessionStart`,
  `UserPromptSubmit`, `Stop`, `SessionEnd` sırası V3 metadata kayıtlarında görüldü ve iki
  taraftaki bağlantı dosyaları otomatik oluştu.
- Compaction simülasyonunda saat, proje kimliği, `PROJECT_MEMORY.md` içeriği ve receipt
  session kimliği yeniden enjekte edildi.
- Kurulu plugin cache'indeki hook JSON'u kaynak kopyayla SHA-256 eşleşti ve
  `--all-local-roots` taşıdığı doğrulandı.
- `C:\Windows` üzerinde yapılan koruma testi yalnız saat bağlamı döndürdü ve proje kaydı
  denemedi.
- Yapay proje-kilidi hatası modele açık `registration failed` uyarısı verdi ve
  `hook-error.json` içinde `project-registration/TimeoutError` kaydetti. Test kilidi ve
  boş test klasörü kaldırıldı; sağlıklı queue drain hata dosyasını temizledi.
- V3 senkronizasyonu uyarı/çakışma olmadan tamamlandı. Doktor altı Codex olayını da
  `observed_metadata` olarak gördü.

## Davranış sınırı

Codex CLI boş açılış ekranında henüz conversation yaratmaz. Yeni ve daha önce güvenilmemiş
bir dizinde önce dizin güveni onaylanır; gerçek `SessionStart` ilk kullanıcı promptuyla
oluşur. Bu yüzden otomatik proje dosyaları klasör seçildiği anda değil, o projedeki ilk
gerçek Codex oturumu başladığında görünür.

Semantik kararın ne olduğunu model yazar; hook bunun yerine geçmez. Hook proje kimliği,
dosya bağlantıları, yaşam döngüsü checkpoint'leri, receipt şeması ve eksik receipt
görünürlüğünü deterministik olarak sağlar.
