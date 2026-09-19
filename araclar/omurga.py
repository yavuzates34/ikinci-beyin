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

TAM OMURGA (--tam, 19.09): kullanici mesajlari + modelin METIN cevaplari.
Arac cagrilari, arac ciktilari ve dusunme bloklari yine disarida. Olcumler,
elenen fikirler ve gerekceler model cevaplarinda durdugu icin, temiz baglamla
dogan bir ajanin (gece derleyicisinin cagirdigi) not yazabilmesi icin gerekli.
Yalnizca kullanici mesajlarindan yazilan not eksik malzemeyle yazilmis olur.

Kullanim:
    python araclar/omurga.py <oturum-id>          # kullanici mesajlari
    python araclar/omurga.py <oturum-id> --tam    # + model cevaplari
    python araclar/omurga.py --liste              # bu projedeki tum oturumlar
    python araclar/omurga.py                      # en son yazilan kayit (riskli)

Ilgili: BEYIN.md, AGENTS.md (kapanis rituelı), ara.py, oku.py, gece_kayit.py
"""

import sys

import kayit


def omurga_metni(oturum: kayit.Oturum, tam: bool = False) -> tuple[str, int, int]:
    """Omurgayi metin olarak dondurur: (metin, kullanici mesaji, model mesaji).
    gece_kayit.py de bunu kullanir; bicim tek yerde durur."""
    mesajlar = [m for m in kayit.mesajlar(oturum)
                if tam or m.rol == kayit.KULLANICI]
    ku = sum(1 for m in mesajlar if m.rol == kayit.KULLANICI)
    mo = len(mesajlar) - ku
    satir = [f"# Oturum omurgasi{' (tam)' if tam else ''} - {oturum.kimlik}",
             f"# kayit: {oturum.boyut / 1024:.0f} KB | kaynak: {oturum.kaynak}", ""]
    i = 0
    for m in mesajlar:
        if m.rol == kayit.KULLANICI:
            i += 1
            satir.append(f"--- [{i}] {m.an:%d.%m %H:%M} ---")
        else:
            satir.append(f"--- model {m.an:%d.%m %H:%M} ---")
        satir += [m.metin, ""]
    return "\n".join(satir), ku, mo


def main() -> int:
    kayit.utf8_zorla()
    tam = "--tam" in sys.argv
    argler = [a for a in sys.argv[1:] if a != "--tam"]
    arg = argler[0] if argler else None

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

    metin, ku, mo = omurga_metni(oturum, tam)
    if not ku:
        print(f"UYARI: {oturum.kisa} icinde kullanici mesaji yok", file=sys.stderr)
        return 1
    print(metin)
    # Sessiz basari yasak: ne yaptigini sayiyla soyle.
    ek = f", {mo} model mesaji" if tam else ""
    print(f"# {ku} kullanici mesaji{ek}, {len(metin.encode('utf-8')) / 1024:.1f} KB omurga")
    return 0


if __name__ == "__main__":
    sys.exit(main())
