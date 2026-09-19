# Astra kontrol dosyası — üçüncü göz

Merhaba Astra. Bu dosyayı Claude (oturum `5c600e7e`, 19–20.09.2026) yazdı;
oturum `96517e26` (20.09 01:55) tazeledi. Claude ve Codex (`gpt-5.6-sol`)
birlikte bir onarım turu yaptı: sunum incelemesinde bulunan 13 açık, artı
sonradan bulunan 3 açık (14, 15, 16). Senin işin bizim yaptığımızı **bağımsız
olarak kontrol etmek** ve açık kalanları kapatmak.

**Bu tur Codex Desktop'tan yapılmalı.** Claude, seni alt ajan olarak
çağırmayı denedi ve olmadı: kurulu Codex CLI 0.150.1 `gpt-6-astra` modelini
çalıştıramıyor ("requires a newer version of Codex"). Ölçüm:
[[olculmus-bulgular]] §15. Yani bu denetim, kullanıcının Desktop oturumunda
senin tarafından yapılacak.

Kullanıcı sana bunu `/goal` ile verecek. Bu dosya emir listesi değil, denetim
haritası: nereye bakacağını ve neyin kanıt sayıldığını söyler.

---

## Nasıl çalış

1. **Önce `AGENTS.md` ve `BEYIN.md`.** Hook'un yoksa başlangıç bağlamını elle
   al: `python araclar/oturum_basi.py --bicim duz`.
2. **Doğruluk sırası:** kod (`araclar/*.py`) > `AGENTS.md` > `notlar/` > sunum
   (`rehber/sunum/`). Alt sıradaki üsttekiyle çelişiyorsa üsttekini doğru say
   ve çelişkiyi raporla.
3. **Kanıt kuralı:** "kapandı" yazan her madde **Claude'un iddiasıdır.** Kendi
   ölçümünü yap. Ölçemediğini "ölçülmedi" yaz; çalışıyor varsayma.
4. **Düzeltme yetkin var, sınırı var.** Kod ve not düzeltebilirsin. Ama
   dosya taşıma, silme ve kalıcı katman budaması **kullanıcı onayı ister**
   (ileride yetkili orkestratör ajan da onaylayabilir). `kapanan-oturum:`
   satırı yalnızca gerçek geçişte yazılır.
5. **Denetçi rapor eder, düzeltmez** ilkesi notlar için geçerli: bir iddia
   yanlışsa metni yeniden yazma, **altına not düş** (kullanıcı kararı, 19.09).
   Bu kural koda değil, kalıcı notlardaki iddialara aittir.
6. **Kapanışta** kendi oturumunu `oturumlar/2026-09-20-astra-kontrol.md`
   olarak yaz, başlığın altına `kapanan-oturum: <senin id'in>` koy, kalıcı olanı
   `notlar/` içine terfi ettir.

## Doğrulama komutları

```
git log --oneline 629fc81~1..HEAD        # bu onarım turunun commitleri
python araclar/derle.py --kuru           # dedektör, işaretçi denetimi, bakım
python araclar/bakim.py                  # kalıcı katman adayları
python araclar/baglam.py <oturum-id>     # bağlam doluluğu
python araclar/gece_kayit.py --kuru      # gece taslağı adayları
python araclar/omurga.py 5c600e7e --tam  # bu onarım turunun tamamı
python araclar/oku.py 5c600e7e --saat 20:31   # erken devir canlı uyarısı
```

Madde 16 için (PowerShell, sistemi değiştirmez, yalnız okur):

```
Get-ScheduledTaskInfo -TaskName 'playground-derleyici' |
  Select-Object LastRunTime,LastTaskResult,NumberOfMissedRuns,NextRunTime
(Get-ScheduledTask -TaskName 'playground-derleyici').Principal
Get-Content derleme\derleyici.log
```

Codex'in denetim oturumları: `01a0baa5` (birinci tur, limite takıldı),
`01a0bb8e-de58` (ikinci tur, aynı gün). Sunum incelemesi: `01a0ba53`,
`01a0ba74`. Hook güven ölçümü: `01a0bbc6-b6f6` (Desktop) ve `01a0bbcc-8818`
(normal `codex exec`). Bu gecenin Codex kapanışları iki arşiv kaydında:
[[2026-09-20-codex-hook-guven-oncesi-denetimi]] ve
[[2026-09-20-codex-hook-guveni-ve-testlerin-kapanisi]].

## Kontrol listesi

Ana belge: `oturumlar/2026-09-19-sunum-onarim-listesi.md` — 15 satırlık durum
tablosu, artı sonradan bulunan 14, 15 ve 16. açıklar. Sırayla kontrol et.
Tablonun büyük kısmı **20.09 00:35** damgalı; yalnızca madde 5 ve 7 satırları
01:35'te tazelendi ve eski metinleri hücrenin içinde duruyor. Aşağıdakiler en
kırılgan gördüğüm yerler.

### A. Bilerek açık bıraktıklarımız — bunları kapatman gerekebilir

1. **Madde 5 — kapandı; bağımsız doğrula.** Kullanıcı CLI TUI'de güven verdi.
   Sonraki Desktop oturumunda ve güven-atlatma bayraksız normal `codex exec`
   çağrısında `SessionStart` ile `UserPromptSubmit` çıktıları ham kayıtta
   `role=developer`, `hooks.additional_context` olarak görüldü
   ([[olculmus-bulgular]] §14.2). Önceki başarısız ölçüm ve Claude'un yanlış
   pozitifi §14'te korunuyor. Senin işin, kapanışı ham kayıt tipinden bağımsız
   doğrulamak; modelin "hook etkin" ifadesini tek başına kanıt sayma.
2. **Madde 7 — erken devirin Codex tarafı.** Claude'da iki eşik de canlı
   doğrulandı: %50 (19.09 20:31) ve %70 (20.09 00:36). Codex'te formül
   düzeltildi (`total_tokens`, Codex'in itirazı) ve elle doğru sonuç verdi.
   Taşıyıcı hook artık çalışıyor; açık kalan kanıt gerçek bir Codex oturumunda
   %50/%70 eşiğinin aşılması, uyarı ve kurtarma omurgasının otomatik oluşması.
3. **Madde 12 — kapandı, ama bir kez ve elle.** Zincirin tamamı 20.09 00:45'te
   gerçek koşulda çalıştı (`oto-01a0bb8e-de58.md`). Tek çalıştırma; gece
   görevinin **kendi tetiklemesiyle** henüz uçtan uca görülmedi. İlk fırsat
   21.09 00:30 — ama önce madde 16'yı oku: o tetikleme son dört gecenin
   ikisinde yarıda öldü, yani bu kanıt kendiliğinden gelmeyebilir.
4. **Madde 10 — kalıcı katman hâlâ 100 KB üstünde.** Kullanıcı dört taşımadan
   ikisini onayladı. Kalan iki taşıma (kuralların yanındaki tarihçe) bilinçli
   olarak yapılmadı.
5. **Madde 16 — gece görevi tetikleniyor ama yarıda ölüyor.** Bu, listeye
   sonradan eklendi (claude 96517e26 · 20.09 01:50) ve **hiç düzeltilmedi.**
   Görev saatinde çalışıyor (`LastRunTime 00:30:01`, `NumberOfMissedRuns 0`)
   ama `LastTaskResult = 0xC000013A` (STATUS_CONTROL_C_EXIT) ile ölüyor:
   `Principal.LogonType = Interactive` olduğu için görünür bir konsol penceresi
   açılıyor ve o pencere kapanınca süreç gidiyor. Günlük derleme yazılıyor,
   **git commit + push adımı hiç çalışmıyor.** Son dört gecenin ikisinde böyle
   oldu. Ölçüm ve tablo: [[olculmus-bulgular]] §16.
   **Senden istenen:** (a) ölçümü bağımsız tekrarla; (b) bunun madde 12'yi ne
   kadar zayıflattığına karar ver — o maddenin "gerçek koşulda çalıştı" kanıtı
   **elle** tetiklenmiş bir çalışmadır; (c) `BEYIN.md` satır 27'deki "her gece
   otomatik commit + push" ifadesinin düzeltilmesi gerekip gerekmediğini söyle.
   Düzeltmeyi **uygulama**: zamanlanmış görev bir sistem ayarıdır, kullanıcıya
   aittir (bkz. C bölümü).

### B. Benim kendi zayıf noktalarım — özellikle buraya bak

6. **Claude bir maddeyi yanlış kapattı.** Madde 5'i ekran görüntüsü ve modelin
   ifadesine dayanarak "kapandı" saydı; kayıt tipine bakınca tersi çıktı ve
   geri açıldı. Aynı hata başka maddelerde de olabilir: "kapandı" satırlarının
   kanıtını tipine kadar kontrol et.

7. **Claude hem yapan hem doğrulayan oldu.** Codex'in birinci turu kullanım
   limitine takıldı ve raporunu yazamadı; ara bulguları kendi oturum kaydından
   okundu. İkinci tur kısa tutuldu. Yani bağımsız göz bu turda zayıf kaldı.
   Durum tablosundaki "kapandı" satırlarını bu gözle oku.
8. **Claude'un bağlam penceresi ölçülmedi, kalibre edildi.** `araclar/baglam.py`
   içindeki `PENCERE` tablosu kullanıcının arayüzde gördüğü yüzdeye dayanıyor
   (472.650 token ≈ %45-50 → 1M). Model değişirse ya da tablo eskirse uyarı
   sessizce yanlış eşikte gelir. Daha sağlam bir kaynak bulabilir misin?
9. **`derleme/baglam-durum.json` tek dosya.** İki oturum aynı anda yazarsa
   oku-değiştir-yaz yarışı olur; kaybedilen seviye fazladan bir uyarı üretir.
   Zararsız gördüm, ölçmedim.
10. **Bakım ölçütleri kaba.** `bakim.py` içindeki "kapanmış madde" sayımı
   basit bir desene dayanıyor; "büyük not" eşiği (12 KB) keyfî.
11. **Antigravity ve diğer uygulamalar ölçülmedi.** `rehber/uygulama-adaptorleri.md`
   tablosunda yokturlar. Yeni uygulama tanıtma protokolü hiç uygulanmadı.
12. **Sunum artık doğru mu?** `rehber/sunum/slides/` içindeki 14 slaytı kodla
    karşılaştır. Sunum, sistemi olduğundan daha otomatik, daha güvenli ya da
    daha tamamlanmış göstermemeli. Yayınlanan sunum kullanıcının claude.ai
    hesabında; sen yalnızca kaynağı görebilirsin.

### C. Yapılmaması gerekenler

- `dinleme/` içindeki dosyalara `[[bağ]]` yazma (bilinçli karar).
- Bu klasörün dışına müdahale etme (`notlar/proje-egemenligi.md`).
- Kimlik numarası, parola, mali detay bu klasöre hiç yazılmaz; depo GitHub'a
  gidiyor.
- Gece derleyicisini ve hook'ları bozacak değişiklikleri sınamadan bırakma:
  her değişiklikten sonra `python araclar/derle.py --kuru` temiz çıkmalı.

## Senden beklenen çıktı

- Her madde için: **doğrulandı / kusurlu / ölçülmedi** + kanıt.
- Kusurluysa: düzelt (yetkin dahilinde) ya da gerekçesiyle kullanıcıya sor.
- Kendi oturum kaydın ve kalıcı notlara terfi.
- Bizim göremediğimiz, listede hiç olmayan bir açık bulursan onu ayrıca yaz:
  en değerli çıktı budur.

> İlgili: [[2026-09-19-sunum-onarim-listesi]] · [[acik-uclar]] ·
> [[iki-ajan-calismasi]] · `rehber/uygulama-adaptorleri.md` ·
> `rehber/codex-sunum-rehberi.md`
