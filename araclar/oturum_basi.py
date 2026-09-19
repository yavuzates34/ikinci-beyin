#!/usr/bin/env python3
"""Oturum basi baglami - her oturumun basinda haritayi ve durumu verir.

SAGLAYICIDAN BAGIMSIZ CEKIRDEK. Claude Code bunu SessionStart hook'undan
cagirir; hook'u olan baska bir saglayici kendi hook'undan, hook'u olmayan
bir model ise talimatla (`python araclar/oturum_basi.py --bicim duz`)
cagirir. Metni ureten tek yer burasi; saglayicilar sadece zarfi degistirir.

Bes sey soyler:
1. Sabit yonergeler (araclar/oturum-basi.md; duragan metin kabuk komutunun
   icine gomulmez - bkz. notlar/yasanan-hatalar.md madde 10).
2. DEVIR KUTUSU. PreCompact modele konusamiyor (bkz. araclar/devir.py);
   biraktigi mesaji burasi teslim eder.
3. Bu oturumun KENDI KIMLIGI (girdide varsa). Ayni projede iki oturum
   acikken arac varsayilanlari yanlis oturumu secebiliyor.
4. KAPANMAMIS OTURUMLAR. Arsivde `kapanan-oturum:` satiri olmayan her oturum.
   Onlarda konusulan kalici notlara islenmemistir; ama ham kayit canlidir.
   Eskiden sadece son 6 saate bakiliyordu - kapanmadan 6 saat sessiz kalan
   oturum gorunmez oluyordu (claude 5c600e7e · 19.09 16:40).
5. GECE DERLEYICISI UYARILARI. Rapor diske yaziliyordu ama kimse okumuyordu:
   19.09 00:30'da push dustu ve kullanici sormasa fark edilmeyecekti
   (claude 5c600e7e · 19.09 08:27). Artik uyari varsa buraya tasinir.

Girdi: stdin'den JSON (varsa). Cikti: --bicim claude (varsayilan) -> Claude
hook JSON'u; --bicim duz -> duz metin. Cikis kodu her zaman 0.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kayit  # noqa: E402
import devir  # noqa: E402

YONERGE = kayit.PROJE_KOKU / "araclar" / "oturum-basi.md"
DURUM = kayit.PROJE_KOKU / "derleme" / "son-calisma.json"
CANLI_PENCERE = timedelta(hours=6)  # bu kadar yeni yazilan "muhtemelen acik"
DERLEYICI_SESSIZLIK = timedelta(hours=36)  # daha uzun sessizlik = calismamis


def cikti(metin: str, bicim: str) -> None:
    if bicim == "duz":
        kayit.utf8_zorla()
        print(metin)
        return
    print(json.dumps(
        {"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": metin}},
        ensure_ascii=True,
    ))


def derleyici_uyarilari(simdi: datetime) -> list[str]:
    """son-calisma.json'dan sadece SORUNLARI cikarir. Her sey yolundaysa bos
    liste - her oturumun basina "her sey yolunda" yazmak gurultudur."""
    if not DURUM.exists():
        return ["son-calisma.json yok - gece derleyicisi hic calismamis olabilir"]
    try:
        d = json.loads(DURUM.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return ["son-calisma.json okunamadi ya da bozuk"]

    uyari = []
    try:
        son = datetime.strptime(d.get("baslangic", ""), "%Y-%m-%d %H:%M")
        if simdi - son > DERLEYICI_SESSIZLIK:
            uyari.append(f"son calisma {son:%d.%m %H:%M} - 36 saatten eski; "
                         "gorev calismiyor olabilir (sessizlik 'her sey iyi' demek degil)")
    except ValueError:
        pass
    if not d.get("tamamlandi"):
        uyari.append(f"son calisma ({d.get('baslangic', '?')}) TAMAMLANMADAN kesildi")
    if d.get("push") == "BASARISIZ":
        uyari.append("PUSH BASARISIZ - GitHub yedegi guncel degil (internet?). "
                     "Kullaniciya soyle; elle: git push")
    if d.get("isaretci_kusurlu"):
        uyari.append(f"{len(d['isaretci_kusurlu'])} kaynak isaretcisi KUSURLU "
                     "(oturum ya da damga yok)")
    if d.get("isaretci_denetlenemeyen"):
        uyari.append(f"{len(d['isaretci_denetlenemeyen'])} isaretci denetlenemedi "
                     "(bicim okunamadi)")
    return uyari


def main() -> int:
    ap = argparse.ArgumentParser(description="Oturum basi baglami")
    ap.add_argument("--bicim", choices=("claude", "duz"), default="claude")
    a = ap.parse_args()

    girdi = {}
    if a.bicim == "claude":
        try:
            girdi = json.loads(sys.stdin.read() or "{}")
        except (ValueError, OSError):
            girdi = {}

    beyin = kayit.PROJE_KOKU / "BEYIN.md"
    if not beyin.exists() or not YONERGE.exists():
        cikti("UYARI: BEYIN.md ya da araclar/oturum-basi.md bulunamadi. "
              "Bu projenin giris ve haritasi BEYIN.md'dir; yoksa olustur.", a.bicim)
        return 0

    st = beyin.stat()
    metin = YONERGE.read_text(encoding="utf-8")
    for anahtar, deger in {
        "{KB}": str(round(st.st_size / 1024)),
        "{T}": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
        "{N}": str(len(list((kayit.PROJE_KOKU / "notlar").glob("*.md")))),
        "{O}": str(len(list((kayit.PROJE_KOKU / "oturumlar").glob("*.md")))),
    }.items():
        metin = metin.replace(anahtar, deger)

    ek = []
    simdi = datetime.now()

    bekleyen = devir.al()
    if bekleyen:
        ek.append("DEVIR KUTUSUNDAN:" + chr(10) + bekleyen)

    uyarilar = derleyici_uyarilari(simdi)
    if uyarilar:
        ek.append("GECE DERLEYICISI UYARISI (derleme/son-calisma.json):\n"
                  + "\n".join(f"  - {u}" for u in uyarilar)
                  + "\nBunlari kullaniciya ilk cevapta soyle.")

    kimlik = girdi.get("session_id")
    if kimlik:
        ek.append(
            f"BU OTURUMUN KIMLIGI: {kimlik}\n"
            f"Araclara kesin kimlik ver: python araclar/omurga.py {kimlik[:8]}\n"
            f"Kapanista arsiv dosyasina su satiri yaz: kapanan-oturum: {kimlik[:8]}"
        )

    try:
        kapali = kayit.kapanmis_kimlikler()
        acik = [o for o in kayit.oturumlar("proje")
                if o.kisa not in kapali and not (kimlik and o.kimlik == kimlik)]
    except OSError:
        acik = []

    if acik:
        satirlar = "\n".join(
            f"  - {o.kisa} ({o.kaynak}, son yazma {o.an:%d.%m %H:%M}, "
            f"{o.boyut / 1024:.0f} KB"
            + (", muhtemelen HALA ACIK" if simdi - o.an < CANLI_PENCERE else "")
            + (f", GECE TASLAGI VAR: oturumlar/oto-{o.kisa}.md"
               if (kayit.PROJE_KOKU / "oturumlar" / f"oto-{o.kisa}.md").exists() else "")
            + ")" for o in acik[:8]
        )
        ek.append(
            "KAPANMAMIS OTURUMLAR: bu projede kapanis rituelinden gecmemis "
            "oturum var:\n" + satirlar + "\n"
            "Orada konusulanlar kalici notlara (notlar/) islenmemistir ve "
            "haritada gorunmez. Ama ham kayit okunabilir:\n"
            "  python araclar/omurga.py <id>          -> o oturumun iskeleti\n"
            "  python araclar/oku.py <id> --saat SS:DD -> tam dokum\n"
            "Kullanici 'az once sunu konusmustuk' derse ve notlarda yoksa, "
            "tahmin etme - bu kayitlari oku.\n"
            "GECE TASLAGI olanlari kullaniciya soyle: taslak gozden gecirilir, "
            "terfi onerileri notlara islenir, dosya gercek arsiv kaydina cevrilir "
            "ve `kapanan-oturum:` yazilir (AGENTS.md)."
        )

    cikti(metin.rstrip() + ("\n\n" + "\n\n".join(ek) if ek else ""), a.bicim)
    return 0


if __name__ == "__main__":
    sys.exit(main())
