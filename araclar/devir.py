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

Kutu oturum kimlikli bir kuyruktur. Tur hook'u yalniz kendi mesajini alir;
yeni oturum, baska oturumun mesajini acik devir etiketiyle alabilir.
Bayat mesaj teslim edilmez (BAYAT_ESIK).
"""

import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kayit  # noqa: E402
from dosya_kilidi import kilit

KUTU = kayit.PROJE_KOKU / "derleme" / "omurga-anlik" / "devir-bekliyor.json"
BAYAT_ESIK = timedelta(hours=12)


def _oku() -> list[dict]:
    if not KUTU.exists():
        return []
    veri = json.loads(KUTU.read_text(encoding='utf-8'))
    liste = veri.get('kuyruk', [veri] if veri.get('metin') else [])
    simdi = datetime.now().astimezone()
    return [v for v in liste if v.get('metin') and
            simdi - datetime.fromisoformat(v['an']).astimezone() <= BAYAT_ESIK]


def _yaz(liste: list[dict]) -> None:
    KUTU.parent.mkdir(parents=True, exist_ok=True)
    gecici = KUTU.with_name(KUTU.name + '.' + uuid.uuid4().hex + '.tmp')
    gecici.write_text(json.dumps({'surum': 2, 'kuyruk': liste}, ensure_ascii=True), encoding='utf-8', newline='\n')
    os.replace(gecici, KUTU)


def birak(metin: str, session_id: str | None = None) -> None:
    """Mesaji ekle; diger oturumun bekleyen kurtarma mesajini ezme."""
    try:
        with kilit(KUTU.with_suffix('.lock')):
            liste = _oku()
            liste.append({'an': datetime.now().isoformat(timespec='seconds'),
                          'metin': metin, 'session_id': session_id})
            _yaz(liste)
    except (OSError, ValueError, KeyError):
        print('UYARI: devir mesaji kuyruğa yazilamadi; omurga dosyasini kontrol et.', file=sys.stderr)


def al(session_id: str | None = None, devral: bool = False) -> str | None:
    """Bir mesaji atomik olarak teslim al. Diger oturuma aitse acikca etiketle."""
    if not KUTU.exists():
        return None
    try:
        with kilit(KUTU.with_suffix('.lock')):
            liste = _oku()
            indeks = next((i for i,v in enumerate(liste)
                           if session_id and v.get('session_id') == session_id), None)
            if indeks is None and devral and liste:
                indeks = 0
            if indeks is None:
                return None
            veri = liste.pop(indeks)
            _yaz(liste)
        if veri.get('session_id') != session_id:
            return ('BASKA OTURUMDAN KURTARMA BILGISI: '
                    + str(veri.get('session_id') or 'eski, kimliksiz kutu')
                    + '. Asagidaki talimat kaynak oturuma aittir; mevcut oturumun kapanisi degildir.\n'
                    + veri['metin'])
        return veri['metin']
    except (OSError, ValueError, KeyError):
        return 'DEVIR KUTUSU OKUNAMADI; kurtarma dosyalari denetlenmeli.'


def main() -> int:
    try:
        girdi = json.loads(sys.stdin.read() or "{}")
    except (ValueError, OSError):
        girdi = {}
    parcalar = []
    metin = al(girdi.get('session_id'))
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
