"""Install shared AI-DLC Lite skills and hooks into a Git project."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def install(agent: str, target: Path) -> Path:
    source = Path(__file__).resolve().parent
    root = Path(subprocess.check_output(
        ['git', '-C', str(target), 'rev-parse', '--show-toplevel'], text=True
    ).strip())
    config_path = root / ('.claude/settings.json' if agent == 'claude' else '.codex/hooks.json')
    settings = json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {}
    hooks = settings.setdefault('hooks', {})
    incoming = json.loads((source / 'config' / (agent + '.json')).read_text(encoding='utf-8'))
    for event, groups in incoming['hooks'].items():
        existing = hooks.setdefault(event, [])
        if agent == 'claude':
            script = 'lite_audit.py' if event == 'UserPromptSubmit' else 'lite_session.py'
            legacy = {'type': 'command', 'command': 'python',
                      'args': ['${CLAUDE_PROJECT_DIR}/.claude/hooks/' + script], 'timeout': 10}
            for group in existing:
                group['hooks'] = [groups[0]['hooks'][0] if hook == legacy else hook
                                  for hook in group['hooks']]
        for group in groups:
            if group not in existing:
                existing.append(group)

    skills = root / ('.claude/skills' if agent == 'claude' else '.agents/skills')
    for skill in (source / 'skills').iterdir():
        if not skill.is_dir():
            continue
        destination = skills / skill.name
        shutil.copytree(skill, destination, dirs_exist_ok=True)
        if agent == 'claude':
            path = destination / 'SKILL.md'
            text = path.read_text(encoding='utf-8')
            path.write_text(text.replace('---\n', '---\ndisable-model-invocation: true\n', 1), encoding='utf-8')
    shutil.copytree(source / 'hooks', root / '.aidlc-lite/hooks', dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    config_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = config_path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(config_path)
    return root


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('agent', choices=['claude', 'codex'])
    parser.add_argument('target', type=Path, help='Target Git project (or a subdirectory)')
    args = parser.parse_args()
    try:
        root = install(args.agent, args.target)
    except (OSError, ValueError, TypeError, AttributeError, subprocess.CalledProcessError) as error:
        parser.exit(1, 'Installation failed: ' + str(error) + '\n')
    print('Installed AI-DLC Lite for ' + args.agent + ' in ' + str(root))
    print('Add AGENTS-snippet.md to the project instructions. Restart the agent.')
    if args.agent == 'codex':
        print('Review and trust the installed hooks with /hooks before use.')
