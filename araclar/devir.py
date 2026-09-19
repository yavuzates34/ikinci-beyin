#!/usr/bin/env python3
"""Devir kutusu - bir hook'un soyleyemedigini baska bir hook'a soyletir.

NEDEN VAR
`PreCompact` hook'u modele konusamiyor. 16 Eylul'de gercek bir sikistirmada
olculdu: Claude Code, PreCompact'in `hookSpecificOutput.additionalContext`
ciktisini SEMA HATASI diye reddediyor (bkz. notlar/yasanan-hatalar.md madde 15).
`additionalContext` sadece su olaylarda gecerli: UserPromptSubmit, SessionStart,
PreToolUse, PostToolUse, Stop ve birkac kardesi. PreCompact listede yok.

COZUM
PreCompact mesaji diske birakir; konusabilen bir hook onu alip enjekte eder.
Iki alici var, hangisi once tetiklenirse o teslim eder ve kutuyu bosaltir:
  - UserPromptSubmit (bu dosya __main__ olarak) -> sikistirmadan sonraki ilk
    promptta, ayni oturum icinde teslim eder. Asil yol.
  - SessionStart (oturum_basi.py) -> oturum sikistirmadan sonra hic devam
    etmediyse, yeni oturum mesaji devralir. Yedek yol.

Kutu tek mesaj tutar; yenisi eskisini ezer. Bayat mesaj teslim edilmez
(BAYAT_ESIK), cunku gunler sonra gelen "simdi yaz" emri zarar verir.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kayit  # noqa: E402

KUTU = kayit.PROJE_KOKU / "derleme" / "omurga-anlik" / "devir-bekliyor.json"
BAYAT_ESIK = timedelta(hours=12)


def birak(metin: str) -> None:
    """Mesaji kutuya koy. Hata yutulur: kutu calismasa da asil is (omurga
    dosyasi) yazilmis olur, ag yine is gorur."""
    try:
        KUTU.parent.mkdir(parents=True, exist_ok=True)
        KUTU.write_text(json.dumps(
            {"an": datetime.now().isoformat(timespec="seconds"), "metin": metin},
            ensure_ascii=True,
        ), encoding="utf-8")
    except OSError:
        pass


def al() -> str | None:
    """Kutuyu bosalt ve mesaji dondur. Bayatsa dusur, bos dondur."""
    if not KUTU.exists():
        return None
    try:
        veri = json.loads(KUTU.read_text(encoding="utf-8"))
        KUTU.unlink()
    except (OSError, ValueError):
        try:
            KUTU.unlink()
        except OSError:
            pass
        return None
    try:
        an = datetime.fromisoformat(veri.get("an", ""))
    except ValueError:
        return None
    if datetime.now() - an > BAYAT_ESIK:
        return None
    return veri.get("metin") or None


def main() -> int:
    try:
        girdi = json.loads(sys.stdin.read() or "{}")
    except (ValueError, OSError):
        girdi = {}
    parcalar = []
    metin = al()
    if metin:
        parcalar.append(metin)
    # Erken devir: tur sinirinda baglam dolulugu (bkz. araclar/baglam.py).
    # Hata yutulur; devir kutusu teslimi hicbir kosulda bozulmamali.
    try:
        import baglam
        uyari = baglam.kontrol(girdi.get("transcript_path"), girdi.get("session_id"))
        if uyari:
            parcalar.append(uyari)
    except Exception:  # noqa: BLE001
        pass
    if parcalar:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "\n\n".join(parcalar)}},
            ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
