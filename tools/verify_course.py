"""Execute course notebooks and solution-filled copies in fresh kernels."""
from copy import deepcopy
from pathlib import Path
import argparse
import asyncio
import json
import platform
import sys
import time

import matplotlib
import nbformat
import numpy as np
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def execute(notebook, directory):
    nbformat.validate(notebook)
    NotebookClient(
        notebook, timeout=180, kernel_name='python3',
        resources={'metadata': {'path': str(directory)}},
        allow_errors=False,
    ).execute()
    errors = [output for cell in notebook.cells if cell.cell_type == 'code'
              for output in cell.get('outputs', []) if output.output_type == 'error']
    assert not errors
    return notebook


def main():
    if sys.platform == 'win32' and sys.version_info < (3, 14):
        # Native selector support avoids a background event-loop adapter for ZeroMQ.
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    parser = argparse.ArgumentParser()
    parser.add_argument('--save-outputs', action='store_true',
                        help='Also write verified outputs back to original notebooks.')
    args = parser.parse_args()
    output = ROOT / 'artifacts' / 'validation'
    output.mkdir(parents=True, exist_ok=True)
    results = []
    paths = sorted((ROOT / 'notebooks').glob('*.ipynb'))
    assert len(paths) == 18, f'Expected 18 notebooks, found {len(paths)}'
    for path in paths:
        start = time.perf_counter()
        original = nbformat.read(path, as_version=4)
        exercises = [c for c in original.cells if 'exercise' in c.metadata.get('tags', [])]
        solutions = [c for c in original.cells if 'solution' in c.metadata.get('tags', [])]
        assert len(exercises) == len(solutions) == 2
        executed = execute(deepcopy(original), path.parent)
        nbformat.write(executed, output / path.name)
        if args.save_outputs:
            nbformat.write(executed, path)
        answered = deepcopy(original)
        answer_cells = [c for c in answered.cells if 'exercise' in c.metadata.get('tags', [])]
        for exercise, solution in zip(answer_cells, solutions):
            first_line = solution.source.splitlines()[0]
            reference_name, expression = first_line.split(' = ', 1)
            variable = reference_name.removeprefix('reference_')
            placeholder = f'{variable} = None  # TODO: replace None with your answer'
            # Preserve setup and intentionally replace learner answers only in the in-memory copy.
            lines = exercise.source.splitlines()
            matching = [i for i, line in enumerate(lines) if line.startswith(f'{variable} = ')]
            if not matching:
                raise ValueError(f'Cannot locate answer variable {variable} in {path.name}')
            if placeholder in exercise.source:
                exercise.source = exercise.source.replace(placeholder, f'{variable} = {expression}')
            else:
                # For edited/multiline answers, retain the user's setup and append the reference answer.
                exercise.source += f'\n{variable} = {expression}'
        execute(answered, path.parent)
        check_outputs = '\n'.join(
            o.get('text', '') for c in answered.cells
            if 'exercise-check' in c.metadata.get('tags', []) for o in c.get('outputs', [])
        )
        assert 'Exercise 1 passed!' in check_outputs and 'Exercise 2 passed!' in check_outputs
        entry = dict(notebook=path.name, code_cells=sum(c.cell_type == 'code' for c in original.cells),
                     exercises=2, status='passed', seconds=round(time.perf_counter() - start, 2))
        results.append(entry)
        print(f'PASS {path.name} (examples + both exercise checks)', flush=True)
    report = dict(python=platform.python_version(), numpy=np.__version__, matplotlib=matplotlib.__version__,
                  notebooks=len(results), exercises=sum(r['exercises'] for r in results),
                  kernel_executions=len(results) * 2, results=results)
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'results'}, indent=2))


if __name__ == '__main__':
    main()
