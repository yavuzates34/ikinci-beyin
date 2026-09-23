---
{
  "kind": "fact",
  "project": "codex-usage-display",
  "visibility": "internal"
}
---
# Codex kullanım göstergesi araştırması

## Sonuç

Codex masaüstü uygulamasının kalıcı kabuğuna bir bar ekleyen belgelenmiş resmî bir skill veya plugin bulunamadı. Bu, resmî plugin mimarisinin skill, MCP aracı, yaşam döngüsü hook'u ve etkileşim içi UI kaynağı sunmasına; kalıcı uygulama chrome'u için bir genişletme noktası belgelememesine dayanan bir çıkarımdır. Plugin dizini aramasında da bu işe özel bir sonuç çıkmadı.

Codex'in resmî yerel app-server protokolü `account/rateLimits/read` ve `account/rateLimits/updated` üzerinden `usedPercent`, `windowDurationMins` ve `resetsAt` alanlarını sağlar. Bu nedenle harici, yerel bir Windows göstergesi güvenilir biçimde yapılabilir.

## Adaylar

- **D1NOOO/codex-usage-monitor v0.1.9:** Codex/ChatGPT penceresini izleyen tıklama-geçirgen overlay; üst başlık çubuğu veya sağ alt konum; pencereye bağlı ya da masaüstünde sürekli üstte mod. Yerel `codex app-server` ile konuşur, `auth.json` okumaz ve telemetri içermez. Kullanıcının tarif ettiği uygulamaya ilişik bar davranışına en yakın adaydır. Resmî değildir, yürütülebilir dosya imzasızdır ve protokol değişikliklerinden etkilenebilir. 2026-08-20 yayını; ZIP SHA-256: `d53b7e41e427c8e0fec6d01da0eb31350cfd6e028ce744c59c8f2b89a21e6130`.
- **ognjeeen/codex-usage-widget v1.7.1:** Sürekli üstte masaüstü widget'ı veya bildirim alanı yanında görev çubuğu etiketi; iki dakikada bir yenileme. Yalnız yerel Codex CLI app-server'ı ile konuştuğunu, kimlik bilgisi okumadığını ve telemetri kullanmadığını bildirir. Daha güncel ve daha genel amaçlı öneridir; Codex pencere çerçevesine bağlanmaz. 2026-09-21 yayını; ZIP SHA-256: `32674e67d2e4d952aabdb26eca8884d62c291030dd8a09e82607c30b42ed9cea`.
- **upstream-ray/codex-usage-monitor v1.9.1:** Windows görev çubuğunda iki kullanım satırı gösterir; ancak Codex `auth.json` dosyasını doğrudan okur. İlk iki adaya göre daha geniş kimlik bilgisi erişimi nedeniyle öncelik verilmedi.

## Context penceresi ek araştırması

Codex App Server aktif thread için `thread/tokenUsage/updated` olayı yayımlar. Resmî Codex kaynak kodu bağlam doluluğunda `last_token_usage.total_tokens` ile `model_context_window` değerlerini kullanır; uzun oturumlarda compaction sonrası değerlerin yeniden değerlendirilmesi gerekir.

`D1NOOO/codex-usage-monitor` v0.1.9 context doluluğu göstermez; kaynak kodu `thread/tokenUsage/updated` bildiriminden açıkça vazgeçer ve yalnız `account/rateLimits/read` kullanır.

- **wtf12345789/codex-context-hud v0.3.0:** Microsoft Store Codex Desktop'ın mevcut native context halkasını korur; hemen soluna kalan hesap kotasını ve compaction göstergesini ekler. Uygulama dosyalarını değiştirmez ancak özel başlatıcı ve yalnız loopback'e bağlanan yerel debugging endpoint üzerinden renderer'a bağlanır. En bütünleşik görünüm budur; Codex arayüz değişikliklerine karşı daha kırılgandır. 2026-09-09 yayını; portable ZIP SHA-256: `ec10bb0083e76334d99c111c184bdd9290fd600ba2f5bb4c55409cff4fb7065b`.
- **libaie/codex-usage-widget v1.1.1 (ön sürüm):** Ekran kenarına yapışabilen sürekli üstte bir halka; kalan kota, context kullanımı ve son aktif görevleri birlikte gösterir. Yalnız yerel Codex oturum kayıtlarını okur, kimlik bilgisi/API/telemetri kullanmaz. Codex penceresine bağlanmaz ve sayılar yerel tahmindir. Windows ZIP SHA-256: `b213ceccd12c1f09db06476acaa37593cb516297fd24f6d8845b8f0eaf3e73a9`.

## Dinamik proje, oturum ve hesap geçişi denetimi

Yavuz'un hedeflediği davranış, Codex'in alt composer çubuğunda kalıcı duran tek göstergenin soldan seçilen aktif proje/oturuma göre context değerini, uygulamadaki aktif hesaba göre de kalan kotayı otomatik değiştirmesidir.

`codex-context-hud` v0.3.0 kaynak kodu aktif thread kimliğini ve arayüzdeki görev seçimini izler; görev değişiminde context/compaction durumunu yeniden yükler. Bu nedenle proje ve oturum geçişi hedef davranışla uyumludur. Kota için başlangıçta `account/rateLimits/read` çağırır ve `account/rateLimits/updated` bildirimlerini işler. Ancak `account/updated` olayını dinlemez, hesap değişirken mevcut kota değerini temizlemez ve yeni hesap için zorunlu yeniden okuma yapmaz. Sonuç olarak uygulama yeni rate-limit verisi yayımlarsa kota güncellenebilir, fakat canlı hesap değişiminin her durumda doğru ve anında işleyeceği mevcut sürümde garanti değildir; kısa süre eski hesabın kotası kalabilir.

Tam hedef davranış için en küçük güvenli uyarlama, `account/updated` geldiğinde kota durumunu bilinmeyene sıfırlayıp `account/rateLimits/read` çağrısını yeniden başlatmak; çıkış durumunda göstergede hesap olmadığını belirtmek ve dönüşü aktif hesapla sınamaktır.

## Yerel uygunluk

2026-09-22 kontrolünde bilgisayarda `codex-cli 0.155.1` PATH üzerinde bulundu, .NET Framework 4.8.1 mevcut, yerel canlı kullanım sorgusu başarılı oldu ve aktif Codex oturum kaydında context kullanım alanları (`last_token_usage.total_tokens`, `model_context_window`) doğrulandı. Dolayısıyla hem kota hem context gösterimi teknik olarak mümkün.

## Öneri

Kota ve context'in Codex arayüzünde birlikte görünmesi öncelikliyse `codex-context-hud` en yakın tabandır; proje/oturum geçişini karşılar, fakat garantili canlı hesap değişimi için küçük bir kaynak yaması ve test gerekir. Uygulamaya müdahalesi daha düşük, bağımsız ve taşınabilir bir yüzey öncelikliyse `libaie/codex-usage-widget` seçilmeli. D1NOOO yalnız kota göstergesi istendiğinde uygun kalır. Kurulumdan önce yayın arşivi SHA-256 ile doğrulanmalı.

## Kaynaklar

- [OpenAI Codex App Server](https://learn.chatgpt.com/docs/app-server)
- [OpenAI plugin architecture](https://developers.openai.com/plugins/concepts/plugins)
- [D1NOOO/codex-usage-monitor](https://github.com/D1NOOO/codex-usage-monitor)
- [ognjeeen/codex-usage-widget](https://github.com/ognjeeen/codex-usage-widget)
- [upstream-ray/codex-usage-monitor](https://github.com/upstream-ray/codex-usage-monitor)
- [OpenAI Codex token usage implementation](https://github.com/openai/codex/blob/main/codex-rs/tui/src/token_usage.rs)
- [Codex Context HUD](https://github.com/wtf12345789/codex-context-hud)
- [libaie Codex Usage Widget](https://github.com/libaie/codex-usage-widget)
