from typing import Optional

class OpenAddressingHashTable:
    def __init__(self, size: int = 8, hash_func=hash, probe_type='linear'):
        self.size = size
        self.hash_func = hash_func
        self.probe_type = probe_type
        self.table = [None] * size
        self.count = 0

    def _resize(self):
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0
        for item in old_table:
            if item:
                self.insert(*item)

    def _probe(self, key: str, i: int) -> int:
        h1 = self.hash_func(key) % self.size
        if self.probe_type == 'linear':
            return (h1 + i) % self.size
        elif self.probe_type == 'double':
            h2 = 1 + (self.hash_func(key) % (self.size - 1))
            return (h1 + i * h2) % self.size
        else:
            raise ValueError("Unknown probe type")

    def insert(self, key: str, value: any):
        if self.count / self.size > 0.7:
            self._resize()
        for i in range(self.size):
            index = self._probe(key, i)
            if self.table[index] is None or self.table[index][0] == key:
                if self.table[index] is None:
                    self.count += 1
                self.table[index] = (key, value)
                return

    def search(self, key: str) -> Optional[any]:
        for i in range(self.size):
            index = self._probe(key, i)
            if self.table[index] is None:
                return None
            if self.table[index][0] == key:
                return self.table[index][1]
        return None

    def delete(self, key: str):
        for i in range(self.size):
            index = self._probe(key, i)
            if self.table[index] is None:
                return
            if self.table[index][0] == key:
                self.table[index] = None
                self.count -= 1
                return
