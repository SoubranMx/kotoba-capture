"""Portable configuration tests; all paths and contents are synthetic."""
import json
import tempfile
import unittest
from pathlib import Path
from kotoba_capture.pilot_config import ConfigError, load_config, read_env

POLICY = dict(roi=[0, 0, 1, 1], mainHeight=[.1, .3], rowCenterTolerance=.02,
              maxInlineGap=.1, maxRowGap=.1, minHorizontalOverlap=.2)


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'media').mkdir()
        (self.root / 'media/sample.mp4').write_bytes(b'synthetic video')
        for model in ('det', 'rec'):
            folder = self.root / '.local' / model
            folder.mkdir(parents=True)
            for name in ('inference.json', 'inference.yml', 'inference.pdiparams'):
                (folder / name).write_bytes(b'synthetic model')
        (self.root / '.local/policy.json').write_text(json.dumps({'policies': {'manual': POLICY}}))
        self.env = dict(KOTOBA_MEDIA_ROOT='media', KOTOBA_EXPERIMENT_DATA_DIR='.local',
                        KOTOBA_PILOT_DET_MODEL_DIR='.local/det', KOTOBA_PILOT_REC_MODEL_DIR='.local/rec',
                        KOTOBA_PILOT_POLICY_FILE='.local/policy.json', KOTOBA_PILOT_PROFILE_ID='manual')

    def config(self, **kwargs):
        environment = kwargs.pop('environment', self.env)
        return load_config(self.root, 'sample.mp4', 'trial', environment=environment, **kwargs)

    def test_portable_relative_paths_and_optional_vault(self):
        c = self.config()
        self.assertEqual(c.video, self.root / 'media/sample.mp4')
        self.assertEqual(c.interval, .5)
        self.assertEqual(c.threads, 10)
        self.assertEqual(c.device, 'cpu')
        self.assertEqual(c.policy, POLICY)

    def test_device_accepts_only_cpu_or_explicit_first_gpu(self):
        self.assertEqual(self.config().device, 'cpu')
        self.assertEqual(self.config(environment={**self.env, 'KOTOBA_PILOT_DEVICE': 'gpu:0'}).device, 'gpu:0')
        for value in ('gpu', 'gpu:1', 'cuda:0', 'CPU', ' cpu', ''):
            with self.subTest(value=value), self.assertRaises(ConfigError):
                self.config(environment={**self.env, 'KOTOBA_PILOT_DEVICE': value})

    def test_env_loader_and_environment_precedence(self):
        (self.root / '.env').write_text('KOTOBA_PILOT_CPU_THREADS="2" # comment\nKOTOBA_PILOT_INTERVAL=0.25\n')
        self.env['KOTOBA_PILOT_CPU_THREADS'] = '3'
        self.assertEqual(self.config().threads, 3)
        self.assertEqual(self.config().interval, .25)

    def test_env_parser_rejects_shell_syntax_and_duplicates(self):
        for raw in ('export X=1', 'X=$(touch danger)', 'X=${HOME}', 'X=one\nX=two', 'X="unterminated', 'bad-key=1'):
            with self.subTest(raw=raw):
                p = self.root / 'bad.env'; p.write_text(raw)
                with self.assertRaises(ConfigError): read_env(p)

    def test_env_quotes_comments_no_execution(self):
        p = self.root / 'simple.env'; p.write_text('A="spaces # literal" # note\nB=word # note\nC=\'quoted\'\n')
        self.assertEqual(read_env(p), {'A': 'spaces # literal', 'B': 'word', 'C': 'quoted'})

    def test_missing_settings_and_errors_do_not_leak_values(self):
        self.env.pop('KOTOBA_MEDIA_ROOT')
        with self.assertRaises(ConfigError) as caught: self.config()
        self.assertNotIn(str(self.root), str(caught.exception))

    def test_traversal_absolute_and_symlink_escape(self):
        outside = self.root / 'outside.mp4'; outside.write_bytes(b'outside')
        (self.root / 'media/link.mp4').symlink_to(outside)
        for alias in ('../outside.mp4', str(outside), 'link.mp4'):
            with self.subTest(alias=alias), self.assertRaises(ConfigError):
                load_config(self.root, alias, 'trial', environment=self.env)

    def test_invalid_output_token_or_experiment_root(self):
        for name in ('../x', '/absolute', 'has/slash', '.', 'a b'):
            with self.subTest(name=name), self.assertRaises(ConfigError):
                load_config(self.root, 'sample.mp4', name, environment=self.env)
        self.env['KOTOBA_EXPERIMENT_DATA_DIR'] = 'public'
        with self.assertRaises(ConfigError): self.config()

    def test_output_symlink_escape(self):
        (self.root / '.local/trial').symlink_to(self.root / 'media', target_is_directory=True)
        with self.assertRaises(ConfigError): self.config()

    def test_invalid_numbers(self):
        for field in ('KOTOBA_PILOT_INTERVAL', 'KOTOBA_PILOT_CPU_THREADS'):
            for value in ('nan', 'inf', '0', '-1', '1e400', '999999999999999999999999999'):
                with self.subTest(field=field, value=value):
                    changed = {**self.env, field: value}
                    with self.assertRaises(ConfigError):
                        load_config(self.root, 'sample.mp4', 'trial', environment=changed)

    def test_unknown_or_invalid_profile_and_missing_model(self):
        for content in ({'policies': {}}, {'policies': {'manual': {'roi': [0, 0, 1, 1]}}}):
            (self.root / '.local/policy.json').write_text(json.dumps(content))
            with self.assertRaises(ConfigError): self.config()
        (self.root / '.local/policy.json').write_text(json.dumps({'policies': {'manual': POLICY}}))
        (self.root / '.local/det/inference.json').unlink()
        with self.assertRaises(ConfigError): self.config()

    def test_model_symlink_escape(self):
        p = self.root / '.local/det/inference.json'; p.unlink()
        p.symlink_to(self.root / 'media/sample.mp4')
        with self.assertRaises(ConfigError): self.config()
