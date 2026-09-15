#!/usr/bin/env python3
"""Oturum arsivinde sozcuksel arama.

Aramalarin cogu anlamsal degil sozcukseldir ("whisper neydi", "ffmpeg hatasi").
Bu katman bedavadir: dosyalar zaten diskte ve zaten guncel, kurulacak servis
ya da senkron tutulacak indeks yok. Anlamsal aramaya (anlam.py) ancak burasi
yetmediginde gidilmeli.

Ham `grep` neden yetmiyor: dosyalar JSON. grep sana kacis karakterleriyle dolu,
meta veriyle sarili, kilometrelerce tek satir verir; icinde base64 gomulu
gorseller de vardir. Burada JSON cozulup mesajin icindeki metne bakiliyor.

Kullanim:
    python araclar/ara.py "whisper"
    python araclar/ara.py "ffmpeg" --kapsam proje       # sadece bu klasor
    python araclar/ara.py "hook" --rol kullanici        # sadece benim yazdiklarim
    python araclar/ara.py "mem0" --tam                  # eslesmenin tum mesajini bas
    python araclar/ara.py "izle\\.py" --re              # duzenli ifade

Sonra: python araclar/omurga.py <oturum-id>   -> o oturumun kemigi
       python araclar/oku.py <oturum-id> --saat 14:00-14:30  -> tam dokum

Ilgili: BEYIN.md
"""

import argparse
import re
import sys
from datetime import datetime

import kayit


def kes(metin: str, bas: int, son: int, pencere: int = 110) -> str:
    """Eslesmeyi ortalayan tek satirlik baglam."""
    b = max(0, bas - pencere)
    s = min(len(metin), son + pencere)
    parca = metin[b:s].replace("\n", " ")
    parca = re.sub(r"\s{2,}", " ", parca).strip()
    return ("..." if b > 0 else "") + parca + ("..." if s < len(metin) else "")


def main() -> int:
    kayit.utf8_zorla()
    ap = argparse.ArgumentParser(description="Oturum arsivinde arama")
    ap.add_argument("desen", help="aranacak metin (varsayilan: duz metin)")
    ap.add_argument(
        "--kapsam", default="hepsi", choices=["proje", "claude", "codex", "hepsi"]
    )
    ap.add_argument("--rol", default="hepsi", choices=["kullanici", "model", "hepsi"])
    ap.add_argument("--son", type=int, help="sadece en yeni N oturum")
    ap.add_argument("--sonra", help="YYYY-AA-GG tarihinden sonrasi")
    ap.add_argument("--tam", action="store_true", help="eslesen mesajin tamamini bas")
    ap.add_argument("--re", action="store_true", help="deseni duzenli ifade say")
    ap.add_argument("--yeni-once", action="store_true",
                    help="en yeniden eskiye sirala (varsayilan: eskiden yeniye, "
                         "boylece son soz en altta kalir)")
    a = ap.parse_args()

    try:
        kalip = re.compile(
            a.desen if a.re else re.escape(a.desen), re.IGNORECASE | re.MULTILINE
        )
    except re.error as e:
        print(f"HATA: gecersiz duzenli ifade: {e}", file=sys.stderr)
        return 1

    havuz = kayit.oturumlar(a.kapsam)
    if not havuz:
        print(f"HATA: '{a.kapsam}' kapsaminda oturum kaydi yok", file=sys.stderr)
        return 1
    if a.son:
        havuz = havuz[: a.son]
    if a.sonra:
        try:
            esik = datetime.fromisoformat(a.sonra).astimezone()
        except ValueError:
            print("HATA: --sonra bicimi YYYY-AA-GG olmali", file=sys.stderr)
            return 1
        havuz = [o for o in havuz if o.an >= esik]

    # Varsayilan sira ESKIDEN YENIYE. Gerekce: bir konu hakkinda en son ne
    # soylendigi, ilk ne soylendiginden daha baglayicidir. Ekranda en altta
    # kalan satir en gunceli olsun ki eski bir cumle nihai karar sanilmasin.
    havuz = sorted(havuz, key=lambda o: o.an, reverse=a.yeni_once)

    oturum_sayisi = eslesme = 0
    en_yeni = None
    for o in havuz:
        vurus = []
        try:
            for m in kayit.mesajlar(o):
                if a.rol != "hepsi" and m.rol != a.rol:
                    continue
                for bul in kalip.finditer(m.metin):
                    vurus.append((m, bul.start(), bul.end()))
                    break  # mesaj basina bir vurus yeter
        except (OSError, ValueError):
            continue
        if not vurus:
            continue
        oturum_sayisi += 1
        eslesme += len(vurus)
        print(f"\n=== {o.kaynak} {o.kisa} | {o.proje} | {o.an:%d.%m.%Y} "
              f"| {len(vurus)} eslesme ===")
        for m, b, s in vurus:
            etiket = "BEN" if m.rol == kayit.KULLANICI else "MODEL"
            if en_yeni is None or m.an > en_yeni[0]:
                en_yeni = (m.an, o, m)
            print(f"  [{m.an:%d.%m.%Y %H:%M}] {etiket}: "
                  f"{m.metin if a.tam else kes(m.metin, b, s)}")

    # Sessiz basari yasak: ne bulundugunu sayiyla soyle.
    print(f"\n# '{a.desen}' -> {oturum_sayisi} oturumda {eslesme} mesaj "
          f"({len(havuz)} oturum tarandi, kapsam: {a.kapsam})")
    if en_yeni:
        an, o, m = en_yeni
        etiket = "BEN" if m.rol == kayit.KULLANICI else "MODEL"
        # En son soylenen, en baglayici olandir. Ayrica goster ki siralamayi
        # gozden kacirip eski bir cumleyi nihai karar sanma.
        print(f"# EN GUNCEL: {an:%d.%m.%Y %H:%M} | {o.kaynak} {o.kisa} "
              f"| {o.proje} | {etiket}")
        print(f"#   python araclar/oku.py {o.kisa} --saat {an:%H:%M}")
    if not eslesme:
        print("# Sozcuksel arama bos dondu. Kelimeyi hatirlamiyorsan: "
              "python araclar/anlam.py \"tarif\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
