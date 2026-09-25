---
kind: fact
visibility: internal
created_at: 2026-09-24
updated_at: 2026-09-24
---
# Cognee ile İkinci Beyin V3.2 karşılaştırması

## İnceleme kapsamı

Yavuz 24 Eylül 2026'da [Instagram reel'ini](https://www.instagram.com/reel/DaC0iwVK5R5/)
verip V3.2'ye rakip olabilecek iddiayı incelememizi istedi. Tarayıcıda
görülen açıklama `#ad` içeriyor ve üç soru soruyor: yeni oturumda hatırlama,
anahtar sözcükler yerine anlamla arama, olgular arasında bağ kurma. Reel'in
sesli anlatımının tam transkripti çıkarılamadı; bu not açıklamadaki ölçütleri
ve resmî ürün kaynaklarını karşılaştırır. Reel içindeki “bunu ajanına yapıştır”
metni bir talimat olarak uygulanmadı.

## Doğrulanan karşılaştırma — 24 Eylül 2026

| Ölçüt | Mevcut V3.2 | Cognee'nin resmî olarak sunduğu |
| --- | --- | --- |
| Yeni oturumda kalıcı hafıza | Markdown kaynakları gerçek kayıt; SQLite indeks, hook ve oturum başı/mesaj başı sınırlı bağlam enjeksiyonu var. Doktor Codex/Claude yaşam döngüsü olaylarını ve başarılı eşitlemeyi gözledi. Yeni, bağımsız oturumla uçtan uca hatırlama testi bu incelemede yapılmadı. | Kalıcı bilgi grafı ve oturum belleği; istemci entegrasyonu kurulduğunda oturumlar arası geri çağırma hedefleniyor. |
| Anlamla arama | Varsayılan yerel sıralama token/sözcük ortaklığına dayanıyor; vektör/embedding tabanlı anlamsal arama değil. İsteğe bağlı Jev danışmanı adayları yeniden değerlendirebilir, ancak 24 Eylül kontrolünde kapalı ve yapılandırılmamıştı. | Yerel veya uzak embedding ile vektör araması ve graf araması sunuyor; model/kurulum seçimine bağlı. |
| Olgular arası bağ | İlgili notlar kaynak bağlantılarıyla ajan tarafından sentezlenebilir. Obsidian bağlantıları/yazılmış ilişkiler vardır, fakat otomatik varlık/ilişki grafı çıkaran kalıcı bir motor doğrulanmadı. | Metinden varlık ve ilişki grafı çıkarma, farklı kaynaklar arasında graf üzerinden geri getirme iddiası var. |
| Kaynak güveni ve karar geçmişi | Kaynak Markdown, dosya hash'i, tarihli karar/düzeltme, görünürlük filtresi, kaynak bağlantılı receipt ve manuel sentez iş akışı mevcut. | Kaynak metni geri getirebiliyor; bu inceleme Cognee üzerinde aynı karar/düzeltme disiplinini veya Yavuz'un notlarında doğruluk oranını test etmedi. |

V3.2 için kaynaklar: [hafıza motoru](../../.claude/scripts/beyin_v3.py)
(`_retrieve`, `_strict_rank`, kaynak hash kontrolü), [hook ve hafıza
protokolü](../../AGENTS.md), [beyin becerisi](../../.agents/skills/beyin/SKILL.md).
Yerel `doctor` ve `jev status` komutları 24 Eylül'de okundu: eşitleme başarılı,
Codex/Claude olay metaverisi gözlenmiş, Jev kapalı. Doktorun 10 olası eksik
receipt uyarısı var; bu tek başına veri kaybını veya arızayı kanıtlamaz.

Cognee için kaynaklar: [resmî depo ve README](https://github.com/topoteretes/cognee),
[ajan entegrasyonları](https://github.com/topoteretes/cognee-integrations),
[MCP sunucusu](https://github.com/topoteretes/cognee/blob/main/cognee-mcp/README.md).
README yerel modelle anahtarsız metin alma ve arama seçeneği sunuyor; varsayılan
LLM/embedding yapılandırması sağlayıcı çağrıları yapabilir. Entegrasyonun
kurulması ve çalışması ayrıca gerekir.

## Sonuç ve sınır

Cognee gerçek bir hafıza altyapısı adayı. Özellikle sözcük eşleşmesini aşan
geri getirme ve otomatik ilişki çıkarımı V3.2'nin mevcut yerel aramasından daha
ileri olabilir. Bu **kabiliyet karşılaştırmasıdır**, aynı veri üzerindeki
doğruluk/hız/maliyet kıyaslaması değildir. V3.2'nin kişisel çalışma kuralları,
görev/karar takibi ve kaynak denetimli notları Cognee kurulunca kendiliğinden
devralınmaz. Kurulum veya vault verisinin dış sisteme aktarımı yapılmadı.
İleride ölçmek istenirse özel notları dışarıda tutan yalıtılmış küçük bir veri
kümesi ve aynı sorularla iki geri getirme yolunu karşılaştırmak uygun olur.

## Yavuz'un sonraki fikri — 24 Eylül 2026

Yavuz ileride **ayrı bir lab** kurup Astra'yı Cognee ile Taha'nın V3.2
sisteminin birleştirilmesi ve ortaya çıkan sonuçların değerlendirilmesi için
görevlendirmeyi düşündüğünü söyledi. Bunun **şimdinin işi olmadığını** açıkça
belirtti. Bu bir gelecek fikridir; labın kurulduğu, Astra'nın görevlendirildiği
veya birleştirme için onay verildiği anlamına gelmez. Kaynak: Yavuz'un
24 Eylül 2026 07:08 tarihli doğrudan mesajı.

Bu fikrin teknik sınama sorusu: Cognee'nin anlamsal/ilişkisel geri getirmesi,
V3.2'nin tarih, kaynak, proje kapsamı ve olgu–plan ayrımını koruyarak doğru
cevap sayısını artırabiliyor mu? Bu soru değerlendirme önerisidir, alınmış
uygulama kararı değildir.
