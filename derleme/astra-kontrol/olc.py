"""Astra denetimi: ham kayıttan özet kanıt. Kullanıcı mesajlarını kopyalamaz."""
import collections
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'araclar'))
import kayit
import baglam
import bakim


def run():
    pool = kayit.oturumlar()
    groups = collections.defaultdict(list)
    for o in pool:
        groups[o.kimlik[:8]].append(o.kimlik)
    collisions = {k: v for k, v in groups.items() if len(v) > 1}
    closed = kayit.kapanmis_kimlikler()
    report = {'an': datetime.now().isoformat(), 'oturum_sayisi': len(pool),
              'ilk8_cakismalar': collisions,
              'belirsiz_kapanislar': {k: v for k, v in collisions.items() if k in closed},
              'bakim': bakim.olc(), 'kayitlar': []}
    for prefix in ('01a0bbc6-b6f6', '01a0bbcc-8818', '01a0bc5c-f1c4',
                   '01a0bb8e-de58', '01a0bb8e-4631', '5c600e7e', '96517e26'):
        o = kayit.oturum_bul(prefix)
        if not o:
            report['kayitlar'].append({'aranan': prefix, 'yok': True})
            continue
        row = {'id': o.kimlik, 'dosya': str(o.yol), 'olcum': baglam.olc(o),
               'hook_kaniti': [], 'claude_esik': []}
        with o.yol.open(encoding='utf-8') as f:
            for number, line in enumerate(f, 1):
                try:
                    data = json.loads(line)
                except ValueError:
                    continue
                p = data.get('payload') or {}
                if data.get('type') == 'session_meta':
                    row['meta'] = {k: p.get(k) for k in ('originator', 'source', 'cli_version')}
                if data.get('type') == 'response_item' and p.get('role') == 'developer':
                    blocks = p.get('content') or []
                    text = '\n'.join(b.get('text', '') for b in blocks if isinstance(b, dict))
                    if 'hooks.additional_context' in line:
                        row['hook_kaniti'].append({'satir': number, 'an': data.get('timestamp'),
                            'tip': data.get('type'), 'rol': p.get('role'),
                            'kind': (p.get('internal_chat_message_metadata_passthrough') or {}).get('content_item_kinds'),
                            'harita': 'BU PROJENIN BEYNI' in text,
                            'saat': 'Su anki yerel tarih ve saat:' in text,
                            'esik': 'BAGLAM ' in text, 'uzunluk': len(text)})
                if o.kaynak == 'claude' and ('BAGLAM 5' in line or 'BAGLAM 7' in line):
                    row['claude_esik'].append({'satir': number, 'an': data.get('timestamp'),
                        'tip': data.get('type'), 'alt_tip': data.get('subtype'),
                        'toolUseResult': 'toolUseResult' in data})
        report['kayitlar'].append(row)
    out = ROOT / 'derleme/astra-kontrol' / (sys.argv[1] if len(sys.argv) > 1 else 'ilk-olcum.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    kayit.utf8_zorla()
    run()
