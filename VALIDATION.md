# Course verification

Verified on **10 October 2026** in the course's local Windows environment.

| Item | Result |
|---|---|
| Python | 3.12.14 |
| NumPy | 2.5.3 |
| Matplotlib | 3.11.2 |
| JupyterLab | 4.6.4 |
| Notebook format validation | All 18 passed |
| Fresh-kernel example and reference-solution runs | All 18 passed |
| Fresh-kernel runs with reference answers in exercise slots | All 18 passed |
| Exercise checks | All 36 passed with reference answers |
| Error outputs in delivered notebooks | None |

The automated validation executed each notebook twice, using 36 fresh kernels. The supplied notebooks retain the verified example outputs and leave learner answer variables set to `None`. Their Pending messages are intentional. Assertions cover numerical results, shapes, dtypes, shared memory, file round trips, matrix reconstruction, FFT reconstruction, and clustering invariants where relevant.

The memory notebook was also rerun successfully after configuring the validation runner to use the native Windows selector event loop. This followed a transient ZeroMQ shutdown message during the initial run; the notebook's calculations and assertions had already passed.

The FFT spectrum, sales dashboard, and PCA cluster plot were visually inspected for readable labels and layout. Random examples use explicit local seeds. Performance timings are observations and have no hardware-dependent pass threshold.

The independent challenges are learner tasks, not precompleted or automatically graded submissions. This validation does not certify arbitrary edits you make later, statistical assumptions for real datasets, or identical random outputs across future package versions.

Reproduce the checks with:

```powershell
.\.venv\Scripts\python.exe tools/verify_course.py
```

The machine-readable results are written to `artifacts/validation/report.json`. Exact installed versions are recorded in `requirements-lock.txt`.
