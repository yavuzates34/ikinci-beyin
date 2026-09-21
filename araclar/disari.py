#!/usr/bin/env python3
"""Kasadan disari cikan her seyin tek kapisi - ve disaridaki sizintinin bulucusu.

NEDEN VAR
`gorunurluk.py` bir SORU cevaplar: "bu dosya nereye kadar gidebilir?" Ama soru
sorulmazsa cevap da yoktur. Olculdu (claude 96517e26 · 21.09 07:52):
`disari_cikabilir()` fonksiyonunun kasada SIFIR cagiran noktasi vardi, oysa
AGENTS.md "model cagiran her yol bundan gecer" diyordu. Kural yaziliydi,
kurulu degildi.

Ayni olcumde gercek bir sizinti yolu bulundu: `gece_kayit.yazdir()` her gece
tam omurgayi (ham kullanici mesajlari, 600 KB'a kadar) bir model surecine
boruyor. Omurganin kaynagi ham oturum kaydi; o dosya proje kokunun disinda,
yani `ozel`. Avenox'a gerek yoktu - sizinti bizimdi.

UC KATMAN, GUCTEN ZAYIFA
1. KAPI  (`kapi`, `dene`)   Bizim kodumuz gondermeden once sorar. Gecmezse
                            gondermez. Yalniz bizim kodumuzu baglar.
2. YANSIMA (`yansit`)       Yabanci araca kasanin kendisi DEGIL, yalniz
                            cikabilenlerden olusan bir kopya verilir. Arac
                            kurala uymak zorunda degil: yasak icerik orada
                            yoktur. Sozlesmeyi bayta cevirir.
3. BULUCU (`denetle`)       Herhangi bir agaci tarar, icinde `ozel` iceriginin
                            izi var mi bakar. Yabanci arac kasayi dogrudan
                            okuduysa yakalanan tek katman budur.

Katman 2 tasiyicidir: yalniz o, "rica" olmaktan cikip "orada yok"a doner.
Katman 1 ve 3 onu cevreler. Ucu birden, bir aracin kasayi kendi basina
taramasini ENGELLEMEZ - onu ancak isletim sistemi izinleri engeller. Lab'de
`avenox` kullanicisinin sudo'su yok; ayni ayrim burada dosya izniyle de
kurulabilir. Bu dosya o adimi atmaz, cunku kendi araclarimizi da kilitlerdi.

IMZA NEDIR
Bulucu, `ozel` dosyalardan "imza satiri" cikarir: kasanin TAMAMINDA yalniz bir
kez gecen, yeterince uzun bir satir. Tek kez gecmesi sarti sablon/baslik
gurultusunu tanim geregi eler. Boyle bir satir yabanci bir agacta gorunuyorsa
oraya bizden gitmistir. Parcalayarak indeksleyen araclari da yakalar, cunku
parca genelde satiri butun tasir.

Kullanim:
    python araclar/disari.py --kapi notlar/acik-uclar.md BEYIN.md
    python araclar/disari.py --yansit <dizin> --hedef model
    python araclar/disari.py --denetle <dizin>
    python araclar/disari.py --imza-sayisi

Ilgili: gorunurluk.py, AGENTS.md, notlar/acik-uclar.md (madde 8), gece_kayit.py
"""

import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Iterable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gorunurluk  # noqa: E402

KOK = gorunurluk.KOK
YANSIMA_KUNYESI = "_yansima.json"

# Imza satiri esigi. 60 karakter altindaki satirlar teknik metinde sik tekrar
# eder ve yanlis alarm uretir; ustu pratikte tek bir cumledir.
IMZA_UZUNLUK = 60
IMZA_BASINA = 4  # dosya basina en fazla kac imza taranir

# Satir basi/sonu isaretlerini atip bosluklari tekillestirir. Bir aracin
# yeniden bicimlendirdigi metni de yakalamak icin.
_BOSLUK = re.compile(r"\s+")


class Engel(NamedTuple):
    yol: str
    duzey: str
    neden: str


class Karar(NamedTuple):
    gecti: bool
    hedef: str
    izin: tuple[str, ...]
    engel: tuple[Engel, ...]

    @property
    def mesaj(self) -> str:
        if self.gecti:
            return f"{len(self.izin)} dosya '{self.hedef}' hedefine cikabilir"
        satir = [f"GORUNURLUK KAPISI KAPALI (hedef={self.hedef}): "
                 f"{len(self.engel)} dosya cikamaz."]
        for e in self.engel:
            satir.append(f"  {e.yol}  [{e.duzey}] {e.neden}")
        satir.append("  Karar kullanicinin: ya gonderim bu dosyayi disarida")
        satir.append("  birakacak, ya da gorunurluk.json'a acik bir kural girecek.")
        return "\n".join(satir)


class SizintiHatasi(RuntimeError):
    """Kapidan gecmeyen bir gonderim denendi."""


class Sizinti(NamedTuple):
    dosya: str  # taranan agactaki yol
    tur: str  # "birebir-kopya" | "imza" | "yol"
    kaynak: str  # kasadaki hangi `ozel` dosyadan
    kanit: str


# --------------------------------------------------------------------- kapi


def _goster(yol) -> str:
    """Kasaya gore yol; disarida kalanlar oldugu gibi yazilir."""
    try:
        return gorunurluk._bagil(yol)
    except ValueError:
        return str(Path(yol))


def _neden(yol, duzey: str) -> str:
    try:
        bagil = gorunurluk._bagil(yol)
    except ValueError:
        return "proje kokunun disinda - disarisi hakkinda soz veremeyiz"
    if bagil in gorunurluk.etiketsizler():
        return "etiketsiz, varsayilanla ozel"
    return f"gorunurluk.json kurali: {duzey}"


def dene(yollar: Iterable, hedef: str = "model") -> Karar:
    """Bir gonderimde gecen butun yollari birden denetler.

    Tek tek degil birden, cunku gonderim bolunemez: bir istem icinde bir
    dosya bile cikamiyorsa istemin tamami cikamaz.
    """
    izin, engel = [], []
    for y in yollar:
        g = _goster(y)
        if gorunurluk.disari_cikabilir(y, hedef):
            izin.append(g)
        else:
            d = gorunurluk.duzey(y)
            engel.append(Engel(g, d, _neden(y, d)))
    return Karar(not engel, hedef, tuple(izin), tuple(engel))


def kapi(yollar: Iterable, hedef: str = "model") -> Karar:
    """dene()'nin sert hali: gecmezse istisna atar.

    Gonderimi yazan kodun hatayi yutmasi zor olsun diye ayri fonksiyon.
    """
    k = dene(yollar, hedef)
    if not k.gecti:
        raise SizintiHatasi(k.mesaj)
    return k


# ------------------------------------------------------------------ yansima


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for blok in iter(lambda: f.read(1 << 16), b""):
            h.update(blok)
    return h.hexdigest()


def _commit() -> str:
    try:
        s = subprocess.run(["git", "rev-parse", "HEAD"], cwd=KOK,
                           capture_output=True, text=True, timeout=10)
        return s.stdout.strip() if s.returncode == 0 else "?"
    except (OSError, subprocess.TimeoutExpired):
        return "?"


def _yansima_hedefi_uygun(cikti: Path) -> str | None:
    """Yansimanin yazilabilecegi yer mi? Uygunsa None, degilse gerekce."""
    c = cikti.resolve()
    k = KOK.resolve()
    if c == k or k in c.parents:
        return (f"yansima kasanin ICINE yazilamaz ({c}). Icine yazilirsa "
                f"kasayi tarayan arac yansimayi da tarar; sizinti kapanmaz, "
                f"bir kopya daha olur.")
    if c in k.parents:
        return f"yansima kasayi kapsayan bir dizine yazilamaz ({c})"
    if c.exists():
        if not c.is_dir():
            return f"{c} bir dizin degil"
        icerik = list(c.iterdir())
        if icerik and not (c / YANSIMA_KUNYESI).exists():
            return (f"{c} bos degil ve bizim yansimamiz degil "
                    f"({len(icerik)} girdi, {YANSIMA_KUNYESI} yok). "
                    f"Uzerine yazmiyorum.")
    return None


def yansit(cikti, hedef: str = "model", kuru: bool = False) -> dict:
    """Kasanin yalniz `hedef`e cikabilen dosyalarindan olusan bir kopya uretir.

    Yabanci araca verilecek olan budur, kasanin kendisi degil. Yazdiktan sonra
    ciktiyi YENIDEN tarar ve her dosyanin kapidan gectigini dogrular; gecmeyen
    varsa ciktiyi siler ve basarisiz doner. Kendi kodumuza da guvenmeyiz.
    """
    cikti = Path(cikti)
    gerekce = _yansima_hedefi_uygun(cikti)
    if gerekce:
        return {"tamam": False, "hata": gerekce}

    alinan, birakilan = [], []
    for p in gorunurluk.taranacak_dosyalar():
        (alinan if gorunurluk.disari_cikabilir(p, hedef) else birakilan).append(p)

    # Uzanti suzgecinin disinda kalanlar sessizce dusmesin: rapor edilir.
    suzgec_disi = sum(
        1 for p in KOK.rglob("*")
        if p.is_file()
        and not any(par in gorunurluk.ATLA for par in p.relative_to(KOK).parts)
        and p.suffix.lower() not in {".md", ".py", ".json", ".txt", ".ps1",
                                     ".cjs", ".cmd"})

    ozet = {"tamam": True, "hedef": hedef, "cikti": str(cikti.resolve()),
            "alinan": len(alinan), "birakilan": len(birakilan),
            "uzanti_disi_birakilan": suzgec_disi, "kuru": kuru}
    if kuru:
        ozet["ornek"] = [gorunurluk._bagil(p) for p in alinan[:10]]
        return ozet

    if cikti.exists():
        shutil.rmtree(cikti)
    cikti.mkdir(parents=True)
    kunye = {"hedef": hedef, "an": datetime.now().isoformat(timespec="seconds"),
             "commit": _commit(), "uretici": "araclar/disari.py", "dosyalar": {}}
    for p in alinan:
        bagil = gorunurluk._bagil(p)
        varis = cikti / bagil
        varis.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, varis)
        kunye["dosyalar"][bagil] = _sha(p)
    (cikti / YANSIMA_KUNYESI).write_text(
        json.dumps(kunye, ensure_ascii=False, indent=2), encoding="utf-8")

    kacak = [y for y in kunye["dosyalar"]
             if not gorunurluk.disari_cikabilir(KOK / y, hedef)]
    if kacak:
        shutil.rmtree(cikti)
        return {"tamam": False,
                "hata": f"yansima dogrulamasi COKTU: {kacak[:5]} cikamamaliydi. "
                        f"Cikti silindi."}
    ozet["kunye"] = str((cikti / YANSIMA_KUNYESI).resolve())
    return ozet


# -------------------------------------------------------------------- bulucu


def _metin(p: Path, sinir: int = 4 << 20) -> str | None:
    try:
        ham = p.read_bytes()[:sinir]
    except OSError:
        return None
    if b"\x00" in ham[:4096]:
        return None
    try:
        return ham.decode("utf-8")
    except UnicodeDecodeError:
        return ham.decode("utf-8", "ignore")


def _satirlar(metin: str) -> list[str]:
    return [_BOSLUK.sub(" ", s).strip() for s in metin.splitlines()]


def imzalar() -> dict[str, list[str]]:
    """`ozel` dosyalardan imza satirlari. Kasada TEK KEZ gecenler secilir.

    Tek kez gecme sarti, sablon ve baslik gurultusunu tanim geregi eler:
    "## Acik uclar" gibi bir satir birden cok dosyada oldugu icin imza olamaz.
    """
    sayac: Counter[str] = Counter()
    dosya_satirlari: dict[Path, list[str]] = {}
    for p in gorunurluk.taranacak_dosyalar():
        m = _metin(p)
        if m is None:
            continue
        sat = [s for s in _satirlar(m) if len(s) >= IMZA_UZUNLUK]
        dosya_satirlari[p] = sat
        sayac.update(set(sat))

    sonuc: dict[str, list[str]] = {}
    for p, sat in dosya_satirlari.items():
        if gorunurluk.duzey(p) != "ozel":
            continue
        tekil = [s for s in dict.fromkeys(sat) if sayac[s] == 1]
        tekil.sort(key=len, reverse=True)
        if tekil:
            sonuc[gorunurluk._bagil(p)] = tekil[:IMZA_BASINA]
    return sonuc


def denetle(dizin, hedef: str = "model") -> list[Sizinti]:
    """Herhangi bir agacta `ozel` icerigin izi var mi.

    Uc kontrol: birebir dosya kopyasi (sha256), imza satiri, ve kasadaki
    yasakli bir yolun aynen tekrarlanmasi. Ilk ikisi icerige bakar, yani
    dosya adi degistirilmis olsa da yakalar.

    Bu bir KANIT aracidir, garanti degil: ozetlenmis, cevrilmis ya da
    yeniden yazilmis icerigi yakalamaz.
    """
    dizin = Path(dizin).resolve()
    ozel_hash: dict[str, str] = {}
    for p in gorunurluk.taranacak_dosyalar():
        if gorunurluk.duzey(p) == "ozel":
            ozel_hash[_sha(p)] = gorunurluk._bagil(p)
    imza = imzalar()

    bulgu: list[Sizinti] = []
    for p in sorted(dizin.rglob("*")):
        if not p.is_file():
            continue
        if any(par in gorunurluk.ATLA for par in p.relative_to(dizin).parts):
            continue
        bagil = p.relative_to(dizin).as_posix()
        if bagil == YANSIMA_KUNYESI:
            continue

        h = _sha(p)
        if h in ozel_hash:
            bulgu.append(Sizinti(bagil, "birebir-kopya", ozel_hash[h],
                                 f"sha256={h[:12]}"))
            continue

        if not gorunurluk.disari_cikabilir(KOK / bagil, hedef):
            if (KOK / bagil).exists():
                bulgu.append(Sizinti(bagil, "yol", bagil,
                                     "kasada ayni yol var ve cikamaz"))

        m = _metin(p)
        if m is None:
            continue
        duz = _BOSLUK.sub(" ", m)
        for kaynak, satirlar in imza.items():
            for s in satirlar:
                if s in duz:
                    bulgu.append(Sizinti(bagil, "imza", kaynak,
                                         s[:80] + ("..." if len(s) > 80 else "")))
                    break
    return bulgu


# ----------------------------------------------------------------------- CLI


def main() -> int:
    arg = sys.argv[1:]
    hedef = arg[arg.index("--hedef") + 1] if "--hedef" in arg else "model"

    if "--kapi" in arg:
        i = arg.index("--kapi") + 1
        yollar = []
        while i < len(arg) and not arg[i].startswith("--"):
            yollar.append(arg[i])
            i += 1
        if not yollar:
            print("--kapi en az bir yol ister", file=sys.stderr)
            return 2
        k = dene(yollar, hedef)
        print(k.mesaj)
        return 0 if k.gecti else 1

    if "--yansit" in arg:
        cikti = arg[arg.index("--yansit") + 1]
        o = yansit(cikti, hedef, kuru="--kuru" in arg)
        if not o["tamam"]:
            print("YANSIMA YAZILMADI:", o["hata"], file=sys.stderr)
            return 1
        print(f"YANSIMA ({o['hedef']}) -> {o['cikti']}")
        print(f"  alinan    : {o['alinan']} dosya")
        print(f"  birakilan : {o['birakilan']} dosya (gorunurluk)")
        if o["uzanti_disi_birakilan"]:
            print(f"  {o['uzanti_disi_birakilan']} dosya uzanti suzgeci disinda "
                  f"kaldi; yansimada YOK")
        if o["kuru"]:
            print("  (kuru calisma - hicbir sey yazilmadi)")
        return 0

    if "--denetle" in arg:
        d = arg[arg.index("--denetle") + 1]
        bulgu = denetle(d, hedef)
        if not bulgu:
            print(f"TEMIZ: {d} icinde `ozel` icerik izi bulunmadi.")
            print("  (birebir kopya, imza satiri ve yol kontrolu yapildi;")
            print("   ozetlenmis/yeniden yazilmis icerik yakalanmaz)")
            return 0
        print(f"SIZINTI: {len(bulgu)} bulgu")
        for b in bulgu:
            print(f"  [{b.tur}] {b.dosya}")
            print(f"      kaynak: {b.kaynak}")
            print(f"      kanit : {b.kanit}")
        return 1

    if "--imza-sayisi" in arg:
        im = imzalar()
        print(f"{len(im)} `ozel` dosyadan "
              f"{sum(len(v) for v in im.values())} imza satiri cikarildi")
        return 0

    print(__doc__.split("Kullanim:")[1].strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
