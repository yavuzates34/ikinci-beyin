# Proje egemenliği

Her klasör kendi devleti. Bu notun tamamı bir kuraldır, gözlem değil.

> Merkez: [[BEYIN]] · İlgili: [[kullanici-baglami]] · [[iki-ajan-calismasi]] · [[ikinci-beyin-mimarisi]]

---

## Kural

**Her proje, her klasör, her vault ayrı bir devlet gibidir. Birbirlerinin iç
süreçlerine karışamazlar.** Okuyabilirler, inceleyebilirler, analiz
edebilirler — ama kullanıcı **özellikle söylemediği sürece** müdahale
edemezler. (claude 7f10f7a3 · 17.09 02:54)

Kuralın yönü çift taraflıdır:

- Playground'daki ajan, Nar Ajans klasörüne yazamaz.
- Nar Ajans'taki ajanlar da buraya yazamaz; okuyabilirler, değiştiremezler.

## Nar Ajans örneği — kuralın doğduğu yer

16–17 Eylül'de bu klasörden Nar Ajans klasörüne müdahale edildi: klasör yapısı
düzenlendi, hafıza mimarisi kuruldu, hook'lar yazıldı. Kullanıcının tanımıyla
bu **bir defalık bir "start verme" hareketiydi** ve bitti.

Bundan sonra orada gerçekleşecek her süreç, o projenin kendi ajanları
tarafından yürütülür. Buradan oraya müdahale yok. Oranın açık uçları,
denetimi, `/compact` testi, mükerrer oturum sorunu — hiçbiri bu klasörün
işi değil.

Bu yüzden [[acik-uclar]] içindeki "Nar Ajans'tan devreden" başlığı **devredilen
iş listesi değil, sadece tarihsel kayıttır.** O maddeler burada kapatılmaz.

## Neden böyle

İki sebep, biri pratik biri yapısal:

- **Pratik:** iki ajan aynı dosyaya farklı bağlamlardan yazarsa, hangisinin
  neyi neden değiştirdiği kaybolur. Bkz. [[iki-ajan-calismasi]].
- **Yapısal:** bir klasörün hafızası o klasörde çalışan ajanın kararlarıyla
  oluşur. Dışarıdan yazılan bir karar, o klasörde **kaynağı olmayan bir
  iddiaya** dönüşür — ve hatırlayan bir sistemin en tehlikeli hâli,
  uydurduğunu hatırlıyor sanmasıdır.

## Sınır nerede

| Yapılabilir | Yapılamaz |
|---|---|
| Okumak, listelemek, analiz etmek | Dosya yazmak, düzenlemek, silmek |
| Oradaki yapıdan ders çıkarıp buraya yazmak | Oraya not/karar/görev yazmak |
| Kullanıcı açıkça isterse müdahale | Kendi inisiyatifiyle müdahale |

Şüphedeysen: **sor.** İzin bir kez verilir, her seferinde yenilenir; bir
projede verilen izin başka bir projeye geçmez.
