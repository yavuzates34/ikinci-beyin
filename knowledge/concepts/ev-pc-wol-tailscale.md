---
{
  "kind": "fact",
  "visibility": "internal"
}
---
# Ev PC'sini dışarıdan uyandırma (WoL + Tailscale rölesi)

## Amaç ve sonuç
Yavuz dışarıdayken evdeki PC kapalıysa/uykudaysa onu uzaktan açmak istiyordu. 25 Eylül 2026 sabahı uçtan uca kuruldu ve doğrulandı: iPhone (mobil veri + Tailscale) → evdeki oppo-a52 (Termux wake.py) → PC S5'ten açıldı, otomatik giriş yaptı, başlangıç uygulamaları çalıştı. Wake adresi iPhone'da favorilere eklendi.

## Ağ ve donanım (kullanıcı beyanı + yerel ölçüm)
- Fiber → Huawei OptiXstar HG8010H (yalnız ONT) → ZTE ZXHN H3600P V9 ana router (192.168.1.1). Kaynak: C:\Users\Anj\Documents\home-network-notes.md ve modem arayüz ekran görüntüleri (kullanıcının paylaştığı ekranlar).
- PC: ASUS PRIME B450M-A II (BIOS 4402), Realtek PCIe GbE kablolu, H3600P LAN2. MAC C8:7F:54:70:6E:FA, DHCP bağlama ile 192.168.1.3 sabitlendi. Yerel komutlarla doğrulandı.
- Ev yardımcısı: oppo-a52 (evde kalacak), Wi-Fi MAC 56:0a:73:11:f0:74 → 192.168.1.6 sabitlendi. Dışarıdaki cihaz: iPhone 14 Pro Max.
- Kritik bulgu: modem WAN IP 10.170.14.27 (CGNAT). Dışarıdan direkt port yönlendirme ÇALIŞMAZ. Bu yüzden Tailscale röle yolu seçildi. Vercel/Netlify serverless ile olmaz; VDS ancak buluşma noktası olur.

## Yapılan ayarlar
- BIOS (kullanıcı uyguladı): Power On By PCI-E Enabled, ErP Ready Disabled, Restore AC Power Loss Power On, Energy Star/CEC/RTC Disabled.
- Windows sürücü (yönetici PowerShell ile uygulandı, geri okumayla doğrulandı): Energy-Efficient Ethernet, Green Ethernet, Power Saving Mode → Disabled. Wake on Magic Packet ve S5WakeOnLan Enabled kaldı.
- H3600P: DHCP havuzu .2–.249; DHCP bağlama PC (.3) + AndroidEv (.6); Port yönlendirme UDP 9→192.168.1.3 Açık (ev içi için; CGNAT nedeniyle dışarıdan etkisiz).
- Otomatik giriş: netplwiz tiki kaldırıldı (önce PasswordLess registry DevicePasswordLessBuildVersion=0 gerekti; hesap Microsoft bağlantılı çıktı). Uykuda şifre sorma: Hiçbir zaman.
- Başlangıç klasörüne eklendi: ChatGPT Classic, Codex, Claude (Store AppID'leri explorer shell:AppsFolder ile), AnyDesk (Downloads'daki portable exe).
- oppo-a52: Tailscale (100.68.28.26), WoL uygulaması (PC-Anj kaydı), Termux (F-Droid) + C:\Users\Anj\Documents\android-wake-server\wake.py → 0.0.0.0:8080 dinliyor. iPhone Tailscale (100.67.87.92) ile /ping testi 'ok' verdi.

## Test sonuçları
- Uyku (S3) + ev Wi-Fi WoL: önce başarısızdı (BIOS yapılmamış + EEE/Green/PowerSaving Enabled idi); düzeltmelerden sonra çalıştı.
- S5 tam kapatma + iPhone mobil veri üzerinden wake adresi: 'woken' döndü, PC açıldı. DOĞRULANDI.

## Açık kalanlar
1. Termux kalıcılığı: oppo yeniden başlarsa wake.py açılmıyor; Termux:Boot + boot betiği gerekli.
2. AnyDesk katılımsız erişim şifresi kullanıcı tarafından AnyDesk içinde belirlenecek (bana verilmedi, vault'a yazılmadı).
3. ASUS DSL-AC750 AP Ethernet'siz/kapalı; salon Wi-Fi hız sorunu ayrı iş.
4. Qwen yerel model işi kullanıcı kararıyla rafta: indirme/kurulum yapılmadı.

## Güvenlik sınırları
IMEI, seri no, parolalar vault'a yazılmadı. wake.py içindeki token yalnız PC'deki dosyadadır, bu nota alınmadı. Yönetici panel şifresi istenmedi/alınmadı.

