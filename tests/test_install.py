import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', SOURCE / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="aidlc project's $ ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.nested = self.root / 'src'
        self.nested.mkdir()

    def config_path(self, agent):
        return self.root / ('.claude/settings.json' if agent == 'claude' else '.codex/hooks.json')

    def run_hook(self, agent, event, data):
        config = json.loads(self.config_path(agent).read_text())
        command = config['hooks'][event][-1]['hooks'][0]['command']
        env = dict(os.environ, CLAUDE_PROJECT_DIR='/unused-claude-project')
        result = subprocess.run(command, shell=True, cwd=self.nested, env=env,
                                input=json.dumps(dict(data, cwd=str(self.nested))),
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        return result.stdout

    def test_install_preserves_settings_and_is_repeatable(self):
        for agent in ('claude', 'codex'):
            with self.subTest(agent=agent):
                path = self.config_path(agent)
                path.parent.mkdir(exist_ok=True)
                original = {'custom': True, 'hooks': {'Stop': [{'hooks': [
                    {'type': 'command', 'command': 'echo existing'}]}]}}
                path.write_text(json.dumps(original))
                self.assertEqual(installer.install(agent, self.nested), self.root)
                first = path.read_text()
                installer.install(agent, self.root)
                self.assertEqual(path.read_text(), first)
                settings = json.loads(first)
                self.assertTrue(settings['custom'])
                self.assertEqual(settings['hooks']['Stop'], original['hooks']['Stop'])
                skills = self.root / ('.claude/skills' if agent == 'claude' else '.agents/skills')
                self.assertEqual(len(list(skills.glob('*/SKILL.md'))), 6)
                for skill in skills.glob('*/SKILL.md'):
                    self.assertEqual('disable-model-invocation: true' in skill.read_text(), agent == 'claude')
                    self.assertIn('allow_implicit_invocation: false',
                                  (skill.parent / 'agents/openai.yaml').read_text())

    def test_legacy_claude_hooks_are_replaced(self):
        path = self.config_path('claude')
        path.parent.mkdir()
        config = {'hooks': {}}
        for event, script in [('UserPromptSubmit', 'lite_audit.py'), ('SessionStart', 'lite_session.py')]:
            group = {'hooks': [{'type': 'command', 'command': 'python',
                               'args': ['${CLAUDE_PROJECT_DIR}/.claude/hooks/' + script], 'timeout': 10}]}
            if event == 'SessionStart':
                group['matcher'] = 'startup|resume|clear|compact'
            config['hooks'][event] = [group]
        path.write_text(json.dumps(config))
        installer.install('claude', self.root)
        installed = json.loads(path.read_text())
        for groups in installed['hooks'].values():
            self.assertEqual(len(groups), 1)
            self.assertIn('.aidlc-lite/hooks/', groups[0]['hooks'][0]['command'])

    def test_invalid_settings_are_not_overwritten(self):
        path = self.config_path('codex')
        path.parent.mkdir()
        path.write_text('invalid JSON')
        with self.assertRaises(ValueError):
            installer.install('codex', self.root)
        self.assertEqual(path.read_text(), 'invalid JSON')
        self.assertFalse((self.root / '.agents/skills').exists())

    def test_both_invocations_log_at_git_root_and_restore_session(self):
        for agent, prefix in [('claude', '/'), ('codex', '$')]:
            with self.subTest(agent=agent):
                installer.install(agent, self.root)
                docs = self.root / 'aidlc-docs'
                if docs.exists():
                    for path in docs.iterdir():
                        path.unlink()
                    docs.rmdir()
                self.assertEqual(self.run_hook(agent, 'SessionStart', {}), '')
                for prompt in ('hello', '$literature', '/literal'):
                    self.assertEqual(self.run_hook(agent, 'UserPromptSubmit', {'prompt': prompt}), '')
                self.assertFalse(docs.exists())
                prompt = prefix + 'lite-0-current'
                self.assertIn('Timestamp:', self.run_hook(agent, 'UserPromptSubmit', {'prompt': prompt}))
                audit = docs / 'audit.md'
                self.assertIn(prompt, audit.read_text())
                self.assertFalse((self.nested / 'aidlc-docs').exists())
                (docs / 'state.md').write_text('**Current Step**: requirements\n'
                    '**Next Step**: design\n**Status**: waiting for approval\n'
                    '- [x] current\n- [ ] requirements\n  - [x] US-01\n')
                output = self.run_hook(agent, 'SessionStart', {'source': 'compact'})
                self.assertIn('requirements', output)
                self.assertIn('waiting for approval', output)
                self.assertIn('1/2', output)
                self.assertIn('1/1', output)
                self.run_hook(agent, 'UserPromptSubmit', {'prompt': 'continue'})
                self.assertIn('continue', audit.read_text())
                before = audit.read_text()
                self.run_hook(agent, 'UserPromptSubmit', {'prompt': '<task-notification>internal'})
                self.assertEqual(audit.read_text(), before)


if __name__ == '__main__':
    unittest.main()
