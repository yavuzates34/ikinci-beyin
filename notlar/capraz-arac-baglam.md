# Çapraz-araç bağlam sorunu

Kapalı sohbet uygulamalarındaki konuşmalara erişim yok. Çözülmemiş.

> Merkez: [[BEYIN]] · İlgili: [[ikinci-beyin-mimarisi]] · [[acik-uclar]]

---

| Araç | Konuşma nerede | Otomatik erişim |
|---|---|---|
| Claude Code | `~/.claude/projects/**.jsonl` | ✅ |
| Codex CLI | `~/.codex/sessions/**` | ✅ |
| ChatGPT uygulaması | OpenAI sunucularında | ❌ |
| Gemini / Grok | Kendi sunucularında | ❌ |

**Sert gerçek:** kapalı sohbet uygulamasındaki konuşmaya canlı erişim yok. Bu bir
ayar meselesi değil, mimari gerçek — bu şirketlerin "geçmiş konuşmalarımı oku"
arayüzü yok.

**Yakalama seçenekleri:**

- **Masaüstü tarayıcı:** eklenti ile otomatik, her prompt, ücretsiz, kendi
  makinende. En yakın karşılık bu.
- **iPhone uygulaması:** otomatik yakalama **mümkün değil** (kapalı kutu). Ama
  paylaş menüsü + iOS Kısayollar ile iki dokunuşta not düşürülebilir. Her
  uygulamada çalışır.
- **Dönemsel dışa aktarma:** gecikmeli ama boşluk bırakmaz.
- **Ekran kaydı yöntemi (kullanıcının fikri):** sohbeti yavaşça kaydırarak video
  çek, `izle.py` ile çözümle. Duvarı aşan tek yol; görselleri de yakalıyor.
  Detay: hafızadaki `sohbet-ekran-kaydi-yakalama` notu.

**Avenox'un cümlesi bu yüzden anlamlı:** *"Asla chat arayüzünü kullanmam, her şeyi
kendi vault'umun içerisinde yönetirim."* Bu bir üslup tercihi değil, zorunluluk.

---
