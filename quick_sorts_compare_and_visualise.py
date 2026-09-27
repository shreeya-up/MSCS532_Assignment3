import random
import time
import tracemalloc
import matplotlib.pyplot as plt

from quick_sorts import ran_quick_sort, det_quick_sort

# This script compares the performance of randomized quicksort and deterministic quicksort algorithms on random data and visualizes the results.
# AI has been used to write some of the code for this script, but it has been reviewed and modified by me to ensure accuracy and clarity.

size = [500, 1000, 1500, 2000]
types = ["random", "sorted", "reverse", "repeated"]
algorithms = {
    "Randomized quick sort": ran_quick_sort,
    "Deterministic quick sort": det_quick_sort,
}

# Building the input data
def build_data(type, n):
    if type == "random":
        return random.sample(range(n), n)
    if type == "sorted":
        return list(range(n))
    if type == "reverse":
        return list(range(n, 0, -1))
    if type == "repeated":
        return [random.randint(0, 20) for _ in range(n)]


#Measure the time taken by a sorting algorithm to sort an array
def measure_time(sort_func, data):
    best = float("inf")
    for _ in range(3):
        copy = data[:]
        start = time.perf_counter()
        sort_func(copy)
        best = min(best, time.perf_counter() - start)
    return best

def measure_memory(sort_func, data):
    copy = data[:]
    tracemalloc.start()
    sort_func(copy)
    peak  = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return peak/1024        # Conversion to kB

# Run and visualize the results

times = {}
memory = {}
for type in types:
    for name, sort_func in algorithms.items():
        times[(type, name)] = []
        memory[(type, name)] = []
        for n in size:
            data = build_data(type, n)
            times[(type, name)].append(measure_time(sort_func, data))
            memory[(type, name)].append(measure_memory(sort_func, data))
            print(type, name, n, "done")


# Plotting the results
fig, axes = plt.subplots(2, 4, figsize=(15, 8))
for col, type in enumerate(types):
    for name in algorithms:
        axes[0][col].plot(size, times[(type, name)], marker="o", label=name)
        axes[1][col].plot(size, memory[(type, name)], marker="o", label=name)
    axes[0][col].set_title(type)
    axes[0][col].set_ylabel("time (seconds)")
    axes[1][col].set_ylabel("peak extra memory (KiB)")
    axes[1][col].set_xlabel("n (number of elements)")
axes[0][0].legend()
plt.tight_layout()
plt.savefig("results.png", dpi=150)
plt.show()