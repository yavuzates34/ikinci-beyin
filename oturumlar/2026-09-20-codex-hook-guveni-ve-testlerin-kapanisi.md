# Codex hook güveni ve test oturumlarının kapanışı — 20 Eylül 2026
kapanan-oturum: 01a0bba1-ed7e, 01a0bba2-5237, 01a0bba5-99c3, 01a0bbcc-8818, 01a0bbc6-b6f6

Beş Codex kaydı aynı iş zincirinin parçalarıydı: güven öncesi/sonrası hook
testleri, başarısız Astra ön-denemesi ve sonucu kalıcı katmana işleyen ana
Desktop oturumu. Kullanıcının isteğiyle birlikte kapatıldılar.

## Kronoloji

- `01a0bba1-ed7e` (00:45): normal `codex exec` başlangıç bağlamı almadı.
  Güven kaydı henüz yoktu.
- `01a0bba2-5237` (00:46): aynı sınama güven-atlatma ile başlangıç bağlamını
  aldı. Bu karşılaştırma sorunun adaptörde değil güven katmanında olduğunu
  gösterdi ([[olculmus-bulgular]] §14.1).
- `01a0bba5-99c3` (00:49): Astra ile salt-okunur ön-denetim başlatılmak istendi,
  ancak kurulu CLI sürümü modeli çalıştırmadı; oturum model cevabı üretmeden
  bitti. Kalıcı sonuç [[olculmus-bulgular]] §15'te duruyor.
- `01a0bbc6-b6f6` (01:28–01:38): kullanıcı proje hook'larının kurulmasını
  istedi. `.codex/hooks.json` içinde gerekli üç olay grubunun ve dört komutun
  zaten doğru kurulu olduğu, eksik güvenin kullanıcı tarafından verilmiş
  olduğu görüldü. Bu yeni Desktop oturumunda `SessionStart` ve
  `UserPromptSubmit` ham kayıtta gerçek `hooks.additional_context` olarak
  doğrulandı (codex 01a0bbc6-b6f6 · 20.09 01:28).
- `01a0bbcc-8818` (01:32): güven-atlatma bayrağı olmadan izole normal
  `codex exec` sınaması yapıldı. Aynı iki hook çıktısı ham kayıtta gerçek
  enjeksiyon olarak görüldü ve model başlangıç satırını doğru aktardı
  (codex 01a0bbcc-8818 · 20.09 01:32).

## Kararlar ve neden

- Yeni hook eklenmedi. Mevcut `SessionStart`, iki komutlu `UserPromptSubmit`
  ve `PreCompact` bu projenin gereken ince adaptörüdür; sorun yapılandırma
  eksikliği değil kalıcı güvendi.
- `Stop` eklenmedi: erken-devir ölçümü bir sonraki kullanıcı mesajından önce
  `UserPromptSubmit` ile tur sınırında modele ulaşır. `SessionEnd` de semantik
  kapanış sayılmadığı ve terk edilmiş oturumları gece derleyicisi yakaladığı
  için kullanılmıyor.
- Kanıt ölçütü modelin beyanı değil ham kayıttaki
  `hooks.additional_context` türüdür. Önceki yanlış pozitif bu ölçütle ayrıldı.

## Yazılanlar

- [[olculmus-bulgular]] §14.2'ye güven sonrası Desktop ve CLI ölçümü eklendi.
- `rehber/uygulama-adaptorleri.md`, `rehber/astra-kontrol.md`, [[acik-uclar]]
  ve `BEYIN.md` güncel sonuçla düzeltildi.
- Kapanan güven maddesi [[acik-uclar-tarihce]] dosyasına taşındı; geçmişteki
  başarısız ölçüm silinmedi.

## Açık kalan

- Codex'te gerçek `PreCompact` olayı henüz canlı sınanmadı.
- Codex oturumu %50/%70 bağlam eşiğini geçtiğinde uyarı ve kurtarma omurgasının
  otomatik oluşması henüz canlı görülmedi.
- Gece derleyicisinin 20.09 00:30 çalışması yarıda kesilmiş durumda.
- Kalıcı katman 117,6 KB ile 100 KB bakım eşiğinin üzerinde; kullanıcı onayı
  olmadan dosya taşınmadı veya silinmedi.

