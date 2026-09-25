---
kind: fact
visibility: internal
created_at: 2026-09-25
---
# PC ayarları için yerel model seçimi

## Amaç ve durum

Yavuz, 25 Eylül 2026'da birkaç PC ayarı/konfigürasyonu için OpenAI veya
Anthropic kotası tüketmeyen yerel bir model sordu. Çalışmayı İkinci Beyin
klasöründe yürütmeyi düşünüyor. İlk ölçüm ve öneri aşağıdadır; aynı gün
sonraki oturumda kurulum ve yerel yanıt testi yapıldı.

## 25 Eylül 03:17 civarı yerel ölçüm

- Windows PC: AMD Ryzen 7 2700X, yaklaşık 7,91 GB fiziksel RAM; ölçüm anında
  yaklaşık 0,49 GB boş RAM.
- NVIDIA RTX 3060 Ti: 8.192 MiB VRAM, ölçüm anında 7.181 MiB boş.
- Disk boşluğu: C: yaklaşık 13,8 GB, D: yaklaşık 127,6 GB.
- `Get-Command` yolunda Ollama, LM Studio CLI ve OpenCode bulunmadı. Bu,
  uygulamaların makinede hiçbir yerde bulunmadığını kanıtlamaz.

## Kaynaklı öneri

- İlk aday: [Qwen3.5 4B](https://huggingface.co/Qwen/Qwen3.5-4B),
  [Ollama'daki `qwen3.5:4b`](https://ollama.com/library/qwen3.5:4b) etiketiyle.
  Ollama dağıtımı 3,4 GB model boyutu ve araç kullanımı bildiriyor. 8 GB
  VRAM için makul başlangıç; bağlam belleği ve çalışma zamanı da alan
  kullandığı için 256K azami bağlamı hedeflememek, küçük bağlamla başlamak
  gerekir. Bu makinedeki gerçek hız ve araç kalitesi henüz sınanmadı.
- [OpenCode](https://opencode.ai/docs/providers) yerel Ollama uç noktasını
  (`http://localhost:11434/v1`) sağlayıcı olarak kullanabiliyor. Böylece
  modelin dosya/komut araçlarına eriştiği ajan oturumu İkinci Beyin
  klasöründe açılabilir. Model tek başına PC ayarı yapmaz; araçları ajan
  çalıştırır.
- Büyük `qwen3.5:9b` etiketi Ollama'da 6,6 GB görünüyor. 8 GB VRAM ve
  şu anki çok düşük boş sistem RAM'iyle ilk tercih değildir. 4B de aktif
  Opus/Claude ve tarayıcı yükü sürerken denenmemeli; önce bellek rahatlamalı.
- Model ağırlıkları vault dışında, tercihen boş alanı bol D: üzerinde
  saklanmalı; vault çalışma klasörü olabilir. Bu depolama/çalışma düzeni
  öneridir, uygulanmış karar değildir.

## Sınır

Yerel 4B model, düşük riskli ayar incelemesi ve komut taslağı için adaydır.
Yönetici yetkisi isteyen veya geri alınması güç PC değişikliklerinde komut
ve beklenen etki ayrıca gözden geçirilmelidir. Yukarıdaki donanım ve kurulum
durumu 03:17 ölçümüne aittir; güncel kurulum aşağıdadır.

## 25 Eylül sabahı kurulum ve doğrulama

- Ollama 0.34.4 ve OpenCode Desktop 1.18.32 Windows kullanıcı hesabına
  kuruldu. `C:\Users\Anj\Desktop\OpenCode.lnk` kısayolu OpenCode.exe'ye
  işaret ediyor.
- Ollama model dosyaları `D:\AI\LocalAI\Ollama\models` içinde. `qwen3.5:4b`
  indirildi; aynı ağırlıkları kullanan `qwen3.5:4b-pc` profili
  `D:\AI\LocalAI\Ollama\Qwen3.5-4B-PC.Modelfile` ile 16.384 bağlam
  sınırında oluşturuldu.
- Vault kökündeki [OpenCode proje ayarı](../../opencode.json) varsayılan ve
  küçük modeli `ollama/qwen3.5:4b-pc` seçiyor, yalnız `ollama` sağlayıcısını
  açıyor ve `http://127.0.0.1:11434/v1` adresine bağlanıyor. Kullanıcının
  genel `opencode.jsonc` ayarı değiştirilmedi. Bu proje için OpenAI veya
  Anthropic sağlayıcısı seçilemeyecek.
- Yerel Ollama `/api/chat` testi `HAZIR` yanıtıyla tamamlandı; model %100
  GPU üzerinde ve 16.384 bağlamla yüklendi, test sonunda bellekten çıkarıldı.
  İlk yükleme 81,4 saniye sürdü. OpenCode arayüzünde ajan/araç kalitesi
  henüz gerçek bir PC işiyle sınanmadı. Projeyi arayüzden Yavuz seçecek.

Kaynak: 25 Eylül yerel `ollama list`, `ollama show`, `/v1/models`, `/api/chat`,
`ollama ps`, Windows kısayol ve OpenCode proje ayarı kontrolleri;
[OpenCode Ollama sağlayıcı belgeleri](https://opencode.ai/docs/providers),
[OpenCode yapılandırma belgeleri](https://dev.opencode.ai/docs/config/).
