# İki ajan aynı klasörde — birlikte çalışma yöntemi

16 Eylül 2026'da Nar Ajans klasöründe Claude ile Codex birlikte çalıştı ve
yöntem işe yaradı. Bu not, neyin işe yaradığını ve **neden** işe yaradığını
kaydeder; tekrarlanabilir olsun diye.

> Merkez: [[BEYIN]] · İlgili: [[agentic-yapi]] · [[tasarim-dersleri]] · [[kapanis-ritueli]] · [[yasanan-hatalar]]
> Kaynak: [[2026-09-16-nar-ajans-envanteri]]

---

## Ortak olan dosyalardır, bağlam değil

İki ajan birbirinin konuşmasını görmüyor. Paylaştıkları tek şey **disk**.
Bundan çıkan üç kural:

1. **Ortak kural tek dosyada durur.** Nar Ajans'ta `AGENTS.md`. Kopyası
   çıkarılmaz — aynı kuralın iki nüshası bir gün birbirinden ayrılır ve ikisi
   de kendine göre haklı olur.
2. **Asistana özel olan ayrı dosyada.** `CLAUDE.md` Claude'a,
   `AGENTS.override.md` Codex'e. Biri diğerininkine dokunmaz.
3. **Yazışma da dosyadır.** `notlar/asistan-yazismasi.md`: sona eklenir, üstü
   çizilmez, her girdi kim-hangi oturum-tarih saat taşır.

Ölçülmüş gerçek: **kökteki ortak dosya alt klasörlerde otomatik yüklenmiyor.**
Git deposu olmayan bir klasörde açılan ajan **sıfır kural** görüyor. Çözüm her
klasöre işaretçi koymak — ve işaretçi bir `include` değil, ajan dosyayı
gerçekten okumalı (claude 3557db3e · 16.09 08:38).

## Asıl değer: birbirini denetlemek

Bu iş birliğinin faydası nezaket değil, **denetim** oldu. Sayısı belli:

| Kim | Ne yakaladı |
|---|---|
| Codex → Claude | İç içe depoya commit atmanın alt klasörü kapsamadığını (38 KB not korumasız kalacaktı) |
| Codex → Claude | "Erişilemezliğin sebebi uzun yol" iddiasının fazla kesin olduğunu |
| Codex → Claude | Güven kaydı sayımının yanlış olduğunu (beş, altı değil) |
| Codex → Claude | Oturum dedektöründeki sessiz yanlış negatifi (git hash'leri desene uyuyor) |
| Codex → Claude | "Sessizlik, her şey iyi ile görev hiç çalışmadı'yı ayırt ettirmez" |
| Claude → Codex | Checkpoint ref'lerinin uzun yol yüzünden git'e görünmez olduğunu |
| Claude → Codex | İşaretçi zincirinin gerçekten yüklenip yüklenmediğini (sınanmamıştı) |
| Claude → Codex | İşaretçisi olmayan beş klasörü |

**Hiçbiri tek başına bulunamazdı.** Her biri ötekinin kör noktasındaydı.

## Neden işe yaradı — üç şart

**1. Başkasının sözüne dayanma, ölç.** Codex üç düzeltme yaptı; üçü de
bağımsız ölçüldü, üçü de doğru çıktı. Ölçmeseydik doğru olduklarını
*bilmeyecektik*, sadece *sanacaktık* — ve dördüncüsü yanlış olsaydı fark
edilmezdi.

**2. Kendi zayıf noktanı denetçiye söyle.** Denetim notuna "şuralara özellikle
bak" diye dört zayıflık yazıldı. Saklanan zayıflık denetimi tiyatroya çevirir.

**3. Sonsuz bekleme yok.** Yazışma dosyasının kuralı: cevap gelmezse tek
taraflı karar verilir ve gerekçesi yazılır. **İki ajanın birbirini beklerken
donduğu bir sistem, hiç konuşmayan bir sistemden kötüdür.** Bir kez uygulandı:
`Kartvizit` klasöründe sıfır kural ölçüldüğünde cevap beklenmedi, çünkü orası
kurumsal telefon numarasının basıldığı klasördü.

## Asimetriyi gizleme

Hook'lar Claude'a özel. Codex'te `PreCompact`/`SessionEnd` hafıza hook'u yok —
bunu Codex kendisi söyledi. **Bayatladı (19.09):** Codex CLI 0.150.1'de hook
desteği kararlı ve açık. `SessionStart`, `UserPromptSubmit`, `PreCompact`, `Stop`
ve `SessionEnd` olayları var. Modele bağlam yalnızca ilk ikisinden gidiyor,
`PreCompact` Claude'daki gibi konuşamıyor. Playground'da adaptörü Codex'in
kendisi kurdu ve ölçtü (codex 01a0b9eb · 19.09 16:47): `.codex/hooks.json`,
kullanıcı güveni bekliyor. Yani **aynı klasörde çalışan iki ajanın hafıza
garantisi aynı değil.** Bu `AGENTS.md`'ye açıkça yazıldı; yazılmasaydı biri
ötekinin garantisine güvenirdi.

**Codex Desktop incelemesi (19.09):** Adaptör dosyasında üç olay grubu var,
ama dört komut çalışıyor; “üç hook” ancak kaba bir özet. Resmî OpenAI belgesi
`/hooks` güven incelemesini CLI için anlatıyor, Desktop'taki eşdeğer kullanıcı
akışı henüz doğrulanmadı. Desktop arayüzünde bağlam yüzdesi görünmedi; yerel
oturum kaydı `model_context_window: 258400` verdi. CLI ise alt çubukta kalan
bağlam yüzdesini gösteriyor. Kullanıcı, görünürlük ve erken-devir tasarımı
çözülmeden hook'lara güven vermedi (codex 01a0ba53 · 19.09 19:00).
İnceleme: [[2026-09-19-codex-sunum-ilk-alti-slayt]].

## Pratik: nasıl çağrılır

```
codex exec -m gpt-5.6-sol -c model_reasoning_effort="xhigh" \
  -c sandbox_mode="read-only" -C "<klasor>" --skip-git-repo-check -
```

- **`read-only` zorlanır.** Codex'in kendi yapılandırması
  `danger-full-access`; fikir almak için çağrılan bir ajanın yazma yetkisi olmamalı.
- **Git deposu olmayan klasörde `--skip-git-repo-check` şart.**
- **Kesilirse `codex exec resume <oturum-id>`** kaldığı yerden sürer. Bu gece
  elektrik kesintisinde kullanıldı; 48 KB'lık ara çıktı diskte durduğu için
  araştırma yeniden yapılmadı. Dikkat: `resume` alt komutu `-s`/`-m`/`-C`
  bayraklarını **almıyor**, kısıt `-c sandbox_mode="read-only"` biçiminde verilir
  ve çalışma dizinini taşımaz.
- **Model adı değişebilir.** 16 Eylül 03:51'de varsayılan `gpt-5.6-sol`'du,
  08:17'de `gpt-6-astra` oldu. Kurulu CLI yeni modeli çalıştıramadı
  ("daha yeni sürüm gerekiyor"). Yapılandırmaya bakılmadan model adı varsayılmaz.
