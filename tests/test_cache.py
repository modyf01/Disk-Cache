import os
import numpy as np
import pandas as pd
from disk_cache import DiskCache


def test_cache_basic():
    cache = DiskCache(cache_dir=".test_cache")

    @cache.cache
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
    assert add(2, 3) == 5

    os.system("rm -r .test_cache")


def test_cache_numpy_pandas():
    cache = DiskCache(cache_dir=".test_cache")

    @cache.cache
    def process(arr, series):
        return arr.mean() + series.sum()

    arr = np.array([1, 2, 3])
    series = pd.Series([4, 5, 6])

    assert process(arr, series) == 21
    assert process(arr, series) == 21

    os.system("rm -r .test_cache")