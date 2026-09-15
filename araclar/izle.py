#!/usr/bin/env python3
"""
izle.py - video araliklarini bir yapay zeka modelinin okuyabilecegi hale cevirir.

  1) TARAMA   : python araclar/izle.py <kaynak> --basla 0:00 --bitir 16:39
                -> sadece ses cekilir, zaman damgali transkript uretilir. Kare yok.
  2) YAKIN BAK: python araclar/izle.py <kaynak> --basla 4:00 --bitir 6:00 --kare
                -> o dar araligin videosu alinir, kareler cikarilir.
  3) KONTROL   : python araclar/izle.py --kontrol
                -> ortami sinar, neyin eksik oldugunu soyler.

<kaynak>: yerel dosya yolu VEYA YouTube linki.
Ayarlar (ortam degiskeni): IZLE_MODEL, IZLE_MODEL_DIZIN, IZLE_CUDA_LIB
"""
import argparse, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

KOK         = Path(__file__).parent
MODEL_ADI   = os.environ.get("IZLE_MODEL", "large-v3")
MODEL_DIZIN = os.environ.get("IZLE_MODEL_DIZIN", "D:/AI/whisper")
CUDA_LIB    = os.environ.get("IZLE_CUDA_LIB", "D:/AI/pylibs/nvidia")
# Bu esigin ustundeki YouTube videolarinda tamamini indirmek yerine kirp (saniye).
YT_KIRPMA_ESIGI = float(os.environ.get("IZLE_KIRPMA_ESIGI", "3600"))
FALLBACK    = Path(os.environ.get("LOCALAPPDATA", "")) / (
    "Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    "/ffmpeg-9.0.1-full_build/bin")


def bul(n):
    return shutil.which(n) or str(FALLBACK / (n + ".exe"))


FFMPEG, FFPROBE = bul("ffmpeg"), bul("ffprobe")


def cuda_dll():
    """cuBLAS/cuDNN D diskinde duruyor; Windows'a nerede arayacagini soyler."""
    kok, n = Path(CUDA_LIB), 0
    if kok.exists():
        for b in kok.glob("*/bin"):
            try:
                os.add_dll_directory(str(b))
                n += 1
            except OSError:
                pass
    return n


def saniye(s):
    if s is None:
        return None
    p = [float(x) for x in str(s).split(":")]
    while len(p) < 3:
        p.insert(0, 0.0)
    return p[0] * 3600 + p[1] * 60 + p[2]


def mmss(t):
    t = int(t)
    return "%02d:%02d" % (t // 60, t % 60)


def kos(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


def sure(v):
    r = kos([FFPROBE, "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(v)])
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


# --- kaynak hazirlama -------------------------------------------------------

def hazirla(kaynak, bas, bit, kok, sadece_ses):
    """Istenen araligi indirir/keser. sadece_ses=True ise video akisi hic cekilmez."""
    hedef = kok / ("ses.m4a" if sadece_ses else "kesit.mp4")
    if hedef.exists():
        return hedef

    if str(kaynak).startswith("http"):
        bicim = (["-f", "ba/b"] if sadece_ses else
                 ["-f", "bv*[height<=1080]+ba/b", "--merge-output-format", "mp4"])
        temel = ["yt-dlp", "--ffmpeg-location", str(Path(FFMPEG).parent)]

        # Olculen davranis (bkz. KURULUM notlari):
        #   tam indirme  -> sure ile dogru orantili buyur, ama tam hizda iner
        #   kirpma       -> sabit maliyet (~1 sn video icin ~0.5 sn), kaynaktan bagimsiz
        # Kisa videoda tam indirme hizli; uzun videoda kirpma sart.
        # NOT: --force-keyframes-at-cuts 403 Forbidden veriyor, kullanma.
        d = 0.0
        r = kos(temel + ["--print", "duration", "--skip-download", kaynak])
        try:
            d = float(r.stdout.strip().splitlines()[0])
        except (ValueError, IndexError):
            pass

        kirp = (bas is not None and not sadece_ses and d > YT_KIRPMA_ESIGI)
        if kirp:
            son = mmss(bit) if bit is not None else "inf"
            print("(kaynak %.0f dk -> araliksal indirme)" % (d / 60), flush=True)
            r = kos(temel + bicim + ["--download-sections", "*" + mmss(bas) + "-" + son,
                                     "-o", str(hedef), kaynak])
            if not hedef.exists():
                sys.exit("yt-dlp (araliksal) basarisiz:\n" + r.stderr[-1500:])
            return hedef

        tam = kok / ("tam.m4a" if sadece_ses else "tam.mp4")
        if not tam.exists():
            r = kos(temel + bicim + ["-o", str(tam), kaynak])
            if not tam.exists():
                sys.exit("yt-dlp basarisiz:\n" + r.stderr[-1500:])
        if bas is None and bit is None:
            return tam
        kaynak = tam  # asagidaki yerel kesme yoluna dus

    if bas is None and bit is None and not sadece_ses:
        return Path(kaynak)

    cmd = [FFMPEG, "-y", "-loglevel", "error"]
    if bas is not None:
        cmd += ["-ss", str(bas)]
    if bit is not None:
        cmd += ["-to", str(bit)]
    cmd += ["-i", str(kaynak)]
    cmd += ["-vn", "-c:a", "aac"] if sadece_ses else ["-c", "copy"]
    cmd += [str(hedef)]
    r = kos(cmd)
    if not hedef.exists():
        sys.exit("ffmpeg kesme basarisiz:\n" + r.stderr[-800:])
    return hedef


# --- 1. asama: konusma ------------------------------------------------------

def _coz(m, ses, sz, ofset):
    """Generator burada gercekten calisir - hatalar bu satirda yuzeye cikar."""
    segs, _ = m.transcribe(str(ses), language="tr", vad_filter=True,
                           initial_prompt=sz or None)
    return ["[" + mmss(ofset + g.start) + "] " + g.text.strip() for g in segs]


def transkript(kaynak_dosya, kok, ofset):
    hedef = kok / "transkript.txt"
    if hedef.exists():
        print("(transkript onbellekten okundu)")
        return hedef.read_text(encoding="utf-8").splitlines()

    import ctranslate2
    from faster_whisper import WhisperModel
    bulunan = cuda_dll()
    gpu = ctranslate2.get_cuda_device_count() > 0

    ses = kok / "ses.wav"
    kos([FFMPEG, "-y", "-loglevel", "error", "-i", str(kaynak_dosya),
         "-vn", "-ac", "1", "-ar", "16000", str(ses)])

    sz = ""
    sp = KOK / "sozluk.txt"
    if sp.exists():
        sz = sp.read_text(encoding="utf-8").strip()

    satirlar = None
    if gpu:
        print("[whisper %s / cuda] cozumleniyor (dll klasoru: %d)..."
              % (MODEL_ADI, bulunan), flush=True)
        try:
            m = WhisperModel(MODEL_ADI, device="cuda", compute_type="float16",
                             download_root=MODEL_DIZIN)
            satirlar = _coz(m, ses, sz, ofset)
        except Exception as e:
            print("!! GPU CALISMADI -> %s: %s" % (type(e).__name__, str(e)[:160]))
            print("!! CPU'ya dusuluyor (daha yavas).", flush=True)

    if satirlar is None:
        print("[whisper %s / cpu] cozumleniyor..." % MODEL_ADI, flush=True)
        m = WhisperModel(MODEL_ADI, device="cpu", compute_type="int8",
                         download_root=MODEL_DIZIN)
        satirlar = _coz(m, ses, sz, ofset)

    ses.unlink(missing_ok=True)
    hedef.write_text("\n".join(satirlar), encoding="utf-8")
    return satirlar


# --- 2. asama: kareler ------------------------------------------------------

def kareler(video, klasor, ofset, max_kare, sahne_esik=None):
    """Varsayilan: araliga esit araliklarla max_kare adet kare.

    Ekran kayitlarinda sahne algilama calismaz (ekran yavas degisir),
    o yuzden varsayilan esit aralikli ornekleme.
    """
    klasor.mkdir(parents=True, exist_ok=True)
    if sahne_esik is not None:
        r = kos([FFMPEG, "-y", "-loglevel", "info", "-i", str(video),
                 "-vf", "select='gt(scene,%s)',showinfo" % sahne_esik,
                 "-fps_mode", "vfr", "-qscale:v", "3", str(klasor / "%05d.jpg")])
        zamanlar = [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    else:
        d = sure(video)
        adim = max(1.0, d / max_kare) if d else 3.0
        kos([FFMPEG, "-y", "-loglevel", "error", "-i", str(video),
             "-vf", "fps=1/%.4f" % adim, "-fps_mode", "vfr",
             "-qscale:v", "3", str(klasor / "%05d.jpg")])
        zamanlar = None

    ham = sorted(klasor.glob("[0-9]*.jpg"))
    if zamanlar is None:
        d = sure(video)
        adim = max(1.0, d / max_kare) if d else 3.0
        zamanlar = [i * adim for i in range(len(ham))]

    out = []
    for i, h in enumerate(ham):
        t = ofset + (zamanlar[i] if i < len(zamanlar) else 0)
        yeni = klasor / ("%03d_t%ss.jpg" % (i + 1, mmss(t).replace(":", "m")))
        h.rename(yeni)
        out.append((t, yeni))
    return out


# --- ortam kontrolu ---------------------------------------------------------

def kontrol():
    """Skoru soyler: ne var, ne yok, nerede duruyoruz."""
    print("=== izle.py ortam kontrolu ===")
    for ad in ("ffmpeg", "ffprobe"):
        y = bul(ad)
        print("%-10s %s" % (ad, y if Path(y).exists() or shutil.which(ad) else "YOK"))
    print("%-10s %s" % ("yt-dlp", shutil.which("yt-dlp") or "YOK (YouTube calismaz)"))
    try:
        import ctranslate2
        n = ctranslate2.get_cuda_device_count()
        print("%-10s ctranslate2 %s, cuda cihaz: %d"
              % ("whisper", ctranslate2.__version__, n))
        print("%-10s %d klasor kayitli (%s)" % ("cuda dll", cuda_dll(), CUDA_LIB))
    except ImportError:
        print("%-10s YOK -> pip install faster-whisper" % "whisper")
    md = Path(MODEL_DIZIN)
    print("%-10s %s %s" % ("model", MODEL_ADI,
                           "-> " + str(md) if md.exists() else "(indirilmemis)"))
    print("%-10s %s" % ("sozluk", "var" if (KOK / "sozluk.txt").exists() else "YOK"))


# --- ana akis ---------------------------------------------------------------

def main():
    a = argparse.ArgumentParser()
    a.add_argument("kaynak", nargs="?")
    a.add_argument("--basla")
    a.add_argument("--bitir")
    a.add_argument("--kare", action="store_true", help="2. asama: kare de cikar")
    a.add_argument("--max-kare", type=int, default=24, dest="max_kare")
    a.add_argument("--sahne", type=float, default=None)
    a.add_argument("--sessiz", action="store_true", help="transkript uretme")
    a.add_argument("--kontrol", action="store_true", help="ortami sina ve cik")
    a.add_argument("--cikti", default=None)
    n = a.parse_args()

    if n.kontrol:
        kontrol()
        return
    if not n.kaynak:
        sys.exit("kaynak gerekli (dosya yolu veya YouTube linki)")
    # Yerel kaynagi en basta dogrula: yoksa ffmpeg'e kadar tasimaya gerek yok.
    if not str(n.kaynak).startswith("http") and not Path(n.kaynak).exists():
        sys.exit("KAYNAK BULUNAMADI: " + str(n.kaynak))

    bas, bit = saniye(n.basla), saniye(n.bitir)
    ofset = bas or 0.0
    kok = Path(n.cikti) if n.cikti else Path(tempfile.mkdtemp(prefix="izle_"))
    kok.mkdir(parents=True, exist_ok=True)
    print("KLASOR: " + str(kok))

    dosya = hazirla(n.kaynak, bas, bit, kok, sadece_ses=not n.kare)

    if not n.sessiz:
        satirlar = transkript(dosya, kok, ofset)
        print("TRANSKRIPT: %s (%d satir)" % (kok / "transkript.txt", len(satirlar)))

    if n.kare:
        kl = kareler(dosya, kok / "kareler", ofset, n.max_kare, n.sahne)
        aralik = (bit - bas) if (bas is not None and bit is not None) else sure(dosya)
        print("KARE SAYISI: %d  (aralik %.1f dk -> %.0f sn'de bir kare)"
              % (len(kl), aralik / 60, aralik / max(len(kl), 1)))
        for t, p in kl:
            print("  [%s] %s" % (mmss(t), p.name))
        if aralik > 300:
            print("!! UYARI: aralik genis, kareler seyrek."
                  " Ekran metni okumak icin 2-3 dakikalik aralik ver.")
    else:
        print("SONRAKI ADIM: ilgili zamani secip --kare ile dar aralik iste.")


if __name__ == "__main__":
    main()
