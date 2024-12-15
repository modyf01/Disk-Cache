# MatrixDiskCache

MatrixDiskCache is a lightweight Python library designed to cache function results to disk. It ensures that the results of expensive computations are saved locally, enabling reuse between multiple program executions. With support for caching complex data structures like NumPy arrays and pandas Series/DataFrames, it offers robust functionality for modern data-intensive applications.

## Features

- **Persistent Caching**: Cache function results to disk to reuse them across program runs.
- **Support for Complex Data**: Handles `numpy.ndarray`, `pandas.Series`, and `pandas.DataFrame` objects seamlessly.
- **Customizable Cache Size**: Set a maximum size for the cache directory to limit storage usage.
- **Easy to Use**: Decorate your functions with `@cache` to enable caching immediately.

---

## Installation

You can install MatrixDiskCache via pip (soon to be available on PyPI):

```bash
pip install matrix-disk-cache
```
---

## Quickstart

Here is an example demonstrating how to use MatrixDiskCache:

```python
from matrix_disk_cache import MatrixDiskCache

# Initialize the cache with an optional maxsize
cache = MatrixDiskCache(cache_dir="my_cache", maxsize=100)

@cache.cache
def expensive_computation(x, y):
    print("Computing...")
    return x + y

# First call computes and caches the result
result = expensive_computation(2, 3)  # Output: Computing...
print(result)  # Output: 5

# Second call retrieves the result from cache
result = expensive_computation(2, 3)  # No "Computing..." this time
print(result)  # Output: 5
```

---

## Advanced Usage

### Caching Complex Data

MatrixDiskCache supports caching of complex data types such as NumPy arrays and pandas Series/DataFrames. These are serialized into a hashable format to ensure uniqueness.

```python
import numpy as np
import pandas as pd

@cache.cache
def process_data(array, series):
    return array.mean() + series.sum()

arr = np.array([1, 2, 3])
ser = pd.Series([4, 5, 6])

# Compute and cache the result
result = process_data(arr, ser)

# Fetch the cached result
result = process_data(arr, ser)
```

### Limiting Cache Size

Set a maximum number of cached results using the `maxsize` parameter. Oldest files are deleted when the limit is exceeded:

```python
cache = MatrixDiskCache(cache_dir="limited_cache", maxsize=50)
```

---

## API Reference

### `MatrixDiskCache`

#### Initialization
```python
MatrixDiskCache(cache_dir: str = ".matrix_cache", maxsize: int = None)
```
- **`cache_dir`**: Directory to store cached results (default: `.matrix_cache`).
- **`maxsize`**: Maximum number of cache files (default: `None`, unlimited).

#### Methods

- **`cache(func)`**:
    Decorator to enable caching for the given function. Results are cached based on the function name and its arguments.

---

## Testing

To run tests:

```bash
pytest tests
```

---

## Contributing

Contributions are welcome! If you have ideas for new features or improvements, please open an issue or submit a pull request.

---

## License

MatrixDiskCache is licensed under the MIT License.

---

## Acknowledgments

Inspired by `functools.lru_cache`, with an emphasis on persistent disk caching and support for data science workflows.

