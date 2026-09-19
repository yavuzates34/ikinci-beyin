#!/usr/bin/env python3
"""Baglam dolulugu ve erken devir uyarisi - saglayicidan bagimsiz cekirdek.

NEDEN VAR (onarim listesi madde 6-7)
Ana kapanis yolu, kullanicinin anlamli bir yerde "oturumu kapatalim"
demesiydi. Bu yol, kullanicinin baglam dolulugunu gormesine dayaniyordu. Codex
Desktop bu sayaci gostermiyor. Olculdu: 01a0ba74 oturumu uyarisiz %83'e
cikti ve 20:07'de sikistirildi (claude 5c600e7e · 19.09 20:28). PreCompact
son savunma hattidir, kontrollu devir degildir.

KARAR (kullanici, 19.09.2026 · claude 5c600e7e · 19.09 20:12)
- %50'de uyar, %70'te tekrar uyar.
- Esik asilinca tur sonunda uyar ve omurgayi diske al. Kapanisi kullanici
  "devret" ya da "kapatalim" diyerek baslatir.
- `kapanan-oturum:` yalnizca gercek gecis onayiyla yazilir. Onayi kullanici
  verir; ileride yetkili bir orkestrator ajan da verebilir.

OLCUM KAYNAKLARI (ikisi de ham kayittan, arayuzden bagimsiz)
- Codex: son `token_count` olayi. Doluluk
  `last_token_usage.input_tokens / model_context_window`; pencere kayitta var.
- Claude: son ana zincir asistan satirinin `message.usage` alani. Doluluk
  `input + cache_read + cache_creation`. Pencere kayitta YOK.
  PENCERE tablosundan gelir. Tablodaki deger kalibre edildi: 472.650 token
  arayuzde yaklasik %45-50 goruldu, yani pencere yaklasik 1M
  (claude 5c600e7e · 19.09 20:26). Pencere bilinmiyorsa yuzde uretilmez;
  uyari "olculemedi" der, sayac varmis gibi davranmaz.

TETIK
Tur sinirinda calisir: `devir.py`, UserPromptSubmit'te bunu cagirir.
Kullanici yeni mesaj yazdiginda onceki tur bitmistir; yani uyari cumlenin
ortasina degil, anlamli bir sinira duser. Ayni seviye tekrar uyarilmaz;
yalnizca seviye yukselince uyarilir.

Kullanim:
    python araclar/baglam.py <oturum-id>    # olcumu ekrana bas
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kayit  # noqa: E402

KOK = kayit.PROJE_KOKU
DURUM = KOK / "derleme" / "baglam-durum.json"
ANLIK = KOK / "derleme" / "omurga-anlik"
ESIKLER = (0.50, 0.70)  # kullanici karari 19.09
# Claude kaydinda pencere yok. Model adina gore; kalibrasyon kaynagi yukarida.
PENCERE = {"claude-opus-5": 1_000_000}


def _claude_olc(yol: Path) -> dict:
    son = None
    for satir in open(yol, encoding="utf-8", errors="replace"):
        if '"usage"' not in satir:
            continue
        try:
            k = json.loads(satir)
        except ValueError:
            continue
        if k.get("type") == "assistant" and not k.get("isSidechain"):
            m = k.get("message") or {}
            if m.get("usage"):
                son = m
    if not son:
        return {"token": None, "pencere": None, "not": "usage kaydi yok"}
    u = son["usage"]
    token = (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
             + u.get("cache_creation_input_tokens", 0))
    model = str(son.get("model", ""))
    pencere = next((v for k, v in PENCERE.items() if model.startswith(k)), None)
    return {"token": token, "pencere": pencere, "model": model,
            "not": None if pencere else f"pencere bilinmiyor ({model})"}


def _codex_olc(yol: Path) -> dict:
    son = None
    for satir in open(yol, encoding="utf-8", errors="replace"):
        if '"token_count"' not in satir:
            continue
        try:
            p = json.loads(satir).get("payload") or {}
        except ValueError:
            continue
        if p.get("type") == "token_count" and p.get("info"):
            son = p["info"]
    if not son:
        return {"token": None, "pencere": None, "not": "token_count kaydi yok"}
    return {"token": (son.get("last_token_usage") or {}).get("input_tokens"),
            "pencere": son.get("model_context_window"), "not": None}


def olc(oturum: kayit.Oturum) -> dict:
    o = _codex_olc(oturum.yol) if oturum.kaynak == "codex" else _claude_olc(oturum.yol)
    o["kaynak"] = oturum.kaynak
    o["yuzde"] = (round(o["token"] / o["pencere"], 3)
                  if o.get("token") and o.get("pencere") else None)
    return o


def _durum_oku() -> dict:
    try:
        return json.loads(DURUM.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _omurga_al(oturum: kayit.Oturum, seviye: int) -> str | None:
    """Kurtarma kontrol noktasi: tam omurga diske. Hata yutulur."""
    try:
        from omurga import omurga_metni
        metin, _, _ = omurga_metni(oturum, tam=True)
        ANLIK.mkdir(parents=True, exist_ok=True)
        yuzde = int(ESIKLER[seviye - 1] * 100)
        p = ANLIK / f"{datetime.now():%Y-%m-%d-%H%M}-{oturum.kisa}-esik{yuzde}.md"
        p.write_text(metin, encoding="utf-8")
        try:
            return p.relative_to(KOK).as_posix()
        except ValueError:  # proje disi (sinama): tam yol
            return p.as_posix()
    except Exception:  # noqa: BLE001
        return None


def kontrol(transcript_path: str | None, session_id: str | None) -> str | None:
    """Tur sinirinda cagrilir. Esik yeni asildiysa uyari metni dondurur."""
    oturum = None
    if transcript_path and Path(transcript_path).exists():
        p = Path(transcript_path)
        kaynak = "codex" if ".codex" in p.parts else "claude"
        kimlik = session_id or p.stem
        st = p.stat()
        oturum = kayit.Oturum(kaynak, kimlik, p, p.parent.name,
                              datetime.fromtimestamp(st.st_mtime), st.st_size)
    elif session_id:
        oturum = kayit.oturum_bul(session_id[:8], "hepsi")
    if oturum is None:
        return None

    o = olc(oturum)
    durum = _durum_oku()
    onceki = durum.get(oturum.kisa, {}).get("seviye", 0)
    yuzde = o.get("yuzde")
    if yuzde is None:
        return None  # olculemeyen oturumda her tur uyarmak gurultu olur
    seviye = sum(1 for e in ESIKLER if yuzde >= e)
    # Compact sonrasi doluluk duser: seviye geri iner, sonra yeniden uyarabilir.
    durum[oturum.kisa] = {"seviye": seviye, "yuzde": yuzde,
                          "an": datetime.now().isoformat(timespec="minutes")}
    try:
        DURUM.parent.mkdir(parents=True, exist_ok=True)
        DURUM.write_text(json.dumps(durum, ensure_ascii=False, indent=1),
                         encoding="utf-8")
    except OSError:
        pass
    if seviye <= onceki:
        return None

    anlik = _omurga_al(oturum, seviye)
    son_cagri = seviye == len(ESIKLER)
    return (
        f"BAGLAM {yuzde:.0%} ({o['token']:,} / {o['pencere']:,} token, kaynak: "
        f"{oturum.kaynak} ham kaydi). Esik %{int(ESIKLER[seviye - 1] * 100)} asildi"
        + (" - SON CAGRI" if son_cagri else "") + ".\n"
        + (f"Kurtarma icin omurga diske alindi: {anlik}\n" if anlik else "")
        + "Bu turun cevabinin SONUNDA kullaniciya tek cumleyle soyle: anlamli "
        "bir yerde 'devret' ya da 'oturumu kapatalim' diyebilir, devam etmek "
        "de serbest. Konuyu kesme. `kapanan-oturum:` yalnizca gercek gecis "
        "onayiyla yazilir (kullanici ya da yetkili orkestrator ajan)."
        + (" %70'i gectik: kapanis notunu yazacak yer daraliyor." if son_cagri else "")
    )


if __name__ == "__main__":
    kayit.utf8_zorla()
    if len(sys.argv) < 2:
        print("kullanim: python araclar/baglam.py <oturum-id>")
        sys.exit(1)
    o_ = kayit.oturum_bul(sys.argv[1], "hepsi")
    if not o_:
        print(f"HATA: {sys.argv[1]} yok")
        sys.exit(1)
    print(json.dumps(olc(o_), ensure_ascii=False, indent=1))
