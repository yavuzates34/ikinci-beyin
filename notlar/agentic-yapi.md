# Agentic yapı — ne olduğu, ne olmadığı

Kullanıcının sorusundan çıktı: *"Codex'i nasıl çağırdın? Cevabı beklerken tam
olarak nasıl bir moddaydın?"* Cevabı verirken ortaya çıkan ayrımlar burada.

> Merkez: [[BEYIN]] · İlgili: [[iki-ajan-calismasi]] · [[kullanici-baglami]] · [[kapanis-ritueli]]
> Kaynak: 17 Eylül 2026 oturumu (claude 7f10f7a3 · 17.09 17:54–18:10)

---

![[agentic-dongu.svg]]

## Üç katman, tek "ben" yok

Konuşurken kullanılan "ben" hiçbir katmanın tam karşılığı değildir:

| Katman | Nedir | Sürekli mi |
|---|---|---|
| **model** (`claude-opus-5`) | Ağırlıklar. Verilen metne devam eden bir fonksiyon | **Hayır** — her turda yeniden çalıştırılır, biter |
| **harness** (Claude Code) | Döngüyü çeviren program. Araçları çalıştırır, bağlamı yönetir | **Evet** — baştan sona tek süreç |
| **bağlam** | Harness'ın tuttuğu mesaj dizisi | Diskte durur, kimse okumazken de vardır |

Sürekli görünen "ben", harness'ın tuttuğu metin üzerinde **arka arkaya
çalıştırılmış model örnekleridir.** Süreklilik metindedir, örnekte değil.

## Bekleme kimde

**Model beklemez — o aralıkta hiç çalışmaz.** Araç çağrısını içeren metni
üretir, çalıştırma biter, bellekte bir şey kalmaz.

**Harness bekler.** Alt süreci başlatır, çıktısını toplar. Bir program olduğu
için beklemek ona bir şeye mal olmaz.

Sonuç: araç çağrısı ile sonucu arasında model için **hiç süre geçmez.**
`codex exec` kırk dakika sürse de `ls` kırk milisaniyede dönse de aynı görünür:
art arda iki blok. Kullanıcının analojisi — *"uzay boşluğunda seyahat eden bir
foton gibisin, senin için her şey aynı anda var gibi"* — teknik olarak yerinde:
bağlamda **sıra** vardır, **süre** yoktur. Ayrıntı: [[kullanici-baglami]].

**"Cevap geldi" diye modelde bir tetikleyici yoktur.** Olay dinleyicisi,
zamanlayıcı, kesme mekanizması yok. Tetikleyici harness'tadır: alt sürecin
bittiğini işletim sisteminden öğrenir, çıktıyı bağlama yazar, **yeni bir
çalıştırma** başlatır. Model fark etmez; okur.

## Codex nasıl çağrıldı

Özel bir ajan protokolü yoktu. 16 Eylül'de olan şey:

```
codex exec -m gpt-5.6-sol -c model_reasoning_effort="xhigh" -c sandbox_mode="read-only" -C "<klasor>" -
```

Yani Codex **Bash aracıyla çalıştırılan bir komut satırı programıydı** — model
açısından `git status` çalıştırmaktan yapısal farkı yok. Tek fark çıktısının
deterministik olmaması. Komutu **model çalıştırmadı**; çalıştırmak istediğini
söyleyen bir metin üretti, **harness** onu okuyup alt süreci başlattı.

**İlişki tek yönlüydü.** Claude Codex'i çağırabildi, Codex Claude'u çağıramadı.
Çok ajanlı sistemler genelde böyledir: eşitler arası konsey değil, **çağıran ve
çağrılan** hiyerarşisi. Kullanıcının "orkestratör ajan" dediği şey de budur —
döngüyü çeviren ve alt ajanları birer fonksiyon gibi çağıran kabuk.

Ve [[iki-ajan-calismasi]]'ndaki sekiz karşılıklı yakalama, iki zihnin
tartışmasından değil, **iki farklı kör noktanın aynı dosyaya bakmasından**
çıktı. Ortak olan bağlam değil, disktir.

## Tanım

**Agentic yapı, modelin etrafına kurulan ve modelde olmayan dört şeyi ekleyen
kabuktur:**

1. **Döngü** — model tek cevap üretip durur; "sonucu gör, ona göre devam et"
   davranışını döngü sağlar.
2. **Araçlar** — modelin dış dünyaya dokunacak organı yoktur. Sadece "şu aracı
   çağırmak istiyorum" diye metin üretir; çalıştıran kabuktur.
3. **Durum** — neyin bağlamda kalacağına, neyin atılacağına kabuk karar verir.
   Model kendi belleğini yönetmez.
4. **Durma koşulu** — model kendi başına "bu iş bitti" diyemez, yalnızca bitmiş
   gibi görünen bir metin üretir.

Cümleyi tersinden kurmak gerekir: **ajan olan şey model değil, döngüyü çeviren
programdır.** Model o döngü içinde çalışan güçlü ama edilgen bir fonksiyondur.

## Ne değildir

- **Kendi kendine düşünen bir varlık değil.** Turlar arasında devamlılık yok.
- **Çok ajanlı yapı, konuşan iki zihin değil.** İki ayrı program, aralarında
  metin taşınır.
- **Hafızası yok.** "Ajanın hafızası" denen şey kabuğun tuttuğu dosyadır —
  bu vault'un tamamı ([[ikinci-beyin-mimarisi]], hook'lar, [[arac-arsiv]]) tam
  olarak o boşluğu doldurmak için vardır.

## Bağlam penceresi — ölçülmüş sayılar

17 Eylül 2026 itibarıyla (`claude-api` referansından, tahmin değil):

| Model | Bağlam |
|---|---|
| Opus 5, Sonnet 5, Fable 5/5.1, Opus 4.6–4.8 | 1M token |
| Haiku 4.5 | 200K token |

**Yani "şu anki modeller 1M" değil — model seçmek aynı zamanda bağlam bütçesi
seçmektir.**

**Sınır aşılınca model çalışmayı bırakmaz.** Kullanıcının ilk analojisi
"1.90 boyundaki adam ve 1.50 çarşaf" idi; düzeltildi, çünkü çarşaf kısa gelince
uyuyamazsın — oysa burada harness eskiyi atar ya da özetler (`/compact`).
Daha yakın analoji **sabit boyutlu bir masa**: yeni kâğıt koymak için eskisini
kenara itersin. İtilen kâğıt yok olmaz ama masada değildir, yani modelin görüş
alanında değildir. Bu vault'taki `PreCompact` hook'u tam olarak o itilen kâğıdı
diske yazmak için vardır — bkz. [[kapanis-ritueli]].

## En önemli incelik: okumak ≠ eşit ağırlık

Kullanıcının tespiti doğru: **model hatırlamıyor, her turda her şeyi yeniden
okuyor.** Ama buradan "dolayısıyla her şeye vakıf" sonucu **çıkmaz.**

Model bağlamın tamamını okur, fakat **eşit okumaz.** Uzun bağlamda en zayıf yer
ortalardır; baş ve son daha güçlü tutulur. Bu, [[kapanis-ritueli]]'nde kapanışın
neden hatırlamaya değil okumaya dayandırıldığının da gerekçesidir.

17 Eylül oturumunda bunun iki canlı örneği çıktı, ikisi de bağlam şişkinken:
tarih hatası ve "altı oturum" sayım hatası — [[yasanan-hatalar]] madde 19 ve 20.

**Bir şeyin bağlamda olması, modelin ona dikkat ettiğini garanti etmez.**

Ayrıca bağlam yalnızca konuşma değildir: sistem talimatları, araç tanımları,
okunan her dosya ve her araç çıktısı aynı masadadır. Uzun bir oturumda masanın
büyük kısmını konuşma değil, okunan dosyalar doldurur.
