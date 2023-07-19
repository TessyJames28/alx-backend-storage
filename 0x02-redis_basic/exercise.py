#!/usr/bin/env python3
"""Write string to Redis"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """a class Cache"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ a method that takes data argument and returns a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """a get method to read from redis"""
        val = self._redis.get(key)
        if fn:
            return fn(val)
        return val

    def get_str(self, key: str) -> str:
        """ convert value to str format """
        val = self._redis.get(key)
        return val.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ convert value to int format """
        val = self._redis.get(key)
        return val.decode("utf-8")
