# Learn NumPy by doing

An 18-notebook course that progresses from your first array to advanced numerical work. Each notebook contains three explained examples, experiments to try, two exercises with automatic checks, reference solutions, and an independent challenge. All data is generated locally: no dataset downloads or accounts are needed.

## Start here on this computer

A local Python environment is provided in `.venv`. Open PowerShell in this folder and run:

```powershell
.\.venv\Scripts\python.exe -m jupyterlab notebooks/00_start_here.ipynb
```

You can also double-click **`Start Learning.cmd`**. Keep its terminal window open while using JupyterLab; press **Ctrl+C** in that window when you want to stop the server.

In JupyterLab, click a code cell and press **Shift+Enter**. Begin with notebook 00 and follow the **Next** links. Use the file browser to open another notebook if a navigation link does not open in your editor. The initial notebooks include a short Python refresher; no previous NumPy knowledge is assumed.

In VS Code, open this folder, open a notebook, and choose `.venv\Scripts\python.exe` as its Python kernel. The Python and Jupyter extensions must be installed to run notebooks there.

## Learning path

| Order | Notebook | What you will practice |
|---|---|---|
| 00 | [Start here](notebooks/00_start_here.ipynb) | Cells, Python basics, errors, and assertions |
| 01 | [Arrays and dtypes](notebooks/01_arrays_and_dtypes.ipynb) | Constructors, dimensions, shapes, numeric types |
| 02 | [Indexing and filtering](notebooks/02_indexing_and_filtering.ipynb) | Slices, masks, paired versus rectangular selection |
| 03 | [Shapes and axes](notebooks/03_shapes_and_axes.ipynb) | Reshape, transpose, reduction axes, stack and concatenate |
| 04 | [Math and ufuncs](notebooks/04_math_and_ufuncs.ipynb) | Elementwise math, clipping, conditional and safe calculations |
| 05 | [Broadcasting](notebooks/05_broadcasting.ipynb) | Shape rules, centering, pairwise calculations |
| 06 | [Statistics](notebooks/06_statistics_and_aggregation.ipynb) | Spread, percentiles, weighted and cumulative metrics |
| 07 | [Randomness and simulation](notebooks/07_randomness_and_simulation.ipynb) | Generators, Monte Carlo, bootstrap sampling |
| 08 | [Cleaning and file I/O](notebooks/08_cleaning_and_file_io.ipynb) | Missing values, imputation, CSV, NPY and NPZ |
| 09 | [Sorting, searching, grouping](notebooks/09_sorting_searching_grouping.ipynb) | Ranking, insertion positions, grouped reductions |
| 10 | [Linear algebra](notebooks/10_linear_algebra.ipynb) | Matrix multiplication, solving systems, least squares, SVD |
| 11 | [Copies, views, memory](notebooks/11_copies_views_and_memory.ipynb) | Shared buffers, strides, contiguity, memory mapping |
| 12 | [Vectorization and performance](notebooks/12_vectorization_and_performance.ipynb) | Correctness comparisons, timings, buffers, chunking |
| 13 | [Numerical stability](notebooks/13_numerical_stability.ipynb) | Floating point tolerances, overflow, stable softmax |
| 14 | [Advanced array patterns](notebooks/14_advanced_array_patterns.ipynb) | Einsum, overlapping windows, repeated-index accumulation |
| 15 | [Signal processing](notebooks/15_signal_processing_with_fft.ipynb) | FFT frequencies, spectra, filtering, reconstruction |
| 16 | [Sales analysis project](notebooks/16_project_sales_analysis.ipynb) | A complete cleaning, analysis, visualization and export workflow |
| 17 | [PCA and clustering project](notebooks/17_project_pca_and_clustering.ipynb) | Standardization, dimensionality reduction, iterative clustering |

## A practical study routine

Spend roughly 30–50 minutes per topic and 60–90 minutes per project. Allow extra sessions for the independent challenges. These are estimates, not deadlines.

1. **Predict:** write down the output shape and a few expected values.
2. **Run:** execute the example and read its output.
3. **Change:** do the Try it experiment and explain what changed.
4. **Solve:** replace each exercise's `None` with your answer and rerun its check.
5. **Reflect:** complete the challenge, explain the main idea, and test a changed input.

Untouched exercises print **Pending**. This allows a complete reference run without pretending that the exercises are solved. The reference solutions at the end use separate variables and do not fill in your answers. Their source may be collapsed in JupyterLab; expand it when ready. Each solution includes a check and a short explanation.

Use **Kernel → Restart Kernel and Run All Cells** after finishing a notebook. A fresh kernel reveals missing imports and accidental dependence on out-of-order execution. Every notebook is independent and can start with a fresh kernel.

Suggested milestones:

- After 00–04: create a score table, select rows, and calculate totals unaided.
- After 05–09: clean a numeric dataset and produce grouped summaries.
- After 10–15: explain correctness, numerical accuracy, shape, and memory tradeoffs.
- After 16–17: complete both project extensions and explain their assumptions.

This course provides beginner-to-advanced coverage with expert practice topics. Expertise develops through repeated work on unfamiliar problems. More specialized areas such as NumPy's C API, custom dtypes, and distributed or GPU computing are outside its scope.

## Setup on another computer

Install Python 3.12 or newer. In PowerShell, from the course directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab notebooks/00_start_here.ipynb
```

If you use a different supported Python version, adjust the `py` selector. With `uv` installed, you can instead run:

```powershell
uv venv --python 3.12 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

`requirements.txt` lists compatible version ranges; `requirements-lock.txt` records the exact package versions used for the verified run. The lock includes Windows-specific dependencies; use the general requirements file on other operating systems.

The CSV, binary-save, and memory-mapping demonstrations use temporary directories and clean up automatically. To keep your own exports, choose an explicit directory such as `my_results` and create it with `Path(...).mkdir(exist_ok=True)`.

## Troubleshooting

| Symptom | What to do |
|---|---|
| `python` opens the Microsoft Store | Use `.\.venv\Scripts\python.exe` as shown above. |
| `ModuleNotFoundError: numpy` | Select this folder's `.venv` kernel or install requirements into the selected environment. |
| `NameError` for a variable | Restart the kernel, then run the notebook from the top. |
| A shape or broadcasting error | Print each input's `.shape` and align dimensions from the right. |
| An exercise says Pending | Replace its `None`, rerun the answer cell, then the check cell. |
| An assertion fails | Compare expected and actual values, shape, dtype, and floating point tolerance. |
| A plot does not appear | Run all preceding cells and confirm the Matplotlib dependency is installed. |

## Verification and course maintenance

The supplied notebooks include outputs from execution in fresh Jupyter kernels. See [VALIDATION.md](VALIDATION.md) for the actual verified environment and results.

To recheck all notebooks without changing your saved work:

```powershell
.\.venv\Scripts\python.exe tools/verify_course.py
```

Executed verification copies and a machine-readable report go in `artifacts/validation/`. The validator also runs copies with reference answers inserted into the exercise slots, ensuring that exercise check cells work. It does not claim to validate your independent challenge submissions.

`tools/build_course.py` contains the original course source. **Running it overwrites the notebooks, including your edits.** Save your own work separately before rebuilding. It is not needed for learning.

## Official references

The course uses original examples and links to the relevant NumPy documentation in each notebook. Useful starting points are the [NumPy beginner guide](https://numpy.org/doc/stable/user/absolute_beginners.html), [broadcasting guide](https://numpy.org/doc/stable/user/basics.broadcasting.html), [copies and views guide](https://numpy.org/doc/stable/user/basics.copies.html), and [random Generator reference](https://numpy.org/doc/stable/reference/random/generator.html).
