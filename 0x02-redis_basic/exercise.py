#!/usr/bin/env python3
"""Write string to Redis"""
import redis
import uuid
from typing import Union


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
