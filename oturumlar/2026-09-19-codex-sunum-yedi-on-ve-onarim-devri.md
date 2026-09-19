# Codex sunum incelemesi — 7–10. slaytlar ve onarım devri

kapanan-oturum: 01a0ba74

**Aralık:** 19.09.2026 19:16–20:04  
**Konu:** “İkinci Beyin — Kullanım Rehberi”nin 7–10. slaytlarının sesli
incelemesi; kalıcı katman, gece taslağı, Codex hook'ları ve erken devir
mimarisindeki açıkların ölçülmesi; Claude + Codex ortak onarım devri.

> Merkez: [[BEYIN]] · Önceki bölüm:
> [[2026-09-19-codex-sunum-ilk-alti-slayt]] · Kalıcı devir:
> [[sunum-incelemesi-onarim-listesi]] · İlgili: [[acik-uclar]] ·
> [[kapanis-ritueli]] · [[gece-derleyicisi]] · [[iki-ajan-calismasi]]

---

## Ne konuşuldu ve ne yapıldı

İnceleme 7. slayttan sürdü. Kullanıcı önce farklı sağlayıcıların aynı beyni
kullanabilmesi için altyapının ilk oturumda kurulması gerektiğini söyledi.
Burada “sağlayıcı adaptörü” kavramı düzeltildi: hook'lar model sağlayıcısının
değil Claude Code ve Codex gibi somut uygulama/harness'ın yeteneği. Ortak çekirdek
çoğaltılmamalı; ilk temas komutu uygulamayı ve gerçek yeteneklerini tanıyıp ince
adaptörü kurmalı ve sınamalı (codex 01a0ba74 · 19.09 19:18–19:21).

7. slayttaki “Kapat” kartı ayrıştırıldı. Kapatmak pencereyi kapatmak değil;
canlı oturumun zengin bağlamı kaybolmadan önce ham kayıttan omurgayı okuyup
kronolojik arşiv ile kalıcı terfiyi yazmak, kaynakları bağlamak ve gerçek
geçişte kapanış işaretini koymak. Kullanıcının vurgusu kabul edildi: aynı canlı
model, yalnızca sonradan ham kaydı okuyan temiz bir modele göre oturumun
görünmeyen muhakeme sürekliliğinden ve önem değerlendirmesinden yararlanabilir.
Bu yüzden en iyi an context'in tamamen tükendiği an değil, zengin fakat hâlâ
çalışılabilir olduğu erken devir aralığıdır (codex 01a0ba74 · 19.09 19:22–19:25).

Kalıcı notların büyümesi kaynaklardan denetlendi. Başlangıçta bütün notların
yüklenmediği doğrulandı: `AGENTS.md`, küçük `BEYIN.md` haritası ve başlangıç
yönergesi sıcak katman; konu notları seçilerek açılıyor, oturum arşivi yalnızca
aranınca okunuyor. Buna rağmen kalıcı Markdown katmanı yaklaşık 123 KB'a
ulaşmıştı; hem 65 KB seçmeli-okuma hem 100 KB bölme eşiği aşılmıştı. Kaynak
incelemesi üç tortu örneği buldu: `acik-uclar.md` çok sayıda kapanmış tarihsel
madde taşıyor, `kapanis-ritueli.md` güncel yöntem ile elenmiş SessionEnd
tasarımını karıştırıyor, `ortam-kurulum.md` kalıcı olduğu hâlde `BEYIN.md`
haritasında yoktu (codex 01a0ba74 · 19.09 19:26–19:30).

Gece derleyicisinin kalıcı notları budamadığı doğrulandı. Tasarım ilkesi “ölçer,
yazmaz”: boyutu, işaretçileri, kapanış eksiklerini ve yedek sağlığını raporluyor;
tek anlatı istisnası kapanışsız oturum için yazdığı geçici arşiv taslağı.
Büyümeyi ölçmek ile onu bakıma bağlamak arasında açık var. Karar: otomatik
silme yapılmamalı; derleyici büyük dosya, kapanmış madde, haritasız not,
güncel/tarihsel karışması ve yoğun tekrar için budama adayları üretmeli, gerçek
bakım canlı oturumda kullanıcıyla yapılmalı (codex 01a0ba74 · 19.09 19:30–19:32).

8. slayt bu açığın kullanıcıya ulaşacağı doğal yer olarak belirlendi. Mevcut
başlangıç uyarıları operasyonel; bilgi tabanı sağlığı uyarısı yok. “Her şey
yolundaysa ajan hiçbir şey söylemez” cümlesi fazla güçlü: sessizlik yalnızca
tanımlı uyarı olmadığını gösterir. Codex tarafında hook dosyalarının gerçekten
kurulu olduğu, fakat proje güveni ve Desktop `SessionStart` zincirinin otomatik
çalışmasının uçtan uca doğrulanmadığı ayrıştırıldı. Bu oturumda başlangıç
betiğinin elle çalıştırılması otomatik hook kanıtı sayılmadı
(codex 01a0ba74 · 19.09 19:34–19:37).

9. slayttaki “Gece taslağını işleyelim” cümlesinin kapsamı daraltıldı. Aynı
oturuma ertesi gün devam edilirse taslağı işlemek gerekmez; canlı bağlam ve ham
kayıt sürer. Taslak asıl olarak farklı/yeni bir oturumun kapanışsız eski oturumu
kurtarması içindir; paralel çalışma bundan yararlanabilir ama taslak özel bir
paralelleştirme mekanizması değildir. İlk anda “mevcut oturum kendi taslağını
görmüyor” durumu hata sanıldı; kullanıcı itirazından sonra bu değerlendirme
düzeltildi. Açık kalan dar test: aynı oturum normal kapandığında eski
`oto-<id>.md` dosyası temizleniyor mu (codex 01a0ba74 · 19.09 19:39–19:41).

10. slayttaki “omurgayı kayıttan okur” ifadesinin belirsiz olduğu bulundu.
Buradaki kayıt `oturumlar/` altındaki Markdown arşiv değil, Claude veya Codex'in
konuşma sırasında tuttuğu ham JSONL günlüğüdür. Normal omurga kullanıcı
mesajlarını; `--tam` ise gece yazıcısı gibi temiz bağlamlı ajanlar için modelin
metin cevaplarını da çıkarır. Araç çıktıları ve düşünme blokları ikisinde de
dışarıda kalır (codex 01a0ba74 · 19.09 19:42).

Codex ham kaydındaki son tamamlanmış ölçümde etkin context penceresi 258.400,
son tur kullanımı yaklaşık 165.406 token bulundu: yaklaşık %64. Desktop bunu
arayüzde göstermediği için ölçüm JSONL `token_count` olayından yapıldı. Bu,
erken devir sorununu somutlaştırdı (codex 01a0ba74 · 19.09 19:45).

Önceki incelemenin sekiz bulgusu ile bu oturumdaki beş yeni bulgu birleştirilip
13 maddelik bağımsız onarım dosyası yazıldı: [[sunum-incelemesi-onarim-listesi]].
Dosya `BEYIN.md` haritasına ve bir sonraki oturum notuna eklendi; her maddede
kaynaklar, bitiş ölçütleri, kullanıcı kararları ve Claude + Codex ortak çalışma
sırası var (codex 01a0ba74 · 19.09 19:50–19:55).

## Kararlar ve gerekçeler

1. **Adaptör sağlayıcıya değil uygulamaya göre kurulur.** Aynı sağlayıcının
   farklı uygulamaları aynı hook yeteneklerini taşımayabilir.
2. **Erken devir P0'dır ve hibrit olmalıdır.** Yalnız manuel kapanış, doluluk
   göstergesi olmayan uygulamalarda görünmez sorumluluk yükler. Tam otomatik
   `PreCompact` kapanışı ise çok geç ve konu ortasında gelebilir. Uygulama
   otomatik ölçer, güvenli eşikte turun sonunda kontrol noktası ve devir önerisi
   üretir; kullanıcı anlamlı geçişi onaylar; gerçek geçiş olmadan
   `kapanan-oturum:` yazılmaz. `PreCompact` son ağ kalır
   (codex 01a0ba74 · 19.09 19:58–19:59).
3. **Budama otomatik silme değildir.** Derleyici adayları bildirir; semantik
   temizlik kullanıcıyla canlı oturumda yapılır.
4. **Gece taslağı aynı oturumun devamı için zorunlu değildir.** Eski bir
   oturumun başka bir oturumdan kurtarılması için güvenlik malzemesidir.
5. **Ölçülmemiş otomasyon varmış gibi anlatılmaz.** Codex adaptörü diskte var;
   güven ve gerçek Desktop başlangıcı sınanana kadar otomatik zincir açık kalır.

## Denenen, elenen ve düzeltilen yorumlar

- Her sağlayıcının ayrı beyin kurması elendi; tek çekirdek + uygulama adaptörü
  seçildi.
- “Bütün kalıcı notlar her oturumda okunuyor” varsayımı yanlışlandı; seçmeli
  okuma çalışıyor, sorun kalıcı katmanın kendi içindeki tortu.
- “Gece derleyicisi notları zaten buduyor” varsayımı yanlışlandı; yalnızca
  ölçüyor ve raporluyor.
- Manuel kapanışın tek başına yeterli olması ve `PreCompact`ın ana kapanış yolu
  olması elendi. Tam otomatik semantik kapanış da seçilmedi.
- Aynı oturumun kendi gece taslağını görmemesi önce hata sanıldı; kullanıcı
  ayrımıyla düzeltildi. Yalnızca artık taslak dosyanın kapanışta temizlenmesi
  test edilmeli.
- “Codex kurulumu var mı bilinmiyor” ifadesi düzeltildi: dosya kurulumu var;
  etkinlik ve otomatik teslim doğrulanmamış.

## Açık kalanlar

1. [[sunum-incelemesi-onarim-listesi]] içindeki 13 maddeyi Claude ana oturumunda
   bir Codex ajanıyla birlikte, önce sistem sonra notlar sonra sunum sırasıyla
   kapatmak.
2. Kullanıcının Codex proje hook'larını güven arayüzünde inceleyip onaylaması;
   yeni Codex oturumunda gerçek `SessionStart` teslimini ölçmek.
3. Erken devir eşiği, erteleme davranışı ve yeni oturuma gerçek geçişin ne kadar
   otomatik olacağına kullanıcıyla karar vermek.
4. Budama aday raporunu ve başlangıç uyarısını tasarlamak; mevcut kalıcı katmanı
   kullanıcı onayıyla temizlemek.
5. Aynı oturum normal kapandığında eski gece taslağının temizlenmesini sınamak.
6. Sunum incelemesine 10. slaytın kalan maddelerinden devam etmek; 11–14 henüz
   incelenmedi.

