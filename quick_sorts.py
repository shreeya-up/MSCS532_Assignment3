import random

# Code for Quicksort
def partition(a, lo, hi, p_index):
    """Decides on the pivot index based on the p_index parameter and partitions the array."""
    if p_index == "random":
        m = random.randint(lo, hi)
    elif p_index == "first":
        m = lo
    elif p_index == "median3":
        mid = (lo + hi) // 2
        m = sorted((lo, mid, hi), key=lambda i: a[i])[1]
    else:
        m = hi
    a[m], a[hi] = a[hi], a[m]
    x = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= x:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1

def quick_sort(a, p_index):
    """Sorts the array in place using the quicksort algorithm."""
    def sort(lo, hi):
        while lo<hi:
            q = partition(a, lo, hi, p_index)
            if q - lo < hi - q:
                sort(lo, q - 1)
                lo = q + 1
            else:
                sort(q + 1, hi)
                hi = q - 1
    sort(0, len(a) - 1)

def det_quick_sort(a):
       """Sorts the array in place using the deterministic quicksort algorithm."""
       quick_sort(a, "first")

def ran_quick_sort(a):
    """Sorts the array in place using the randomized quicksort algorithm."""
    quick_sort(a, "random")