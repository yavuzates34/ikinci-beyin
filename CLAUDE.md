@AGENTS.md

# Claude'a özel

Ortak kurallar yukarıda, `AGENTS.md` içinde. Burada yalnızca Claude Code'a özgü
olanlar durur.

## Claude tarafındaki refleksler (hook'lar)

`.claude/settings.json` içinde, hepsi aynı çekirdek betikleri çağırır:

| Olay | Betik | Ne yapar |
|---|---|---|
| `SessionStart` | `araclar/oturum_basi.py` | Harita özeti, oturum kimliği, kapanmamış oturumlar, gece derleyicisi uyarıları, devir kutusu |
| `PreCompact` | `araclar/precompact.py` | Omurgayı diske alır, "şimdi yaz" uyarısını devir kutusuna bırakır |
| `UserPromptSubmit` | `araclar/devir.py` | Devir kutusunda mesaj varsa teslim eder (yedek yol) |

Saat bilgisi global ayarlardaki ayrı bir hook'tan gelir (`~/.claude/settings.json`).

Başka bir ajan bu klasörde çalışırken bu refleksler **onda yoktur**, kendi
hook'larını kurmadıkça. İki ajanın hafıza garantisi aynı sanılmasın.

## İşaretçi biçimi

Claude oturumları için `(claude <8 hane> · GG.AA SS:DD)`.
