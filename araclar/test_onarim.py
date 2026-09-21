"""Bağımsız onarım regresyonları. Test verisi işletim sisteminin geçici alanında.

Gerçek ham kayıtlar, görev ayarları, git uzak deposu veya kullanıcı dosyaları
değiştirilmez. Model çağrıları sahtedir. Sentetik test canlı hook kanıtı değildir.
Her test kendi geçici ağacını başarıda ve hatada temizler; Obsidian kasasına
sahte BEYIN.md yazılmaz. Ani süreç öldürülse bile kalıntı kasa dışında kalır.
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import time
import subprocess
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import baglam
import bakim
import derle
import devir
import disari
import gece_kayit
import gorunurluk
import kayit
import oturum_basi
import precompact

class OnarimTests(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory(prefix='playground-onarim-')
        self.addCleanup(self._temp.cleanup)  # setUp da hata verse çalışır
        self.root = Path(self._temp.name).resolve()
        assert self.root.parent == Path(tempfile.gettempdir()).resolve()
        assert not self.root.is_relative_to(kayit.PROJE_KOKU.resolve())
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

    def acik_kapi(self):
        """Görünürlük kapısını yalnız bu test için açık tutar.

        Fikstür oturumu geçici ağaçta durur, yani gerçek manifestoya göre
        `ozel`dir ve kapı onu haklı olarak durdurur. Kapının kendi testi
        `test_gece_yazicisi_kapiyi_sormadan_model_cagirmaz`. Buradaki testler
        taslak yazımını ölçtüğü için kapı açıkça açılır — sessizce değil.
        """
        return patch.object(gece_kayit.disari, 'dene',
                            return_value=disari.Karar(True, 'model', (), ()))

    def test_gece_yazicisi_kapiyi_sormadan_model_cagirmaz(self):
        """Tanınmayan ham kayıt `ozel`dir; gece yazıcısı onu modele veremez.

        19.09'dan 21.09'a kadar her gece veriyordu ve hiçbir yer sormuyordu
        (claude 96517e26 · 21.09 07:52). Kullanıcı 21.09 20:29'da BU KASANIN
        kayıtlarını açtı (`dis_kaynaklar`); fikstür kaydı kasanın kayıt
        klasöründe değil, bu yüzden kapalı kalır. Model çağrısının HİÇ
        yapılmadığını ölçer: kapı, isteği göndermeden önce durdurmalı.
        """
        with patch.object(gece_kayit, 'istem', return_value='fixture'), \
             patch.object(gece_kayit.subprocess, 'run') as cagri:
            ok, neden = gece_kayit.yazdir(self.a, self.root / 'olmamali.md')
        self.assertFalse(ok)
        cagri.assert_not_called()
        self.assertIn('gorunurluk kapisi', neden)
        self.assertFalse((self.root / 'olmamali.md').exists())

    def test_explicit_dry_run_never_calls_model(self):
        with patch.object(sys, 'argv', ['gece_kayit.py', '--kuru', '--oturum', self.a.kimlik]), \
             patch.object(kayit, 'oturum_bul', return_value=self.a), \
             patch.object(gece_kayit, 'yazdir', return_value=(True, 'mock')) as write, contextlib.redirect_stdout(io.StringIO()):
            gece_kayit.main()
        write.assert_not_called()

    def test_model_cannot_write_closure_marker_in_draft(self):
        fake = type('Result', (), {'stdout': '# Taslak\nkapanan-oturum: '+self.a.kisa+'\n'+'a'*250, 'stderr':'', 'returncode':0})()
        with self.acik_kapi(), patch.object(gece_kayit, 'istem', return_value='fixture'), \
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
        with self.acik_kapi(), patch.object(gece_kayit,'istem',return_value='fixture'), \
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

    def test_fixture_is_cleaned_even_when_setup_fails(self):
        created=[]
        class BrokenSetup(OnarimTests):
            def setUp(inner):
                super().setUp()
                created.append(inner.root)
                raise RuntimeError('denetimli setUp hatasi')
            def runTest(inner):
                pass
        result=unittest.TestResult()
        BrokenSetup('runTest').run(result)
        self.assertEqual(len(result.errors),1)
        self.assertEqual(len(created),1)
        self.assertFalse(created[0].exists())

    def test_compact_summary_is_not_counted_as_user_message(self):
        """Sikistirma ozeti type=user gorunur ama kullanici yazmadi.

        Omurgaya girerse kapanisi yazan ajan modelin kayipli ozetini ham
        kayit sanir - ritualin tek garantisi budur. Kayittaki
        isCompactSummary alani ayrimi acikca veriyor.
        (olculmus-bulgular §17, claude 96517e26 · 21.09 02:48)
        """
        yol = self.root / 'claude-compact.jsonl'
        satirlar = [
            {'type': 'user', 'timestamp': '2026-09-21T01:00:00Z',
             'message': {'role': 'user', 'content': 'Gercek kullanici sozu'}},
            {'type': 'user', 'timestamp': '2026-09-21T02:42:00Z',
             'isCompactSummary': True, 'isVisibleInTranscriptOnly': True,
             'message': {'role': 'user',
                         'content': 'This session is being continued from a '
                                    'previous conversation that ran out of context.'}},
            {'type': 'user', 'timestamp': '2026-09-21T03:00:00Z',
             'message': {'role': 'user', 'content': 'Sikistirmadan sonraki soz'}},
        ]
        yol.write_text(chr(10).join(json.dumps(r) for r in satirlar), encoding='utf-8')
        oturum = kayit.Oturum('claude', 'compact-test', yol, 'test',
                              datetime.now(), yol.stat().st_size)
        govdeler = [m.metin for m in kayit.mesajlar(oturum)
                    if m.rol == kayit.KULLANICI]
        self.assertEqual(govdeler, ['Gercek kullanici sozu', 'Sikistirmadan sonraki soz'])
        self.assertFalse(any('ran out of context' in g for g in govdeler),
                         'sikistirma ozeti omurgaya kullanici mesaji olarak girdi')


    def test_fixture_is_cleaned_when_assertion_fails(self):
        created=[]
        class BrokenAssertion(OnarimTests):
            def runTest(inner):
                created.append(inner.root)
                inner.fail('denetimli assertion hatasi')
        result=unittest.TestResult()
        BrokenAssertion('runTest').run(result)
        self.assertEqual(len(result.failures),1)
        self.assertFalse(created[0].exists())


class SizintiTests(unittest.TestCase):
    """Astra'nın İ2 deneyinin kalıcı hâli.

    Astra 21.09 07:26'da ölçtü: açıkça `ozel` ve etiketsiz iki notu yabancı bir
    araç `internal` indeksledi, içeriği bağlama verdi ve gölge modunda sağlayıcı
    taşıyıcısına ulaştırdı (astra-denetim-raporu, [İ2] ÇÜRÜTÜLDÜ). O deney bir
    kez koştu ve bitti. Burada her test koşusunda tekrar koşar — bu sefer
    onarıma karşı.

    En kritik test `test_bulucu_yabanci_indekste_yakalar`: bulucunun "TEMİZ"
    demesi, ancak bulucu gerçekten bulabiliyorsa bir şey ifade eder. O test
    olmadan diğerlerinin hepsi boş yere geçer.
    """

    # 60 karakterden uzun ve kasada tek: imza seçiminin şartı bu.
    KANARYA_GIZLI = ('Musteri gorusmesinde konusulan rakam ve tarih burada '
                     'yazili duruyor, disari cikmamali')
    KANARYA_ETIKETSIZ = ('Bu satir hicbir gorunurluk kuralina baglanmadi, '
                         'varsayilan geregi kasadan cikmamali')
    KANARYA_IC = ('Bu satir ic duzeydedir ve bizim sectigimiz bir modele '
                  'islenmek uzere gidebilir')

    def setUp(self):
        self._temp = tempfile.TemporaryDirectory(prefix='playground-sizinti-')
        self.addCleanup(self._temp.cleanup)
        self.root = Path(self._temp.name).resolve()
        assert not self.root.is_relative_to(kayit.PROJE_KOKU.resolve())
        self._cikti = tempfile.TemporaryDirectory(prefix='playground-yansima-')
        self.addCleanup(self._cikti.cleanup)
        self.disa = Path(self._cikti.name).resolve()

        (self.root / 'notlar').mkdir()
        (self.root / 'AGENTS.md').write_text('# kural\n', encoding='utf-8')
        (self.root / 'notlar' / 'paylasilir.md').write_text(
            f'# Paylasilir\n\n{self.KANARYA_IC}\n', encoding='utf-8')
        (self.root / 'notlar' / 'gizli.md').write_text(
            f'# Gizli\n\n{self.KANARYA_GIZLI}\n', encoding='utf-8')
        # Manifestoda HIC gecmez: varsayilan 'ozel' bunu tutmali.
        (self.root / 'notlar' / 'yeni.md').write_text(
            f'# Yeni\n\n{self.KANARYA_ETIKETSIZ}\n', encoding='utf-8')

        manifesto = self.root / 'gorunurluk.json'
        manifesto.write_text(json.dumps({
            'varsayilan': 'ozel',
            'kurallar': [
                {'desen': 'AGENTS.md', 'duzey': 'acik'},
                {'desen': 'notlar/paylasilir.md', 'duzey': 'ic'},
                {'desen': 'notlar/gizli.md', 'duzey': 'ozel'},
            ]}), encoding='utf-8')

        for y in (patch.object(gorunurluk, 'KOK', self.root),
                  patch.object(gorunurluk, 'MANIFESTO', manifesto),
                  patch.object(disari, 'KOK', self.root)):
            y.start()
            self.addCleanup(y.stop)

    def yabanci_indeks(self, hedef: Path) -> Path:
        """Yabancı bir aracın kasayı tarayıp parçalayarak indekslediği hâl.

        Dosya adları kaybolur, sıra bozulur, içerik JSON'a gömülür ve hepsi
        `internal` etiketlenir — Avenox'un `beyin_v3_sync` davranışı. Birebir
        dosya karşılaştırması bunu yakalayamaz; imza satırı yakalamalı.
        """
        parca = []
        for md in sorted((self.root / 'notlar').glob('*.md')):
            for blok in md.read_text(encoding='utf-8').split('\n\n'):
                parca.append({'id': f'chunk-{len(parca)}', 'scope': 'internal',
                              'text': blok.strip()})
        hedef.mkdir(parents=True, exist_ok=True)
        (hedef / 'index.json').write_text(
            json.dumps(parca, ensure_ascii=False), encoding='utf-8')
        return hedef

    def test_bulucu_yabanci_indekste_yakalar(self):
        """NEGATİF KONTROL: bulucu gerçekten buluyor mu?

        Bu geçmezse bu sınıftaki 'temiz' sonuçlarının hiçbiri kanıt değildir.
        """
        indeks = self.yabanci_indeks(self.disa / 'yabanci')
        bulgu = disari.denetle(indeks)
        kaynaklar = {b.kaynak for b in bulgu}
        self.assertIn('notlar/gizli.md', kaynaklar)
        self.assertIn('notlar/yeni.md', kaynaklar,
                      'etiketsiz not varsayilanla ozel; sizintisi yakalanmali')
        self.assertTrue(any(b.tur == 'imza' for b in bulgu),
                        'parcalanmis indeks yalniz imza satiriyla yakalanir')
        self.assertNotIn('notlar/paylasilir.md', kaynaklar,
                         "'ic' dosya sizinti sayilmamali")

    def test_yansima_ozel_dosyayi_disarida_birakir(self):
        o = disari.yansit(self.disa / 'y', hedef='model')
        self.assertTrue(o['tamam'], o.get('hata'))
        kalan = {p.relative_to(self.disa / 'y').as_posix()
                 for p in (self.disa / 'y').rglob('*') if p.is_file()}
        self.assertIn('notlar/paylasilir.md', kalan)
        self.assertNotIn('notlar/gizli.md', kalan)
        self.assertNotIn('notlar/yeni.md', kalan)

    def test_yansima_ozel_icerigi_hicbir_dosyada_tasimaz(self):
        """Dosya adı yokken içerik başka bir dosyada geçiyor olabilir."""
        disari.yansit(self.disa / 'y', hedef='model')
        govde = '\n'.join(p.read_text(encoding='utf-8', errors='ignore')
                          for p in (self.disa / 'y').rglob('*') if p.is_file())
        self.assertNotIn(self.KANARYA_GIZLI, govde)
        self.assertNotIn(self.KANARYA_ETIKETSIZ, govde)
        self.assertIn(self.KANARYA_IC, govde)

    def test_bulucu_temiz_yansimada_alarm_vermez(self):
        disari.yansit(self.disa / 'y', hedef='model')
        self.assertEqual(disari.denetle(self.disa / 'y'), [])

    def test_yayin_yansimasi_ic_duzeyi_de_birakir(self):
        disari.yansit(self.disa / 'y', hedef='yayin')
        govde = '\n'.join(p.read_text(encoding='utf-8', errors='ignore')
                          for p in (self.disa / 'y').rglob('*') if p.is_file())
        self.assertNotIn(self.KANARYA_IC, govde)
        self.assertNotIn(self.KANARYA_GIZLI, govde)

    def test_kapi_etiketsiz_dosyayi_durdurur(self):
        k = disari.dene([self.root / 'AGENTS.md',
                         self.root / 'notlar' / 'yeni.md'], hedef='model')
        self.assertFalse(k.gecti)
        self.assertEqual([e.yol for e in k.engel], ['notlar/yeni.md'])
        self.assertIn('etiketsiz', k.engel[0].neden)
        with self.assertRaises(disari.SizintiHatasi):
            disari.kapi([self.root / 'notlar' / 'yeni.md'])

    def test_kapi_proje_disindaki_yolu_durdurur(self):
        """Ham oturum kaydı kasanın dışında durur; gece yazıcısı onu gönderir."""
        disarisi = self.disa / 'ham-kayit.jsonl'
        disarisi.write_text('{}', encoding='utf-8')
        k = disari.dene([disarisi], hedef='model')
        self.assertFalse(k.gecti)
        self.assertIn('proje kokunun disinda', k.engel[0].neden)

    def dis_kaynakli_manifesto(self, acik=True):
        m = json.loads((self.root / 'gorunurluk.json').read_text(encoding='utf-8'))
        if acik:
            m['dis_kaynaklar'] = [{'tur': 'oturum-kaydi', 'duzey': 'ic'}]
        (self.root / 'gorunurluk.json').write_text(json.dumps(m), encoding='utf-8')

    def sahte_ev(self):
        """Bu kasanın ve başka bir projenin oturum kayıtları, sahte bir evde."""
        ev = self.disa / 'ev'
        buraya = ev / '.claude' / 'projects' / kayit.proje_adi(self.root)
        baska = ev / '.claude' / 'projects' / 'C--Users-Anj-Desktop-Nar-Ajans'
        for d in (buraya, baska):
            d.mkdir(parents=True)
            (d / 'oturum.jsonl').write_text('{}', encoding='utf-8')
        cx = ev / '.codex' / 'sessions' / '2026' / '09' / '21'
        cx.mkdir(parents=True)
        for ad, cwd in (('bizim.jsonl', self.root), ('onlarin.jsonl', self.disa)):
            (cx / ad).write_text(json.dumps({'type': 'session_meta', 'payload': {
                'cwd': str(cwd)}}) + '\n', encoding='utf-8')
        return ev, buraya / 'oturum.jsonl', baska / 'oturum.jsonl', \
            cx / 'bizim.jsonl', cx / 'onlarin.jsonl'

    def test_dis_kaynak_yalniz_bu_kasanin_oturum_kaydini_acar(self):
        """Kullanıcı kararı 21.09 20:29: gece derleyicisi lokalde açık kalır.

        Kural bu kasanın ham kayıtlarını `ic` yapar — ama `~/.claude/projects`
        Nar Ajans'ın kayıtlarını da tutar ve Codex projeye göre klasörlemez.
        Başka projenin kaydı `ozel` kalmalı; müşteri malzemesi orada.
        """
        self.dis_kaynakli_manifesto()
        ev, claude_bizim, claude_baska, codex_bizim, codex_baska = self.sahte_ev()
        with patch.object(Path, 'home', return_value=ev):
            self.assertEqual(gorunurluk.duzey(claude_bizim), 'ic')
            self.assertEqual(gorunurluk.duzey(codex_bizim), 'ic')
            self.assertEqual(gorunurluk.duzey(claude_baska), 'ozel')
            self.assertEqual(gorunurluk.duzey(codex_baska), 'ozel')
            self.assertEqual(gorunurluk.duzey(self.disa / 'rastgele.jsonl'), 'ozel')

    def test_dis_kaynak_kurali_yoksa_bu_kasanin_kaydi_da_ozel(self):
        """Varsayılan güvenli taraf korunur: kasayı açan kuralın kendisidir."""
        self.dis_kaynakli_manifesto(acik=False)
        ev, claude_bizim, _, codex_bizim, _ = self.sahte_ev()
        with patch.object(Path, 'home', return_value=ev):
            self.assertEqual(gorunurluk.duzey(claude_bizim), 'ozel')
            self.assertEqual(gorunurluk.duzey(codex_bizim), 'ozel')

    def test_yansima_kasanin_icine_yazilamaz(self):
        o = disari.yansit(self.root / 'yansima', hedef='model')
        self.assertFalse(o['tamam'])
        self.assertIn('ICINE yazilamaz', o['hata'])
        self.assertFalse((self.root / 'yansima').exists())

    def test_yansima_yabanci_dolu_dizini_ezmez(self):
        yabanci = self.disa / 'baskasinin-isi'
        yabanci.mkdir()
        (yabanci / 'onemli.txt').write_text('silinmemeli', encoding='utf-8')
        o = disari.yansit(yabanci, hedef='model')
        self.assertFalse(o['tamam'])
        self.assertEqual((yabanci / 'onemli.txt').read_text(encoding='utf-8'),
                         'silinmemeli')



class DevirBorcTests(unittest.TestCase):
    """Devir kutusunun sonuç-temelli borç modeli.

    Astra bu sınıfın ilk hâlini de denetledi ve haklı çıktı (21.09 12:11):
    kilit `nullcontext` ile değiştirildiğinde 11 testin 11'i yine geçiyordu —
    yani kilit testi kilidi hiç sınamıyordu, aynı süreçte sıralı çağrılardı.
    Rapor testleri de eski hatayı kabul şartına çevirmişti.

    Buradaki testler onun karşı örneklerinin kalıcı hâli. Kabul koşulları:
    alakasız/kısmi kanıt borcu kapatmasın · tamamlama kaydı gerçekleşince
    tekrar teslim olmasın · bildirim listelemekle kapanmasın · son sahiplik
    bitmeden başarısızlık ilan edilmesin · geç kanıt terminal durumu kapatsın ·
    yarış GERÇEK iki süreçle sınansın.
    """

    def setUp(self):
        self._temp = tempfile.TemporaryDirectory(prefix='playground-devir-')
        self.addCleanup(self._temp.cleanup)
        self.root = Path(self._temp.name).resolve()
        assert not self.root.is_relative_to(kayit.PROJE_KOKU.resolve())
        (self.root / 'oturumlar').mkdir()
        (self.root / 'derleme' / 'omurga-anlik').mkdir(parents=True)
        self.kutu = self.root / 'derleme' / 'omurga-anlik' / 'devir-bekliyor.json'
        self.tamam = self.root / 'derleme' / 'omurga-anlik' / 'tamamlanan'
        for y in (patch.object(devir, 'KUTU', self.kutu),
                  patch.object(devir, 'TAMAMLANAN', self.tamam),
                  patch.object(kayit, 'PROJE_KOKU', self.root)):
            y.start()
            self.addCleanup(y.stop)

    def durum(self, event_id=None):
        veri = json.loads(self.kutu.read_text(encoding='utf-8'))
        hepsi = veri['kuyruk'] + veri.get('gecmis', [])
        if event_id is None:
            return hepsi
        return next(b for b in hepsi if b['event_id'] == event_id)

    # --- kanıt sözleşmesi -------------------------------------------------

    def test_tamamlama_kaydi_borcu_kapatir_ve_tekrar_teslim_etmez(self):
        olay = devir.birak('SIMDI YAZ', 'oturum-a')
        self.assertEqual(devir.al('oturum-a'), 'SIMDI YAZ')
        devir.tamamlandi(olay)
        self.assertIsNone(devir.al('oturum-a'))
        self.assertEqual(self.durum(olay)['durum'], devir.KAPANDI)

    def test_alakasiz_kimlik_animi_borcu_kapatmaz(self):
        """Astra karşı örneği: başka notta kimliğin geçmesi kanıt değil.

        Eski buluşsal kanıt, 'Pending review: 96517e26 — Work has NOT been
        done.' yazan bir dosyayı bile tamamlanma sayıyordu.
        """
        olay = devir.birak('SIMDI YAZ', 'oturum-a')
        (self.root / 'oturumlar' / 'baska.md').write_text(
            f'Inceleme bekliyor: {olay} ve 96517e26. Is YAPILMADI.',
            encoding='utf-8')
        self.assertEqual(devir.al('oturum-a'), 'SIMDI YAZ')

    def test_kismi_is_borcu_kapatmaz(self):
        """Borç üç iş istiyor (arşiv, terfi, harita); biri yetmez."""
        olay = devir.birak('SIMDI YAZ', 'oturum-a')
        p = self.root / 'oturumlar' / '2026-09-21-is.md'
        p.write_text('arsiv yazildi', encoding='utf-8')
        os.utime(p, (time.time() + 60, time.time() + 60))
        self.assertEqual(devir.al('oturum-a'), 'SIMDI YAZ')
        self.assertFalse((self.root / 'notlar').exists())

    def test_ayni_saniyedeki_eski_dosya_borcu_kapatmaz(self):
        """mtime karşılaştırması kalktı; saniye kırpması açığı da kalktı."""
        p = self.root / 'oturumlar' / 'eski.md'
        p.write_text('eski', encoding='utf-8')
        devir.birak('SIMDI YAZ', 'oturum-a')
        os.utime(p, (time.time() + 1, time.time() + 1))
        self.assertEqual(devir.al('oturum-a'), 'SIMDI YAZ')

    def test_her_borcun_kimligi_var(self):
        """Kanıtsız borç kalmadı: yedek PreCompact yolu da kimlik taşır."""
        olay = devir.birak('KAYIT BULUNAMADI', 'oturum-a')
        self.assertTrue(olay)
        self.assertEqual(self.durum(olay)['event_id'], olay)

    # --- sahiplik ve yeniden teslim ---------------------------------------

    def test_sahiplik_dolunca_yeniden_teslim(self):
        devir.birak('SIMDI YAZ', 'oturum-a')
        with patch.object(devir, 'SAHIPLIK_OMRU', timedelta(seconds=-1)):
            self.assertEqual(devir.al('oturum-a'), 'SIMDI YAZ')
        self.assertEqual(devir.al('oturum-a'), 'SIMDI YAZ')

    def test_canli_son_deneme_basarisiz_ilan_edilmez(self):
        """Astra ek bulgusu: üçüncü işleyici hâlâ çalışırken alakasız bir
        yoklama borcu başarısız sayıyordu."""
        devir.birak('SIMDI YAZ', 'oturum-a')
        with patch.object(devir, 'SAHIPLIK_OMRU', timedelta(seconds=-1)):
            for _ in range(devir.MAX_DENEME - 1):
                devir.al('oturum-a')
        olay = self.durum()[0]['event_id']
        self.assertEqual(devir.al('oturum-a'), 'SIMDI YAZ')  # son deneme, canli
        devir.al('baska-oturum', devral=True)  # alakasiz yoklama
        self.assertEqual(self.durum(olay)['durum'], devir.TESLIM)
        self.assertEqual(devir.raporlanacaklar(), [])

    def test_gec_gelen_kanit_terminal_durumu_kapatir(self):
        """İşleyici geç bitirdiyse başarı yine gözlenmeli."""
        olay = devir.birak('SIMDI YAZ', 'oturum-a')
        with patch.object(devir, 'SAHIPLIK_OMRU', timedelta(seconds=-1)):
            for _ in range(devir.MAX_DENEME + 1):
                devir.al('oturum-a')
        self.assertEqual(self.durum(olay)['durum'], devir.BASARISIZ)
        devir.tamamlandi(olay)
        devir.al('oturum-a')
        self.assertEqual(self.durum(olay)['durum'], devir.KAPANDI)
        self.assertEqual(devir.raporlanacaklar(), [])

    # --- bildirim: listeleme onay değildir --------------------------------

    def test_raporlamak_kuyrugu_degistirmez(self):
        """Astra [İ11]: okurken çıkarmak, düzeltilen hatanın aynısıydı."""
        devir.birak('SIMDI YAZ', 'oturum-a')
        with patch.object(devir, 'SAHIPLIK_OMRU', timedelta(seconds=-1)):
            for _ in range(devir.MAX_DENEME + 1):
                devir.al('oturum-a')
        once = self.kutu.read_text(encoding='utf-8')
        self.assertEqual(len(devir.raporlanacaklar()), 1)
        self.assertEqual(self.kutu.read_text(encoding='utf-8'), once)
        self.assertEqual(len(devir.raporlanacaklar()), 1, 'tekrar bildirilmeli')

    def test_onaysiz_bildirim_gecmis_kapasitesine_tabi_degil(self):
        """Astra: 21 yeni borç kapatılınca ilk borcun son izi siliniyordu."""
        devir.birak('ILK BORC', 'oturum-a')
        with patch.object(devir, 'SAHIPLIK_OMRU', timedelta(seconds=-1)):
            for _ in range(devir.MAX_DENEME + 1):
                devir.al('oturum-a')
        for i in range(devir.GECMIS_SINIRI + 5):
            o = devir.birak(f'yeni {i}', f'oturum-{i}')
            devir.al(f'oturum-{i}')
            devir.tamamlandi(o)
            devir.al(f'oturum-{i}')
        rapor = devir.raporlanacaklar()
        self.assertTrue(any('ILK BORC' in m for _, m in rapor),
                        'onaysiz bildirim gecmis baskisiyla kaybolmamali')

    def test_onay_gelince_kuyruktan_cikar(self):
        devir.birak('SIMDI YAZ', 'oturum-a')
        with patch.object(devir, 'SAHIPLIK_OMRU', timedelta(seconds=-1)):
            for _ in range(devir.MAX_DENEME + 1):
                devir.al('oturum-a')
        (olay, _), = devir.raporlanacaklar()
        self.assertEqual(devir.rapor_onayla([olay]), 1)
        self.assertEqual(devir.raporlanacaklar(), [])

    def test_vazgec_yalniz_terminal_borcu_kapatir_ve_is_yapildi_demez(self):
        """`rapor_onayla`'nın komut satırı yolu yoktu; bildirim ancak "iş
        yapıldı" yalanıyla kapatılabiliyordu. `--vazgec` bunu ayırır."""
        acik = devir.birak('HALA ACIK', 'oturum-b')
        basarisiz = devir.birak('DUSTU', 'oturum-a')
        with patch.object(devir, 'SAHIPLIK_OMRU', timedelta(seconds=-1)):
            for _ in range(devir.MAX_DENEME + 1):
                devir.al('oturum-a')
        for olay, beklenen in ((acik, 1), (basarisiz, 0)):
            with patch.object(sys, 'argv', ['devir.py', '--vazgec', olay]), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(devir.main(), beklenen)
        self.assertEqual(devir.raporlanacaklar(), [])
        self.assertEqual(self.durum(basarisiz)['durum'], devir.BASARISIZ,
                         'vazgecmek isi yapilmis saymaz')
        self.assertFalse((self.tamam / f'{basarisiz}.json').exists())
        self.assertEqual(self.durum(acik)['durum'], devir.BEKLIYOR)

    def test_bayat_borc_silinmez_raporlanir(self):
        devir.birak('ESKI BORC', 'oturum-a')
        veri = json.loads(self.kutu.read_text(encoding='utf-8'))
        veri['kuyruk'][0]['an'] = (datetime.now().astimezone()
                                   - timedelta(hours=13)).isoformat()
        self.kutu.write_text(json.dumps(veri), encoding='utf-8')
        self.assertIsNone(devir.al('oturum-a'))
        rapor = devir.raporlanacaklar()
        self.assertEqual(len(rapor), 1)
        self.assertIn('BAYAT', rapor[0][1])

    # --- gerçek iki süreç -------------------------------------------------

    ISCI = '''
import json, sys, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import kayit, devir
kayit.PROJE_KOKU = Path(sys.argv[2])
devir.KUTU = Path(sys.argv[3])
devir.TAMAMLANAN = Path(sys.argv[4])
kapi = Path(sys.argv[5])
while not kapi.exists():
    time.sleep(0.002)
m = devir.al('oturum-a')
print('ALDI' if m else 'BOS')
'''

    def test_iki_gercek_surec_ayni_talimati_iki_kez_basmaz(self):
        """Astra'nın ilk turda kırdığı yarış — bu sefer kendi testimizde.

        Aynı süreçte sıralı çağrı bunu sınamaz: kilit `nullcontext` yapılsa
        bile geçer. Bu yüzden iki AYRI süreç, dosya kapısıyla hizalanıyor.
        """
        devir.birak('SIMDI YAZ', 'oturum-a')
        kapi = self.root / 'kapi'
        arg = [str(Path(__file__).parent), str(self.root), str(self.kutu),
               str(self.tamam), str(kapi)]
        isciler = [subprocess.Popen([sys.executable, '-c', self.ISCI, *arg],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True)
                   for _ in range(2)]
        time.sleep(0.4)  # ikisi de kapida beklesin
        kapi.write_text('git', encoding='utf-8')
        ciktilar = [p.communicate(timeout=60)[0].strip() for p in isciler]
        self.assertEqual(sorted(ciktilar), ['ALDI', 'BOS'],
                         f'tam olarak bir surec almali, cikti: {ciktilar}')

    # --- eski sürüm -------------------------------------------------------

    def test_eski_surum_kutusu_okunabilir(self):
        self.kutu.write_text(json.dumps({'surum': 2, 'kuyruk': [
            {'an': datetime.now().isoformat(timespec='seconds'),
             'metin': 'ESKI SURUM', 'session_id': 'oturum-a',
             'kanit': {'tur': 'oturum-kaydi', 'oturum': 'x'}}]}), encoding='utf-8')
        self.assertEqual(devir.al('oturum-a'), 'ESKI SURUM')

    def test_baska_oturumun_borcu_etiketlenir(self):
        devir.birak('BASKA ISIN', 'oturum-b')
        metin = devir.al('oturum-a', devral=True)
        self.assertIn('BASKA OTURUMDAN KURTARMA BILGISI', metin)
        self.assertIn('BASKA ISIN', metin)


if __name__ == '__main__':
    kayit.utf8_zorla()
    unittest.main(verbosity=2)
