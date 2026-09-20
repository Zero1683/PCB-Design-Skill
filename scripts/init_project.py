#!/usr/bin/env python3
"""Create a PCB handoff scaffold without touching an existing project. Python 3.10+."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys


def create_project(output: Path, name: str) -> Path:
    if not name.strip() or '\n' in name or '\r' in name:
        raise ValueError('Project name must be a nonempty single line')
    if output.exists() or output.is_symlink():
        raise ValueError('Output already exists; use the templates manually without overwriting project records')
    templates = Path(__file__).resolve().parents[1] / 'assets'
    mapping = {'PROJECT.template.md': 'PROJECT.md',
               'HANDOFF.template.md': 'HANDOFF.md',
               'CHECKS.template.csv': 'CHECKS.csv'}
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    prepared = {}
    for source, target in mapping.items():
        content = (templates / source).read_text(encoding='utf-8')
        prepared[target] = content.replace('{{PROJECT_NAME}}', name.strip()).replace('{{CREATED_UTC}}', now)
    output = output.absolute()
    output.mkdir(parents=True, exist_ok=False)
    for target, content in prepared.items():
        with (output / target).open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(content)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--name', required=True)
    args = parser.parse_args()
    try:
        created = create_project(args.output, args.name)
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    print(f'Created project records: {created}')
    print('All checks start as NOT_RUN; no PCB or hardware has been validated.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
