"""Rebuild the original course. This overwrites notebooks: save your work first."""
from pathlib import Path
import textwrap
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'notebooks'
OUT.mkdir(exist_ok=True)
lessons = []

def clean(text):
    return textwrap.dedent(text).strip()

def lesson(slug, title, level, goals, prerequisites, sections, exercises, challenge, references):
    lessons.append(dict(slug=slug, title=title, level=level, goals=goals,
                        prerequisites=prerequisites, sections=sections,
                        exercises=exercises, challenge=challenge, references=references))

# A section is (title, explanation, executable example, experiment).
# An exercise is (task, setup, learner variable, check, reference solution).
lesson('00_start_here', 'Start here: Jupyter and the Python you need', 'Beginner',
       'Run cells, read errors, use Python lists and functions, and check an answer.', 'None.', [
('Your first notebook', '''A notebook mixes text cells with code cells. Click a code cell and press **Shift+Enter** to run it and move on. The number beside a cell records execution order. Variables live in the kernel (the running Python process), so run from top to bottom. Use **Kernel → Restart Kernel and Run All Cells** to check that your work does not depend on old variables.

Start by predicting each printed value. Run the cell, change one input, and explain the new output. An `assert` is a check: no error means the condition passed.''',
'''name = "NumPy learner"
minutes_per_day = 30
days = 5
print(f"Hello, {name}!")
print("Weekly practice minutes:", minutes_per_day * days)
assert minutes_per_day * days == 150''', 'Change days to 7 and update the expected value in the assertion.'),
('Lists, loops, and functions', '''A list stores a sequence. Indexing begins at zero. A `for` loop repeats work. A function gives a reusable name to a calculation; `return` sends its result back. Indentation is part of Python syntax.''',
'''prices = [10, 20, 30]
print("First price:", prices[0])
discounted = [price * 0.9 for price in prices]
def total_with_tax(values, tax_rate=0.05):
    return sum(values) * (1 + tax_rate)
print(discounted)
print(total_with_tax(prices))''', 'Call the function with tax_rate=0.10. Explain what changed.'),
('Meet NumPy and read an error', '''NumPy provides arrays for numerical calculations. The usual import name is `np`. Here, multiplying an array changes every value. Multiplying a Python list repeats its contents. Errors are learning tools: read the last line first. We catch this intentional error so Run All still works.''',
'''values = np.array([10, 20, 30])
print("List:", [10, 20, 30] * 2)
print("Array:", values * 2)
try:
    print(values[99])
except IndexError as error:
    print("Intentional indexing error:", error)
np.testing.assert_array_equal(values * 2, [20, 40, 60])''', 'Replace index 99 with 2. What is the largest valid positive index?')], [
('Calculate the total minutes for 25 minutes per day over 6 days.', '', 'practice_minutes', 'assert practice_minutes == 150', '25 * 6'),
('Convert temperatures [0, 10, 20] from Celsius to Fahrenheit using F = C * 9/5 + 32.', 'celsius = np.array([0., 10., 20.])', 'fahrenheit', 'np.testing.assert_allclose(fahrenheit, [32, 50, 68])', 'celsius * 9 / 5 + 32')],
'Write a Python function that accepts a NumPy array of minutes and returns hours. Check it on [30, 60, 90].',
['https://numpy.org/doc/stable/user/absolute_beginners.html'])

lesson('01_arrays_and_dtypes', 'Create arrays and understand data types', 'Beginner',
       'Create arrays; inspect shape, dimensions, size, and dtype; choose numeric storage.', 'Notebook 00.', [
('Read the shape', '''An array is a rectangular collection of values with one dtype. `shape` gives the length of each axis, `ndim` counts axes, and `size` counts all elements. For a table, axis 0 runs through rows and axis 1 through columns.''',
'''sales = np.array([[12, 15, 18], [20, 22, 25]], dtype=np.int64)
print(sales)
print("shape:", sales.shape, "ndim:", sales.ndim, "size:", sales.size)
print("dtype:", sales.dtype, "bytes:", sales.nbytes)
assert sales.shape == (2, 3)
assert sales.size == 6''', 'Add one complete row. Predict shape and size before running.'),
('Choose a constructor', '''`arange(start, stop, step)` excludes stop. `linspace(start, stop, num)` includes both endpoints by default and is convenient for floating point grids. `zeros`, `ones`, and `full` create known initial values. `empty` allocates uninitialized numerical storage: fill every entry before reading it.''',
'''print("Even numbers:", np.arange(0, 10, 2))
print("Five points:", np.linspace(0, 1, 5))
print("Zeros:\\n", np.zeros((2, 3)))
print("Full:\\n", np.full((2, 2), 7))
buffer = np.empty(3)
buffer[:] = 4.5
print("Filled buffer:", buffer)''', 'Create seven evenly spaced points from -3 to 3.'),
('Dtype affects results', '''Integers cannot store a fractional part. Converting floats to integers truncates toward zero. Small integer types have limited ranges; inspect `iinfo` before choosing one. Use explicit floating point arrays when your calculation needs fractions.''',
'''prices = np.array([1, 2, 3], dtype=np.int64)
prices[0] = 1.9
print("After integer assignment:", prices)
floating = prices.astype(np.float64)
floating[0] = 1.9
print("Floating version:", floating)
print("int8 limits:", np.iinfo(np.int8).min, np.iinfo(np.int8).max)
assert floating.dtype == np.float64''', 'Compare nbytes for 1,000 values stored as float32 and float64.')], [
('Create a 3-row, 4-column array filled with 2.5, using float64.', '', 'filled', 'assert filled.shape == (3, 4)\nassert filled.dtype == np.float64\nnp.testing.assert_allclose(filled, 2.5)', 'np.full((3, 4), 2.5, dtype=np.float64)'),
('Create an integer array containing 5, 10, 15, 20, 25.', '', 'multiples', 'np.testing.assert_array_equal(multiples, [5, 10, 15, 20, 25])\nassert np.issubdtype(multiples.dtype, np.integer)', 'np.arange(5, 26, 5)')],
'Represent the scores of 4 students in 3 subjects. Print a sentence explaining each dimension and compute the storage in bytes.',
['https://numpy.org/doc/stable/user/basics.creation.html', 'https://numpy.org/doc/stable/user/basics.types.html'])

lesson('02_indexing_and_filtering', 'Select, slice, and filter data', 'Beginner',
       'Select individual values, slice tables, and combine Boolean conditions.', 'Notebooks 00–01.', [
('Indexing and slicing', '''Use `a[row, column]` for a 2D array. A slice is `start:stop:step`; stop is excluded. A missing start or stop means the boundary. Negative indices count from the end. A single integer removes an axis; a slice preserves it.''',
'''scores = np.array([[65, 80, 90], [75, 60, 85], [95, 88, 92], [50, 70, 68]])
print("Last student's last score:", scores[-1, -1])
print("First two students:\\n", scores[:2])
print("Second subject:", scores[:, 1])
print("Shapes:", scores[:, 1].shape, scores[:, 1:2].shape)
print("Every other student:\\n", scores[::2])''', 'Select the last two students and the first two subjects.'),
('Boolean masks', '''A comparison creates a Boolean array. A mask chooses entries where it is True. Combine array conditions with `&` (and), `|` (or), and `~` (not), and put each comparison in parentheses. Python `and` cannot combine elementwise array conditions.''',
'''marks = np.array([45, 62, 78, 90, 55, 84])
mask = (marks >= 60) & (marks < 85)
print("Mask:", mask)
print("Selected:", marks[mask])
print("Positions:", np.flatnonzero(mask))
assert np.count_nonzero(mask) == 3''', 'Select marks below 50 or at least 85.'),
('Choose rows and columns carefully', '''Two integer index arrays select paired coordinates. To select every combination of some rows and columns, use `np.ix_`. Assign through one indexing expression to change the original array. Later we will study copies and views in detail.''',
'''table = np.arange(12).reshape(3, 4)
print(table)
print("Paired:", table[[0, 2], [1, 3]])
print("Rectangle:\\n", table[np.ix_([0, 2], [1, 3])])
adjusted = table.copy()
adjusted[adjusted < 4] = -1
print("Adjusted:\\n", adjusted)''', 'Select the middle row in reverse order.')], [
('Select all rows and the last two columns of grid.', 'grid = np.arange(20).reshape(4, 5)', 'last_columns', 'np.testing.assert_array_equal(last_columns, [[3, 4], [8, 9], [13, 14], [18, 19]])', 'grid[:, -2:]'),
('Keep prices that are at least 100 and at most 300.', 'prices = np.array([80, 100, 150, 300, 450])', 'affordable', 'np.testing.assert_array_equal(affordable, [100, 150, 300])', 'prices[(prices >= 100) & (prices <= 300)]')],
'Create a 5×3 score table. Select students whose first subject is at least 70, then set every score below 40 to 40 on a copy.',
['https://numpy.org/doc/stable/user/basics.indexing.html'])

lesson('03_shapes_and_axes', 'Reshape, combine, and understand axes', 'Beginner',
       'Reshape without changing element count; transpose; join and split arrays.', 'Notebooks 00–02.', [
('Reshape preserves the number of values', '''A shape is a contract about how values are arranged. `reshape` does not add or remove values. One dimension may be -1: NumPy calculates its length from the others. A 1D vector has no separate row and column axes; use a new axis when you need a column.''',
'''values = np.arange(12)
table = values.reshape(3, 4)
print(table)
print("Infer columns:\\n", values.reshape(2, -1))
print("Column shape:", values[:, None].shape)
print("Row shape:", values[None, :].shape)
assert table.size == values.size''', 'Try reshape(5, -1) inside a try/except and explain the failure.'),
('Transpose and reductions', '''Transpose rearranges axes. For a 2D table, `.T` exchanges rows and columns. A reduction collapses the axis you name: for shape (students, subjects), summing axis 0 gives one result per subject. Summing axis 1 gives one result per student.''',
'''points = np.array([[1, 2, 3], [4, 5, 6]])
print("Transposed:\\n", points.T)
print("Per-column totals:", points.sum(axis=0))
print("Per-row totals:", points.sum(axis=1))
print("Keep the reduced axis:", points.sum(axis=1, keepdims=True).shape)
np.testing.assert_array_equal(points.sum(axis=0), [5, 7, 9])''', 'Draw a 2×3 grid and label which entries contribute to each total.'),
('Concatenate versus stack', '''`concatenate` joins along an existing axis, so other axis lengths must match. `stack` adds a new axis and requires equal input shapes. `array_split` can divide into uneven pieces; `split` requires equal pieces when given an integer count.''',
'''a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("Concatenate:", np.concatenate([a, b]))
print("Stack rows:\\n", np.stack([a, b], axis=0))
print("Stack columns:\\n", np.stack([a, b], axis=1))
print("Uneven pieces:", np.array_split(np.arange(7), 3))''', 'Stack three length-4 arrays. Predict the shape for axis=0 and axis=1.')], [
('Reshape readings into 2 days × 3 sensors × 4 measurements.', 'readings = np.arange(24)', 'cube', 'assert cube.shape == (2, 3, 4)\nnp.testing.assert_array_equal(cube.ravel(), readings)', 'readings.reshape(2, 3, 4)'),
('Compute one total per row, retaining shape (3, 1).', 'counts = np.array([[1, 2], [3, 4], [5, 6]])', 'row_totals', 'assert row_totals.shape == (3, 1)\nnp.testing.assert_array_equal(row_totals, [[3], [7], [11]])', 'counts.sum(axis=1, keepdims=True)')],
'Create an array shaped (2 stores, 7 days, 3 products). Compute totals per store, per day, and per product, explaining each axis tuple.',
['https://numpy.org/doc/stable/reference/routines.array-manipulation.html'])

lesson('04_math_and_ufuncs', 'Array arithmetic and universal functions', 'Beginner',
       'Calculate elementwise, use ufuncs, and handle division deliberately.', 'Notebooks 00–03.', [
('Elementwise calculations', '''Operations such as +, -, *, / and ** apply to corresponding entries. Universal functions (ufuncs) such as `sqrt`, `exp`, and `log` also operate elementwise. `*` is elementwise multiplication; matrix multiplication uses `@` in a later notebook.''',
'''quantity = np.array([2, 3, 1])
price = np.array([50., 20., 100.])
revenue = quantity * price
print("Revenue by product:", revenue)
print("Total:", revenue.sum())
print("Square roots:", np.sqrt([1., 4., 9.]))
np.testing.assert_allclose(np.log(np.exp([0., 1., 2.])), [0, 1, 2])''', 'Apply a 10% discount to all prices before calculating revenue.'),
('Conditions and clipping', '''`where(condition, yes, no)` chooses an output per element. `clip` limits values to an interval. The arguments to `where` are evaluated before selection; it does not prevent an invalid calculation inside an argument.''',
'''scores = np.array([-5, 45, 75, 110])
bounded = np.clip(scores, 0, 100)
labels = np.where(bounded >= 60, "pass", "retry")
print(bounded)
print(labels)
np.testing.assert_array_equal(bounded, [0, 45, 75, 100])''', 'Create three labels using np.select: below 50, 50–79, and at least 80.'),
('Safe division with an output buffer', '''Use a ufunc's `where=` argument to avoid calculating invalid entries. Initialize `out` first so masked entries have a known value. Here an undefined unit price is represented by NaN, a floating point missing-value marker.''',
'''revenue = np.array([100., 0., 90.])
units = np.array([2., 0., 3.])
unit_price = np.full_like(revenue, np.nan)
np.divide(revenue, units, out=unit_price, where=units != 0)
print(unit_price)
np.testing.assert_allclose(unit_price, [50, np.nan, 30], equal_nan=True)''', 'Use a zero-filled output buffer and explain why the missing-value meaning changes.')], [
('Calculate the area of circles with these radii: pi * radius squared.', 'radii = np.array([1., 2., 3.])', 'areas', 'np.testing.assert_allclose(areas, np.pi * np.array([1, 4, 9]))', 'np.pi * radii ** 2'),
('Replace negative inventory entries with zero, preserving positive values.', 'inventory = np.array([3, -2, 7, -1, 0])', 'clean_inventory', 'np.testing.assert_array_equal(clean_inventory, [3, 0, 7, 0, 0])', 'np.clip(inventory, 0, None)')],
'Compute percentage growth between consecutive daily sales. Return NaN when the earlier day is zero, and verify the other entries by hand.',
['https://numpy.org/doc/stable/reference/ufuncs.html'])

lesson('05_broadcasting', 'Broadcasting: calculate across dimensions', 'Intermediate',
       'Predict compatible shapes and use broadcasting for normalization and distance.', 'Notebooks 00–04.', [
('Align dimensions from the right', '''For broadcasting, compare shapes from right to left. Each pair must be equal or one must be 1; absent leading dimensions behave as 1. Shape (3, 2) plus (2,) works. Shape (3, 2) plus (3,) does not. Broadcasting avoids explicitly repeating the inputs, but the result still needs memory.''',
'''prices = np.array([[100., 200.], [150., 250.], [80., 120.]])
tax_rate = np.array([0.05, 0.10])
print("Shapes:", prices.shape, tax_rate.shape)
print("Taxed prices:\\n", prices * (1 + tax_rate))
discount_by_customer = np.array([10., 20., 5.])
print("Discounted:\\n", prices - discount_by_customer[:, None])
assert np.broadcast_shapes((3, 2), (3, 1)) == (3, 2)''', 'Predict the result of broadcasting (4, 1, 3) with (2, 3). Verify with broadcast_shapes.'),
('Center columns and rows', '''Subtracting a column mean from every row centers each feature. `keepdims=True` preserves a length-1 axis, making the intended alignment visible. For row centering this is essential unless you insert the axis yourself.''',
'''data = np.array([[1., 10.], [3., 20.], [5., 30.]])
centered_columns = data - data.mean(axis=0, keepdims=True)
centered_rows = data - data.mean(axis=1, keepdims=True)
print(centered_columns)
print(centered_rows)
np.testing.assert_allclose(centered_columns.mean(axis=0), 0, atol=1e-12)
np.testing.assert_allclose(centered_rows.mean(axis=1), 0, atol=1e-12)''', 'Remove keepdims from the row calculation. Explain why its shapes fail.'),
('Pairwise differences', '''A column of x values minus a row of y values creates every pairwise difference. This forms an outer operation. Here the output has shape (number of x values, number of y values). Write the shape beside each intermediate before scaling up.''',
'''x = np.array([1., 4., 7.])
y = np.array([2., 5.])
differences = x[:, None] - y[None, :]
print(differences)
distances = np.abs(differences)
assert distances.shape == (3, 2)
np.testing.assert_allclose(distances, [[1, 4], [2, 1], [5, 2]])''', 'Use 2D points and produce distances of shape (3, 2) by summing squared coordinate differences.')], [
('Add one offset per row to matrix.', 'matrix = np.array([[1, 2, 3], [4, 5, 6]])\noffsets = np.array([10, 20])', 'shifted', 'np.testing.assert_array_equal(shifted, [[11, 12, 13], [24, 25, 26]])', 'matrix + offsets[:, None]'),
('Create the 1–5 multiplication table, shape (5, 5), using broadcasting.', 'numbers = np.arange(1, 6)', 'times_table', 'assert times_table.shape == (5, 5)\nnp.testing.assert_array_equal(times_table, [[i*j for j in range(1, 6)] for i in range(1, 6)])', 'numbers[:, None] * numbers[None, :]')],
'For a (4, 3) feature table, perform min-max scaling per column. Handle a constant column by returning zeros there.',
['https://numpy.org/doc/stable/user/basics.broadcasting.html'])

lesson('06_statistics_and_aggregation', 'Summarize and analyze numerical data', 'Intermediate',
       'Choose reduction axes, summarize distributions, and build cumulative metrics.', 'Notebooks 00–05.', [
('Mean, median, and spread', '''The mean is sensitive to extreme values; the median is the middle ordered value. Standard deviation measures spread around the mean. NumPy defaults to `ddof=0`, dividing variance by N. `ddof=1` divides by N-1 and is commonly used to estimate population variance from a sample with more than one value.''',
'''delivery_minutes = np.array([20., 22., 21., 23., 90.])
print("Mean:", delivery_minutes.mean())
print("Median:", np.median(delivery_minutes))
print("Population std:", delivery_minutes.std(ddof=0))
print("Sample std:", delivery_minutes.std(ddof=1))
print("Quartiles:", np.percentile(delivery_minutes, [25, 50, 75]))''', 'Replace 90 with 24 and compare how much the mean and median move.'),
('Reduce the intended axis', '''Use a 2D table to separate questions: totals per day reduce products, and totals per product reduce days. `argmax` returns a position, while `max` returns a value. We use both to label the largest result.''',
'''sales = np.array([[5, 3, 2], [7, 2, 4], [4, 6, 3], [8, 4, 5]])
products = np.array(["tea", "coffee", "juice"])
daily = sales.sum(axis=1)
product_totals = sales.sum(axis=0)
print("Daily:", daily)
print("Product totals:", product_totals)
print("Top product:", products[product_totals.argmax()])
assert daily.sum() == product_totals.sum()''', 'Find the best day for each product using argmax(axis=0).'),
('Weighted and cumulative summaries', '''A weighted mean lets observations contribute differently; weights must have a nonzero sum. Cumulative sums track running totals. Differences compare adjacent observations and shorten that axis by one.''',
'''marks = np.array([70., 80., 90.])
weights = np.array([0.2, 0.3, 0.5])
print("Weighted grade:", np.average(marks, weights=weights))
daily_sales = np.array([100., 150., 120., 180.])
print("Running total:", np.cumsum(daily_sales))
print("Changes:", np.diff(daily_sales))
np.testing.assert_allclose(np.average(marks, weights=weights), 83.)''', 'Compute the running mean with cumsum divided by arange(1, n+1).')], [
('Compute the mean temperature per city (columns).', 'temperatures = np.array([[20., 30.], [22., 32.], [24., 34.]])', 'city_means', 'np.testing.assert_allclose(city_means, [22, 32])', 'temperatures.mean(axis=0)'),
('Compute the running mean of spending, including the current day.', 'spending = np.array([10., 30., 20., 40.])', 'running_mean', 'np.testing.assert_allclose(running_mean, [10, 20, 20, 25])', 'np.cumsum(spending) / np.arange(1, spending.size + 1)')],
'Analyze 30 days of synthetic sales: report mean, median, standard deviation, the 90th percentile, best day, and cumulative revenue.',
['https://numpy.org/doc/stable/reference/routines.statistics.html'])

lesson('07_randomness_and_simulation', 'Reproducible randomness and simulations', 'Intermediate',
       'Use Generator, sample distributions, simulate uncertainty, and bootstrap a mean.', 'Notebooks 00–06.', [
('A local random generator', '''Create a generator with `np.random.default_rng(seed)`. A seed makes the same sequence reproducible for the same generator setup and calls; it does not make a sample equal to its theoretical distribution. Calling the generator advances its state. Avoid relying on exact random values across arbitrary future NumPy versions.''',
'''rng = np.random.default_rng(42)
print("Dice:", rng.integers(1, 7, size=12))
print("Uniform:", rng.uniform(0, 1, size=4))
print("Normal:", rng.normal(loc=170, scale=10, size=4))
a = np.random.default_rng(123).integers(0, 100, 5)
b = np.random.default_rng(123).integers(0, 100, 5)
np.testing.assert_array_equal(a, b)''', 'Run the rng cell twice, then run just a later sampling line twice. Explain the difference.'),
('Monte Carlo probability', '''Monte Carlo estimates a quantity by repeated random trials. Each row below is one trial with two dice. A Boolean event is 1 for success and 0 for failure, so its mean estimates probability. The standard error describes typical sampling variation; it is not a guarantee for a particular run.''',
'''rng = np.random.default_rng(7)
dice = rng.integers(1, 7, size=(50_000, 2))
event = dice.sum(axis=1) == 7
estimate = event.mean()
standard_error = np.sqrt(estimate * (1 - estimate) / event.size)
print("Estimated P(sum=7):", estimate)
print("Exact probability:", 6 / 36)
print("Estimated standard error:", standard_error)
assert 0 <= estimate <= 1''', 'Try 500 and 50,000 trials. Compare uncertainty, without expecting every larger sample to be closer.'),
('Bootstrap a sample mean', '''A bootstrap resamples the observed dataset with replacement. Each row is a new sample of the same size. Quantiles of bootstrap means give a simple percentile interval. This illustration assumes independent, representative observations; resampling cannot repair biased data.''',
'''observed = np.array([12., 14., 9., 15., 13., 11., 18., 16.])
rng = np.random.default_rng(10)
resampled = rng.choice(observed, size=(2_000, observed.size), replace=True)
bootstrap_means = resampled.mean(axis=1)
interval = np.quantile(bootstrap_means, [0.025, 0.975])
print("Observed mean:", observed.mean())
print("Illustrative 95% percentile interval:", interval)
assert bootstrap_means.shape == (2_000,)''', 'Plot the bootstrap means with plt.hist. Try a larger observed sample.')], [
('Generate 100 die rolls (integers 1 through 6) with a generator seeded with 99.', '', 'rolls', 'assert rolls.shape == (100,)\nassert np.issubdtype(rolls.dtype, np.integer)\nassert np.all((rolls >= 1) & (rolls <= 6))\nnp.testing.assert_array_equal(rolls, np.random.default_rng(99).integers(1, 7, size=100))', 'np.random.default_rng(99).integers(1, 7, size=100)'),
('Estimate the proportion of trials containing at least one head; 1 means heads.', 'coin_trials = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])', 'probability', 'np.testing.assert_allclose(probability, 0.75)', '(coin_trials == 1).any(axis=1).mean()')],
'Estimate pi by sampling points in the unit square and counting points with x²+y² <= 1. Repeat with several seeds and sample sizes.',
['https://numpy.org/doc/stable/reference/random/generator.html'])

lesson('08_cleaning_and_file_io', 'Clean missing data and save your work', 'Intermediate',
       'Detect invalid values, impute deliberately, and round-trip text and binary data.', 'Notebooks 00–07.', [
('Missing is not zero', '''NaN represents a missing or undefined floating point value. Test it with `isnan`, because NaN does not equal itself. `isfinite` rejects both NaN and infinities. Here we treat infinity as invalid and convert it to NaN; this is a data policy, not a universal rule.''',
'''raw = np.array([[10., np.nan], [12., 20.], [np.inf, 22.]])
cleaned = raw.copy()
cleaned[~np.isfinite(cleaned)] = np.nan
print("Missing mask:\\n", np.isnan(cleaned))
print("Column means ignoring missing:", np.nanmean(cleaned, axis=0))
assert np.isnan(cleaned).sum() == 2''', 'Count missing entries by row and by column.'),
('Imputation with a stated assumption', '''Imputation replaces missing values. Column-mean imputation preserves the observed column mean but changes the distribution and can understate variation. An entirely missing column needs another policy; here we reject it before computing its mean.''',
'''if np.any(np.all(np.isnan(cleaned), axis=0)):
    raise ValueError("A column has no observed values")
column_means = np.nanmean(cleaned, axis=0)
imputed = np.where(np.isnan(cleaned), column_means, cleaned)
print(imputed)
assert np.isfinite(imputed).all()
np.testing.assert_allclose(imputed.mean(axis=0), column_means)''', 'Compare the standard deviation before and after filling a missing entry.'),
('CSV and NumPy binary formats', '''CSV is readable but does not preserve array metadata as reliably as `.npy`. Use `.npz` for multiple named arrays. `genfromtxt` can parse simple numeric text with missing entries. Temporary files make this example safe to rerun; replace the directory with a chosen Path when you want persistent files.''',
'''from pathlib import Path
from tempfile import TemporaryDirectory
from io import StringIO
parsed = np.genfromtxt(StringIO("temperature,humidity\\n20,50\\n22,\\n"), delimiter=",", skip_header=1)
print("Parsed CSV:\\n", parsed)
with TemporaryDirectory() as folder:
    folder = Path(folder)
    np.savetxt(folder / "clean.csv", imputed, delimiter=",", header="a,b", comments="")
    from_csv = np.loadtxt(folder / "clean.csv", delimiter=",", skiprows=1)
    np.save(folder / "clean.npy", imputed)
    from_npy = np.load(folder / "clean.npy", allow_pickle=False)
    np.savez_compressed(folder / "bundle.npz", data=imputed, means=column_means)
    with np.load(folder / "bundle.npz", allow_pickle=False) as archive:
        print("Saved names:", archive.files)
        np.testing.assert_allclose(archive["data"], imputed)
    np.testing.assert_allclose(from_csv, imputed)
    np.testing.assert_array_equal(from_npy, imputed)''', 'Save an integer array as .npy and confirm that its dtype survives loading.')], [
('Keep only rows where every value is finite.', 'measurements = np.array([[1., 2.], [np.nan, 3.], [4., 5.], [6., np.inf]])', 'valid_rows', 'np.testing.assert_allclose(valid_rows, [[1, 2], [4, 5]])', 'measurements[np.isfinite(measurements).all(axis=1)]'),
('Replace NaN entries with the median of the observed values.', 'values = np.array([1., np.nan, 3., 9.])', 'filled_values', 'np.testing.assert_allclose(filled_values, [1, 3, 3, 9])', 'np.where(np.isnan(values), np.nanmedian(values), values)')],
'Create a numeric CSV with a header and two missing values. Load it, report missing counts, apply a documented filling policy, and save a verified .npy copy.',
['https://numpy.org/doc/stable/user/how-to-io.html'])

lesson('09_sorting_searching_grouping', 'Sort, search, and aggregate groups', 'Intermediate',
       'Sort related arrays consistently, find insertion points, and reduce by group.', 'Notebooks 00–08.', [
('Sort values and positions', '''`sort` returns sorted values. `argsort` returns indices that reorder the original. Reuse those indices for related columns so names stay aligned with scores. Stable sorting preserves the input order of ties; reversing an ascending result reverses ties too, so sort negative scores for stable descending order.''',
'''names = np.array(["Asha", "Ben", "Chen", "Divya"])
scores = np.array([82, 95, 82, 70])
order = np.argsort(-scores, kind="stable")
print(names[order])
print(scores[order])
np.testing.assert_array_equal(names[order], ["Ben", "Asha", "Chen", "Divya"])''', 'Sort scores ascending and check which tied student appears first.'),
('Search in sorted data', '''`searchsorted` returns insertion positions in an ascending sorted array. `side="left"` inserts before equal values; `side="right"` inserts after them. Their difference counts duplicates. `unique` finds distinct labels and can return group indices and counts.''',
'''sorted_values = np.array([10, 20, 20, 30, 40])
left = np.searchsorted(sorted_values, 20, side="left")
right = np.searchsorted(sorted_values, 20, side="right")
print("Insertion range:", left, right, "count:", right - left)
labels, counts = np.unique(["tea", "coffee", "tea", "juice"], return_counts=True)
print(dict(zip(labels, counts)))
assert right - left == 2''', 'Find the insertion point for 25 and explain why it is not a match.'),
('Group totals without pandas', '''`unique(..., return_inverse=True)` encodes each label as a nonnegative integer. `bincount` adds weights by integer code. This gives group sums; dividing by counts gives group means. Weighted bincount returns floating point output.''',
'''category = np.array(["tea", "coffee", "tea", "juice", "coffee"])
revenue = np.array([10., 20., 15., 12., 30.])
groups, inverse = np.unique(category, return_inverse=True)
totals = np.bincount(inverse, weights=revenue, minlength=groups.size)
counts = np.bincount(inverse, minlength=groups.size)
for group, total, mean in zip(groups, totals, totals / counts):
    print(group, "total:", total, "mean:", mean)
np.testing.assert_allclose(totals.sum(), revenue.sum())''', 'Compute the share of total revenue contributed by each group.')], [
('Return the names of the two highest scorers in descending score order.', 'students = np.array(["A", "B", "C", "D"])\nmarks = np.array([75, 90, 65, 85])', 'top_students', 'np.testing.assert_array_equal(top_students, ["B", "D"])', 'students[np.argsort(-marks)[:2]]'),
('Sum amounts by integer group code; return totals for groups 0, 1, 2.', 'codes = np.array([0, 1, 0, 2, 1])\namounts = np.array([2., 5., 3., 7., 1.])', 'group_totals', 'np.testing.assert_allclose(group_totals, [5, 6, 7])', 'np.bincount(codes, weights=amounts, minlength=3)')],
'Build a product leaderboard with totals, counts, mean sale value, and descending rank. Verify that grouped totals add up to the raw total.',
['https://numpy.org/doc/stable/reference/routines.sort.html', 'https://numpy.org/doc/stable/reference/generated/numpy.bincount.html'])

lesson('10_linear_algebra', 'Vectors, matrices, and least squares', 'Advanced',
       'Multiply matrices, solve linear systems, fit a line, and inspect an SVD.', 'Notebooks 00–09; basic algebra. A matrix is a rectangular table; a vector is a 1D array.', [
('Matrix multiplication combines weighted values', '''For A shaped (m, n) and B shaped (n, p), A @ B has shape (m, p). Each result is a row-column dot product: multiply matching entries and add them. A matrix times a length-n vector produces a length-m vector.''',
'''A = np.array([[1., 2.], [3., 4.]])
v = np.array([10., 20.])
print("Elementwise:\\n", A * A)
print("Matrix product:\\n", A @ A)
print("Matrix times vector:", A @ v)
np.testing.assert_allclose(A @ v, [50, 110])''', 'Compute the first entry of A @ A by hand.'),
('Solve equations and check residuals', '''To solve A x = b for square, full-rank A, use `linalg.solve`. Computing an explicit inverse just to multiply by b usually adds work and numerical error. A residual A @ x - b checks how closely the computed solution satisfies the equations. Nearly dependent columns can make solutions sensitive to input changes.''',
'''A = np.array([[2., 1.], [1., 3.]])
b = np.array([5., 7.])
x = np.linalg.solve(A, b)
print("Solution:", x)
print("Residual norm:", np.linalg.norm(A @ x - b))
print("Condition number:", np.linalg.cond(A))
np.testing.assert_allclose(A @ x, b)''', 'Make both rows identical and catch the resulting LinAlgError.'),
('Fit a line and factor a matrix', '''For more equations than unknowns, least squares minimizes the sum of squared residuals. A column of ones represents the intercept. SVD factors a matrix into orthogonal directions and singular values; small singular values identify directions with little variation. We reconstruct the design matrix to check the factorization.''',
'''x_data = np.arange(5, dtype=float)
y_data = np.array([1.1, 2.9, 5.2, 6.8, 9.0])
design = np.column_stack([np.ones(x_data.size), x_data])
coefficients, residuals, rank, singular_values = np.linalg.lstsq(design, y_data, rcond=None)
prediction = design @ coefficients
print("Intercept, slope:", coefficients)
print("RMSE:", np.sqrt(np.mean((prediction - y_data) ** 2)))
U, s, Vt = np.linalg.svd(design, full_matrices=False)
np.testing.assert_allclose((U * s) @ Vt, design, atol=1e-12)
assert rank == 2''', 'Plot the observed points and fitted line. Add one extreme y value and refit.')], [
('Solve system @ solution = target.', 'system = np.array([[3., 1.], [1., 2.]])\ntarget = np.array([9., 8.])', 'solution', 'np.testing.assert_allclose(solution, [2, 3])\nnp.testing.assert_allclose(system @ solution, target)', 'np.linalg.solve(system, target)'),
('Fit y = intercept + slope*x with least squares; return [intercept, slope].', 'x_fit = np.arange(6, dtype=float)\ny_fit = 4 + 3 * x_fit\nX_fit = np.column_stack([np.ones(x_fit.size), x_fit])', 'line_parameters', 'np.testing.assert_allclose(line_parameters, [4, 3], atol=1e-12)', 'np.linalg.lstsq(X_fit, y_fit, rcond=None)[0]')],
'Fit a quadratic y = a + b*x + c*x² to noisy synthetic data. Compare its training residual with a straight-line model and explain why lower training error alone is insufficient.',
['https://numpy.org/doc/stable/reference/routines.linalg.html'])

lesson('11_copies_views_and_memory', 'Copies, views, strides, and memory', 'Advanced',
       'Predict shared memory, inspect strides, and use a memory-mapped array.', 'Notebooks 00–10.', [
('Basic slicing shares data', '''A view refers to an existing data buffer. Basic slicing normally produces a view; `.copy()` makes independent storage. Changing a view changes the original data. `shares_memory` checks whether two arrays overlap in memory.''',
'''original = np.arange(6)
view = original[1:4]
independent = original[1:4].copy()
view[0] = 99
print("Original:", original)
print("Independent copy:", independent)
assert np.shares_memory(original, view)
assert not np.shares_memory(original, independent)
assert original[1] == 99''', 'Modify independent and confirm original stays unchanged.'),
('Advanced indexing and strides', '''Integer-array and Boolean indexing return copies when reading. Assignment like `a[mask] = value` still writes to a. Avoid chained indexing when you intend to modify the original. Strides are byte jumps between adjacent entries along each axis. A transpose can reorder strides without moving the values.''',
'''a = np.arange(12, dtype=np.int64).reshape(3, 4)
selected = a[[0, 2]]
selected[0, 0] = -100
assert a[0, 0] == 0
print("Original strides:", a.strides)
print("Transpose strides:", a.T.strides)
print("C contiguous:", a.flags.c_contiguous, a.T.flags.c_contiguous)
flat_copy = a.flatten()
flat_maybe_view = a.ravel()
assert not np.shares_memory(a, flat_copy)
assert np.shares_memory(a, flat_maybe_view)
# reshape/ravel may need a copy for other layouts: inspect rather than assume.''', 'Compare shares_memory(a, a.T.reshape(-1)) with shares_memory(a, a.reshape(-1)).'),
('Read a file through memory mapping', '''Memory mapping exposes file-backed array storage without first reading the whole file into a normal array. Operations can still allocate full-size outputs, so process slices when data is large. Here we use a small temporary file and keep the read-only mapping within its lifetime.''',
'''from pathlib import Path
from tempfile import TemporaryDirectory
with TemporaryDirectory() as folder:
    path = Path(folder) / "values.npy"
    np.save(path, np.arange(1000, dtype=np.float64))
    mapped = np.load(path, mmap_mode="r", allow_pickle=False)
    first_chunk_mean = mapped[:100].mean()
    print("Mapped type:", type(mapped).__name__)
    print("First chunk mean:", first_chunk_mean)
    np.testing.assert_allclose(first_chunk_mean, 49.5)
    del mapped  # release the file mapping before temporary directory cleanup on Windows''', 'Compute the mean using ten chunks and compare with the full-array result.')], [
('Take an independent copy of the first two rows of source.', 'source = np.arange(12).reshape(4, 3)', 'safe_rows', 'np.testing.assert_array_equal(safe_rows, [[0, 1, 2], [3, 4, 5]])\nassert not np.shares_memory(source, safe_rows)', 'source[:2].copy()'),
('Take every second element as a view, without copying.', 'source_vector = np.arange(10)', 'every_second', 'np.testing.assert_array_equal(every_second, [0, 2, 4, 6, 8])\nassert np.shares_memory(source_vector, every_second)', 'source_vector[::2]')],
'Compare the shape, strides, contiguity flags, and sharing behavior of a matrix, its transpose, a stepped slice, and an explicitly contiguous copy.',
['https://numpy.org/doc/stable/user/basics.copies.html', 'https://numpy.org/doc/stable/reference/generated/numpy.memmap.html'])

lesson('12_vectorization_and_performance', 'Vectorization and measured performance', 'Advanced',
       'Replace loops thoughtfully, measure runtime fairly, and limit temporary memory.', 'Notebooks 00–11.', [
('Establish correctness before timing', '''Vectorization moves repeated numeric work into array operations. Keep a small, clear reference implementation to verify the faster version. `np.vectorize` is a convenience wrapper around repeated Python calls, not a general performance optimization.''',
'''def squared_distance_loop(a, b):
    total = 0.0
    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2
    return total

def squared_distance_numpy(a, b):
    return np.sum((a - b) ** 2)

rng = np.random.default_rng(4)
a, b = rng.normal(size=(2, 20_000))
np.testing.assert_allclose(squared_distance_loop(a, b), squared_distance_numpy(a, b))
print("Agreement checked.")''', 'Check both functions on equal vectors and on one-element vectors.'),
('Benchmark repeated runs', '''Use repeated timings on the same inputs and report the setup. A minimum timing approximates a less interrupted run; real workloads may differ. Small arrays may not benefit from vectorization. Hardware, dtype, memory layout, and library builds influence results, so speed is not an assertion.''',
'''from timeit import repeat
loop_seconds = min(repeat(lambda: squared_distance_loop(a, b), number=3, repeat=3)) / 3
numpy_seconds = min(repeat(lambda: squared_distance_numpy(a, b), number=3, repeat=3)) / 3
print(f"Python loop: {loop_seconds:.6f} seconds/call")
print(f"NumPy:       {numpy_seconds:.6f} seconds/call")
print(f"Observed ratio: {loop_seconds / numpy_seconds:.1f}x")
print("Input shape/dtype:", a.shape, a.dtype)''', 'Repeat for 10 values and 100,000 values; do not assume the same speed ratio.'),
('Reuse buffers and process chunks', '''Array expressions can create large temporaries. Ufunc `out=` lets you reuse storage. Chunking limits intermediate size. Here squared differences are computed a chunk at a time; the sum of chunk results matches the reference within floating point tolerance.''',
'''scratch = np.empty_like(a)
np.subtract(a, b, out=scratch)
np.square(scratch, out=scratch)
buffer_result = scratch.sum()
chunk_result = 0.0
chunk_size = 2048
for start in range(0, a.size, chunk_size):
    difference = a[start:start + chunk_size] - b[start:start + chunk_size]
    chunk_result += np.sum(difference ** 2)
np.testing.assert_allclose(buffer_result, chunk_result)
print("Full scratch bytes:", scratch.nbytes)
print("One chunk difference bytes (maximum):", chunk_size * a.itemsize)''', 'Explain why repeatedly calling np.append in a loop can repeatedly allocate and copy data.')], [
('Compute the sum of squares for each row without a Python loop.', 'features = np.array([[1., 2., 3.], [4., 5., 6.]])', 'row_energy', 'np.testing.assert_allclose(row_energy, [14, 77])', '(features ** 2).sum(axis=1)'),
('Implement f(x)=3*x+2 using array operations.', 'inputs = np.arange(5, dtype=float)', 'transformed', 'np.testing.assert_allclose(transformed, [2, 5, 8, 11, 14])', '3 * inputs + 2')],
'Benchmark row-wise Euclidean norms using a loop and a vectorized expression. Check correctness, state shape/dtype, and explain temporary memory costs.',
['https://numpy.org/doc/stable/reference/ufuncs.html', 'https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html'])

lesson('13_numerical_stability', 'Floating point accuracy and numerical stability', 'Advanced',
       'Use tolerances, avoid overflow and cancellation, and inspect precision limits.', 'Notebooks 00–12.', [
('Approximate arithmetic needs meaningful tolerances', '''Many decimal fractions have no exact binary representation. `isclose` and `assert_allclose` compare with absolute and relative tolerances. Choose tolerances from the scale and accuracy needs of your problem; default tolerances are not a universal specification. Near zero, absolute tolerance matters especially.''',
'''value = 0.1 + 0.2
print("Stored sum:", repr(value))
print("Exact equality:", value == 0.3)
print("Close:", np.isclose(value, 0.3, rtol=1e-12, atol=1e-15))
print("float32 epsilon:", np.finfo(np.float32).eps)
print("float64 epsilon:", np.finfo(np.float64).eps)
np.testing.assert_allclose(value, 0.3, rtol=1e-12, atol=1e-15)''', 'Compare 1e-12 and 0 using different absolute tolerances.'),
('Preserve small changes and avoid overflow', '''Subtracting nearly equal quantities can lose meaningful digits. Use `log1p(x)` for log(1+x) and `expm1(x)` for exp(x)-1 when x is small. NumPy integer arithmetic has fixed-width limits, so promote the dtype before arithmetic that may overflow.''',
'''tiny = 1e-16
print("Naive log:", np.log(1 + tiny))
print("log1p:", np.log1p(tiny))
print("Naive exp change:", np.exp(tiny) - 1)
print("expm1:", np.expm1(tiny))
small = np.array([120], dtype=np.int8)
print("Overflowed int8 sum:", small + small)
print("Promoted sum:", small.astype(np.int64) + small.astype(np.int64))
np.testing.assert_allclose(np.log1p(tiny), tiny, rtol=1e-12, atol=0)''', 'Find a value for which float32 rounds 1 + x back to 1, while float64 does not.'),
('Stable softmax', '''Softmax converts finite scores into positive weights summing to one. Direct exponentials can overflow for large scores. Subtract the row maximum first: the largest exponent becomes exp(0)=1, and the normalized result is mathematically unchanged. Very small probabilities can still underflow to zero.''',
'''def softmax(scores):
    scores = np.asarray(scores, dtype=np.float64)
    shifted = scores - scores.max(axis=-1, keepdims=True)
    exponentials = np.exp(shifted)
    return exponentials / exponentials.sum(axis=-1, keepdims=True)

scores = np.array([[1000., 1001., 1002.], [-1000., -1000., -999.]])
probabilities = softmax(scores)
print(probabilities)
assert np.isfinite(probabilities).all()
np.testing.assert_allclose(probabilities.sum(axis=1), 1)
np.testing.assert_allclose(softmax(scores + 500), probabilities)''', 'Add a test for equal scores and another for a row containing only one score.')], [
('Compute log(1 + x) accurately for very small x.', 'tiny_values = np.array([1e-16, 1e-12, 1e-8])', 'accurate_logs', 'np.testing.assert_allclose(accurate_logs, np.log1p(tiny_values), rtol=1e-12, atol=0)', 'np.log1p(tiny_values)'),
('Use softmax to convert [10000, 10000] into normalized probabilities.', 'large_scores = np.array([10000., 10000.])', 'weights', 'assert np.isfinite(weights).all()\nnp.testing.assert_allclose(weights, [0.5, 0.5])', 'softmax(large_scores)')],
'Compare summing float32 values with default accumulation and dtype=float64. Construct a dataset with very different magnitudes and explain any difference.',
['https://numpy.org/doc/stable/reference/generated/numpy.allclose.html', 'https://numpy.org/doc/stable/reference/generated/numpy.log1p.html'])

lesson('14_advanced_array_patterns', 'Einsum, rolling windows, and repeated indices', 'Expert practice',
       'Express tensor contractions, calculate rolling features, and accumulate repeated indices.', 'Notebooks 00–13.', [
('Einsum names the axes', '''`einsum` expresses sums of products using axis labels. In `ij,jk->ik`, j appears in both inputs and is absent from the output, so it is summed. Labels in the output survive. Start with an explicit output expression and compare with familiar operations before using more complex contractions.''',
'''A = np.arange(6, dtype=float).reshape(2, 3)
B = np.arange(12, dtype=float).reshape(3, 4)
product = np.einsum("ij,jk->ik", A, B, optimize=True)
row_energy = np.einsum("ij,ij->i", A, A)
print(product)
print("Row energy:", row_energy)
np.testing.assert_allclose(product, A @ B)
np.testing.assert_allclose(row_energy, (A * A).sum(axis=1))''', 'Express the dot product of two 1D arrays and the trace of a square matrix with einsum.'),
('Rolling windows as views', '''`sliding_window_view` exposes overlapping windows without copying every window. By default the view is read-only because windows overlap. A window of width w on n values gives n-w+1 valid windows. Reducing all windows still performs work proportional to the number of window entries; for large rolling sums, cumulative sums can be cheaper.''',
'''from numpy.lib.stride_tricks import sliding_window_view
signal = np.array([1., 2., 3., 4., 5., 6.])
windows = sliding_window_view(signal, window_shape=3)
rolling_mean = windows.mean(axis=-1)
print(windows)
print("Rolling means:", rolling_mean)
assert windows.shape == (4, 3)
assert not windows.flags.writeable
assert np.shares_memory(signal, windows)
np.testing.assert_allclose(rolling_mean, [2, 3, 4, 5])''', 'Compute rolling minima and maxima, then align each result with the last index in its window.'),
('Repeated indices need unbuffered accumulation', '''`a[index] += value` uses buffered advanced indexing. Repeated positions may be updated only once rather than once per occurrence. `np.add.at` accumulates every occurrence. For nonnegative integer codes, bincount can be a simpler and often faster sum operation.''',
'''indices = np.array([0, 0, 2])
values = np.array([1., 1., 5.])
buffered = np.zeros(3)
buffered[indices] += values
accumulated = np.zeros(3)
np.add.at(accumulated, indices, values)
print("Buffered:", buffered)
print("Accumulated:", accumulated)
np.testing.assert_allclose(accumulated, [2, 0, 5])
np.testing.assert_allclose(accumulated, np.bincount(indices, weights=values, minlength=3))''', 'Use np.maximum.at to compute the largest value per group, starting from -infinity.')], [
('Use einsum to compute one dot product per pair of corresponding rows.', 'left = np.array([[1., 2.], [3., 4.]])\nright = np.array([[5., 6.], [7., 8.]])', 'row_dots', 'np.testing.assert_allclose(row_dots, [17, 53])', 'np.einsum("ij,ij->i", left, right)'),
('Calculate valid rolling means with window width 2.', 'series = np.array([2., 4., 8., 10.])', 'rolling', 'np.testing.assert_allclose(rolling, [3, 6, 9])', 'sliding_window_view(series, 2).mean(axis=-1)')],
'Create a batch shaped (4, 3, 2). Compute each batch member’s 2×2 Gram matrix using both swapaxes(..., -1, -2) @ data and einsum, then compare.',
['https://numpy.org/doc/stable/reference/generated/numpy.einsum.html', 'https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html', 'https://numpy.org/doc/stable/reference/generated/numpy.ufunc.at.html'])

lesson('15_signal_processing_with_fft', 'Explore signals with NumPy FFT', 'Expert practice',
       'Build a sampled signal, identify frequency peaks, and reconstruct a filtered signal.', 'Notebooks 00–14; a sine wave repeats at a frequency measured in cycles per second.', [
('Build a signal with known frequencies', '''Sampling records a signal at evenly spaced times. A sample rate of fs gives a Nyquist frequency fs/2; frequencies above that limit cannot be uniquely recovered without additional assumptions. We use endpoint=False so a one-second record contains exactly fs samples without repeating the endpoint.''',
'''import matplotlib.pyplot as plt
sample_rate = 256
time = np.arange(sample_rate) / sample_rate
signal = np.sin(2 * np.pi * 5 * time) + 0.4 * np.sin(2 * np.pi * 40 * time)
fig, ax = plt.subplots(figsize=(9, 3))
ax.plot(time, signal)
ax.set(xlabel="Time (seconds)", ylabel="Amplitude", title="5 Hz + 40 Hz signal")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
assert signal.shape == (256,)''', 'Change the 40 Hz amplitude and predict how the signal and spectrum change.'),
('Transform time into frequency', '''For a real-valued signal, `rfft` returns the nonnegative-frequency coefficients. `rfftfreq` provides their frequencies. The frequency-bin spacing is fs/N. Our one-second example uses whole cycles, reducing boundary discontinuities. Non-integer cycles cause spectral leakage; windowing is a useful extension.''',
'''spectrum = np.fft.rfft(signal)
frequencies = np.fft.rfftfreq(signal.size, d=1 / sample_rate)
amplitude = np.abs(spectrum) / signal.size
# Double only bins that have negative-frequency partners: this N is even.
amplitude[1:-1] *= 2
peak_indices = np.argsort(amplitude)[-2:][::-1]
print("Peak frequencies:", frequencies[peak_indices])
print("Peak amplitudes:", amplitude[peak_indices])
np.testing.assert_allclose(frequencies[peak_indices], [5, 40])
fig, ax = plt.subplots(figsize=(9, 3))
ax.stem(frequencies, amplitude, basefmt=" ")
ax.set(xlim=(0, 60), xlabel="Frequency (Hz)", ylabel="Amplitude", title="One-sided spectrum")
plt.tight_layout()
plt.show()''', 'Use 5.5 Hz instead of 5 Hz and inspect the leakage into nearby bins.'),
('Filter and reconstruct', '''Here we zero coefficients above 10 Hz and invert the FFT. This is a learning example of an ideal frequency cutoff. Abrupt cutoffs can create ringing for other signals; real filtering design also considers boundaries and transient behavior. Passing n preserves the intended length, including for odd-length signals.''',
'''filtered_spectrum = spectrum.copy()
filtered_spectrum[frequencies > 10] = 0
filtered = np.fft.irfft(filtered_spectrum, n=signal.size)
expected = np.sin(2 * np.pi * 5 * time)
np.testing.assert_allclose(filtered, expected, atol=1e-12)
np.testing.assert_allclose(np.fft.irfft(spectrum, n=signal.size), signal, atol=1e-12)
fig, ax = plt.subplots(figsize=(9, 3))
ax.plot(time, signal, alpha=0.4, label="Original")
ax.plot(time, filtered, label="Below 10 Hz")
ax.set(xlabel="Time (seconds)", ylabel="Amplitude", title="Frequency filtering")
ax.legend()
plt.tight_layout()
plt.show()''', 'Set the cutoff to 50 Hz and check that the original signal is recovered.')], [
('Find the dominant frequency in this 8 Hz signal, sampled at 100 Hz.', 'fs = 100\nt = np.arange(100) / fs\nwave = np.sin(2 * np.pi * 8 * t)', 'dominant_hz', 'np.testing.assert_allclose(dominant_hz, 8)', 'np.fft.rfftfreq(wave.size, d=1/fs)[np.abs(np.fft.rfft(wave)).argmax()]'),
('Reconstruct wave by applying rfft then irfft; preserve its length.', '', 'reconstructed', 'assert reconstructed.shape == wave.shape\nnp.testing.assert_allclose(reconstructed, wave, atol=1e-12)', 'np.fft.irfft(np.fft.rfft(wave), n=wave.size)')],
'Add seeded Gaussian noise to a sine wave. Compare reconstruction RMSE before and after a frequency cutoff. Explain why an appropriate cutoff depends on the signal.',
['https://numpy.org/doc/stable/reference/routines.fft.html'])

lesson('16_project_sales_analysis', 'Project: analyze a month of store sales', 'Capstone',
       'Combine cleaning, broadcasting, aggregation, plots, and business interpretation.', 'Notebooks 00–09; revisit 11–13 for memory and accuracy.', [
('Project brief and reproducible data', '''You manage three stores selling four products over 30 days. Build a report of revenue per store, top products, and daily trends. Quantities have shape **(day, store, product)**. This dataset is synthetic, and prices are fixed for the exercise. Treat a NaN as an unavailable count, not as zero sales.

Before running each stage, sketch the expected output shape. The worked pipeline is a model; the exercises ask you to extend it.''',
'''rng = np.random.default_rng(2026)
stores = np.array(["North", "Central", "South"])
products = np.array(["Tea", "Coffee", "Juice", "Water"])
prices = np.array([20., 40., 35., 15.])
units = rng.poisson(lam=np.array([12, 8, 6, 15]), size=(30, 3, 4)).astype(float)
units[2, 0, 1] = np.nan
units[10, 2, 3] = np.nan
print("Shape:", units.shape, "missing:", np.isnan(units).sum())
assert units.shape == (30, 3, 4)''', 'Add a fifth product and update the rate vector and prices consistently.'),
('Clean and calculate revenue', '''Fill a missing count with that store/product pair’s average observed count across days. This gives fractional estimated counts, so report them as estimates. Keep the original array and missing mask for auditing. Broadcasting aligns the price vector with the last axis.''',
'''missing = np.isnan(units)
if np.any(missing.all(axis=0)):
    raise ValueError("A store/product pair has no observed counts")
mean_units = np.nanmean(units, axis=0, keepdims=True)
filled_units = np.where(missing, mean_units, units)
revenue = filled_units * prices
store_revenue = revenue.sum(axis=(0, 2))
product_revenue = revenue.sum(axis=(0, 1))
daily_revenue = revenue.sum(axis=(1, 2))
print("Revenue by store:", dict(zip(stores, store_revenue.round(2))))
print("Top product:", products[product_revenue.argmax()])
print("Revenue from imputed entries:", revenue[missing].sum().round(2))
assert np.isfinite(revenue).all()
np.testing.assert_allclose(store_revenue.sum(), daily_revenue.sum())
np.testing.assert_allclose(product_revenue.sum(), revenue.sum())''', 'Compare the total against dropping only missing entries with nansum(units * prices). Explain the difference.'),
('Visualize and interpret', '''A line chart shows daily change; bars compare totals across stores. A rolling mean smooths short-term variation but omits the initial incomplete windows here. Label every chart with units and keep interpretation separate from what synthetic data can establish.''',
'''import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view
weekly_trend = sliding_window_view(daily_revenue, 7).mean(axis=-1)
fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
axes[0].plot(np.arange(1, 31), daily_revenue, alpha=0.5, label="Daily")
axes[0].plot(np.arange(7, 31), weekly_trend, linewidth=2, label="7-day mean")
axes[0].set(xlabel="Day", ylabel="Revenue (currency units)", title="Monthly revenue trend")
axes[0].legend()
axes[1].bar(stores, store_revenue)
axes[1].set(ylabel="Revenue (currency units)", title="Revenue by store")
plt.tight_layout()
plt.show()
print("Best day:", daily_revenue.argmax() + 1)
print("Estimated total revenue:", round(revenue.sum(), 2))''', 'Write three findings using numbers and one limitation caused by missing data.')], [
('Compute each store’s fraction of total revenue, in store order.', '', 'store_share', 'assert store_share.shape == (3,)\nnp.testing.assert_allclose(store_share.sum(), 1)\nnp.testing.assert_allclose(store_share, store_revenue / revenue.sum())', 'store_revenue / revenue.sum()'),
('Compute average DAILY revenue by store and product, shape (3, 4).', '', 'average_daily', 'assert average_daily.shape == (3, 4)\nnp.testing.assert_allclose(average_daily * 30, revenue.sum(axis=0))', 'revenue.mean(axis=0)')],
'''Independent deliverable: create a report cell with total revenue, best store, best product, missing count, and imputed revenue share. Export the cleaned data and summary arrays to .npz, reload them, and verify equality. Add a scenario where Coffee price rises 10% with fixed units; label the fixed-demand assumption. Success means correct shapes, reconciled totals, labeled plots, and a clear explanation of the cleaning policy.''',
['https://numpy.org/doc/stable/reference/routines.statistics.html', 'https://numpy.org/doc/stable/reference/generated/numpy.savez_compressed.html'])

lesson('17_project_pca_and_clustering', 'Project: PCA and k-means from NumPy building blocks', 'Capstone / expert practice',
       'Standardize features, implement PCA with SVD, and build a checked k-means loop.', 'Notebooks 00–14. PCA finds directions of variation; clustering groups nearby observations.', [
('Build and standardize a feature table', '''Imagine three groups of observations with three numeric features. Each row is an observation and each column a feature. Standardization puts features on comparable scales. Constant columns need special handling to avoid dividing by zero. Here the full dataset is used for exploratory analysis; predictive workflows fit preprocessing only on training data.''',
'''rng = np.random.default_rng(21)
centers = np.array([[-4., -3., 0.], [0., 4., 4.], [4., -2., -3.]])
X = np.concatenate([rng.normal(loc=center, scale=0.55, size=(60, 3)) for center in centers])
feature_mean = X.mean(axis=0)
feature_std = X.std(axis=0)
safe_std = np.where(feature_std == 0, 1, feature_std)
Z = (X - feature_mean) / safe_std
np.testing.assert_allclose(Z.mean(axis=0), 0, atol=1e-12)
np.testing.assert_allclose(Z.std(axis=0), 1)
print("Observations, features:", Z.shape)''', 'Multiply one raw feature by 100 and compare distances before and after standardization.'),
('PCA through singular value decomposition', '''PCA rotates centered data toward directions of greatest variance. In the SVD Z = U diag(s) Vt, rows of Vt are principal directions. Keeping two directions compresses three features to two. Explained variance ratios use squared singular values. Signs of principal directions are arbitrary; validate reconstruction and variance, not a particular sign.''',
'''U, s, Vt = np.linalg.svd(Z, full_matrices=False)
components = Vt[:2]
embedding = Z @ components.T
explained_ratio = s ** 2 / np.sum(s ** 2)
reconstructed_Z = embedding @ components
print("Explained variance ratios:", explained_ratio)
print("Retained fraction:", explained_ratio[:2].sum())
print("Reconstruction MSE:", np.mean((Z - reconstructed_Z) ** 2))
assert embedding.shape == (180, 2)
np.testing.assert_allclose((U * s) @ Vt, Z, atol=1e-12)
np.testing.assert_allclose(components @ components.T, np.eye(2), atol=1e-12)''', 'Keep one component and then all three. Compare reconstruction error.'),
('K-means: assign, update, repeat', '''K-means alternates between assigning each observation to its nearest center and replacing centers with group means. It minimizes a local squared-distance objective and depends on initialization. Empty clusters retain their previous center here. Run several seeds and keep the smallest final inertia. Cluster numbers are arbitrary labels.

The distance tensor below has shape (observations, clusters, features). This simple implementation is for small finite 2D data; a large dataset needs chunking or a more memory-efficient distance calculation.''',
'''def kmeans(data, k, seed=0, max_iter=100):
    data = np.asarray(data, dtype=float)
    if data.ndim != 2 or not np.isfinite(data).all():
        raise ValueError("Expected a finite 2D feature table")
    if not 1 <= k <= len(data) or max_iter < 1:
        raise ValueError("Invalid k or max_iter")
    rng = np.random.default_rng(seed)
    centers = data[rng.choice(len(data), k, replace=False)].copy()
    previous_labels = None
    history = []
    for _ in range(max_iter):
        squared = ((data[:, None, :] - centers[None, :, :]) ** 2).sum(axis=-1)
        labels = squared.argmin(axis=1)
        history.append(float(squared[np.arange(len(data)), labels].sum()))
        if previous_labels is not None and np.array_equal(labels, previous_labels):
            break
        for group in range(k):
            members = data[labels == group]
            if len(members):
                centers[group] = members.mean(axis=0)
        previous_labels = labels.copy()
    # Reassign after the final update, even when max_iter is reached.
    squared = ((data[:, None, :] - centers[None, :, :]) ** 2).sum(axis=-1)
    labels = squared.argmin(axis=1)
    inertia = float(squared[np.arange(len(data)), labels].sum())
    return centers, labels, inertia, np.array(history + [inertia])

runs = [kmeans(Z, 3, seed=seed) for seed in range(5)]
cluster_centers, labels, inertia, history = min(runs, key=lambda result: result[2])
print("Inertia:", inertia, "cluster sizes:", np.bincount(labels, minlength=3))
assert np.all(np.diff(history) <= 1e-9)
assert labels.shape == (len(Z),)
np.testing.assert_allclose(inertia, np.sum((Z - cluster_centers[labels]) ** 2))
tiny_data = np.array([[0., 0.], [0., 1.], [10., 10.], [10., 11.]])
_, tiny_labels, tiny_inertia, _ = kmeans(tiny_data, 2, seed=0)
assert tiny_labels[0] == tiny_labels[1] and tiny_labels[2] == tiny_labels[3]
assert tiny_labels[0] != tiny_labels[2]
np.testing.assert_allclose(tiny_inertia, 1.)
_, _, duplicate_inertia, _ = kmeans(np.zeros((4, 2)), 3)
assert duplicate_inertia == 0  # exercises empty-cluster handling
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(embedding[:, 0], embedding[:, 1], c=labels, cmap="viridis", s=18)
ax.set(xlabel="Principal component 1", ylabel="Principal component 2", title="K-means clusters in PCA view")
plt.tight_layout()
plt.show()''', 'Compare k=2, 3, and 4. Lower inertia for larger k alone does not prove better clustering.')], [
('Reconstruct standardized Z using all PCA components.', '', 'full_reconstruction', 'np.testing.assert_allclose(full_reconstruction, Z, atol=1e-12)', '(Z @ Vt.T) @ Vt'),
('Return one count per cluster, including any empty clusters.', '', 'cluster_counts', 'assert cluster_counts.shape == (3,)\nassert cluster_counts.sum() == len(Z)\nnp.testing.assert_array_equal(cluster_counts, [(labels == group).sum() for group in range(3)])', 'np.bincount(labels, minlength=3)')],
'''Independent deliverable: wrap standardization and PCA in reusable functions, compare k=2–6 across five seeds, plot inertia, and explain a cluster-count choice without assuming the synthetic labels are known. Add tests for constant features, a single cluster, duplicate points, and max_iter=1. Describe at least two limitations: sensitivity to scaling, initialization, non-spherical groups, or outliers.''',
['https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html', 'https://numpy.org/doc/stable/user/basics.broadcasting.html'])


SOLUTION_NOTES = [
    ('Multiply the daily duration by the number of days; this is ordinary scalar arithmetic.',
     'The formula is applied to every element of celsius. Multiplication and division happen before adding 32.'),
    ('full takes the requested shape and fill value. Explicit float64 preserves the fractional part.',
     'arange excludes its stop, so 26 includes 25 when counting from 5 in steps of 5.'),
    ('The first colon keeps every row. The -2: slice selects the final two columns and preserves both axes.',
     'Each comparison creates a mask. Their elementwise intersection keeps both endpoints and rejects values outside the interval.'),
    ('The dimensions multiply to 24, matching the number of readings, so reshape only rearranges their interpretation.',
     'Reducing axis 1 adds the columns within each row. keepdims retains the reduced axis with length 1.'),
    ('Squaring is elementwise, so each radius gets its own area. pi is the NumPy constant.',
     'A lower clip bound of zero raises negative entries to zero; None leaves the upper side unbounded.'),
    ('Inserting a length-1 column axis turns offsets into shape (2, 1), so each row receives its own offset.',
     'A (5, 1) column times a (1, 5) row broadcasts to all 25 products.'),
    ('Axis 0 runs over days, so reducing it leaves one mean for each city column.',
     'The cumulative sum contains the total so far. Divide each entry by the number of days included at that position.'),
    ('integers excludes its high bound, so use 7 to allow 6. A fresh generator with seed 99 reproduces the requested sequence.',
     'any(axis=1) marks each trial containing a head. The mean of those Boolean values is the fraction of successful trials.'),
    ('isfinite builds an element mask; all(axis=1) requires every entry in a row to be valid before that row is selected.',
     'nanmedian ignores NaN when estimating the replacement value. where replaces only missing entries.'),
    ('Sorting negative marks gives descending score indices. Taking the first two and applying them to students keeps names aligned.',
     'bincount adds each amount to the total for its code. minlength ensures all three group positions exist.'),
    ('solve directly finds the unknown vector. Substituting the result into the original system checks both equations.',
     'The design columns are ones then x, so the fitted coefficient order is intercept then slope. lstsq returns coefficients first.'),
    ('The slice chooses the rows, and copy separates their storage from the source.',
     'A step of 2 skips every other entry. Basic slicing shares the underlying buffer.'),
    ('Square each feature value and sum across columns, leaving one energy value per row.',
     'Scalar multiplication and addition broadcast across the entire input array.'),
    ('log1p computes the small logarithmic change without first rounding 1+x to a nearby representable value.',
     'Subtracting the maximum makes both shifted scores zero. Their exponentials are both one and normalize to equal weights.'),
    ('The label i survives as the row axis. The repeated j label is summed, giving a dot product for each corresponding row pair.',
     'The window view exposes adjacent pairs. Averaging its final axis produces one mean per complete pair.'),
    ('Find the largest magnitude FFT coefficient, then look up its matching frequency using the actual sample interval.',
     'The forward and inverse real transforms round-trip the signal; n explicitly preserves the original sample count.'),
    ('Dividing every store total by the overall total produces fractions that sum to one.',
     'A mean over the day axis leaves store and product axes. Multiplying by 30 recovers their monthly totals.'),
    ('All orthonormal principal directions preserve the full feature space, so projecting and projecting back reconstructs Z.',
     'bincount counts observations assigned to each nonnegative label. minlength retains slots for empty clusters.'),
]


def build():
    for index, item in enumerate(lessons):
        cells = []
        def md(value):
            cells.append(nbf.v4.new_markdown_cell(clean(value)))
        def code(value, **metadata):
            cells.append(nbf.v4.new_code_cell(clean(value), metadata=metadata))
        previous = f"[← Previous]({lessons[index-1]['slug']}.ipynb)" if index else ''
        following = f"[Next →]({lessons[index+1]['slug']}.ipynb)" if index+1 < len(lessons) else ''
        md(f"# {index:02d} · {item['title']}\n\n**Level:** {item['level']} · **Practice time:** {'60–90' if index >= 16 else '30–50'} minutes\n\n{previous} · [Course guide](../README.md) · {following}\n\n**You will learn:** {item['goals']}\n\n**Prerequisites:** {item['prerequisites']}")
        md('''## How to learn with this notebook

1. Run cells from top to bottom. Predict results before executing each example.
2. Do the **Try it** experiment by editing the example or adding a cell below it.
3. Replace `None` in each exercise with your answer, then rerun its check cell.
4. Consult the solutions at the end only after trying. An untouched exercise prints **Pending**, so Run All succeeds without claiming you solved it.
5. Complete the independent challenge, then restart the kernel and run all cells again.

Each notebook imports its own dependencies and creates its own data. You do not need variables from another notebook. The supplied outputs show a verified reference run; rerun cells to explore your changes.''')
        code('''import numpy as np
np.set_printoptions(precision=4, suppress=True)
print("NumPy version:", np.__version__)''', tags=['setup'])
        for number, (title, explanation, example, experiment) in enumerate(item['sections'], 1):
            md(f"## Step {number} · {title}\n\n{explanation}")
            code(example)
            md(f"**Try it:** {experiment}")
        md('## Your practice exercises\n\nUse the named answer variables. The checks verify your result; they do not require the same approach as the reference solution. If an assertion fails, read the expected value and inspect your shape and dtype.')
        for number, (task, setup, variable, check, solution) in enumerate(item['exercises'], 1):
            md(f"### Exercise {number}\n\n{task}")
            code((setup + '\n\n' if setup else '') + f'{variable} = None  # TODO: replace None with your answer', tags=['exercise'])
            indented = textwrap.indent(check, '    ')
            code(f'if {variable} is None:\n    print("Pending: complete Exercise {number} first.")\nelse:\n{indented}\n    print("Exercise {number} passed!")', tags=['exercise-check'])
        md(f"## Independent challenge\n\n{item['challenge']}\n\nAdd code and explanation cells below. Decide on expected results before checking your implementation.")
        code('# Your independent challenge work goes here.', tags=['challenge'])
        md('''## Before you move on

- Explain the main idea in your own words without reading the examples.
- Make both exercise checks print **passed**.
- Try at least one changed input or edge case and explain the result.
- Finish the independent challenge or write down a specific question to revisit.

Expertise comes from repeated practice and debugging unfamiliar problems. Completing these notebooks gives you a broad practical foundation, not a substitute for that experience.

---

## Reference solutions — try first

These cells use separate reference variables, so they do not fill in your exercise answers. They also check the reference result. Compare your reasoning as well as the output.''')
        for number, (task, setup, variable, check, solution) in enumerate(item['exercises'], 1):
            md(f'### Solution {number}\n\n{task}\n\n**Why it works:** {SOLUTION_NOTES[index][number-1]}')
            ref = f'reference_{variable}'
            code(f'{ref} = {solution}\n{check.replace(variable, ref)}\nprint({ref})', tags=['solution'], jupyter={'source_hidden': True})
        md('## Continue learning\n\n' + '\n'.join(f'- [Official NumPy documentation: {url.rsplit("/", 1)[-1].replace(".html", "")} ]({url})' for url in item['references']) + f'\n\n{following}')
        nb = nbf.v4.new_notebook(cells=cells, metadata={
            'kernelspec': {'display_name': 'Python 3 (ipykernel)', 'language': 'python', 'name': 'python3'},
            'language_info': {'name': 'python', 'version': '3.12'},
            'course': {'level': item['level'], 'sequence': index, 'title': item['title']},
        })
        # Stable IDs keep rebuild diffs focused on content.
        for cell_index, cell in enumerate(nb.cells):
            cell.id = f'lesson-{index:02d}-cell-{cell_index:03d}'
        nbf.validate(nb)
        nbf.write(nb, OUT / f"{item['slug']}.ipynb")
    print(f'Built {len(lessons)} notebooks in {OUT}')


if __name__ == '__main__':
    build()
