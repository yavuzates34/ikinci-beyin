#!/usr/bin/env python3
"""Aksam derleyicisi - her gece calisir, derleme/ altina rapor yazar.

ILKE: OLCER, YAZMAZ.
Anlati uretmez, sayi uretir. Gerekce notlar/tasarim-dersleri.md icindeki kural:
olculebileni olc, olculemeyeni yaz. Anlatiyi model kapanista yazar; derleyici
anlati yazarsa vasat ozet uretip kalici katmani kirletir.

UC CIKTI
  gunluk/  : o gun kapanis kaydi yazilmadan biten oturumlarin DEDEKTORU
  haftalik/: faaliyet dokumu (kac oturum, hangi projeler, neler degisti)
  aylik/   : acik uclarin YASI + damitma kalitesi gostergesi

Ayrica her calismada:
  - git commit (yerel surum gecmisi; push kullanici hazir oldugunda)
  - 30 gunden eski omurga-anlik anlik goruntulerini temizler

Kullanim:
    python araclar/derle.py            # gunluk; pazartesi haftalik, ayin 1'i aylik
    python araclar/derle.py --hepsi    # ucunu de zorla (sinama icin)
    python araclar/derle.py --kuru     # hicbir sey yazma, ekrana bas
"""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kayit  # noqa: E402

KOK = kayit.PROJE_KOKU
DERLEME = KOK / "derleme"
ANLIK_OMUR = 30  # gun
# Kayit boyutunun konusma metnine orani bunun altindaysa "ince" sayilir.
# Kaliteyi yargilamiyor, ORANTISIZLIGI gosteriyor.
INCE_ESIK = 0.02


def git(*arg) -> str:
    try:
        s = subprocess.run(["git", *arg], cwd=KOK, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        return s.stdout.strip()
    except OSError:
        return ""


def islenmis_kimlikler() -> set:
    """notlar/ ve oturumlar/ icinde adi gecen oturum kimlikleri (ilk 8 karakter)."""
    metin = []
    for klasor in ("notlar", "oturumlar"):
        for p in (KOK / klasor).glob("*.md"):
            metin.append(p.read_text(encoding="utf-8", errors="replace"))
    return " ".join(metin)


def yaz(yol: Path, govde: str, kuru: bool) -> None:
    if kuru:
        print(f"\n===== {yol.relative_to(KOK)} =====\n{govde}")
        return
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(govde, encoding="utf-8")
    print(f"  yazildi: {yol.relative_to(KOK)} ({len(govde)} bayt)")


# ---------------------------------------------------------------- GUNLUK
def gunluk(bugun: datetime, kuru: bool) -> int:
    dun = bugun - timedelta(days=1)
    # Dedektor SADECE bu projeyi izler. Diger projelerde bu yapi henuz yok;
    # onlari "islenmemis" diye listelemek her gece onlarca satir gurultu uretir
    # ve rapor coplugee doner. Yapi baska projeye tasindiginda orada kendi
    # derleyicisi calisir. Diger projeler burada sadece tek satir sayidir.
    taze = [o for o in kayit.oturumlar("proje") if o.an >= dun]
    diger = [o for o in kayit.oturumlar("claude") if o.an >= dun and o not in taze]
    metinler = islenmis_kimlikler()

    islenmemis, islenmis = [], []
    for o in taze:
        (islenmis if o.kimlik[:8] in metinler else islenmemis).append(o)

    s = [f"# Gunluk derleme - {bugun:%d.%m.%Y}", "",
         f"Bu projede son 24 saatte yazilan oturum kaydi: **{len(taze)}**",
         f"Diger projelerde: {len(diger)} oturum (bu yapi orada henuz yok, "
         f"dedektor kapsam disi)", ""]

    if islenmemis:
        s += ["## ISLENMEMIS OTURUMLAR", "",
              "Bu oturumlarin kimligi hicbir notta gecmiyor - yani kapanis kaydi",
              "yazilmamis olabilir. Kalici olan bir sey varsa kaybolmadan isle.", ""]
        for o in islenmemis:
            s.append(f"- `{o.kimlik[:8]}` | {o.proje} | son yazma {o.an:%d.%m %H:%M} "
                     f"| {o.boyut / 1024:.0f} KB")
            s.append(f"  - oku: `python araclar/omurga.py {o.kimlik[:8]}`")
        s.append("")
    else:
        s += ["## Islenmemis oturum yok", "",
              "Son 24 saatte yazilan her oturumun kimligi en az bir notta geciyor.", ""]

    if islenmis:
        s += ["## Islenmis", ""]
        s += [f"- `{o.kimlik[:8]}` | {o.proje} | {o.boyut / 1024:.0f} KB"
              for o in islenmis]
        s.append("")

    # PreCompact anlik goruntuleri + eskilerini temizle
    anlik = sorted((DERLEME / "omurga-anlik").glob("*.md"))
    yeni_anlik = [p for p in anlik
                  if datetime.fromtimestamp(p.stat().st_mtime) >= dun]
    silinen = 0
    for p in anlik:
        if datetime.fromtimestamp(p.stat().st_mtime) < bugun - timedelta(days=ANLIK_OMUR):
            if not kuru:
                p.unlink()
            silinen += 1
    s += [f"## PreCompact", "",
          f"Son 24 saatte alinan omurga anlik goruntusu: **{len(yeni_anlik)}** "
          f"(agin devreye girdigi an sayisi)",
          f"{ANLIK_OMUR} gunden eski silinen: {silinen}", ""]

    degisen = git("log", "--since=24 hours ago", "--name-only", "--pretty=format:")
    dosyalar = sorted({d for d in degisen.splitlines() if d.strip()})
    s += ["## Son 24 saatte degisen dosyalar (git)", ""]
    s += [f"- `{d}`" for d in dosyalar] if dosyalar else ["- (commit yok)"]
    s.append("")

    yaz(DERLEME / "gunluk" / f"{bugun:%Y-%m-%d}.md", "\n".join(s), kuru)
    return len(islenmemis)


# --------------------------------------------------------------- HAFTALIK
def haftalik(bugun: datetime, kuru: bool) -> None:
    esik = bugun - timedelta(days=7)
    havuz = [o for o in kayit.oturumlar("hepsi") if o.an >= esik]
    projeler = {}
    for o in havuz:
        projeler[o.proje] = projeler.get(o.proje, 0) + 1

    commit = git("log", "--since=7 days ago", "--oneline")
    commitler = [c for c in commit.splitlines() if c.strip()]

    s = [f"# Haftalik derleme - {esik:%d.%m} / {bugun:%d.%m.%Y}", "",
         f"Oturum: **{len(havuz)}** | Commit: **{len(commitler)}**", "",
         "## Projeye gore oturum", ""]
    s += [f"- {p}: {n}" for p, n in sorted(projeler.items(), key=lambda x: -x[1])]
    s += ["", "## Bu haftaki commitler", ""]
    s += [f"- {c}" for c in commitler] if commitler else ["- yok"]

    kalici = sorted((KOK / "notlar").glob("*.md"))
    toplam = sum(p.stat().st_size for p in kalici)
    s += ["", "## Kalici katman", "",
          f"- Not sayisi: {len(kalici)}",
          f"- Toplam boyut: {toplam / 1024:.1f} KB "
          f"({'ESIK ASILDI - haritadan gerekeni ac' if toplam > 65 * 1024 else 'esik altinda (65 KB)'})"]

    yaz(DERLEME / "haftalik" / f"{bugun:%Y-%m-%d}.md", "\n".join(s) + "\n", kuru)


# ------------------------------------------------------------------ AYLIK
def aylik(bugun: datetime, kuru: bool) -> None:
    s = [f"# Aylik derleme - {bugun:%m.%Y}", "",
         "## Acik uclarin yasi", "",
         "`notlar/acik-uclar.md` icindeki maddelerin git gecmisindeki yasi.",
         "Yas, git deposunun basladigi tarihten (16.09.2026) olculur.", ""]

    blame = git("blame", "--date=short", "-l", "notlar/acik-uclar.md")
    acik = []
    for satir in blame.splitlines():
        if ")" not in satir:
            continue
        bas, _, govde = satir.partition(")")
        govde = govde.strip()
        if not govde.startswith("- ") or govde.startswith("- ~~"):
            continue  # ustu cizili = kapanmis
        parca = bas.split()
        tarih = next((p for p in parca if p.count("-") == 2 and len(p) == 10), None)
        if not tarih:
            continue
        try:
            yas = (bugun - datetime.strptime(tarih, "%Y-%m-%d")).days
        except ValueError:
            continue
        acik.append((yas, govde[2:96]))

    if acik:
        for yas, govde in sorted(acik, reverse=True):
            isaret = " **<- 60 gunu gecti**" if yas > 60 else ""
            s.append(f"- {yas:>3} gun | {govde}{isaret}")
    else:
        s.append("- (olculemedi: git gecmisi yetersiz ya da acik madde yok)")

    s += ["", "## Damitma kalitesi gostergesi", "",
          "Bir oturumun konusma metni ile o oturum icin yazilan kaydin boyutu",
          "karsilastirilir. Kalite yargilanmiyor - ORANTISIZLIK gosteriliyor.",
          f"Esik: kayit, konusmanin %{INCE_ESIK * 100:.0f}'inden kucukse 'ince'.", ""]

    metinler = islenmis_kimlikler()
    kayitlar = {p.name: p.stat().st_size for p in (KOK / "oturumlar").glob("*.md")}
    toplam_kayit = sum(kayitlar.values())
    ince = []
    for o in kayit.oturumlar("proje"):
        if o.kimlik[:8] not in metinler:
            continue
        try:
            harf = sum(len(m.metin) for m in kayit.mesajlar(o))
        except OSError:
            continue
        if harf < 2000:
            continue
        oran = toplam_kayit / harf
        if oran < INCE_ESIK:
            ince.append((oran, o, harf))
    if ince:
        for oran, o, harf in sorted(ince):
            s.append(f"- `{o.kimlik[:8]}` | konusma {harf / 1024:.0f} KB | "
                     f"oran %{oran * 100:.1f} - **ince, gozden gecir**")
    else:
        s.append("- Orantisiz kayit bulunmadi.")

    yaz(DERLEME / "aylik" / f"{bugun:%Y-%m}.md", "\n".join(s) + "\n", kuru)


def main() -> int:
    kayit.utf8_zorla()
    ap = argparse.ArgumentParser(description="Aksam derleyicisi")
    ap.add_argument("--hepsi", action="store_true", help="uc raporu da zorla")
    ap.add_argument("--kuru", action="store_true", help="yazma, ekrana bas")
    a = ap.parse_args()

    bugun = datetime.now()
    print(f"# Derleme - {bugun:%d.%m.%Y %H:%M}")

    eksik = gunluk(bugun, a.kuru)
    if a.hepsi or bugun.weekday() == 0:
        haftalik(bugun, a.kuru)
    if a.hepsi or bugun.day == 1:
        aylik(bugun, a.kuru)

    if not a.kuru:
        git("add", "-A")
        durum = git("status", "--porcelain")
        if durum:
            git("-c", "core.quotepath=false", "commit", "-q", "-m",
                f"Derleme {bugun:%Y-%m-%d}")
            print(f"  git: commit atildi ({len(durum.splitlines())} dosya)")
        else:
            print("  git: degisiklik yok")

    # Sessiz basari yasak: ne bulundugunu sayiyla soyle.
    print(f"# Islenmemis oturum: {eksik}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
