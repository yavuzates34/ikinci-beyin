#!/usr/bin/env python3
"""Kalici katman bakim olcumu - budama ADAYLARINI bulur, hicbir sey silmez.

NEDEN VAR
Gece derleyicisi kalici notlarin boyutunu olcuyordu ama kimse bu olcume gore
davranmiyordu: 19.09.2026'da notlar 118 KB'a cikmisti, AGENTS.md'deki 65 KB
secmeli okuma ve 100 KB bolme esikleri sessizce asilmisti. Buyuk dosyalar
bolunmuyor, kapanmis tarihce sicak katmanda kaliyor, haritada gorunmeyen not
birikiyordu (codex 01a0ba74 · 19.09 19:26).

KARAR (kullanici, 19.09.2026): derleyici bakim ADAYLARINI raporlar ve oturum
basinda uyarir. Kapanmis tarihce oturumlar/ altina tasinir; otomatik silme
yok. Bakimi kullanici yapar, ileride yetkili orkestrator ajanlar da yapabilir
(claude 5c600e7e · 19.09 20:12).

Olcutler deterministiktir, model gerektirmez:
- notlar/ toplam boyutu ve iki esik (65 KB secmeli okuma, 100 KB bolme)
- buyuk notlar (BUYUK_NOT'u asan)
- haritasiz notlar: BEYIN.md'de [[ad]] olarak gecmeyen notlar/*.md
- acik-uclar.md icindeki kapanmis (ustu cizili) maddelerin boyutu
- yetim gece taslaklari: oturumu kapanmis ama oto-<id>.md dosyasi duran

Kullanim:
    python araclar/bakim.py          # olcumu ekrana bas
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kayit  # noqa: E402

KOK = kayit.PROJE_KOKU
SECMELI_ESIK = 65 * 1024
BOLME_ESIK = 100 * 1024
BUYUK_NOT = 12 * 1024
# Madde basi: "1. ", "- ", "* " ile baslayan satir (girinti yok)
MADDE = re.compile(r"^(?:\d+\.|[-*])\s+")


def _kapanmis_madde_bayti(metin: str) -> int:
    """acik-uclar.md: ustu cizili (~~) baslayan ust duzey maddelerin boyutu.
    Bir madde, bir sonraki ust duzey madde ya da baslik gelene kadar surer."""
    toplam, kapali, bayt = 0, False, 0
    for satir in metin.splitlines(keepends=True):
        if MADDE.match(satir) or satir.startswith("#"):
            if kapali:
                toplam += bayt
            govde = MADDE.sub("", satir, count=1).lstrip()
            kapali = bool(MADDE.match(satir)) and govde.startswith("~~")
            bayt = 0
        bayt += len(satir.encode("utf-8"))
    if kapali:
        toplam += bayt
    return toplam


def olc() -> dict:
    notlar = sorted((KOK / "notlar").glob("*.md"))
    boyut = {p.stem: p.stat().st_size for p in notlar}
    toplam = sum(boyut.values())
    harita = (KOK / "BEYIN.md").read_text(encoding="utf-8", errors="replace")
    haritasiz = [ad for ad in boyut if f"[[{ad}]]" not in harita]

    acik = KOK / "notlar" / "acik-uclar.md"
    kapanmis = (_kapanmis_madde_bayti(acik.read_text(encoding="utf-8"))
                if acik.exists() else 0)

    kapali = kayit.kapanmis_kimlikler()
    # Taslak dosyasinin adindaki kimlik, kapanis isaretlerinden birinin
    # ONEKI ise yetimdir (8 ve 13 haneli isaretler birlikte calisir).
    yetim = sorted(p.name for p in (KOK / "oturumlar").glob("oto-*.md")
                   if any(p.stem[4:].startswith(i) or i.startswith(p.stem[4:])
                          for i in kapali))

    return {
        "notlar_kb": round(toplam / 1024, 1),
        "esik": ("bolme" if toplam > BOLME_ESIK
                 else "secmeli" if toplam > SECMELI_ESIK else "tamam"),
        "buyuk": [f"{ad} ({b / 1024:.0f} KB)"
                  for ad, b in sorted(boyut.items(), key=lambda x: -x[1])
                  if b > BUYUK_NOT],
        "haritasiz": haritasiz,
        "acik_uclar_kapanmis_kb": round(kapanmis / 1024, 1),
        "yetim_taslak": yetim,
    }


def uyarilar(b: dict) -> list[str]:
    """Olcumden oturum basi uyarilari. Esik asilmamissa ve aday yoksa bos."""
    u = []
    if b.get("esik") in ("secmeli", "bolme"):
        esik = "100 KB bolme" if b["esik"] == "bolme" else "65 KB secmeli okuma"
        buyuk = ", ".join(b.get("buyuk", [])[:4])
        u.append(f"KALICI KATMAN BAKIM ESIGINI ASTI: notlar/ {b['notlar_kb']} KB "
                 f"({esik} esigi). En buyukler: {buyuk}. Budama adaylarini "
                 "kullaniciyla gozden gecir; silme yok, tarihce oturumlar/ altina")
    if b.get("haritasiz"):
        u.append("HARITASIZ NOT: " + ", ".join(b["haritasiz"])
                 + " - BEYIN.md haritasina satir eklenmeli")
    if b.get("acik_uclar_kapanmis_kb", 0) > 4:
        u.append(f"acik-uclar.md {b['acik_uclar_kapanmis_kb']} KB kapanmis madde "
                 "tasiyor - tarihce adayi")
    if b.get("yetim_taslak"):
        u.append("YETIM GECE TASLAGI (oturumu kapanmis): "
                 + ", ".join(b["yetim_taslak"]) + " - birlestirilip kaldirilmali")
    return u


if __name__ == "__main__":
    kayit.utf8_zorla()
    sonuc = olc()
    print(json.dumps(sonuc, ensure_ascii=False, indent=1))
    for satir in uyarilar(sonuc):
        print("! " + satir)
