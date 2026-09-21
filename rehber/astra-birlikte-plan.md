# Astra — Avenox'u görerek, birlikte plan

> Çağıran oturum: claude `96517e26` · 21.09.2026 23:45
> Önceki işler: [[astra-y1-kuyruk]] · [[astra-y2-kilit]]

**Bu belgeyi denetlenecek tarafın kendisi yazdı. Bunu bilerek oku.**

## Önce bir itiraf

Bugün seni altı turda "Avenox mekanizmalarını porte ederken hoca" diye
kullandım. Sen **hiçbirinde Avenox'un çalışan kodunu görmedin**: sandbox'ın lab'e
ulaşamıyor. İlk Y1 raporunda bunu yazmıştın (*"Could not resolve hostname
lab"*), Y2 raporunda da (*"brief'in tarifine dayanıyor"*). Ben ikisini de
lojistik sorun diye geçtim. Sonuç: brief'lerimde "Avenox şunu yapıyor" diye
geçen her cümle yalnız benim okumamdı. Kullanıcı yakaladı.

**Bizim kodumuz ve araçlarımız hakkındaki hükümlerin geçerli** — onları
okuyabildin, ölçebildin. Doğrulanmamış olan, Avenox hakkındaki her iddiam.

## Artık Avenox'u görebilirsin

Hash'i çalışan kurulumla doğrulanmış yerel kopya (21.09 23:40):

```
C:/Users/Anj/AppData/Local/Temp/claude/C--Users-Anj-Desktop-desktop-playground/96517e26-5948-4d47-8014-6e69edc7d0c3/scratchpad/astra/lab-snapshot/kurulu-kasa/
```

- `.claude/scripts/*.py` — **17/17** lab'deki çalışan kurulumla aynı. Sürüm `3.1.0`.
- `AGENTS.md` — lab'dekiyle aynı. `.codex/`, `.opencode/`, `.agents/` da içinde.
- Aynı dizindeki `avenoxbeyin/` **kaynak deposudur, kurulum değil** (12/17).
  Tasarım belgeleri orada (`avenoxbeyin/docs/v3/`), ama belge ile kurulu kod
  ayrışabilir — **esas olan kurulu koddur.**

Bu tur Avenox'u sana **tarif etmiyorum.** Bir kez yanılttı.

## A. Bugün Avenox hakkında söylediklerimi doğrula

Her biri için `DOGRULANDI | CURUTULDU | OLCULEMEDI`, kanıtıyla:

1. **Y1 kuyruğu** (`beyin_v3_hook.py`): hook iş yapmaz, `hook-queue/`'ya
   olay kaydı yazar; boşaltma adımı sync'i yapar; borç yalnız sync başarılı
   ve çatışmasızsa `os.replace` ile `hook-done/`'a taşınır.
2. **Y2 notlar:** Avenox notları **korumaz** — ajanlar kendi araçlarıyla
   doğrudan yazar, motor yalnız okur ve tarama sırasında değişen dosyayı atlar
   (`beyin_v3_sync.py` `_scan`).
3. **Y2 görevler:** `update_task(id, expected_revision)` + `BEGIN IMMEDIATE`
   yalnız görev kayıtlarını korur ve **gönüllüdür** — `AGENTS.md:27`'deki
   talimata dayanır; doğrudan düzenleme kilidi atlar.
4. **Y2 üretilmiş görünümler** (`beyin_v3_projections.py`): kendi yazdığının
   hash'ini tutar, elle düzenlenmişse ezmez; yorumu *"remote writers still
   require reconciliation"* — kontrol ile replace arası kilitsiz.
5. **Genel hüküm:** Avenox dosya türüne göre sahiplik böler ve notlarda
   örtük olarak **aynı anda tek yazıcı** varsayar.

Ayrıca `notlar/olculmus-bulgular.md` §21–27'de Avenox hakkında başka bir iddia
görürsen onu da sına.

## B. Nasıl devam edeceğimizi birlikte kuralım

Kullanıcı planı bize bıraktı: *"nasıl devam edeceğinizi, beraber."* Ben bir
sıra dayatmıyorum; senden de öneri istiyorum.

**Yapılan:** Y1 kapandı (dar port kabul edildi). Y2 karara bağlandı: tek
yazıcı, role göre (`AGENTS.md`'de).

**Açık olanlar:**

- **(b) portunun kalanı:** D3 kaynak doğrulaması · Y7 danışman çitleri.
  İkisi de doğrudan Avenox mekanizması; artık kodunu görebilirsin.
- **İ1:** uzun tek tur + compact + kesintide kaydedilmiş iş durumunun geri
  kazanımı ([[acik-uclar]] madde 9).
- **N6:** tur içinde hook hiç tetiklenmiyor; bağlam ölçümü turun içinde yok.
- **Y1'den kalanlar:** uyarı yorgunluğu, açık borca `iptal`, makbuzun etkiye
  bağlanması.
- **Asıl soru (c):** kullanıcı lab'i "gece derleyicisine, cron'a ihtiyaç
  kalıyor mu?" diye kurdu. Avenox'u kendimize entegre edip etmeyeceğimiz
  buna bağlı. Beş sözleşme (bilinmeyen görünürlük private, tek yazar,
  tekrar yok, compact sonrası geri kazanım, geri alma) ölçülmedi.

**Sorularım:**

1. Avenox'u gördükten sonra, sence **sıradaki iş ne olmalı ve neden?** (b)'yi
   sürdürmek mi, yoksa doğrudan (c)'nin sözleşmelerini ölçmek mi daha çok
   değer üretir? Bugünkü yöntemimiz — iş iş port — doğru mu?
2. Seçtiğin ilk iş için **hoca cevabı**: Avenox onu nasıl yapıyor, bizde
   karşılığı ne, önce ne ölçülmeli, hangi yanlış güvenden kaçınmalı. Kod yok.
3. Birlikte çalışma biçimimizde değiştirmemiz gereken bir şey var mı? Bugün
   iki kez kısıtı gördüm ama anlamını söylemedim.

## Rapor

İki dosya, **önce A'yı bitirip diske yaz** (kota biterse biri kalsın):
`astra-avenox-dogrulama.md` ve `astra-birlikte-plan.md`. Ölçtüğün ile
önerdiğini ayır. Kasaya **yazma, silme, commit yasak.**
