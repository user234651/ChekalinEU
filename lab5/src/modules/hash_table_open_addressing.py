from typing import Any, Optional
from modules.hash_functions import HashFunction

class _Deleted:
    pass

class OpenAddressingHashTable:
    """Открытая адресация: поддержка линейного пробирования и двойного хеширования.

    Временная сложность операций:
    - average: insert/get/delete — O(1) (при низкой нагрузке и хорошем хешировании)
    - worst: insert/get/delete — O(n)
    """

    def __init__(self, initial_capacity: int = 17, method: str = 'linear', hash_fn: HashFunction = None):
        self._capacity = initial_capacity
        self._keys = [None] * self._capacity
        self._values = [None] * self._capacity
        self._size = 0
        self._deleted = _Deleted()
        self._method = method
        self._hash_fn = hash_fn or HashFunction(lambda k: sum(ord(c) for c in k), "sum_hash")

    @property
    def size(self):
        return self._size

    def capacity(self):
        return self._capacity

    def _resize(self, new_capacity: int) -> None:
        old_keys = self._keys
        old_values = self._values

        self._capacity = new_capacity
        self._keys = [None] * self._capacity
        self._values = [None] * self._capacity
        self._size = 0

        for k, v in zip(old_keys, old_values):
            if k is not None and k is not self._deleted:
                self.insert(k, v)


    def _probe(self, key: str, i: int) -> int:
        h1 = self._hash_fn(key) % self._capacity
        if self._method == 'linear':
            return (h1 + i) % self._capacity
        elif self._method == 'double':
            h2 = 1 + (self._hash_fn(key) % (self._capacity - 1))
            return (h1 + i * h2) % self._capacity
        else:
            return (h1 + i) % self._capacity

    def _find_slot(self, key: str) -> int:
        for i in range(self._capacity):
            idx = self._probe(key, i)
            k = self._keys[idx]
            if k is None or k is self._deleted or k == key:
                return idx
        return -1

    def insert(self, key: str, value: Any) -> None:
        if self._size / self._capacity > 0.6:
            self._resize(self._capacity * 2 + 1)

        slot = self._find_slot(key)
        if slot == -1:
            return

        if self._keys[slot] is None or self._keys[slot] is self._deleted:
            self._keys[slot] = key
            self._values[slot] = value
            self._size += 1
        else:
            self._values[slot] = value

    def get(self, key: str) -> Optional[Any]:
        for i in range(self._capacity):
            idx = self._probe(key, i)
            k = self._keys[idx]
            if k is None:
                return None
            if k is self._deleted:
                continue
            if k == key:
                return self._values[idx]
        return None

    def delete(self, key: str) -> bool:
        for i in range(self._capacity):
            idx = self._probe(key, i)
            k = self._keys[idx]
            if k is None:
                return False
            if k is self._deleted:
                continue
            if k == key:
                self._keys[idx] = self._deleted
                self._values[idx] = None
                self._size -= 1
                return True
        return False
