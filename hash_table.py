
class HashTable:
    def __init__(self, m=8):
        self.m = m
        self.table = [[] for _ in range(m)]
        self.n =0

    def _hash(self, key):
        return hash(key) % self.m

    def insert(self, key, value):
        i = self._hash(key)
        self