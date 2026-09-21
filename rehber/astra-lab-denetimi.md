# Astra — lab denetimi ve C planı kararı

**Hazırlayan:** Claude (oturum `96517e26`), 21.09.2026 07:00.
**Okuyan:** Astra (`gpt-6-astra`), üçüncü göz.

> Bu belgeyi **denetlenecek tarafın kendisi yazdı.** Bunu bilerek oku. Nereye
> bakacağını söylüyorum ama neye varacağını söylemiyorum; vardığım sonuçlar
> §5'te ayrı başlık altında, **iddia** olarak duruyor.

---

## 1. Rolün

Üç iş var, karıştırma:

1. **Doğrula** — §3'teki iddiaların kaynakla tutup tutmadığı.
2. **Boşluğu göster** — §4'te doğrulanmamış diye listelediklerim. Oradan saldır.
3. **Karar sorusuna gerekçe üret** — §6.

**Kural: rapor et, düzeltme.** Proje kuralı (kullanıcı, 19.09): denetçi
uyuşmazlık bulursa iddianın altına not düşer, metni yeniden yazmaz. Kasada
dosya değiştirme, commit atma.

**Sandbox.** Bu tur salt okunur çalışmalı. Çağıran taraf `-s read-only`
verecek. Yazma ihtiyacın olursa **rapor et, kendin açma.**

## 2. Kota gerçeği — buna göre çalış

Kotan hızlı bitiyor ve bittiğinde 5 saat bekleniyor (kullanıcı, 21.09 06:57).
Ölçüm: tek kelimelik bir cevap `xhigh` eforda **20.624 token** yedi.

Bu yüzden:

- Kontroller **numaralı ve bağımsız**. Sırayla git, her birinin sonucunu
  tamamlayınca yaz. Kota ortada biterse sonraki pencerede **kaldığın
  numaradan** devam edilir, baştan başlanmaz.
- **Keşif serbest** (kullanıcı, 21.09 07:03). Lab'daki sistemi kendin gez,
  kur, çalıştır, kurcala. Aşağıdaki yollar sana **zaman kazandırmak** için
  var, seni kısıtlamak için değil. Verilen bir yol yanlışsa ya da eksikse,
  bunu bulgu say ve raporla.
- Kota biterse sorun değil; 5 saat beklenir, kaldığın numaradan devam edilir.
  Bu yüzden **ilerlemeni yaz**: her kontrolün sonucunu tamamlandığı anda
  rapora ekle, sona saklama.
- Uzun dosyayı gereksiz yere baştan sona okuma; satır aralığı verilen yerleri
  aç. Ama gerekiyorsa tamamını oku — karar senin.

## 3. Ortam — nerede ne var

**Lab sunucusu.** `ssh avenox` (89.144.20.133, yetkisiz kullanıcı, sudo yok).
Bizim kasaya erişimi yoktur, olmamalı da.

| Yol | İçerik |
|---|---|
| `~/kasa/` | git deposu, dal `ana`, 5 commit |
| `~/kasa/avenoxbeyin/` | Avenox kaynak deposu (v3.1.0) |
| `~/kasa/kurulu-kasa/` | kurulmuş kasanın anlık görüntüsü |
| `~/kasa/olcumler/*.json` | alt ajanın ölçüm çıktıları |
| `~/kasa/video/<id>/` | iki videonun **dört** kaynaklı transkriptleri |
| `~/lab/vault/` | **çalışan** kurulum (v3.1.0), `beyin.py` burada |
| `~/lab/avenoxbeyin-git/` | tam git geçmişi (128 commit, etiketler) |

Lab commit'leri: `fcbfed4` `00a1a45` `f3d2eba` `8bd8468` `23d1e68`.

**Bizim kasa.** `C:\Users\Anj\Desktop\desktop\playground`, dal `ana`.
Bu turun commit'leri: `4359df0` `226cb11` `50a7941` `7c4458e` `4a94a87`
`6530904`.

| Dosya | Ne için |
|---|---|
| `oturumlar/2026-09-21-tam-otomasyon-plani.md` | **ana iş belgesi.** Tasarım, elenen fikir, C planı |
| `notlar/olculmus-bulgular.md` | §15 güncellemesi, §17, §18, §19 |
| `notlar/arac-izle.md` | transkripsiyon kaynak seçme kuralı |
| `gorunurluk.json` + `araclar/gorunurluk.py` | yeni görünürlük ayrımı |

## 4. Doğrulanmış iddialar — örnekleme, tam denetim değil

Avenox bulgularının tamamı **bir alt ajanın raporundan** geliyor. Ben dört
noktada örnekleme yaptım, dördü de tuttu. Komutları veriyorum ki aynısını
yapabilesin.

**D1 — Depo halka açık ve v3.1.0 en güncel.**
`cd ~/lab/avenoxbeyin-git && git tag && git log -1 --format='%h %ad %s' --date=iso`
Beklenen: etiketler `v3.0.0 v3.0.1 v3.0.2 v3.1.0`, son commit 21.09 02:41.

**D2 — `beyin.md:31` kurulum isteğini paket kurma yetkisi sayıyor.**
`sed -n '29,35p' ~/kasa/beyin.md`
Alt ajan bunu "yetki genişletme" diye raporladı; cümlenin devamında yönetici
izni gerekirse **kullanıcıdan onay istendiği** yazıyor. Ajan yarısını
aktarmıştı, ben tamamını okudum. **İkisi de doğru olabilir — yorum senin.**

**D3 — Kaynak hash'i sorgu anında yeniden hesaplanıyor, tutmazsa kayıt dışlanıyor.**
`sed -n '445,458p' ~/kasa/kurulu-kasa/.claude/scripts/beyin_v3.py`

**D4 — Makbuzsuz tur zaman damgalı açık uç olarak raporlanıyor.**
`cat ~/kasa/olcumler/receipt-gaps.json`

## 5. DOĞRULANMAMIŞ — asıl işin burası

Aşağıdakilerin hiçbirini ben kontrol etmedim. Alt ajanın raporunda ölçüm
olarak geçiyorlar; **ölçüm olduklarını doğrulamadım.**

**Y1.** Kuyruk telafisi: "3 olay kuyrukta bırakıldı, sonraki olayda 4'ü birden
işlendi" (`beyin_v3_hook.py:46-103`).
**Y2.** Paralellik: "bayat revizyonla update → `RevisionConflict`; 12 paralel
hook → 12/12, `integrity_check: ok`" (`beyin_v3_sync.py:455-530`).
**Y3.** Companion bütçe payı: "Kurallar %40, Last-Session %20 taban"
(`beyin_v3_companion.py:6-7`).
**Y4.** Gizli veri süzgeci: `secrets_redacted: 1`.
**Y5.** `doctor` çıktısının kapsamı (`beyin_v3_cli.py:194-221`).
**Y6.** Beş istemci adaptörünün gerçekten aynı betiğe düşmesi.
**Y7.** Jev çit tasarımı: gölge modu, kill-switch, içeriksiz çağrı kaydı
(`docs/v3/JEV.md`). Ben belgeyi okudum, **davranışı ölçmedim.**
**Y8.** `PostToolUse`'un tek başına kayıt düşürdüğü iddiası.

Ayrıca **benim** ölçümlerimden denetlenmesi gerekenler:

**Y9.** "Avenox'ta bağlam doluluğu ölçümü hiç yok." Ben `grep` ile aradım ve
bulamadım. Bulamamak yok demek değildir — başka adla aranmalı.
**Y10.** "Compaction diskteki ham kaydı silmiyor, özeti ekliyor." Tek bir
`/compact` olayında (21.09 02:42, oturum `96517e26`) gözlendi. Tek gözlem.
**Y11.** VDS'te bellek rezervasyonu yok (`vmware-toolbox-cmd stat memres → 0`).
Aracın okuyamayıp 0 basma ihtimali elenmedi.

## 6. Karar sorusu

Kullanıcı, bizim sistemimizin Avenox'un üstüne kurulup kurulmayacağına karar
verecek. Üç duruş:

**(a) Onun sistemini al, içeriğimizi taşı.** Hızlı, bakımlı, beş istemcili
temel. Bedeli: arşiv arama gider, içerik onun kayıt biçimine sığar, yol
haritasına bağlanırız.

**(b) Bizimkini koru, mekanizmalarını porte et.** Bedeli: onun çözdüğünü
yeniden türetmek.

**(c) İki katman.** Onun sistemi sürekli alt yapı; bizimki üstte anlatı ve
denetim katmanı, `ara.py`/`omurga.py` ham konuşma kaydı üstünde kalır.
Gerekçe: iki sistem **farklı kaynağı** okuyor — onunki kasa dosyalarını,
bizimki harness'ın JSONL kayıtlarını. Aynı soruya cevap vermedikleri için
çakışmazlar.

**Ölçüt önerim (bu da denetlenecek):** taşınamayan tek şey içeriktir, makine
değildir. 130 KB'lık kalıcı katman ve onun taşıdığı gerekçeler varlıktır.

Bakılması gereken karşı kanıt: Taha videoda *"notlarınızdan kayıp olmayacak,
sadece arkadaki motoru değiştiriyorsunuz"* diyor
(`~/kasa/video/NpzqWvKR_iw/yerel-large-v3-transkript.txt`, 06:48–07:08).
Yani motor değişimi tasarımın öngördüğü kullanım. **Bu, (c)'nin riskini
düşürüyor mu, yoksa bağımlılığı gizliyor mu?**

## 7. Benim yargılarım — karar değil, denetlenecek iddia

**İ1. Dört katmanlı tur içi bağlam ölçümü gereksiz.** Gerekçem Y10'a dayanıyor
ve Y10 tek gözlem. Y10 çürürse İ1 de çürür.

**İ2. (c) duruşu doğru.** Gerekçem §6'daki "farklı kaynak" ayrımı.

**İ3. Bayatlama işareti anlatılan şeye takılmalı** — `derle.py` davranışına
dair bulgu `derle.py`'nin hash'ini taşısın. Hiç denenmedi.

**Bu üçünü çürütmeye çalış.** Bu turda benim bir kez kendi tasarımımı çürüttüğüm
ve iki yanlış iddiamın 20.09'da yine senin tarafından yakalandığı kayıtlı
([[olculmus-bulgular]] §16 altındaki not).

## 8. Rapor biçimi

Kontrol numarası başına tek blok:

```
[D3] DOGRULANDI | CURUTULDU | OLCULEMEDI
  kanit: <komut ya da dosya:satir>
  gozlem: <ne gordun>
  not:    <varsa>
```

Sonunda: **§6 karar sorusuna gerekçeli cevabın** ve §7'deki üç iddia için
ayrı ayrı hüküm. Uzun tutma; her hüküm kaynağını göstersin.

> Merkez: [[BEYIN]] · İş belgesi: [[2026-09-21-tam-otomasyon-plani]] ·
> Ölçümler: [[olculmus-bulgular]] · Önceki tur: [[astra-kontrol]]
