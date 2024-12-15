import os
import numpy as np
import pandas as pd
from matrix_disk_cache import MatrixDiskCache


def test_cache_basic():
    cache = MatrixDiskCache(cache_dir=".test_cache")

    @cache.disk_cache
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
    assert add(2, 3) == 5

    os.system("rm -r .test_cache")

def test_cache_numpy():
    cache = MatrixDiskCache(cache_dir=".test_cache")

    @cache.disk_cache
    def process(arr):
        return arr.mean()

    arr = np.array([1, 2, 3])

    assert process(arr) == 2.0
    assert process(arr) == 2.0

    os.system("rm -r .test_cache")

def test_cache_pandas():
    cache = MatrixDiskCache(cache_dir=".test_cache")

    @cache.disk_cache
    def process(series):
        return series.sum()

    series = pd.Series([4, 5, 6])

    assert process(series) == 15
    assert process(series) == 15

    os.system("rm -r .test_cache")

def test_cache_random_matrix_numpy():
    cache = MatrixDiskCache(cache_dir=".test_cache")

    @cache.disk_cache
    def generate_matrix(rows, cols, first_row):
        data = np.random.rand(rows, cols)
        data[0] = first_row
        return data

    first_row = [1, 2, 3]
    arr1 = generate_matrix(3, 3, first_row)
    arr2 = generate_matrix(3, 3, first_row)

    # The numpy arrays generated should be cached and identical
    assert np.array_equal(arr1, arr2)

    os.system("rm -r .test_cache")

def test_cache_random_matrix_pandas():
    cache = MatrixDiskCache(cache_dir=".test_cache")

    @cache.disk_cache
    def generate_matrix(rows, cols, first_row):
        data = np.random.rand(rows, cols)
        data[0] = first_row
        return pd.DataFrame(data)

    first_row = [1, 2, 3]
    df1 = generate_matrix(3, 3, first_row)
    df2 = generate_matrix(3, 3, first_row)

    # The DataFrame generated should be cached and identical
    assert df1.equals(df2)

    os.system("rm -r .test_cache")

def test_cache_dataframe_sum_pandas():
    cache = MatrixDiskCache(cache_dir=".test_cache")

    @cache.disk_cache
    def sum_dataframe(df):
        return df.values.sum()

    df1 = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
    df2 = pd.DataFrame([[7, 8, 9], [10, 11, 12]])

    # Cached results for the same DataFrame should be identical
    assert sum_dataframe(df1) == 21
    assert sum_dataframe(df1) == 21

    # Different DataFrame should have different results
    assert sum_dataframe(df2) == 57
    assert sum_dataframe(df2) == 57

    os.system("rm -r .test_cache")

def test_cache_matrix_sum_numpy():
    cache = MatrixDiskCache(cache_dir=".test_cache")

    @cache.disk_cache
    def sum_matrix(arr):
        return arr.sum()

    arr1 = np.array([[1, 2, 3], [4, 5, 6]])
    arr2 = np.array([[7, 8, 9], [10, 11, 12]])

    # Cached results for the same numpy array should be identical
    assert sum_matrix(arr1) == 21
    assert sum_matrix(arr1) == 21

    # Different numpy arrays should have different results
    assert sum_matrix(arr2) == 57
    assert sum_matrix(arr2) == 57

    os.system("rm -r .test_cache")
