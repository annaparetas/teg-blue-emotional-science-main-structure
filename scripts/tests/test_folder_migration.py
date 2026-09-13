"""New working names and old bookmarks must reach the same repository owners."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

serve = load('serve')
carry = load('carry')
connections = load('build-engine-connections')

class FolderMigration(unittest.TestCase):
    def test_historical_framework_connections_survive_folder_rename(self):
        migration = json.loads((connections.ENGINE / 'development/registers/framework-identifier-migration.json').read_text())
        rows = connections.relationships(connections.engine_files())
        moves = [move for move in migration['paths'] if move['repo'] in connections.ENGINE_NAMES]
        self.assertTrue(moves)
        for move in moves:
            with self.subTest(source=move['old']):
                self.assertIn(move['old'], rows)
                self.assertEqual(rows[move['old']][0], rows[move['new']][0])

    def test_new_and_legacy_mounts(self):
        handler = object.__new__(serve.Handler)
        for name in serve.ENGINE_NAMES:
            self.assertEqual(Path(handler.translate_path('/' + name + '/project-map.html')), carry.ENGINE / 'project-map.html')
        for name in serve.SITE_NAMES:
            self.assertEqual(Path(handler.translate_path('/' + name + '/index.html')), ROOT / 'index.html')

    def test_new_and_legacy_carry_links_preserve_query_and_anchor(self):
        for name in serve.SITE_NAMES:
            self.assertEqual(carry.rewrite('../../../' + name + '/02-model-1-ess-cls-me/me-access.html?bia=1#bodily-access', 'models/01-information-systems', '02-model-1-ess-cls-me'), 'me-access.html?bia=1#bodily-access')

    def test_aliases_do_not_open_other_folders_or_git_metadata(self):
        handler = object.__new__(serve.Handler)
        for name in serve.SITE_NAMES + serve.ENGINE_NAMES:
            for suffix in ('/%2e%2e/outside', '/.git/config'):
                self.assertEqual(Path(handler.translate_path('/' + name + suffix)).name, '.unavailable-preview-path')

if __name__ == '__main__':
    unittest.main()
