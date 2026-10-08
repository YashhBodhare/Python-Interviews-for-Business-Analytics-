"""Run every interview example in an isolated subprocess; no network access needed."""
from pathlib import Path
import subprocess
import sys

def main():
    examples = sorted((Path(__file__).parent / 'examples').glob('q*.py'))
    if len(examples) != 50:
        raise RuntimeError(f'Expected 50 examples, found {len(examples)}')
    for path in examples:
        result = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, timeout=30)
        if result.returncode:
            raise RuntimeError(f'{path.name} failed:\n{result.stdout}\n{result.stderr}')
        print(f'{path.name}: PASS')
    print(f'All 50 examples passed on Python {sys.version.split()[0]}.')

if __name__ == '__main__':
    main()
