#!/usr/bin/env python3
"""SessionStart hook'u - her oturumun basinda haritayi ve durumu enjekte eder.

Uc sey soyler:
1. Sabit yonergeler (.claude/oturum-basi.md dosyasindan okunur; durağan metin
   kabuk komutunun icine gomulmez - bkz. notlar/yasanan-hatalar.md madde 10).
2. Bu oturumun KENDI KIMLIGI. Ayni projede iki oturum acikken arac
   varsayilanlari ("en son yazilan kayit") yanlis oturumu secebiliyor; kimlik
   bilinince `omurga.py <id>` kesin olur.
3. PARALEL OTURUMLAR. Bu projede son saatlerde yazilmis baska oturum kaydi
   varsa listelenir. Kritik: yan yana acilan bir oturum, otekinde konusulani
   KALICI NOTLARDAN goremez - cunku o oturum henuz kapanmamis, damitilmamistir.
   Ama ham kayit CANLIDIR: jsonl surekli yaziliyor, yani okunabiliyor.

Girdi: stdin'den JSON. Cikti: stdout'a hook JSON'u. Cikis kodu her zaman 0.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kayit  # noqa: E402

YONERGE = kayit.PROJE_KOKU / ".claude" / "oturum-basi.md"
PARALEL_PENCERE = timedelta(hours=6)  # bu kadar once yazilmis kayit "acik" sayilir


def cikti(metin: str) -> None:
    print(json.dumps(
        {"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": metin}},
        ensure_ascii=True,
    ))


def main() -> int:
    try:
        girdi = json.loads(sys.stdin.read() or "{}")
    except (ValueError, OSError):
        girdi = {}

    beyin = kayit.PROJE_KOKU / "BEYIN.md"
    if not beyin.exists() or not YONERGE.exists():
        cikti("UYARI: BEYIN.md ya da .claude/oturum-basi.md bulunamadi. "
              "Bu projenin giris ve haritasi BEYIN.md'dir; yoksa olustur.")
        return 0

    st = beyin.stat()
    notlar = len(list((kayit.PROJE_KOKU / "notlar").glob("*.md")))
    oturumlar = len(list((kayit.PROJE_KOKU / "oturumlar").glob("*.md")))

    metin = YONERGE.read_text(encoding="utf-8")
    for anahtar, deger in {
        "{KB}": str(round(st.st_size / 1024)),
        "{T}": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
        "{N}": str(notlar),
        "{O}": str(oturumlar),
    }.items():
        metin = metin.replace(anahtar, deger)

    ek = []
    kimlik = girdi.get("session_id")
    if kimlik:
        ek.append(
            f"BU OTURUMUN KIMLIGI: {kimlik}\n"
            f"Araclara kesin kimlik ver: python araclar/omurga.py {kimlik[:8]}\n"
            f"(Argumansiz cagri 'en son yazilan kaydi' secer; ayni projede iki\n"
            f"oturum acikken yanlis oturumu secebilir.)"
        )

    # Paralel oturumlar: son saatlerde yazilmis, bu oturum olmayan kayitlar
    try:
        simdi = datetime.now()
        paralel = [
            o for o in kayit.oturumlar("proje")
            if simdi - o.an < PARALEL_PENCERE
            and not (kimlik and o.kimlik == kimlik)
        ]
    except OSError:
        paralel = []

    if paralel:
        satirlar = "\n".join(
            f"  - {o.kimlik[:8]} (son yazma {o.an:%d.%m %H:%M}, "
            f"{o.boyut / 1024:.0f} KB)" for o in paralel[:5]
        )
        ek.append(
            "PARALEL OTURUM UYARISI: bu projede yakin zamanda yazilmis baska "
            "oturum kaydi var:\n" + satirlar + "\n"
            "Bu oturumlar HENUZ KAPANMAMIS olabilir - yani orada konusulanlar "
            "kalici notlara (notlar/) islenmemistir ve haritada gorunmez.\n"
            "Ama ham kayit CANLIDIR, okunabilir:\n"
            "  python araclar/omurga.py <id>          -> o oturumun iskeleti\n"
            "  python araclar/oku.py <id> --saat SS:DD -> tam dokum\n"
            "Kullanici 'az once sunu konusmustuk' derse ve notlarda yoksa, "
            "tahmin etme - paralel oturumun kaydini oku."
        )

    cikti(metin.rstrip() + ("\n\n" + "\n\n".join(ek) if ek else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
