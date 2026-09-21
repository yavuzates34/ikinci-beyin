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
Iki alici var:
  - UserPromptSubmit (bu dosya __main__ olarak) -> sikistirmadan sonraki ilk
    promptta, ayni oturum icinde teslim eder. Asil yol.
  - SessionStart (oturum_basi.py) -> oturum sikistirmadan sonra hic devam
    etmediyse, yeni oturum mesaji devralir. Yedek yol.

BORC DENEMEYLE DEGIL, SONUCUN GOZLENMESIYLE KAPANIR
Eski surum mesaji kuyruktan `pop` edip diske yaziyordu, teslim ise SONRA
oluyordu. Arada korumasiz pencere vardi: `print`/`flush` patlarsa, hook zaman
asimiyla oldurulurse ya da harness ciktiyi yok sayarsa mesaj gidiyordu. Yedek
yol da bunu kapatmiyordu, cunku ayni `al()`'i cagiriyor - kuyrugun ikinci
TUKETICISI, kurtaricisi degil (claude 96517e26 · 21.09 08:11).

Onerilen ilk duzeltme "print+flush basariliysa onayla" idi ve olculup CURUDU:
  - Iki Windows sureci bariyerle siralandiginda AYNI talimat iki ayri stdout
    akisina cikti; damga kilit degildir (Astra [I7], 21.09 08:22).
  - Cikti baytlarini tuketip modele hic eklemeyen bir alici kuruldugunda
    gonderici `done=1` gordu, model baglamina 0 mesaj girdi. Yani flush
    "teslim edildi" demek degil (Astra, ayni rapor).

Dogru olcut, is urununun KENDISI: borc, "mesaj basildi"da degil, "istenen is
yapildi"da kapanir. Her borc yaninda bir KANIT tarifi tasir; `al()` once ona
bakar. Kanit gerceklestiyse mesaj hic teslim edilmez ve borc kapanir - bu,
yeniden teslimi tanim geregi zararsiz kilar. Gerceklesmediyse yeniden teslim
DOGRU davranistir, cunku is hala yapilmamistir.

Kayip kaydedilir, silinmez. Bayat ve basarisiz borclar kuyrukta KALIR, oturum
basinda raporlanana kadar; boylece "sessizce dustu" hali mumkun olmaz.
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

# Sahiplik omru. Isi degil, yalniz AYNI ANDA iki tuketicinin ayni borcu
# teslim etmesini engeller. Suresi dolunca yeniden teslim serbest kalir;
# kanit kontrolu zaten cift uygulamayi onluyor.
SAHIPLIK_OMRU = timedelta(minutes=5)

MAX_DENEME = 3
GECMIS_SINIRI = 20  # kapanan borclarin saklanan sayisi

BEKLIYOR, TESLIM, KAPANDI, BASARISIZ, BAYAT = (
    "bekliyor", "teslim-edildi", "kapandi", "basarisiz", "bayat")
ACIK_DURUMLAR = (BEKLIYOR, TESLIM)
RAPORLANACAK = (BASARISIZ, BAYAT)


def _an(metin: str) -> datetime:
    return datetime.fromisoformat(metin).astimezone()


def _simdi() -> datetime:
    return datetime.now().astimezone()


def _yukselt(v: dict) -> dict:
    """Surum 2 girdisini surum 3'e cevirir. Eski kutu bosa dusmesin."""
    v.setdefault("event_id", uuid.uuid4().hex)
    v.setdefault("durum", BEKLIYOR)
    v.setdefault("deneme", 0)
    v.setdefault("sahip", None)
    v.setdefault("kanit", None)
    return v


def _oku() -> tuple[list[dict], list[dict]]:
    """(kuyruk, gecmis). SUZMEZ: bayat girdiyi burada dusurmek, kaybi
    gorunmez yapiyordu (K2). Bayatlik artik `al()` icinde damgalanir."""
    if not KUTU.exists():
        return [], []
    veri = json.loads(KUTU.read_text(encoding="utf-8"))
    ham = veri.get("kuyruk", [veri] if veri.get("metin") else [])
    return ([_yukselt(v) for v in ham if v.get("metin")],
            list(veri.get("gecmis", [])))


def _yaz(kuyruk: list[dict], gecmis: list[dict]) -> None:
    KUTU.parent.mkdir(parents=True, exist_ok=True)
    gecici = KUTU.with_name(KUTU.name + "." + uuid.uuid4().hex + ".tmp")
    gecici.write_text(
        json.dumps({"surum": 3, "kuyruk": kuyruk,
                    "gecmis": gecmis[-GECMIS_SINIRI:]}, ensure_ascii=True),
        encoding="utf-8", newline="\n")
    os.replace(gecici, KUTU)


# ------------------------------------------------------------------- kanit


def _kanit_gerceklesti(borc: dict) -> bool:
    """Borcun istedigi is YAPILDI mi.

    Tek tur destekli: "oturum-kaydi" - `oturumlar/` altinda o oturumdan soz
    eden, borctan SONRA yazilmis bir kayit var mi. Gece taslaklari (`oto-*.md`)
    sayilmaz; taslak kapanis degildir (AGENTS.md).

    Kaniti olmayan borc kendiliginden kapanmaz; MAX_DENEME'ye kadar yeniden
    teslim edilir, sonra `basarisiz` olarak raporlanir.
    """
    k = borc.get("kanit")
    if not k or k.get("tur") != "oturum-kaydi":
        return False
    kisa = str(k.get("oturum") or "")
    if not kisa:
        return False
    dizin = kayit.PROJE_KOKU / "oturumlar"
    if not dizin.is_dir():
        return False
    esik = _an(borc["an"]).timestamp()
    for p in dizin.glob("*.md"):
        if p.name.startswith("oto-"):
            continue
        try:
            if p.stat().st_mtime <= esik:
                continue
            if kisa in p.read_text(encoding="utf-8", errors="ignore"):
                return True
        except OSError:
            continue
    return False


def _sahip_canli(borc: dict, simdi: datetime) -> bool:
    s = borc.get("sahip")
    if not s:
        return False
    try:
        return _an(s["bitis"]) > simdi
    except (KeyError, ValueError):
        return False


# ------------------------------------------------------------------ yazma


def birak(metin: str, session_id: str | None = None,
          kanit: dict | None = None) -> str | None:
    """Borcu ekle; diger oturumun bekleyen kurtarma mesajini ezme.

    `kanit`, borcun kapandigini gosteren gozlemin tarifi. Ornegin
    {"tur": "oturum-kaydi", "oturum": "96517e26"}. Verilmezse borc yalnizca
    deneme sayisiyla sinirlanir.
    """
    event_id = uuid.uuid4().hex
    try:
        with kilit(KUTU.with_suffix(".lock")):
            kuyruk, gecmis = _oku()
            kuyruk.append({"event_id": event_id,
                           "an": datetime.now().isoformat(timespec="seconds"),
                           "metin": metin, "session_id": session_id,
                           "kanit": kanit, "sahip": None,
                           "deneme": 0, "durum": BEKLIYOR})
            _yaz(kuyruk, gecmis)
        return event_id
    except (OSError, ValueError, KeyError):
        print("UYARI: devir mesaji kuyruga yazilamadi; omurga dosyasini kontrol et.",
              file=sys.stderr)
        return None


# ------------------------------------------------------------------ okuma


def al(session_id: str | None = None, devral: bool = False) -> str | None:
    """Bir borcu teslim al. Diger oturuma aitse acikca etiketle.

    Sira onemli: once KANIT (is yapildi mi), sonra bayatlik, sonra deneme
    tavani, en sonunda sahiplik. Kanit onde oldugu icin yapilmis isin talimati
    bir daha teslim edilmez.
    """
    if not KUTU.exists():
        return None
    try:
        with kilit(KUTU.with_suffix(".lock")):
            kuyruk, gecmis = _oku()
            simdi = _simdi()
            degisti = False
            secilen = None
            for borc in kuyruk:
                if borc["durum"] not in ACIK_DURUMLAR:
                    continue
                if _kanit_gerceklesti(borc):
                    borc["durum"] = KAPANDI
                    borc["sahip"] = None
                    degisti = True
                    continue
                if simdi - _an(borc["an"]) > BAYAT_ESIK:
                    borc["durum"] = BAYAT
                    degisti = True
                    continue
                if borc["deneme"] >= MAX_DENEME:
                    borc["durum"] = BASARISIZ
                    degisti = True
                    continue
                if secilen is not None:
                    continue
                bizim = session_id and borc.get("session_id") == session_id
                if not (bizim or devral):
                    continue
                if _sahip_canli(borc, simdi):
                    continue  # baska tuketici teslim ediyor; cift basmayiz
                borc["sahip"] = {"token": uuid.uuid4().hex,
                                 "bitis": (simdi + SAHIPLIK_OMRU).isoformat(
                                     timespec="seconds")}
                borc["deneme"] += 1
                borc["durum"] = TESLIM
                secilen = borc
                degisti = True
            if degisti:
                kapanan = [b for b in kuyruk if b["durum"] == KAPANDI]
                kuyruk = [b for b in kuyruk if b["durum"] != KAPANDI]
                _yaz(kuyruk, gecmis + kapanan)
        if secilen is None:
            return None
        if secilen.get("session_id") != session_id:
            return ("BASKA OTURUMDAN KURTARMA BILGISI: "
                    + str(secilen.get("session_id") or "eski, kimliksiz kutu")
                    + ". Asagidaki talimat kaynak oturuma aittir; mevcut "
                      "oturumun kapanisi degildir.\n" + secilen["metin"])
        return secilen["metin"]
    except (OSError, ValueError, KeyError):
        return "DEVIR KUTUSU OKUNAMADI; kurtarma dosyalari denetlenmeli."


def raporlanacaklar() -> list[str]:
    """Basarisiz ve bayat borclar. Rapor edildikten sonra gecmise tasinir.

    Sinirli bir listeye erken tasinsalardi, raporlanmadan kapasite disina
    dusebilirlerdi - yeni bir sessiz kayip. Bu yuzden rapor ANI tasima anidir.
    """
    if not KUTU.exists():
        return []
    try:
        with kilit(KUTU.with_suffix(".lock")):
            kuyruk, gecmis = _oku()
            dusen = [b for b in kuyruk if b["durum"] in RAPORLANACAK]
            if not dusen:
                return []
            kuyruk = [b for b in kuyruk if b["durum"] not in RAPORLANACAK]
            _yaz(kuyruk, gecmis + dusen)
        return [f"{b['durum'].upper()} devir borcu ({b['an']}, "
                f"{b['deneme']} deneme): {b['metin'][:120]}" for b in dusen]
    except (OSError, ValueError, KeyError):
        return ["DEVIR KUTUSU OKUNAMADI; kurtarma dosyalari denetlenmeli."]


def main() -> int:
    try:
        girdi = json.loads(sys.stdin.read() or "{}")
    except (ValueError, OSError):
        girdi = {}
    parcalar = []
    metin = al(girdi.get("session_id"))
    if metin:
        parcalar.append(metin)
    # Basarisiz/bayat borc sessizce dusmesin: tur basinda da soylenir.
    dusen = raporlanacaklar()
    if dusen:
        parcalar.append("TESLIM EDILEMEYEN DEVIR BORCU:\n"
                        + "\n".join("  - " + d for d in dusen))
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
