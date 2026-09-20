# Araçlar: arşiv arama (omurga, ara, anlam, oku)

123 oturumluk konuşma arşivini aranabilir kılan dört araç ve altlarındaki ortak
okuyucu. Hepsi `araclar/` içinde, proje kökünden çağrılır.

> Merkez: [[BEYIN]] · İlgili: [[kapanis-ritueli]] · [[olculmus-bulgular]] · [[yasanan-hatalar]]
> Kaynak: [[2026-09-07-ikinci-oturum]] (claude 3557db3e · 08.09)

---

## Üç basamak (izle.py ile aynı mantık)

Önce ucuz ve geniş tarama, sonra dar aralıkta yakın bakış:

```bash
python araclar/ara.py "whisper"                       # 1. sözcüksel, ~10 sn
python araclar/anlam.py "tarif" --kapsam proje        # 2. kelimeyi hatırlamıyorsan
python araclar/oku.py 3557db3e --saat 14:00-14:30     # 3. tam döküm, dar aralık
python araclar/omurga.py                              # kapanışta: bu oturumun kemiği
```

Ortak seçenekler: `--kapsam proje|claude|codex|hepsi`, `--rol kullanici|model|hepsi`,
`--sonra YYYY-AA-GG`.

## Neden ham grep yetmiyor

Dosyalar JSON. `grep` kaçış karakterleriyle dolu, meta veriyle sarılı,
kilometrelerce tek satır verir; içinde base64 gömülü görseller de vardır.
Araçlar JSON'u çözüp mesajın içindeki metne bakar.

## Mimari: tek okuyucu, dört araç

`araclar/kayit.py` ortak katman. Claude ve Codex konuşmaları diske **farklı
biçimlerde** yazıyor; ayrıştırma dört yerde tekrarlanmasın diye tek yere kondu.

| Biçim | Yol | Mesaj nerede |
|---|---|---|
| Claude | `~/.claude/projects/<proje>/<id>.jsonl` | `type: user\|assistant`, `message.content[]` |
| Codex | `~/.codex/sessions/<yıl>/<ay>/<gün>/rollout-*.jsonl` | `type: response_item`, `payload.type: message` |

Proje kökü `kayit.py`'nin konumundan hesaplanır (`__file__` → bir üst klasör),
çalışma dizininden değil. Araç nereden çağrılırsa çağrılsın aynı projeyi bulur;
klasör taşınırsa da kendini bulmaya devam eder.

## Kronoloji: en güncel veri kuralı

`anlam.py` başlangıçta sonuçları yalnızca **benzerliğe** göre sıralıyordu. Bir
konuda fikir değiştirildiyse, sonradan çürütülmüş eski bir cümle nihai kararın
üstünde çıkabilir.

Düzeltme: **seçim benzerliğe göre, gösterim zamana göre.** Ekranda en altta kalan
satır en günceli olur ve `<- EN GUNCEL` ile işaretlenir. `ara.py` da eskiden
yeniye sıralar ve sonunda en güncel eşleşmenin hazır `oku.py` komutunu basar.

Gerekçe: **bir konu hakkında en son ne söylendiği, ilk ne söylendiğinden daha
bağlayıcıdır.**

**İlke — arşiv kanıttır, hüküm değil.** Bir konuda ne *kararlaştırıldığı*
`notlar/` içinde yazar; arşiv o kararın nasıl oluştuğunu gösterir.

## anlam.py: anlamsal arama

Model `paraphrase-multilingual-mpnet-base-v2` (1 GB, 768 boyut), ONNX üzerinden
(`fastembed`) — torch değil, çünkü torch 2-3 GB ve C: dar. Model ve indeks D:'de
(`D:\AI\gomme`, `D:\AI\beyin-indeks`), `BEYIN_MODEL` / `BEYIN_INDEKS` ortam
değişkenleriyle taşınabilir.

```bash
python araclar/anlam.py --kur          # artımlı tazele
python araclar/anlam.py --durum
```

İndeks artımlı: her oturumun imzası `boyut:son-yazma`; değişmeyen yeniden
gömülmez. Model değişirse indeks kendini sıfırlar.

**Kalite sınırı (dürüst hâli):** dar kapsamda iyi, tüm arşivde zayıf. 10.436
parça içinde skorlar 0.53–0.68 bandına sıkışıyor; alakasız sonuç alakalıya yakın
puan alabiliyor. Pratik kural: **`--kapsam` ile daralt.** Daha yüksek isabet
gerekirse `anlam.py` içindeki `MODEL` sabitini `intfloat/multilingual-e5-large`
yapıp `--kur --yenile` çalıştırmak yeterli (bedeli: 2.24 GB, daha yavaş sorgu).


> **Astra denetim notu:** En büyük dosyayı seçen tekilleştirme üç Codex oturumunda 81 farklı mesajı gizliyordu. Okuyucu artık bütün parçaları birleştirir; belirsiz kimlik öneğini seçmez. Gömme indeksinin tazelenmesi bu ölçümün kapsamında değil.
> Kanıtlar: [[astra-denetim-bulgulari]] · [[2026-09-20-astra-kontrol]].
> (codex 01a0bc5c-f1c4 · 20.09 04:22)
