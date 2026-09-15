#!/usr/bin/env python3
"""Bir oturumun tam dokumu - istenirse dar bir zaman araliginda.

Uclunun son adimi. Mantik izle.py ile ayni: once ucuz ve genis tarama
(ara.py / anlam.py), sonra dar aralikta yakin bakis (burasi). Bir oturumun
tamamini bagla yuklemek pahalidir; ilgili yarim saati yuklemek degildir.

Kullanim:
    python araclar/oku.py 3557db3e                      # tamami
    python araclar/oku.py 3557db3e --saat 14:00-14:30   # aralik
    python araclar/oku.py 3557db3e --saat 14:12         # o anin +-15 dakikasi
    python araclar/oku.py 3557db3e --rol kullanici      # sadece benim yazdiklarim
    python araclar/oku.py 3557db3e --son 10             # son 10 mesaj
    python araclar/oku.py --liste                       # oturumlari listele

Ilgili: BEYIN.md, ara.py, anlam.py, omurga.py
"""

import argparse
import re
import sys
from datetime import timedelta

import kayit


def aralik_coz(ifade: str):
    """'14:00-14:30' -> (840, 870) dakika. '14:12' -> +-15 dakika."""
    kalip = r"^(\d{1,2}):(\d{2})$"
    if "-" in ifade:
        bas, son = ifade.split("-", 1)
        b, s = re.match(kalip, bas.strip()), re.match(kalip, son.strip())
        if not (b and s):
            raise ValueError("bicim: SS:DD-SS:DD")
        return (int(b[1]) * 60 + int(b[2]), int(s[1]) * 60 + int(s[2]))
    t = re.match(kalip, ifade.strip())
    if not t:
        raise ValueError("bicim: SS:DD ya da SS:DD-SS:DD")
    orta = int(t[1]) * 60 + int(t[2])
    return (max(0, orta - 15), min(24 * 60, orta + 15))


def main() -> int:
    kayit.utf8_zorla()
    ap = argparse.ArgumentParser(description="Oturum dokumu")
    ap.add_argument("oturum", nargs="?", help="oturum kimliginin bas kismi")
    ap.add_argument("--saat", help="SS:DD-SS:DD ya da SS:DD (+-15 dk)")
    ap.add_argument("--rol", default="hepsi", choices=["kullanici", "model", "hepsi"])
    ap.add_argument("--son", type=int, help="sadece son N mesaj")
    ap.add_argument("--liste", action="store_true")
    ap.add_argument("--kapsam", default="hepsi",
                    choices=["proje", "claude", "codex", "hepsi"])
    a = ap.parse_args()

    if a.liste or not a.oturum:
        havuz = kayit.oturumlar(a.kapsam)
        print(f"# {len(havuz)} oturum ({a.kapsam})\n")
        for o in havuz[:60]:
            print(o.satir())
        if len(havuz) > 60:
            print(f"\n# ...{len(havuz) - 60} oturum daha")
        return 0 if a.liste else 1

    o = kayit.oturum_bul(a.oturum, a.kapsam)
    if not o:
        print(f"HATA: '{a.oturum}' ile baslayan oturum yok "
              f"(bakmak icin: python araclar/oku.py --liste)", file=sys.stderr)
        return 1

    pencere = None
    if a.saat:
        try:
            pencere = aralik_coz(a.saat)
        except ValueError as e:
            print(f"HATA: {e}", file=sys.stderr)
            return 1

    secilen = []
    for m in kayit.mesajlar(o):
        if a.rol != "hepsi" and m.rol != a.rol:
            continue
        if pencere:
            dk = m.an.hour * 60 + m.an.minute
            if not (pencere[0] <= dk <= pencere[1]):
                continue
        secilen.append(m)
    if a.son:
        secilen = secilen[-a.son:]

    print(f"# {o.kaynak} {o.kimlik} | {o.proje} | {o.an:%d.%m.%Y}")
    if pencere:
        print(f"# aralik: {timedelta(minutes=pencere[0])} - "
              f"{timedelta(minutes=pencere[1])}")
    print()
    harf = 0
    for m in secilen:
        etiket = "BEN" if m.rol == kayit.KULLANICI else "MODEL"
        harf += len(m.metin)
        print(f"--- [{m.an:%d.%m %H:%M}] {etiket} ---")
        print(m.metin)
        print()

    # Sessiz basari yasak: ne dokuldugunu sayiyla soyle.
    print(f"# {len(secilen)} mesaj, {harf / 1024:.1f} KB")
    if not secilen:
        print("# Filtre bos dondu. --saat araligini genislet ya da kaldir.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
