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
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
from urllib.parse import urlparse

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


def youtube_url(kaynak):
    """Only YouTube URLs are supported for network sources."""
    p = urlparse(str(kaynak))
    host = (p.hostname or "").lower()
    return p.scheme in ("http", "https") and (
        host == "youtu.be" or host == "youtube.com" or host.endswith(".youtube.com")
    )


def cikti_klasoru(kaynak, bas, bit, n):
    """Use one empty output folder per run; never trust old cached media/results."""
    if not n.cikti:
        kok = Path(tempfile.mkdtemp(prefix="izle_"))
    else:
        kok = Path(n.cikti).expanduser().resolve()
        vault = Path(__file__).resolve().parents[4]
        if kok == vault or vault in kok.parents:
            raise ValueError("Cikti klasoru Ikinci Beyin vault'u disinda olmali")
        if kok.exists():
            if not kok.is_dir() or any(kok.iterdir()):
                raise ValueError("--cikti bos bir klasor olmali; onbellek yeniden kullanilmaz")
        else:
            kok.mkdir(parents=True)
    kimlik = {
        "kaynak": str(kaynak), "basla_saniye": bas, "bitir_saniye": bit,
        "kare": n.kare, "kare_sn": n.kare_sn, "max_kare": n.max_kare,
        "ocr": n.ocr, "altyazi": n.altyazi, "sessiz": n.sessiz,
        "model": MODEL_ADI,
    }
    (kok / "izle-manifest.json").write_text(
        json.dumps(kimlik, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return kok


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

    if youtube_url(kaynak):
        bicim = (["-f", "ba/b"] if sadece_ses else
                 ["-f", "bv*[height<=1080]+ba/b", "--merge-output-format", "mp4"])
        temel = ["yt-dlp", "--ignore-config", "--no-playlist",
                 "--ffmpeg-location", str(Path(FFMPEG).parent)]

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
            if r.returncode != 0 or not hedef.is_file() or hedef.stat().st_size == 0:
                sys.exit("yt-dlp (araliksal) basarisiz:\n" + r.stderr[-1500:])
            return hedef

        tam = kok / ("tam.m4a" if sadece_ses else "tam.mp4")
        if not tam.exists():
            r = kos(temel + bicim + ["-o", str(tam), kaynak])
            if r.returncode != 0 or not tam.is_file() or tam.stat().st_size == 0:
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
    if r.returncode != 0 or not hedef.is_file() or hedef.stat().st_size == 0:
        sys.exit("ffmpeg kesme basarisiz:\n" + r.stderr[-800:])
    return hedef


# --- 1. asama: konusma ------------------------------------------------------

def _coz(m, ses, sz, ofset):
    """Generator burada gercekten calisir - hatalar bu satirda yuzeye cikar."""
    segs, _ = m.transcribe(str(ses), language="tr", vad_filter=True,
                           initial_prompt=sz or None)
    return ["[" + mmss(ofset + g.start) + "] " + g.text.strip() for g in segs]


def transkript(kaynak_dosya, kok, ofset, terimler=""):
    hedef = kok / "transkript.txt"
    if hedef.exists():
        print("(transkript onbellekten okundu)")
        return hedef.read_text(encoding="utf-8").splitlines()

    import ctranslate2
    from faster_whisper import WhisperModel
    bulunan = cuda_dll()
    gpu = ctranslate2.get_cuda_device_count() > 0

    ses = kok / "ses.wav"
    r = kos([FFMPEG, "-y", "-loglevel", "error", "-i", str(kaynak_dosya),
             "-vn", "-ac", "1", "-ar", "16000", str(ses)])
    if r.returncode != 0 or not ses.is_file() or ses.stat().st_size == 0:
        raise RuntimeError("ffmpeg ses donusumu basarisiz: " + r.stderr[-800:])

    # No prompt or vocabulary is imported from the legacy system. Optional
    # user-supplied terms are passed only for this invocation.
    sz = terimler.strip()

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

def kareler(video, klasor, ofset, max_kare, sahne_esik=None, kare_sn=None):
    """Kare cikarir. Iki ayri birim:

      max_kare : SAYI sabit  -> aralik uzadikca kareler seyreler (eski davranis)
      kare_sn  : SIKLIK sabit -> kare sayisi aralikla buyur (dogru birim)

    kare_sn verilirse max_kare yok sayilir.
    Sahne algilama (--sahne) ekran kayitlarinda calismaz; mpdecimate ise
    animasyonlu videolarda calismaz (17.09 olcumu). Eleme icin dhash kullan.
    """
    klasor.mkdir(parents=True, exist_ok=True)
    if sahne_esik is not None:
        r = kos([FFMPEG, "-y", "-loglevel", "info", "-i", str(video),
                 "-vf", "select='gt(scene,%s)',showinfo" % sahne_esik,
                 "-fps_mode", "vfr", "-qscale:v", "3", str(klasor / "%05d.jpg")])
        if r.returncode != 0:
            raise RuntimeError("ffmpeg sahne cikarimi basarisiz: " + r.stderr[-800:])
        zamanlar = [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    else:
        d = sure(video)
        adim = float(kare_sn) if kare_sn else (max(1.0, d / max_kare) if d else 3.0)
        r = kos([FFMPEG, "-y", "-loglevel", "error", "-i", str(video),
                 "-vf", "fps=1/%.4f" % adim, "-fps_mode", "vfr",
                 "-qscale:v", "3", str(klasor / "%05d.jpg")])
        if r.returncode != 0:
            raise RuntimeError("ffmpeg kare cikarimi basarisiz: " + r.stderr[-800:])
        zamanlar = None

    ham = sorted(klasor.glob("[0-9]*.jpg"))
    if not ham:
        raise RuntimeError("Video araligindan hic kare cikarilamadi")
    if zamanlar is None:
        d = sure(video)
        adim = float(kare_sn) if kare_sn else (max(1.0, d / max_kare) if d else 3.0)
        zamanlar = [i * adim for i in range(len(ham))]

    out = []
    for i, h in enumerate(ham):
        t = ofset + (zamanlar[i] if i < len(zamanlar) else 0)
        yeni = klasor / ("%03d_t%ss.jpg" % (i + 1, mmss(t).replace(":", "m")))
        h.rename(yeni)
        out.append((t, yeni))
    return out


# --- 2b. eleme: algisal hash ------------------------------------------------

def dhash(yol, s=16):
    """Komsu piksel karsilastirmasi -> s*s bitlik parmak izi.

    Gorsel benzerligi olcer, BILGISEL benzerligi degil. Konusan kafada
    'farkli' der ama bilgi aynidir; slaytta tek kelime degisirse 'ayni' der.
    Bu yuzden OCR varsa son soz onundur.
    """
    from PIL import Image
    im = Image.open(yol).convert("L").resize((s + 1, s))
    px = list(im.getdata())
    bits = 0
    for r in range(s):
        for c in range(s):
            if px[r * (s + 1) + c] < px[r * (s + 1) + c + 1]:
                bits |= 1 << (r * s + c)
    return bits


def ele_benzer(kare_listesi, esik):
    """Kendinden onceki SECILMIS karelerin hepsine uzaksa tut."""
    if esik <= 0 or not kare_listesi:
        return kare_listesi, []
    tutulan, hashler, atilan = [], [], []
    for t, p in kare_listesi:
        h = dhash(p)
        if not hashler or min(bin(h ^ o).count("1") for o in hashler) > esik:
            tutulan.append((t, p))
            hashler.append(h)
        else:
            atilan.append((t, p))
    return tutulan, atilan


# --- 3. asama: karedeki yazi ------------------------------------------------

TESSERACT = shutil.which("tesseract") or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA  = os.environ.get("IZLE_TESSDATA", "D:/AI/tessdata")


def ocr_kare(yol, dil="tur", psm="6"):
    """Karedeki yaziyi metne cevirir. Gurultu ayiklanir: sus sekillerinden
    gelen 1-2 karakterlik anlamsiz parcalar atilir."""
    ortam = dict(os.environ, TESSDATA_PREFIX=TESSDATA)
    r = subprocess.run([TESSERACT, str(yol), "-", "-l", dil, "--psm", psm],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam)
    if r.returncode != 0:
        raise RuntimeError("Tesseract OCR basarisiz: " + r.stderr[-800:])
    temiz = []
    for parca in r.stdout.split():
        if len(parca) >= 3 or parca.isdigit() or parca in ("mi", "mı", "ve", "bu"):
            temiz.append(parca)
    return " ".join(temiz).strip()


def yazi_degisti(a, b, oran=0.80):
    """Iki kare metni ayni bilgiyi mi tasiyor? Jaccard benzerligi."""
    ka, kb = set(a.lower().split()), set(b.lower().split())
    if not ka and not kb:
        return False
    ortak = len(ka & kb)
    toplam = len(ka | kb)
    return (ortak / toplam if toplam else 0) < oran


# --- 1b. ikinci tanik: YouTube altyazisi ------------------------------------

def altyazi_cek(url, kok, bas=None, bit=None):
    """YouTube'daki hazir altyaziyi ceker. IKI TUR VAR ve ayrimi onemli:

      'subtitles'         -> kanalin kendi yukledigi (Avenox'ta bu da bir AI
                             transkripsiyon aracinin ciktisi, elle yazilmamis;
                             ama kaynak ses HAM kayit, YouTube'un sikistirmasi
                             degil - bu yuzden Whisper'dan bagimsiz bir taniktir)
      'automatic_captions'-> YouTube'un kendi konusma tanimasi

    Ikisi de tahmindir. Hakem yoktur, iki tanik vardir: uyustuklari yer guclu,
    ayristiklari yer suphelidir.
    """
    if not youtube_url(url):
        return None, None
    onek = str(kok / "ay")
    for bayrak, tur in (("--write-subs", "kanal"), ("--write-auto-subs", "otomatik")):
        for p in kok.glob("ay*.srt"):
            p.unlink(missing_ok=True)
        kos(["yt-dlp", "--ignore-config", "--no-playlist", "--skip-download",
             bayrak, "--sub-langs", "tr",
             "--convert-subs", "srt", "-o", onek, url])
        bulunan = list(kok.glob("ay*.srt"))
        if bulunan:
            satirlar = srt_oku(bulunan[0], bas, bit)
            if satirlar:
                return satirlar, tur
    return None, None


def srt_oku(yol, bas=None, bit=None):
    """SRT'yi [mm:ss] metin satirlarina cevirir, istenen araliga kirpar."""
    ham = yol.read_text(encoding="utf-8", errors="replace")
    out = []
    for blok in re.split(r"\n\s*\n", ham):
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->", blok)
        if not m:
            continue
        t = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        if bas is not None and t < bas:
            continue
        if bit is not None and t > bit:
            continue
        metin = " ".join(s.strip() for s in blok.splitlines()[2:] if s.strip())
        metin = re.sub(r"<[^>]+>", "", metin).strip()
        if metin:
            out.append("[" + mmss(t) + "] " + metin)
    return out


# --- 4. asama: birlestirme --------------------------------------------------

def _damgali(satirlar):
    """[mm:ss] metin -> (saniye, metin) listesi."""
    out = []
    for s in satirlar or []:
        m = re.match(r"\[(\d+):(\d+)\]\s*(.*)", s)
        if m:
            out.append((int(m.group(1)) * 60 + int(m.group(2)), m.group(3).strip()))
    return out


_NOKTALAMA = str.maketrans("", "", ".,;:!?\"'()[]{}…“”‘’–—")


def _kelimeler(metin):
    return {k for k in metin.lower().translate(_NOKTALAMA).split() if len(k) >= 3}


def birlestir(kok, transkript_satir, altyazi_satir, kare_yazi_satir, kova=20):
    """Uc kaynagi tek zaman cizelgesinde toplar ve AYRISMAYI isaretler.

    Iki konusma kaynagi da tahmindir; hakem yoktur. Bu yuzden birlestirme
    'dogruyu sec' degil, 'nerede ayrisiyorlar' sorusunu cevaplar. Ayrisan
    kelime, ya birinin hatasi ya otekinin duydugu ek bilgidir - ikisi de
    bakmaya degerdir.
    """
    tr = _damgali(transkript_satir)
    ay = _damgali(altyazi_satir)
    kr = _damgali(kare_yazi_satir)
    if not tr and not ay and not kr:
        return None

    hepsi = [t for t, _ in tr + ay + kr]
    bas, son = min(hepsi), max(hepsi)
    out, ayrisma_say = [], 0

    def pencere(L, t0, genislik=1):
        """genislik=1 -> komsu kovalar da dahil. Iki kaynak ayni ani farkli
        damgaliyor (whisper segmentin BASINI damgalar, altyazi her cumleyi),
        bu yuzden kelime karsilastirmasi toleransli pencerede yapilir; yoksa
        hizalama kaymasi gercek ayrisma gibi gorunur."""
        a = t0 - genislik * kova
        b = t0 + (genislik + 1) * kova
        return [m for s, m in L if a <= s < b]

    t = (bas // kova) * kova
    while t <= son:
        dar = lambda L: [m for s, m in L if t <= s < t + kova]
        a, b, c = dar(tr), dar(ay), dar(kr)
        if not (a or b or c):
            t += kova
            continue
        out.append("## [%s]" % mmss(t))
        if a:
            out.append("**ses (whisper):** " + " ".join(a))
        if b:
            out.append("**ses (altyazi):** " + " ".join(b))
        if a and b:
            # dar pencerede soylenen, GENIS pencerede otekinde var mi?
            ka, kb = _kelimeler(" ".join(a)), _kelimeler(" ".join(b))
            gw = _kelimeler(" ".join(pencere(tr, t)))
            ga = _kelimeler(" ".join(pencere(ay, t)))
            yalniz_w, yalniz_a = sorted(ka - ga), sorted(kb - gw)
            if yalniz_w or yalniz_a:
                ayrisma_say += 1
                out.append("**! ayrisma:** whisper'da `%s` | altyazida `%s`"
                           % (", ".join(yalniz_w) or "-", ", ".join(yalniz_a) or "-"))
        if c:
            out.append("**ekranda:** " + " ".join(c))
        out.append("")
        t += kova

    basl = ["# Birlesik dokum", "",
            "Kaynak: %s%s%s. Iki konusma kaynagi da tahmindir, hakem yoktur;"
            % ("whisper" if tr else "",
               " + altyazi" if ay else "",
               " + ekran yazisi (ocr)" if kr else ""),
            "ayrisan kelimeler isaretlendi (%d pencerede)." % ayrisma_say, ""]
    hedef = kok / "birlesik.md"
    hedef.write_text("\n".join(basl + out), encoding="utf-8")
    return hedef, ayrisma_say


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
    print("%-10s komut satirindan istege bagli" % "terimler")
    try:
        import PIL
        print("%-10s Pillow %s (dhash elemesi calisir)" % ("pillow", PIL.__version__))
    except ImportError:
        print("%-10s YOK -> pip install pillow (dhash elemesi calismaz)" % "pillow")
    if Path(TESSERACT).exists() or shutil.which("tesseract"):
        r = subprocess.run([TESSERACT, "--list-langs"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           env=dict(os.environ, TESSDATA_PREFIX=TESSDATA))
        diller = [x.strip() for x in r.stdout.splitlines()[1:] if x.strip()]
        print("%-10s %s  diller: %s" % ("tesseract", TESSDATA, ", ".join(diller) or "?"))
        if "tur" not in diller:
            print("%-10s !! tur.traineddata yok -> tessdata_best'ten indir" % "")
    else:
        print("%-10s YOK -> winget install UB-Mannheim.TesseractOCR" % "tesseract")


# --- ana akis ---------------------------------------------------------------

def main():
    a = argparse.ArgumentParser()
    a.add_argument("kaynak", nargs="?")
    a.add_argument("--basla")
    a.add_argument("--bitir")
    a.add_argument("--kare", action="store_true", help="2. asama: kare de cikar")
    a.add_argument("--max-kare", type=int, default=24, dest="max_kare",
                   help="SAYI sabit (eski birim): aralik uzadikca kareler seyreler")
    a.add_argument("--kare-sn", type=float, default=None, dest="kare_sn",
                   help="SIKLIK sabit: kac saniyede bir kare (dogru birim)")
    a.add_argument("--benzer", type=int, default=24,
                   help="dhash eleme esigi (0 = eleme yok, 24 onerilen)")
    a.add_argument("--ocr", action="store_true",
                   help="3. asama: karelerdeki yaziyi oku (Tesseract)")
    a.add_argument("--altyazi", action="store_true",
                   help="YouTube'daki hazir altyaziyi da cek (ikinci tanik)")
    a.add_argument("--terimler", default="",
                   help="Bu calistirmaya ozel teknik terimler; eski sozluk kullanilmaz")
    a.add_argument("--kova", type=int, default=20,
                   help="birlesik dokumde zaman penceresi (saniye)")
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
    if str(n.kaynak).startswith(("http://", "https://")):
        if not youtube_url(n.kaynak):
            sys.exit("Yalniz YouTube baglantilari desteklenir")
    elif not Path(n.kaynak).is_file():
        sys.exit("KAYNAK DOSYA BULUNAMADI: " + str(n.kaynak))

    bas, bit = saniye(n.basla), saniye(n.bitir)
    if (bas is not None and bas < 0) or (bit is not None and bit < 0):
        sys.exit("Zaman degerleri negatif olamaz")
    if bas is not None and bit is not None and bit <= bas:
        sys.exit("--bitir --basla degerinden buyuk olmali")
    if n.max_kare < 1 or (n.kare_sn is not None and n.kare_sn <= 0) or n.kova < 1:
        sys.exit("--max-kare ve --kova pozitif; --kare-sn sifirdan buyuk olmali")
    if n.benzer < 0 or (n.sahne is not None and not 0 <= n.sahne <= 1):
        sys.exit("--benzer negatif olamaz; --sahne 0 ile 1 arasinda olmali")
    if n.ocr and not n.kare:
        sys.exit("--ocr icin --kare gerekli")
    if n.altyazi and not youtube_url(n.kaynak):
        sys.exit("--altyazi yalniz YouTube baglantisinda kullanilabilir")
    if n.sessiz and not (n.kare or n.altyazi):
        sys.exit("--sessiz icin --kare veya --altyazi gerekli")
    if len(n.terimler) > 2000:
        sys.exit("--terimler en fazla 2000 karakter olabilir")
    ofset = bas or 0.0
    try:
        kok = cikti_klasoru(n.kaynak, bas, bit, n)
    except ValueError as e:
        sys.exit(str(e))
    print("KLASOR: " + str(kok))

    dosya = hazirla(n.kaynak, bas, bit, kok, sadece_ses=not n.kare)

    ay_satir, tr_satir, kr_satir = [], [], []

    if n.altyazi:
        ay_satir, tur = altyazi_cek(n.kaynak, kok, bas, bit)
        ay_satir = ay_satir or []
        if ay_satir:
            (kok / "altyazi.txt").write_text("\n".join(ay_satir), encoding="utf-8")
            print("ALTYAZI (%s): %s (%d satir)"
                  % (tur, kok / "altyazi.txt", len(ay_satir)))
        else:
            print("ALTYAZI: bulunamadi")

    if not n.sessiz:
        tr_satir = transkript(dosya, kok, ofset, n.terimler)
        print("TRANSKRIPT: %s (%d satir)" % (kok / "transkript.txt", len(tr_satir)))

    if n.kare:
        kl = kareler(dosya, kok / "kareler", ofset, n.max_kare, n.sahne, n.kare_sn)
        aralik = (bit - bas) if (bas is not None and bit is not None) else sure(dosya)
        ham_sayi = len(kl)

        atilan = []
        if n.benzer > 0 and n.sahne is None:
            kl, atilan = ele_benzer(kl, n.benzer)
            for _, p in atilan:
                p.unlink(missing_ok=True)

        yazilar = {}
        if n.ocr:
            print("[ocr] %d kare okunuyor..." % len(kl), flush=True)
            son_metin, ikinci_ele = "", []
            kalan = []
            for t, p in kl:
                m = ocr_kare(p)
                if m and not yazi_degisti(son_metin, m):
                    ikinci_ele.append((t, p))   # ayni yazi: kare tekrar
                    p.unlink(missing_ok=True)
                    continue
                if m:
                    son_metin = m
                yazilar[p.name] = m
                kalan.append((t, p))
            if ikinci_ele:
                print("[ocr] yazisi degismeyen %d kare daha elendi" % len(ikinci_ele))
            kl = kalan
            kr_satir = ["[%s] %s" % (mmss(t), yazilar.get(p.name, ""))
                        for t, p in kl]
            (kok / "kare-yazilari.txt").write_text("\n".join(kr_satir),
                                                   encoding="utf-8")
            print("KARE YAZILARI: %s" % (kok / "kare-yazilari.txt"))

        print("KARE SAYISI: %d  (ham %d -> elendi %d)  aralik %.1f dk -> %.0f sn'de bir"
              % (len(kl), ham_sayi, ham_sayi - len(kl), aralik / 60,
                 aralik / max(len(kl), 1)))
        for t, p in kl:
            ek = ("  | " + yazilar[p.name][:70]) if yazilar.get(p.name) else ""
            print("  [%s] %s%s" % (mmss(t), p.name, ek))
        if aralik > 300 and not n.kare_sn:
            print("!! UYARI: aralik genis, kareler seyrek."
                  " --kare-sn 3 ile sikligi sabitle.")
    else:
        print("SONRAKI ADIM: ilgili zamani secip --kare ile dar aralik iste.")

    # 4. asama: elde birden fazla kaynak varsa tek dokumde birlestir
    kaynak_sayisi = sum(1 for x in (tr_satir, ay_satir, kr_satir) if x)
    if kaynak_sayisi >= 2:
        sonuc = birlestir(kok, tr_satir, ay_satir, kr_satir, n.kova)
        if sonuc:
            yol, ayr = sonuc
            print("BIRLESIK: %s  (%d pencerede ayrisma isaretlendi)" % (yol, ayr))
    elif kaynak_sayisi == 1:
        print("(birlestirme atlandi: tek kaynak var, karsilastiracak tanik yok)")


if __name__ == "__main__":
    main()
