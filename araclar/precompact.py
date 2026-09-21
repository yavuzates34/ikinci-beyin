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
2. DOLAYLI ENJEKSIYON: "simdi yaz" uyarisi devir kutusuna birakilir; konusabilen
   bir hook (UserPromptSubmit ya da SessionStart) onu modele tasir.

NEDEN DOLAYLI
16 Eylul'de gercek bir sikistirmada olculdu: PreCompact'in kendisi modele
KONUSAMIYOR. `hookSpecificOutput.additionalContext` bu olayda gecerli degil,
Claude Code sema hatasi verip ciktiyi dusuruyor (bkz. yasanan-hatalar madde 15).
Bu yuzden mesaj araclar/devir.py uzerinden aktariliyor.

NEDEN BLOKE ETMIYOR
Hook cikis kodu 2 ile sikistirmayi engelleyebilir. Denenmedi ve bilerek
secilmedi: sikistirma engellenirse ve pencere zaten doluysa oturum sert bir
sinira carpabilir. Agin kendisi hasara yol acmamali.

Girdi: stdin'den JSON (session_id, transcript_path, trigger, cwd).
`--bicim codex` Codex transcript semasini secer; varsayilan `claude`dur.
Cikti: stdout'a JSON - sadece `systemMessage` (kullaniciya gorunen tek satir).
Cikis kodu her zaman 0 - bu bir ag, bir bariyer degil.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kayit  # noqa: E402
import devir  # noqa: E402

ANLIK = kayit.PROJE_KOKU / "derleme" / "omurga-anlik"


def cikti(satir: str) -> None:
    """Kullaniciya gorunen tek satir. ensure_ascii=True: konsol kodlamasi ne
    olursa olsun saglam kalsin (bkz. notlar/yasanan-hatalar.md madde 11)."""
    print(json.dumps({"systemMessage": satir}, ensure_ascii=True))


def main() -> int:
    ap = argparse.ArgumentParser(description="PreCompact guvenlik agi")
    ap.add_argument("--bicim", choices=("claude", "codex"), default="claude")
    a = ap.parse_args()

    try:
        girdi = json.loads(sys.stdin.read() or "{}")
    except (ValueError, OSError):
        girdi = {}

    tetik = girdi.get("trigger", "?")
    kayit_yolu = girdi.get("transcript_path")

    # Transcript yoksa yalniz verilen kimligi kullan. Son yazilan kayit
    # paralel bir oturuma ait olabilir; tahminle kurtarma yapilmaz.
    oturum = None
    if kayit_yolu:
        p = Path(kayit_yolu)
        if p.exists():
            st = p.stat()
            # Codex ve Claude transcript semalari farkli. Varsayilan Claude
            # davranisini aynen koru; Codex adaptorunun acik secimini kullan.
            kaynak = "codex" if a.bicim == "codex" else "claude"
            kimlik = (
                (girdi.get("session_id") or p.stem)
                if kaynak == "codex" else p.stem
            )
            oturum = kayit.Oturum(
                kaynak, kimlik, p, p.parent.name,
                datetime.fromtimestamp(st.st_mtime), st.st_size,
            )
    if oturum is None:
        kimlik = girdi.get("session_id")
        oturum = kayit.oturum_bul(kimlik, "hepsi") if kimlik else None
        if oturum is None:
            devir.birak("PreCompact: oturum kaydi bulunamadi, omurga alinamadi. "
                        "Baglam sikistirildi - onemli bir sey varsa simdi yaz.", kimlik)
            cikti("PreCompact: oturum kaydi bulunamadi, omurga alinamadi.")
            return 0

    mesajlar = [m for m in kayit.mesajlar(oturum) if m.rol == kayit.KULLANICI]
    if not mesajlar:
        cikti("PreCompact: bu oturumda kullanici mesaji bulunamadi.")
        return 0

    ANLIK.mkdir(parents=True, exist_ok=True)
    an = datetime.now()
    dosya = ANLIK / f"{an:%Y-%m-%d-%H%M%S-%f}-{oturum.kimlik}.md"

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
    devir.birak(
        f"BAGLAM SIKISTIRILDI ({an:%d.%m %H:%M}, PreCompact, tetik: {tetik}).\n\n"
        f"Ilgili oturum: {oturum.kimlik}. Omurgasi sikistirmadan hemen once "
        f"diske alindi: {goreli} ({len(mesajlar)} kullanici mesaji, "
        f"{harf / 1024:.1f} KB). O dosya sikistirmadan etkilenmedi.\n\n"
        f"SIMDI YAP - AGENTS.md'deki kapanis rituelinin ayni sirasi:\n"
        f"1) Bu oturumun kaydini oturumlar/ altina yaz (ya da varsa guncelle).\n"
        f"2) Kalici olani notlar/ icindeki ilgili konu notuna terfi ettir.\n"
        f"3) BEYIN.md haritasini ve kaynak isaretcilerini guncelle.\n"
        f"`kapanan-oturum:` satirini YAZMA - oturum bitmiyor, sadece sikisti.\n\n"
        f"Ayrinti hatirlamiyorsan once yukaridaki omurga dosyasini oku - "
        f"konusmanin iskeleti orada, zaman damgalariyla.\n\n"
        f"Bu bir guvenlik agidir: kullanici 'kapatalim' demeden sikistirma "
        f"geldi. Oturum bitmiyor; yazdiktan sonra kaldigin yerden devam et.",
        oturum.kimlik,
        # Borcun kapandigini gosteren gozlem: bu oturumdan soz eden bir arsiv
        # kaydi, borctan SONRA yazilmis olsun. Mesajin basilmasi degil, ISTENEN
        # ISIN yapilmasi olcut (bkz. araclar/devir.py).
        kanit={"tur": "oturum-kaydi", "oturum": oturum.kisa},
    )
    cikti(f"Omurga diske alindi: {goreli} ({len(mesajlar)} mesaj, "
          f"{harf / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
