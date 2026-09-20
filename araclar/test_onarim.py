"""Bağımsız onarım regresyonları. Test verisi derleme/astra-kontrol altında kalır.

Gerçek ham kayıtlar, görev ayarları, git uzak deposu veya kullanıcı dosyaları
değiştirilmez. Model çağrıları sahtedir. Sentetik test canlı hook kanıtı değildir.
"""
import contextlib
import io
import json
import sys
import tempfile
import subprocess
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import baglam
import bakim
import derle
import devir
import gece_kayit
import kayit
import oturum_basi
import precompact

ARTIFACTS = kayit.PROJE_KOKU / 'derleme' / 'astra-kontrol'
ARTIFACTS.mkdir(parents=True, exist_ok=True)


class OnarimTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix='test-', dir=ARTIFACTS))
        (self.root / 'oturumlar').mkdir()
        (self.root / 'notlar').mkdir()
        (self.root / 'BEYIN.md').write_text('[[acik-uclar]]', encoding='utf-8')
        self.a = self.session('01a0bb8e-1111-7000-8000-000000000001', 60)
        self.b = self.session('01a0bb8e-2222-7000-8000-000000000002', 80)

    def session(self, ident, used):
        path = self.root / (ident + '.jsonl')
        rows = [
            {'type': 'session_meta', 'payload': {'id': ident, 'cwd': str(self.root)}},
            {'type': 'response_item', 'timestamp': '2026-09-20T01:00:00Z',
             'payload': {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'Test kararı'}]}},
            {'type': 'event_msg', 'payload': {'type': 'token_count', 'info': {
                'last_token_usage': {'input_tokens': used-10, 'total_tokens': used}, 'model_context_window': 100}}},
        ]
        path.write_text('\n'.join(json.dumps(r) for r in rows), encoding='utf-8')
        return kayit.Oturum('codex', ident, path, 'test', datetime.now()-timedelta(hours=7), path.stat().st_size)

    def test_ambiguous_lookup_does_not_select_first(self):
        with patch.object(kayit, 'oturumlar', return_value=[self.b, self.a]):
            self.assertIsNone(kayit.oturum_bul('01a0bb8e'))
            self.assertEqual(kayit.oturum_bul(self.a.kimlik), self.a)

    def test_context_fallback_keeps_full_identity(self):
        with patch.object(kayit, 'oturumlar', return_value=[self.b, self.a]), \
             patch.object(baglam, 'DURUM', self.root/'state.json'), \
             patch.object(baglam, 'ANLIK', self.root/'snapshots'):
            message = baglam.kontrol(None, self.a.kimlik)
        self.assertIn('60%', message)
        self.assertNotIn('80%', message)

    def test_startup_does_not_emit_sibling_identity(self):
        with patch.object(kayit, 'oturumlar', return_value=[self.b, self.a]), \
             patch.object(kayit, 'PROJE_KOKU', self.root), \
             patch.object(oturum_basi.devir, 'al', return_value=None), \
             patch.object(oturum_basi, 'YONERGE', self.root/'BEYIN.md'), \
             patch.object(oturum_basi, 'DURUM', self.root/'absent.json'), \
             patch.object(bakim, 'KOK', self.root), \
             patch.object(sys, 'stdin', io.StringIO(json.dumps({'session_id': self.a.kimlik}))), \
             patch.object(sys, 'argv', ['oturum_basi.py']), contextlib.redirect_stdout(io.StringIO()) as out:
            oturum_basi.main()
        self.assertIn('kapanan-oturum: '+self.a.kisa, out.getvalue())
        self.assertNotIn('kapanan-oturum: '+self.b.kisa, out.getvalue())

    def test_precompact_without_path_uses_requested_session(self):
        seen = []
        with patch.object(kayit, 'oturumlar', return_value=[self.b, self.a]), \
             patch.object(kayit, 'PROJE_KOKU', self.root), \
             patch.object(precompact, 'ANLIK', self.root/'snapshots'), \
             patch.object(precompact.devir, 'birak'), \
             patch.object(kayit, 'mesajlar', side_effect=lambda o: seen.append(o.kimlik) or []), \
             patch.object(sys, 'stdin', io.StringIO(json.dumps({'session_id': self.a.kimlik}))), \
             patch.object(sys, 'argv', ['precompact.py', '--bicim', 'codex']), \
             contextlib.redirect_stdout(io.StringIO()):
            precompact.main()
        self.assertEqual(seen, [self.a.kimlik])

    def test_precompact_snapshots_do_not_overwrite_sibling(self):
        with patch.object(kayit, 'PROJE_KOKU', self.root), \
             patch.object(precompact, 'ANLIK', self.root/'snapshots'), \
             patch.object(precompact.devir, 'birak'), contextlib.redirect_stdout(io.StringIO()):
            for o in (self.a, self.b):
                with patch.object(sys, 'stdin', io.StringIO(json.dumps({'session_id': o.kimlik, 'transcript_path': str(o.yol)}))), \
                     patch.object(sys, 'argv', ['precompact.py', '--bicim', 'codex']):
                    precompact.main()
        self.assertEqual(len(list((self.root/'snapshots').glob('*.md'))), 2)

    def test_context_unknown_window_is_reported(self):
        with patch.object(baglam, 'DURUM', self.root/'state.json'), \
             patch.object(baglam, 'olc', return_value={'yuzde': None, 'not': 'pencere bilinmiyor'}):
            message = baglam.kontrol(str(self.a.yol), self.a.kimlik)
        self.assertIsNotNone(message)
        self.assertIn('OLCULEMEDI', message)

    def test_failed_snapshot_is_retried(self):
        with patch.object(baglam, 'DURUM', self.root/'state.json'), \
             patch.object(baglam, '_omurga_al', side_effect=[None, 'recovered.md']) as snap:
            first = baglam.kontrol(str(self.a.yol), self.a.kimlik)
            second = baglam.kontrol(str(self.a.yol), self.a.kimlik)
        self.assertEqual(snap.call_count, 2)
        self.assertIn('ALINAMADI', first)
        self.assertIn('recovered.md', second)

    def test_closure_ignores_code_example_and_draft(self):
        (self.root/'oturumlar/example.md').write_text('# Örnek\n```\nkapanan-oturum: '+self.a.kisa+'\n```\n', encoding='utf-8')
        (self.root/'oturumlar/oto-test.md').write_text('# Taslak\nkapanan-oturum: '+self.b.kisa, encoding='utf-8')
        with patch.object(kayit, 'PROJE_KOKU', self.root):
            self.assertEqual(kayit.kapanmis_kimlikler(), set())

    def test_legacy_ambiguous_closure_does_not_close_siblings(self):
        with patch.object(kayit, 'oturumlar', return_value=[self.b, self.a]):
            self.assertFalse(kayit.kapanmis_mi(self.a, {'01a0bb8e'}))

    def test_explicit_dry_run_never_calls_model(self):
        with patch.object(sys, 'argv', ['gece_kayit.py', '--kuru', '--oturum', self.a.kimlik]), \
             patch.object(kayit, 'oturum_bul', return_value=self.a), \
             patch.object(gece_kayit, 'yazdir', return_value=(True, 'mock')) as write, contextlib.redirect_stdout(io.StringIO()):
            gece_kayit.main()
        write.assert_not_called()

    def test_model_cannot_write_closure_marker_in_draft(self):
        fake = type('Result', (), {'stdout': '# Taslak\nkapanan-oturum: '+self.a.kisa+'\n'+'a'*250, 'stderr':'', 'returncode':0})()
        with patch.object(gece_kayit, 'istem', return_value='fixture'), \
             patch.object(gece_kayit.subprocess, 'run', return_value=fake):
            ok, note = gece_kayit.yazdir(self.a, self.root/'bad-draft.md')
        self.assertFalse(ok)
        self.assertFalse((self.root/'bad-draft.md').exists())

    def test_citation_invalid_id_not_silently_skipped(self):
        p = self.root/'citation.md'
        p.write_text('(codex xyz · 20.09 04:00)', encoding='utf-8')
        total, bad, unknown = derle.isaretci_denetle([p])
        self.assertEqual(total, 1)
        self.assertEqual(len(unknown), 1)

    def test_token_zero_is_valid_measurement(self):
        o = self.session('01a00000-0000-7000-8000-000000000001', 0)
        self.assertEqual(baglam.olc(o)['yuzde'], 0)

    def test_parallel_context_updates_are_preserved(self):
        script = """import sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import baglam
baglam.DURUM=Path(sys.argv[2]); baglam.ANLIK=Path(sys.argv[3])
original=baglam._durum_oku
def slow():
 d=original(); time.sleep(0.2); return d
baglam._durum_oku=slow
baglam.kontrol(sys.argv[4],sys.argv[5])
"""
        workers = [subprocess.Popen([sys.executable, '-c', script, str(Path(__file__).parent),
                   str(self.root/'parallel.json'), str(self.root/'snaps'), str(o.yol), o.kimlik],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE) for o in (self.a,self.b)]
        for p in workers:
            p.communicate(timeout=10)
            self.assertEqual(p.returncode,0)
        data = json.loads((self.root/'parallel.json').read_text(encoding='utf-8'))
        self.assertIn(self.a.kimlik, data)
        self.assertIn(self.b.kimlik, data)

    def test_git_commit_failure_cannot_report_success(self):
        def fake(*args):
            if args[0] == 'status':
                return subprocess.CompletedProcess(args,0,' M file.md','')
            if 'commit' in args:
                return subprocess.CompletedProcess(args,1,'','commit failed')
            return subprocess.CompletedProcess(args,0,'','')
        with patch.object(derle,'git_sonuc',side_effect=fake), contextlib.redirect_stdout(io.StringIO()) as out:
            result = derle.yedekle()
        self.assertEqual(result['commit'],'BASARISIZ')
        self.assertNotIn('commit atildi',out.getvalue())

    def test_failed_push_cannot_be_masked_by_local_tracking_ref(self):
        def fake(*args):
            if args[0] == 'remote':
                return subprocess.CompletedProcess(args,0,'origin','')
            if args[0] == 'push':
                return subprocess.CompletedProcess(args,1,'','network failure')
            return subprocess.CompletedProcess(args,0,'','')
        with patch.object(derle,'git_sonuc',side_effect=fake), contextlib.redirect_stdout(io.StringIO()):
            result = derle.yedekle()
        self.assertEqual(result['push'],'BASARISIZ')

    def test_monthly_ratio_uses_only_this_sessions_archive(self):
        (self.root/'oturumlar/a.md').write_text('# A\nkapanan-oturum: '+self.a.kisa+'\nsmall',encoding='utf-8')
        (self.root/'oturumlar/b.md').write_text('# B\nkapanan-oturum: '+self.b.kisa+'\n'+'b'*20000,encoding='utf-8')
        messages=[kayit.Mesaj(kayit.KULLANICI,datetime.now().astimezone(),'karar '*5000)]
        with patch.object(derle,'KOK',self.root), patch.object(kayit,'PROJE_KOKU',self.root), \
             patch.object(kayit,'oturumlar',return_value=[self.a,self.b]), \
             patch.object(kayit,'mesajlar',return_value=messages), \
             patch.object(derle,'git',return_value=''), patch.object(derle,'yaz') as write:
            derle.aylik(datetime.now(),True)
        self.assertIn(self.a.kisa,write.call_args.args[1])

    def test_failed_nightly_writer_is_visible_at_startup(self):
        p=self.root/'status.json'
        p.write_text(json.dumps({'baslangic':datetime.now().strftime('%Y-%m-%d %H:%M'),
            'tamamlandi':True,'oto_kayit':['- x BASARISIZ: timeout'],'commit':'BASARISIZ'}),encoding='utf-8')
        with patch.object(oturum_basi,'DURUM',p):
            warnings=oturum_basi.derleyici_uyarilari(datetime.now())
        self.assertTrue(any('TASLA' in s or 'GECE KAYDI' in s for s in warnings))
        self.assertTrue(any('COMMIT' in s for s in warnings))

    def test_dedup_preserves_messages_unique_to_smaller_file(self):
        copy_path=self.root/'small-copy.jsonl'
        rows=self.a.yol.read_text(encoding='utf-8').splitlines()
        row=json.loads(rows[1]); row['payload']['content'][0]['text']='Devam parcasindaki karar'
        copy_path.write_text(rows[0]+'\n'+json.dumps(row),encoding='utf-8')
        other=self.a._replace(yol=copy_path,boyut=copy_path.stat().st_size,an=datetime.now())
        merged=kayit._tekille([self.a,other])
        self.assertEqual(len(merged),1)
        texts=[m.metin for m in kayit.mesajlar(merged[0])]
        self.assertEqual(set(texts),{'Test kararı','Devam parcasindaki karar'})

    def test_handoff_queue_preserves_two_sessions_and_delivers_to_owner(self):
        with patch.object(devir,'KUTU',self.root/'queue.json'):
            devir.birak('Birinci oturum',self.a.kimlik)
            devir.birak('Ikinci oturum',self.b.kimlik)
            self.assertIsNone(devir.al('unknown'))
            self.assertEqual(devir.al(self.a.kimlik),'Birinci oturum')
            self.assertEqual(devir.al(self.b.kimlik),'Ikinci oturum')
            self.assertIsNone(devir.al(self.a.kimlik))

    def test_draft_candidates_respect_six_hours_and_existing_draft(self):
        now=datetime.now()
        old=self.a._replace(an=now-timedelta(hours=6))
        fresh=self.b._replace(an=now-timedelta(hours=6)+timedelta(seconds=1))
        with patch.object(kayit,'oturumlar',return_value=[old,fresh]), \
             patch.object(kayit,'kapanmis_kimlikler',return_value=set()), \
             patch.object(gece_kayit,'KOK',self.root):
            self.assertEqual(gece_kayit.adaylar(now),[old])
            gece_kayit.oto_dosyasi(old).write_text('oto-kayit: '+old.kisa+' '+old.an.strftime('%Y-%m-%d %H:%M'),encoding='utf-8')
            self.assertEqual(gece_kayit.adaylar(now),[])

    def test_orphan_and_unmapped_notes_are_detected_with_aliases(self):
        (self.root/'notlar/acik-uclar.md').write_text('',encoding='utf-8')
        (self.root/'notlar/aliased.md').write_text('a',encoding='utf-8')
        (self.root/'notlar/missing.md').write_text('a',encoding='utf-8')
        (self.root/'BEYIN.md').write_text('[[acik-uclar]] [[aliased#Bölüm|Görüntü]]',encoding='utf-8')
        (self.root/'oturumlar'/('oto-'+self.a.kisa+'.md')).write_text('taslak',encoding='utf-8')
        with patch.object(bakim,'KOK',self.root), \
             patch.object(kayit,'kapanmis_kimlikler',return_value={self.a.kimlik}):
            result=bakim.olc()
        self.assertEqual(result['haritasiz'],['missing'])
        self.assertEqual(result['yetim_taslak'],['oto-'+self.a.kisa+'.md'])

    def test_same_and_other_session_draft_startup_messages(self):
        (self.root/'oturumlar'/('oto-'+self.a.kisa+'.md')).write_text('taslak',encoding='utf-8')
        def startup(ident):
            with patch.object(kayit,'oturumlar',return_value=[self.a]), \
                 patch.object(kayit,'PROJE_KOKU',self.root), \
                 patch.object(oturum_basi.devir,'al',return_value=None), \
                 patch.object(oturum_basi,'YONERGE',self.root/'BEYIN.md'), \
                 patch.object(bakim,'KOK',self.root), \
                 patch.object(sys,'stdin',io.StringIO(json.dumps({'session_id':ident}))), \
                 patch.object(sys,'argv',['oturum_basi.py']),contextlib.redirect_stdout(io.StringIO()) as out:
                oturum_basi.main()
            return json.loads(out.getvalue())['hookSpecificOutput']['additionalContext']
        self.assertIn('BU OTURUM ICIN GECE TASLAGI VAR',startup(self.a.kimlik))
        self.assertIn('GECE TASLAGI VAR: oturumlar/',startup(self.b.kimlik))

    def test_threshold_crossings_repeat_only_after_reset(self):
        with patch.object(baglam,'DURUM',self.root/'sequence.json'), \
             patch.object(baglam,'ANLIK',self.root/'snaps'):
            outputs=[]
            for value in (49,50,60,70,80,20,50):
                self.a=self.session(self.a.kimlik,value)
                outputs.append(baglam.kontrol(str(self.a.yol),self.a.kimlik))
        self.assertEqual([x is not None for x in outputs],[False,True,False,True,False,False,True])

    def test_model_success_writes_only_draft(self):
        fake=type('Result',(),{'stdout':'# Denetim taslagi\n'+'Açıklama. '*40,'stderr':'','returncode':0})()
        with patch.object(gece_kayit,'istem',return_value='fixture'), \
             patch.object(gece_kayit.subprocess,'run',return_value=fake):
            ok,_=gece_kayit.yazdir(self.a,self.root/'draft.md')
        self.assertTrue(ok)
        self.assertIn('oto-kayit:',(self.root/'draft.md').read_text(encoding='utf-8'))
        self.assertEqual(list((self.root/'notlar').iterdir()),[])

    def test_goal_scheduler_context_is_not_a_user_message(self):
        block={'type':'input_text','text':'<codex_internal_context source="goal">scheduler</codex_internal_context>'}
        self.assertEqual(kayit._blok_metni([block]),'')
        real={'type':'input_text','text':'/goal Bu klasoru denetle.'}
        self.assertEqual(kayit._blok_metni([real]),real['text'])


if __name__ == '__main__':
    kayit.utf8_zorla()
    unittest.main(verbosity=2)
