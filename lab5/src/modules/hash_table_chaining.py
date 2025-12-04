from typing import Any, List
from modules.hash_functions import HashFunction

class _Node:
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value

class HashTableChaining:
    """Метод цепочек c динамическим масштабированием.

    Временная сложность операций:
    - average: insert/get/delete — O(1)
    - worst: insert/get/delete — O(n)
    """

    def __init__(self, initial_capacity: int = 11, hash_fn: HashFunction = None):
        self._buckets: List[List[_Node]] = [[] for _ in range(initial_capacity)]
        self._size = 0
        self._hash_fn = hash_fn or HashFunction(lambda k: sum(ord(c) for c in k), "sum_hash")

    @property
    def size(self):
        return self._size

    def capacity(self):
        return len(self._buckets)

    def _index(self, key: str) -> int:
        return self._hash_fn(key) % self.capacity()

    def insert(self, key: str, value: Any) -> None:
        idx = self._index(key)
        bucket = self._buckets[idx]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(_Node(key, value))
        self._size += 1

        if self._size / self.capacity() > 0.75:
            self._resize(self.capacity() * 2 + 1)

    def get(self, key: str):
        idx = self._index(key)
        for node in self._buckets[idx]:
            if node.key == key:
                return node.value
        return None

    def delete(self, key: str) -> bool:
        idx = self._index(key)
        bucket = self._buckets[idx]

        for i, node in enumerate(bucket):
            if node.key == key:
                del bucket[i]
                self._size -= 1

                if self.capacity() > 11 and self._size / self.capacity() < 0.2:
                    new_cap = max(11, (self.capacity() // 2) | 1)
                    self._resize(new_cap)

                return True

        return False

    def _resize(self, new_capacity: int) -> None:
        old = self._buckets
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0

        for bucket in old:
            for node in bucket:
                self.insert(node.key, node.value)

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None
