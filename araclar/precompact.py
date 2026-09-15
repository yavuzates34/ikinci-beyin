#!/usr/bin/env python3
"""PreCompact hook'u - baglam sikistirilmadan once devreye giren guvenlik agi.

NEDEN VAR
Asil kapanis yolu elle devirdir: kullanici konu bittiginde "kapatalim" der,
model tam baglamla notu yazar. Bu iyi bir yoldur cunku devir ANLAMLI BIR
SINIRDA olur. Ama kullanici demezse - pencere dolarsa, makine kapanirsa - o
oturumda ogrenilen her sey buharlasir. Buna "Durum B" deniyor (bkz.
notlar/kapanis-ritueli.md). Bu script Durum B'nin agidir, ana yolu degil.

IKI AYAK
1. DETERMINISTIK: oturumun omurgasi diske dokulur. Model hicbir sey yapmasa,
   enjeksiyon hic calismasa bile ham malzeme kurtulur. Omurga dosyasi
   sikistirmadan etkilenmez - diskte durur, sonra okunur.
2. BEST-EFFORT: baglama "simdi yaz" uyarisi enjekte edilir. Calisirsa model
   sikistirmadan once ya da hemen sonra notu yazar.

NEDEN BLOKE ETMIYOR
Hook cikis kodu 2 ile sikistirmayi engelleyebilir. Denenmedi ve bilerek
secilmedi: sikistirma engellenirse ve pencere zaten doluysa oturum sert bir
sinira carpabilir. Agin kendisi hasara yol acmamali. Bunun yerine omurga
dosyasi kurtarma malzemesi olarak birakiliyor - sikistirma sonrasinda bile
oturum kaydi ondan yazilabilir.

Girdi: stdin'den JSON (session_id, transcript_path, trigger, cwd).
Cikti: stdout'a JSON (hookSpecificOutput.additionalContext).
Cikis kodu her zaman 0 - bu bir ag, bir bariyer degil.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kayit  # noqa: E402

ANLIK = kayit.PROJE_KOKU / "derleme" / "omurga-anlik"


def cikti(metin: str) -> None:
    """Hook ciktisi. ensure_ascii=True: konsol kodlamasi ne olursa olsun
    saglam kalsin (bkz. notlar/yasanan-hatalar.md madde 11)."""
    print(json.dumps(
        {"hookSpecificOutput": {
            "hookEventName": "PreCompact", "additionalContext": metin}},
        ensure_ascii=True,
    ))


def main() -> int:
    try:
        girdi = json.loads(sys.stdin.read() or "{}")
    except (ValueError, OSError):
        girdi = {}

    tetik = girdi.get("trigger", "?")
    kayit_yolu = girdi.get("transcript_path")

    # Oturumu once transcript_path'ten bul (kesin), olmazsa en son yazilan
    # kayda dus (bu projede calisan oturum odur).
    oturum = None
    if kayit_yolu:
        p = Path(kayit_yolu)
        if p.exists():
            st = p.stat()
            oturum = kayit.Oturum(
                "claude", p.stem, p, p.parent.name,
                datetime.fromtimestamp(st.st_mtime), st.st_size,
            )
    if oturum is None:
        havuz = kayit.oturumlar("proje")
        if not havuz:
            cikti("PreCompact: oturum kaydi bulunamadi, omurga alinamadi. "
                  "Baglam sikistirilmak uzere - onemli bir sey varsa simdi yaz.")
            return 0
        oturum = havuz[0]

    mesajlar = [m for m in kayit.mesajlar(oturum) if m.rol == kayit.KULLANICI]
    if not mesajlar:
        cikti("PreCompact: bu oturumda kullanici mesaji bulunamadi.")
        return 0

    ANLIK.mkdir(parents=True, exist_ok=True)
    an = datetime.now()
    dosya = ANLIK / f"{an:%Y-%m-%d-%H%M}-{oturum.kimlik[:8]}.md"

    govde = [
        f"# Omurga anlik goruntusu - {an:%d.%m.%Y %H:%M}",
        "",
        f"Oturum: `{oturum.kimlik}` | Tetik: `{tetik}` | "
        f"Kayit: {oturum.boyut / 1024:.0f} KB",
        "",
        "Baglam sikistirilmadan hemen once alindi. Bu dosya kurtarma "
        "malzemesidir: sikistirma sonrasinda oturum kaydi bundan yazilabilir.",
        "",
        "---",
        "",
    ]
    harf = 0
    for i, m in enumerate(mesajlar, 1):
        harf += len(m.metin)
        govde += [f"## [{i}] {m.an:%d.%m %H:%M}", "", m.metin, ""]
    dosya.write_text("\n".join(govde), encoding="utf-8")

    goreli = dosya.relative_to(kayit.PROJE_KOKU).as_posix()
    cikti(
        f"BAGLAM SIKISTIRILMAK UZERE (PreCompact, tetik: {tetik}).\n\n"
        f"Bu oturumun omurgasi diske alindi: {goreli} "
        f"({len(mesajlar)} kullanici mesaji, {harf / 1024:.1f} KB). "
        f"Bu dosya sikistirmadan etkilenmez.\n\n"
        f"SIMDI YAP - CLAUDE.md'deki kapanis rituelinin ayni sirasi:\n"
        f"1) Bu oturumun kaydini oturumlar/ altina yaz (ya da varsa guncelle).\n"
        f"2) Kalici olani notlar/ icindeki ilgili konu notuna terfi ettir.\n"
        f"3) BEYIN.md haritasini ve kaynak isaretcilerini guncelle.\n\n"
        f"Ayrinti hatirlamiyorsan yukaridaki omurga dosyasini oku - "
        f"konusmanin iskeleti orada, zaman damgalariyla.\n\n"
        f"Bu bir guvenlik agidir: kullanici 'kapatalim' demeden sikistirma "
        f"geldi. Oturum bitmiyor, sadece baglam sikisiyor; yazdiktan sonra "
        f"kaldigin yerden devam et."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
