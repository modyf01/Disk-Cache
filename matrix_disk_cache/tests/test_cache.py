import os
import numpy as np
import pandas as pd
import shutil
import pytest

from matrix_disk_cache import MatrixDiskCache

@pytest.fixture
def clean_cache():
    cache_dir = ".my_cache"
    yield cache_dir
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

def test_cache_basic(clean_cache):
    cache = MatrixDiskCache(cache_dir=clean_cache)

    @cache.cache
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
    assert add(2, 3) == 5

def test_cache_numpy(clean_cache):
    cache = MatrixDiskCache(cache_dir=clean_cache)

    @cache.cache
    def process(arr):
        return arr.mean()

    arr = np.array([1, 2, 3])

    assert process(arr) == 2.0
    assert process(arr) == 2.0

def test_cache_pandas(clean_cache):
    cache = MatrixDiskCache(cache_dir=clean_cache)

    @cache.cache
    def process(series):
        return series.sum()

    series = pd.Series([4, 5, 6])

    assert process(series) == 15
    assert process(series) == 15

def test_cache_random_matrix_numpy(clean_cache):
    cache = MatrixDiskCache(cache_dir=clean_cache)

    @cache.cache
    def generate_matrix(rows, cols, first_row):
        data = np.random.rand(rows, cols)
        data[0] = first_row
        return data

    first_row = [1, 2, 3]
    arr1 = generate_matrix(3, 3, first_row)
    arr2 = generate_matrix(3, 3, first_row)

    assert np.array_equal(arr1, arr2)

def test_cache_random_matrix_pandas(clean_cache):
    cache = MatrixDiskCache(cache_dir=clean_cache)

    @cache.cache
    def generate_matrix(rows, cols, first_row):
        data = np.random.rand(rows, cols)
        data[0] = first_row
        return pd.DataFrame(data)

    first_row = [1, 2, 3]
    df1 = generate_matrix(3, 3, first_row)
    df2 = generate_matrix(3, 3, first_row)

    assert df1.equals(df2)

def test_cache_dataframe_sum_pandas(clean_cache):
    cache = MatrixDiskCache(cache_dir=clean_cache)

    @cache.cache
    def sum_dataframe(df):
        return df.values.sum()

    df1 = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
    df2 = pd.DataFrame([[7, 8, 9], [10, 11, 12]])

    assert sum_dataframe(df1) == 21
    assert sum_dataframe(df1) == 21
    assert sum_dataframe(df2) == 57
    assert sum_dataframe(df2) == 57

def test_cache_matrix_sum_numpy(clean_cache):
    cache = MatrixDiskCache(cache_dir=clean_cache)

    @cache.cache
    def sum_matrix(arr):
        return arr.sum()

    arr1 = np.array([[1, 2, 3], [4, 5, 6]])
    arr2 = np.array([[7, 8, 9], [10, 11, 12]])

    assert sum_matrix(arr1) == 21
    assert sum_matrix(arr1) == 21
    assert sum_matrix(arr2) == 57
    assert sum_matrix(arr2) == 57

class CollidingObject:
    def __init__(self, value, identifier):
        self.value = value
        self.identifier = identifier

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, CollidingObject):
            return self.identifier == other.identifier
        return False

def test_cache_hash_collision(clean_cache):
    cache = MatrixDiskCache(cache_dir=clean_cache)

    @cache.cache
    def process(obj):
        return f"Processed-{obj.identifier}"

    obj1 = CollidingObject(value=123, identifier="A")
    obj2 = CollidingObject(value=123, identifier="B")

    assert hash(obj1) == hash(obj2)
    assert obj1 != obj2

    result1 = process(obj1)
    result2 = process(obj2)

    assert result1 == "Processed-A"
    assert result2 == "Processed-B"

class NonHashableObject:
    def __init__(self, value):
        self.value = value

def test_cache_non_hashable(clean_cache):
    cache = MatrixDiskCache(cache_dir=clean_cache)

    call_count = {"count": 0}

    @cache.cache
    def process(obj):
        call_count["count"] += 1
        return f"Processed-{obj.value}"

    obj1 = NonHashableObject(value="Test1")
    obj2 = NonHashableObject(value="Test2")

    result1 = process(obj1)
    result2 = process(obj2)

    assert result1 == "Processed-Test1"
    assert result2 == "Processed-Test2"

    result1_cached = process(obj1)
    result2_cached = process(obj2)

    assert result1_cached == result1
    assert result2_cached == result2

    assert call_count["count"] == 2
