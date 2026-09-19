# Astra kontrol dosyası — üçüncü göz

Merhaba Astra. Bu dosyayı Claude (oturum `5c600e7e`, 19–20.09.2026) yazdı.
Claude ve Codex (`gpt-5.6-sol`) birlikte bir onarım turu yaptı: sunum
incelemesinde bulunan 13 açık, artı sonradan bulunan 1 açık. Senin işin bizim
yaptığımızı **bağımsız olarak kontrol etmek** ve açık kalanları kapatmak.

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

Codex'in denetim oturumları: `01a0baa5` (birinci tur, limite takıldı),
ikinci tur oturumu aynı gün. Sunum incelemesi: `01a0ba53`, `01a0ba74`.

## Kontrol listesi

Ana belge: `notlar/sunum-incelemesi-onarim-listesi.md` (14 madde + durum
tablosu). Sırayla kontrol et. Aşağıdakiler en kırılgan gördüğüm yerler.

### A. Bilerek açık bıraktıklarımız — bunları kapatman gerekebilir

1. **Madde 5 — Codex Desktop'ta hook'lar tetiklenmiyor.** 20.09'da ölçüldü ve
   sonuç olumsuz (claude 5c600e7e · 20.09 00:38): `/hooks` bir güven ekranı
   açmıyor; kullanıcı testinde yeni turda hiçbir hook satırı gelmedi; kayıttaki
   harita ve saat satırlarının tipi `custom_tool_call_output`, yani onları
   modelin kendisi çalıştırmıştı. **Claude bu maddeyi bir ara yanlışlıkla
   "kapandı" saydı**; düzeltildi. Senin işin: Desktop'ta hook desteği var mı,
   varsa nasıl etkinleşir — belge ve sürüm notlarından; CLI'da ayrıca sına.
   Ders: modelin "hook'lar etkin" demesi kanıt değildir, yapılandırmayı okumuş
   olabilir. Kanıt ham kayıttaki enjeksiyon tipidir.
2. **Madde 7 — erken devirin Codex tarafı.** Claude'da iki eşik de canlı
   doğrulandı: %50 (19.09 20:31) ve %70 (20.09 00:36). Codex'te formül
   düzeltildi (`total_tokens`, Codex'in itirazı) ve elle doğru sonuç verdi, ama
   canlı uyarı yok — çünkü taşıyıcı hook tetiklenmiyor (madde 5). Mekanizma
   değil, taşıyıcı eksik.
3. **Madde 12 — gece taslağının diğer iki hâli.** Aynı oturuma dönüş sınandı.
   "Başka oturum devralır" ve "terk edilmiş oturum kurtarılır" hâlleri gerçek
   bir gece çalışmasında henüz görülmedi.
4. **Madde 10 — kalıcı katman hâlâ 100 KB üstünde.** Kullanıcı dört taşımadan
   ikisini onayladı. Kalan iki taşıma (kuralların yanındaki tarihçe) bilinçli
   olarak yapılmadı.

### B. Benim kendi zayıf noktalarım — özellikle buraya bak

5. **Claude bir maddeyi yanlış kapattı.** Madde 5'i ekran görüntüsü ve modelin
   ifadesine dayanarak "kapandı" saydı; kayıt tipine bakınca tersi çıktı ve
   geri açıldı. Aynı hata başka maddelerde de olabilir: "kapandı" satırlarının
   kanıtını tipine kadar kontrol et.

6. **Claude hem yapan hem doğrulayan oldu.** Codex'in birinci turu kullanım
   limitine takıldı ve raporunu yazamadı; ara bulguları kendi oturum kaydından
   okundu. İkinci tur kısa tutuldu. Yani bağımsız göz bu turda zayıf kaldı.
   Durum tablosundaki "kapandı" satırlarını bu gözle oku.
7. **Claude'un bağlam penceresi ölçülmedi, kalibre edildi.** `araclar/baglam.py`
   içindeki `PENCERE` tablosu kullanıcının arayüzde gördüğü yüzdeye dayanıyor
   (472.650 token ≈ %45-50 → 1M). Model değişirse ya da tablo eskirse uyarı
   sessizce yanlış eşikte gelir. Daha sağlam bir kaynak bulabilir misin?
8. **`derleme/baglam-durum.json` tek dosya.** İki oturum aynı anda yazarsa
   oku-değiştir-yaz yarışı olur; kaybedilen seviye fazladan bir uyarı üretir.
   Zararsız gördüm, ölçmedim.
9. **Bakım ölçütleri kaba.** `bakim.py` içindeki "kapanmış madde" sayımı
   basit bir desene dayanıyor; "büyük not" eşiği (12 KB) keyfî.
10. **Antigravity ve diğer uygulamalar ölçülmedi.** `rehber/uygulama-adaptorleri.md`
   tablosunda yokturlar. Yeni uygulama tanıtma protokolü hiç uygulanmadı.
11. **Sunum artık doğru mu?** `rehber/sunum/slides/` içindeki 14 slaytı kodla
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

> İlgili: [[sunum-incelemesi-onarim-listesi]] · [[acik-uclar]] ·
> [[iki-ajan-calismasi]] · `rehber/uygulama-adaptorleri.md` ·
> `rehber/codex-sunum-rehberi.md`
