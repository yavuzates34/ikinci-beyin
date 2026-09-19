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
import json
import re
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


def islenmis_metin() -> str:
    """notlar/ ve oturumlar/ icindeki tum metin, tek parca.

    Kimlik ARANIR, cikarilmaz: `o.kimlik[:8] in metin`. Metinden 8 haneli
    onaltilik desen CEKMEK yanlis olurdu - git commit hash'leri de o desene
    uyar ve alakasiz oturumlari "islenmis" gosterirdi. Bu hata Nar Ajans
    derleyicisinde yapildi ve Codex yakaladi (claude 3557db3e · 16.09 10:22).
    Imza eskiden `-> set` yaziyordu ama metin donduruyordu; yanilticiydi."""
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
def gunluk(bugun: datetime, kuru: bool, oto: list[str] | None = None) -> int:
    dun = bugun - timedelta(days=1)
    # Dedektor SADECE bu projeyi izler. Nar Ajans'in ARTIK kendi derleyicisi
    # var (16 Eyl 2026), oradaki oturumlari o sayar. Diger projelerde yapi yok;
    # onlari "islenmemis" diye listelemek her gece onlarca satir gurultu uretir
    # ve rapor coplugee doner. Yapi baska projeye tasindiginda orada kendi
    # derleyicisi calisir. Diger projeler burada sadece tek satir sayidir.
    proje = kayit.oturumlar("proje")
    taze = [o for o in proje if o.an >= dun]
    diger = [o for o in kayit.oturumlar("claude") if o.an >= dun and o not in taze]

    # Kapanmis = arsivde `kapanan-oturum: <id>` satiri var. Eskiden "kimlik bir
    # notta geciyor mu" diye bakiliyordu; oturum icinde yazilan tek bir kaynak
    # isaretcisi acik oturumu "islenmis" gosteriyordu (claude 5c600e7e · 19.09
    # 08:27). Ayrica sadece son 24 saate bakiliyordu: kapanmadan 24 saat sessiz
    # kalan oturum bir daha hic raporlanmiyordu. Artik zaman siniri yok.
    kapali = kayit.kapanmis_kimlikler()
    islenmemis = [o for o in proje if o.kisa not in kapali]

    s = [f"# Gunluk derleme - {bugun:%d.%m.%Y}", "",
         f"Bu projede son 24 saatte yazilan oturum kaydi: **{len(taze)}**",
         f"Diger projelerde: {len(diger)} oturum (kendi derleyicisi olanlar dahil, "
         f"dedektor kapsam disi)", ""]

    if islenmemis:
        s += ["## KAPANMAMIS OTURUMLAR", "",
              "Arsivde `kapanan-oturum:` satiri yok - kapanis rituelinden gecmemis.",
              "Son 6 saatte yazilan muhtemelen hala acik; eskiler kapanissiz kalmis.", ""]
        for o in islenmemis:
            acik = " | muhtemelen hala acik" if bugun - o.an < timedelta(hours=6) else ""
            s.append(f"- `{o.kisa}` | {o.kaynak} | son yazma {o.an:%d.%m %H:%M} "
                     f"| {o.boyut / 1024:.0f} KB{acik}")
            s.append(f"  - oku: `python araclar/omurga.py {o.kisa}`")
        s.append("")
    else:
        s += ["## Kapanmamis oturum yok", "",
              "Bu projenin her oturumu arsivde `kapanan-oturum:` satiriyla kapanmis.", ""]

    if oto:
        s += ["## Gece kaydi (taslak)", "",
              "Kapanissiz ve 6 saattir sessiz oturumlara temiz baglamla yazdirilan",
              "taslaklar (`oturumlar/oto-*.md`). Kalici notlara terfi EDILMEDI.", ""]
        s += oto + [""]

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

    metinler = islenmis_metin()
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


# --- saglik: derleyici kendi kesintisini bildirir ---------------------------

DURUM = DERLEME / "son-calisma.json"


def onceki_calisma() -> str | None:
    """Onceki calisma tamamlandi mi? Tamamlanmadiysa sebebini dondur.

    Neden: 18.09 00:30'da gorev cikis kodu 0xC000013A (kontrol kesmesi) ile
    bitti, ama gunluk dosya yazilmis ve commit atilmisti. Gorev "Ready"
    gorunuyordu. Yani denetim mekanizmasinin kendisi sessizce bozulabiliyor -
    ve boyle bir mekanizmanin denetledigi seyler hakkinda soyledikleri de
    guvenilmez olur.
    """
    if not DURUM.exists():
        return None
    try:
        d = json.loads(DURUM.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return "son-calisma.json okunamadi ya da bozuk"
    if not d.get("tamamlandi"):
        return f"onceki calisma ({d.get('baslangic', '?')}) TAMAMLANMADAN kesildi"
    return None


def durum_yaz(bugun: datetime, tamamlandi: bool, kuru: bool, **ek) -> None:
    if kuru:
        return
    DURUM.parent.mkdir(parents=True, exist_ok=True)
    DURUM.write_text(
        json.dumps({"baslangic": f"{bugun:%Y-%m-%d %H:%M}",
                    "tamamlandi": tamamlandi, **ek},
                   ensure_ascii=False, indent=1),
        encoding="utf-8")


# --- telafi: "bugun hangi gun" degil, "eksik olan var mi" -------------------

def haftalik_gerekli(bugun: datetime) -> bool:
    """Bu hafta icinde haftalik uretilmis mi?

    Eski kosul "bugun pazartesi mi" idi ve bir acik biraktir: makine pazartesi
    gecesi kapaliysa gorev sali gunu telafi olarak calisir (StartWhenAvailable),
    ama icerde "bugun pazartesi degil" diye haftaligi ATLAR. Sessizce.
    Dogru soru gune degil, eksige bakar.
    """
    hafta_basi = (bugun - timedelta(days=bugun.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0)
    for p in (DERLEME / "haftalik").glob("*.md"):
        try:
            if datetime.strptime(p.stem, "%Y-%m-%d") >= hafta_basi:
                return False
        except ValueError:
            continue
    return True


def aylik_gerekli(bugun: datetime) -> bool:
    return not (DERLEME / "aylik" / f"{bugun:%Y-%m}.md").exists()


# --- denetim: kaynak isaretcileri -------------------------------------------

# Saglayici adi claude ya da codex: beyin tek saglayiciya bagli degil (19.09).
ISARETCI = re.compile(r"\((?:claude|codex) ([0-9a-f]{8})([^)]*)\)", re.S)
# Gun.ay, istege bagli saat. Tek isaretcide birden fazla damga olabilir:
# "(claude 3557db3e - 16.09 10:20 ve 17.09 01:55)" gibi. Saatsiz olan da
# gecerlidir; o zaman sadece "o gun o oturumda mesaj var mi" sorulur.
DAMGA = re.compile(r"(\d{1,2})\.(\d{2})(?:\s+(\d{1,2}):(\d{2}))?")
DAMGA_TOLERANS = 3  # dakika


def isaretci_denetle(dosyalar: list[Path] | None = None) -> tuple[int, list[str], list[str]]:
    """Notlardaki kaynak isaretcilerini ham kayda karsi dogrular.

    ICERIGI denetlemez - sadece "bu adres var mi" der: oturum kaydi gercek mi,
    o damgada bir mesaj var mi. Uydurulmus bir isaretci hatanin en tehlikeli
    turudur, cunku denetlenebilirlik GORUNUSU verir ve o yuzden kimse acip
    bakmaz. Bu ayak model gerektirmez, yargi gerektirmez: deterministiktir.

    UC kategori dondurur, ve ucuncusu onemli: deseni tutmayan bir isaretci
    SESSIZCE ATLANMAMALI. 18.09'da ilk surum tam da bunu yapiyordu - 40
    isaretcinin 32'sini denetleyip 8'ini gormezden geliyordu.
    """
    kusurlu: list[str] = []
    denetlenemeyen: list[str] = []
    toplam = 0
    onbellek: dict[str, list | None] = {}
    # Gece yazicisinin taslaklari da denetlenir: gozetimsiz yazilan metin
    # uydurma damga uretebilir ve onu once bu ayak yakalar (19.09).
    if dosyalar is None:
        dosyalar = (sorted((KOK / "notlar").glob("*.md"))
                    + sorted((KOK / "oturumlar").glob("oto-*.md")))
    for p in dosyalar:
        try:
            metin = p.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in ISARETCI.finditer(metin):
            toplam += 1
            kimlik, govde = m.group(1), m.group(2)
            damgalar = DAMGA.findall(govde)
            if not damgalar:
                denetlenemeyen.append(
                    f"{p.name}: {kimlik} - damga okunamadi ({govde.strip()[:40]})")
                continue
            if kimlik not in onbellek:
                o = kayit.oturum_bul(kimlik)
                onbellek[kimlik] = list(kayit.mesajlar(o)) if o else None
            mesajlar = onbellek[kimlik]
            if mesajlar is None:
                kusurlu.append(f"{p.name}: {kimlik} - oturum kaydi bulunamadi")
                continue
            for gun, ay, saat, dakika in damgalar:
                ayni_gun = [x for x in mesajlar
                            if (x.an.day, x.an.month) == (int(gun), int(ay))]
                if not ayni_gun:
                    kusurlu.append(
                        f"{p.name}: {kimlik} {gun}.{ay} - o gun mesaj yok")
                    continue
                if not saat:
                    continue  # saatsiz isaretci: gun eslesmesi yeterli
                hedef = int(saat) * 60 + int(dakika)
                if not any(abs(x.an.hour * 60 + x.an.minute - hedef)
                           <= DAMGA_TOLERANS for x in ayni_gun):
                    kusurlu.append(
                        f"{p.name}: {kimlik} {gun}.{ay} {saat}:{dakika}"
                        " - o damgada mesaj yok")
    return toplam, kusurlu, denetlenemeyen


def main() -> int:
    kayit.utf8_zorla()
    ap = argparse.ArgumentParser(description="Aksam derleyicisi")
    ap.add_argument("--hepsi", action="store_true", help="uc raporu da zorla")
    ap.add_argument("--kuru", action="store_true", help="yazma, ekrana bas")
    a = ap.parse_args()

    bugun = datetime.now()
    print(f"# Derleme - {bugun:%d.%m.%Y %H:%M}")

    kesinti = onceki_calisma()
    if kesinti:
        print(f"  !! SAGLIK: {kesinti}")
    durum_yaz(bugun, False, a.kuru)

    # Gece kaydi: kapanissiz oturumlara taslak. Dedektorden ONCE calisir ki
    # sonucu ayni rapora girsin. Basarisizligi derlemeyi bozmaz.
    try:
        import gece_kayit
        oto = gece_kayit.calistir(a.kuru)
    except Exception as e:  # noqa: BLE001 - ag bozulursa derleme surmeli
        oto = [f"- GECE KAYDI CALISMADI: {type(e).__name__}: {e}"]
    for satir in oto:
        print(f"  oto: {satir[2:]}")

    eksik = gunluk(bugun, a.kuru, oto)
    if a.hepsi or haftalik_gerekli(bugun):
        haftalik(bugun, a.kuru)
    if a.hepsi or aylik_gerekli(bugun):
        aylik(bugun, a.kuru)

    toplam_i, kusurlu, denetlenemeyen = isaretci_denetle()
    if kusurlu or denetlenemeyen:
        print(f"  !! ISARETCI: {toplam_i} isaretci - "
              f"{len(kusurlu)} kusurlu, {len(denetlenemeyen)} denetlenemedi")
        for k in (kusurlu + denetlenemeyen)[:12]:
            print(f"     - {k}")
        artan = len(kusurlu) + len(denetlenemeyen) - 12
        if artan > 0:
            print(f"     ... ve {artan} tane daha")
    else:
        print(f"  isaretci: {toplam_i} isaretcinin hepsi dogrulandi")

    push = "kuru calisma"
    if not a.kuru:
        git("add", "-A")
        durum = git("status", "--porcelain")
        if durum:
            git("-c", "core.quotepath=false", "commit", "-q", "-m",
                f"Derleme {bugun:%Y-%m-%d}")
            print(f"  git: commit atildi ({len(durum.splitlines())} dosya)")
        else:
            print("  git: degisiklik yok")

        # Dis yedek: private GitHub deposuna gonder. Basarisizlik derlemeyi
        # bozmamali - internet yoksa ya da kimlik dusmusse yerel commit yine
        # duruyor, sonraki gece gonderilir.
        if git("remote"):
            onceki = git("rev-parse", "@{u}") or ""
            git("push", "-q", "origin", "HEAD")
            simdi_u = git("rev-parse", "@{u}") or ""
            yerel = git("rev-parse", "HEAD") or ""
            if simdi_u == yerel:
                push = "tamam" if simdi_u != onceki else "uzak guncel"
                print(f"  git: push {push}")
            else:
                push = "BASARISIZ"
                print("  git: PUSH BASARISIZ - dis yedek guncel degil")
        else:
            push = "uzak depo yok"

    # Sessiz basari yasak: ne bulundugunu sayiyla soyle.
    print(f"# Islenmemis oturum: {eksik}")
    durum_yaz(bugun, True, a.kuru,
              islenmemis_oturum=eksik,
              push=push,
              oto_kayit=oto,
              isaretci_toplam=toplam_i,
              isaretci_kusurlu=kusurlu,
              isaretci_denetlenemeyen=denetlenemeyen,
              onceki_kesinti=kesinti)
    print("# Derleme tamamlandi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
