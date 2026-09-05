"""Presentation must survive carry without changing provenance or active routes."""
import importlib.util
from pathlib import Path
import sys
import unittest
import tempfile
from unittest.mock import patch
import contextlib, io
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import presentation

class PresentationBoundary(unittest.TestCase):
    def test_gradient_table_is_active_despite_legacy_anchor_handler(self):
        path='03-model-2-gradient/positions.html'
        self.assertTrue(presentation.active(path,(ROOT/path).read_text()))

    def test_compatibility_and_history_remain_untouched(self):
        for path in ['02-model-1-ess-cls-me/access.html','02-model-1-ess-cls-me/notes/sources/relational-capacities.html','archive/pre-numbered-main-structure-2026-09-04/index.html']:
            text=(ROOT/path).read_text()
            self.assertEqual(text,presentation.attach(text,path))

    def test_repeat_import_does_not_duplicate_presentation(self):
        path='04-model-3-esc/cycle.html'
        text=(ROOT/path).read_text()
        first=presentation.attach(text,path)
        self.assertEqual(first,presentation.attach(first,path))
        self.assertEqual(first.count('<!-- Site presentation -->'),1)
        self.assertIn('presentation/theme.css',first)

    def test_carry_applies_presentation_without_graduating_source(self):
        spec=importlib.util.spec_from_file_location('carry',ROOT/'scripts/carry.py')
        carry=importlib.util.module_from_spec(spec);spec.loader.exec_module(carry)
        path='05-frameworks/F01/timeline.html'
        source='<html><head><style>body { background: white; }</style></head><body><h1 id="source">Working account</h1></body></html>'
        ownership=dict(carry.GRADUATED_SITE_FILES)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with patch.object(carry,'ROOT',root), patch.object(presentation,'ROOT',root), patch.object(carry,'MANIFEST',[(path,path,None,None,None)]), patch.object(carry,'source_text',return_value=source), patch.object(sys,'argv',['carry.py',path]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(carry.main(),0)
            output=(root/path).read_text()
            self.assertIn('presentation/theme.css',output)
            self.assertIn('<h1 id="source">Working account</h1>',output)
            self.assertTrue((root/'assets/presentation/05-frameworks--F01--timeline.css').exists())
        self.assertEqual(ownership,carry.GRADUATED_SITE_FILES)
