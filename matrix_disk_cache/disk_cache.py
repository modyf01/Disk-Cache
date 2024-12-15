import hashlib
import os
import pickle
from functools import wraps
from typing import Callable, Any

import numpy as np
import pandas as pd


class MatrixDiskCache:
    def __init__(self, cache_dir: str = ".matrix_disk_cache", maxsize: int = None):
        """
        Initialize the DiskCache.

        :param cache_dir: Directory where cache files will be stored.
        :param maxsize: Maximum number of cache files to retain. If None, no limit.
        """
        self.cache_dir = cache_dir
        self.maxsize = maxsize
        os.makedirs(cache_dir, exist_ok=True)

    def _convert_to_hashable(self, obj: Any) -> Any:
        """
        Convert complex objects like numpy arrays or pandas Series/DataFrame into hashable representations.

        :param obj: The object to convert.
        :return: A hashable representation of the object.
        """
        if isinstance(obj, np.ndarray):
            return obj.tobytes()  # Convert ndarray to bytes
        elif isinstance(obj, (pd.Series, pd.DataFrame)):
            return obj.to_numpy().tobytes()  # Convert pandas objects to bytes
        elif isinstance(obj, (list, tuple)):
            return tuple(self._convert_to_hashable(x) for x in obj)  # Handle nested structures
        elif isinstance(obj, dict):
            return tuple((k, self._convert_to_hashable(v)) for k, v in obj.items())  # Handle dictionaries
        else:
            return obj  # Keep other types unchanged

    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """
        Generate a unique key for a function call based on its name and arguments.

        :param func_name: Name of the function.
        :param args: Positional arguments of the function.
        :param kwargs: Keyword arguments of the function.
        :return: A hash key as a string.
        """
        # Convert arguments to hashable representations
        hashable_args = tuple(self._convert_to_hashable(arg) for arg in args)
        hashable_kwargs = frozenset((k, self._convert_to_hashable(v)) for k, v in kwargs.items())

        # Serialize and hash
        key_data = (func_name, hashable_args, hashable_kwargs)
        return hashlib.md5(pickle.dumps(key_data)).hexdigest()

    def _get_cache_path(self, key: str) -> str:
        """
        Get the path to the cache file for a given key.

        :param key: Cache key.
        :return: Path to the cache file.
        """
        return os.path.join(self.cache_dir, f"{key}.cache")

    def _enforce_maxsize(self):
        """
        Ensure that the number of cache files does not exceed the maximum size.
        If the limit is exceeded, remove the oldest files.
        """
        if self.maxsize is not None:
            cache_files = sorted(
                (os.path.join(self.cache_dir, f) for f in os.listdir(self.cache_dir)),
                key=os.path.getmtime
            )
            while len(cache_files) > self.maxsize:
                os.remove(cache_files.pop(0))

    def disk_cache(self, func: Callable) -> Callable:
        """
        Decorator to cache a function's result on disk.

        :param func: The function to cache.
        :return: The wrapped function with caching.
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = self._generate_key(func.__name__, args, kwargs)
            cache_path = self._get_cache_path(key)

            if os.path.exists(cache_path):
                # Load result from cache
                with open(cache_path, 'rb') as cache_file:
                    return pickle.load(cache_file)

            # Compute result and save to cache
            result = func(*args, **kwargs)
            with open(cache_path, 'wb') as cache_file:
                pickle.dump(result, cache_file)

            # Enforce maxsize constraint
            self._enforce_maxsize()

            return result

        return wrapper
