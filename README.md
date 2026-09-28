# Assignment 3: Understanding Algorithm Efficiency and Scalability

This repository contains Python implementations and analysis for two topics:

1. **Randomized Quicksort**, compared empirically against Deterministic Quicksort (first-element pivot).
2. **Hashing with Chaining**, using a universal hash function, with optional dynamic resizing.

## Repository layout

| File | Purpose |
|---|---|
| `quick_sorts.py` | `partition`, `quick_sort`, `det_quick_sort` (first-element pivot) and `ran_quick_sort` (random pivot) |
| `tests_quicksort.py` | Correctness tests: compares both sorts against Python's `sorted()` |
| `compare_and_visualise.py` | Benchmark: runtime and peak memory on four dataset types, saves `results.png` |
| `hash_table.py` | `HashTable` class: chaining, universal hashing, insert / search / delete (and resizing, if you use the extended version) |
| `tests_hash_table.py` | Correctness tests for the hash table, including forced collisions and a comparison against `dict` |
| `benchmark_hash_table.py` | *(Optional)* Load factor and search time, with and without resizing; saves `hash_table_results.png` |
| `report` | Theoretical analysis, empirical comparison and discussion |

> Adjust the file names above to match the ones actually in your repository.

## Requirements

- Python 3.8 or newer
- `matplotlib` for the benchmark plots

```
pip install matplotlib
```

## How to run

Run every command from the repository folder.

**1. Check correctness first**
```
python tests_quicksort.py
python tests_hash_table.py
```
Each script prints a confirmation for every test and raises an `AssertionError` if something fails.

**2. Quicksort benchmark**
```
python compare_and_visualise.py
```
Runs both sorts on input sizes 500, 1000, 1500 and 2000 across four datasets (random, sorted, reverse sorted, repeated elements). It prints progress, saves `results.png` and opens the plot. Top row: runtime. Bottom row: peak extra memory.

The sorted and reverse-sorted runs with the first-element pivot are Θ(n²), so keep the sizes modest.

**3. Hash table benchmark (optional)**
```
python benchmark_hash_table.py
```
Inserts 4000 keys into a table with resizing and a table fixed at 8 slots, recording load factor and mean search time every 200 inserts. Saves `hash_table_results.png`.

## Using the code

```python
from quick_sorts import ran_quick_sort, det_quick_sort

data = [5, 2, 9, 1, 5, 6]
ran_quick_sort(data)          # sorts in place
print(data)                   # [1, 2, 5, 5, 6, 9]
```

```python
from hash_table import HashTable

ht = HashTable()
ht.insert("apple", 3)
ht.insert("apple", 7)         # updates the existing key
print(ht.search("apple"))     # 7
ht.delete("apple")
ht.search("apple")            # raises KeyError
```

## Implementation notes

**Quicksort**
- In place, using Lomuto partitioning with a `<=` comparison.
- Recurses on the smaller partition and loops on the larger one, so stack depth stays O(log n). This prevents recursion-limit errors, but it does not change the running time.
- `ran_quick_sort` picks the pivot uniformly at random. `det_quick_sort` always picks the first element.

**Hash table**
- Collisions are resolved by chaining. Each slot holds a list of `(key, value)` pairs.
- Hash function: `h(k) = ((a·k + b) mod p) mod m`, with `p = 2^61 − 1` and random `a`, `b` chosen when the table is created.
- `hash(key)` is reduced mod `p` first, which handles the negative values Python's `hash()` can return.
- `insert` updates the value if the key already exists. `search` and `delete` raise `KeyError` for missing keys, like a built-in `dict`.
- With resizing enabled, the table doubles when the load factor n/m exceeds 1, and every key is rehashed.

## Summary of findings

### Part 1: Randomized Quicksort

- **Average case:** using indicator random variables, the expected number of comparisons is `2(n+1)Hₙ − 4n = Θ(n log n)` for any input of distinct keys. A direct count at n = 1024 averaged about 11,350 comparisons against a predicted 11,298.
- **Random data:** both algorithms grow as Θ(n log n). Deterministic was slightly faster, since randomized pays for a `random.randint` call on every partition.
- **Sorted and reverse-sorted data:** deterministic Quicksort degraded to Θ(n²). At n = 2000 it took roughly 0.08 s and 0.16 s, against a few milliseconds for randomized.
- **Repeated elements:** both algorithms grew roughly quadratically. With the `<=` partition, every element ties with the pivot, so each split is (n−1, 0) whichever index is chosen. The average-case proof assumes distinct keys, so its guarantee does not apply here. Three-way partitioning is the standard fix, and it is not implemented.
- Memory use was small and noisy for both algorithms. Both are in place, and `tracemalloc` does not capture the recursion stack.

### Part 2: Hashing with Chaining

- **Expected time:** under simple uniform hashing, search, insert and delete are all Θ(1 + α), where α = n/m is the load factor.
- **Load factor:** without resizing, 4000 keys in 8 slots gives α = 500 and search time rises steadily. With resizing (threshold α > 1, doubling), α stays near 1 and search time stays flat over 9 resizes.
- **Why doubling:** a single resize costs Θ(n), but the sizes form a geometric series, so the amortized cost per insert is O(1).
- **Universal hashing** protects against adversarial key sets in the same way that a random pivot protects against adversarial arrays.

## Reference

Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms* (CLRS): the chapters on Quicksort (randomized analysis) and Hash Tables (chaining, load factor, universal hashing).
