from typing import List, Tuple, Optional

class ChainingHashTable:
    def __init__(self, size: int = 8, hash_func=hash):
        self.size = size
        self.hash_func = hash_func
        self.table: List[List[Tuple[str, any]]] = [[] for _ in range(size)]
        self.count = 0

    def _resize(self):
        new_size = self.size * 2
        new_table: List[List[Tuple[str, any]]] = [[] for _ in range(new_size)]
        for bucket in self.table:
            for key, value in bucket:
                index = self.hash_func(key) % new_size
                new_table[index].append((key, value))
        self.size = new_size
        self.table = new_table

    def insert(self, key: str, value: any):
        if self.count / self.size > 0.7:
            self._resize()
        index = self.hash_func(key) % self.size
        for i, (k, _) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))
        self.count += 1

    def search(self, key: str) -> Optional[any]:
        index = self.hash_func(key) % self.size
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key: str):
        index = self.hash_func(key) % self.size
        for i, (k, _) in enumerate(self.table[index]):
            if k == key:
                self.table[index].pop(i)
                self.count -= 1
                return
