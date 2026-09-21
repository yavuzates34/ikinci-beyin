#!/usr/bin/env python3
"""Hangi dosyanin icerigi nereye kadar gidebilir - tek karar noktasi.

NEDEN VAR
Tam otomasyon, sistemin kendi kendine karar vermesi demek: ornekleme denetimi,
eskime alarmi, "bu satir kalici mi" ayiklamasi. Bunlar tipli karar isleri ve
Opus cagirmak icin pahali; ucuz bir karar modeline (ornegin Jev) gitmeleri
mantikli. Ama bu, not iceriginin ucuncu bir saglayiciya gitmesi demek. Kasada
kullanicinin kisisel baglami ve musteri malzemesi var.

Avenox'un v3 cozumu olculdu: notlar private/internal/public olarak ayriliyor,
`private` olanlar saglayiciya hic gonderilmiyor (kurulu-kasa/docs/v3/JEV.md,
21.09.2026). Kullanici ayni ayrimi bizde de kurmaya karar verdi
(kullanici, 21.09 05:35).

TASARIM KARARI: etiket dosyanin icine gomulmuyor.
Proje bilerek sablondan kacinir ("zorunlu baslik bos baslik uretir", AGENTS.md)
ve 42 dosyanin hicbirinde frontmatter yok. Etiket ayri bir manifestoda durur:
gorunurluk.json. Bunun bedeli manifestonun bayatlamasidir; bedeli kabul
edilebilir kilan sey su:

    ESLESMEYEN HER SEY 'ozel' SAYILIR.

Yani manifesto bayatladiginda yeni bir dosya sessizce disari sizmaz, sadece
gereksiz yere kapali kalir ve `--etiketsiz` onu rapor eder. Hata yonu
guvenli taraftadir. Bu yuzden notlar/ ve rehber/ dosyalari tek tek yazilir,
"notlar/*" gibi toplu desen KULLANILMAZ - toplu desen yeni dosyayi da
kapsar ve varsayilani bozar.

Duzeyler:
    ozel  Makineden cikmaz. Dis modele gonderilmez, yayimlanmaz.
    ic    Bizim sectigimiz bir modele islenmek uzere gidebilir. Yayimlanmaz.
    acik  Yayimlanabilir.

Kullanim:
    python araclar/gorunurluk.py                 # tablo + etiketsizler
    python araclar/gorunurluk.py --etiketsiz     # yalniz etiketsizler
    python araclar/gorunurluk.py --dosya notlar/acik-uclar.md

Koddan:
    import gorunurluk
    gorunurluk.duzey("notlar/kullanici-baglami.md")          -> "ozel"
    gorunurluk.disari_cikabilir(yol, hedef="model")          -> False

Ilgili: BEYIN.md, AGENTS.md, notlar/olculmus-bulgular.md, bakim.py
"""

import fnmatch
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kayit  # noqa: E402

KOK = kayit.PROJE_KOKU
MANIFESTO = KOK / "gorunurluk.json"

# Dusukten yuksege. "model" hedefi ic'i de kabul eder, "yayin" yalniz acik'i.
SIRA = {"ozel": 0, "ic": 1, "acik": 2}

# Tarama disi: uretilen, gecici ya da surum kontrolu disi olanlar.
ATLA = {".git", "__pycache__", ".obsidian", "node_modules", ".pytest_cache"}


def _manifesto() -> dict:
    with MANIFESTO.open(encoding="utf-8") as f:
        return json.load(f)


def _bagil(yol) -> str:
    """Proje kokune gore POSIX yolu. Disarida kalan yol icin ValueError."""
    p = Path(yol)
    if not p.is_absolute():
        p = KOK / p
    return p.resolve().relative_to(KOK.resolve()).as_posix()


def _eslesir(desen: str, yol: str) -> bool:
    # "dizin/**" dizinin tamamini kapsar; fnmatch ** ayrimi yapmadigi icin
    # onek eslesmesi olarak ele alinir.
    if desen.endswith("/**"):
        return yol.startswith(desen[:-2])
    return fnmatch.fnmatchcase(yol, desen)


def bu_projenin_oturum_kaydi(yol) -> bool:
    """Ham oturum kaydi mi, ve BU KASANIN mi.

    `~/.claude/projects` butun projelerin kayitlarini tutar - Nar Ajans'inki
    dahil. Codex ise projeye gore klasorlemez; hangi kasaya ait oldugu kaydin
    ilk satirindaki `cwd`'dedir. Dis kaynak istisnasi YALNIZ bu soruya evet
    cevabi veren yola uygulanir; baska projenin kaydi `ozel` kalir.
    """
    p = Path(yol)
    if p.suffix.lower() != ".jsonl":
        return False
    try:
        p = p.resolve()
    except OSError:
        return False
    ev = Path.home()
    claude = (ev / ".claude" / "projects" / kayit.proje_adi(KOK)).resolve()
    if p.parent == claude:
        return True
    codex = (ev / ".codex").resolve()
    if codex in p.parents:
        return kayit._codex_cwd(p) == str(KOK).lower()
    return False


def _dis_duzey(yol, m: dict) -> str:
    """Kasa disindaki yolun duzeyi. Varsayilan 'ozel' - disarisi hakkinda soz
    veremeyiz. Tek istisna manifestoda ADIYLA gecen dis kaynak turu, o da
    yalniz bu kasaya aitse."""
    for kural in m.get("dis_kaynaklar", []):
        if kural.get("tur") == "oturum-kaydi" and bu_projenin_oturum_kaydi(yol):
            return kural["duzey"]
    return "ozel"


def duzey(yol) -> str:
    """Dosyanin gorunurluk duzeyi. Ilk eslesen kural kazanir.

    Eslesme yoksa manifestodaki varsayilan doner ('ozel'). Proje kokunun
    disindaki bir yol da 'ozel' sayilir, `dis_kaynaklar` acikca aksini
    soylemedikce (bkz. `_dis_duzey`).
    """
    m = _manifesto()
    try:
        bagil = _bagil(yol)
    except ValueError:
        return _dis_duzey(yol, m)
    for kural in m["kurallar"]:
        if _eslesir(kural["desen"], bagil):
            return kural["duzey"]
    return m.get("varsayilan", "ozel")


def disari_cikabilir(yol, hedef: str = "model") -> bool:
    """Bu dosyanin icerigi verilen hedefe gonderilebilir mi.

    hedef="model"  bizim sectigimiz bir modele/servise islenmek uzere
    hedef="yayin"  herkese acik bir yere

    Model cagiran her kod once bunu sormak zorundadir. AGENTS.md'de yazili
    olmasi yetmez: kural ancak kod ona sordugunda kuraldir.
    """
    gerekli = {"model": "ic", "yayin": "acik"}[hedef]
    return SIRA[duzey(yol)] >= SIRA[gerekli]


def taranacak_dosyalar():
    """Kasadaki metin dosyalari, tarama disi dizinler atlanarak."""
    for p in sorted(KOK.rglob("*")):
        if not p.is_file():
            continue
        if any(par in ATLA for par in p.relative_to(KOK).parts):
            continue
        if p.suffix.lower() not in {".md", ".py", ".json", ".txt", ".ps1", ".cjs", ".cmd"}:
            continue
        yield p


def etiketsizler() -> list[str]:
    """Hicbir kurala uymayan, yani varsayilanla 'ozel' kalan dosyalar."""
    m = _manifesto()
    desenler = [k["desen"] for k in m["kurallar"]]
    bulunan = []
    for p in taranacak_dosyalar():
        bagil = _bagil(p)
        if not any(_eslesir(d, bagil) for d in desenler):
            bulunan.append(bagil)
    return bulunan


def _yaz_tablo() -> int:
    sayac = {"ozel": 0, "ic": 0, "acik": 0}
    for p in taranacak_dosyalar():
        sayac[duzey(p)] += 1
    print("GORUNURLUK")
    for d in ("ozel", "ic", "acik"):
        print(f"  {d:5s} {sayac[d]:4d} dosya")
    eksik = etiketsizler()
    print()
    if eksik:
        print(f"  !! ETIKETSIZ: {len(eksik)} dosya - varsayilanla 'ozel' sayiliyor")
        for y in eksik[:20]:
            print(f"     {y}")
        if len(eksik) > 20:
            print(f"     ... {len(eksik) - 20} dosya daha")
        print("  Sizma riski yok; bu dosyalar disari cikamaz. Etiketlemek")
        print("  isteyen gorunurluk.json'a satir ekler.")
    else:
        print("  etiketsiz dosya yok")
    return len(eksik)


def main() -> int:
    arg = sys.argv[1:]
    if "--dosya" in arg:
        yol = arg[arg.index("--dosya") + 1]
        d = duzey(yol)
        print(f"{yol}: {d}")
        print(f"  modele gidebilir : {disari_cikabilir(yol, 'model')}")
        print(f"  yayimlanabilir   : {disari_cikabilir(yol, 'yayin')}")
        return 0
    if "--etiketsiz" in arg:
        eksik = etiketsizler()
        for y in eksik:
            print(y)
        return 0
    _yaz_tablo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
