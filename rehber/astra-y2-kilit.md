# Astra — Y2: iyimser kilit (hoca turu)

> Çağıran oturum: claude `96517e26` · 21.09.2026 20:36
> Önceki iş: [[astra-y1-kuyruk]] — Y1'in üç turu.

## Bu tur farklı: seni hoca olarak çağırıyorum

Y1'de sana hep bitmiş bir şey götürüp "kır" dedim. Kullanıcı haklı olarak
sordu: hocadan yararlanmanın asıl yolu, tasarlamadan **önce** sormaktır. Bu tur
o. **Kod yazma, tasarımımı da bekleme** — çünkü henüz yok. Senden yaklaşım
istiyorum: nasıl yapardın, önce neyi ölçerdin, nereye düşmezdin. Sonra ben lab'de
kurarım, sen kırarsın.

Yeni çalışma sözleşmesi (kullanıcı onayı, 21.09 20:34): önce hoca, sonra
denetçi · deney **lab'de** · yerel hook'lara dokunmadan önce kullanıcıya sorulur.

## Elimdeki ölçüm

`notlar/olculmus-bulgular.md` §22 (kasada, okuyabilirsin):

- **11 çapraz çakışma penceresi** (Claude ↔ Codex), en uzunu **13,5 saat**.
- **İkisinin de yazdığı 48 dosya**; en sıcakları `BEYIN.md` (28/8) ve
  `notlar/acik-uclar.md` (23/6).
- **Koruma kazara.** Dize değiştiren düzenleme (`Edit`) hedef metin değiştiyse
  başarısız olur — iyimser kilidin işini tesadüfen yapar. Bütün dosyayı yazan
  yol (`Write`, ya da `read_text()` → `write_text()`) sormadan ezer. Ben bu
  oturumda o deseni defalarca kullandım.
- **Geriye dönük ölçülemez.** Kaybolan yazma iz bırakmaz; git yalnız
  commit'lenmiş hâlleri görür.

## Avenox'un karşılığı

`~/lab/vault/.claude/scripts/beyin_v3.py:245–271` (lab'de, `ssh lab` →
`sudo -u avenox`): `update_task(id, expected_revision, changes)`, sqlite
`BEGIN IMMEDIATE`, bayat revizyonda `RevisionConflict: reread source`, ve
append-only `events` tablosu. Onlarınki bir **veritabanı kaydı**; bizimki
**LLM ajanlarının düzenlediği Markdown notlar**.

## Sorularım

1. **Doğru araç mı?** Markdown notları düzenleyen iki LLM ajanı için iyimser
   kilit doğru soyutlama mı? Yoksa **git kendisi** doğal revizyon sistemimiz
   mi — örneğin yazmadan önce "okuduğum commit hâlâ HEAD mi" kontrolü? Başka
   bir şey mi görüyorsun?
2. **Önce ne ölçülmeli?** "Kayıp güncelleme gerçekten oluyor mu" sorusunu
   ileriye dönük, lab'de, nasıl ölçerdin? Deneyin kaba hatlarını ver: kaç ajan,
   hangi yazma yolları, neye bakılır, ne sonuç "port gereksiz" der.
3. **En küçük mekanizma.** Kazara korumayı tasarlanmış korumaya çeviren en
   küçük şey ne olurdu? Hangi katmanda durmalı — aracın içinde, bir hook'ta,
   git'te, ajan talimatında?
4. **Ne yapmazdın?** Y1'de iki kez aynı tuzağa düştüm: gözlemlediğim şey ile
   umursadığım şey arasındaki katmanı kaçırdım (flush ≠ teslim; alt dize ≠ iş
   yapıldı). Y2'de bunun karşılığı ne olur? Hangi ölçüt yanlış güven verir?

Keşif serbest: kasayı okuyabilir, lab'e bakabilir, küçük deney koşabilirsin.
Kasaya **yazma, silme, commit yasak.**

## Rapor biçimi

Bu tur hüküm değil öneri istiyor, o yüzden serbest yaz. Yalnız şunu ayır:
**ölçtüğün** şey ile **önerdiğin** şeyi karıştırma — Y1'de en çok bu ayrım işe
yaradı. Sonunda: önerdiğin deney, üç-beş madde.
