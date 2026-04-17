# © 2026 Aboubacar Sidick Meite (ApollonIUGB77) — All Rights Reserved
"""
Searching Algorithms — 6 implementations with step-by-step tracing.

Algorithms:
  linear_search        O(n)         unsorted arrays
  binary_search        O(log n)     sorted arrays
  jump_search          O(√n)        sorted arrays
  interpolation_search O(log log n) avg, O(n) worst — sorted, uniformly distributed
  exponential_search   O(log n)     sorted arrays (good for unbounded/infinite)
  fibonacci_search     O(log n)     sorted arrays (only additions, no division)
"""

from __future__ import annotations
from dataclasses import dataclass, field
import math


# ── Result type ────────────────────────────────────────────────────────────────

@dataclass
class SearchResult:
    algorithm:   str
    target:      Any
    array:       list
    index:       int            # -1 if not found
    found:       bool
    comparisons: int
    steps:       list[dict] = field(default_factory=list)
    complexity:  dict = field(default_factory=dict)

    def summary(self) -> str:
        status = f"found at index {self.index}" if self.found else "not found"
        return f"[{self.algorithm}] {self.target} → {status} ({self.comparisons} comparisons)"


from typing import Any


# ── 1. Linear Search ───────────────────────────────────────────────────────────

def linear_search(arr: list, target: Any, trace: bool = False) -> SearchResult:
    """
    Scans each element sequentially until target is found or array exhausted.
    Works on unsorted arrays.  Time: O(n) | Space: O(1)
    """
    steps: list[dict] = []
    for i, val in enumerate(arr):
        if trace:
            steps.append({"index": i, "value": val, "match": val == target})
        if val == target:
            return SearchResult(
                "Linear Search", target, arr, i, True, i + 1, steps,
                {"best": "O(1)", "average": "O(n)", "worst": "O(n)", "space": "O(1)"},
            )
    return SearchResult(
        "Linear Search", target, arr, -1, False, len(arr), steps,
        {"best": "O(1)", "average": "O(n)", "worst": "O(n)", "space": "O(1)"},
    )


# ── 2. Binary Search ───────────────────────────────────────────────────────────

def binary_search(arr: list, target: Any, trace: bool = False) -> SearchResult:
    """
    Repeatedly halves the search space on a sorted array.
    Requires sorted input.  Time: O(log n) | Space: O(1)
    """
    lo, hi = 0, len(arr) - 1
    comps = 0
    steps: list[dict] = []

    while lo <= hi:
        mid = (lo + hi) // 2
        comps += 1
        if trace:
            steps.append({"low": lo, "high": hi, "mid": mid, "mid_value": arr[mid]})
        if arr[mid] == target:
            return SearchResult(
                "Binary Search", target, arr, mid, True, comps, steps,
                {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)", "space": "O(1)"},
            )
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return SearchResult(
        "Binary Search", target, arr, -1, False, comps, steps,
        {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)", "space": "O(1)"},
    )


# ── 3. Jump Search ─────────────────────────────────────────────────────────────

def jump_search(arr: list, target: Any, trace: bool = False) -> SearchResult:
    """
    Jumps √n steps ahead to find the block containing target, then linear scans.
    Requires sorted input.  Time: O(√n) | Space: O(1)
    """
    n = len(arr)
    step = int(math.isqrt(n))
    prev = 0
    comps = 0
    steps: list[dict] = []

    # Jump forward until arr[min(step,n)-1] >= target
    while step < n and arr[step - 1] < target:
        comps += 1
        if trace:
            steps.append({"phase": "jump", "block_end": step - 1, "value": arr[step - 1]})
        prev = step
        step += int(math.isqrt(n))

    # Linear scan in the identified block
    for i in range(prev, min(step, n)):
        comps += 1
        if trace:
            steps.append({"phase": "linear", "index": i, "value": arr[i], "match": arr[i] == target})
        if arr[i] == target:
            return SearchResult(
                "Jump Search", target, arr, i, True, comps, steps,
                {"best": "O(1)", "average": "O(√n)", "worst": "O(√n)", "space": "O(1)"},
            )

    return SearchResult(
        "Jump Search", target, arr, -1, False, comps, steps,
        {"best": "O(1)", "average": "O(√n)", "worst": "O(√n)", "space": "O(1)"},
    )


# ── 4. Interpolation Search ────────────────────────────────────────────────────

def interpolation_search(arr: list, target: Any, trace: bool = False) -> SearchResult:
    """
    Estimates the position of target using linear interpolation (like how humans search a phone book).
    Best for uniformly distributed sorted data.
    Time: O(log log n) avg, O(n) worst | Space: O(1)
    """
    lo, hi = 0, len(arr) - 1
    comps = 0
    steps: list[dict] = []

    while lo <= hi and arr[lo] <= target <= arr[hi]:
        if arr[hi] == arr[lo]:
            if arr[lo] == target:
                return SearchResult(
                    "Interpolation Search", target, arr, lo, True, comps + 1, steps,
                    {"best": "O(1)", "average": "O(log log n)", "worst": "O(n)", "space": "O(1)"},
                )
            break

        # Probe position
        pos = lo + int(((target - arr[lo]) / (arr[hi] - arr[lo])) * (hi - lo))
        comps += 1
        if trace:
            steps.append({"low": lo, "high": hi, "probe": pos, "probe_value": arr[pos]})

        if arr[pos] == target:
            return SearchResult(
                "Interpolation Search", target, arr, pos, True, comps, steps,
                {"best": "O(1)", "average": "O(log log n)", "worst": "O(n)", "space": "O(1)"},
            )
        elif arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1

    return SearchResult(
        "Interpolation Search", target, arr, -1, False, comps, steps,
        {"best": "O(1)", "average": "O(log log n)", "worst": "O(n)", "space": "O(1)"},
    )


# ── 5. Exponential Search ──────────────────────────────────────────────────────

def exponential_search(arr: list, target: Any, trace: bool = False) -> SearchResult:
    """
    Doubles the range exponentially to find the block, then binary searches it.
    Great for unbounded/infinite sorted arrays.
    Time: O(log n) | Space: O(1)
    """
    n = len(arr)
    if not n:
        return SearchResult("Exponential Search", target, arr, -1, False, 0, [],
                            {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)", "space": "O(1)"})

    if arr[0] == target:
        return SearchResult("Exponential Search", target, arr, 0, True, 1, [],
                            {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)", "space": "O(1)"})

    i = 1
    comps = 1
    steps: list[dict] = []
    while i < n and arr[i] <= target:
        comps += 1
        if trace:
            steps.append({"phase": "exponential", "i": i, "value": arr[i]})
        i *= 2

    # Binary search in the identified range
    lo = i // 2
    hi = min(i, n - 1)
    if trace:
        steps.append({"phase": "binary_search_range", "low": lo, "high": hi})

    while lo <= hi:
        mid = (lo + hi) // 2
        comps += 1
        if trace:
            steps.append({"phase": "binary", "mid": mid, "value": arr[mid]})
        if arr[mid] == target:
            return SearchResult(
                "Exponential Search", target, arr, mid, True, comps, steps,
                {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)", "space": "O(1)"},
            )
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return SearchResult(
        "Exponential Search", target, arr, -1, False, comps, steps,
        {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)", "space": "O(1)"},
    )


# ── 6. Fibonacci Search ────────────────────────────────────────────────────────

def fibonacci_search(arr: list, target: Any, trace: bool = False) -> SearchResult:
    """
    Uses Fibonacci numbers to divide the array — no division, only additions.
    Useful in systems where division is expensive.
    Time: O(log n) | Space: O(1)
    """
    n = len(arr)
    fib_m2 = 0   # (m-2)th Fibonacci
    fib_m1 = 1   # (m-1)th Fibonacci
    fib_m  = fib_m1 + fib_m2

    while fib_m < n:
        fib_m2 = fib_m1
        fib_m1 = fib_m
        fib_m  = fib_m1 + fib_m2

    offset = -1
    comps  = 0
    steps: list[dict] = []

    while fib_m > 1:
        i = min(offset + fib_m2, n - 1)
        comps += 1
        if trace:
            steps.append({"fib_m": fib_m, "fib_m2": fib_m2, "index": i, "value": arr[i]})

        if arr[i] < target:
            fib_m  = fib_m1
            fib_m1 = fib_m2
            fib_m2 = fib_m - fib_m1
            offset = i
        elif arr[i] > target:
            fib_m  = fib_m2
            fib_m1 = fib_m1 - fib_m2
            fib_m2 = fib_m - fib_m1
        else:
            return SearchResult(
                "Fibonacci Search", target, arr, i, True, comps, steps,
                {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)", "space": "O(1)"},
            )

    if fib_m1 and offset + 1 < n and arr[offset + 1] == target:
        comps += 1
        return SearchResult(
            "Fibonacci Search", target, arr, offset + 1, True, comps, steps,
            {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)", "space": "O(1)"},
        )

    return SearchResult(
        "Fibonacci Search", target, arr, -1, False, comps, steps,
        {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)", "space": "O(1)"},
    )


# ── Registry ───────────────────────────────────────────────────────────────────

ALL_SEARCHES = {
    "linear":        linear_search,
    "binary":        binary_search,
    "jump":          jump_search,
    "interpolation": interpolation_search,
    "exponential":   exponential_search,
    "fibonacci":     fibonacci_search,
}
