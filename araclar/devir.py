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
Iki alici var: UserPromptSubmit (bu dosya __main__ olarak, asil yol) ve
SessionStart (oturum_basi.py, oturum hic devam etmediyse yedek yol).

BORC DENEMEYLE DEGIL, SONUCUN GOZLENMESIYLE KAPANIR
Ilk surum mesaji `pop` edip diske yaziyordu, teslim ise SONRA oluyordu; arada
kayip penceresi vardi. Ikinci surum "print+flush basariliysa onayla" dedi ve
olculup curudu: cikti baytlarini tuketip modele hic eklemeyen bir alici
kuruldugunda gonderici basariyi gordu, model baglamina 0 mesaj girdi
(Astra, 21.09 08:22).

Ucuncu surum kaniti BULUSSAL yapti - "oturumlar/ altinda kimlikten soz eden,
borctan yeni bir dosya" - ve o da curudu (Astra, 21.09 12:11):
  - Baska bir notta kimligin gecmesi borcu kapatiyordu; metin "Work has NOT
    been done" dese bile.
  - Borcun uc isinden (arsiv, terfi, harita) yalniz biri yapilinca kapaniyordu.
  - Damga saniyeye kirpildigi icin borctan ONCE yazilmis dosya bile yeni
    sayilabiliyordu.

BU SURUM: KANIT BULUSSAL DEGIL, ACIK BIR TAMAMLAMA KAYDIDIR.
Is biten ajan sunu calistirir:

    python araclar/devir.py --tamamlandi <event_id>

Bu, `tamamlanan/<event_id>.json` dosyasini yazar. Kanit budur: alt dize yok,
mtime karsilastirmasi yok, tahmin yok. Ajan calistirmazsa borc KAPANMAZ -
fazladan teslim olur ve sonunda raporlanir. Hata yonu guvenli tarafta.

GONDERICI ON KONTROLU GARANTI DEGIL, OPTIMIZASYONDUR.
`al()` kaniti kontrol eder ama kontrol ile `print` arasinda is bitebilir; Astra
bunu olctu. O yuzden TALIMATIN KENDISI olay kimligini tasir ve isleyiciye
"bunu zaten yaptiysan tekrarlama" der. Tekrara dayaniklilik isleyicinin
sorumlulugudur; gonderici yalniz gereksiz teslimi azaltir.

BILDIRIM, LISTELENDIGI ICIN DEGIL, ONAYLANDIGI ICIN KAPANIR.
`raporlanacaklar()` bir zamanlar okundugu anda kuyruktan cikariyordu - yani
duzeltmeye calistigim hatanin aynisi bir katman yukarida. Artik listeleme hicbir
sey degistirmez; girdi ancak `rapor_onayla()` ile gecmise gider ve onaysiz
girdi gecmis kapasitesine hic tabi olmaz.
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
TAMAMLANAN = kayit.PROJE_KOKU / "derleme" / "omurga-anlik" / "tamamlanan"
BAYAT_ESIK = timedelta(hours=12)

# Sahiplik omru. Isi degil, yalniz AYNI ANDA iki tuketicinin ayni borcu teslim
# etmesini engeller. Iki gercek Windows sureciyle olculdu (Astra [I9]).
SAHIPLIK_OMRU = timedelta(minutes=5)

MAX_DENEME = 3
GECMIS_SINIRI = 20  # YALNIZ kapanan ve onaylanan borclar icin

BEKLIYOR, TESLIM, KAPANDI, BASARISIZ, BAYAT = (
    "bekliyor", "teslim-edildi", "kapandi", "basarisiz", "bayat")
ACIK_DURUMLAR = (BEKLIYOR, TESLIM)
RAPORLANACAK = (BASARISIZ, BAYAT)


def _an(metin: str) -> datetime:
    return datetime.fromisoformat(metin).astimezone()


def _simdi() -> datetime:
    return datetime.now().astimezone()


def _yukselt(v: dict) -> dict:
    """Eski surum girdisini bu surume cevirir. Eski kutu bosa dusmesin."""
    v.setdefault("event_id", uuid.uuid4().hex)
    v.setdefault("durum", BEKLIYOR)
    v.setdefault("deneme", 0)
    v.setdefault("sahip", None)
    v.pop("kanit", None)  # bulussal kanit kaldirildi
    return v


def _oku() -> tuple[list[dict], list[dict]]:
    """(kuyruk, gecmis). SUZMEZ: bayat girdiyi okurken dusurmek kaybi gorunmez
    yapiyordu (K2). Bayatlik artik `al()` icinde damgalanir."""
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
        json.dumps({"surum": 4, "kuyruk": kuyruk,
                    "gecmis": gecmis[-GECMIS_SINIRI:]}, ensure_ascii=True),
        encoding="utf-8", newline="\n")
    os.replace(gecici, KUTU)


# ------------------------------------------------------------------- kanit


def tamamlandi(event_id: str) -> Path:
    """Borcun istedigi isin yapildigini KAYDA GECIRIR.

    Bunu is biten taraf calistirir. Tek kanit budur; bulussal cikarim yok.
    """
    TAMAMLANAN.mkdir(parents=True, exist_ok=True)
    p = TAMAMLANAN / f"{event_id}.json"
    p.write_text(json.dumps({"event_id": event_id,
                             "an": _simdi().isoformat(timespec="seconds")},
                            ensure_ascii=True), encoding="utf-8", newline="\n")
    return p


def _kanit_gerceklesti(borc: dict) -> bool:
    return (TAMAMLANAN / f"{borc['event_id']}.json").exists()


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
          event_id: str | None = None) -> str | None:
    """Borcu ekle; diger oturumun bekleyen kurtarma mesajini ezme.

    `event_id` disaridan verilebilir: cagiran, kimligi MESAJIN ICINE yazmak
    isteyebilir - isleyicinin tekrari taniyabilmesi icin gerekli.
    """
    event_id = event_id or uuid.uuid4().hex
    try:
        with kilit(KUTU.with_suffix(".lock")):
            kuyruk, gecmis = _oku()
            kuyruk.append({"event_id": event_id,
                           "an": _simdi().isoformat(timespec="microseconds"),
                           "metin": metin, "session_id": session_id,
                           "sahip": None, "deneme": 0, "durum": BEKLIYOR})
            _yaz(kuyruk, gecmis)
        return event_id
    except (OSError, ValueError, KeyError):
        print("UYARI: devir mesaji kuyruga yazilamadi; omurga dosyasini kontrol et.",
              file=sys.stderr)
        return None


# ------------------------------------------------------------------ okuma


def al(session_id: str | None = None, devral: bool = False) -> str | None:
    """Bir borcu teslim al.

    Sira, Astra'nin karsi orneklerine gore duzeltildi:
      1. KANIT once, ve `kapandi` disinda HER durum icin - gec gelen kanit
         basarisiz/bayat damgasini da kapatmali.
      2. Basarisizlik ancak CANLI SAHIP YOKKEN ilan edilir; son denemeye
         taninan sure bitmeden borc basarisiz sayilamaz.
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
                if borc["durum"] == KAPANDI:
                    continue
                if _kanit_gerceklesti(borc):  # gec kanit da kapatir
                    borc["durum"] = KAPANDI
                    borc["sahip"] = None
                    degisti = True
                    continue
                if borc["durum"] in RAPORLANACAK:
                    continue  # raporlanmayi bekliyor; teslim edilmez
                canli = _sahip_canli(borc, simdi)
                if simdi - _an(borc["an"]) > BAYAT_ESIK and not canli:
                    borc["durum"] = BAYAT
                    degisti = True
                    continue
                if borc["deneme"] >= MAX_DENEME and not canli:
                    borc["durum"] = BASARISIZ
                    degisti = True
                    continue
                if secilen is not None or canli:
                    continue
                if borc["deneme"] >= MAX_DENEME:
                    continue
                if not ((session_id and borc.get("session_id") == session_id)
                        or devral):
                    continue
                borc["sahip"] = {"bitis": (simdi + SAHIPLIK_OMRU)
                                 .isoformat(timespec="seconds")}
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


def raporlanacaklar() -> list[tuple[str, str]]:
    """(event_id, metin) - basarisiz ve bayat borclar. HICBIR SEY DEGISTIRMEZ.

    Listeleme onay degildir. Onceki surum okurken kuyruktan cikariyordu ve
    cikti basilmadan olen surecte bildirim kayboluyordu; sonra gecmis
    kapasitesi son izi de siliyordu (Astra [I11]). Onay ayri: `rapor_onayla`.
    """
    if not KUTU.exists():
        return []
    try:
        kuyruk, _ = _oku()
    except (OSError, ValueError, KeyError):
        return [("?", "DEVIR KUTUSU OKUNAMADI; kurtarma dosyalari denetlenmeli.")]
    return [(b["event_id"],
             f"{b['durum'].upper()} devir borcu ({b['an'][:16]}, "
             f"{b['deneme']} deneme, kimlik {b['event_id'][:8]}): "
             f"{b['metin'][:120]}")
            for b in kuyruk if b["durum"] in RAPORLANACAK]


def rapor_onayla(event_idler: list[str]) -> int:
    """Bildirimin GORULDUGUNU kaydet; ancak o zaman gecmise tasinir."""
    if not event_idler or not KUTU.exists():
        return 0
    try:
        with kilit(KUTU.with_suffix(".lock")):
            kuyruk, gecmis = _oku()
            onaylanan = [b for b in kuyruk
                         if b["event_id"] in event_idler
                         and b["durum"] in RAPORLANACAK]
            if not onaylanan:
                return 0
            kalan = [b for b in kuyruk if b not in onaylanan]
            _yaz(kalan, gecmis + onaylanan)
        return len(onaylanan)
    except (OSError, ValueError, KeyError):
        return 0


def main() -> int:
    if "--tamamlandi" in sys.argv:
        i = sys.argv.index("--tamamlandi") + 1
        if i >= len(sys.argv):
            print("--tamamlandi <event_id> ister", file=sys.stderr)
            return 2
        p = tamamlandi(sys.argv[i])
        print(f"tamamlandi: {p}")
        return 0
    try:
        girdi = json.loads(sys.stdin.read() or "{}")
    except (ValueError, OSError):
        girdi = {}
    parcalar = []
    metin = al(girdi.get("session_id"))
    if metin:
        parcalar.append(metin)
    dusen = raporlanacaklar()
    if dusen:
        parcalar.append(
            "TESLIM EDILEMEYEN DEVIR BORCU:\n"
            + "\n".join("  - " + d for _, d in dusen)
            + "\nBunlari kullaniciya soyle. Gorup islediysen kapat:\n"
            + "  python araclar/devir.py --tamamlandi <kimlik>")
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
