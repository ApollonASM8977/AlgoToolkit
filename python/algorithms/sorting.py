# © 2026 Aboubacar Sidick Meite (ApollonIUGB77) — All Rights Reserved
"""
Sorting Algorithms — 8 implementations with step-by-step tracing and complexity metadata.

Each function accepts a list of comparables and returns a SortResult dataclass with:
  - sorted array
  - number of comparisons and swaps
  - time complexity (best / average / worst)
  - space complexity
  - optional step trace

Algorithms:
  bubble_sort      O(n²)   stable
  selection_sort   O(n²)   unstable
  insertion_sort   O(n²)   stable
  merge_sort       O(n log n) stable
  quick_sort       O(n log n) avg, O(n²) worst — unstable
  heap_sort        O(n log n) unstable
  counting_sort    O(n+k)  stable  (integers only)
  radix_sort       O(nk)   stable  (non-negative integers only)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import copy


# ── Result type ────────────────────────────────────────────────────────────────

@dataclass
class SortResult:
    algorithm:    str
    original:     list
    sorted_arr:   list
    comparisons:  int
    swaps:        int
    complexity:   dict          # best / average / worst / space
    steps:        list[dict] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"[{self.algorithm}] "
            f"{len(self.sorted_arr)} elements | "
            f"{self.comparisons} comparisons | "
            f"{self.swaps} swaps | "
            f"avg O({self.complexity['average']})"
        )


# ── Helpers ────────────────────────────────────────────────────────────────────

def _complexity(best: str, avg: str, worst: str, space: str = "O(1)") -> dict:
    return {"best": best, "average": avg, "worst": worst, "space": space}


# ── 1. Bubble Sort ─────────────────────────────────────────────────────────────

def bubble_sort(arr: list, trace: bool = False) -> SortResult:
    """
    Repeatedly swaps adjacent elements if out of order.
    Stable | Time: O(n) best, O(n²) avg/worst | Space: O(1)
    """
    a = copy.copy(arr)
    n = len(a)
    comps = swaps = 0
    steps: list[dict] = []

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if trace:
            steps.append({"pass": i + 1, "array": copy.copy(a)})
        if not swapped:          # early exit — already sorted
            break

    return SortResult(
        algorithm="Bubble Sort",
        original=arr,
        sorted_arr=a,
        comparisons=comps,
        swaps=swaps,
        complexity=_complexity("O(n)", "O(n²)", "O(n²)"),
        steps=steps,
    )


# ── 2. Selection Sort ──────────────────────────────────────────────────────────

def selection_sort(arr: list, trace: bool = False) -> SortResult:
    """
    Finds the minimum in the unsorted portion and places it at the front.
    Unstable | Time: O(n²) all cases | Space: O(1)
    """
    a = copy.copy(arr)
    n = len(a)
    comps = swaps = 0
    steps: list[dict] = []

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
        if trace:
            steps.append({"pass": i + 1, "array": copy.copy(a), "placed": a[i]})

    return SortResult(
        algorithm="Selection Sort",
        original=arr,
        sorted_arr=a,
        comparisons=comps,
        swaps=swaps,
        complexity=_complexity("O(n²)", "O(n²)", "O(n²)"),
        steps=steps,
    )


# ── 3. Insertion Sort ──────────────────────────────────────────────────────────

def insertion_sort(arr: list, trace: bool = False) -> SortResult:
    """
    Builds a sorted subarray by inserting each element in the correct position.
    Stable | Time: O(n) best, O(n²) avg/worst | Space: O(1)
    """
    a = copy.copy(arr)
    n = len(a)
    comps = swaps = 0
    steps: list[dict] = []

    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                j -= 1
            else:
                break
        a[j + 1] = key
        if trace:
            steps.append({"inserted": key, "position": j + 1, "array": copy.copy(a)})

    return SortResult(
        algorithm="Insertion Sort",
        original=arr,
        sorted_arr=a,
        comparisons=comps,
        swaps=swaps,
        complexity=_complexity("O(n)", "O(n²)", "O(n²)"),
        steps=steps,
    )


# ── 4. Merge Sort ──────────────────────────────────────────────────────────────

def merge_sort(arr: list, trace: bool = False) -> SortResult:
    """
    Divides array in half, recursively sorts, then merges.
    Stable | Time: O(n log n) all cases | Space: O(n)
    """
    steps: list[dict] = []
    comps_ref = [0]

    def _merge(left: list, right: list) -> list:
        result: list = []
        i = j = 0
        while i < len(left) and j < len(right):
            comps_ref[0] += 1
            if left[i] <= right[j]:
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def _sort(a: list, depth: int = 0) -> list:
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left  = _sort(a[:mid],  depth + 1)
        right = _sort(a[mid:],  depth + 1)
        merged = _merge(left, right)
        if trace:
            steps.append({"depth": depth, "merged": merged})
        return merged

    sorted_arr = _sort(copy.copy(arr))
    return SortResult(
        algorithm="Merge Sort",
        original=arr,
        sorted_arr=sorted_arr,
        comparisons=comps_ref[0],
        swaps=0,
        complexity=_complexity("O(n log n)", "O(n log n)", "O(n log n)", "O(n)"),
        steps=steps,
    )


# ── 5. Quick Sort ──────────────────────────────────────────────────────────────

def quick_sort(arr: list, trace: bool = False) -> SortResult:
    """
    Picks a pivot, partitions array around it, recursively sorts partitions.
    Unstable | Time: O(n log n) avg, O(n²) worst | Space: O(log n)
    Uses median-of-three pivot selection to reduce worst-case frequency.
    """
    a = copy.copy(arr)
    steps: list[dict] = []
    comps_ref = [0]
    swaps_ref = [0]

    def _median_of_three(lo: int, hi: int) -> int:
        mid = (lo + hi) // 2
        if a[lo] > a[mid]: a[lo], a[mid] = a[mid], a[lo]
        if a[lo] > a[hi]:  a[lo], a[hi]  = a[hi],  a[lo]
        if a[mid] > a[hi]: a[mid], a[hi] = a[hi],  a[mid]
        return mid

    def _partition(lo: int, hi: int) -> int:
        pivot_idx = _median_of_three(lo, hi)
        pivot = a[pivot_idx]
        a[pivot_idx], a[hi] = a[hi], a[pivot_idx]
        i = lo - 1
        for j in range(lo, hi):
            comps_ref[0] += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                swaps_ref[0] += 1
        a[i + 1], a[hi] = a[hi], a[i + 1]
        swaps_ref[0] += 1
        return i + 1

    def _sort(lo: int, hi: int) -> None:
        if lo < hi:
            p = _partition(lo, hi)
            if trace:
                steps.append({"pivot": a[p], "partition_idx": p, "array": copy.copy(a)})
            _sort(lo, p - 1)
            _sort(p + 1, hi)

    if a:
        _sort(0, len(a) - 1)

    return SortResult(
        algorithm="Quick Sort",
        original=arr,
        sorted_arr=a,
        comparisons=comps_ref[0],
        swaps=swaps_ref[0],
        complexity=_complexity("O(n log n)", "O(n log n)", "O(n²)", "O(log n)"),
        steps=steps,
    )


# ── 6. Heap Sort ───────────────────────────────────────────────────────────────

def heap_sort(arr: list, trace: bool = False) -> SortResult:
    """
    Builds a max-heap, then repeatedly extracts the maximum.
    Unstable | Time: O(n log n) all cases | Space: O(1)
    """
    a = copy.copy(arr)
    n = len(a)
    comps_ref = [0]
    swaps_ref = [0]
    steps: list[dict] = []

    def _heapify(size: int, root: int) -> None:
        largest = root
        left    = 2 * root + 1
        right   = 2 * root + 2
        if left < size:
            comps_ref[0] += 1
            if a[left] > a[largest]:
                largest = left
        if right < size:
            comps_ref[0] += 1
            if a[right] > a[largest]:
                largest = right
        if largest != root:
            a[root], a[largest] = a[largest], a[root]
            swaps_ref[0] += 1
            _heapify(size, largest)

    # Build max-heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(n, i)

    # Extract elements
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        swaps_ref[0] += 1
        _heapify(i, 0)
        if trace:
            steps.append({"extracted": a[i], "heap_size": i, "array": copy.copy(a)})

    return SortResult(
        algorithm="Heap Sort",
        original=arr,
        sorted_arr=a,
        comparisons=comps_ref[0],
        swaps=swaps_ref[0],
        complexity=_complexity("O(n log n)", "O(n log n)", "O(n log n)"),
        steps=steps,
    )


# ── 7. Counting Sort ───────────────────────────────────────────────────────────

def counting_sort(arr: list[int], trace: bool = False) -> SortResult:
    """
    Counts occurrences of each value, then reconstructs the sorted array.
    Stable | Time: O(n+k) | Space: O(k) — integers only, k = value range
    """
    if not arr:
        return SortResult("Counting Sort", arr, [], 0, 0,
                          _complexity("O(n+k)", "O(n+k)", "O(n+k)", "O(k)"))

    mn, mx = min(arr), max(arr)
    k = mx - mn + 1
    count = [0] * k
    for x in arr:
        count[x - mn] += 1

    steps: list[dict] = []
    if trace:
        steps.append({"count_array": count[:], "offset": mn})

    # Prefix sums for stability
    for i in range(1, k):
        count[i] += count[i - 1]

    output = [0] * len(arr)
    for x in reversed(arr):
        output[count[x - mn] - 1] = x
        count[x - mn] -= 1

    if trace:
        steps.append({"output": output[:]})

    return SortResult(
        algorithm="Counting Sort",
        original=arr,
        sorted_arr=output,
        comparisons=0,
        swaps=0,
        complexity=_complexity("O(n+k)", "O(n+k)", "O(n+k)", "O(k)"),
        steps=steps,
    )


# ── 8. Radix Sort ──────────────────────────────────────────────────────────────

def radix_sort(arr: list[int], trace: bool = False) -> SortResult:
    """
    Sorts integers digit-by-digit from least significant to most significant.
    Stable | Time: O(nk) where k = number of digits | Space: O(n+k)
    Non-negative integers only.
    """
    if not arr:
        return SortResult("Radix Sort", arr, [], 0, 0,
                          _complexity("O(nk)", "O(nk)", "O(nk)", "O(n+k)"))

    a = copy.copy(arr)
    steps: list[dict] = []
    max_val = max(a)
    exp = 1

    def _counting_pass(data: list[int], exp: int) -> list[int]:
        output = [0] * len(data)
        count  = [0] * 10
        for x in data:
            count[(x // exp) % 10] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for x in reversed(data):
            idx = (x // exp) % 10
            output[count[idx] - 1] = x
            count[idx] -= 1
        return output

    while max_val // exp > 0:
        a = _counting_pass(a, exp)
        if trace:
            steps.append({"digit_place": exp, "array": copy.copy(a)})
        exp *= 10

    return SortResult(
        algorithm="Radix Sort",
        original=arr,
        sorted_arr=a,
        comparisons=0,
        swaps=0,
        complexity=_complexity("O(nk)", "O(nk)", "O(nk)", "O(n+k)"),
        steps=steps,
    )


# ── Registry ───────────────────────────────────────────────────────────────────

ALL_SORTS = {
    "bubble":    bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge":     merge_sort,
    "quick":     quick_sort,
    "heap":      heap_sort,
    "counting":  counting_sort,
    "radix":     radix_sort,
}
