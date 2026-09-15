#!/usr/bin/env python3
"""Oturum omurgasi - bir oturumun kaydindan sadece kullanicinin mesajlari.

Neden: kapanis aninda model baglam yuku altindadir; uzun bir oturumun
ortasinda konusulani kendiliginden gundeme getirme ihtimali dusuktur.
Bu arac kapanisi HATIRLAMAKTAN OKUMAYA cevirir. Kayit zaten diskte ve
zaman damgali duruyor; ozet yazmadan once omurga okunur.

Omurga = konusmanin iskeleti. Sen soruyu sorarsin, yonu verirsin; model
cevaplari ve arac ciktilari o iskelete asilan ettir. Iskeleti tek basina
okuyunca konusmanin sekli cikar: ne soruldu, ne kararlastirildi, hangi
sirayla. Olculdu: kullanicinin mesajlari kaydin ~%3'u (336 KB -> 9.8 KB).

Sinir: omurga bir ICINDEKILER LISTESIDIR, kaydin kendisi degil. Ne olculdugu,
ne kuruldugu model cevaplarindadir. Kapanista baglam zaten yuklu oldugu icin
bu yeterlidir; eski bir oturumu okurken degildir - orada oku.py gerekir.

Kullanim:
    python araclar/omurga.py             # bu oturum (en son yazilan kayit)
    python araclar/omurga.py --liste     # bu projedeki tum oturumlar
    python araclar/omurga.py <oturum-id>

Ilgili: BEYIN.md, CLAUDE.md (kapanis rituelı), ara.py, oku.py
"""

import sys

import kayit


def main() -> int:
    kayit.utf8_zorla()
    arg = sys.argv[1] if len(sys.argv) > 1 else None

    havuz = kayit.oturumlar("proje")
    if not havuz:
        print(f"HATA: bu projede oturum kaydi yok ({kayit.proje_adi()})",
              file=sys.stderr)
        print("Bu komut projenin kok dizininde calistirilmali.", file=sys.stderr)
        return 1

    if arg == "--liste":
        print(f"{len(havuz)} oturum kaydi - {kayit.proje_adi()}\n")
        for o in havuz:
            print(o.satir())
        return 0

    if arg:
        oturum = kayit.oturum_bul(arg, "proje") or kayit.oturum_bul(arg, "hepsi")
        if not oturum:
            print(f"HATA: '{arg}' ile baslayan oturum yok", file=sys.stderr)
            return 1
    else:
        # En son yazilan kayit = su an calisan oturum. Ayni projede iki oturum
        # acikken yaniltabilir; supheliysen --liste ile bak.
        oturum = havuz[0]

    satirlar = [m for m in kayit.mesajlar(oturum) if m.rol == kayit.KULLANICI]
    if not satirlar:
        print(f"UYARI: {oturum.kisa} icinde kullanici mesaji yok", file=sys.stderr)
        return 1

    print(f"# Oturum omurgasi - {oturum.kimlik}")
    print(f"# kayit: {oturum.boyut / 1024:.0f} KB\n")
    toplam = 0
    for i, m in enumerate(satirlar, 1):
        toplam += len(m.metin)
        print(f"--- [{i}] {m.an:%d.%m %H:%M} ---")
        print(m.metin)
        print()

    # Sessiz basari yasak: ne yaptigini sayiyla soyle.
    print(f"# {len(satirlar)} kullanici mesaji, {toplam / 1024:.1f} KB omurga")
    return 0


if __name__ == "__main__":
    sys.exit(main())
