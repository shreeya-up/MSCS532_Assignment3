
class HashTable:
    def __init__(self, m=8):
        self.m = m
        self.table = [[] for _ in range(m)]
        self.n =0

    def _hash(self, key):
        return hash(key) % self.m

    def insert(self, key, value):
        i = self._hash(key)
        for j, (k, v) in enumerate(self.table[i]):
            if k == key:
                self.table[i][j] = (key, value)
                return
        self.table[i].append((key, value))
        self.n += 1
            