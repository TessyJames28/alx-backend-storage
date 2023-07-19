#!/usr/bin/env python3
"""Write string to Redis"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """a decorator that counts the number of times cache method was called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """function that wraps the decorator and returns a wrapper"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """function that wraps the decorator and returns a wrapper"""
        input = str(args)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """display the history of calls of a particular function"""
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


class Cache:
    """a class Cache"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
