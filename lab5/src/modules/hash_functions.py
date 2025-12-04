from typing import Callable

class HashFunction:
    def __init__(self, fn: Callable[[str], int], name: str = None):
        self.fn = fn
        self.name = name or fn.__name__


    def __call__(self, key: str) -> int:
        return self.fn(key)

# 1) Простая хеш-функция: сумма кодов символов
def sum_hash(key: str) -> int:
    s = 0
    for ch in key:
        s += ord(ch)
    return s

# 2) Полиномиальная хеш-функция (rolling polynomial)
def poly_hash(key: str, base: int = 257) -> int:
    h = 0
    for ch in key:
        h = h * base + ord(ch)
    return h

# 3) DJB2
def djb2_hash(key: str) -> int:
    h = 5381
    for ch in key:
        h = ((h << 5) + h) + ord(ch) # h * 33 + c
    return h & 0xFFFFFFFFFFFFFFFF
