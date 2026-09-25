---
kind: fact
visibility: internal
created_at: 2026-09-24
---
# arXivisual — araştırma makalesini görsel anlatıma dönüştürme

Yavuz'un [24 Eylül 2026'da verdiği reel](https://www.instagram.com/reel/DdleHuriHYq/)
mevcut [video inceleme aracı](video-inceleme-araci.md) ile transkript, 40
seçilmiş kare ve OCR üzerinden incelendi. Videoda ad “Archive Visuals” gibi
duyuluyor; 00:36–00:37 karelerinde GitHub deposu açıkça
[`rajshah6/arXivisual`](https://github.com/rajshah6/arXivisual) olarak görünüyor.

[Resmî site](https://www.arxivisual.org/) bir arXiv URL/ID girerek makaleyi
görsel açıklamaya dönüştürmeyi ve `arxiv.org` adresine `isual` eklemeyi
anlatıyor. [Proje README'si](https://github.com/rajshah6/arXivisual)
çok ajanlı makale/konu analizi, bölüm planı, Manim animasyonları, seslendirme
ve etkileşimli kaydırmalı sunum akışını tanımlıyor. 24 Eylül GitHub ağaç
kontrolünde `SKILL.md` bulunmadı: bu, hazır bir Codex/Claude becerisi değil,
web uygulaması ve kaynak kod projesidir. Reel'deki “bir günde geliştirildi”
ifadesi bu kontrolde bağımsız doğrulanmadı.

**Gelecekteki kullanım:** Yavuz AI operatörlüğü öğrenirken arXiv'deki teknik
makalelerin zor kavramlarını görselleştirmek için aday. Video-inceleme aracı
var olan videoyu analiz eder; arXivisual makaleden yeni görsel anlatım üretir.
Kaynak README'sine göre yerel kurulum Node/Python, Manim ve Azure OpenAI
dağıtımı gibi bağımlılıklar ister. Önce web sitesinde uygun bir makaleyle
çıktı kalitesi ve kullanım koşulları görülebilir. Bu turda siteye makale
gönderilmedi, repo indirilmedi ve kurulum yapılmadı.
