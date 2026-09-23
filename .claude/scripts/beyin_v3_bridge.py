#!/usr/bin/env python3
"""Explicitly scoped global lifecycle bridge for Codex and other local harnesses."""
import argparse
import base64
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

sys.dont_write_bytecode = True
EVENTS = ('SessionStart', 'UserPromptSubmit', 'PostToolUse', 'Stop', 'PreCompact', 'SessionEnd')
CONTEXT_EVENTS = ('SessionStart', 'UserPromptSubmit')


def working_directory(payload, harness):
    value = payload.get('cwd')
    if value is None:
        value = os.environ.get('CLAUDE_PROJECT_DIR') if harness == 'claude' else None
    if value is None:
        value = os.getcwd()
    if not isinstance(value, str) or not value or not Path(value).is_absolute():
        return None
    return Path(value).resolve()


def origin(payload, harness):
    cwd = working_directory(payload, harness)
    if cwd is None:
        return {}
    name = ''.join(c for c in cwd.name if c.isalnum() or c in ' ._-')[:80] or 'project'
    from beyin_v3_projects import project_id
    return dict(project=name, project_id=project_id(cwd))


def _hook_result(vault, state, harness, payload, metadata_only=False):
    """Run the existing V3 hook in-process and return its JSON response."""
    from beyin_v3_hook import main as hook_main
    previous_argv, previous_stdin = sys.argv, sys.stdin
    output = io.StringIO()
    try:
        sys.argv = ['beyin_v3_hook.py', '--vault', str(vault), '--state', str(state),
                    '--harness', harness] + (['--metadata-only'] if metadata_only else [])
        sys.stdin = io.StringIO(json.dumps(payload))
        with contextlib.redirect_stdout(output):
            hook_main()
    finally:
        sys.argv, sys.stdin = previous_argv, previous_stdin
    try:
        value = json.loads(output.getvalue().strip() or '{}')
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def _merge_context(result, harness, event, text):
    if not text or event not in CONTEXT_EVENTS:
        return result
    if harness == 'antigravity':
        steps = result.setdefault('injectSteps', [])
        steps.insert(0, {'ephemeralMessage': text})
        return result
    hook = result.setdefault('hookSpecificOutput', {})
    hook['hookEventName'] = event
    existing = hook.get('additionalContext', '')
    hook['additionalContext'] = text + ('\n' + existing if existing else '')
    return result


def shell_command(argv):
    if any(any(c in str(value) for c in '\r\n\x00') for value in argv):
        raise ValueError('Unsupported command path')
    if os.name != 'nt':
        return shlex.join(map(str, argv))
    script = '& ' + ' '.join("'" + str(v).replace("'", "''") + "'" for v in argv) + '; exit $LASTEXITCODE'
    encoded = base64.b64encode(script.encode('utf-16le')).decode()
    system = Path(os.environ.get('SYSTEMROOT') or os.environ.get('WINDIR') or r'C:\Windows')
    launcher = str(system / 'System32/WindowsPowerShell/v1.0/powershell.exe').replace('\\', '/')
    return subprocess.list2cmdline([launcher]) + ' -NoProfile -NonInteractive -EncodedCommand ' + encoded


def main(argv=None):
    if hasattr(sys.stdin, 'reconfigure'):
        sys.stdin.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--state', type=Path, help='Defaults to the installed vault runtime locator')
    parser.add_argument('--harness', choices=('claude', 'codex'), required=True)
    parser.add_argument('--project-root', type=Path, action='append')
    parser.add_argument('--all-local-roots', action='store_true',
                        help='Allow explicitly opened projects on every mounted local filesystem')
    parser.add_argument('--context-chars', type=int, default=5000, help='Maximum external-project context; 0 keeps time only')
    parser.add_argument('--event', choices=EVENTS, action='append', help='Allowed events; default all lifecycle events')
    parser.add_argument('--print-config', action='store_true', help='Print hook groups to merge into global JSON; changes nothing')
    args = parser.parse_args(argv)
    try:
        vault = args.vault.expanduser().resolve()
        if not vault.is_dir() or not 0 <= args.context_chars <= 12000:
            raise ValueError('Invalid vault or context budget')
        state = args.state or Path(json.loads((vault / '.beyin-runtime.json').read_text(encoding='utf-8'))['state'])
        if not state.is_absolute():
            raise ValueError('Runtime state must be absolute')
        state = state.resolve()
        if state.is_relative_to(vault):
            raise ValueError('Runtime state must be outside vault')
        from beyin_v3_projects import local_project_roots
        roots = [p.expanduser().resolve() for p in (args.project_root or [])]
        if args.all_local_roots:
            roots.extend(local_project_roots())
        roots = list(dict.fromkeys(roots))
        if not roots:
            raise ValueError('At least one project root is required')
        if any(not p.is_dir() for p in roots):
            raise ValueError('Project roots must exist')
        events = list(dict.fromkeys(args.event or EVENTS))
        if args.print_config:
            command = [sys.executable, str(Path(__file__).resolve()), '--vault', str(vault),
                       '--state', str(state), '--harness', args.harness, '--context-chars', str(args.context_chars)]
            if args.all_local_roots:
                command.append('--all-local-roots')
            for root in roots:
                command.extend(['--project-root', str(root)])
            for event in events:
                command.extend(['--event', event])
            shell = shell_command(command)
            groups = {}
            for event in events:
                group = {'hooks': [{'type': 'command', 'command': shell,
                                    'timeout': 3 if event == 'SessionEnd' else 20}]}
                if event == 'PostToolUse':
                    group['matcher'] = 'Edit|Write|apply_patch'
                groups[event] = [group]
            print(json.dumps({'hooks': groups}, indent=2))
            return 0
        payload = json.loads(sys.stdin.read(1_000_000) or '{}')
        if not isinstance(payload, dict):
            raise ValueError('Invalid hook payload')
        event = payload.get('hook_event_name')
        if event not in events or os.environ.get('BEYIN_V3_INTERNAL'):
            print('{}'); return 0
        cwd = working_directory(payload, args.harness)
        from beyin_v3_projects import eligible, external_context, local_time_context, register_project
        clock = local_time_context() if event in CONTEXT_EVENTS else ''
        # An explicit no-memory request disables storage and retrieval, but the
        # ephemeral current-time context remains useful and stores no prompt.
        if payload.get('no_memory') is True:
            from beyin_v3_hook import output_context
            print(json.dumps(output_context(args.harness, event, clock)) if clock else '{}')
            return 0
        valid_session = isinstance(payload.get('session_id'), str) and payload['session_id'] not in ('', 'unknown')
        if cwd is not None and cwd.is_relative_to(vault):
            result = _hook_result(vault, state, args.harness, payload) if valid_session else {}
            print(json.dumps(_merge_context(result, args.harness, event, clock)))
            return 0
        if not eligible(cwd, vault, roots):
            from beyin_v3_hook import output_context
            print(json.dumps(output_context(args.harness, event, clock)) if clock else '{}')
            return 0
        if not valid_session:
            from beyin_v3_hook import output_context
            warning = clock + '\nSecond Brain could not register this project because the host supplied no stable session id.'
            print(json.dumps(output_context(args.harness, event, warning)) if event in CONTEXT_EVENTS else '{}')
            return 0
        from beyin_v3_preferences import read
        settings = read(vault)
        if not settings['auto_sync']:
            from beyin_v3_hook import output_context
            notice = clock + '\nSecond Brain automatic sync is paused by preference.'
            print(json.dumps(output_context(args.harness, event, notice)) if event in CONTEXT_EVENTS else '{}')
            return 0
        # Stable per-project session namespace prevents identical session IDs in
        # two external projects from satisfying each other's receipt checkpoints.
        payload['cwd'] = str(cwd)
        payload['session_id'] = json.dumps([str(cwd), payload.get('session_id', 'unknown')])
        if payload.get('event_id'):
            payload['event_id'] = json.dumps([args.harness, str(cwd), event, payload['event_id']])
        session = hashlib.sha256(payload['session_id'].encode()).hexdigest()[:24]
        result = _hook_result(vault, state, args.harness, payload, metadata_only=True)
        if event not in CONTEXT_EVENTS:
            print(json.dumps(result)); return 0
        try:
            registration = register_project(vault, state, cwd)
            memory = '' if settings['context_mode'] == 'off' else external_context(
                vault, state, registration, args.harness, session, payload.get('prompt', ''), args.context_chars)
            text = clock + ('\n' + memory if memory else '')
        except Exception as exc:
            # The host stays usable, while the injected warning and hook-error file
            # make registration failures visible rather than silently losing memory.
            from beyin_v3_hook import atomic
            atomic(state / 'hook-error.json', {'at': __import__('time').time(),
                                                'error': type(exc).__name__,
                                                'component': 'project-registration'})
            text = clock + '\nSecond Brain project registration failed; run the local brain doctor before trusting continuity.'
        print(json.dumps(_merge_context(result, args.harness, event, text)))
        return 0
    except Exception:
        if args.print_config:
            print('Bridge configuration invalid; verify paths and budget.', file=sys.stderr)
            return 1
        print('{}')  # Never block the host or expose a path/payload in an error.
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
