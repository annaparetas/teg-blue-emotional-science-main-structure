"""Regression checks for access ownership, historical sources and carried links."""
import contextlib
import importlib.util
import io
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

carry = load('carry')
serve = load('serve')

class AccessConsolidation(unittest.TestCase):
    def test_retired_links_reach_their_semantic_owner(self):
        cases = [
            ('models/01-information-systems/coordinated-conscious-access.html', 'functional-sequence', '04-model-3-esc/cycle.html', 'operating-sequence'),
            ('models/01-information-systems/coordinated-conscious-access.html', '', '02-model-1-ess-cls-me/me-access.html', 'coordinated-access'),
            ('models/01-information-systems/relational-capacities.html', 'capacity-key', '02-model-1-ess-cls-me/me-access.html', 'capacity-key'),
            ('models/01-information-systems/relational-capacities.html', 'config-001', '02-model-1-ess-cls-me/me-access.html', 'config-001'),
            ('models/01-information-systems/relational-capacities.html', 'capacity-mentalizing', '02-model-1-ess-cls-me/me-access.html', 'mentalizing-access'),
            ('models/02-nervous-system-gradient/index.html', 'me-affective-sharing-access', '02-model-1-ess-cls-me/me-access.html', 'affective-sharing-access'),
            ('models/02-nervous-system-gradient/index.html', 'access-mentalizing', '02-model-1-ess-cls-me/me-access.html', 'mentalizing-access'),
            ('models/02-nervous-system-gradient/index.html', 'fluid-interoceptive-processing', '03-model-2-gradient/positions.html', 'fluid-interoceptive-processing'),
        ]
        for old, fragment, target, anchor in cases:
            with self.subTest(old=old, fragment=fragment):
                self.assertEqual(carry.new_target(old, fragment), (target, anchor))

    def test_direct_sibling_links_become_site_local_without_losing_state(self):
        self.assertEqual(carry.rewrite(
            '../../../teg-blue-emotional-science-main-structure/02-model-1-ess-cls-me/me-access.html?bia=1&asa=2&mau=3#bodily-access',
            'models/01-information-systems', '02-model-1-ess-cls-me'),
            'me-access.html?bia=1&asa=2&mau=3#bodily-access')

    def test_carry_cannot_overwrite_consolidated_pages(self):
        protected = [p for p in carry.GRADUATED_SITE_FILES if p.startswith(('02-', '04-'))]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in protected:
                file = root / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text('reviewed site content')
            with patch.object(carry, 'ROOT', root), patch.object(carry, 'source_text', side_effect=AssertionError('A graduated file must not read a replacement source')):
                for name in protected:
                    with patch.object(carry.sys, 'argv', ['carry.py', name]), contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(carry.main(), 0)
                    self.assertEqual((root / name).read_text(), 'reviewed site content')

    def test_retired_source_lookup_uses_content_before_the_redirect(self):
        for name, source, ref, _, _ in carry.MANIFEST:
            if name in ('02-model-1-ess-cls-me/access.html', '02-model-1-ess-cls-me/notes/sources/relational-capacities.html'):
                with self.subTest(name=name):
                    self.assertIsNotNone(ref)
                    old = carry.source_text(source, ref)
                    self.assertGreater(len(old), 10000)
                    self.assertNotIn('data-access-page=', old)

    def test_only_dials_have_active_access_controls(self):
        dials = (ROOT / '02-model-1-ess-cls-me/me-access.html').read_text()
        self.assertEqual(len(re.findall(r'<input\b', dials)), 3)
        for file in [ROOT / '03-model-2-gradient/positions.html', carry.ENGINE / 'models/02-nervous-system-gradient/index.html']:
            text = file.read_text()
            self.assertNotRegex(text, r'<input\b')
            self.assertNotIn('updateAccessModel', text)
        snapshot = (ROOT / '02-model-1-ess-cls-me/notes/sources/relational-capacities.html').read_text()
        self.assertNotRegex(snapshot, r'<(?:script|button|input)\b')
        self.assertEqual(len(re.findall('class="config-card"', snapshot)), 8)

    def test_approved_band_and_configuration_readings_are_preserved(self):
        current = (ROOT / '02-model-1-ess-cls-me/me-access.html').read_text()
        before = subprocess.check_output(['git', '-C', str(ROOT), 'show', 'c815582:02-model-1-ess-cls-me/me-access.html'], text=True)
        pattern = r'var CARDS = (.*?)(?=      function bandWord)'
        self.assertEqual(re.search(pattern, current, re.S)[1], re.search(pattern, before, re.S)[1])
        old_capacities = subprocess.check_output(['git', '-C', str(ROOT), 'show', 'c815582:assets/capacities.js'], text=True)
        current_capacities = (ROOT / 'assets/capacities.js').read_text()
        self.assertEqual(current_capacities.split('  var listeners')[0], old_capacities.split('  var listeners')[0])

    def test_preview_mounts_only_the_two_repositories(self):
        handler = object.__new__(serve.Handler)
        self.assertEqual(Path(handler.translate_path('/02-model-1-ess-cls-me/me-access.html?bia=2')), ROOT / '02-model-1-ess-cls-me/me-access.html')
        self.assertEqual(Path(handler.translate_path('/inner-compass-nervous-system-organization-gradient/project-map.html')), carry.ENGINE / 'project-map.html')
        for url in ('/../outside', '/%2e%2e/outside', '/.git/config'):
            self.assertEqual(Path(handler.translate_path(url)).name, '.unavailable-preview-path')

if __name__ == '__main__':
    unittest.main()
