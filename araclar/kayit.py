#!/usr/bin/env python3
"""Oturum kayitlarini okuyan ortak katman.

Claude Code ve Codex CLI konusmalari diske farkli bicimlerde yaziyor.
Bu modul ikisini de tek bir bicime cevirir; omurga.py, ara.py, oku.py ve
anlam.py bunun uzerine oturur. Ayristirma tek yerde dursun diye var.

Bicimler (8 Eylul 2026'da olculdu):

  Claude  ~/.claude/projects/<proje>/<oturum-id>.jsonl
          satir: {"type":"user|assistant","timestamp":...,"message":{...}}
          arac ciktisi da type=user gorunur; ayrimi "toolUseResult" alani yapar

  Codex   ~/.codex/sessions/<yil>/<ay>/<gun>/rollout-<tarih>-<id>.jsonl
          satir: {"type":"response_item","payload":{"type":"message",
                  "role":"user|assistant|developer","content":[...]}}
          role=developer sistem enjeksiyonudur, kullanici degildir

Ilgili: BEYIN.md, CLAUDE.md (kapanis rituelinde omurga.py kullanilir)
"""

import io
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterator, NamedTuple

# Hook'lar, sistem enjeksiyonlari ve kabuk gurultusu. Bunlar kullanicinin
# yazdigi metin degildir; omurgaya ve indekse karismamalari gerekir.
GURULTU_ONEK = (
    "Su anki yerel tarih ve saat:",
    "<system-reminder>",
    "<command-name>",
    "<command-message>",
    "<command-args>",
    "<local-command-stdout>",
    "<local-command-caveat>",
    "<app-context>",
    "<recommended_plugins>",
    "<multi_agent_role>",
    "<multi_agent_mode>",
    "<user_instructions>",
    "<environment_context>",
    "<available_plugins>",
    "<codex_internal_context",
    "Caveat: The messages below were generated",
    # Reply bicimli mesajlarda her parcanin arkasina harness ekliyor; bu
    # oturumun omurgasini 17 sahte mesajla sisiriyordu (claude 5c600e7e · 19.09 17:24).
    "[Request interrupted by user",
)

# Bu isaretlerden birini tasiyan mesaj bastan asagi sistem uretimidir
# (arka plan gorev bildirimi, CI olayi). Satir satir temizlemek yetmez,
# mesajin tamami atilir - yoksa omurgaya kullanici mesaji gibi girer.
TAM_GURULTU = (
    "[SYSTEM NOTIFICATION - NOT USER INPUT]",
    "<task-notification>",
    "<ci-monitor-event>",
)

# Codex, kural dosyasini ve ortam bilgisini role=user mesajinin AYRI BLOKLARI
# olarak yaziyor. Satir satir temizlemek AGENTS.md'nin govdesini birakiyordu;
# blogun tamami atilir. Codex yakaladi, 01a0b9eb omurgasinda olculdu
# (claude 5c600e7e · 19.09 17:20).
ENJEKSIYON_BLOK = (
    "<codex_internal_context",
    "# AGENTS.md instructions for",
    "<recommended_plugins>",
    "<available_plugins>",
    "<environment_context>",
    "<user_instructions>",
    "<INSTRUCTIONS>",
)

KULLANICI = "kullanici"
MODEL = "model"


class Oturum(NamedTuple):
    kaynak: str  # "claude" | "codex"
    kimlik: str
    yol: Path
    proje: str
    an: datetime  # son yazma zamani (yerel)
    boyut: int  # bayt
    parcalar: tuple[Path, ...] = ()  # ayni mantiksal oturumun tum ham dosyalari

    @property
    def kisa(self) -> str:
        """Kisa kimlik. Codex UUID'leri ZAMAN TABANLI: ayni dakikada acilan iki
        oturum ayni ilk 8 haneyi paylasiyor. 20.09'da arsivde 24 ayri ilk-8
        cakismasi olctuk, biri dort oturumluk (claude 5c600e7e · 20.09 00:29).
        Bu yuzden Codex'te 13 hane (8 + '-' + 4) kullanilir."""
        return self.kimlik[:13] if self.kaynak == "codex" else self.kimlik[:8]

    def satir(self) -> str:
        return (
            f"{self.an:%d.%m.%Y %H:%M}  {self.kaynak:<6} {self.kisa}  "
            f"{self.boyut / 1024:>7.0f} KB  {self.proje}"
        )


class Mesaj(NamedTuple):
    rol: str  # KULLANICI | MODEL
    an: datetime  # yerel saat
    metin: str


def utf8_zorla() -> None:
    """Windows konsolu cp1254'e dusup Turkce'yi bozuyor; cikti boruya ya da
    dosyaya gitse bile bozuluyor. Turkce basan her script'te gerekli."""
    for akis in (sys.stdout, sys.stderr):
        if hasattr(akis, "reconfigure"):
            akis.reconfigure(encoding="utf-8", errors="replace")


def ham_satirlar(yol: Path) -> Iterator[str]:
    with io.open(yol, encoding='utf-8', errors='replace') as f:
        yield from f


# Proje koku = bu dosyanin bir ustu (araclar/ icinde yasiyor). Calisma
# dizinine BAKILMIYOR: araclar nereden cagrilirsa cagrilsin ayni projeyi
# bulsun diye. Klasor tasinirsa (bkz. hata 9) yine kendini bulur.
PROJE_KOKU = Path(__file__).resolve().parent.parent


def proje_adi(yol: Path | None = None) -> str:
    """Proje yolunu Claude Code'un kayit klasoru adina cevirir.

    C:/Users/Anj/Desktop/playground -> C--Users-Anj-Desktop-playground
    """
    return re.sub(r"[^A-Za-z0-9]", "-", str(yol or PROJE_KOKU))


def _yerel(damga) -> datetime:
    """Kayitlardaki UTC damgasini yerel saate cevirir (fark: 3 saat)."""
    if isinstance(damga, str):
        try:
            return datetime.fromisoformat(damga.replace("Z", "+00:00")).astimezone()
        except ValueError:
            pass
    return datetime.now().astimezone()


def _temizle(metin: str) -> str:
    """Gurultu satirlarini atar, bosluklari sadelestirir."""
    if any(im in metin for im in TAM_GURULTU):
        return ""
    tutulan = [
        s for s in metin.splitlines() if not s.lstrip().startswith(GURULTU_ONEK)
    ]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(tutulan)).strip()


def _blok_metni(icerik) -> str:
    """Claude ve Codex'in icerik bloklarindan duz metni toplar."""
    if isinstance(icerik, str):
        return icerik
    if not isinstance(icerik, list):
        return ""
    parcalar = []
    for blok in icerik:
        if not isinstance(blok, dict):
            continue
        if blok.get("type") in ("text", "input_text", "output_text"):
            metin = blok.get("text", "")
            if metin.lstrip().startswith(ENJEKSIYON_BLOK):
                continue
            parcalar.append(metin)
    return "\n".join(parcalar)


# --------------------------------------------------------------------------
# Oturumlari bulma
# --------------------------------------------------------------------------


def _codex_projesi(yol: Path) -> str:
    """Codex kaydinin ilk satirindaki session_meta icinde cwd durur."""
    try:
        with io.open(yol, encoding="utf-8") as f:
            ilk = json.loads(f.readline())
        cwd = (ilk.get("payload") or {}).get("cwd")
        return Path(cwd).name if cwd else "?"
    except (OSError, ValueError, TypeError):
        return "?"


def _codex_kimlik(yol: Path, yedek: str) -> str:
    """Codex kimligini KAYIT ICINDEN alir; dosya adi yedektir. Codex yakaladi
    (codex 01a0bb8e-de58 · 20.09 00:35): 3 kayitta dosya adindaki kimlik ile
    session_meta icindeki farkli - bunlar ayni oturumun devam kayitlari."""
    try:
        with io.open(yol, encoding="utf-8") as f:
            p = json.loads(f.readline()).get("payload") or {}
        return p.get("id") or p.get("session_id") or yedek
    except (OSError, ValueError, TypeError):
        return yedek


def _codex_cwd(yol: Path) -> str:
    """Codex kaydinin calisma dizini, tam yol ve kucuk harf (karsilastirma icin)."""
    try:
        with io.open(yol, encoding="utf-8") as f:
            ilk = json.loads(f.readline())
        cwd = (ilk.get("payload") or {}).get("cwd") or ""
        return str(Path(cwd)).lower() if cwd else ""
    except (OSError, ValueError, TypeError):
        return ""


def oturumlar(kapsam: str = "hepsi", proje: str | None = None) -> list[Oturum]:
    """kapsam: proje | claude | codex | hepsi

    "proje" icinde bulunulan klasorun oturumlarini verir: Claude kayitlari VE
    calisma dizini bu klasor olan Codex kayitlari. Beyin tek saglayiciya bagli
    kalmasin diye (kullanici karari, 19.09) - Codex'in kapanissiz biraktigi
    oturum da dedektore gorunmeli.
    """
    bulunan: list[Oturum] = []
    ev = Path.home()

    if kapsam in ("proje", "claude", "hepsi"):
        kok = ev / ".claude" / "projects"
        desen = f"{proje or proje_adi()}/*.jsonl" if kapsam == "proje" else "*/*.jsonl"
        for p in kok.glob(desen):
            st = p.stat()
            bulunan.append(
                Oturum(
                    "claude",
                    p.stem,
                    p,
                    p.parent.name,
                    datetime.fromtimestamp(st.st_mtime),
                    st.st_size,
                )
            )

    if kapsam in ("codex", "hepsi", "proje"):
        kok_yol = str(PROJE_KOKU).lower()
        # Codex Desktop kapatilan (arsivlenen) oturumu sessions/'dan
        # archived_sessions/'a TASIYOR. Yalnizca sessions/ taranirken 61 oturum
        # aramaya, dedektore ve isaretci denetimine gorunmuyordu
        # (claude 5c600e7e · 19.09 20:10).
        codex_kok = ev / ".codex"
        kaynaklar = [*(codex_kok / "sessions").glob("**/*.jsonl"),
                     *(codex_kok / "archived_sessions").glob("*.jsonl")]
        for p in kaynaklar:
            if kapsam == "proje" and (proje or _codex_cwd(p) != kok_yol):
                continue
            st = p.stat()
            # rollout-2026-09-05T04-35-45-<uuid>.jsonl
            kimlik = _codex_kimlik(p, p.stem.split("-", 1)[-1][20:] or p.stem)
            bulunan.append(
                Oturum(
                    "codex",
                    kimlik,
                    p,
                    _codex_projesi(p),
                    datetime.fromtimestamp(st.st_mtime),
                    st.st_size,
                )
            )

    return sorted(_tekille(bulunan), key=lambda o: o.an, reverse=True)


def _tekille(havuz: list[Oturum]) -> list[Oturum]:
    """Oturumu bir kez say, parcalarini atma. En buyuk dosya tam kopya
    olmayabilir: Astra olcumu uc Codex grubunda 81 ozel mesaj buldu.
    Ana yol en yeni yazilan parcadir; mesajlar() tum parcalari birlestirir."""
    en_iyi: dict[tuple[str, str], Oturum] = {}
    for o in havuz:
        anahtar = (o.kaynak, o.kimlik)
        mevcut = en_iyi.get(anahtar)
        if mevcut is None:
            en_iyi[anahtar] = o
        else:
            yollar = tuple(dict.fromkeys((mevcut.parcalar or (mevcut.yol,))
                                         + (o.parcalar or (o.yol,))))
            yeni = max((mevcut, o), key=lambda x: x.an)
            en_iyi[anahtar] = yeni._replace(parcalar=yollar,
                boyut=sum(p.stat().st_size for p in yollar))
    return list(en_iyi.values())


def oturum_bul(parca: str, kapsam: str = "hepsi") -> Oturum | None:
    """Tam kimlik veya benzersiz onek. Belirsizlikte ilk kaydi SECMEZ."""
    havuz = oturumlar(kapsam)
    tam = [o for o in havuz if o.kimlik == parca]
    eslesen = tam or [o for o in havuz if o.kimlik.startswith(parca)
                     or o.yol.stem.startswith(parca)]
    if len(eslesen) == 1:
        return eslesen[0]
    if len(eslesen) > 1:
        print(f"UYARI: belirsiz oturum '{parca}'; tam kimlik ver: "
              + ", ".join(o.kimlik for o in eslesen), file=sys.stderr)
    return None


# --------------------------------------------------------------------------
# Mesajlari okuma
# --------------------------------------------------------------------------


def _claude_mesajlari(yol: Path) -> Iterator[Mesaj]:
    for satir in ham_satirlar(yol):
        satir = satir.strip()
        if not satir:
            continue
        try:
            k = json.loads(satir)
        except json.JSONDecodeError:
            continue
        tip = k.get("type")
        if tip not in ("user", "assistant") or k.get("isSidechain"):
            continue
        if tip == "user" and "toolUseResult" in k:
            continue  # arac ciktisi, kullanici mesaji degil
        if k.get("isMeta"):
            continue  # skill metni, komut uyarisi, sistem notu: harness yazdi, kullanici degil
        if k.get("isCompactSummary"):
            # Sikistirma ozeti. type=user gorunur ama kullanici yazmadi: modelin
            # kendi kayipli ozetidir, harness enjekte eder. Omurgaya girerse
            # ritualin "hatirlamaya degil okumaya dayan" garantisi bozulur -
            # kapanisi yazan ajan ozeti ham kayit sanir. Olculdu: ayni oturumda
            # 41 mesaj / 19,5 KB -> 43 mesaj / 44,2 KB, farkin tamami bu tek
            # girdiden ([[olculmus-bulgular]] §17, claude 96517e26 · 21.09 02:48).
            # Kayittaki isCompactSummary alani bunu acikca soyluyor; metin
            # desenine bakmaya gerek yok. Sikistirmanin KENDISI kaybolmuyor:
            # PreCompact zaten derleme/omurga-anlik/ altina anlik goruntu yazip
            # devir kutusuna not birakiyor.
            continue
        govde = _temizle(_blok_metni((k.get("message") or {}).get("content", "")))
        if govde:
            yield Mesaj(
                KULLANICI if tip == "user" else MODEL, _yerel(k.get("timestamp")), govde
            )


def _codex_mesajlari(yol: Path) -> Iterator[Mesaj]:
    for satir in ham_satirlar(yol):
        satir = satir.strip()
        if not satir:
            continue
        try:
            k = json.loads(satir)
        except json.JSONDecodeError:
            continue
        p = k.get("payload")
        if k.get("type") != "response_item" or not isinstance(p, dict):
            continue
        if p.get("type") != "message":
            continue
        rol = p.get("role")
        if rol not in ("user", "assistant"):
            continue  # developer = sistem enjeksiyonu
        govde = _temizle(_blok_metni(p.get("content", "")))
        if govde:
            yield Mesaj(
                KULLANICI if rol == "user" else MODEL, _yerel(k.get("timestamp")), govde
            )


def mesajlar(oturum: Oturum) -> Iterator[Mesaj]:
    """Bir oturumun konusma mesajlari: arac ciktisi, dusunme ve sistem
    enjeksiyonu haric, kronolojik sirada."""
    okuyucu = _claude_mesajlari if oturum.kaynak == "claude" else _codex_mesajlari
    if not oturum.parcalar:
        yield from okuyucu(oturum.yol)
        return
    # Ayni mesaj ayni damga/rol/metinle kopyalandiysa bir kez; farkli devam
    # parcalarindaki mesajlar korunur. Dosyalara tasima/silme/yazma yapilmaz.
    birlesik = dict.fromkeys(m for p in oturum.parcalar for m in okuyucu(p))
    yield from sorted(birlesik, key=lambda m: m.an)


# Kapanis isareti: bir oturumun kapandigini soyleyen TEK kaynak.
# Eskiden "kimlik herhangi bir notta geciyor mu" diye bakiliyordu; oturum icinde
# yazilan tek bir kaynak isaretcisi, kapanmamis oturumu "islenmis" gosteriyordu
# (claude 5c600e7e · 19.09 08:27). Arsiv dosyalari da baska oturumlara atif
# yapiyor, yani "oturumlar/ icinde geciyor mu" da yetmez. Isaret acik olmali.
KAPANIS_DESENI = re.compile(r"^kapanan-oturum:\s*(.+)$", re.MULTILINE | re.IGNORECASE)


def kapanmis_mi(oturum: "Oturum", kapali: set[str]) -> bool:
    """Eski onek ancak tek oturumu gosteriyorsa kapanis kanitidir."""
    if oturum.kimlik in kapali:
        return True
    for i in kapali:
        if oturum.kimlik.startswith(i):
            bulunan = oturum_bul(i)
            if bulunan and bulunan.kimlik == oturum.kimlik:
                return True
    return False


def kod_disindaki(metin: str) -> str:
    """Markdown kod citi ornekleri mekanik isaret sanilmasin."""
    sonuc, cit, uzunluk = [], None, 0
    for satir in metin.splitlines(keepends=True):
        m = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", satir.rstrip("\r\n"))
        if m:
            isaret, kuyruk = m.groups()
            if cit is None:
                cit, uzunluk = isaret[0], len(isaret)
            elif isaret[0] == cit and len(isaret) >= uzunluk and not kuyruk.strip():
                cit = None
            continue
        if cit is None:
            sonuc.append(satir)
    return "".join(sonuc)


def kapanmis_kimlikler() -> set[str]:
    """oturumlar/*.md icindeki `kapanan-oturum: <id>[, <id>]` satirlarindan
    kapanmis oturumlarin benzersiz cozulmus tam kimlikleri.
    Taslaklar ve kod ornekleri onay sayilmaz."""
    kimlikler: set[str] = set()
    for p in (PROJE_KOKU / "oturumlar").glob("*.md"):
        if p.name.startswith("oto-"):
            continue  # model taslagi insanin kapanis onayi olamaz
        metin = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^oto-kayit:", metin, re.M):
            continue
        for satir in KAPANIS_DESENI.findall(kod_disindaki(metin)):
            for parca in re.split(r"[,\s]+", satir.strip()):
                parca = parca.strip("`")
                if re.fullmatch(r"[0-9a-f]{8}[0-9a-f-]*", parca):
                    kimlikler.add(parca)
    # Bir kez coz; dedektorun her oturum icin arsivi yeniden taramasi gerekmez.
    if not kimlikler:
        return set()
    havuz = oturumlar()
    sonuc = set()
    for i in kimlikler:
        eslesen = [o for o in havuz if o.kimlik.startswith(i)]
        if len(eslesen) == 1:
            sonuc.add(eslesen[0].kimlik)
        elif len(eslesen) > 1:
            print(f"UYARI: kapanis isareti belirsiz: {i}", file=sys.stderr)
    return sonuc
