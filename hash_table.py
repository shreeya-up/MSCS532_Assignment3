import random


class HashTable:
    def __init__(self, m=8):
        self.m = m                              # number of slots in the hash table
        self.table = [[] for _ in range(m)]     # initialize the hash table with empty lists
        self.n =0                               # number of key-value pairs in the hash table
        self.p = 2**61 - 1                     # large prime number
        self.a = random.randint(1, self.p - 1)  # random coefficient
        self.b = random.randint(0, self.p - 1)  # random offset

    def _hash(self, key):
        k = hash(key) % self.p              # Deals with negative hash values, maps to different results
        return ((self.a * k + self.b) % self.p) % self.m

    def insert(self, key, value):
        i = self._hash(key)
        for j, (k, v) in enumerate(self.table[i]):
            if k == key:
                self.table[i][j] = (key, value)     # update existing key-value pair when found
                return
        self.table[i].append((key, value))          # add new key-value pair if not found
        self.n += 1

    def search(self, key):
        i = self._hash(key)
        for k, v in self.table[i]:
            if k == key:
                return v
        raise KeyError(key)

    def delete(self, key):
        i = self._hash(key)
        for j, (k, v) in enumerate(self.table[i]):
            if k == key:
                self.table[i].pop(j)        # remove the key-value pair if found
                self.n -= 1                 # reduce the count of key-value pairs
                return
        raise KeyError(key)