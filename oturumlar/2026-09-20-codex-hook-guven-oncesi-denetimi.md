# Codex hook güven öncesi denetimi — 20 Eylül 2026
kapanan-oturum: 01a0bb8e-de58

Bu kısa Desktop oturumu, proje hook'larının güven verilmeden önce gerçekten
tetiklenip tetiklenmediğini ölçtü. Kullanıcı önce `/hooks` yazdı; Desktop bunu
hook tarayıcısı olarak açmak yerine normal mesaj olarak modele gönderdi. Model
yapılandırmayı okuyup üç hook grubunu listeledi ve başlangıç hook'unun
çalıştığını sandı. İkinci turdaki doğrudan sınamada ise hiçbir saat ya da başka
hook satırı gelmediğini söyledi (codex 01a0bb8e-de58 · 20.09 00:35).

## Sonuç ve sonradan yapılan düzeltme

İlk gece taslağı, `UserPromptSubmit` hook'unun yalnız bazı turlarda çalışıyor
olabileceğini önerdi. Bu çıkarım **elendi**: ham kayıttaki ilk tur harita ve
saat satırları `custom_tool_call_output` idi; yani hook enjeksiyonu değil,
modelin kendi çalıştırdığı komutların çıktısıydı. Güven verilmeden önce gerçek
hook zinciri sessizce atlanıyordu ([[olculmus-bulgular]] §14).

Daha sonra CLI TUI'de güven verildi. Yeni Desktop ve normal `codex exec`
oturumlarında `SessionStart` ile `UserPromptSubmit` çıktıları
`role=developer`, `hooks.additional_context` olarak ham kayıtta doğrulandı
([[olculmus-bulgular]] §14.2). Dolayısıyla bu oturumun kalıcı değeri, yanlış
pozitif ile gerçek hook enjeksiyonu arasındaki ayrımı göstermesidir.

## Yapılanlar, elenenler ve açık kalan

- Dosya ya da yapılandırma değiştirilmedi; yalnız teşhis yapıldı.
- “Model hook'lar etkin dedi, demek ki çalışıyor” çıkarımı elendi. Model
  yapılandırmayı okuyabilir; kanıt ham kayıttaki içerik türüdür.
- Bu oturumdan ayrı kalan testler: Codex'te gerçek `PreCompact` olayı ve canlı
  %50/%70 erken-devir eşiği.

