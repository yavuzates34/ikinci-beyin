#!/usr/bin/env python3
"""Oturum arsivinde anlamsal arama (yerel, cevrimdisi).

Ne zaman kullanilir: sozcuksel arama (ara.py) kelimeyi bildiginde yeter.
"Suna benzer bir sey dusunmustum ama kelimesini hatirlamiyorum" dediginde
yetmez. Burasi o durum icin.

Once ara.py denenmeli. Bu katman bedava degil: indeks kurulmasi ve arsiv
buyudukce tazelenmesi gerekiyor.

Nasil calisir: her mesaj bir vektore cevrilir, soru da vektore cevrilir,
en yakin komsular dondurulur. Kelime ortakligi aranmaz; anlam yakinligi aranir.
rclip'in gorsellerde yaptiginin metin karsiligi - ayni makinede, internetsiz.

Model: paraphrase-multilingual-mpnet-base-v2 (768 boyut, ~1 GB).
torch degil ONNX (fastembed) kullaniliyor: torch 2-3 GB ve C: dar.
Model ve indeks D:'ye kuruluyor (buyuk dosyalar D'ye kurallı).

Kullanim:
    python araclar/anlam.py --kur                  # indeksi kur/tazele (artimli)
    python araclar/anlam.py --kur --yenile         # sifirdan kur
    python araclar/anlam.py "ikinci beyin katmanlari"
    python araclar/anlam.py "hangi modeli sectik" --kapsam proje --adet 15
    python araclar/anlam.py --durum

Ilgili: BEYIN.md, ara.py (once bunu dene), omurga.py, oku.py
"""

import argparse
import io
import json
import os
import sys
import warnings
from pathlib import Path

import kayit

MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
# Buyuk dosyalar D'ye (C: ~10 GB bos, D: ~163 GB). Bkz. notlar/ortam-kurulum.md
KOK = Path(os.environ.get("BEYIN_INDEKS", r"D:\AI\beyin-indeks"))
MODEL_KOKU = Path(os.environ.get("BEYIN_MODEL", r"D:\AI\gomme"))
GOMME = KOK / "gomme.npy"
PARCA = KOK / "parca.jsonl"
KUNYE = KOK / "kunye.json"

PARCA_BOY = 1200  # karakter
BINDIRME = 200  # parcalar arasi ortusme, cumle ortasinda kesilen baglam icin


def parcala(metin: str):
    """Uzun mesajlari bindirmeli parcalara boler; kisa mesaj tek parca kalir."""
    if len(metin) <= PARCA_BOY:
        return [metin]
    parcalar, bas = [], 0
    while bas < len(metin):
        son = bas + PARCA_BOY
        if son < len(metin):  # kelime ortasinda kesme
            bosluk = metin.rfind(" ", bas + PARCA_BOY // 2, son)
            if bosluk > 0:
                son = bosluk
        parcalar.append(metin[bas:son].strip())
        if son >= len(metin):
            break
        bas = son - BINDIRME
    return [p for p in parcalar if p]


def _model():
    try:
        from fastembed import TextEmbedding
    except ImportError:
        print("HATA: fastembed kurulu degil -> python -m pip install fastembed",
              file=sys.stderr)
        raise SystemExit(1)
    MODEL_KOKU.mkdir(parents=True, exist_ok=True)
    # fastembed 0.8 bu model icin havuzlama degisikligini her cagride uyari
    # olarak basiyor; ciktinin basina karisiyor, bilgi degeri yok.
    warnings.filterwarnings("ignore", message=".*mean pooling.*")
    return TextEmbedding(model_name=MODEL, cache_dir=str(MODEL_KOKU))


def _kunye_oku() -> dict:
    if KUNYE.exists():
        return json.loads(KUNYE.read_text(encoding="utf-8"))
    return {"model": MODEL, "oturumlar": {}}


def kur(yenile: bool = False) -> int:
    import numpy as np

    KOK.mkdir(parents=True, exist_ok=True)
    kunye = {"model": MODEL, "oturumlar": {}} if yenile else _kunye_oku()
    if kunye.get("model") != MODEL:
        print(f"Model degismis ({kunye.get('model')} -> {MODEL}), sifirdan kuruluyor.")
        kunye = {"model": MODEL, "oturumlar": {}}
        yenile = True

    onceki = kunye["oturumlar"]
    havuz = kayit.oturumlar("hepsi")
    # Imza = boyut + son yazma. Degismeyen oturum yeniden gommeye girmez.
    yeni = [o for o in havuz if onceki.get(o.yol.name) != f"{o.boyut}:{int(o.an.timestamp())}"]

    if not yeni and not yenile and GOMME.exists():
        print(f"# Indeks guncel: {len(havuz)} oturum, degisen yok.")
        return 0

    print(f"# {len(havuz)} oturumun {len(yeni)} tanesi yeni/degismis, taraniyor...")

    # Degismeyen oturumlarin parcalarini koru, degisenleri bastan uret.
    tazele = {o.yol.name for o in yeni}
    eski_parca, eski_gomme = [], None
    if not yenile and PARCA.exists() and GOMME.exists():
        tut = []
        for i, satir in enumerate(io.open(PARCA, encoding="utf-8")):
            p = json.loads(satir)
            if p["dosya"] not in tazele:
                eski_parca.append(p)
                tut.append(i)
        if tut:
            eski_gomme = np.load(GOMME)[tut]
        print(f"# {len(eski_parca)} parca korunuyor.")

    taze = []
    for o in yeni:
        try:
            for m in kayit.mesajlar(o):
                for p in parcala(m.metin):
                    if len(p) < 40:  # tek kelimelik onaylar indekse girmesin
                        continue
                    taze.append({
                        "dosya": o.yol.name, "kaynak": o.kaynak, "kimlik": o.kimlik,
                        "proje": o.proje, "an": m.an.isoformat(timespec="minutes"),
                        "rol": m.rol, "metin": p,
                    })
        except (OSError, ValueError) as e:
            print(f"  atlandi {o.kisa}: {e}", file=sys.stderr)

    print(f"# {len(taze)} yeni parca gommeye giriyor (model yukleniyor)...")
    if taze:
        model = _model()
        vekt = []
        for i, v in enumerate(model.embed([p["metin"] for p in taze], batch_size=32), 1):
            vekt.append(v)
            if i % 500 == 0:
                print(f"  {i}/{len(taze)}")
        yeni_gomme = np.array(vekt, dtype="float32")
    else:
        yeni_gomme = np.zeros((0, 768), dtype="float32")

    parcalar = eski_parca + taze
    if eski_gomme is not None and len(eski_gomme):
        gomme = np.vstack([eski_gomme, yeni_gomme]) if len(yeni_gomme) else eski_gomme
    else:
        gomme = yeni_gomme

    # Kosinus benzerligi nokta carpima insin diye birim uzunluga getir.
    boy = np.linalg.norm(gomme, axis=1, keepdims=True)
    gomme = gomme / np.clip(boy, 1e-9, None)

    np.save(GOMME, gomme)
    with io.open(PARCA, "w", encoding="utf-8") as f:
        for p in parcalar:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    for o in havuz:
        kunye["oturumlar"][o.yol.name] = f"{o.boyut}:{int(o.an.timestamp())}"
    KUNYE.write_text(json.dumps(kunye, ensure_ascii=False), encoding="utf-8")

    print(f"# Indeks hazir: {len(parcalar)} parca, {gomme.nbytes / 2**20:.0f} MB "
          f"-> {KOK}")
    return 0


def durum() -> int:
    if not GOMME.exists():
        print(f"# Indeks yok. Kurmak icin: python araclar/anlam.py --kur\n# Yer: {KOK}")
        return 1
    import numpy as np

    g = np.load(GOMME, mmap_mode="r")
    kunye = _kunye_oku()
    print(f"# Indeks: {g.shape[0]} parca x {g.shape[1]} boyut, "
          f"{GOMME.stat().st_size / 2**20:.0f} MB")
    print(f"# Model: {kunye.get('model')}")
    print(f"# Kapsanan oturum: {len(kunye.get('oturumlar', {}))}")
    print(f"# Yer: {KOK}")
    return 0


def ara(soru: str, adet: int, kapsam: str, rol: str,
        sirala: str = "zaman", sonra: str | None = None) -> int:
    if not GOMME.exists():
        print("HATA: indeks yok -> python araclar/anlam.py --kur", file=sys.stderr)
        return 1
    import numpy as np

    gomme = np.load(GOMME)
    parcalar = [json.loads(s) for s in io.open(PARCA, encoding="utf-8")]
    if len(parcalar) != len(gomme):
        print("HATA: indeks bozuk (parca/gomme sayisi tutmuyor) -> "
              "python araclar/anlam.py --kur --yenile", file=sys.stderr)
        return 1

    proje = kayit.proje_adi()
    secim = [
        i for i, p in enumerate(parcalar)
        if (kapsam == "hepsi"
            or (kapsam == "proje" and p["proje"] == proje)
            or kapsam == p["kaynak"])
        and (rol == "hepsi" or p["rol"] == rol)
        and (not sonra or p["an"][:10] >= sonra)
    ]
    if not secim:
        print(f"HATA: '{kapsam}' kapsaminda parca yok", file=sys.stderr)
        return 1

    v = next(iter(_model().embed([soru])))
    v = np.asarray(v, dtype="float32")
    v /= max(float(np.linalg.norm(v)), 1e-9)

    skor = gomme[secim] @ v

    # Ayni metin birden fazla oturumda durabiliyor (devam ettirilen ya da
    # catallanan oturumlar ayni konusmayi tasir). Ayni cumleyi iki kez
    # gostermek sonuc sayisini bosa harciyor; ilk (en yakin) kopya tutulur.
    sira, gorulen = [], set()
    for j in np.argsort(-skor):
        imza = " ".join(parcalar[secim[j]]["metin"].split())[:200]
        if imza in gorulen:
            continue
        gorulen.add(imza)
        sira.append(j)
        if len(sira) >= adet:
            break

    # Benzerlik EN YAKIN olani bulur, EN GUNCEL olani degil. Bir konuda fikir
    # degistirdiysen, curutulmus eski bir cumle nihai karardan daha yuksek
    # skor alabilir. Bu yuzden secim benzerlige gore, GOSTERIM zamana gore:
    # ekranda en altta kalan satir en gunceli olur.
    if sirala == "zaman":
        sira = sorted(sira, key=lambda j: parcalar[secim[j]]["an"])

    print(f'\n# "{soru}" -> {len(secim)} parca icinde en yakin {len(sira)}')
    print(f"# secim: benzerlik | gosterim: {sirala}"
          + (f" | {sonra} sonrasi" if sonra else "") + "\n")

    for k, j in enumerate(sira, 1):
        p = parcalar[secim[j]]
        etiket = "BEN" if p["rol"] == kayit.KULLANICI else "MODEL"
        an = p["an"].replace("T", " ")[:16]
        metin = " ".join(p["metin"].split())
        son = sirala == "zaman" and k == len(sira)
        print(f"[{k}]{' <- EN GUNCEL' if son else ''} benzerlik {skor[j]:.3f}  "
              f"{p['kaynak']} {p['kimlik']}  {an}  {p['proje']}  {etiket}")
        print(f"    {metin[:400]}{'...' if len(metin) > 400 else ''}\n")

    yeni = max((parcalar[secim[j]] for j in sira), key=lambda p: p["an"])
    print(f"# En guncel eslesme: {yeni['an'].replace('T', ' ')[:16]} "
          f"({yeni['kaynak']} {yeni['kimlik']})")
    print(f"# Tam dokum: python araclar/oku.py {yeni['kimlik']} "
          f"--saat {yeni['an'][11:16]}")
    print("# UYARI: bunlar kanit, hukum degil. Bir konuda ne KARARLASTIRILDIGI "
          "notlar/ icinde yazar; arsiv o kararin nasil olustugunu gosterir.")
    return 0


def main() -> int:
    kayit.utf8_zorla()
    ap = argparse.ArgumentParser(description="Arsivde anlamsal arama")
    ap.add_argument("soru", nargs="?", help="aranacak tarif (kelime degil, anlam)")
    ap.add_argument("--kur", action="store_true", help="indeksi kur/tazele")
    ap.add_argument("--yenile", action="store_true", help="--kur ile: sifirdan")
    ap.add_argument("--durum", action="store_true")
    ap.add_argument("--adet", type=int, default=8)
    # Varsayilan "proje": anlamsal arama dar kapsamda iyi, tum arsivde zayif
    # (skorlar 0.53-0.68 bandina sikisiyor). Iyi olan durum varsayilan olmali.
    ap.add_argument("--kapsam", default="proje",
                    choices=["proje", "claude", "codex", "hepsi"])
    ap.add_argument("--rol", default="hepsi", choices=["kullanici", "model", "hepsi"])
    ap.add_argument("--sirala", default="zaman", choices=["zaman", "benzerlik"],
                    help="gosterim sirasi (varsayilan zaman: son soz en altta)")
    ap.add_argument("--sonra", help="YYYY-AA-GG tarihinden sonrasi")
    a = ap.parse_args()

    if a.durum:
        return durum()
    if a.kur:
        return kur(a.yenile)
    if not a.soru:
        ap.print_help()
        return 1
    return ara(a.soru, a.adet, a.kapsam, a.rol, a.sirala, a.sonra)


if __name__ == "__main__":
    sys.exit(main())
